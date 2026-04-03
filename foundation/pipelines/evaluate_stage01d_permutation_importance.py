#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import joblib
import pandas as pd
from sklearn.inspection import permutation_importance
from sklearn.metrics import accuracy_score, balanced_accuracy_score, f1_score, log_loss

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from foundation.features.catalog import FEATURE_ORDER
from foundation.pipelines.run_stage01b_model_compare import write_json, write_text


UTC = timezone.utc


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Evaluate Stage 01D final model permutation importance on the held-out test split."
    )
    parser.add_argument(
        "--final-selection-json",
        default="stages/01_base_feature_ml/04_selected/01D_final_stage01_selection.json",
        help="Stage 01D final selection JSON path",
    )
    parser.add_argument(
        "--stage-root",
        default="stages/01_base_feature_ml",
        help="Stage 01 root directory",
    )
    parser.add_argument(
        "--n-repeats",
        type=int,
        default=20,
        help="Number of shuffle repeats for permutation importance",
    )
    parser.add_argument(
        "--random-state",
        type=int,
        default=42,
        help="Deterministic random seed",
    )
    parser.add_argument(
        "--top-k",
        type=int,
        default=15,
        help="Top features to include in the markdown summary",
    )
    return parser


def utc_now_iso() -> str:
    return datetime.now(tz=UTC).isoformat()


def main() -> int:
    args = build_parser().parse_args()

    final_selection_path = ROOT_DIR / args.final_selection_json
    stage_root = ROOT_DIR / args.stage_root

    final_selection = json.loads(final_selection_path.read_text(encoding="utf-8"))
    final_run_name = final_selection["final_stage01_run_name"]
    run_dir = stage_root / "02_runs" / "active" / final_run_name

    run_config = json.loads((run_dir / "config.json").read_text(encoding="utf-8"))
    model = joblib.load(run_dir / "model.joblib")
    dataset_path = ROOT_DIR / run_config["dataset_path"]
    dataset = pd.read_parquet(dataset_path)
    test_df = dataset.loc[dataset["split"].eq("test")].copy()

    x_test = test_df[FEATURE_ORDER]
    y_test = test_df["label"]

    y_pred = model.predict(x_test)
    y_proba = model.predict_proba(x_test)

    base_metrics = {
        "macro_f1": float(f1_score(y_test, y_pred, average="macro")),
        "balanced_accuracy": float(balanced_accuracy_score(y_test, y_pred)),
        "accuracy": float(accuracy_score(y_test, y_pred)),
        "log_loss": float(log_loss(y_test, y_proba, labels=[0, 1, 2])),
    }

    perm = permutation_importance(
        model,
        x_test,
        y_test,
        scoring="f1_macro",
        n_repeats=args.n_repeats,
        random_state=args.random_state,
        n_jobs=-1,
    )

    importance_df = pd.DataFrame(
        {
            "feature": FEATURE_ORDER,
            "importance_mean": perm.importances_mean,
            "importance_std": perm.importances_std,
        }
    ).sort_values(["importance_mean", "importance_std"], ascending=[False, False], ignore_index=True)
    importance_df["rank"] = importance_df.index + 1
    importance_df["importance_pct_of_base_macro_f1"] = importance_df["importance_mean"] / base_metrics["macro_f1"]

    csv_path = stage_root / "03_reviews" / "01D_permutation_importance.csv"
    json_path = stage_root / "03_reviews" / "01D_permutation_importance.json"
    md_path = stage_root / "03_reviews" / "01D_permutation_importance.md"

    importance_df.to_csv(csv_path, index=False)

    payload = {
        "generated_at_utc": utc_now_iso(),
        "phase": "01D_feature_importance_review",
        "run_name": final_run_name,
        "model_family": final_selection["final_model_family"],
        "dataset_path": str(dataset_path.relative_to(ROOT_DIR)),
        "split_used": "test",
        "scoring": "f1_macro",
        "n_repeats": int(args.n_repeats),
        "random_state": int(args.random_state),
        "test_row_count": int(len(test_df)),
        "base_metrics": base_metrics,
        "top_features": importance_df.head(args.top_k).to_dict(orient="records"),
    }
    write_json(json_path, payload)

    top_lines = [
        "# 01D Permutation Importance Review",
        "",
        f"Generated at: `{payload['generated_at_utc']}`",
        "",
        "## Scope",
        "",
        f"- run: `{final_run_name}`",
        f"- model: `{final_selection['final_model_family']}`",
        "- split: `test`",
        "- scoring: `macro_f1`",
        f"- repeats: `{args.n_repeats}`",
        "",
        "## Base Test Metrics",
        "",
        f"- macro_f1: `{base_metrics['macro_f1']:.4f}`",
        f"- balanced_accuracy: `{base_metrics['balanced_accuracy']:.4f}`",
        f"- accuracy: `{base_metrics['accuracy']:.4f}`",
        f"- log_loss: `{base_metrics['log_loss']:.4f}`",
        "",
        "## Top Features",
        "",
        "| rank | feature | mean drop in macro_f1 | std |",
        "| --- | --- | ---: | ---: |",
    ]

    for row in importance_df.head(args.top_k).itertuples(index=False):
        top_lines.append(
            f"| {row.rank} | `{row.feature}` | {row.importance_mean:.6f} | {row.importance_std:.6f} |"
        )

    top_lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- Higher mean drop means the model loses more test macro_f1 when that feature is shuffled.",
            "- This is a better practical proxy for feature contribution than raw coefficients alone.",
            "- Near-zero or negative values usually mean the feature adds little stable test-time value on its own.",
            "",
            "## Artifacts",
            "",
            f"- full csv: `{csv_path.relative_to(ROOT_DIR)}`",
            f"- summary json: `{json_path.relative_to(ROOT_DIR)}`",
        ]
    )
    write_text(md_path, "\n".join(top_lines) + "\n")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
