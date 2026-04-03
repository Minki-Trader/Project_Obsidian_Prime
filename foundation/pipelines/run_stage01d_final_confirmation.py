#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from lightgbm import LGBMClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, balanced_accuracy_score, f1_score, log_loss
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.utils.class_weight import compute_sample_weight

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from foundation.features.catalog import FEATURE_ORDER
from foundation.pipelines.export_experiment_bundle_assets import run_export_bundle_assets
from foundation.pipelines.run_stage01b_model_compare import write_json, write_text


UTC = timezone.utc
LABEL_MAP = {0: "short", 1: "flat", 2: "long"}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run Stage 01D final held-out confirmation.")
    parser.add_argument(
        "--selected-final-json",
        default="stages/01_base_feature_ml/04_selected/01C_selected_final_candidate.json",
        help="Stage 01C selected final candidate JSON",
    )
    parser.add_argument(
        "--stage-root",
        default="stages/01_base_feature_ml",
        help="Stage 01 root",
    )
    parser.add_argument(
        "--random-state",
        type=int,
        default=42,
        help="Random state for deterministic refit",
    )
    parser.add_argument(
        "--bundle-export-experiment-id",
        help="If supplied, run post-confirmation ONNX/request/bundle export for the final run",
    )
    parser.add_argument(
        "--bundle-export-output-dir",
        help="Optional export output directory. Defaults to <final-run-dir>/bundle_export",
    )
    parser.add_argument(
        "--bundle-export-stage-id",
        default="optimize_v1",
        help="Bundle stage id for post-confirmation export",
    )
    parser.add_argument(
        "--bundle-export-stage-name",
        default="ea_optimize",
        help="Bundle stage name for post-confirmation export",
    )
    parser.add_argument(
        "--bundle-export-selection-json",
        help="Selection JSON used to derive the bundle rule stack",
    )
    parser.add_argument(
        "--bundle-export-logic-family",
        choices=["threshold_only", "margin_only", "prob_diff_only", "custom"],
        help="Logic family for auto rule-stack recovery during post-confirmation export",
    )
    parser.add_argument(
        "--bundle-export-selection-key",
        help="Optional selection block override for post-confirmation export",
    )
    parser.add_argument(
        "--bundle-export-rule-stack-json",
        help="Explicit rule_stack JSON for post-confirmation export",
    )
    parser.add_argument(
        "--bundle-export-smoke-split",
        default="test",
        help="Preferred split for smoke row selection during post-confirmation export",
    )
    parser.add_argument(
        "--bundle-export-smoke-row-index",
        type=int,
        default=0,
        help="Row index within the preferred smoke split for post-confirmation export",
    )
    parser.add_argument(
        "--bundle-export-max-hold-bars",
        type=int,
        default=3,
        help="Exit max_hold_bars when auto-building the post-confirmation export rule stack",
    )
    return parser


def utc_now_iso() -> str:
    return datetime.now(tz=UTC).isoformat()


def class_counts(series: pd.Series) -> dict[str, int]:
    counts = series.value_counts().to_dict()
    return {LABEL_MAP[key]: int(counts.get(key, 0)) for key in LABEL_MAP}


def save_test_outputs(
    run_dir: Path,
    test_df: pd.DataFrame,
    y_pred: np.ndarray,
    y_proba: np.ndarray,
) -> None:
    out = test_df[["timestamp", "split", "forward_return", "label"]].copy()
    out = out.rename(columns={"label": "label_true"})
    out["label_pred"] = y_pred
    out["p_short"] = y_proba[:, 0]
    out["p_flat"] = y_proba[:, 1]
    out["p_long"] = y_proba[:, 2]
    out.to_parquet(run_dir / "test_predictions.parquet", index=False)

    confusion = (
        pd.DataFrame({"label_true": out["label_true"], "label_pred": out["label_pred"]})
        .groupby(["label_true", "label_pred"])
        .size()
        .unstack(fill_value=0)
        .reindex(index=[0, 1, 2], columns=[0, 1, 2], fill_value=0)
    )
    confusion.index = [LABEL_MAP[idx] for idx in confusion.index]
    confusion.columns = [LABEL_MAP[idx] for idx in confusion.columns]
    confusion.to_csv(run_dir / "test_confusion_matrix.csv")


def fit_logistic(train_valid_df: pd.DataFrame, random_state: int) -> Pipeline:
    x_train = train_valid_df[FEATURE_ORDER]
    y_train = train_valid_df["label"]
    model = Pipeline(
        steps=[
            ("scaler", StandardScaler()),
            (
                "classifier",
                LogisticRegression(
                    solver="lbfgs",
                    max_iter=3000,
                    class_weight="balanced",
                    random_state=random_state,
                ),
            ),
        ]
    )
    model.fit(x_train, y_train)
    return model


def fit_lightgbm(train_valid_df: pd.DataFrame, best_iteration: int, random_state: int) -> LGBMClassifier:
    x_train = train_valid_df[FEATURE_ORDER]
    y_train = train_valid_df["label"]
    sample_weight = compute_sample_weight(class_weight="balanced", y=y_train)
    n_estimators = best_iteration if best_iteration and best_iteration > 0 else 500
    model = LGBMClassifier(
        objective="multiclass",
        num_class=3,
        n_estimators=n_estimators,
        learning_rate=0.05,
        num_leaves=31,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=random_state,
        n_jobs=-1,
    )
    model.fit(x_train, y_train, sample_weight=sample_weight)
    return model


def maybe_run_bundle_export(args: argparse.Namespace, final_run_dir: Path) -> dict[str, str] | None:
    if not args.bundle_export_experiment_id:
        return None

    has_explicit_rule_stack = bool(args.bundle_export_rule_stack_json)
    has_selection_rule_source = bool(args.bundle_export_selection_json and args.bundle_export_logic_family)
    if not has_explicit_rule_stack and not has_selection_rule_source:
        raise ValueError(
            "bundle export requires either --bundle-export-rule-stack-json "
            "or both --bundle-export-selection-json and --bundle-export-logic-family"
        )

    export_output_dir = (
        ROOT_DIR / args.bundle_export_output_dir
        if args.bundle_export_output_dir
        else final_run_dir / "bundle_export"
    )
    export_args = argparse.Namespace(
        run_dir=str(final_run_dir),
        experiment_id=args.bundle_export_experiment_id,
        stage_id=args.bundle_export_stage_id,
        output_dir=str(export_output_dir),
        stage_name=args.bundle_export_stage_name,
        bundle_version="1.0.0",
        created_by="python_orchestrator",
        config_json=None,
        dataset_path=None,
        selection_json=args.bundle_export_selection_json,
        logic_family=args.bundle_export_logic_family,
        selection_key=args.bundle_export_selection_key,
        rule_stack_json=args.bundle_export_rule_stack_json,
        smoke_split=args.bundle_export_smoke_split,
        smoke_row_index=args.bundle_export_smoke_row_index,
        max_hold_bars=args.bundle_export_max_hold_bars,
        build_bundle=True,
    )
    return run_export_bundle_assets(export_args)


def main() -> int:
    args = build_parser().parse_args()

    selected_final_path = ROOT_DIR / args.selected_final_json
    stage_root = ROOT_DIR / args.stage_root

    selected_payload = json.loads(selected_final_path.read_text(encoding="utf-8"))
    candidate = selected_payload["selected_final_candidate"]
    run_name = candidate["run_name"]
    model_family = candidate["model_family"]

    active_run_dir = stage_root / "02_runs" / "active" / run_name
    run_config_path = active_run_dir / "config.json"
    if not run_config_path.exists():
        raise FileNotFoundError(f"missing selected run config: {run_config_path}")

    run_config = json.loads(run_config_path.read_text(encoding="utf-8"))
    dataset_path = ROOT_DIR / run_config["dataset_path"]
    dataset = pd.read_parquet(dataset_path)

    train_valid_df = dataset[dataset["split"].isin(["train", "valid"])].copy()
    test_df = dataset[dataset["split"].eq("test")].copy()

    final_run_name = f"01D_run_0001_final_{run_name.split('01C_run_0001_', 1)[-1]}"
    final_run_dir = stage_root / "02_runs" / "active" / final_run_name
    final_run_dir.mkdir(parents=True, exist_ok=True)

    final_config = {
        "run_name": final_run_name,
        "phase": "01D_final_confirmation",
        "generated_at_utc": utc_now_iso(),
        "source_selected_final_json": str(selected_final_path.relative_to(ROOT_DIR)),
        "source_01C_run_name": run_name,
        "model_family": model_family,
        "horizon_bars": int(candidate["horizon_bars"]),
        "band": float(candidate["band"]),
        "dataset_path": str(dataset_path.relative_to(ROOT_DIR)),
        "refit_policy": "train_plus_valid_refit_then_test_once",
        "row_counts": {
            "train_valid": int(len(train_valid_df)),
            "test": int(len(test_df)),
        },
        "class_counts": {
            "train_valid": class_counts(train_valid_df["label"]),
            "test": class_counts(test_df["label"]),
        },
    }
    write_json(final_run_dir / "config.json", final_config)

    if model_family == "logistic_regression":
        model = fit_logistic(train_valid_df, args.random_state)
    elif model_family == "lightgbm":
        model = fit_lightgbm(train_valid_df, int(candidate.get("best_iteration", 0)), args.random_state)
    else:
        raise ValueError(f"unsupported final confirmation model family: {model_family}")

    x_test = test_df[FEATURE_ORDER]
    y_test = test_df["label"].to_numpy(dtype=np.int64)
    y_proba = model.predict_proba(x_test)
    y_pred = np.argmax(y_proba, axis=1)

    joblib.dump(model, final_run_dir / "model.joblib")
    save_test_outputs(final_run_dir, test_df, y_pred, y_proba)

    metrics = {
        "run_name": final_run_name,
        "model_family": model_family,
        "test_rows": int(len(test_df)),
        "test_macro_f1": float(f1_score(y_test, y_pred, average="macro")),
        "test_balanced_accuracy": float(balanced_accuracy_score(y_test, y_pred)),
        "test_accuracy": float(accuracy_score(y_test, y_pred)),
        "test_log_loss": float(log_loss(y_test, y_proba, labels=[0, 1, 2])),
    }
    write_json(final_run_dir / "metrics.json", metrics)

    review_lines = [
        "# 01D Final Confirmation Review",
        "",
        f"Generated at: `{utc_now_iso()}`",
        "",
        "## Frozen Candidate",
        "",
        f"- source run: `{run_name}`",
        f"- model: `{model_family}`",
        f"- horizon: `{int(candidate['horizon_bars'])}` bars",
        f"- band: `{float(candidate['band']):.5f}`",
        "- refit policy: `train+valid refit -> single held-out test check`",
        "",
        "## Test Metrics",
        "",
        f"- macro_f1: `{metrics['test_macro_f1']:.4f}`",
        f"- balanced_accuracy: `{metrics['test_balanced_accuracy']:.4f}`",
        f"- accuracy: `{metrics['test_accuracy']:.4f}`",
        f"- log_loss: `{metrics['test_log_loss']:.4f}`",
    ]
    write_text(stage_root / "03_reviews" / "01D_final_confirmation_review.md", "\n".join(review_lines) + "\n")

    final_selected = {
        "generated_at_utc": utc_now_iso(),
        "phase": "01D_final_confirmation",
        "final_stage01_run_name": final_run_name,
        "final_model_family": model_family,
        "final_horizon_bars": int(candidate["horizon_bars"]),
        "final_band": float(candidate["band"]),
        "valid_reference": {
            "macro_f1": float(candidate["valid_macro_f1"]),
            "balanced_accuracy": float(candidate["valid_balanced_accuracy"]),
            "accuracy": float(candidate["valid_accuracy"]),
            "log_loss": float(candidate["valid_log_loss"]),
        },
        "test_confirmation": metrics,
        "next_phase": "02_individual_thresholds",
    }
    write_json(stage_root / "04_selected" / "01D_final_stage01_selection.json", final_selected)
    write_text(
        stage_root / "04_selected" / "01D_final_stage01_selection.md",
        "\n".join(
            [
                "# Stage 01 Final Selection",
                "",
                f"- final run: `{final_run_name}`",
                f"- model: `{model_family}`",
                f"- horizon: `{int(candidate['horizon_bars'])}` bars",
                f"- band: `{float(candidate['band']):.5f}`",
                f"- test macro_f1: `{metrics['test_macro_f1']:.4f}`",
                f"- test balanced_accuracy: `{metrics['test_balanced_accuracy']:.4f}`",
                f"- test accuracy: `{metrics['test_accuracy']:.4f}`",
                f"- next stage: `02_individual_thresholds`",
            ]
        )
        + "\n",
    )

    bundle_export_result = maybe_run_bundle_export(args, final_run_dir)
    if bundle_export_result is not None:
        final_selected["bundle_export"] = bundle_export_result
        write_json(stage_root / "04_selected" / "01D_final_stage01_selection.json", final_selected)
        write_text(
            stage_root / "04_selected" / "01D_final_stage01_selection.md",
            "\n".join(
                [
                    "# Stage 01 Final Selection",
                    "",
                    f"- final run: `{final_run_name}`",
                    f"- model: `{model_family}`",
                    f"- horizon: `{int(candidate['horizon_bars'])}` bars",
                    f"- band: `{float(candidate['band']):.5f}`",
                    f"- test macro_f1: `{metrics['test_macro_f1']:.4f}`",
                    f"- test balanced_accuracy: `{metrics['test_balanced_accuracy']:.4f}`",
                    f"- test accuracy: `{metrics['test_accuracy']:.4f}`",
                    f"- next stage: `02_individual_thresholds`",
                    f"- bundle export: `{bundle_export_result['bundle_path']}`",
                ]
            )
            + "\n",
        )

    print(json.dumps(final_selected, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
