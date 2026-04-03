#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from foundation.features.catalog import FEATURE_ORDER
from foundation.pipelines.experiment_bundle_models import (
    CapabilityRequirement,
    DataSnapshot,
    ExternalInputRequirement,
    LabelConfig,
    OutputSchema,
    RuleDefinition,
    RuleStack,
    RuntimeSnapshot,
    SplitBoundaries,
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


UTC = timezone.utc
DEFAULT_SPLIT_BOUNDARIES = SplitBoundaries(
    train_start_utc="2022-09-01T00:00:00Z",
    train_end_utc_exclusive="2025-01-01T00:00:00Z",
    validation_end_utc_exclusive="2025-10-01T00:00:00Z",
    test_end_utc_exclusive="2026-03-01T00:00:00Z",
)
DEFAULT_OUTPUT_SCHEMA = OutputSchema(schema_type="probs3", output_order=["p_short", "p_flat", "p_long"])
DEFAULT_REQUIRED_CAPABILITIES = [
    CapabilityRequirement(name="output.probs3", min_version="1.0.0"),
    CapabilityRequirement(name="runtime.real_ticks", min_version="1.0.0"),
    CapabilityRequirement(name="logic.rule_stack", min_version="1.0.0"),
    CapabilityRequirement(name="external_inputs.exact_closed_bar_match", min_version="1.0.0"),
]
DEFAULT_EXTERNAL_INPUT_SPECS = [
    ("ext_vix", "VIX", "macro_external"),
    ("ext_us10yr", "US10YR", "macro_external"),
    ("ext_usdx", "USDX", "macro_external"),
    ("ext_aapl", "AAPL.xnas", "breadth_constituent"),
    ("ext_amzn", "AMZN.xnas", "breadth_constituent"),
    ("ext_amd", "AMD.xnas", "breadth_constituent"),
    ("ext_googl", "GOOGL.xnas", "breadth_constituent"),
    ("ext_meta", "META.xnas", "breadth_constituent"),
    ("ext_msft", "MSFT.xnas", "breadth_constituent"),
    ("ext_nvda", "NVDA.xnas", "breadth_constituent"),
    ("ext_tsla", "TSLA.xnas", "breadth_constituent"),
]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Prepare bundle_request.json from experiment metadata and selection artifacts.")
    parser.add_argument("--experiment-id", required=True, help="Logical experiment id")
    parser.add_argument("--stage-id", required=True, help="Stage id for the bundle identity")
    parser.add_argument("--output-dir", required=True, help="Directory for bundle_request.json and generated helper artifacts")
    parser.add_argument("--stage-name", default="ea_optimize", help="Stage name for the bundle identity")
    parser.add_argument("--bundle-version", default="1.0.0", help="Bundle version")
    parser.add_argument("--created-by", default="python_orchestrator", help="Bundle creator tag")
    parser.add_argument("--onnx-path", required=True, help="Exported ONNX model path")
    parser.add_argument("--smoke-input-path", required=True, help="Smoke-test input array path")
    parser.add_argument("--smoke-output-path", required=True, help="Smoke-test expected output path")
    parser.add_argument("--smoke-input-format", choices=["json", "npy"], default="json")
    parser.add_argument("--smoke-output-format", choices=["json", "npy"], default="json")
    parser.add_argument("--smoke-input-key", help="Optional JSON key for smoke input")
    parser.add_argument("--smoke-output-key", help="Optional JSON key for smoke output")
    parser.add_argument("--feature-schema-path", help="Existing feature schema artifact path")
    parser.add_argument("--feature-names-json", help="JSON file containing feature names/order")
    parser.add_argument("--use-catalog-feature-order", action="store_true", help="Generate feature schema from foundation.features.catalog.FEATURE_ORDER")
    parser.add_argument("--order-version", help="Feature order version tag; defaults to experiment id")
    parser.add_argument("--dataset-path", help="Optional dataset/parquet path to register as a source artifact")
    parser.add_argument("--dataset-id", help="Dataset id; defaults to dataset path stem or experiment id")
    parser.add_argument("--model-config-json", help="Optional model config JSON to source dataset_path / horizon_bars / band")
    parser.add_argument("--horizon-bars", type=int, help="Label horizon bars; overrides model-config-json")
    parser.add_argument("--band", type=float, help="Label band; overrides model-config-json")
    parser.add_argument("--split-counts-json", help="Optional JSON object of split counts")
    parser.add_argument("--selection-json", help="Stage selection JSON for Stage02/03/04 auto rule-stack construction")
    parser.add_argument(
        "--logic-family",
        choices=["threshold_only", "margin_only", "prob_diff_only", "custom"],
        help="Rule-stack family. Required unless --rule-stack-json is supplied.",
    )
    parser.add_argument("--selection-key", help="Override the selection object key inside selection JSON")
    parser.add_argument("--rule-stack-json", help="Explicit rule_stack JSON path for custom/advanced logic")
    parser.add_argument("--max-hold-bars", type=int, default=3, help="Exit rule max hold bars")
    parser.add_argument("--external-inputs-json", help="Optional explicit external_inputs JSON path")
    parser.add_argument("--extra-artifacts-json", help="Optional JSON list of extra artifact definitions")
    parser.add_argument(
        "--source-artifact-id",
        action="append",
        default=[],
        help="Additional artifact_id values to include in data_snapshot.source_artifact_ids",
    )
    return parser


def utc_now_iso() -> str:
    return datetime.now(tz=UTC).isoformat()


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def resolve_path(value: str, *, base_dir: Path) -> Path:
    path = Path(value)
    if not path.is_absolute():
        path = (base_dir / path).resolve()
    return path


def portable_path(path: Path, *, base_dir: Path) -> str:
    try:
        return path.resolve().relative_to(base_dir.resolve()).as_posix()
    except ValueError:
        return path.resolve().as_posix()


def extract_feature_names(payload: Any) -> list[str]:
    if isinstance(payload, list):
        if all(isinstance(item, str) for item in payload):
            return [str(item) for item in payload]
        if all(isinstance(item, dict) and "name" in item for item in payload):
            return [str(item["name"]) for item in payload]

    if isinstance(payload, dict):
        for key in ("feature_names", "feature_order"):
            value = payload.get(key)
            if isinstance(value, list) and all(isinstance(item, str) for item in value):
                return [str(item) for item in value]
        features = payload.get("features")
        if isinstance(features, list):
            if all(isinstance(item, str) for item in features):
                return [str(item) for item in features]
            if all(isinstance(item, dict) and "name" in item for item in features):
                return [str(item["name"]) for item in features]

    raise ValueError("could not extract feature names from supplied JSON")


def build_default_external_inputs() -> list[ExternalInputRequirement]:
    return [
        ExternalInputRequirement(
            input_id=input_id,
            symbol=symbol,
            timeframe="M5",
            required=True,
            alignment_rule="exact_closed_bar_match",
            role=role,
        )
        for input_id, symbol, role in DEFAULT_EXTERNAL_INPUT_SPECS
    ]


def load_external_inputs(path: Path | None) -> list[ExternalInputRequirement]:
    if path is None:
        return build_default_external_inputs()

    payload = read_json(path)
    if not isinstance(payload, list):
        raise ValueError("external_inputs JSON must be a list")
    return [ExternalInputRequirement.model_validate(item) for item in payload]


def build_feature_schema_artifact(
    args: argparse.Namespace,
    *,
    output_dir: Path,
    workspace_dir: Path,
) -> tuple[ArtifactRequest, FeatureSchemaRequest]:
    order_version = args.order_version or args.experiment_id

    if args.feature_schema_path:
        feature_schema_path = resolve_path(args.feature_schema_path, base_dir=workspace_dir)
        if not feature_schema_path.exists():
            raise FileNotFoundError(f"missing feature schema artifact: {feature_schema_path}")
        feature_count = None
        try:
            feature_count = len(extract_feature_names(read_json(feature_schema_path)))
        except Exception:  # noqa: BLE001
            feature_count = None

        return (
            ArtifactRequest(
                artifact_id="art_feature_schema",
                role="feature_schema",
                path=portable_path(feature_schema_path, base_dir=output_dir),
                format=feature_schema_path.suffix.lstrip(".") or "json",
                required=True,
            ),
            FeatureSchemaRequest(
                feature_count=feature_count,
                order_version=order_version,
                feature_schema_artifact_id="art_feature_schema",
            ),
        )

    if args.feature_names_json:
        source_payload = read_json(resolve_path(args.feature_names_json, base_dir=workspace_dir))
        feature_names = extract_feature_names(source_payload)
    elif args.use_catalog_feature_order:
        feature_names = list(FEATURE_ORDER)
    else:
        raise ValueError(
            "one of --feature-schema-path, --feature-names-json, or --use-catalog-feature-order is required"
        )

    generated_artifacts_dir = output_dir / "artifacts"
    generated_artifacts_dir.mkdir(parents=True, exist_ok=True)
    generated_schema_path = generated_artifacts_dir / "feature_schema.json"
    write_json(generated_schema_path, {"feature_names": feature_names})

    return (
        ArtifactRequest(
            artifact_id="art_feature_schema",
            role="feature_schema",
            path=portable_path(generated_schema_path, base_dir=output_dir),
            format="json",
            required=True,
        ),
        FeatureSchemaRequest(
            feature_count=len(feature_names),
            order_version=order_version,
            feature_schema_artifact_id="art_feature_schema",
        ),
    )


def build_dataset_artifact(
    *,
    dataset_path: Path | None,
    output_dir: Path,
) -> ArtifactRequest | None:
    if dataset_path is None:
        return None
    if not dataset_path.exists():
        raise FileNotFoundError(f"missing dataset artifact: {dataset_path}")
    return ArtifactRequest(
        artifact_id="art_dataset",
        role="dataset",
        path=portable_path(dataset_path, base_dir=output_dir),
        format=dataset_path.suffix.lstrip(".") or "bin",
        required=False,
    )


def load_extra_artifacts(path: Path | None, *, workspace_dir: Path, output_dir: Path) -> list[ArtifactRequest]:
    if path is None:
        return []
    payload = read_json(path)
    if not isinstance(payload, list):
        raise ValueError("extra_artifacts JSON must be a list")

    artifacts: list[ArtifactRequest] = []
    for item in payload:
        artifact = ArtifactRequest.model_validate(item)
        resolved = resolve_path(artifact.path, base_dir=workspace_dir)
        artifacts.append(
            ArtifactRequest(
                artifact_id=artifact.artifact_id,
                role=artifact.role,
                path=portable_path(resolved, base_dir=output_dir),
                format=artifact.format,
                required=artifact.required,
            )
        )
    return artifacts


def coerce_model_config(args: argparse.Namespace, *, request_dir: Path) -> dict[str, Any]:
    if not args.model_config_json:
        return {}
    path = resolve_path(args.model_config_json, base_dir=request_dir)
    payload = read_json(path)
    if not isinstance(payload, dict):
        raise ValueError("model_config_json must be a JSON object")
    return payload


def derive_dataset_path(args: argparse.Namespace, model_config: dict[str, Any], *, request_dir: Path) -> Path | None:
    if args.dataset_path:
        return resolve_path(args.dataset_path, base_dir=request_dir)
    dataset_path = model_config.get("dataset_path")
    if isinstance(dataset_path, str):
        return resolve_path(dataset_path, base_dir=request_dir)
    return None


def derive_label_config(args: argparse.Namespace, model_config: dict[str, Any]) -> LabelConfig:
    horizon_bars = args.horizon_bars if args.horizon_bars is not None else model_config.get("horizon_bars")
    band = args.band if args.band is not None else model_config.get("band")
    if horizon_bars is None or band is None:
        raise ValueError("horizon_bars and band must be supplied directly or via --model-config-json")
    return LabelConfig(label_type="three_class", horizon_bars=int(horizon_bars), band=float(band))


def derive_dataset_id(args: argparse.Namespace, dataset_path: Path | None) -> str:
    if args.dataset_id:
        return args.dataset_id
    if dataset_path is not None:
        return dataset_path.stem
    return args.experiment_id


def load_split_counts(path: Path | None) -> dict[str, int]:
    if path is None:
        return {}
    payload = read_json(path)
    if not isinstance(payload, dict):
        raise ValueError("split_counts JSON must be an object")
    return {str(key): int(value) for key, value in payload.items()}


def pick_selection_block(payload: dict[str, Any], *, logic_family: str, selection_key: str | None) -> dict[str, Any]:
    if selection_key:
        block = payload.get(selection_key)
        if not isinstance(block, dict):
            raise ValueError(f"selection key '{selection_key}' is missing or is not an object")
        return block

    candidates_by_family = {
        "threshold_only": ["blended_leader", "selected_pair", "preferred_seed"],
        "margin_only": ["stability_leader", "blended_leader", "selected_seed"],
        "prob_diff_only": ["blended_leader", "selected_seed", "top_test_read"],
    }
    for candidate in candidates_by_family.get(logic_family, []):
        block = payload.get(candidate)
        if isinstance(block, dict):
            return block
    raise ValueError(f"could not locate a default selection block for logic_family={logic_family}")


def build_rule_stack_from_selection(
    *,
    selection_json: Path,
    logic_family: str,
    selection_key: str | None,
    max_hold_bars: int,
) -> RuleStack:
    payload = read_json(selection_json)
    if not isinstance(payload, dict):
        raise ValueError("selection JSON must be an object")

    block = pick_selection_block(payload, logic_family=logic_family, selection_key=selection_key)
    position_rules = [
        RuleDefinition(
            rule_id="position_01",
            type="single_position_only",
            enabled=True,
            params={"max_concurrent_positions": 1},
        )
    ]
    exit_rules = [
        RuleDefinition(
            rule_id="exit_01",
            type="time_exit",
            enabled=True,
            params={"max_hold_bars": max_hold_bars},
        )
    ]

    if logic_family == "threshold_only":
        return RuleStack(
            entry=[
                RuleDefinition(
                    rule_id="entry_01",
                    type="threshold_entry",
                    enabled=True,
                    params={
                        "short_threshold": float(block["short_threshold"]),
                        "long_threshold": float(block["long_threshold"]),
                    },
                )
            ],
            filters=[],
            position=position_rules,
            exit=exit_rules,
        )

    if logic_family == "margin_only":
        return RuleStack(
            entry=[
                RuleDefinition(
                    rule_id="entry_01",
                    type="threshold_entry",
                    enabled=True,
                    params={
                        "short_threshold": 1.0 / 3.0,
                        "long_threshold": 1.0 / 3.0,
                    },
                )
            ],
            filters=[
                RuleDefinition(
                    rule_id="filter_01",
                    type="max_probability_margin",
                    enabled=True,
                    params={"min_margin": float(block["min_margin"])},
                )
            ],
            position=position_rules,
            exit=exit_rules,
        )

    if logic_family == "prob_diff_only":
        return RuleStack(
            entry=[
                RuleDefinition(
                    rule_id="entry_01",
                    type="threshold_entry",
                    enabled=True,
                    params={
                        "short_threshold": 1.0 / 3.0,
                        "long_threshold": 1.0 / 3.0,
                    },
                )
            ],
            filters=[
                RuleDefinition(
                    rule_id="filter_01",
                    type="probability_difference",
                    enabled=True,
                    params={"min_probability_diff": float(block["min_probability_diff"])},
                )
            ],
            position=position_rules,
            exit=exit_rules,
        )

    raise ValueError(f"unsupported logic_family for auto rule stack: {logic_family}")


def load_rule_stack(
    args: argparse.Namespace,
    *,
    request_dir: Path,
) -> RuleStack:
    if args.rule_stack_json:
        path = resolve_path(args.rule_stack_json, base_dir=request_dir)
        return RuleStack.model_validate(read_json(path))

    if not args.selection_json or not args.logic_family:
        raise ValueError("either --rule-stack-json or (--selection-json and --logic-family) is required")

    selection_json = resolve_path(args.selection_json, base_dir=request_dir)
    return build_rule_stack_from_selection(
        selection_json=selection_json,
        logic_family=args.logic_family,
        selection_key=args.selection_key,
        max_hold_bars=args.max_hold_bars,
    )


def build_request(args: argparse.Namespace) -> BundleBuildRequest:
    request_dir = ROOT_DIR
    output_dir = resolve_path(args.output_dir, base_dir=request_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    model_config = coerce_model_config(args, request_dir=request_dir)
    dataset_path = derive_dataset_path(args, model_config, request_dir=request_dir)
    label_config = derive_label_config(args, model_config)
    dataset_id = derive_dataset_id(args, dataset_path)

    feature_schema_artifact, feature_schema_request = build_feature_schema_artifact(
        args,
        output_dir=output_dir,
        workspace_dir=request_dir,
    )
    dataset_artifact = build_dataset_artifact(dataset_path=dataset_path, output_dir=output_dir)

    artifacts = [
        ArtifactRequest(
            artifact_id="art_onnx_model",
            role="onnx_model",
            path=portable_path(resolve_path(args.onnx_path, base_dir=request_dir), base_dir=output_dir),
            format=resolve_path(args.onnx_path, base_dir=request_dir).suffix.lstrip(".") or "onnx",
            required=True,
        ),
        feature_schema_artifact,
    ]
    if dataset_artifact is not None:
        artifacts.append(dataset_artifact)
    artifacts.extend(
        load_extra_artifacts(
            resolve_path(args.extra_artifacts_json, base_dir=request_dir) if args.extra_artifacts_json else None,
            workspace_dir=request_dir,
            output_dir=output_dir,
        )
    )

    source_artifact_ids = ["art_feature_schema"]
    if dataset_artifact is not None:
        source_artifact_ids.append(dataset_artifact.artifact_id)
    source_artifact_ids.extend(args.source_artifact_id)

    external_inputs = load_external_inputs(
        resolve_path(args.external_inputs_json, base_dir=request_dir) if args.external_inputs_json else None
    )
    rule_stack = load_rule_stack(args, request_dir=request_dir)

    split_counts = load_split_counts(
        resolve_path(args.split_counts_json, base_dir=request_dir) if args.split_counts_json else None
    )
    runtime_snapshot = RuntimeSnapshot(
        symbol="US100",
        timeframe="M5",
        tester_model="real_ticks",
        deposit=500,
        currency="USD",
        leverage=100,
        sizing_mode="fixed_lot",
        fixed_lot=0.1,
        entry_timing="next_tick_after_closed_bar_signal",
        max_concurrent_positions=1,
        cost_behavior="broker_native",
    )
    data_snapshot = DataSnapshot(
        dataset_id=dataset_id,
        source_artifact_ids=source_artifact_ids,
        split_boundaries=DEFAULT_SPLIT_BOUNDARIES,
        label_config=label_config,
        split_counts=split_counts,
        extra={
            "dataset_path": portable_path(dataset_path, base_dir=output_dir) if dataset_path is not None else None,
            "model_config_json": portable_path(resolve_path(args.model_config_json, base_dir=request_dir), base_dir=output_dir)
            if args.model_config_json
            else None,
        },
    )

    request = BundleBuildRequest(
        identity=IdentityRequest(
            experiment_id=args.experiment_id,
            stage_id=args.stage_id,
            stage_name=args.stage_name,
            bundle_version=args.bundle_version,
            created_by=args.created_by,
            created_at_utc=utc_now_iso(),
        ),
        artifacts=artifacts,
        feature_schema=feature_schema_request,
        output_schema=DEFAULT_OUTPUT_SCHEMA,
        external_inputs=external_inputs,
        data_snapshot=data_snapshot,
        runtime_snapshot=runtime_snapshot,
        rule_stack=rule_stack,
        compatibility=CompatibilityRequest(required_ea_capabilities=DEFAULT_REQUIRED_CAPABILITIES),
        smoke_test=SmokeTestRequest(
            onnx_artifact_id="art_onnx_model",
            input=SmokeArraySpec(
                path=portable_path(resolve_path(args.smoke_input_path, base_dir=request_dir), base_dir=output_dir),
                format=args.smoke_input_format,
                key=args.smoke_input_key,
            ),
            expected_output=SmokeArraySpec(
                path=portable_path(resolve_path(args.smoke_output_path, base_dir=request_dir), base_dir=output_dir),
                format=args.smoke_output_format,
                key=args.smoke_output_key,
            ),
        ),
    )
    return request


def build_summary(request: BundleBuildRequest, *, request_path: Path) -> dict[str, Any]:
    return {
        "status": "success",
        "generated_at_utc": utc_now_iso(),
        "request_path": str(request_path.as_posix()),
        "experiment_id": request.identity.experiment_id,
        "artifact_count": len(request.artifacts),
        "feature_count": request.feature_schema.feature_count,
        "rule_stack_counts": {
            "entry": len(request.rule_stack.entry),
            "filters": len(request.rule_stack.filters),
            "position": len(request.rule_stack.position),
            "exit": len(request.rule_stack.exit),
        },
        "external_input_count": len(request.external_inputs),
    }


def main() -> int:
    args = build_parser().parse_args()
    output_dir = resolve_path(args.output_dir, base_dir=ROOT_DIR)
    output_dir.mkdir(parents=True, exist_ok=True)

    request_path = output_dir / "bundle_request.json"
    summary_path = output_dir / "bundle_request_build_summary.json"

    request = build_request(args)
    request_path.write_text(request.model_dump_json(indent=2), encoding="utf-8")
    write_json(summary_path, build_summary(request, request_path=request_path))

    print(f"[done] request={request_path}")
    print(f"[done] summary={summary_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
