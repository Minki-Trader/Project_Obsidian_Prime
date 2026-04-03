#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from lightgbm import LGBMClassifier, early_stopping, log_evaluation
from sklearn.metrics import accuracy_score, balanced_accuracy_score, f1_score, log_loss
from sklearn.utils.class_weight import compute_sample_weight

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from foundation.features.catalog import FEATURE_ORDER


UTC = timezone.utc
LABEL_MAP = {0: "short", 1: "flat", 2: "long"}


@dataclass
class RunMetric:
    run_name: str
    band: float
    train_rows: int
    valid_rows: int
    test_rows: int
    valid_macro_f1: float
    valid_balanced_accuracy: float
    valid_accuracy: float
    valid_log_loss: float
    best_iteration: int


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run Stage 01A smoke experiments.")
    parser.add_argument(
        "--feature-path",
        default="data/processed/fpmarkets_v2/features/extended_window/feature_matrix.parquet",
        help="Shared feature matrix parquet",
    )
    parser.add_argument(
        "--validity-path",
        default="data/processed/fpmarkets_v2/features/extended_window/feature_validity.parquet",
        help="Shared feature validity parquet",
    )
    parser.add_argument(
        "--us100-raw-root",
        default="data/raw/mt5_bars/m5/US100",
        help="US100 raw M5 parquet root",
    )
    parser.add_argument(
        "--stage-root",
        default="stages/01_base_feature_ml",
        help="Stage 01 root directory",
    )
    parser.add_argument(
        "--modeling-start",
        default="2022-09-01T00:00:00Z",
        help="Inclusive modeling start timestamp in UTC",
    )
    parser.add_argument(
        "--horizon-bars",
        type=int,
        default=6,
        help="Forward horizon in bars for the smoke run",
    )
    parser.add_argument(
        "--bands",
        default="0.00075,0.00100,0.00125",
        help="Comma-separated absolute return bands for short/flat/long labeling",
    )
    parser.add_argument(
        "--train-end",
        default="2025-01-01T00:00:00Z",
        help="Exclusive end of train split in UTC",
    )
    parser.add_argument(
        "--valid-end",
        default="2025-10-01T00:00:00Z",
        help="Exclusive end of valid split in UTC",
    )
    parser.add_argument(
        "--test-end",
        default="2026-03-01T00:00:00Z",
        help="Exclusive end of test split in UTC",
    )
    parser.add_argument(
        "--random-state",
        type=int,
        default=42,
        help="Random seed for the baseline model",
    )
    return parser


def parse_utc(value: str) -> pd.Timestamp:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=UTC)
    else:
        parsed = parsed.astimezone(UTC)
    return pd.Timestamp(parsed)


def utc_now_iso() -> str:
    return datetime.now(tz=UTC).isoformat()


def load_us100_target_frame(raw_root: Path, horizon_bars: int) -> pd.DataFrame:
    paths = sorted(raw_root.rglob("*.parquet"))
    if not paths:
        raise FileNotFoundError(f"missing raw US100 parquet files under {raw_root}")

    frames: list[pd.DataFrame] = []
    for path in paths:
        frame = pd.read_parquet(path, columns=["time_utc", "open", "close"])
        if frame.empty:
            continue
        frame["time_utc"] = pd.to_datetime(frame["time_utc"], utc=True)
        frames.append(frame)

    if not frames:
        raise RuntimeError("US100 raw parquet files exist but no rows were loaded")

    us100 = pd.concat(frames, ignore_index=True)
    us100 = us100.drop_duplicates(subset=["time_utc"]).sort_values("time_utc").reset_index(drop=True)
    us100["timestamp"] = us100["time_utc"] + pd.Timedelta(minutes=5)
    us100["entry_open"] = us100["open"].shift(-1)
    us100["exit_close"] = us100["close"].shift(-horizon_bars)
    us100["future_timestamp"] = us100["timestamp"].shift(-horizon_bars)
    us100["forward_return"] = (us100["exit_close"] / us100["entry_open"]) - 1
    return us100[["timestamp", "future_timestamp", "entry_open", "exit_close", "forward_return"]]


def assign_split(
    timestamp: pd.Timestamp,
    future_timestamp: pd.Timestamp,
    modeling_start: pd.Timestamp,
    train_end: pd.Timestamp,
    valid_end: pd.Timestamp,
    test_end: pd.Timestamp,
) -> str | None:
    if pd.isna(timestamp) or pd.isna(future_timestamp):
        return None
    if timestamp < modeling_start:
        return None
    if modeling_start <= timestamp < train_end and future_timestamp < train_end:
        return "train"
    if train_end <= timestamp < valid_end and future_timestamp < valid_end:
        return "valid"
    if valid_end <= timestamp < test_end and future_timestamp < test_end:
        return "test"
    return None


def class_counts(series: pd.Series) -> dict[str, int]:
    counts = series.value_counts().to_dict()
    return {LABEL_MAP[key]: int(counts.get(key, 0)) for key in LABEL_MAP}


def split_counts(series: pd.Series) -> dict[str, int]:
    counts = series.value_counts().to_dict()
    return {key: int(counts.get(key, 0)) for key in ("train", "valid", "test")}


def build_base_dataset(
    feature_path: Path,
    validity_path: Path,
    us100_target: pd.DataFrame,
    modeling_start: pd.Timestamp,
    train_end: pd.Timestamp,
    valid_end: pd.Timestamp,
    test_end: pd.Timestamp,
) -> pd.DataFrame:
    feature = pd.read_parquet(feature_path)
    validity = pd.read_parquet(validity_path, columns=["timestamp", "is_feature_row_valid"])

    feature["timestamp"] = pd.to_datetime(feature["timestamp"], utc=True)
    validity["timestamp"] = pd.to_datetime(validity["timestamp"], utc=True)
    base = feature.merge(validity, on="timestamp", how="left")
    base = base.merge(us100_target, on="timestamp", how="left")
    base = base[base["symbol"].eq("US100")].copy()
    base = base[base["is_feature_row_valid"].fillna(False)].copy()
    base["split"] = [
        assign_split(ts, fts, modeling_start, train_end, valid_end, test_end)
        for ts, fts in zip(base["timestamp"], base["future_timestamp"], strict=False)
    ]
    base = base[base["split"].notna()].copy()
    base = base[base["forward_return"].notna()].copy()
    return base.reset_index(drop=True)


def make_label(forward_return: pd.Series, band: float) -> pd.Series:
    label = np.where(forward_return <= -band, 0, np.where(forward_return >= band, 2, 1))
    return pd.Series(label, index=forward_return.index, dtype="int64")


def train_lightgbm(
    train_df: pd.DataFrame,
    valid_df: pd.DataFrame,
    band: float,
    run_dir: Path,
    random_state: int,
) -> RunMetric:
    x_train = train_df[FEATURE_ORDER]
    y_train = train_df["label"]
    x_valid = valid_df[FEATURE_ORDER]
    y_valid = valid_df["label"]

    sample_weight = compute_sample_weight(class_weight="balanced", y=y_train)

    model = LGBMClassifier(
        objective="multiclass",
        num_class=3,
        n_estimators=400,
        learning_rate=0.05,
        num_leaves=31,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=random_state,
        n_jobs=-1,
    )
    model.fit(
        x_train,
        y_train,
        sample_weight=sample_weight,
        eval_set=[(x_valid, y_valid)],
        eval_metric="multi_logloss",
        callbacks=[early_stopping(stopping_rounds=50, verbose=False), log_evaluation(period=0)],
    )

    valid_proba = model.predict_proba(x_valid)
    valid_pred = np.argmax(valid_proba, axis=1)

    metrics = RunMetric(
        run_name=run_dir.name,
        band=band,
        train_rows=int(len(train_df)),
        valid_rows=int(len(valid_df)),
        test_rows=0,
        valid_macro_f1=float(f1_score(y_valid, valid_pred, average="macro")),
        valid_balanced_accuracy=float(balanced_accuracy_score(y_valid, valid_pred)),
        valid_accuracy=float(accuracy_score(y_valid, valid_pred)),
        valid_log_loss=float(log_loss(y_valid, valid_proba, labels=[0, 1, 2])),
        best_iteration=int(getattr(model, "best_iteration_", 0) or model.n_estimators),
    )

    joblib.dump(model, run_dir / "model.joblib")

    pd.DataFrame(
        {
            "feature": FEATURE_ORDER,
            "importance": model.feature_importances_,
        }
    ).sort_values("importance", ascending=False).to_csv(run_dir / "feature_importance.csv", index=False)

    valid_out = valid_df[["timestamp", "split", "forward_return"]].copy()
    valid_out["label_true"] = y_valid.to_numpy()
    valid_out["label_pred"] = valid_pred
    valid_out["p_short"] = valid_proba[:, 0]
    valid_out["p_flat"] = valid_proba[:, 1]
    valid_out["p_long"] = valid_proba[:, 2]
    valid_out.to_parquet(run_dir / "valid_predictions.parquet", index=False)

    return metrics


def write_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")


def band_tag(value: float) -> str:
    return f"{value:.5f}".replace(".", "")


def main() -> int:
    args = build_parser().parse_args()

    feature_path = ROOT_DIR / args.feature_path
    validity_path = ROOT_DIR / args.validity_path
    us100_raw_root = ROOT_DIR / args.us100_raw_root
    stage_root = ROOT_DIR / args.stage_root

    modeling_start = parse_utc(args.modeling_start)
    train_end = parse_utc(args.train_end)
    valid_end = parse_utc(args.valid_end)
    test_end = parse_utc(args.test_end)
    bands = [float(item) for item in args.bands.split(",") if item.strip()]
    if len(bands) < 2 or len(bands) > 3:
        raise ValueError("Stage 01A expects exactly 2 or 3 band candidates")

    inputs_dir = stage_root / "01_inputs"
    active_dir = stage_root / "02_runs" / "active"
    review_dir = stage_root / "03_reviews"
    selected_dir = stage_root / "04_selected"
    inputs_dir.mkdir(parents=True, exist_ok=True)
    active_dir.mkdir(parents=True, exist_ok=True)
    review_dir.mkdir(parents=True, exist_ok=True)
    selected_dir.mkdir(parents=True, exist_ok=True)

    us100_target = load_us100_target_frame(us100_raw_root, args.horizon_bars)
    base = build_base_dataset(
        feature_path=feature_path,
        validity_path=validity_path,
        us100_target=us100_target,
        modeling_start=modeling_start,
        train_end=train_end,
        valid_end=valid_end,
        test_end=test_end,
    )

    dataset_name = f"stage01a_h{args.horizon_bars:02d}_dataset"
    base_dataset_path = inputs_dir / f"{dataset_name}.parquet"
    base_summary_path = inputs_dir / f"{dataset_name}_summary.json"
    smoke_plan_path = inputs_dir / "01A_smoke_plan.json"

    base[["timestamp", "future_timestamp", "split", "forward_return", *FEATURE_ORDER]].to_parquet(base_dataset_path, index=False)

    base_summary = {
        "generated_at_utc": utc_now_iso(),
        "horizon_bars": args.horizon_bars,
        "modeling_start_utc": modeling_start.isoformat(),
        "train_end_utc_exclusive": train_end.isoformat(),
        "valid_end_utc_exclusive": valid_end.isoformat(),
        "test_end_utc_exclusive": test_end.isoformat(),
        "row_count": int(len(base)),
        "split_counts": split_counts(base["split"]),
        "feature_count": len(FEATURE_ORDER),
        "return_formula": "forward_return = exit_close[t+h] / entry_open[t+1] - 1",
    }
    write_json(base_summary_path, base_summary)

    smoke_plan = {
        "phase": "01A_smoke",
        "generated_at_utc": utc_now_iso(),
        "horizon_bars": args.horizon_bars,
        "bands": bands,
        "baseline_model": "lightgbm_multiclass",
        "frozen_items": [
            "[p_short, p_flat, p_long]",
            "US100 M5 base frame",
            "chronological split ordering",
            "shared FPMarkets v2 feature contract",
        ],
        "search_items": [
            "band candidate",
        ],
        "selection_metric": "valid_macro_f1",
    }
    write_json(smoke_plan_path, smoke_plan)

    results: list[RunMetric] = []
    for index, band in enumerate(bands, start=1):
        run_name = f"01A_run_{index:04d}_h{args.horizon_bars:02d}_band{band_tag(band)}_lgbm"
        run_dir = active_dir / run_name
        run_dir.mkdir(parents=True, exist_ok=True)

        labeled = base.copy()
        labeled["label"] = make_label(labeled["forward_return"], band)

        train_df = labeled[labeled["split"].eq("train")].copy()
        valid_df = labeled[labeled["split"].eq("valid")].copy()
        test_df = labeled[labeled["split"].eq("test")].copy()

        run_config = {
            "run_name": run_name,
            "phase": "01A_smoke",
            "generated_at_utc": utc_now_iso(),
            "horizon_bars": args.horizon_bars,
            "band": band,
            "model": "lightgbm_multiclass",
            "modeling_start_utc": modeling_start.isoformat(),
            "train_end_utc_exclusive": train_end.isoformat(),
            "valid_end_utc_exclusive": valid_end.isoformat(),
            "test_end_utc_exclusive": test_end.isoformat(),
            "dataset_path": str(base_dataset_path.relative_to(ROOT_DIR)),
            "label_rule": {
                "short": f"forward_return <= -{band:.5f}",
                "flat": f"-{band:.5f} < forward_return < {band:.5f}",
                "long": f"forward_return >= {band:.5f}",
            },
            "class_counts": {
                "train": class_counts(train_df["label"]),
                "valid": class_counts(valid_df["label"]),
                "test": class_counts(test_df["label"]),
            },
        }
        write_json(run_dir / "config.json", run_config)

        metric = train_lightgbm(
            train_df=train_df,
            valid_df=valid_df,
            band=band,
            run_dir=run_dir,
            random_state=args.random_state,
        )
        metric.test_rows = int(len(test_df))
        write_json(run_dir / "metrics.json", asdict(metric))
        results.append(metric)

    results_df = pd.DataFrame([asdict(item) for item in results]).sort_values(
        by=["valid_macro_f1", "valid_balanced_accuracy", "valid_accuracy", "valid_log_loss"],
        ascending=[False, False, False, True],
    )
    results_df.to_csv(review_dir / "01A_smoke_results.csv", index=False)

    best = results_df.iloc[0].to_dict()
    review_lines = [
        "# 01A Smoke Review",
        "",
        f"Generated at: `{utc_now_iso()}`",
        "",
        "## Summary",
        "",
        f"- horizon: `{args.horizon_bars}` bars",
        f"- bands tested: `{', '.join(f'{band:.5f}' for band in bands)}`",
        f"- baseline model: `lightgbm_multiclass`",
        f"- selection metric: `valid_macro_f1`",
        "",
        "## Ranked Results",
        "",
    ]
    for row in results_df.itertuples(index=False):
        review_lines.append(
            f"- `{row.run_name}`: macro_f1={row.valid_macro_f1:.4f}, "
            f"balanced_acc={row.valid_balanced_accuracy:.4f}, "
            f"accuracy={row.valid_accuracy:.4f}, log_loss={row.valid_log_loss:.4f}"
        )
    review_lines.extend(
        [
            "",
            "## Winner For 01B",
            "",
            f"- selected run: `{best['run_name']}`",
            f"- selected band: `{best['band']:.5f}`",
            f"- next phase: freeze this label setup and compare learning tools in `01B`",
        ]
    )
    write_text(review_dir / "01A_smoke_review.md", "\n".join(review_lines) + "\n")

    selected_payload = {
        "phase": "01A_smoke",
        "selected_at_utc": utc_now_iso(),
        "selected_run_name": best["run_name"],
        "selected_band": float(best["band"]),
        "selected_horizon_bars": args.horizon_bars,
        "selection_metric": "valid_macro_f1",
        "selected_run_metrics": {
            "valid_macro_f1": float(best["valid_macro_f1"]),
            "valid_balanced_accuracy": float(best["valid_balanced_accuracy"]),
            "valid_accuracy": float(best["valid_accuracy"]),
            "valid_log_loss": float(best["valid_log_loss"]),
        },
        "next_phase": "01B_model_compare",
    }
    write_json(selected_dir / "01A_selected_label.json", selected_payload)

    selected_note = [
        "# 01A Selected Label",
        "",
        f"- selected run: `{best['run_name']}`",
        f"- horizon: `{args.horizon_bars}` bars",
        f"- selected band: `{best['band']:.5f}`",
        f"- valid macro_f1: `{best['valid_macro_f1']:.4f}`",
        f"- valid balanced_accuracy: `{best['valid_balanced_accuracy']:.4f}`",
        "",
        "This is the label setup that should be frozen for Stage 01B model comparison.",
    ]
    write_text(selected_dir / "01A_selected_label.md", "\n".join(selected_note) + "\n")

    print(json.dumps(selected_payload, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
