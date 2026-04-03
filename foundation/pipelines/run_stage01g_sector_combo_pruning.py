#!/usr/bin/env python3
from __future__ import annotations

import argparse
import itertools
import json
import shutil
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

import pandas as pd

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from foundation.pipelines.run_stage01b_model_compare import write_json, write_text
from foundation.pipelines.run_stage01f_sector_ablation import (
    REVIEW_JSON as STAGE01F_REVIEW_JSON,
    RUN_DIR as STAGE01F_RUN_DIR,
    SECTOR_MAP,
    STAGE_ROOT,
    fit_and_eval,
    load_context,
    utc_now_iso,
    validate_sector_map,
)


RUN_DIR = STAGE_ROOT / "02_runs" / "archived" / "01G_run_0001_sector_combo_pruning"
REVIEW_MD = STAGE_ROOT / "03_reviews" / "01G_sector_combo_pruning_review.md"
REVIEW_JSON = STAGE_ROOT / "03_reviews" / "01G_sector_combo_pruning_review.json"


@dataclass
class ComboEvalResult:
    variant: str
    removed_sectors: str
    combo_size: int
    num_removed_features: int
    num_features: int
    valid_macro_f1: float
    valid_balanced_accuracy: float
    valid_accuracy: float
    valid_log_loss: float


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Stage 01G sector combination pruning diagnostics.")
    parser.add_argument(
        "--final-selection-json",
        default="stages/01_base_feature_ml/04_selected/01D_final_stage01_selection.json",
        help="Stage 01D final selection JSON",
    )
    parser.add_argument(
        "--source-01f-review-json",
        default=str(STAGE01F_REVIEW_JSON.relative_to(ROOT_DIR)),
        help="Stage 01F summary JSON used to pick candidate sectors",
    )
    parser.add_argument(
        "--random-state",
        type=int,
        default=42,
        help="Random state for logistic regression",
    )
    return parser.parse_args()


def load_candidate_sectors(source_review_path: Path) -> list[str]:
    review_payload = json.loads(source_review_path.read_text(encoding="utf-8"))
    candidate_sectors = [row["removed_sector"] for row in review_payload["most_helpful_removals"]]
    if not candidate_sectors:
        raise ValueError("01F summary did not produce candidate sectors")
    missing = [name for name in candidate_sectors if name not in SECTOR_MAP]
    if missing:
        raise ValueError(f"candidate sectors missing from sector map: {missing}")
    return candidate_sectors


def build_feature_subset(removed_sector_names: tuple[str, ...]) -> tuple[list[str], int]:
    removed_features = {
        feature
        for sector_name in removed_sector_names
        for feature in SECTOR_MAP[sector_name]
    }
    # Preserve the original frozen feature order.
    from foundation.features.catalog import FEATURE_ORDER

    kept_features = [feature for feature in FEATURE_ORDER if feature not in removed_features]
    return kept_features, len(removed_features)


def combo_variant_name(removed_sector_names: tuple[str, ...]) -> str:
    return "combo_without_" + "__".join(removed_sector_names)


def main() -> int:
    args = parse_args()
    validate_sector_map()

    if RUN_DIR.exists():
        shutil.rmtree(RUN_DIR)
    RUN_DIR.mkdir(parents=True, exist_ok=True)

    final_selection_path = ROOT_DIR / args.final_selection_json
    source_review_path = ROOT_DIR / args.source_01f_review_json
    candidate_sectors = load_candidate_sectors(source_review_path)

    final_selection, run_config, dataset = load_context(final_selection_path)
    train_df = dataset.loc[dataset["split"].eq("train")].copy()
    valid_df = dataset.loc[dataset["split"].eq("valid")].copy()

    from foundation.features.catalog import FEATURE_ORDER

    baseline = fit_and_eval(
        train_df=train_df,
        valid_df=valid_df,
        features=FEATURE_ORDER,
        variant="baseline_full",
        removed_sector="",
        random_state=args.random_state,
    )

    results: list[ComboEvalResult] = [
        ComboEvalResult(
            variant="baseline_full",
            removed_sectors="",
            combo_size=0,
            num_removed_features=0,
            num_features=len(FEATURE_ORDER),
            valid_macro_f1=baseline.valid_macro_f1,
            valid_balanced_accuracy=baseline.valid_balanced_accuracy,
            valid_accuracy=baseline.valid_accuracy,
            valid_log_loss=baseline.valid_log_loss,
        )
    ]

    for combo_size in range(1, len(candidate_sectors) + 1):
        for removed_sector_names in itertools.combinations(candidate_sectors, combo_size):
            kept_features, num_removed_features = build_feature_subset(removed_sector_names)
            eval_result = fit_and_eval(
                train_df=train_df,
                valid_df=valid_df,
                features=kept_features,
                variant=combo_variant_name(removed_sector_names),
                removed_sector=",".join(removed_sector_names),
                random_state=args.random_state,
            )
            results.append(
                ComboEvalResult(
                    variant=eval_result.variant,
                    removed_sectors=",".join(removed_sector_names),
                    combo_size=combo_size,
                    num_removed_features=num_removed_features,
                    num_features=len(kept_features),
                    valid_macro_f1=eval_result.valid_macro_f1,
                    valid_balanced_accuracy=eval_result.valid_balanced_accuracy,
                    valid_accuracy=eval_result.valid_accuracy,
                    valid_log_loss=eval_result.valid_log_loss,
                )
            )

    result_df = pd.DataFrame([asdict(item) for item in results])
    result_df["delta_macro_f1_vs_full"] = result_df["valid_macro_f1"] - baseline.valid_macro_f1
    result_df["delta_balanced_accuracy_vs_full"] = result_df["valid_balanced_accuracy"] - baseline.valid_balanced_accuracy
    result_df["delta_accuracy_vs_full"] = result_df["valid_accuracy"] - baseline.valid_accuracy
    result_df["delta_log_loss_vs_full"] = result_df["valid_log_loss"] - baseline.valid_log_loss

    combo_df = result_df.loc[result_df["combo_size"].gt(0)].copy()
    combo_df = combo_df.sort_values(
        ["delta_macro_f1_vs_full", "delta_balanced_accuracy_vs_full"],
        ascending=[False, False],
        ignore_index=True,
    )

    best_single = combo_df.loc[combo_df["combo_size"].eq(1)].head(1)
    best_pair = combo_df.loc[combo_df["combo_size"].eq(2)].head(1)
    best_triple = combo_df.loc[combo_df["combo_size"].eq(3)].head(1)
    top_overall = combo_df.head(5)

    result_df.to_csv(RUN_DIR / "sector_combo_results.csv", index=False)
    combo_df.to_csv(RUN_DIR / "sector_combo_sorted.csv", index=False)
    write_json(
        RUN_DIR / "config.json",
        {
            "generated_at_utc": utc_now_iso(),
            "phase": "01G_sector_combo_pruning",
            "source_final_selection_json": str(final_selection_path.relative_to(ROOT_DIR)),
            "source_01f_review_json": str(source_review_path.relative_to(ROOT_DIR)),
            "source_01f_run_dir": str(STAGE01F_RUN_DIR.relative_to(ROOT_DIR)),
            "source_final_run_name": final_selection["final_stage01_run_name"],
            "dataset_path": run_config["dataset_path"],
            "fit_split": "train",
            "eval_split": "valid",
            "candidate_sectors": candidate_sectors,
            "random_state": int(args.random_state),
        },
    )

    summary_payload = {
        "generated_at_utc": utc_now_iso(),
        "phase": "01G_sector_combo_pruning",
        "candidate_sectors": candidate_sectors,
        "baseline": {
            "valid_macro_f1": baseline.valid_macro_f1,
            "valid_balanced_accuracy": baseline.valid_balanced_accuracy,
            "valid_accuracy": baseline.valid_accuracy,
            "valid_log_loss": baseline.valid_log_loss,
            "num_features": len(FEATURE_ORDER),
        },
        "best_single": best_single.to_dict(orient="records"),
        "best_pair": best_pair.to_dict(orient="records"),
        "best_triple": best_triple.to_dict(orient="records"),
        "top_overall": top_overall.to_dict(orient="records"),
    }
    write_json(RUN_DIR / "summary.json", summary_payload)
    write_json(REVIEW_JSON, summary_payload)

    lines = [
        "# 01G Sector Combo Pruning Review",
        "",
        f"Generated at: `{summary_payload['generated_at_utc']}`",
        "",
        "## Scope",
        "",
        "- purpose: `test whether the helpful single-sector removals from 01F still help when combined`",
        "- model family: `logistic_regression`",
        "- fit split: `train`",
        "- eval split: `valid`",
        "- held-out test: `not touched in 01G`",
        f"- candidate sectors from 01F: `{', '.join(candidate_sectors)}`",
        "",
        "## Full Baseline",
        "",
        f"- valid macro_f1: `{baseline.valid_macro_f1:.4f}`",
        f"- valid balanced_accuracy: `{baseline.valid_balanced_accuracy:.4f}`",
        f"- valid accuracy: `{baseline.valid_accuracy:.4f}`",
        f"- valid log_loss: `{baseline.valid_log_loss:.4f}`",
        "",
        "## Best Single",
        "",
        "| removed sectors | delta macro_f1 vs full | delta balanced_accuracy | removed feature count |",
        "| --- | ---: | ---: | ---: |",
    ]

    for row in best_single.itertuples(index=False):
        lines.append(
            f"| `{row.removed_sectors}` | {row.delta_macro_f1_vs_full:.4f} | {row.delta_balanced_accuracy_vs_full:.4f} | {row.num_removed_features} |"
        )

    lines.extend(
        [
            "",
            "## Best Pair",
            "",
            "| removed sectors | delta macro_f1 vs full | delta balanced_accuracy | removed feature count |",
            "| --- | ---: | ---: | ---: |",
        ]
    )

    for row in best_pair.itertuples(index=False):
        lines.append(
            f"| `{row.removed_sectors}` | {row.delta_macro_f1_vs_full:.4f} | {row.delta_balanced_accuracy_vs_full:.4f} | {row.num_removed_features} |"
        )

    lines.extend(
        [
            "",
            "## Triple Cut",
            "",
            "| removed sectors | delta macro_f1 vs full | delta balanced_accuracy | removed feature count |",
            "| --- | ---: | ---: | ---: |",
        ]
    )

    for row in best_triple.itertuples(index=False):
        lines.append(
            f"| `{row.removed_sectors}` | {row.delta_macro_f1_vs_full:.4f} | {row.delta_balanced_accuracy_vs_full:.4f} | {row.num_removed_features} |"
        )

    lines.extend(
        [
            "",
            "## Top Overall Variants",
            "",
            "| removed sectors | combo size | delta macro_f1 vs full | delta balanced_accuracy | delta accuracy |",
            "| --- | ---: | ---: | ---: | ---: |",
        ]
    )

    for row in top_overall.itertuples(index=False):
        lines.append(
            f"| `{row.removed_sectors}` | {row.combo_size} | {row.delta_macro_f1_vs_full:.4f} | {row.delta_balanced_accuracy_vs_full:.4f} | {row.delta_accuracy_vs_full:.4f} |"
        )

    lines.extend(
        [
            "",
            "## Notes",
            "",
            "- This phase stays inside post-selection diagnostics and does not replace the frozen Stage 01 final baseline.",
            "- Strong pair or triple gains suggest a compact variant worth revisiting later as a dedicated compact-model phase.",
            "- Weak pair or triple gains suggest the single-sector improvement was local and should not be over-read.",
            "",
            "## Artifacts",
            "",
            "- full table: `02_runs/archived/01G_run_0001_sector_combo_pruning/sector_combo_results.csv`",
            "- sorted table: `02_runs/archived/01G_run_0001_sector_combo_pruning/sector_combo_sorted.csv`",
        ]
    )
    write_text(REVIEW_MD, "\n".join(lines) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
