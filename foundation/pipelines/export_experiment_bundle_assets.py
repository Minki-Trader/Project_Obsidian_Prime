#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import joblib
import numpy as np
import onnx
import pandas as pd
from skl2onnx import convert_sklearn
from skl2onnx.common.data_types import FloatTensorType

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from foundation.features.catalog import FEATURE_ORDER
from foundation.pipelines.build_experiment_bundle import (
    assemble_bundle,
    build_failure_report,
    build_success_summary,
    write_json,
)
from foundation.pipelines.experiment_bundle_models import (
    DataSnapshot,
    LabelConfig,
    OutputSchema,
    RuleStack,
    RuntimeSnapshot,
)
from foundation.pipelines.experiment_bundle_request_models import (
    ArtifactRequest,
    BundleBuildRequest,
    CompatibilityRequest,
    FeatureSchemaRequest,
    IdentityRequest,
    SmokeArraySpec,
    SmokeTestRequest,
)
from foundation.pipelines.prepare_experiment_bundle_request import (
    DEFAULT_REQUIRED_CAPABILITIES,
    DEFAULT_SPLIT_BOUNDARIES,
    build_default_external_inputs,
    build_rule_stack_from_selection,
    portable_path,
    read_json,
    resolve_path,
)


UTC = timezone.utc
EXPECTED_CLASS_ORDER = [0, 1, 2]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Export model artifacts and build bundle files for an experiment run.")
    parser.add_argument("--run-dir", required=True, help="Run directory containing model.joblib and config.json")
    parser.add_argument("--experiment-id", required=True, help="Logical experiment id")
    parser.add_argument("--stage-id", required=True, help="Bundle stage id")
    parser.add_argument("--output-dir", help="Output directory. Defaults to <run-dir>/bundle_export")
    parser.add_argument("--stage-name", default="ea_optimize", help="Bundle stage name")
    parser.add_argument("--bundle-version", default="1.0.0", help="Bundle version")
    parser.add_argument("--created-by", default="python_orchestrator", help="Bundle creator tag")
    parser.add_argument("--config-json", help="Optional config.json override. Defaults to <run-dir>/config.json")
    parser.add_argument("--dataset-path", help="Optional dataset path override")
    parser.add_argument("--selection-json", help="Selection JSON used to derive the rule stack")
    parser.add_argument(
        "--logic-family",
        choices=["threshold_only", "margin_only", "prob_diff_only", "custom"],
        help="Logic family for auto rule-stack recovery",
    )
    parser.add_argument("--selection-key", help="Optional selection block override")
    parser.add_argument("--rule-stack-json", help="Explicit rule_stack JSON for custom/advanced logic")
    parser.add_argument("--smoke-split", default="test", help="Preferred split to source the smoke sample from")
    parser.add_argument("--smoke-row-index", type=int, default=0, help="Row index within the selected smoke split")
    parser.add_argument("--max-hold-bars", type=int, default=3, help="Exit max_hold_bars when auto-building rule stacks")
    parser.add_argument(
        "--sizing-mode",
        default="fixed_lot",
        choices=["fixed_lot", "risk_pct"],
        help="Runtime sizing mode written into the bundle runtime snapshot.",
    )
    parser.add_argument("--fixed-lot", type=float, default=0.1, help="Fallback fixed lot stored in the runtime snapshot.")
    parser.add_argument("--risk-pct", type=float, help="Percent of capital to risk per trade when using risk_pct sizing.")
    parser.add_argument(
        "--capital-base",
        default="balance",
        choices=["balance", "equity"],
        help="Capital base for risk_pct sizing.",
    )
    parser.add_argument(
        "--stop-model",
        choices=["atr"],
        help="Stop model used for risk_pct sizing. Required when --sizing-mode=risk_pct.",
    )
    parser.add_argument(
        "--stop-execution-mode",
        default="ea_managed",
        choices=["ea_managed", "broker_native"],
        help="How the initial stop should be enforced when using risk_pct sizing.",
    )
    parser.add_argument(
        "--stop-policy",
        default="fixed",
        choices=["fixed", "regime_bucket", "direction_split"],
        help="How ATR multiplier should be chosen for risk_pct sizing.",
    )
    parser.add_argument("--stop-atr-period", type=int, default=14, help="ATR period for ATR-based stop sizing.")
    parser.add_argument("--stop-atr-mult", type=float, help="ATR multiplier for ATR-based stop sizing.")
    parser.add_argument("--stop-long-atr-mult", type=float, help="Long-side ATR multiplier for direction_split policy.")
    parser.add_argument("--stop-short-atr-mult", type=float, help="Short-side ATR multiplier for direction_split policy.")
    parser.add_argument("--stop-low-vol-threshold", type=float, help="ATR14/ATR50 threshold for low-vol regime.")
    parser.add_argument("--stop-high-vol-threshold", type=float, help="ATR14/ATR50 threshold for high-vol regime.")
    parser.add_argument("--stop-low-atr-mult", type=float, help="Low-vol ATR multiplier for regime_bucket policy.")
    parser.add_argument("--stop-mid-atr-mult", type=float, help="Mid-vol ATR multiplier for regime_bucket policy.")
    parser.add_argument("--stop-high-atr-mult", type=float, help="High-vol ATR multiplier for regime_bucket policy.")
    parser.add_argument("--build-bundle", action="store_true", help="Build final experiment_bundle.json after export")
    return parser


def utc_now_iso() -> str:
    return datetime.now(tz=UTC).isoformat()


def infer_feature_names(model: Any) -> list[str]:
    if hasattr(model, "feature_names_in_"):
        return [str(name) for name in model.feature_names_in_]

    if hasattr(model, "named_steps"):
        for step in reversed(model.named_steps.values()):
            if hasattr(step, "feature_names_in_"):
                return [str(name) for name in step.feature_names_in_]
            if hasattr(step, "feature_name_"):
                return [str(name) for name in step.feature_name_]

    if hasattr(model, "feature_name_"):
        return [str(name) for name in model.feature_name_]

    if hasattr(model, "booster_") and hasattr(model.booster_, "feature_name"):
        return [str(name) for name in model.booster_.feature_name()]

    return list(FEATURE_ORDER)


def ensure_class_order(model: Any) -> None:
    classes = getattr(model, "classes_", None)
    if classes is None and hasattr(model, "named_steps"):
        for step in reversed(model.named_steps.values()):
            classes = getattr(step, "classes_", None)
            if classes is not None:
                break
    if classes is None:
        raise ValueError("model has no classes_ attribute; cannot verify probs3 class order")

    classes_list = [int(value) for value in np.asarray(classes).tolist()]
    if classes_list != EXPECTED_CLASS_ORDER:
        raise ValueError(f"expected classifier classes {EXPECTED_CLASS_ORDER}, got {classes_list}")


def export_sklearn_probonly_onnx(
    model: Any,
    *,
    feature_count: int,
    output_path: Path,
) -> None:
    if model.__class__.__module__.startswith("catboost."):
        model.save_model(str(output_path), format="onnx")
        onnx_model = onnx.load(str(output_path))
    elif model.__class__.__module__.startswith("xgboost."):
        try:
            from onnxmltools import convert_xgboost
            from onnxmltools.convert.common.data_types import FloatTensorType as OnnxMlFloatTensorType
        except ModuleNotFoundError as exc:
            raise ModuleNotFoundError(
                "XGBoost ONNX export requires 'onnxmltools'. "
                "Install it with `python -m pip install onnxmltools`."
            ) from exc

        onnx_model = convert_xgboost(
            model,
            initial_types=[("input", OnnxMlFloatTensorType([None, feature_count]))],
            target_opset=13,
        )
    elif model.__class__.__module__.startswith("lightgbm."):
        try:
            from onnxmltools import convert_lightgbm
            from onnxmltools.convert.common.data_types import FloatTensorType as OnnxMlFloatTensorType
        except ModuleNotFoundError as exc:
            raise ModuleNotFoundError(
                "LightGBM ONNX export requires 'onnxmltools'. "
                "Install it with `python -m pip install onnxmltools`."
            ) from exc

        onnx_model = convert_lightgbm(
            model,
            initial_types=[("input", OnnxMlFloatTensorType([None, feature_count]))],
            target_opset=13,
            zipmap=False,
        )
    else:
        onnx_model = convert_sklearn(
            model,
            initial_types=[("input", FloatTensorType([None, feature_count]))],
            options={id(model): {"zipmap": False}},
            target_opset=13,
        )

    outputs = list(onnx_model.graph.output)
    if not outputs:
        raise ValueError("exported ONNX model has no outputs")

    selected_output = next((item for item in outputs if item.name == "probabilities"), outputs[-1])
    trimmed_output = onnx.ValueInfoProto()
    trimmed_output.CopyFrom(selected_output)
    del onnx_model.graph.output[:]
    onnx_model.graph.output.append(trimmed_output)
    onnx.save(onnx_model, output_path)


def select_smoke_frame(
    dataset: pd.DataFrame,
    *,
    preferred_split: str,
    row_index: int,
) -> pd.DataFrame:
    split_candidates = [preferred_split, "test", "valid", "train"]
    smoke_df = pd.DataFrame()
    for split_name in split_candidates:
        candidate = dataset[dataset["split"].eq(split_name)]
        if not candidate.empty:
            smoke_df = candidate
            break
    if smoke_df.empty:
        raise ValueError("dataset does not contain any rows for smoke sample selection")
    if row_index < 0 or row_index >= len(smoke_df):
        raise IndexError(f"smoke_row_index={row_index} is out of range for split with {len(smoke_df)} rows")
    return smoke_df.iloc[[row_index]].copy()


def build_split_counts(dataset: pd.DataFrame) -> dict[str, int]:
    counts = dataset["split"].value_counts(dropna=False).to_dict()
    return {str(key): int(value) for key, value in counts.items()}


def resolve_rule_stack(
    args: argparse.Namespace,
    *,
    workspace_dir: Path,
) -> RuleStack:
    if args.rule_stack_json:
        payload = read_json(resolve_path(args.rule_stack_json, base_dir=workspace_dir))
        return RuleStack.model_validate(payload)

    if not args.selection_json or not args.logic_family:
        raise ValueError("either --rule-stack-json or (--selection-json and --logic-family) is required")

    selection_json = resolve_path(args.selection_json, base_dir=workspace_dir)
    return build_rule_stack_from_selection(
        selection_json=selection_json,
        logic_family=args.logic_family,
        selection_key=args.selection_key,
        max_hold_bars=args.max_hold_bars,
    )


def run_export_bundle_assets(args: argparse.Namespace) -> dict[str, str]:
    run_dir = resolve_path(args.run_dir, base_dir=ROOT_DIR)
    output_dir = resolve_path(args.output_dir, base_dir=ROOT_DIR) if args.output_dir else (run_dir / "bundle_export")
    output_dir.mkdir(parents=True, exist_ok=True)
    artifacts_dir = output_dir / "artifacts"
    artifacts_dir.mkdir(parents=True, exist_ok=True)

    config_path = resolve_path(args.config_json, base_dir=ROOT_DIR) if args.config_json else (run_dir / "config.json")
    if not config_path.exists():
        raise FileNotFoundError(f"missing config.json: {config_path}")

    model_path = run_dir / "model.joblib"
    if not model_path.exists():
        raise FileNotFoundError(f"missing model.joblib: {model_path}")

    config = read_json(config_path)
    if not isinstance(config, dict):
        raise ValueError("run config must be a JSON object")

    dataset_path = resolve_path(args.dataset_path, base_dir=ROOT_DIR) if args.dataset_path else resolve_path(
        str(config["dataset_path"]),
        base_dir=ROOT_DIR,
    )
    if not dataset_path.exists():
        raise FileNotFoundError(f"missing dataset path: {dataset_path}")

    model = joblib.load(model_path)
    ensure_class_order(model)
    feature_names = infer_feature_names(model)

    if args.sizing_mode == "fixed_lot":
        if args.fixed_lot <= 0.0:
            raise ValueError("--fixed-lot must be positive when --sizing-mode=fixed_lot")
    elif args.sizing_mode == "risk_pct":
        if args.risk_pct is None or args.risk_pct <= 0.0:
            raise ValueError("--risk-pct must be positive when --sizing-mode=risk_pct")
        if args.stop_model != "atr":
            raise ValueError("--stop-model=atr is required when --sizing-mode=risk_pct")
        if args.stop_execution_mode not in {"ea_managed", "broker_native"}:
            raise ValueError("--stop-execution-mode must be ea_managed or broker_native")
        if args.stop_policy not in {"fixed", "regime_bucket", "direction_split"}:
            raise ValueError("--stop-policy must be fixed, regime_bucket, or direction_split")
        if args.stop_atr_period <= 0:
            raise ValueError("--stop-atr-period must be positive when --sizing-mode=risk_pct")
        if args.stop_policy == "fixed":
            if args.stop_atr_mult is None or args.stop_atr_mult <= 0.0:
                raise ValueError("--stop-atr-mult must be positive for fixed stop policy")
        elif args.stop_policy == "direction_split":
            if args.stop_long_atr_mult is None or args.stop_long_atr_mult <= 0.0:
                raise ValueError("--stop-long-atr-mult must be positive for direction_split stop policy")
            if args.stop_short_atr_mult is None or args.stop_short_atr_mult <= 0.0:
                raise ValueError("--stop-short-atr-mult must be positive for direction_split stop policy")
        elif args.stop_policy == "regime_bucket":
            if args.stop_low_vol_threshold is None or args.stop_high_vol_threshold is None:
                raise ValueError("--stop-low-vol-threshold and --stop-high-vol-threshold are required for regime_bucket stop policy")
            if args.stop_low_vol_threshold >= args.stop_high_vol_threshold:
                raise ValueError("--stop-low-vol-threshold must be less than --stop-high-vol-threshold")
            if args.stop_low_atr_mult is None or args.stop_low_atr_mult <= 0.0:
                raise ValueError("--stop-low-atr-mult must be positive for regime_bucket stop policy")
            if args.stop_mid_atr_mult is None or args.stop_mid_atr_mult <= 0.0:
                raise ValueError("--stop-mid-atr-mult must be positive for regime_bucket stop policy")
            if args.stop_high_atr_mult is None or args.stop_high_atr_mult <= 0.0:
                raise ValueError("--stop-high-atr-mult must be positive for regime_bucket stop policy")

    dataset = pd.read_parquet(dataset_path)
    missing_columns = [name for name in feature_names if name not in dataset.columns]
    if missing_columns:
        raise ValueError(f"dataset is missing model feature columns: {missing_columns[:10]}")

    label_config = LabelConfig(
        label_type="three_class",
        horizon_bars=int(config["horizon_bars"]),
        band=float(config["band"]),
    )
    split_counts = build_split_counts(dataset)
    smoke_frame = select_smoke_frame(dataset, preferred_split=args.smoke_split, row_index=args.smoke_row_index)
    smoke_input = smoke_frame[feature_names].astype(np.float32)
    smoke_output = np.asarray(model.predict_proba(smoke_input), dtype=np.float32).reshape(-1)
    if smoke_output.size != 3:
        raise ValueError(f"predict_proba smoke output must have size 3, got {smoke_output.size}")

    onnx_path = artifacts_dir / "model_probonly.onnx"
    feature_schema_path = artifacts_dir / "feature_schema.json"
    smoke_input_path = artifacts_dir / "smoke_input.json"
    smoke_output_path = artifacts_dir / "smoke_output.json"
    export_summary_path = output_dir / "export_summary.json"
    request_path = output_dir / "bundle_request.json"
    request_summary_path = output_dir / "bundle_request_build_summary.json"
    bundle_path = output_dir / "experiment_bundle.json"
    bundle_summary_path = output_dir / "bundle_build_summary.json"
    failure_path = output_dir / "bundle_build_failure_report.json"

    export_sklearn_probonly_onnx(model, feature_count=len(feature_names), output_path=onnx_path)
    write_json(feature_schema_path, {"feature_names": feature_names})
    write_json(smoke_input_path, smoke_input.iloc[0].astype(float).tolist())
    write_json(
        smoke_output_path,
        {
            "p_short": float(smoke_output[0]),
            "p_flat": float(smoke_output[1]),
            "p_long": float(smoke_output[2]),
        },
    )

    export_summary = {
        "status": "success",
        "generated_at_utc": utc_now_iso(),
        "run_dir": str(run_dir.as_posix()),
        "config_path": str(config_path.as_posix()),
        "dataset_path": str(dataset_path.as_posix()),
        "model_path": str(model_path.as_posix()),
        "onnx_path": str(onnx_path.as_posix()),
        "feature_schema_path": str(feature_schema_path.as_posix()),
        "feature_count": len(feature_names),
        "smoke_split": str(smoke_frame.iloc[0]["split"]),
        "smoke_timestamp_utc": smoke_frame.iloc[0]["timestamp"].isoformat() if "timestamp" in smoke_frame.columns else None,
    }
    write_json(export_summary_path, export_summary)

    request = BundleBuildRequest(
        identity=IdentityRequest(
            experiment_id=args.experiment_id,
            stage_id=args.stage_id,
            stage_name=args.stage_name,
            bundle_version=args.bundle_version,
            created_by=args.created_by,
            created_at_utc=utc_now_iso(),
        ),
        artifacts=[
            ArtifactRequest(
                artifact_id="art_onnx_model",
                role="onnx_model",
                path=portable_path(onnx_path, base_dir=output_dir),
                format="onnx",
                required=True,
            ),
            ArtifactRequest(
                artifact_id="art_feature_schema",
                role="feature_schema",
                path=portable_path(feature_schema_path, base_dir=output_dir),
                format="json",
                required=True,
            ),
            ArtifactRequest(
                artifact_id="art_dataset",
                role="dataset",
                path=portable_path(dataset_path, base_dir=output_dir),
                format=dataset_path.suffix.lstrip(".") or "parquet",
                required=False,
            ),
            ArtifactRequest(
                artifact_id="art_model_joblib",
                role="trained_model_joblib",
                path=portable_path(model_path, base_dir=output_dir),
                format="joblib",
                required=False,
            ),
            ArtifactRequest(
                artifact_id="art_run_config",
                role="run_config",
                path=portable_path(config_path, base_dir=output_dir),
                format="json",
                required=False,
            ),
        ],
        feature_schema=FeatureSchemaRequest(
            feature_count=len(feature_names),
            order_version=args.experiment_id,
            feature_schema_artifact_id="art_feature_schema",
        ),
        output_schema=OutputSchema(schema_type="probs3", output_order=["p_short", "p_flat", "p_long"]),
        external_inputs=build_default_external_inputs(),
        data_snapshot=DataSnapshot(
            dataset_id=dataset_path.stem,
            source_artifact_ids=["art_feature_schema", "art_dataset", "art_run_config"],
            split_boundaries=DEFAULT_SPLIT_BOUNDARIES,
            label_config=label_config,
            split_counts=split_counts,
            extra={
                "run_name": str(config.get("run_name", run_dir.name)),
                "run_dir": portable_path(run_dir, base_dir=output_dir),
            },
        ),
        runtime_snapshot=RuntimeSnapshot(
            symbol="US100",
            timeframe="M5",
            tester_model="real_ticks",
            deposit=500,
            currency="USD",
            leverage=100,
            sizing_mode=args.sizing_mode,
            fixed_lot=args.fixed_lot,
            risk_pct=args.risk_pct,
            capital_base=args.capital_base if args.sizing_mode == "risk_pct" else None,
            stop_model=args.stop_model if args.sizing_mode == "risk_pct" else None,
            stop_execution_mode=args.stop_execution_mode if args.sizing_mode == "risk_pct" else None,
            stop_policy=args.stop_policy if args.sizing_mode == "risk_pct" else None,
            stop_atr_period=args.stop_atr_period if args.sizing_mode == "risk_pct" else None,
            stop_atr_mult=args.stop_atr_mult if args.sizing_mode == "risk_pct" else None,
            stop_long_atr_mult=args.stop_long_atr_mult if args.sizing_mode == "risk_pct" else None,
            stop_short_atr_mult=args.stop_short_atr_mult if args.sizing_mode == "risk_pct" else None,
            stop_low_vol_threshold=args.stop_low_vol_threshold if args.sizing_mode == "risk_pct" else None,
            stop_high_vol_threshold=args.stop_high_vol_threshold if args.sizing_mode == "risk_pct" else None,
            stop_low_atr_mult=args.stop_low_atr_mult if args.sizing_mode == "risk_pct" else None,
            stop_mid_atr_mult=args.stop_mid_atr_mult if args.sizing_mode == "risk_pct" else None,
            stop_high_atr_mult=args.stop_high_atr_mult if args.sizing_mode == "risk_pct" else None,
            entry_timing="next_tick_after_closed_bar_signal",
            max_concurrent_positions=1,
            cost_behavior="broker_native",
        ),
        rule_stack=resolve_rule_stack(args, workspace_dir=ROOT_DIR),
        compatibility=CompatibilityRequest(required_ea_capabilities=DEFAULT_REQUIRED_CAPABILITIES),
        smoke_test=SmokeTestRequest(
            onnx_artifact_id="art_onnx_model",
            input=SmokeArraySpec(path=portable_path(smoke_input_path, base_dir=output_dir), format="json"),
            expected_output=SmokeArraySpec(path=portable_path(smoke_output_path, base_dir=output_dir), format="json"),
        ),
    )
    request_path.write_text(request.model_dump_json(indent=2), encoding="utf-8")
    write_json(
        request_summary_path,
        {
            "status": "success",
            "generated_at_utc": utc_now_iso(),
            "request_path": str(request_path.as_posix()),
            "feature_count": len(feature_names),
            "artifact_count": len(request.artifacts),
        },
    )

    if args.build_bundle:
        try:
            bundle, smoke_summary = assemble_bundle(request, request_dir=output_dir)
            if failure_path.exists():
                failure_path.unlink()
            bundle_path.write_text(bundle.to_json(indent=2), encoding="utf-8")
            write_json(
                bundle_summary_path,
                build_success_summary(
                    bundle,
                    bundle_path=bundle_path,
                    summary_path=bundle_summary_path,
                    smoke_summary=smoke_summary,
                ),
            )
        except Exception as error:  # noqa: BLE001
            for stale_path in (bundle_path, bundle_summary_path):
                if stale_path.exists():
                    stale_path.unlink()
            write_json(
                failure_path,
                build_failure_report(
                    request_json=request_path,
                    output_dir=output_dir,
                    error=error,
                ),
            )
            raise

    return {
        "run_dir": str(run_dir.as_posix()),
        "output_dir": str(output_dir.as_posix()),
        "export_summary_path": str(export_summary_path.as_posix()),
        "request_path": str(request_path.as_posix()),
        "request_summary_path": str(request_summary_path.as_posix()),
        "bundle_path": str(bundle_path.as_posix()) if args.build_bundle else "",
        "bundle_summary_path": str(bundle_summary_path.as_posix()) if args.build_bundle else "",
    }


def main() -> int:
    args = build_parser().parse_args()
    result = run_export_bundle_assets(args)
    print(f"[done] export_summary={result['export_summary_path']}")
    print(f"[done] request={result['request_path']}")
    if result["bundle_path"]:
        print(f"[done] bundle={result['bundle_path']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
