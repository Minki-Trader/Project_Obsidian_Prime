#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, balanced_accuracy_score, f1_score, log_loss

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))


UTC = timezone.utc
LABEL_INDEX = [0, 1, 2]
LABEL_NAME = {0: "short", 1: "flat", 2: "long"}


@dataclass
class SummaryMetric:
    baseline_name: str
    prediction_style: str
    macro_f1_mean: float
    macro_f1_std: float
    balanced_accuracy_mean: float
    balanced_accuracy_std: float
    accuracy_mean: float
    accuracy_std: float
    log_loss_value: float


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Evaluate Stage 01 control baselines on the selected label setup.")
    parser.add_argument(
        "--run-config",
        default="stages/01_base_feature_ml/02_runs/active/01A_run_0003_h06_band000125_lgbm/config.json",
        help="Selected Stage 01A run config JSON",
    )
    parser.add_argument(
        "--repeats",
        type=int,
        default=300,
        help="Monte Carlo repeat count for sampled control baselines",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed for Monte Carlo control baselines",
    )
    return parser


def utc_now_iso() -> str:
    return datetime.now(tz=UTC).isoformat()


def write_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")


def make_label(forward_return: pd.Series, band: float) -> pd.Series:
    return pd.Series(
        np.where(forward_return <= -band, 0, np.where(forward_return >= band, 2, 1)),
        index=forward_return.index,
        dtype="int64",
    )


def evaluate_predictions(y_true: np.ndarray, y_pred: np.ndarray) -> tuple[float, float, float]:
    return (
        float(f1_score(y_true, y_pred, average="macro")),
        float(balanced_accuracy_score(y_true, y_pred)),
        float(accuracy_score(y_true, y_pred)),
    )


def monte_carlo_sample_metrics(
    y_true: np.ndarray,
    probabilities: np.ndarray,
    repeats: int,
    seed: int,
) -> tuple[float, float, float, float, float, float]:
    rng = np.random.default_rng(seed)
    macro_scores: list[float] = []
    balanced_scores: list[float] = []
    accuracy_scores: list[float] = []
    classes = np.array(LABEL_INDEX, dtype=np.int64)

    for _ in range(repeats):
        sampled = rng.choice(classes, size=len(y_true), p=probabilities)
        macro, balanced, accuracy = evaluate_predictions(y_true, sampled)
        macro_scores.append(macro)
        balanced_scores.append(balanced)
        accuracy_scores.append(accuracy)

    return (
        float(np.mean(macro_scores)),
        float(np.std(macro_scores, ddof=0)),
        float(np.mean(balanced_scores)),
        float(np.std(balanced_scores, ddof=0)),
        float(np.mean(accuracy_scores)),
        float(np.std(accuracy_scores, ddof=0)),
    )


def main() -> int:
    args = build_parser().parse_args()

    run_config_path = ROOT_DIR / args.run_config
    if not run_config_path.exists():
        raise FileNotFoundError(f"missing run config: {run_config_path}")

    run_dir = run_config_path.parent
    stage_root = run_dir.parents[2]
    review_dir = stage_root / "03_reviews"
    selected_dir = stage_root / "04_selected"

    run_config = json.loads(run_config_path.read_text(encoding="utf-8"))
    dataset_path = ROOT_DIR / run_config["dataset_path"]
    band = float(run_config["band"])

    dataset = pd.read_parquet(dataset_path, columns=["timestamp", "split", "forward_return"])
    dataset["label"] = make_label(dataset["forward_return"], band)

    train = dataset[dataset["split"].eq("train")].copy()
    valid = dataset[dataset["split"].eq("valid")].copy()
    y_valid = valid["label"].to_numpy(dtype=np.int64)

    train_probs = (
        train["label"]
        .value_counts(normalize=True)
        .reindex(LABEL_INDEX, fill_value=0.0)
        .to_numpy(dtype=float)
    )
    uniform_probs = np.array([1 / 3, 1 / 3, 1 / 3], dtype=float)

    metrics_path = run_dir / "metrics.json"
    selected_metrics = json.loads(metrics_path.read_text(encoding="utf-8"))

    controls: list[SummaryMetric] = []
    controls.append(
        SummaryMetric(
            baseline_name="selected_model",
            prediction_style="lightgbm_multiclass",
            macro_f1_mean=float(selected_metrics["valid_macro_f1"]),
            macro_f1_std=0.0,
            balanced_accuracy_mean=float(selected_metrics["valid_balanced_accuracy"]),
            balanced_accuracy_std=0.0,
            accuracy_mean=float(selected_metrics["valid_accuracy"]),
            accuracy_std=0.0,
            log_loss_value=float(selected_metrics["valid_log_loss"]),
        )
    )

    flat_pred = np.full_like(y_valid, fill_value=1)
    flat_macro, flat_balanced, flat_accuracy = evaluate_predictions(y_valid, flat_pred)
    eps = 1e-6
    flat_proba = np.tile(np.array([eps, 1 - (2 * eps), eps], dtype=float), (len(y_valid), 1))
    controls.append(
        SummaryMetric(
            baseline_name="flat_only",
            prediction_style="always_predict_flat",
            macro_f1_mean=flat_macro,
            macro_f1_std=0.0,
            balanced_accuracy_mean=flat_balanced,
            balanced_accuracy_std=0.0,
            accuracy_mean=flat_accuracy,
            accuracy_std=0.0,
            log_loss_value=float(log_loss(y_valid, flat_proba, labels=LABEL_INDEX)),
        )
    )

    uniform_macro, uniform_macro_std, uniform_bal, uniform_bal_std, uniform_acc, uniform_acc_std = (
        monte_carlo_sample_metrics(y_valid, uniform_probs, args.repeats, args.seed)
    )
    uniform_proba = np.tile(uniform_probs, (len(y_valid), 1))
    controls.append(
        SummaryMetric(
            baseline_name="uniform_random",
            prediction_style=f"sample_uniform_{args.repeats}x",
            macro_f1_mean=uniform_macro,
            macro_f1_std=uniform_macro_std,
            balanced_accuracy_mean=uniform_bal,
            balanced_accuracy_std=uniform_bal_std,
            accuracy_mean=uniform_acc,
            accuracy_std=uniform_acc_std,
            log_loss_value=float(log_loss(y_valid, uniform_proba, labels=LABEL_INDEX)),
        )
    )

    freq_macro, freq_macro_std, freq_bal, freq_bal_std, freq_acc, freq_acc_std = monte_carlo_sample_metrics(
        y_valid, train_probs, args.repeats, args.seed + 1
    )
    freq_proba = np.tile(train_probs, (len(y_valid), 1))
    controls.append(
        SummaryMetric(
            baseline_name="frequency_based",
            prediction_style=f"sample_train_freq_{args.repeats}x",
            macro_f1_mean=freq_macro,
            macro_f1_std=freq_macro_std,
            balanced_accuracy_mean=freq_bal,
            balanced_accuracy_std=freq_bal_std,
            accuracy_mean=freq_acc,
            accuracy_std=freq_acc_std,
            log_loss_value=float(log_loss(y_valid, freq_proba, labels=LABEL_INDEX)),
        )
    )

    results_df = pd.DataFrame([item.__dict__ for item in controls])
    results_df.to_csv(review_dir / "01A_control_baselines.csv", index=False)

    payload = {
        "generated_at_utc": utc_now_iso(),
        "source_run": run_config["run_name"],
        "band": band,
        "horizon_bars": int(run_config["horizon_bars"]),
        "valid_class_counts": run_config["class_counts"]["valid"],
        "train_class_counts": run_config["class_counts"]["train"],
        "repeats_for_randomized_controls": args.repeats,
        "results": [item.__dict__ for item in controls],
    }
    write_json(review_dir / "01A_control_baselines.json", payload)

    results_by_name = {item.baseline_name: item for item in controls}
    selected = results_by_name["selected_model"]
    flat = results_by_name["flat_only"]
    uniform = results_by_name["uniform_random"]
    freq = results_by_name["frequency_based"]

    lines = [
        "# 01A Control Baselines",
        "",
        f"Generated at: `{payload['generated_at_utc']}`",
        "",
        "## Definitions",
        "",
        "- `flat_only`: always predicts `flat`.",
        f"- `uniform_random`: samples `short/flat/long` uniformly, averaged over `{args.repeats}` Monte Carlo repeats.",
        f"- `frequency_based`: samples classes using the train split class frequencies, averaged over `{args.repeats}` Monte Carlo repeats.",
        "",
        "## Validation Class Counts",
        "",
        f"- valid: `short={run_config['class_counts']['valid']['short']}`, `flat={run_config['class_counts']['valid']['flat']}`, `long={run_config['class_counts']['valid']['long']}`",
        f"- train frequency vector: `short={train_probs[0]:.4f}`, `flat={train_probs[1]:.4f}`, `long={train_probs[2]:.4f}`",
        "",
        "## Results",
        "",
        f"- `selected_model`: macro_f1={selected.macro_f1_mean:.4f}, balanced_acc={selected.balanced_accuracy_mean:.4f}, accuracy={selected.accuracy_mean:.4f}, log_loss={selected.log_loss_value:.4f}",
        f"- `flat_only`: macro_f1={flat.macro_f1_mean:.4f}, balanced_acc={flat.balanced_accuracy_mean:.4f}, accuracy={flat.accuracy_mean:.4f}, log_loss={flat.log_loss_value:.4f}",
        f"- `uniform_random`: macro_f1={uniform.macro_f1_mean:.4f} +/- {uniform.macro_f1_std:.4f}, balanced_acc={uniform.balanced_accuracy_mean:.4f} +/- {uniform.balanced_accuracy_std:.4f}, accuracy={uniform.accuracy_mean:.4f} +/- {uniform.accuracy_std:.4f}, log_loss={uniform.log_loss_value:.4f}",
        f"- `frequency_based`: macro_f1={freq.macro_f1_mean:.4f} +/- {freq.macro_f1_std:.4f}, balanced_acc={freq.balanced_accuracy_mean:.4f} +/- {freq.balanced_accuracy_std:.4f}, accuracy={freq.accuracy_mean:.4f} +/- {freq.accuracy_std:.4f}, log_loss={freq.log_loss_value:.4f}",
        "",
        "## Interpretation",
        "",
        "- The selected Stage 01A model should clear all three simple controls to justify moving into learning-tool comparison.",
        "- `flat_only` is the majority-class shortcut.",
        "- `uniform_random` approximates a no-skill three-way guesser.",
        "- `frequency_based` approximates a predictor that knows only the train label mix, not the features.",
    ]
    write_text(review_dir / "01A_control_baselines.md", "\n".join(lines) + "\n")

    selected_note = [
        "# 01A Selected Label",
        "",
        f"- selected run: `{run_config['run_name']}`",
        f"- horizon: `{run_config['horizon_bars']}` bars",
        f"- selected band: `{band:.5f}`",
        f"- valid macro_f1: `{selected.macro_f1_mean:.4f}`",
        f"- valid balanced_accuracy: `{selected.balanced_accuracy_mean:.4f}`",
        f"- control-baseline check: `passed against flat_only / uniform_random / frequency_based`",
        "",
        "This is the label setup that should be frozen for Stage 01B model comparison.",
    ]
    write_text(selected_dir / "01A_selected_label.md", "\n".join(selected_note) + "\n")

    print(json.dumps(payload, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
