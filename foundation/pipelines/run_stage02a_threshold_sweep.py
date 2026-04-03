#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from itertools import product
from pathlib import Path

import numpy as np
import pandas as pd

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from foundation.pipelines.run_stage01b_model_compare import write_json, write_text


UTC = timezone.utc
DEFAULT_REFERENCE_THRESHOLD = 1.0 / 3.0


@dataclass
class SweepMetric:
    short_threshold: float
    long_threshold: float
    candidate_rows: int
    trade_count: int
    long_trade_count: int
    short_trade_count: int
    no_trade_rows: int
    dual_signal_rows: int
    valid_hit_rate: float
    valid_mean_trade_return: float
    valid_median_trade_return: float
    valid_sum_return: float
    valid_compounded_return: float
    valid_max_drawdown: float


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run Stage 02A individual-threshold sweep.")
    parser.add_argument(
        "--source-run-dir",
        default="stages/01_base_feature_ml/02_runs/archived/01C_run_0001_h03_band000125_logreg",
        help="Stage 01 search-side run directory that contains valid predictions.",
    )
    parser.add_argument(
        "--selected-final-json",
        default="stages/01_base_feature_ml/04_selected/01D_final_stage01_selection.json",
        help="Stage 01 final selection JSON for the frozen handoff reference.",
    )
    parser.add_argument(
        "--stage-root",
        default="stages/02_individual_thresholds",
        help="Stage 02 root directory.",
    )
    parser.add_argument(
        "--short-thresholds",
        default="0.35,0.40,0.45,0.50,0.55,0.60,0.65",
        help="Comma-separated short-threshold candidates.",
    )
    parser.add_argument(
        "--long-thresholds",
        default="0.35,0.40,0.45,0.50,0.55,0.60,0.65",
        help="Comma-separated long-threshold candidates.",
    )
    parser.add_argument(
        "--min-trades",
        type=int,
        default=100,
        help="Minimum number of executed trades required for a threshold pair to qualify.",
    )
    return parser


def utc_now_iso() -> str:
    return datetime.now(tz=UTC).isoformat()


def parse_thresholds(raw: str) -> list[float]:
    values = [float(item.strip()) for item in raw.split(",") if item.strip()]
    if not values:
        raise ValueError("threshold list is empty")
    return values


def load_stage01_source(source_run_dir: Path) -> tuple[pd.DataFrame, dict]:
    config_path = source_run_dir / "config.json"
    predictions_path = source_run_dir / "valid_predictions.parquet"
    if not config_path.exists():
        raise FileNotFoundError(f"missing source config: {config_path}")
    if not predictions_path.exists():
        raise FileNotFoundError(f"missing valid predictions: {predictions_path}")

    config = json.loads(config_path.read_text(encoding="utf-8"))
    dataset_path = ROOT_DIR / config["dataset_path"]
    dataset = pd.read_parquet(
        dataset_path,
        columns=["timestamp", "split", "future_timestamp", "entry_open", "exit_close", "forward_return", "label"],
    )
    predictions = pd.read_parquet(predictions_path)

    dataset["timestamp"] = pd.to_datetime(dataset["timestamp"], utc=True)
    dataset["future_timestamp"] = pd.to_datetime(dataset["future_timestamp"], utc=True)
    predictions["timestamp"] = pd.to_datetime(predictions["timestamp"], utc=True)

    valid_dataset = dataset[dataset["split"].eq("valid")].copy()
    merged = valid_dataset.merge(predictions, on=["timestamp", "split", "forward_return"], how="inner")
    merged = merged.sort_values("timestamp").reset_index(drop=True)

    if len(merged) != len(predictions):
        raise RuntimeError("valid prediction rows do not align cleanly with the source dataset")
    if not merged["label"].equals(merged["label_true"]):
        raise RuntimeError("label mismatch between source dataset and valid predictions")

    return merged, config


def decide_side(row: pd.Series, short_threshold: float, long_threshold: float) -> tuple[int, bool]:
    short_ok = float(row["p_short"]) >= short_threshold
    long_ok = float(row["p_long"]) >= long_threshold
    dual_signal = bool(short_ok and long_ok)

    if short_ok and not long_ok:
        return -1, dual_signal
    if long_ok and not short_ok:
        return 1, dual_signal
    if short_ok and long_ok:
        if float(row["p_long"]) > float(row["p_short"]):
            return 1, dual_signal
        if float(row["p_short"]) > float(row["p_long"]):
            return -1, dual_signal
    return 0, dual_signal


def build_trade_log(trades: list[dict]) -> pd.DataFrame:
    if not trades:
        return pd.DataFrame(
            columns=[
                "signal_timestamp",
                "exit_timestamp",
                "direction",
                "trade_return",
                "entry_open",
                "exit_close",
                "p_short",
                "p_flat",
                "p_long",
                "selected_probability",
                "opposing_probability",
                "probability_gap",
            ]
        )
    frame = pd.DataFrame(trades)
    frame["signal_timestamp"] = pd.to_datetime(frame["signal_timestamp"], utc=True)
    frame["exit_timestamp"] = pd.to_datetime(frame["exit_timestamp"], utc=True)
    return frame


def simulate_threshold_pair(
    valid_frame: pd.DataFrame,
    horizon_bars: int,
    short_threshold: float,
    long_threshold: float,
) -> tuple[SweepMetric, pd.DataFrame]:
    index = 0
    trades: list[dict] = []
    long_trade_count = 0
    short_trade_count = 0
    no_trade_rows = 0
    dual_signal_rows = 0

    while index < len(valid_frame):
        row = valid_frame.iloc[index]
        side, dual_signal = decide_side(row, short_threshold, long_threshold)
        if dual_signal:
            dual_signal_rows += 1

        if side == 0:
            no_trade_rows += 1
            index += 1
            continue

        trade_return = float(row["forward_return"]) * side
        if side > 0:
            direction = "long"
            long_trade_count += 1
            selected_probability = float(row["p_long"])
            opposing_probability = float(row["p_short"])
        else:
            direction = "short"
            short_trade_count += 1
            selected_probability = float(row["p_short"])
            opposing_probability = float(row["p_long"])

        trades.append(
            {
                "signal_timestamp": row["timestamp"],
                "exit_timestamp": row["future_timestamp"],
                "direction": direction,
                "trade_return": trade_return,
                "entry_open": float(row["entry_open"]),
                "exit_close": float(row["exit_close"]),
                "p_short": float(row["p_short"]),
                "p_flat": float(row["p_flat"]),
                "p_long": float(row["p_long"]),
                "selected_probability": selected_probability,
                "opposing_probability": opposing_probability,
                "probability_gap": selected_probability - opposing_probability,
            }
        )
        index += horizon_bars

    trade_log = build_trade_log(trades)
    trade_returns = trade_log["trade_return"].to_numpy(dtype=float) if not trade_log.empty else np.array([], dtype=float)

    if len(trade_returns) == 0:
        metric = SweepMetric(
            short_threshold=short_threshold,
            long_threshold=long_threshold,
            candidate_rows=int(len(valid_frame)),
            trade_count=0,
            long_trade_count=0,
            short_trade_count=0,
            no_trade_rows=int(no_trade_rows),
            dual_signal_rows=int(dual_signal_rows),
            valid_hit_rate=0.0,
            valid_mean_trade_return=0.0,
            valid_median_trade_return=0.0,
            valid_sum_return=0.0,
            valid_compounded_return=0.0,
            valid_max_drawdown=0.0,
        )
        return metric, trade_log

    equity_curve = np.cumprod(1.0 + trade_returns)
    rolling_peak = np.maximum.accumulate(equity_curve)
    drawdown = (equity_curve / rolling_peak) - 1.0

    metric = SweepMetric(
        short_threshold=short_threshold,
        long_threshold=long_threshold,
        candidate_rows=int(len(valid_frame)),
        trade_count=int(len(trade_returns)),
        long_trade_count=int(long_trade_count),
        short_trade_count=int(short_trade_count),
        no_trade_rows=int(no_trade_rows),
        dual_signal_rows=int(dual_signal_rows),
        valid_hit_rate=float(np.mean(trade_returns > 0.0)),
        valid_mean_trade_return=float(np.mean(trade_returns)),
        valid_median_trade_return=float(np.median(trade_returns)),
        valid_sum_return=float(np.sum(trade_returns)),
        valid_compounded_return=float(equity_curve[-1] - 1.0),
        valid_max_drawdown=float(np.min(drawdown)),
    )
    return metric, trade_log


def select_best_rows(results_df: pd.DataFrame, min_trades: int) -> pd.DataFrame:
    qualified = results_df[results_df["trade_count"] >= min_trades].copy()
    if qualified.empty:
        raise RuntimeError(f"no threshold pair met the minimum trade requirement: {min_trades}")
    return qualified.sort_values(
        by=[
            "valid_compounded_return",
            "valid_mean_trade_return",
            "trade_count",
            "valid_hit_rate",
            "valid_max_drawdown",
        ],
        ascending=[False, False, False, False, False],
    ).reset_index(drop=True)


def update_review_index(review_path: Path) -> None:
    lines = [
        "# Review Index",
        "",
        "## Current Entries",
        "",
        "- `02A`: see `02A_threshold_sweep_review.md`",
        "",
        "## Review Rule",
        "",
        "For each completed phase, add:",
        "",
        "- run folder name",
        "- threshold setup summary",
        "- split used for search",
        "- headline result",
        "- keep or archive decision",
        "",
        "Also record the phase code:",
        "",
        "- `02A`",
    ]
    write_text(review_path, "\n".join(lines) + "\n")


def update_selection_status(
    selection_status_path: Path,
    selected_run_name: str,
    short_threshold: float,
    long_threshold: float,
) -> None:
    lines = [
        "# Selection Status",
        "",
        "- stage: `02_individual_thresholds`",
        "- current phase complete: `02A`",
        f"- current preferred threshold seed: `{selected_run_name}`",
        "- search source model: `01C_run_0001_h03_band000125_logreg`",
        "- reserved final confirmation model: `01D_run_0001_final_h03_band000125_logreg`",
        f"- selected short_threshold: `{short_threshold:.2f}`",
        f"- selected long_threshold: `{long_threshold:.2f}`",
        "- next phase: `later confirmation or carry-forward`",
    ]
    write_text(selection_status_path, "\n".join(lines) + "\n")


def main() -> int:
    args = build_parser().parse_args()

    source_run_dir = ROOT_DIR / args.source_run_dir
    selected_final_path = ROOT_DIR / args.selected_final_json
    stage_root = ROOT_DIR / args.stage_root

    short_thresholds = parse_thresholds(args.short_thresholds)
    long_thresholds = parse_thresholds(args.long_thresholds)

    valid_frame, source_config = load_stage01_source(source_run_dir)
    selected_final = json.loads(selected_final_path.read_text(encoding="utf-8"))

    horizon_bars = int(source_config["horizon_bars"])
    run_name = "02A_run_0001_threshold_sweep"

    inputs_dir = stage_root / "01_inputs"
    active_dir = stage_root / "02_runs" / "active"
    archived_dir = stage_root / "02_runs" / "archived"
    review_dir = stage_root / "03_reviews"
    selected_dir = stage_root / "04_selected"
    for path in (inputs_dir, active_dir, archived_dir, review_dir, selected_dir):
        path.mkdir(parents=True, exist_ok=True)

    run_dir = active_dir / run_name
    run_dir.mkdir(parents=True, exist_ok=True)

    plan_payload = {
        "generated_at_utc": utc_now_iso(),
        "phase": "02A_threshold_sweep",
        "stage_root": str(stage_root.relative_to(ROOT_DIR)),
        "source_run_dir": str(source_run_dir.relative_to(ROOT_DIR)),
        "source_dataset_path": source_config["dataset_path"],
        "selection_metric": "valid_compounded_return",
        "search_split": "valid",
        "short_thresholds": short_thresholds,
        "long_thresholds": long_thresholds,
        "min_trades": int(args.min_trades),
        "fixed_items": [
            "individual thresholds only",
            "min_margin = 0",
            "3-bar time exit",
            "no overlap",
            "no flip",
            "zero trading cost assumption",
            "Stage 01 search-side model source",
        ],
    }
    write_json(inputs_dir / "02A_threshold_sweep_plan.json", plan_payload)

    run_config = {
        "run_name": run_name,
        "phase": "02A_threshold_sweep",
        "generated_at_utc": utc_now_iso(),
        "source_run_dir": str(source_run_dir.relative_to(ROOT_DIR)),
        "source_selected_final_json": str(selected_final_path.relative_to(ROOT_DIR)),
        "source_model_family": source_config["model_family"],
        "source_horizon_bars": horizon_bars,
        "source_band": float(source_config["band"]),
        "search_split": "valid",
        "short_thresholds": short_thresholds,
        "long_thresholds": long_thresholds,
        "min_trades": int(args.min_trades),
        "decision_logic": {
            "short_candidate": "p_short >= short_threshold",
            "long_candidate": "p_long >= long_threshold",
            "dual_signal_resolution": "higher of p_short and p_long wins; exact tie becomes no-trade",
            "min_margin": 0.0,
            "position_overlap": "disabled",
            "time_exit_bars": horizon_bars,
            "flip": "disabled",
            "same_bar_reentry": "disabled",
            "cost_assumption": "zero",
        },
    }
    write_json(run_dir / "config.json", run_config)

    metrics: list[SweepMetric] = []
    trade_logs: dict[tuple[float, float], pd.DataFrame] = {}
    for short_threshold, long_threshold in product(short_thresholds, long_thresholds):
        metric, trade_log = simulate_threshold_pair(
            valid_frame=valid_frame,
            horizon_bars=horizon_bars,
            short_threshold=short_threshold,
            long_threshold=long_threshold,
        )
        metrics.append(metric)
        trade_logs[(short_threshold, long_threshold)] = trade_log

    results_df = pd.DataFrame([metric.__dict__ for metric in metrics])
    results_df.to_csv(run_dir / "threshold_sweep_results.csv", index=False)

    qualified_df = select_best_rows(results_df, args.min_trades)
    qualified_df.to_csv(run_dir / "threshold_sweep_sorted.csv", index=False)
    qualified_df.to_csv(review_dir / "02A_threshold_sweep_results.csv", index=False)

    best_row = qualified_df.iloc[0].to_dict()
    runner_up = qualified_df.iloc[1].to_dict() if len(qualified_df) > 1 else None
    best_pair = (float(best_row["short_threshold"]), float(best_row["long_threshold"]))
    best_trade_log = trade_logs[best_pair]
    best_trade_log.to_parquet(run_dir / "selected_trade_log.parquet", index=False)

    default_reference, _ = simulate_threshold_pair(
        valid_frame=valid_frame,
        horizon_bars=horizon_bars,
        short_threshold=DEFAULT_REFERENCE_THRESHOLD,
        long_threshold=DEFAULT_REFERENCE_THRESHOLD,
    )

    symmetric_df = qualified_df[
        np.isclose(qualified_df["short_threshold"].to_numpy(), qualified_df["long_threshold"].to_numpy())
    ].copy()
    best_symmetric = symmetric_df.iloc[0].to_dict() if not symmetric_df.empty else None

    summary_payload = {
        "generated_at_utc": utc_now_iso(),
        "phase": "02A_threshold_sweep",
        "selection_metric": "valid_compounded_return",
        "search_split": "valid",
        "source_search_model": source_run_dir.name,
        "reserved_final_confirmation_model": selected_final["final_stage01_run_name"],
        "source_model_family": source_config["model_family"],
        "source_horizon_bars": horizon_bars,
        "source_band": float(source_config["band"]),
        "selected_threshold_seed": best_row,
        "runner_up": runner_up,
        "default_reference_threshold": {
            "short_threshold": DEFAULT_REFERENCE_THRESHOLD,
            "long_threshold": DEFAULT_REFERENCE_THRESHOLD,
            "trade_count": default_reference.trade_count,
            "valid_compounded_return": default_reference.valid_compounded_return,
            "valid_mean_trade_return": default_reference.valid_mean_trade_return,
        },
        "best_symmetric_threshold_pair": best_symmetric,
        "qualified_pair_count": int(len(qualified_df)),
        "tested_pair_count": int(len(results_df)),
    }
    write_json(run_dir / "summary.json", summary_payload)
    write_json(review_dir / "02A_threshold_sweep_review.json", summary_payload)

    review_lines = [
        "# 02A Threshold Sweep Review",
        "",
        f"Generated at: `{utc_now_iso()}`",
        "",
        "## Scope",
        "",
        f"- purpose: `search short_threshold and long_threshold only on the Stage 01 search-side model`",
        f"- source run: `{source_run_dir.name}`",
        f"- reserved final confirmation model: `{selected_final['final_stage01_run_name']}`",
        f"- source model family: `{source_config['model_family']}`",
        f"- horizon: `{horizon_bars}` bars",
        f"- source band: `{float(source_config['band']):.5f}`",
        "- search split: `valid`",
        "- execution assumptions: `min_margin=0, no overlap, no flip, 3-bar time exit, zero cost`",
        "- selection metric: `valid_compounded_return`",
        f"- qualified threshold pairs after min-trades filter: `{len(qualified_df)}`",
        "",
        "## Reference Reads",
        "",
        (
            f"- default threshold reference (`1/3`, `1/3`): compounded_return="
            f"`{default_reference.valid_compounded_return:.4f}`, trades=`{default_reference.trade_count}`"
        ),
    ]
    if best_symmetric is not None:
        review_lines.append(
            f"- best symmetric pair: `({best_symmetric['short_threshold']:.2f}, {best_symmetric['long_threshold']:.2f})`, "
            f"compounded_return=`{best_symmetric['valid_compounded_return']:.4f}`, "
            f"trades=`{int(best_symmetric['trade_count'])}`"
        )
    review_lines.extend(
        [
            "",
            "## Top Results",
            "",
        ]
    )
    for row in qualified_df.head(10).itertuples(index=False):
        review_lines.append(
            f"- `(Ts={row.short_threshold:.2f}, Tl={row.long_threshold:.2f})`: "
            f"compounded_return={row.valid_compounded_return:.4f}, "
            f"mean_trade_return={row.valid_mean_trade_return:.6f}, "
            f"trades={int(row.trade_count)}, longs={int(row.long_trade_count)}, shorts={int(row.short_trade_count)}, "
            f"max_drawdown={row.valid_max_drawdown:.4f}"
        )
    review_lines.extend(
        [
            "",
            "## Selection",
            "",
            f"- selected threshold seed: `(short_threshold={best_row['short_threshold']:.2f}, long_threshold={best_row['long_threshold']:.2f})`",
            f"- selected run folder: `{run_name}`",
            f"- valid compounded return: `{best_row['valid_compounded_return']:.4f}`",
            f"- valid mean trade return: `{best_row['valid_mean_trade_return']:.6f}`",
            f"- trade count: `{int(best_row['trade_count'])}`",
            f"- long trades: `{int(best_row['long_trade_count'])}`",
            f"- short trades: `{int(best_row['short_trade_count'])}`",
            f"- keep or archive: `keep as current Stage 02 seed`",
            "",
            "## Notes",
            "",
            "- This phase is intentionally threshold-only. No margin or probability-gap logic was introduced.",
            "- The selected pair is a search-stage seed on `valid`; it is not the final confirmation artifact yet.",
            "- A strongly asymmetric seed is acceptable here as long as later stages decide whether to preserve or regularize it.",
        ]
    )
    write_text(review_dir / "02A_threshold_sweep_review.md", "\n".join(review_lines) + "\n")

    selected_payload = {
        "generated_at_utc": utc_now_iso(),
        "phase": "02A_threshold_sweep",
        "selection_metric": "valid_compounded_return",
        "search_source_model": source_run_dir.name,
        "reserved_final_confirmation_model": selected_final["final_stage01_run_name"],
        "selected_threshold_seed": best_row,
        "runner_up": runner_up,
        "default_reference_threshold": {
            "short_threshold": DEFAULT_REFERENCE_THRESHOLD,
            "long_threshold": DEFAULT_REFERENCE_THRESHOLD,
            "trade_count": default_reference.trade_count,
            "valid_compounded_return": default_reference.valid_compounded_return,
        },
        "best_symmetric_threshold_pair": best_symmetric,
        "next_step": "later confirmation or carry-forward",
    }
    write_json(selected_dir / "02A_selected_threshold_seed.json", selected_payload)

    selected_lines = [
        "# 02A Selected Threshold Seed",
        "",
        f"- source search model: `{source_run_dir.name}`",
        f"- reserved final confirmation model: `{selected_final['final_stage01_run_name']}`",
        f"- selected short_threshold: `{best_row['short_threshold']:.2f}`",
        f"- selected long_threshold: `{best_row['long_threshold']:.2f}`",
        f"- valid compounded return: `{best_row['valid_compounded_return']:.4f}`",
        f"- trade count: `{int(best_row['trade_count'])}`",
        f"- next step: `later confirmation or carry-forward`",
    ]
    write_text(selected_dir / "02A_selected_threshold_seed.md", "\n".join(selected_lines) + "\n")

    update_review_index(review_dir / "review_index.md")
    update_selection_status(
        selection_status_path=selected_dir / "selection_status.md",
        selected_run_name=run_name,
        short_threshold=float(best_row["short_threshold"]),
        long_threshold=float(best_row["long_threshold"]),
    )

    print(json.dumps(selected_payload, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
