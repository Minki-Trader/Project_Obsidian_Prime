#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
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
from foundation.features.sector_map import SECTOR_MAP, validate_sector_map
from foundation.pipelines.run_stage01b_model_compare import write_json, write_text


UTC = timezone.utc

STAGE_ROOT = ROOT_DIR / "stages" / "01_base_feature_ml"
RUN_DIR = STAGE_ROOT / "02_runs" / "archived" / "01F_run_0001_sector_ablation"
REVIEW_MD = STAGE_ROOT / "03_reviews" / "01F_sector_ablation_review.md"
REVIEW_JSON = STAGE_ROOT / "03_reviews" / "01F_sector_ablation_review.json"


@dataclass
class EvalResult:
    variant: str
    removed_sector: str
    num_features: int
    valid_macro_f1: float
    valid_balanced_accuracy: float
    valid_accuracy: float
    valid_log_loss: float


def utc_now_iso() -> str:
    return datetime.now(tz=UTC).isoformat()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Stage 01F sector ablation diagnostics.")
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

def fit_and_eval(
    train_df: pd.DataFrame,
    valid_df: pd.DataFrame,
    features: list[str],
    variant: str,
    removed_sector: str,
    random_state: int,
) -> EvalResult:
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
    valid_proba = model.predict_proba(valid_df[features])
    valid_pred = np.argmax(valid_proba, axis=1)
    y_valid = valid_df["label"].to_numpy(dtype=np.int64)
    return EvalResult(
        variant=variant,
        removed_sector=removed_sector,
        num_features=len(features),
        valid_macro_f1=float(f1_score(y_valid, valid_pred, average="macro")),
        valid_balanced_accuracy=float(balanced_accuracy_score(y_valid, valid_pred)),
        valid_accuracy=float(accuracy_score(y_valid, valid_pred)),
        valid_log_loss=float(log_loss(y_valid, valid_proba, labels=[0, 1, 2])),
    )


def load_context(final_selection_path: Path) -> tuple[dict, dict, pd.DataFrame]:
    final_selection = json.loads(final_selection_path.read_text(encoding="utf-8"))
    final_run_name = final_selection["final_stage01_run_name"]
    final_run_dir = STAGE_ROOT / "02_runs" / "active" / final_run_name
    run_config = json.loads((final_run_dir / "config.json").read_text(encoding="utf-8"))
    dataset_path = ROOT_DIR / run_config["dataset_path"]
    dataset = pd.read_parquet(dataset_path)
    return final_selection, run_config, dataset


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

    baseline = fit_and_eval(
        train_df=train_df,
        valid_df=valid_df,
        features=FEATURE_ORDER,
        variant="baseline_full",
        removed_sector="",
        random_state=args.random_state,
    )

    results: list[EvalResult] = [baseline]
    for sector_name, sector_features in SECTOR_MAP.items():
        kept_features = [feature for feature in FEATURE_ORDER if feature not in sector_features]
        results.append(
            fit_and_eval(
                train_df=train_df,
                valid_df=valid_df,
                features=kept_features,
                variant=f"ablation_without_{sector_name}",
                removed_sector=sector_name,
                random_state=args.random_state,
            )
        )

    result_df = pd.DataFrame([asdict(item) for item in results])
    result_df["delta_macro_f1_vs_full"] = result_df["valid_macro_f1"] - baseline.valid_macro_f1
    result_df["delta_balanced_accuracy_vs_full"] = result_df["valid_balanced_accuracy"] - baseline.valid_balanced_accuracy
    result_df["delta_accuracy_vs_full"] = result_df["valid_accuracy"] - baseline.valid_accuracy
    result_df["delta_log_loss_vs_full"] = result_df["valid_log_loss"] - baseline.valid_log_loss

    ablation_df = result_df[result_df["removed_sector"].ne("")].copy()
    ablation_df = ablation_df.sort_values(
        ["delta_macro_f1_vs_full", "delta_balanced_accuracy_vs_full"],
        ascending=[True, True],
        ignore_index=True,
    )

    strongest_drop = ablation_df.head(3).copy()
    strongest_gain = ablation_df.sort_values(
        ["delta_macro_f1_vs_full", "delta_balanced_accuracy_vs_full"],
        ascending=[False, False],
        ignore_index=True,
    ).head(3)

    result_df.to_csv(RUN_DIR / "sector_ablation_results.csv", index=False)
    ablation_df.to_csv(RUN_DIR / "sector_ablation_sorted.csv", index=False)
    write_json(
        RUN_DIR / "config.json",
        {
            "generated_at_utc": utc_now_iso(),
            "phase": "01F_sector_ablation",
            "source_final_selection_json": str(final_selection_path.relative_to(ROOT_DIR)),
            "source_final_run_name": final_selection["final_stage01_run_name"],
            "dataset_path": run_config["dataset_path"],
            "fit_split": "train",
            "eval_split": "valid",
            "random_state": int(args.random_state),
            "sector_map": SECTOR_MAP,
        },
    )

    summary_payload = {
        "generated_at_utc": utc_now_iso(),
        "phase": "01F_sector_ablation",
        "baseline": {
            "valid_macro_f1": baseline.valid_macro_f1,
            "valid_balanced_accuracy": baseline.valid_balanced_accuracy,
            "valid_accuracy": baseline.valid_accuracy,
            "valid_log_loss": baseline.valid_log_loss,
            "num_features": baseline.num_features,
        },
        "most_harmful_removals": strongest_drop.to_dict(orient="records"),
        "most_helpful_removals": strongest_gain.to_dict(orient="records"),
    }
    write_json(RUN_DIR / "summary.json", summary_payload)
    write_json(REVIEW_JSON, summary_payload)

    lines = [
        "# 01F Sector Ablation Review",
        "",
        f"Generated at: `{summary_payload['generated_at_utc']}`",
        "",
        "## Scope",
        "",
        "- purpose: `remove one feature sector at a time and see what actually matters`",
        "- model family: `logistic_regression`",
        "- fit split: `train`",
        "- eval split: `valid`",
        "- held-out test: `not touched in 01F`",
        "",
        "## Full Baseline",
        "",
        f"- valid macro_f1: `{baseline.valid_macro_f1:.4f}`",
        f"- valid balanced_accuracy: `{baseline.valid_balanced_accuracy:.4f}`",
        f"- valid accuracy: `{baseline.valid_accuracy:.4f}`",
        f"- valid log_loss: `{baseline.valid_log_loss:.4f}`",
        "",
        "## Most Harmful Removals",
        "",
        "| removed sector | delta macro_f1 vs full | delta balanced_accuracy | features removed |",
        "| --- | ---: | ---: | ---: |",
    ]

    for row in strongest_drop.itertuples(index=False):
        lines.append(
            f"| `{row.removed_sector}` | {row.delta_macro_f1_vs_full:.4f} | {row.delta_balanced_accuracy_vs_full:.4f} | {len(SECTOR_MAP[row.removed_sector])} |"
        )

    lines.extend(
        [
            "",
            "## Most Helpful Removals",
            "",
            "| removed sector | delta macro_f1 vs full | delta balanced_accuracy | features removed |",
            "| --- | ---: | ---: | ---: |",
        ]
    )

    for row in strongest_gain.itertuples(index=False):
        lines.append(
            f"| `{row.removed_sector}` | {row.delta_macro_f1_vs_full:.4f} | {row.delta_balanced_accuracy_vs_full:.4f} | {len(SECTOR_MAP[row.removed_sector])} |"
        )

    lines.extend(
        [
            "",
            "## Notes",
            "",
            "- Negative delta means that sector was helping the baseline and removing it hurt validation performance.",
            "- Positive delta means that sector may be noisy or redundant in the current Stage 01 setup.",
            "- This is a post-selection diagnostic only. It does not replace the frozen Stage 01 final baseline.",
            "",
            "## Artifacts",
            "",
            "- full table: `02_runs/archived/01F_run_0001_sector_ablation/sector_ablation_results.csv`",
            "- sorted table: `02_runs/archived/01F_run_0001_sector_ablation/sector_ablation_sorted.csv`",
        ]
    )
    write_text(REVIEW_MD, "\n".join(lines) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
