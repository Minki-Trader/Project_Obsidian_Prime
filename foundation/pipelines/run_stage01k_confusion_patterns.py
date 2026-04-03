#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, precision_recall_fscore_support
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from foundation.features.catalog import FEATURE_ORDER
from foundation.pipelines.run_stage01b_model_compare import write_json, write_text
from foundation.pipelines.run_stage01f_sector_ablation import STAGE_ROOT, load_context, utc_now_iso


RUN_DIR = STAGE_ROOT / "02_runs" / "archived" / "01K_run_0001_confusion_patterns"
REVIEW_MD = STAGE_ROOT / "03_reviews" / "01K_confusion_patterns_review.md"
REVIEW_JSON = STAGE_ROOT / "03_reviews" / "01K_confusion_patterns_review.json"
SOURCE_01H_RUN_DIR = STAGE_ROOT / "02_runs" / "archived" / "01H_run_0001_compact_candidate_compare"

CLASS_LABELS = {
    0: "short",
    1: "flat",
    2: "long",
}
LABEL_ORDER = [0, 1, 2]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Stage 01K confusion pattern diagnostics.")
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
        help="Stage 01H feature sets JSON",
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


def fit_predict(
    train_df: pd.DataFrame,
    valid_df: pd.DataFrame,
    features: list[str],
    random_state: int,
) -> np.ndarray:
    model = build_model(random_state=random_state)
    model.fit(train_df[features], train_df["label"])
    return model.predict(valid_df[features]).astype(np.int64)


def build_confusion_frames(model_name: str, y_true: np.ndarray, y_pred: np.ndarray) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    cm = confusion_matrix(y_true, y_pred, labels=LABEL_ORDER)
    row_totals = cm.sum(axis=1, keepdims=True)
    row_rates = np.divide(cm, row_totals, out=np.zeros_like(cm, dtype=float), where=row_totals > 0)

    count_rows: list[dict] = []
    route_rows: list[dict] = []
    for true_idx, true_label in enumerate(LABEL_ORDER):
        for pred_idx, pred_label in enumerate(LABEL_ORDER):
            count = int(cm[true_idx, pred_idx])
            row_rate = float(row_rates[true_idx, pred_idx])
            record = {
                "model": model_name,
                "true_class_id": true_label,
                "true_class": CLASS_LABELS[true_label],
                "pred_class_id": pred_label,
                "pred_class": CLASS_LABELS[pred_label],
                "count": count,
                "row_rate": row_rate,
                "is_correct": bool(true_label == pred_label),
            }
            count_rows.append(record)
            if true_label != pred_label:
                route_rows.append(record)

    precision, recall, f1, support = precision_recall_fscore_support(
        y_true,
        y_pred,
        labels=LABEL_ORDER,
        zero_division=0,
    )
    class_rows = [
        {
            "model": model_name,
            "class_id": class_id,
            "class_name": CLASS_LABELS[class_id],
            "precision": float(precision[idx]),
            "recall": float(recall[idx]),
            "f1": float(f1[idx]),
            "support": int(support[idx]),
        }
        for idx, class_id in enumerate(LABEL_ORDER)
    ]

    return pd.DataFrame(count_rows), pd.DataFrame(route_rows), pd.DataFrame(class_rows)


def merge_route_comparison(full_routes: pd.DataFrame, compact_routes: pd.DataFrame, compact_name: str) -> pd.DataFrame:
    merged = full_routes.merge(
        compact_routes,
        on=["true_class_id", "true_class", "pred_class_id", "pred_class", "is_correct"],
        suffixes=("_full", "_compact"),
    )
    merged["delta_count_compact_minus_full"] = merged["count_compact"] - merged["count_full"]
    merged["delta_row_rate_compact_minus_full"] = merged["row_rate_compact"] - merged["row_rate_full"]
    merged["compact_model"] = compact_name
    return merged.sort_values(
        ["delta_row_rate_compact_minus_full", "delta_count_compact_minus_full"],
        ascending=[True, True],
        ignore_index=True,
    )


def merge_class_comparison(full_class: pd.DataFrame, compact_class: pd.DataFrame, compact_name: str) -> pd.DataFrame:
    merged = full_class.merge(
        compact_class,
        on=["class_id", "class_name", "support"],
        suffixes=("_full", "_compact"),
    )
    for metric in ["precision", "recall", "f1"]:
        merged[f"delta_{metric}_compact_minus_full"] = merged[f"{metric}_compact"] - merged[f"{metric}_full"]
    merged["compact_model"] = compact_name
    return merged


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
    y_valid = valid_df["label"].to_numpy(dtype=np.int64)

    full_pred = fit_predict(
        train_df=train_df,
        valid_df=valid_df,
        features=FEATURE_ORDER,
        random_state=args.random_state,
    )
    compact_pred = fit_predict(
        train_df=train_df,
        valid_df=valid_df,
        features=compact_features,
        random_state=args.random_state,
    )

    full_counts, full_routes, full_class = build_confusion_frames("full_58", y_valid, full_pred)
    compact_counts, compact_routes, compact_class = build_confusion_frames(compact_name, y_valid, compact_pred)

    all_counts = pd.concat([full_counts, compact_counts], ignore_index=True)
    all_routes = pd.concat([full_routes, compact_routes], ignore_index=True)
    all_class = pd.concat([full_class, compact_class], ignore_index=True)

    route_comparison = merge_route_comparison(full_routes, compact_routes, compact_name)
    class_comparison = merge_class_comparison(full_class, compact_class, compact_name)

    improved_routes = route_comparison.loc[
        route_comparison["delta_row_rate_compact_minus_full"].lt(0)
    ].head(3).copy()
    worsened_routes = route_comparison.loc[
        route_comparison["delta_row_rate_compact_minus_full"].gt(0)
    ].sort_values(
        ["delta_row_rate_compact_minus_full", "delta_count_compact_minus_full"],
        ascending=[False, False],
        ignore_index=True,
    ).head(3)
    recall_gains = class_comparison.sort_values("delta_recall_compact_minus_full", ascending=False, ignore_index=True)

    all_counts.to_csv(RUN_DIR / "confusion_counts.csv", index=False)
    all_routes.to_csv(RUN_DIR / "misclassification_routes.csv", index=False)
    all_class.to_csv(RUN_DIR / "class_metrics.csv", index=False)
    route_comparison.to_csv(RUN_DIR / "misclassification_route_comparison.csv", index=False)
    class_comparison.to_csv(RUN_DIR / "class_metric_comparison.csv", index=False)

    summary_payload = {
        "generated_at_utc": utc_now_iso(),
        "phase": "01K_confusion_patterns",
        "source_final_selection_json": str(final_selection_path.relative_to(ROOT_DIR)),
        "source_final_run_name": final_selection["final_stage01_run_name"],
        "source_compact_summary_json": str(compact_summary_path.relative_to(ROOT_DIR)),
        "dataset_path": run_config["dataset_path"],
        "fit_split": "train",
        "eval_split": "valid",
        "full_model": "full_58",
        "compact_model": compact_name,
        "largest_improved_routes": improved_routes.to_dict(orient="records"),
        "largest_worsened_routes": worsened_routes.to_dict(orient="records"),
        "class_metric_comparison": class_comparison.to_dict(orient="records"),
    }
    write_json(RUN_DIR / "summary.json", summary_payload)
    write_json(REVIEW_JSON, summary_payload)

    lines = [
        "# 01K Confusion Patterns Review",
        "",
        f"Generated at: `{summary_payload['generated_at_utc']}`",
        "",
        "## Scope",
        "",
        "- purpose: `compare class confusion structure between the frozen full baseline and the recommended compact candidate`",
        "- model family: `logistic_regression`",
        "- fit split: `train`",
        "- eval split: `valid`",
        "- held-out test: `not touched in 01K`",
        "",
        "## Class Metric Delta",
        "",
        "| class | recall delta compact-full | precision delta compact-full | f1 delta compact-full |",
        "| --- | ---: | ---: | ---: |",
    ]

    for row in recall_gains.itertuples(index=False):
        lines.append(
            f"| `{row.class_name}` | {row.delta_recall_compact_minus_full:.4f} | {row.delta_precision_compact_minus_full:.4f} | {row.delta_f1_compact_minus_full:.4f} |"
        )

    lines.extend(
        [
            "",
            "## Biggest Reduced Error Routes",
            "",
            "| true -> pred | full row rate | compact row rate | delta compact-full | count delta |",
            "| --- | ---: | ---: | ---: | ---: |",
        ]
    )

    for row in improved_routes.itertuples(index=False):
        lines.append(
            f"| `{row.true_class}->{row.pred_class}` | {row.row_rate_full:.4f} | {row.row_rate_compact:.4f} | {row.delta_row_rate_compact_minus_full:.4f} | {row.delta_count_compact_minus_full} |"
        )

    lines.extend(
        [
            "",
            "## Biggest Expanded Error Routes",
            "",
            "| true -> pred | full row rate | compact row rate | delta compact-full | count delta |",
            "| --- | ---: | ---: | ---: | ---: |",
        ]
    )

    for row in worsened_routes.itertuples(index=False):
        lines.append(
            f"| `{row.true_class}->{row.pred_class}` | {row.row_rate_full:.4f} | {row.row_rate_compact:.4f} | {row.delta_row_rate_compact_minus_full:.4f} | {row.delta_count_compact_minus_full} |"
        )

    lines.extend(
        [
            "",
            "## Notes",
            "",
            "- Negative route delta means the compact candidate reduced that specific error route.",
            "- Positive route delta means the compact candidate made that route more often.",
            "- This stays inside post-selection diagnostics and does not replace the frozen 01D handoff.",
            "",
            "## Artifacts",
            "",
            "- confusion counts: `02_runs/archived/01K_run_0001_confusion_patterns/confusion_counts.csv`",
            "- class metrics: `02_runs/archived/01K_run_0001_confusion_patterns/class_metrics.csv`",
            "- route comparison: `02_runs/archived/01K_run_0001_confusion_patterns/misclassification_route_comparison.csv`",
            "- class comparison: `02_runs/archived/01K_run_0001_confusion_patterns/class_metric_comparison.csv`",
        ]
    )
    write_text(REVIEW_MD, "\n".join(lines) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
