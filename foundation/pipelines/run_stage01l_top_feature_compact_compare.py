#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, balanced_accuracy_score, f1_score, log_loss
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from foundation.features.catalog import FEATURE_ORDER
from foundation.pipelines.run_stage01b_model_compare import write_json, write_text
from foundation.pipelines.run_stage01f_sector_ablation import STAGE_ROOT, load_context, utc_now_iso


RUN_DIR = STAGE_ROOT / "02_runs" / "archived" / "01L_run_0001_top_feature_compact_compare"
REVIEW_MD = STAGE_ROOT / "03_reviews" / "01L_top_feature_compact_compare_review.md"
REVIEW_JSON = STAGE_ROOT / "03_reviews" / "01L_top_feature_compact_compare_review.json"
SOURCE_01H_RUN_DIR = STAGE_ROOT / "02_runs" / "archived" / "01H_run_0001_compact_candidate_compare"
DEFAULT_TOP_K = [8, 12, 16, 24, 36]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Stage 01L top-feature compact comparison.")
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
        "--permutation-csv",
        default="stages/01_base_feature_ml/03_reviews/01D_permutation_importance.csv",
        help="Permutation importance CSV used as ranking source",
    )
    parser.add_argument(
        "--top-k",
        nargs="+",
        type=int,
        default=DEFAULT_TOP_K,
        help="Top-k feature counts to compare",
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


def load_ranked_features(permutation_csv_path: Path) -> list[str]:
    perm_df = pd.read_csv(permutation_csv_path)
    perm_df = perm_df.sort_values("rank", ascending=True, kind="stable", ignore_index=True)
    ranked_features = perm_df["feature"].tolist()
    missing = [feature for feature in ranked_features if feature not in FEATURE_ORDER]
    if missing:
        raise ValueError(f"permutation ranking contains unknown features: {missing}")
    return ranked_features


def fit_eval_variant(
    train_df: pd.DataFrame,
    valid_df: pd.DataFrame,
    features: list[str],
    random_state: int,
) -> dict[str, float]:
    model = build_model(random_state=random_state)
    model.fit(train_df[features], train_df["label"])

    train_proba = model.predict_proba(train_df[features])
    train_pred = model.predict(train_df[features])
    valid_proba = model.predict_proba(valid_df[features])
    valid_pred = model.predict(valid_df[features])

    return {
        "train_macro_f1": float(f1_score(train_df["label"], train_pred, average="macro")),
        "train_balanced_accuracy": float(balanced_accuracy_score(train_df["label"], train_pred)),
        "train_accuracy": float(accuracy_score(train_df["label"], train_pred)),
        "train_log_loss": float(log_loss(train_df["label"], train_proba, labels=[0, 1, 2])),
        "valid_macro_f1": float(f1_score(valid_df["label"], valid_pred, average="macro")),
        "valid_balanced_accuracy": float(balanced_accuracy_score(valid_df["label"], valid_pred)),
        "valid_accuracy": float(accuracy_score(valid_df["label"], valid_pred)),
        "valid_log_loss": float(log_loss(valid_df["label"], valid_proba, labels=[0, 1, 2])),
    }


def main() -> int:
    args = parse_args()
    top_k_values = sorted(set(int(value) for value in args.top_k))
    if any(value <= 0 or value > len(FEATURE_ORDER) for value in top_k_values):
        raise ValueError(f"top-k must be between 1 and {len(FEATURE_ORDER)}")

    if RUN_DIR.exists():
        shutil.rmtree(RUN_DIR)
    RUN_DIR.mkdir(parents=True, exist_ok=True)

    final_selection_path = ROOT_DIR / args.final_selection_json
    compact_summary_path = ROOT_DIR / args.compact_summary_json
    compact_feature_sets_path = ROOT_DIR / args.compact_feature_sets_json
    permutation_csv_path = ROOT_DIR / args.permutation_csv

    final_selection, run_config, dataset = load_context(final_selection_path)
    compact_name, compact_features = load_compact_candidate(compact_summary_path, compact_feature_sets_path)
    ranked_features = load_ranked_features(permutation_csv_path)

    train_df = dataset.loc[dataset["split"].eq("train")].copy()
    valid_df = dataset.loc[dataset["split"].eq("valid")].copy()

    variant_feature_sets: dict[str, list[str]] = {
        "full_58": list(FEATURE_ORDER),
        compact_name: compact_features,
    }
    for top_k in top_k_values:
        variant_feature_sets[f"top_{top_k:02d}_perm"] = ranked_features[:top_k]

    result_rows: list[dict] = []
    feature_set_payload: dict[str, dict] = {}
    compact_feature_set = set(compact_features)

    for variant_name, features in variant_feature_sets.items():
        metrics = fit_eval_variant(
            train_df=train_df,
            valid_df=valid_df,
            features=features,
            random_state=args.random_state,
        )
        overlap_with_compact = len(set(features) & compact_feature_set)
        result_rows.append(
            {
                "variant": variant_name,
                "num_features": len(features),
                "overlap_with_compact_36": overlap_with_compact,
                "overlap_ratio_with_compact_36": float(overlap_with_compact / len(compact_features)),
                **metrics,
            }
        )
        feature_set_payload[variant_name] = {
            "num_features": len(features),
            "features": features,
            "overlap_with_compact_36": overlap_with_compact,
            "overlap_ratio_with_compact_36": float(overlap_with_compact / len(compact_features)),
        }

    result_df = pd.DataFrame(result_rows)
    baseline_row = result_df.loc[result_df["variant"].eq("full_58")].iloc[0]
    compact_row = result_df.loc[result_df["variant"].eq(compact_name)].iloc[0]

    result_df["delta_valid_macro_f1_vs_full"] = result_df["valid_macro_f1"] - float(baseline_row["valid_macro_f1"])
    result_df["delta_valid_balanced_accuracy_vs_full"] = result_df["valid_balanced_accuracy"] - float(baseline_row["valid_balanced_accuracy"])
    result_df["delta_valid_accuracy_vs_full"] = result_df["valid_accuracy"] - float(baseline_row["valid_accuracy"])
    result_df["delta_valid_log_loss_vs_full"] = result_df["valid_log_loss"] - float(baseline_row["valid_log_loss"])
    result_df["delta_valid_macro_f1_vs_compact_36"] = result_df["valid_macro_f1"] - float(compact_row["valid_macro_f1"])
    result_df["macro_f1_gap_train_minus_valid"] = result_df["train_macro_f1"] - result_df["valid_macro_f1"]

    sorted_df = result_df.sort_values(
        ["valid_macro_f1", "valid_balanced_accuracy", "num_features"],
        ascending=[False, False, True],
        ignore_index=True,
    )

    top_feature_only_df = sorted_df.loc[sorted_df["variant"].str.startswith("top_")].copy()
    best_top_feature_variant = top_feature_only_df.iloc[0].to_dict()
    compact_advantage = float(compact_row["valid_macro_f1"] - best_top_feature_variant["valid_macro_f1"])

    result_df.to_csv(RUN_DIR / "top_feature_compact_results.csv", index=False)
    sorted_df.to_csv(RUN_DIR / "top_feature_compact_sorted.csv", index=False)
    write_json(RUN_DIR / "feature_sets.json", feature_set_payload)
    write_json(
        RUN_DIR / "config.json",
        {
            "generated_at_utc": utc_now_iso(),
            "phase": "01L_top_feature_compact_compare",
            "source_final_selection_json": str(final_selection_path.relative_to(ROOT_DIR)),
            "source_final_run_name": final_selection["final_stage01_run_name"],
            "source_compact_summary_json": str(compact_summary_path.relative_to(ROOT_DIR)),
            "source_permutation_csv": str(permutation_csv_path.relative_to(ROOT_DIR)),
            "dataset_path": run_config["dataset_path"],
            "fit_split": "train",
            "eval_split": "valid",
            "random_state": int(args.random_state),
            "top_k_values": top_k_values,
        },
    )

    summary_payload = {
        "generated_at_utc": utc_now_iso(),
        "phase": "01L_top_feature_compact_compare",
        "ranking_source": "01D permutation importance on held-out test",
        "best_top_feature_variant": best_top_feature_variant,
        "compact_variant": compact_row.to_dict(),
        "full_variant": baseline_row.to_dict(),
        "compact_macro_f1_advantage_over_best_top_feature": compact_advantage,
        "all_variants": sorted_df.to_dict(orient="records"),
    }
    write_json(RUN_DIR / "summary.json", summary_payload)
    write_json(REVIEW_JSON, summary_payload)

    lines = [
        "# 01L Top-Feature Compact Compare Review",
        "",
        f"Generated at: `{summary_payload['generated_at_utc']}`",
        "",
        "## Scope",
        "",
        "- purpose: `compare sector-pruned compact modeling against simple top-feature-only compact variants`",
        "- model family: `logistic_regression`",
        "- fit split: `train`",
        "- eval split: `valid`",
        "- held-out test: `not touched in 01L`",
        "- ranking source: `01D permutation importance on held-out test`",
        "",
        "## Ranking",
        "",
        "| variant | features | overlap with compact_36 | valid macro_f1 | delta vs full | delta vs compact_36 |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
    ]

    for row in sorted_df.itertuples(index=False):
        lines.append(
            f"| `{row.variant}` | {row.num_features} | {row.overlap_with_compact_36} | {row.valid_macro_f1:.4f} | {row.delta_valid_macro_f1_vs_full:.4f} | {row.delta_valid_macro_f1_vs_compact_36:.4f} |"
        )

    lines.extend(
        [
            "",
            "## Read",
            "",
            f"- best top-feature-only variant: `{best_top_feature_variant['variant']}` (`{best_top_feature_variant['valid_macro_f1']:.4f}`)",
            f"- compact_36 advantage over best top-feature variant: `{compact_advantage:.4f}`",
            f"- compact_36 overlap with `{best_top_feature_variant['variant']}`: `{int(best_top_feature_variant['overlap_with_compact_36'])}` features",
            "",
            "## Notes",
            "",
            "- This is review-only. The ranking source comes from test-based permutation importance, so it should not be used to replace the frozen 01D handoff.",
            "- The point here is not reselection but to check whether a very simple top-feature subset can approach the compact sector-pruned variant.",
            "",
            "## Artifacts",
            "",
            "- full table: `02_runs/archived/01L_run_0001_top_feature_compact_compare/top_feature_compact_results.csv`",
            "- sorted table: `02_runs/archived/01L_run_0001_top_feature_compact_compare/top_feature_compact_sorted.csv`",
            "- feature sets: `02_runs/archived/01L_run_0001_top_feature_compact_compare/feature_sets.json`",
        ]
    )
    write_text(REVIEW_MD, "\n".join(lines) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
