#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np
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
from foundation.pipelines.run_stage01f_sector_ablation import (
    SECTOR_MAP,
    STAGE_ROOT,
    load_context,
    utc_now_iso,
    validate_sector_map,
)


RUN_DIR = STAGE_ROOT / "02_runs" / "archived" / "01H_run_0001_compact_candidate_compare"
REVIEW_MD = STAGE_ROOT / "03_reviews" / "01H_compact_candidate_compare_review.md"
REVIEW_JSON = STAGE_ROOT / "03_reviews" / "01H_compact_candidate_compare_review.json"


VARIANTS: list[tuple[str, tuple[str, ...]]] = [
    ("full_58", ()),
    ("compact_50_without_volatility_band", ("volatility_band",)),
    ("compact_42_without_volatility_band__leader_relative", ("volatility_band", "leader_relative")),
    ("compact_36_without_volatility_band__risk_proxy__leader_relative", ("volatility_band", "risk_proxy", "leader_relative")),
]


@dataclass
class VariantResult:
    variant: str
    removed_sectors: str
    num_removed_features: int
    num_features: int
    train_macro_f1: float
    train_balanced_accuracy: float
    train_accuracy: float
    train_log_loss: float
    valid_macro_f1: float
    valid_balanced_accuracy: float
    valid_accuracy: float
    valid_log_loss: float


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Stage 01H compact candidate comparison.")
    parser.add_argument(
        "--final-selection-json",
        default="stages/01_base_feature_ml/04_selected/01D_final_stage01_selection.json",
        help="Stage 01D final selection JSON",
    )
    parser.add_argument(
        "--random-state",
        type=int,
        default=42,
        help="Random state for logistic regression",
    )
    return parser.parse_args()


def build_feature_subset(removed_sector_names: tuple[str, ...]) -> tuple[list[str], int]:
    removed_features = {
        feature
        for sector_name in removed_sector_names
        for feature in SECTOR_MAP[sector_name]
    }
    kept_features = [feature for feature in FEATURE_ORDER if feature not in removed_features]
    return kept_features, len(removed_features)


def fit_variant(
    train_df: pd.DataFrame,
    valid_df: pd.DataFrame,
    variant_name: str,
    removed_sector_names: tuple[str, ...],
    random_state: int,
) -> VariantResult:
    features, num_removed_features = build_feature_subset(removed_sector_names)
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
    model.fit(train_df[features], train_df["label"])

    train_proba = model.predict_proba(train_df[features])
    train_pred = np.argmax(train_proba, axis=1)
    y_train = train_df["label"].to_numpy(dtype=np.int64)

    valid_proba = model.predict_proba(valid_df[features])
    valid_pred = np.argmax(valid_proba, axis=1)
    y_valid = valid_df["label"].to_numpy(dtype=np.int64)

    return VariantResult(
        variant=variant_name,
        removed_sectors=",".join(removed_sector_names),
        num_removed_features=num_removed_features,
        num_features=len(features),
        train_macro_f1=float(f1_score(y_train, train_pred, average="macro")),
        train_balanced_accuracy=float(balanced_accuracy_score(y_train, train_pred)),
        train_accuracy=float(accuracy_score(y_train, train_pred)),
        train_log_loss=float(log_loss(y_train, train_proba, labels=[0, 1, 2])),
        valid_macro_f1=float(f1_score(y_valid, valid_pred, average="macro")),
        valid_balanced_accuracy=float(balanced_accuracy_score(y_valid, valid_pred)),
        valid_accuracy=float(accuracy_score(y_valid, valid_pred)),
        valid_log_loss=float(log_loss(y_valid, valid_proba, labels=[0, 1, 2])),
    )


def main() -> int:
    args = parse_args()
    validate_sector_map()

    if RUN_DIR.exists():
        shutil.rmtree(RUN_DIR)
    RUN_DIR.mkdir(parents=True, exist_ok=True)

    final_selection_path = ROOT_DIR / args.final_selection_json
    final_selection, run_config, dataset = load_context(final_selection_path)

    train_df = dataset.loc[dataset["split"].eq("train")].copy()
    valid_df = dataset.loc[dataset["split"].eq("valid")].copy()

    results = [
        fit_variant(
            train_df=train_df,
            valid_df=valid_df,
            variant_name=variant_name,
            removed_sector_names=removed_sector_names,
            random_state=args.random_state,
        )
        for variant_name, removed_sector_names in VARIANTS
    ]

    result_df = pd.DataFrame([asdict(item) for item in results])

    baseline_row = result_df.loc[result_df["variant"].eq("full_58")].iloc[0]
    result_df["delta_valid_macro_f1_vs_full"] = result_df["valid_macro_f1"] - float(baseline_row["valid_macro_f1"])
    result_df["delta_valid_balanced_accuracy_vs_full"] = result_df["valid_balanced_accuracy"] - float(baseline_row["valid_balanced_accuracy"])
    result_df["delta_valid_accuracy_vs_full"] = result_df["valid_accuracy"] - float(baseline_row["valid_accuracy"])
    result_df["delta_valid_log_loss_vs_full"] = result_df["valid_log_loss"] - float(baseline_row["valid_log_loss"])
    result_df["macro_f1_gap_train_minus_valid"] = result_df["train_macro_f1"] - result_df["valid_macro_f1"]
    result_df["balanced_accuracy_gap_train_minus_valid"] = result_df["train_balanced_accuracy"] - result_df["valid_balanced_accuracy"]
    result_df["accuracy_gap_train_minus_valid"] = result_df["train_accuracy"] - result_df["valid_accuracy"]
    result_df["log_loss_gap_valid_minus_train"] = result_df["valid_log_loss"] - result_df["train_log_loss"]

    sorted_df = result_df.sort_values(
        ["valid_macro_f1", "valid_balanced_accuracy", "num_features"],
        ascending=[False, False, True],
        ignore_index=True,
    )

    best_raw = sorted_df.iloc[0].to_dict()
    compact_df = sorted_df.loc[sorted_df["variant"].ne("full_58")].copy()
    compact_recommended = compact_df.sort_values(
        ["valid_macro_f1", "num_features", "macro_f1_gap_train_minus_valid"],
        ascending=[False, True, True],
        ignore_index=True,
    ).iloc[0].to_dict()

    feature_sets = {}
    for variant_name, removed_sector_names in VARIANTS:
        features, num_removed_features = build_feature_subset(removed_sector_names)
        feature_sets[variant_name] = {
            "removed_sectors": list(removed_sector_names),
            "num_removed_features": num_removed_features,
            "num_features": len(features),
            "features": features,
        }

    result_df.to_csv(RUN_DIR / "compact_candidate_results.csv", index=False)
    sorted_df.to_csv(RUN_DIR / "compact_candidate_sorted.csv", index=False)
    write_json(RUN_DIR / "feature_sets.json", feature_sets)
    write_json(
        RUN_DIR / "config.json",
        {
            "generated_at_utc": utc_now_iso(),
            "phase": "01H_compact_candidate_compare",
            "source_final_selection_json": str(final_selection_path.relative_to(ROOT_DIR)),
            "source_final_run_name": final_selection["final_stage01_run_name"],
            "dataset_path": run_config["dataset_path"],
            "fit_split": "train",
            "eval_split": "valid",
            "random_state": int(args.random_state),
            "variants": [
                {"variant": variant_name, "removed_sectors": list(removed_sector_names)}
                for variant_name, removed_sector_names in VARIANTS
            ],
        },
    )

    summary_payload = {
        "generated_at_utc": utc_now_iso(),
        "phase": "01H_compact_candidate_compare",
        "baseline_variant": baseline_row.to_dict(),
        "best_valid_variant": best_raw,
        "recommended_compact_variant": compact_recommended,
        "all_variants": sorted_df.to_dict(orient="records"),
    }
    write_json(RUN_DIR / "summary.json", summary_payload)
    write_json(REVIEW_JSON, summary_payload)

    lines = [
        "# 01H Compact Candidate Compare Review",
        "",
        f"Generated at: `{summary_payload['generated_at_utc']}`",
        "",
        "## Scope",
        "",
        "- purpose: `compare the strongest compact candidates from 01G against the frozen full baseline`",
        "- model family: `logistic_regression`",
        "- fit split: `train`",
        "- eval split: `valid`",
        "- held-out test: `not touched in 01H`",
        "",
        "## Ranking",
        "",
        "| variant | features | removed sectors | valid macro_f1 | delta vs full | train-valid macro_f1 gap |",
        "| --- | ---: | --- | ---: | ---: | ---: |",
    ]

    for row in sorted_df.itertuples(index=False):
        removed_label = row.removed_sectors if row.removed_sectors else "-"
        lines.append(
            f"| `{row.variant}` | {row.num_features} | `{removed_label}` | {row.valid_macro_f1:.4f} | {row.delta_valid_macro_f1_vs_full:.4f} | {row.macro_f1_gap_train_minus_valid:.4f} |"
        )

    lines.extend(
        [
            "",
            "## Practical Read",
            "",
            f"- best raw valid score: `{best_raw['variant']}` (`{best_raw['valid_macro_f1']:.4f}`)",
            f"- recommended compact candidate: `{compact_recommended['variant']}` with `{int(compact_recommended['num_features'])}` features",
            "- recommendation rule: prefer the strongest compact variant, but break ties toward fewer features when the score difference is small.",
            "",
            "## Notes",
            "",
            "- This phase compares compact variants only on the existing train/valid split.",
            "- It is still a diagnostic pass and does not replace the frozen 01D selection.",
            "- A recommended compact candidate here is only a candidate for later dedicated compact-model or stability checks.",
            "",
            "## Artifacts",
            "",
            "- full table: `02_runs/archived/01H_run_0001_compact_candidate_compare/compact_candidate_results.csv`",
            "- sorted table: `02_runs/archived/01H_run_0001_compact_candidate_compare/compact_candidate_sorted.csv`",
            "- feature sets: `02_runs/archived/01H_run_0001_compact_candidate_compare/feature_sets.json`",
        ]
    )
    write_text(REVIEW_MD, "\n".join(lines) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
