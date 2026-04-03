#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, log_loss, recall_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from foundation.features.catalog import FEATURE_ORDER
from foundation.pipelines.run_stage01b_model_compare import write_json, write_text
from foundation.pipelines.run_stage01f_sector_ablation import STAGE_ROOT, load_context, utc_now_iso


RUN_DIR = STAGE_ROOT / "02_runs" / "archived" / "01I_run_0001_stability_slices"
REVIEW_MD = STAGE_ROOT / "03_reviews" / "01I_stability_slices_review.md"
REVIEW_JSON = STAGE_ROOT / "03_reviews" / "01I_stability_slices_review.json"
SOURCE_01H_RUN_DIR = STAGE_ROOT / "02_runs" / "archived" / "01H_run_0001_compact_candidate_compare"


SESSION_ORDER = [
    "cash_open_30m",
    "cash_mid",
    "cash_close_30m",
    "overnight",
]


@dataclass
class ModelArtifacts:
    name: str
    features: list[str]
    model: Pipeline
    valid_pred: np.ndarray
    valid_proba: np.ndarray


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Stage 01I monthly/session/hour stability diagnostics.")
    parser.add_argument(
        "--final-selection-json",
        default="stages/01_base_feature_ml/04_selected/01D_final_stage01_selection.json",
        help="Stage 01D final selection JSON",
    )
    parser.add_argument(
        "--compact-summary-json",
        default=str((SOURCE_01H_RUN_DIR / "summary.json").relative_to(ROOT_DIR)),
        help="Stage 01H summary JSON",
    )
    parser.add_argument(
        "--compact-feature-sets-json",
        default=str((SOURCE_01H_RUN_DIR / "feature_sets.json").relative_to(ROOT_DIR)),
        help="Stage 01H feature_sets JSON",
    )
    parser.add_argument(
        "--random-state",
        type=int,
        default=42,
        help="Random state for logistic regression",
    )
    return parser.parse_args()


def build_model(random_state: int) -> Pipeline:
    return Pipeline(
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


def load_compact_candidate(summary_path: Path, feature_sets_path: Path) -> tuple[str, list[str]]:
    summary_payload = json.loads(summary_path.read_text(encoding="utf-8"))
    feature_sets = json.loads(feature_sets_path.read_text(encoding="utf-8"))
    compact_name = summary_payload["recommended_compact_variant"]["variant"]
    if compact_name not in feature_sets:
        raise ValueError(f"compact candidate `{compact_name}` missing from feature sets")
    compact_features = feature_sets[compact_name]["features"]
    return compact_name, compact_features


def fit_for_valid(
    train_df: pd.DataFrame,
    valid_df: pd.DataFrame,
    model_name: str,
    features: list[str],
    random_state: int,
) -> ModelArtifacts:
    model = build_model(random_state=random_state)
    model.fit(train_df[features], train_df["label"])
    valid_proba = model.predict_proba(valid_df[features])
    valid_pred = np.argmax(valid_proba, axis=1)
    return ModelArtifacts(
        name=model_name,
        features=features,
        model=model,
        valid_pred=valid_pred,
        valid_proba=valid_proba,
    )


def session_bucket(frame: pd.DataFrame) -> pd.Series:
    bucket = pd.Series(index=frame.index, dtype="object")
    bucket.loc[frame["is_us_cash_open"].lt(0.5)] = "overnight"
    bucket.loc[frame["is_us_cash_open"].ge(0.5)] = "cash_mid"
    bucket.loc[frame["is_first_30m_after_open"].ge(0.5)] = "cash_open_30m"
    bucket.loc[frame["is_last_30m_before_cash_close"].ge(0.5)] = "cash_close_30m"
    return bucket


def metric_bundle(y_true: np.ndarray, y_pred: np.ndarray, y_proba: np.ndarray) -> dict[str, float]:
    return {
        "macro_f1": float(f1_score(y_true, y_pred, labels=[0, 1, 2], average="macro", zero_division=0)),
        "balanced_accuracy": float(recall_score(y_true, y_pred, labels=[0, 1, 2], average="macro", zero_division=0)),
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "log_loss": float(log_loss(y_true, y_proba, labels=[0, 1, 2])),
    }


def compute_slice_metrics(
    valid_slice_df: pd.DataFrame,
    predictions: dict[str, ModelArtifacts],
    slice_type: str,
    slice_column: str,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    long_rows: list[dict] = []
    comparison_rows: list[dict] = []

    for slice_value, group in valid_slice_df.groupby(slice_column, sort=False):
        row_count = int(len(group))
        y_true = group["label"].to_numpy(dtype=np.int64)
        per_model: dict[str, dict[str, float]] = {}

        for model_name, artifacts in predictions.items():
            y_pred = artifacts.valid_pred[group.index.to_numpy()]
            y_proba = artifacts.valid_proba[group.index.to_numpy()]
            metrics = metric_bundle(y_true=y_true, y_pred=y_pred, y_proba=y_proba)
            per_model[model_name] = metrics
            long_rows.append(
                {
                    "slice_type": slice_type,
                    "slice_value": slice_value,
                    "row_count": row_count,
                    "model": model_name,
                    **metrics,
                }
            )

        full_metrics = per_model["full_58"]
        compact_key = [name for name in per_model.keys() if name != "full_58"][0]
        compact_metrics = per_model[compact_key]
        comparison_rows.append(
            {
                "slice_type": slice_type,
                "slice_value": slice_value,
                "row_count": row_count,
                "full_macro_f1": full_metrics["macro_f1"],
                "compact_macro_f1": compact_metrics["macro_f1"],
                "delta_macro_f1_compact_minus_full": compact_metrics["macro_f1"] - full_metrics["macro_f1"],
                "full_balanced_accuracy": full_metrics["balanced_accuracy"],
                "compact_balanced_accuracy": compact_metrics["balanced_accuracy"],
                "delta_balanced_accuracy_compact_minus_full": compact_metrics["balanced_accuracy"] - full_metrics["balanced_accuracy"],
                "full_accuracy": full_metrics["accuracy"],
                "compact_accuracy": compact_metrics["accuracy"],
                "delta_accuracy_compact_minus_full": compact_metrics["accuracy"] - full_metrics["accuracy"],
                "full_log_loss": full_metrics["log_loss"],
                "compact_log_loss": compact_metrics["log_loss"],
                "delta_log_loss_compact_minus_full": compact_metrics["log_loss"] - full_metrics["log_loss"],
            }
        )

    long_df = pd.DataFrame(long_rows)
    comparison_df = pd.DataFrame(comparison_rows)
    return long_df, comparison_df


def ordered_slice_df(slice_type: str, frame: pd.DataFrame) -> pd.DataFrame:
    ordered = frame.copy()
    if slice_type == "month_ny":
        ordered = ordered.sort_values("slice_value", kind="stable", ignore_index=True)
    elif slice_type == "session_bucket":
        ordered["slice_value"] = pd.Categorical(ordered["slice_value"], categories=SESSION_ORDER, ordered=True)
        ordered = ordered.sort_values("slice_value", kind="stable", ignore_index=True)
        ordered["slice_value"] = ordered["slice_value"].astype(str)
    elif slice_type == "hour_ny":
        ordered["hour_sort"] = ordered["slice_value"].astype(int)
        ordered = ordered.sort_values("hour_sort", kind="stable", ignore_index=True).drop(columns=["hour_sort"])
    return ordered


def main() -> int:
    args = parse_args()

    if RUN_DIR.exists():
        shutil.rmtree(RUN_DIR)
    RUN_DIR.mkdir(parents=True, exist_ok=True)

    final_selection_path = ROOT_DIR / args.final_selection_json
    compact_summary_path = ROOT_DIR / args.compact_summary_json
    compact_feature_sets_path = ROOT_DIR / args.compact_feature_sets_json

    final_selection, run_config, dataset = load_context(final_selection_path)
    compact_name, compact_features = load_compact_candidate(compact_summary_path, compact_feature_sets_path)

    train_df = dataset.loc[dataset["split"].eq("train")].copy()
    valid_df = dataset.loc[dataset["split"].eq("valid")].copy()
    valid_df = valid_df.reset_index(drop=True)

    valid_df["timestamp_ny"] = valid_df["timestamp"].dt.tz_convert("America/New_York")
    valid_df["month_ny"] = valid_df["timestamp_ny"].dt.strftime("%Y-%m")
    valid_df["hour_ny"] = valid_df["timestamp_ny"].dt.strftime("%H")
    valid_df["session_bucket"] = session_bucket(valid_df)

    predictions = {
        "full_58": fit_for_valid(
            train_df=train_df,
            valid_df=valid_df,
            model_name="full_58",
            features=FEATURE_ORDER,
            random_state=args.random_state,
        ),
        compact_name: fit_for_valid(
            train_df=train_df,
            valid_df=valid_df,
            model_name=compact_name,
            features=compact_features,
            random_state=args.random_state,
        ),
    }

    overall_payload = {}
    for model_name, artifacts in predictions.items():
        overall_payload[model_name] = {
            "num_features": len(artifacts.features),
            **metric_bundle(
                y_true=valid_df["label"].to_numpy(dtype=np.int64),
                y_pred=artifacts.valid_pred,
                y_proba=artifacts.valid_proba,
            ),
        }

    long_frames: list[pd.DataFrame] = []
    comparison_frames: list[pd.DataFrame] = []
    for slice_type, slice_column in [
        ("month_ny", "month_ny"),
        ("session_bucket", "session_bucket"),
        ("hour_ny", "hour_ny"),
    ]:
        long_df, comparison_df = compute_slice_metrics(
            valid_slice_df=valid_df,
            predictions=predictions,
            slice_type=slice_type,
            slice_column=slice_column,
        )
        long_df = ordered_slice_df(slice_type, long_df)
        comparison_df = ordered_slice_df(slice_type, comparison_df)
        long_df.to_csv(RUN_DIR / f"{slice_type}_metrics_long.csv", index=False)
        comparison_df.to_csv(RUN_DIR / f"{slice_type}_metrics_comparison.csv", index=False)
        long_frames.append(long_df)
        comparison_frames.append(comparison_df)

    all_long_df = pd.concat(long_frames, ignore_index=True)
    all_comparison_df = pd.concat(comparison_frames, ignore_index=True)
    all_long_df.to_csv(RUN_DIR / "stability_metrics_long.csv", index=False)
    all_comparison_df.to_csv(RUN_DIR / "stability_metrics_comparison.csv", index=False)

    monthly_comparison = ordered_slice_df("month_ny", comparison_frames[0])
    session_comparison = ordered_slice_df("session_bucket", comparison_frames[1])
    hour_comparison = ordered_slice_df("hour_ny", comparison_frames[2])

    summary_payload = {
        "generated_at_utc": utc_now_iso(),
        "phase": "01I_stability_slices",
        "source_final_selection_json": str(final_selection_path.relative_to(ROOT_DIR)),
        "source_final_run_name": final_selection["final_stage01_run_name"],
        "source_compact_summary_json": str(compact_summary_path.relative_to(ROOT_DIR)),
        "dataset_path": run_config["dataset_path"],
        "fit_split": "train",
        "eval_split": "valid",
        "full_variant": "full_58",
        "compact_variant": compact_name,
        "overall_valid": overall_payload,
        "monthly_compact_win_count": int(monthly_comparison["delta_macro_f1_compact_minus_full"].gt(0).sum()),
        "monthly_bucket_count": int(len(monthly_comparison)),
        "session_compact_win_count": int(session_comparison["delta_macro_f1_compact_minus_full"].gt(0).sum()),
        "session_bucket_count": int(len(session_comparison)),
        "hour_compact_win_count": int(hour_comparison["delta_macro_f1_compact_minus_full"].gt(0).sum()),
        "hour_bucket_count": int(len(hour_comparison)),
        "best_month_delta": monthly_comparison.sort_values("delta_macro_f1_compact_minus_full", ascending=False).head(1).to_dict(orient="records"),
        "worst_month_delta": monthly_comparison.sort_values("delta_macro_f1_compact_minus_full", ascending=True).head(1).to_dict(orient="records"),
        "best_session_delta": session_comparison.sort_values("delta_macro_f1_compact_minus_full", ascending=False).head(1).to_dict(orient="records"),
        "worst_session_delta": session_comparison.sort_values("delta_macro_f1_compact_minus_full", ascending=True).head(1).to_dict(orient="records"),
        "best_hours_delta": hour_comparison.sort_values("delta_macro_f1_compact_minus_full", ascending=False).head(3).to_dict(orient="records"),
        "worst_hours_delta": hour_comparison.sort_values("delta_macro_f1_compact_minus_full", ascending=True).head(3).to_dict(orient="records"),
    }
    write_json(RUN_DIR / "summary.json", summary_payload)
    write_json(REVIEW_JSON, summary_payload)

    compact_overall = overall_payload[compact_name]
    full_overall = overall_payload["full_58"]
    lines = [
        "# 01I Stability Slices Review",
        "",
        f"Generated at: `{summary_payload['generated_at_utc']}`",
        "",
        "## Scope",
        "",
        "- purpose: `check whether the recommended compact candidate stays stable across month/session/hour slices`",
        "- model family: `logistic_regression`",
        "- fit split: `train`",
        "- eval split: `valid`",
        "- held-out test: `not touched in 01I`",
        "",
        "## Overall Valid",
        "",
        f"- `full_58`: macro_f1 `{full_overall['macro_f1']:.4f}`, balanced_accuracy `{full_overall['balanced_accuracy']:.4f}`, accuracy `{full_overall['accuracy']:.4f}`, log_loss `{full_overall['log_loss']:.4f}`",
        f"- `{compact_name}`: macro_f1 `{compact_overall['macro_f1']:.4f}`, balanced_accuracy `{compact_overall['balanced_accuracy']:.4f}`, accuracy `{compact_overall['accuracy']:.4f}`, log_loss `{compact_overall['log_loss']:.4f}`",
        "",
        "## Stability Read",
        "",
        f"- monthly compact wins: `{summary_payload['monthly_compact_win_count']}/{summary_payload['monthly_bucket_count']}`",
        f"- session compact wins: `{summary_payload['session_compact_win_count']}/{summary_payload['session_bucket_count']}`",
        f"- hour compact wins: `{summary_payload['hour_compact_win_count']}/{summary_payload['hour_bucket_count']}`",
        "",
        "## Most Positive Slice",
        "",
        f"- month: `{summary_payload['best_month_delta'][0]['slice_value']}` delta macro_f1 `{summary_payload['best_month_delta'][0]['delta_macro_f1_compact_minus_full']:.4f}`",
        f"- session: `{summary_payload['best_session_delta'][0]['slice_value']}` delta macro_f1 `{summary_payload['best_session_delta'][0]['delta_macro_f1_compact_minus_full']:.4f}`",
        "",
        "## Most Negative Slice",
        "",
        f"- month: `{summary_payload['worst_month_delta'][0]['slice_value']}` delta macro_f1 `{summary_payload['worst_month_delta'][0]['delta_macro_f1_compact_minus_full']:.4f}`",
        f"- session: `{summary_payload['worst_session_delta'][0]['slice_value']}` delta macro_f1 `{summary_payload['worst_session_delta'][0]['delta_macro_f1_compact_minus_full']:.4f}`",
        "",
        "## Notes",
        "",
        "- Positive delta means the compact candidate outperformed the full baseline in that slice.",
        "- Negative delta means the full baseline held up better in that slice.",
        "- This remains a post-selection stability diagnostic and does not replace the frozen 01D handoff.",
        "",
        "## Artifacts",
        "",
        "- monthly comparison: `02_runs/archived/01I_run_0001_stability_slices/month_ny_metrics_comparison.csv`",
        "- session comparison: `02_runs/archived/01I_run_0001_stability_slices/session_bucket_metrics_comparison.csv`",
        "- hour comparison: `02_runs/archived/01I_run_0001_stability_slices/hour_ny_metrics_comparison.csv`",
    ]
    write_text(REVIEW_MD, "\n".join(lines) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
