#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
import json
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import joblib
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, balanced_accuracy_score, f1_score, log_loss

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from foundation.pipelines.export_experiment_bundle_assets import run_export_bundle_assets
from foundation.pipelines.show_experiment_leaderboard import BundleView, load_bundle_views, sort_bundle_views


UTC = timezone.utc
REFERENCE_RUN_NAMES = [
    "05DP_05ca_margin0675_hold5_0001",
    "05EM_05dp_short_bias_margin_hold5_0001",
    "05DL_05cc_margin_hold5_0001",
]
REFERENCE_LABELS = {
    "05DP_05ca_margin0675_hold5_0001": "promoted_05dp",
    "05EM_05dp_short_bias_margin_hold5_0001": "closest_short_bias_05em",
    "05DL_05cc_margin_hold5_0001": "lower_ulcer_alt_05dl",
}
CLASS_LABELS = ["short", "flat", "long"]


@dataclass
class OutputShapeSpec:
    stage_id: str
    run_name: str
    experiment_id: str
    variant_label: str
    temperature: float
    class_scales: tuple[float, float, float]
    class_biases: tuple[float, float, float]
    rationale: str


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run output-shape exploration on top of the 05CA -> 05DP line.")
    parser.add_argument("--stage-root", default="stages/05_optimization", help="Stage 05 root directory.")
    parser.add_argument(
        "--source-run-dir",
        default="stages/05_optimization/02_runs/active/05CA_trend_proxy_persistence_riskoff_0001",
        help="Existing trained run directory whose model/features should be reused.",
    )
    parser.add_argument(
        "--logic-reference-run-name",
        default="05DP_05ca_margin0675_hold5_0001",
        help="Current promoted incumbent used for comparison.",
    )
    parser.add_argument("--rebuild-bundle", action="store_true", help="Force bundle rebuild even if present.")
    parser.add_argument(
        "--skip-holdout",
        action="store_true",
        help="Run validation sweep only and do not open holdout for the top-two new output-shape candidates.",
    )
    return parser


def utc_now_iso() -> str:
    return datetime.now(tz=UTC).isoformat()


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_json(path: Path, payload: dict[str, Any]) -> None:
    write_text(path, json.dumps(payload, indent=2, ensure_ascii=False) + "\n")


def build_specs() -> list[OutputShapeSpec]:
    return [
        OutputShapeSpec(
            stage_id="05FA",
            run_name="05FA_05ca_temp115_margin0675_hold5_0001",
            experiment_id="exp_05fa_05ca_temp115_margin0675_hold5_v1",
            variant_label="temp_soft_115",
            temperature=1.15,
            class_scales=(1.0, 1.0, 1.0),
            class_biases=(0.0, 0.0, 0.0),
            rationale="flatten all logits slightly to reduce directional overconfidence",
        ),
        OutputShapeSpec(
            stage_id="05FB",
            run_name="05FB_05ca_temp090_margin0675_hold5_0001",
            experiment_id="exp_05fb_05ca_temp090_margin0675_hold5_v1",
            variant_label="temp_sharp_090",
            temperature=0.90,
            class_scales=(1.0, 1.0, 1.0),
            class_biases=(0.0, 0.0, 0.0),
            rationale="sharpen logits slightly to widen directional margins without changing feature-side structure",
        ),
        OutputShapeSpec(
            stage_id="05FC",
            run_name="05FC_05ca_shortup_longdown_margin0675_hold5_0001",
            experiment_id="exp_05fc_05ca_shortup_longdown_margin0675_hold5_v1",
            variant_label="short_up_long_down_bias",
            temperature=1.0,
            class_scales=(1.0, 1.0, 1.0),
            class_biases=(0.10, 0.00, -0.10),
            rationale="nudge ambiguous directional calls away from long and slightly toward short",
        ),
        OutputShapeSpec(
            stage_id="05FD",
            run_name="05FD_05ca_flatup_longdown_margin0675_hold5_0001",
            experiment_id="exp_05fd_05ca_flatup_longdown_margin0675_hold5_v1",
            variant_label="flat_up_long_down_bias",
            temperature=1.0,
            class_scales=(1.0, 1.0, 1.0),
            class_biases=(0.00, 0.10, -0.10),
            rationale="prefer skip/flat over long when the model is already indecisive in plateau-like zones",
        ),
        OutputShapeSpec(
            stage_id="05FE",
            run_name="05FE_05ca_cls_scale_0001",
            experiment_id="exp_05fe_05ca_cls_scale_v1",
            variant_label="short_scale_up_long_scale_down",
            temperature=1.0,
            class_scales=(1.08, 1.00, 0.92),
            class_biases=(0.00, 0.00, 0.00),
            rationale="apply class-specific logit scaling so short confidence expands while long confidence compresses",
        ),
        OutputShapeSpec(
            stage_id="05FF",
            run_name="05FF_05ca_temp_shortbias_0001",
            experiment_id="exp_05ff_05ca_temp_shortbias_v1",
            variant_label="soft_temp_short_bias_combo",
            temperature=1.10,
            class_scales=(1.0, 1.0, 1.0),
            class_biases=(0.08, 0.00, -0.08),
            rationale="combine mild flattening with a light short-vs-long tilt to test a smoother plateau response",
        ),
    ]


def class_counts(series: pd.Series) -> dict[str, int]:
    counts = series.value_counts().to_dict()
    return {label: int(counts.get(index, 0)) for index, label in enumerate(CLASS_LABELS)}


def build_rule_stack() -> dict[str, Any]:
    return {
        "entry": [
            {
                "rule_id": "entry_01",
                "type": "threshold_entry",
                "enabled": True,
                "params": {
                    "short_threshold": 1.0 / 3.0,
                    "long_threshold": 1.0 / 3.0,
                },
            }
        ],
        "filters": [
            {
                "rule_id": "filter_01",
                "type": "max_probability_margin",
                "enabled": True,
                "params": {"min_margin": 0.0675},
            }
        ],
        "position": [
            {
                "rule_id": "position_01",
                "type": "single_position_only",
                "enabled": True,
                "params": {"max_concurrent_positions": 1},
            }
        ],
        "exit": [
            {
                "rule_id": "exit_01",
                "type": "time_exit",
                "enabled": True,
                "params": {"max_hold_bars": 5},
            }
        ],
    }


def clone_with_output_shape(source_model: Any, spec: OutputShapeSpec) -> Any:
    model = copy.deepcopy(source_model)
    classifier = model.named_steps["classifier"]
    scale_vector = np.asarray(spec.class_scales, dtype=np.float64) / float(spec.temperature)
    bias_vector = np.asarray(spec.class_biases, dtype=np.float64)
    classifier.coef_ = np.asarray(classifier.coef_, dtype=np.float64) * scale_vector[:, None]
    classifier.intercept_ = np.asarray(classifier.intercept_, dtype=np.float64) * scale_vector + bias_vector
    return model


def save_test_outputs(run_dir: Path, test_df: pd.DataFrame, y_pred: np.ndarray, y_proba: np.ndarray) -> None:
    out = test_df[["timestamp", "split", "forward_return", "label"]].copy()
    out = out.rename(columns={"label": "label_true"})
    out["label_pred"] = y_pred
    out["p_short"] = y_proba[:, 0]
    out["p_flat"] = y_proba[:, 1]
    out["p_long"] = y_proba[:, 2]
    out.to_parquet(run_dir / "test_predictions.parquet", index=False)


def predicted_share(y_pred: np.ndarray) -> dict[str, float]:
    return {label: float(np.mean(y_pred == index)) for index, label in enumerate(CLASS_LABELS)}


def mean_probs(y_proba: np.ndarray) -> dict[str, float]:
    return {label: float(y_proba[:, index].mean()) for index, label in enumerate(CLASS_LABELS)}


def calibration_gap_by_predicted_class(y_true: np.ndarray, y_pred: np.ndarray, y_proba: np.ndarray) -> dict[str, float | None]:
    gaps: dict[str, float | None] = {}
    for index, label in enumerate(CLASS_LABELS):
        mask = y_pred == index
        if not mask.any():
            gaps[label] = None
            continue
        avg_conf = float(y_proba[mask, index].mean())
        realized_acc = float(np.mean(y_true[mask] == index))
        gaps[label] = avg_conf - realized_acc
    return gaps


def build_metrics_payload(
    *,
    spec: OutputShapeSpec,
    y_true: np.ndarray,
    y_pred: np.ndarray,
    y_proba: np.ndarray,
) -> dict[str, Any]:
    return {
        "run_name": spec.run_name,
        "variant_label": spec.variant_label,
        "temperature": float(spec.temperature),
        "class_scales": [float(value) for value in spec.class_scales],
        "class_biases": [float(value) for value in spec.class_biases],
        "test_rows": int(len(y_true)),
        "test_macro_f1": float(f1_score(y_true, y_pred, average="macro")),
        "test_balanced_accuracy": float(balanced_accuracy_score(y_true, y_pred)),
        "test_accuracy": float(accuracy_score(y_true, y_pred)),
        "test_log_loss": float(log_loss(y_true, y_proba, labels=[0, 1, 2])),
        "test_mean_probs": mean_probs(y_proba),
        "test_predicted_share": predicted_share(y_pred),
        "test_predicted_class_confidence_gap": calibration_gap_by_predicted_class(y_true, y_pred, y_proba),
    }


def prepare_run_dir(
    *,
    spec: OutputShapeSpec,
    run_dir: Path,
    source_model: Any,
    source_config: dict[str, Any],
    dataset: pd.DataFrame,
    active_features: list[str],
    rebuild_bundle: bool,
) -> Path:
    run_dir.mkdir(parents=True, exist_ok=True)
    model = clone_with_output_shape(source_model, spec)
    joblib.dump(model, run_dir / "model.joblib")

    test_df = dataset[dataset["split"].eq("test")].copy()
    y_true = test_df["label"].to_numpy(dtype=np.int64)
    y_proba = np.asarray(model.predict_proba(test_df[active_features]), dtype=np.float64)
    y_pred = np.argmax(y_proba, axis=1)
    save_test_outputs(run_dir, test_df, y_pred, y_proba)
    write_json(run_dir / "metrics.json", build_metrics_payload(spec=spec, y_true=y_true, y_pred=y_pred, y_proba=y_proba))

    config = dict(source_config)
    config.update(
        {
            "run_name": spec.run_name,
            "phase": "stage05_output_shape_exploration",
            "generated_at_utc": utc_now_iso(),
            "logic_reference_run_name": "05DP_05ca_margin0675_hold5_0001",
            "logic_filter": {"type": "max_probability_margin", "min_margin": 0.0675},
            "logic_exit": {"type": "time_exit", "max_hold_bars": 5},
            "output_shape_transform": {
                "temperature": float(spec.temperature),
                "class_scales": [float(value) for value in spec.class_scales],
                "class_biases": [float(value) for value in spec.class_biases],
                "rationale": spec.rationale,
            },
            "row_counts": {
                "train_valid": int(dataset["split"].isin(["train", "valid"]).sum()),
                "test": int(dataset["split"].eq("test").sum()),
            },
            "class_counts": {
                "train_valid": class_counts(dataset.loc[dataset["split"].isin(["train", "valid"]), "label"]),
                "test": class_counts(dataset.loc[dataset["split"].eq("test"), "label"]),
            },
        }
    )
    write_json(run_dir / "config.json", config)
    write_json(
        run_dir / "candidate_manifest.json",
        {
            "generated_at_utc": utc_now_iso(),
            "candidate_type": "05dp_output_shape",
            "run_name": spec.run_name,
            "experiment_id": spec.experiment_id,
            "stage_id": spec.stage_id,
            "variant_label": spec.variant_label,
            "temperature": float(spec.temperature),
            "class_scales": [float(value) for value in spec.class_scales],
            "class_biases": [float(value) for value in spec.class_biases],
            "rationale": spec.rationale,
        },
    )
    write_json(run_dir / "rule_stack.json", build_rule_stack())

    bundle_path = run_dir / "experiment_bundle.json"
    if bundle_path.exists() and not rebuild_bundle:
        return bundle_path

    export_args = argparse.Namespace(
        run_dir=str(run_dir),
        experiment_id=spec.experiment_id,
        stage_id=spec.stage_id,
        output_dir=str(run_dir),
        stage_name="ea_optimize",
        bundle_version="1.0.0",
        created_by="python_orchestrator",
        config_json=None,
        dataset_path=None,
        selection_json=None,
        logic_family=None,
        selection_key=None,
        rule_stack_json=str(run_dir / "rule_stack.json"),
        smoke_split="test",
        smoke_row_index=0,
        max_hold_bars=5,
        build_bundle=True,
    )
    run_export_bundle_assets(export_args)
    return bundle_path


def run_tester(bundle_path: Path, *, split_name: str) -> None:
    cmd = [
        sys.executable,
        str(ROOT_DIR / "foundation" / "pipelines" / "run_mt5_bundle_tester.py"),
        "--bundle-json",
        str(bundle_path),
        "--split-name",
        split_name,
        "--enable-trading",
    ]
    subprocess.run(cmd, cwd=ROOT_DIR, check=True)


def load_view_map(run_names: set[str], split_name: str) -> dict[str, BundleView]:
    views = load_bundle_views(ROOT_DIR / "stages", split_name)
    filtered = [view for view in views if view.run_name in run_names]
    return {view.run_name: view for view in sort_bundle_views(filtered, "return_pct")}


def load_offline_metrics(run_dir: Path) -> dict[str, Any]:
    return json.loads((run_dir / "metrics.json").read_text(encoding="utf-8-sig"))


def extract_payload(view: BundleView, spec: OutputShapeSpec | None, label: str, run_dir: Path | None) -> dict[str, Any]:
    extra = view.execution.get("extra") or {}
    metrics = load_offline_metrics(run_dir) if run_dir is not None and (run_dir / "metrics.json").exists() else {}
    return {
        "run_name": view.run_name,
        "variant_label": label,
        "temperature": None if spec is None else spec.temperature,
        "class_scales": None if spec is None else [float(value) for value in spec.class_scales],
        "class_biases": None if spec is None else [float(value) for value in spec.class_biases],
        "offline_test_macro_f1": metrics.get("test_macro_f1"),
        "offline_test_balanced_accuracy": metrics.get("test_balanced_accuracy"),
        "offline_test_log_loss": metrics.get("test_log_loss"),
        "offline_predicted_share": metrics.get("test_predicted_share"),
        "return_pct": view.headline.get("return_pct"),
        "profit_factor": view.headline.get("profit_factor"),
        "trade_count": view.headline.get("trade_count"),
        "max_dd_pct": view.headline.get("max_dd_pct"),
        "ulcer_index": view.risk.get("ulcer_index"),
        "ready_row_gap": extra.get("ready_row_gap"),
        "unexpected_skip_count": extra.get("unexpected_skip_count"),
    }


def build_review_payload(
    *,
    ranked_validation: list[dict[str, Any]],
    ranked_holdout: list[dict[str, Any]] | None,
    incumbent_name: str,
    failed_runs: list[dict[str, str]],
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "generated_at_utc": utc_now_iso(),
        "phase": "05FM_mt5_05dp_output_shape_batch",
        "ranked_validation_runs": [{"rank": index + 1, **row} for index, row in enumerate(ranked_validation)],
        "failed_runs": failed_runs,
    }
    if ranked_holdout is not None:
        payload["ranked_test_runs"] = [{"rank": index + 1, **row} for index, row in enumerate(ranked_holdout)]
        holdout_winner = ranked_holdout[0]["run_name"]
        validation_winner = ranked_validation[0]["run_name"]
        if holdout_winner not in REFERENCE_RUN_NAMES and validation_winner == holdout_winner:
            payload["verdict"] = {
                "status": "promote_candidate",
                "selected_run_name": holdout_winner,
                "reason": "output-shape candidate led both validation and holdout versus promoted 05DP",
            }
        elif holdout_winner not in REFERENCE_RUN_NAMES:
            payload["verdict"] = {
                "status": "mixed_holdout_win_keep_incumbent",
                "selected_run_name": incumbent_name,
                "reason": "output-shape candidate improved holdout but did not lead validation, so 05DP remains promoted",
            }
        else:
            payload["verdict"] = {
                "status": "reject_keep_incumbent",
                "selected_run_name": incumbent_name,
                "reason": "no output-shape candidate cleared 05DP on holdout",
            }
    else:
        payload["verdict"] = {
            "status": "validation_only_pending_holdout",
            "selected_run_name": incumbent_name,
            "reason": "holdout not run yet, so 05DP remains selected",
        }
    return payload


def format_metric(value: Any, digits: int = 4) -> str:
    if value is None:
        return "n/a"
    return f"{float(value):.{digits}f}"


def format_vector(values: list[float] | None) -> str:
    if values is None:
        return "-"
    return "[" + ", ".join(f"{float(value):.3f}" for value in values) + "]"


def format_share(values: dict[str, float] | None) -> str:
    if not values:
        return "-"
    return ", ".join(f"{key}={float(value):.3f}" for key, value in values.items())


def build_review_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# 05FM Stage 05 05DP Output Shape Review",
        "",
        f"Generated at: `{payload['generated_at_utc']}`",
        "",
        "## Scope",
        "",
        "- purpose: `keep the 05CA feature/model lineage fixed and explore calibration-aware probability reshaping on top of the 05DP logic surface`",
        "- promoted incumbent: `05DP`",
        "- idea: `test whether temperature, class-bias, or class-specific logit scaling can improve plateau behavior without changing the feature stack or rule family`",
        "",
        "## MT5 Validation Ranking",
        "",
    ]
    for row in payload["ranked_validation_runs"]:
        lines.append(
            f"- [{row['rank']}] `{row['run_name']}`: "
            f"variant=`{row['variant_label']}`, temp={format_metric(row['temperature'], 3)}, "
            f"scales={format_vector(row['class_scales'])}, biases={format_vector(row['class_biases'])}, "
            f"return_pct={format_metric(row['return_pct'], 3)}, profit_factor={format_metric(row['profit_factor'], 4)}, "
            f"max_dd_pct={format_metric(row['max_dd_pct'], 4)}, ulcer_index={format_metric(row['ulcer_index'], 4)}, "
            f"trades={row['trade_count']}, ready_gap={row['ready_row_gap']}, unexpected_skips={row['unexpected_skip_count']}, "
            f"offline_macro_f1={format_metric(row['offline_test_macro_f1'], 4)}, offline_bal_acc={format_metric(row['offline_test_balanced_accuracy'], 4)}, "
            f"offline_log_loss={format_metric(row['offline_test_log_loss'], 4)}, pred_share=`{format_share(row['offline_predicted_share'])}`"
        )
    ranked_test_runs = payload.get("ranked_test_runs")
    if ranked_test_runs:
        lines.extend(["", "## MT5 Holdout Ranking", ""])
        for row in ranked_test_runs:
            lines.append(
                f"- [{row['rank']}] `{row['run_name']}`: "
                f"variant=`{row['variant_label']}`, temp={format_metric(row['temperature'], 3)}, "
                f"scales={format_vector(row['class_scales'])}, biases={format_vector(row['class_biases'])}, "
                f"return_pct={format_metric(row['return_pct'], 3)}, profit_factor={format_metric(row['profit_factor'], 4)}, "
                f"max_dd_pct={format_metric(row['max_dd_pct'], 4)}, ulcer_index={format_metric(row['ulcer_index'], 4)}, "
                f"trades={row['trade_count']}, ready_gap={row['ready_row_gap']}, unexpected_skips={row['unexpected_skip_count']}"
            )
    failed_runs = payload.get("failed_runs") or []
    if failed_runs:
        lines.extend(["", "## Failed Candidates", ""])
        for row in failed_runs:
            lines.append(f"- `{row['run_name']}`: `{row['error']}`")
    verdict = payload["verdict"]
    lines.extend(
        [
            "",
            "## Verdict",
            "",
            f"- status: `{verdict['status']}`",
            f"- selected_run_name: `{verdict['selected_run_name']}`",
            f"- reason: `{verdict['reason']}`",
            "",
            "## Read",
            "",
            "- read: `this batch separates output-shape effects from feature or rule changes, so any win here means the 05CA edge was partly trapped in probability geometry rather than the raw feature stack`",
        ]
    )
    return "\n".join(lines) + "\n"


def update_review_index(review_dir: Path) -> None:
    review_index_path = review_dir / "review_index.md"
    lines = review_index_path.read_text(encoding="utf-8").splitlines() if review_index_path.exists() else []
    entry = "- `05FM`: see `05FM_mt5_05dp_output_shape_review.md`"
    if entry not in lines:
        insert_at = 4 if len(lines) >= 4 else len(lines)
        lines.insert(insert_at, entry)
    write_text(review_index_path, "\n".join(lines).rstrip() + "\n")


def main() -> int:
    args = build_parser().parse_args()

    source_run_dir = (ROOT_DIR / args.source_run_dir).resolve()
    if not source_run_dir.exists():
        raise FileNotFoundError(f"source run dir not found: {source_run_dir}")

    source_config = json.loads((source_run_dir / "config.json").read_text(encoding="utf-8-sig"))
    active_features = list(source_config["active_input_features"])
    dataset_path = ROOT_DIR / source_config["dataset_path"]
    dataset = pd.read_parquet(dataset_path)
    source_model = joblib.load(source_run_dir / "model.joblib")

    stage_root = ROOT_DIR / args.stage_root
    review_dir = stage_root / "03_reviews"
    run_root = stage_root / "02_runs" / "active"
    review_dir.mkdir(parents=True, exist_ok=True)
    run_root.mkdir(parents=True, exist_ok=True)

    specs = build_specs()
    specs_by_run = {spec.run_name: spec for spec in specs}
    run_dirs: dict[str, Path] = {}
    failed_runs: list[dict[str, str]] = []
    for spec in specs:
        run_dir = run_root / spec.run_name
        run_dirs[spec.run_name] = run_dir
        bundle_path = prepare_run_dir(
            spec=spec,
            run_dir=run_dir,
            source_model=source_model,
            source_config=source_config,
            dataset=dataset,
            active_features=active_features,
            rebuild_bundle=args.rebuild_bundle,
        )
        try:
            run_tester(bundle_path, split_name="validation")
        except Exception as exc:
            failed_runs.append({"run_name": spec.run_name, "error": f"{exc.__class__.__name__}: {exc}"})

    validation_views = load_view_map(set(specs_by_run) | set(REFERENCE_RUN_NAMES), "validation")
    ranked_validation: list[dict[str, Any]] = []
    for run_name, view in validation_views.items():
        if run_name in specs_by_run:
            ranked_validation.append(extract_payload(view, specs_by_run[run_name], specs_by_run[run_name].variant_label, run_dirs[run_name]))
        else:
            ranked_validation.append(extract_payload(view, None, REFERENCE_LABELS[run_name], None))

    ranked_holdout: list[dict[str, Any]] | None = None
    if ranked_validation and not args.skip_holdout:
        top_two = [row["run_name"] for row in ranked_validation if row["run_name"] not in REFERENCE_RUN_NAMES][:2]
        for run_name in top_two:
            bundle_path = run_dirs[run_name] / "experiment_bundle.json"
            try:
                run_tester(bundle_path, split_name="test")
            except Exception as exc:
                failed_runs.append({"run_name": run_name, "error": f"{exc.__class__.__name__}: {exc}"})
        holdout_views = load_view_map(set(top_two) | set(REFERENCE_RUN_NAMES), "test")
        ranked_holdout = []
        for run_name, view in holdout_views.items():
            if run_name in specs_by_run:
                ranked_holdout.append(extract_payload(view, specs_by_run[run_name], specs_by_run[run_name].variant_label, run_dirs[run_name]))
            else:
                ranked_holdout.append(extract_payload(view, None, REFERENCE_LABELS[run_name], None))

    review_payload = build_review_payload(
        ranked_validation=ranked_validation,
        ranked_holdout=ranked_holdout,
        incumbent_name=args.logic_reference_run_name,
        failed_runs=failed_runs,
    )
    review_json_path = review_dir / "05FM_mt5_05dp_output_shape_review.json"
    review_md_path = review_dir / "05FM_mt5_05dp_output_shape_review.md"
    write_json(review_json_path, review_payload)
    write_text(review_md_path, build_review_markdown(review_payload))
    update_review_index(review_dir)

    print(f"[done] review_md={review_md_path}")
    print(f"[done] review_json={review_json_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
