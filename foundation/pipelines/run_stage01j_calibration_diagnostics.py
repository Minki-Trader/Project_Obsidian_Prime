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
from sklearn.metrics import accuracy_score, log_loss
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from foundation.features.catalog import FEATURE_ORDER
from foundation.pipelines.run_stage01b_model_compare import write_json, write_text
from foundation.pipelines.run_stage01f_sector_ablation import STAGE_ROOT, load_context, utc_now_iso


RUN_DIR = STAGE_ROOT / "02_runs" / "archived" / "01J_run_0001_calibration_diagnostics"
REVIEW_MD = STAGE_ROOT / "03_reviews" / "01J_calibration_diagnostics_review.md"
REVIEW_JSON = STAGE_ROOT / "03_reviews" / "01J_calibration_diagnostics_review.json"
SOURCE_01H_RUN_DIR = STAGE_ROOT / "02_runs" / "archived" / "01H_run_0001_compact_candidate_compare"

CLASS_LABELS = {
    0: "short",
    1: "flat",
    2: "long",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Stage 01J calibration diagnostics.")
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
        "--num-bins",
        type=int,
        default=10,
        help="Number of calibration bins",
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


def fit_valid_probabilities(
    train_df: pd.DataFrame,
    valid_df: pd.DataFrame,
    features: list[str],
    random_state: int,
) -> tuple[np.ndarray, np.ndarray]:
    model = build_model(random_state=random_state)
    model.fit(train_df[features], train_df["label"])
    valid_proba = model.predict_proba(valid_df[features])
    valid_pred = np.argmax(valid_proba, axis=1)
    return valid_pred, valid_proba


def one_hot_encode(y_true: np.ndarray, n_classes: int) -> np.ndarray:
    eye = np.eye(n_classes, dtype=np.float64)
    return eye[y_true]


def multiclass_brier(y_true: np.ndarray, y_proba: np.ndarray) -> float:
    y_one_hot = one_hot_encode(y_true=y_true, n_classes=y_proba.shape[1])
    return float(np.mean(np.sum((y_one_hot - y_proba) ** 2, axis=1)))


def calibration_bin_index(values: np.ndarray, num_bins: int) -> np.ndarray:
    clipped = np.clip(values, 0.0, 1.0)
    idx = np.floor(clipped * num_bins).astype(int)
    return np.minimum(idx, num_bins - 1)


def top_label_calibration(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    y_proba: np.ndarray,
    num_bins: int,
) -> tuple[pd.DataFrame, dict[str, float]]:
    confidence = np.max(y_proba, axis=1)
    correct = (y_pred == y_true).astype(np.float64)
    bin_idx = calibration_bin_index(confidence, num_bins=num_bins)

    rows: list[dict] = []
    total = float(len(y_true))
    ece = 0.0
    mce = 0.0

    for idx in range(num_bins):
        mask = bin_idx == idx
        row_count = int(mask.sum())
        if row_count == 0:
            continue
        mean_confidence = float(confidence[mask].mean())
        accuracy = float(correct[mask].mean())
        signed_gap = mean_confidence - accuracy
        abs_gap = abs(signed_gap)
        weight = row_count / total
        ece += weight * abs_gap
        mce = max(mce, abs_gap)
        rows.append(
            {
                "bin_index": idx,
                "bin_lower": idx / num_bins,
                "bin_upper": (idx + 1) / num_bins,
                "row_count": row_count,
                "mean_confidence": mean_confidence,
                "empirical_accuracy": accuracy,
                "signed_gap_conf_minus_acc": signed_gap,
                "abs_gap": abs_gap,
            }
        )

    summary = {
        "top_label_ece": float(ece),
        "top_label_mce": float(mce),
        "top_label_mean_confidence": float(confidence.mean()),
        "top_label_accuracy": float(correct.mean()),
        "top_label_signed_gap_conf_minus_acc": float(confidence.mean() - correct.mean()),
    }
    return pd.DataFrame(rows), summary


def classwise_calibration(
    y_true: np.ndarray,
    y_proba: np.ndarray,
    num_bins: int,
) -> tuple[pd.DataFrame, pd.DataFrame, dict[str, float]]:
    rows: list[dict] = []
    per_class_rows: list[dict] = []

    for class_id, class_name in CLASS_LABELS.items():
        class_prob = y_proba[:, class_id]
        class_true = (y_true == class_id).astype(np.float64)
        bin_idx = calibration_bin_index(class_prob, num_bins=num_bins)
        total = float(len(y_true))
        ece = 0.0
        mce = 0.0

        for idx in range(num_bins):
            mask = bin_idx == idx
            row_count = int(mask.sum())
            if row_count == 0:
                continue
            mean_probability = float(class_prob[mask].mean())
            empirical_rate = float(class_true[mask].mean())
            signed_gap = mean_probability - empirical_rate
            abs_gap = abs(signed_gap)
            weight = row_count / total
            ece += weight * abs_gap
            mce = max(mce, abs_gap)
            rows.append(
                {
                    "class_id": class_id,
                    "class_name": class_name,
                    "bin_index": idx,
                    "bin_lower": idx / num_bins,
                    "bin_upper": (idx + 1) / num_bins,
                    "row_count": row_count,
                    "mean_probability": mean_probability,
                    "empirical_rate": empirical_rate,
                    "signed_gap_prob_minus_rate": signed_gap,
                    "abs_gap": abs_gap,
                }
            )

        per_class_rows.append(
            {
                "class_id": class_id,
                "class_name": class_name,
                "classwise_ece": float(ece),
                "classwise_mce": float(mce),
                "mean_probability": float(class_prob.mean()),
                "empirical_rate": float(class_true.mean()),
                "signed_gap_prob_minus_rate": float(class_prob.mean() - class_true.mean()),
            }
        )

    per_bin_df = pd.DataFrame(rows)
    per_class_df = pd.DataFrame(per_class_rows)
    summary = {
        "mean_classwise_ece": float(per_class_df["classwise_ece"].mean()),
        "max_classwise_ece": float(per_class_df["classwise_ece"].max()),
        "mean_classwise_mce": float(per_class_df["classwise_mce"].mean()),
    }
    return per_bin_df, per_class_df, summary


def worst_top_bin(df: pd.DataFrame) -> dict:
    if df.empty:
        return {}
    row = df.sort_values("abs_gap", ascending=False, ignore_index=True).iloc[0]
    return row.to_dict()


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

    variants = {
        "full_58": FEATURE_ORDER,
        compact_name: compact_features,
    }

    overall_rows: list[dict] = []
    top_bin_frames: list[pd.DataFrame] = []
    class_bin_frames: list[pd.DataFrame] = []
    class_summary_frames: list[pd.DataFrame] = []
    summary_payload: dict[str, dict] = {}

    for variant_name, features in variants.items():
        y_pred, y_proba = fit_valid_probabilities(
            train_df=train_df,
            valid_df=valid_df,
            features=features,
            random_state=args.random_state,
        )

        top_bin_df, top_summary = top_label_calibration(
            y_true=y_valid,
            y_pred=y_pred,
            y_proba=y_proba,
            num_bins=args.num_bins,
        )
        top_bin_df.insert(0, "model", variant_name)
        top_bin_frames.append(top_bin_df)

        class_bin_df, class_summary_df, class_summary = classwise_calibration(
            y_true=y_valid,
            y_proba=y_proba,
            num_bins=args.num_bins,
        )
        class_bin_df.insert(0, "model", variant_name)
        class_summary_df.insert(0, "model", variant_name)
        class_bin_frames.append(class_bin_df)
        class_summary_frames.append(class_summary_df)

        overall_row = {
            "model": variant_name,
            "num_features": len(features),
            "valid_accuracy": float(accuracy_score(y_valid, y_pred)),
            "valid_log_loss": float(log_loss(y_valid, y_proba, labels=[0, 1, 2])),
            "valid_multiclass_brier": multiclass_brier(y_true=y_valid, y_proba=y_proba),
            **top_summary,
            **class_summary,
        }
        overall_rows.append(overall_row)

        summary_payload[variant_name] = {
            **overall_row,
            "worst_top_label_bin": worst_top_bin(top_bin_df),
            "classwise_summary": class_summary_df.to_dict(orient="records"),
        }

    overall_df = pd.DataFrame(overall_rows)
    top_bins_df = pd.concat(top_bin_frames, ignore_index=True)
    class_bins_df = pd.concat(class_bin_frames, ignore_index=True)
    class_summary_df = pd.concat(class_summary_frames, ignore_index=True)

    overall_df.to_csv(RUN_DIR / "overall_calibration_summary.csv", index=False)
    top_bins_df.to_csv(RUN_DIR / "top_label_reliability.csv", index=False)
    class_bins_df.to_csv(RUN_DIR / "classwise_reliability.csv", index=False)
    class_summary_df.to_csv(RUN_DIR / "classwise_summary.csv", index=False)

    full_row = overall_df.loc[overall_df["model"].eq("full_58")].iloc[0]
    compact_row = overall_df.loc[overall_df["model"].eq(compact_name)].iloc[0]
    comparison = {
        "delta_valid_log_loss_compact_minus_full": float(compact_row["valid_log_loss"] - full_row["valid_log_loss"]),
        "delta_valid_multiclass_brier_compact_minus_full": float(compact_row["valid_multiclass_brier"] - full_row["valid_multiclass_brier"]),
        "delta_top_label_ece_compact_minus_full": float(compact_row["top_label_ece"] - full_row["top_label_ece"]),
        "delta_mean_classwise_ece_compact_minus_full": float(compact_row["mean_classwise_ece"] - full_row["mean_classwise_ece"]),
    }

    final_summary = {
        "generated_at_utc": utc_now_iso(),
        "phase": "01J_calibration_diagnostics",
        "source_final_selection_json": str(final_selection_path.relative_to(ROOT_DIR)),
        "source_final_run_name": final_selection["final_stage01_run_name"],
        "source_compact_summary_json": str(compact_summary_path.relative_to(ROOT_DIR)),
        "dataset_path": run_config["dataset_path"],
        "fit_split": "train",
        "eval_split": "valid",
        "num_bins": int(args.num_bins),
        "models": summary_payload,
        "comparison": comparison,
    }
    write_json(RUN_DIR / "summary.json", final_summary)
    write_json(REVIEW_JSON, final_summary)

    better_top_ece = compact_name if compact_row["top_label_ece"] < full_row["top_label_ece"] else "full_58"
    better_classwise = compact_name if compact_row["mean_classwise_ece"] < full_row["mean_classwise_ece"] else "full_58"

    lines = [
        "# 01J Calibration Diagnostics Review",
        "",
        f"Generated at: `{final_summary['generated_at_utc']}`",
        "",
        "## Scope",
        "",
        "- purpose: `compare probability calibration between the frozen full baseline and the recommended compact candidate`",
        "- model family: `logistic_regression`",
        "- fit split: `train`",
        "- eval split: `valid`",
        "- held-out test: `not touched in 01J`",
        f"- bins: `{args.num_bins}`",
        "",
        "## Overall Calibration",
        "",
        "| model | features | log_loss | multiclass_brier | top_label_ece | mean_classwise_ece | top_label_signed_gap |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]

    for row in overall_df.itertuples(index=False):
        lines.append(
            f"| `{row.model}` | {row.num_features} | {row.valid_log_loss:.4f} | {row.valid_multiclass_brier:.4f} | {row.top_label_ece:.4f} | {row.mean_classwise_ece:.4f} | {row.top_label_signed_gap_conf_minus_acc:.4f} |"
        )

    lines.extend(
        [
            "",
            "## Read",
            "",
            f"- better top-label calibration: `{better_top_ece}`",
            f"- better classwise calibration: `{better_classwise}`",
            f"- compact minus full top-label ECE: `{comparison['delta_top_label_ece_compact_minus_full']:.4f}`",
            f"- compact minus full mean classwise ECE: `{comparison['delta_mean_classwise_ece_compact_minus_full']:.4f}`",
            "",
            "## Worst Top-Label Bin",
            "",
            f"- `full_58`: bin `{summary_payload['full_58']['worst_top_label_bin'].get('bin_lower', 0):.1f}-{summary_payload['full_58']['worst_top_label_bin'].get('bin_upper', 0):.1f}`, abs gap `{summary_payload['full_58']['worst_top_label_bin'].get('abs_gap', 0.0):.4f}`",
            f"- `{compact_name}`: bin `{summary_payload[compact_name]['worst_top_label_bin'].get('bin_lower', 0):.1f}-{summary_payload[compact_name]['worst_top_label_bin'].get('bin_upper', 0):.1f}`, abs gap `{summary_payload[compact_name]['worst_top_label_bin'].get('abs_gap', 0.0):.4f}`",
            "",
            "## Notes",
            "",
            "- Lower ECE and lower Brier are better.",
            "- Positive signed gap means the model is overconfident on average; negative means underconfident.",
            "- This stays inside post-selection diagnostics and does not replace the frozen 01D handoff.",
            "",
            "## Artifacts",
            "",
            "- overall summary: `02_runs/archived/01J_run_0001_calibration_diagnostics/overall_calibration_summary.csv`",
            "- top-label reliability: `02_runs/archived/01J_run_0001_calibration_diagnostics/top_label_reliability.csv`",
            "- classwise reliability: `02_runs/archived/01J_run_0001_calibration_diagnostics/classwise_reliability.csv`",
            "- classwise summary: `02_runs/archived/01J_run_0001_calibration_diagnostics/classwise_summary.csv`",
        ]
    )
    write_text(REVIEW_MD, "\n".join(lines) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
