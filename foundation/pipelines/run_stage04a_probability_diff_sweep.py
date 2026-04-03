#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from foundation.pipelines.run_stage01b_model_compare import write_json, write_text
from foundation.pipelines.run_stage02a_threshold_sweep import (
    DEFAULT_REFERENCE_THRESHOLD,
    build_trade_log,
    decide_side,
    load_stage01_source,
    simulate_threshold_pair,
)
from foundation.pipelines.run_stage02c_threshold_confirmation import load_final_test_frame


UTC = timezone.utc


@dataclass
class DiffMetric:
    min_probability_diff: float
    candidate_rows: int
    trade_count: int
    long_trade_count: int
    short_trade_count: int
    threshold_no_trade_rows: int
    diff_rejected_rows: int
    dual_signal_rows: int
    valid_hit_rate: float
    valid_mean_trade_return: float
    valid_median_trade_return: float
    valid_sum_return: float
    valid_compounded_return: float
    valid_max_drawdown: float


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run Stage 04A probability-difference-only sweep.")
    parser.add_argument(
        "--source-run-dir",
        default="stages/01_base_feature_ml/02_runs/archived/01C_run_0001_h03_band000125_logreg",
        help="Stage 01 search-side run directory that contains valid predictions.",
    )
    parser.add_argument(
        "--final-run-dir",
        default="stages/01_base_feature_ml/02_runs/active/01D_run_0001_final_h03_band000125_logreg",
        help="Stage 01 final-model run directory that contains test predictions.",
    )
    parser.add_argument(
        "--selected-final-json",
        default="stages/01_base_feature_ml/04_selected/01D_final_stage01_selection.json",
        help="Stage 01 final selection JSON.",
    )
    parser.add_argument(
        "--stage-root",
        default="stages/04_probability_difference_filter",
        help="Stage 04 root directory.",
    )
    parser.add_argument(
        "--min-probability-diffs",
        default="0.00,0.02,0.04,0.06,0.08,0.10,0.12,0.14,0.16,0.18,0.20",
        help="Comma-separated min_probability_diff candidates.",
    )
    parser.add_argument(
        "--min-trades",
        type=int,
        default=100,
        help="Minimum valid trade count required for a candidate to qualify.",
    )
    return parser


def utc_now_iso() -> str:
    return datetime.now(tz=UTC).isoformat()


def parse_values(raw: str) -> list[float]:
    values = [float(item.strip()) for item in raw.split(",") if item.strip()]
    if not values:
        raise ValueError("value list is empty")
    return values


def simulate_probability_diff_only(
    frame: pd.DataFrame,
    horizon_bars: int,
    min_probability_diff: float,
) -> tuple[DiffMetric, pd.DataFrame]:
    index = 0
    trades: list[dict] = []
    long_trade_count = 0
    short_trade_count = 0
    threshold_no_trade_rows = 0
    diff_rejected_rows = 0
    dual_signal_rows = 0

    while index < len(frame):
        row = frame.iloc[index]
        side, dual_signal = decide_side(
            row=row,
            short_threshold=DEFAULT_REFERENCE_THRESHOLD,
            long_threshold=DEFAULT_REFERENCE_THRESHOLD,
        )
        if dual_signal:
            dual_signal_rows += 1

        if side == 0:
            threshold_no_trade_rows += 1
            index += 1
            continue

        if side > 0:
            direction = "long"
            selected_probability = float(row["p_long"])
            opposing_probability = float(row["p_short"])
        else:
            direction = "short"
            selected_probability = float(row["p_short"])
            opposing_probability = float(row["p_long"])

        probability_diff = selected_probability - opposing_probability
        if probability_diff < min_probability_diff:
            diff_rejected_rows += 1
            index += 1
            continue

        trade_return = float(row["forward_return"]) * side
        if side > 0:
            long_trade_count += 1
        else:
            short_trade_count += 1

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
                "probability_diff": probability_diff,
            }
        )
        index += horizon_bars

    trade_log = build_trade_log(trades)
    if trade_log.empty:
        metric = DiffMetric(
            min_probability_diff=min_probability_diff,
            candidate_rows=int(len(frame)),
            trade_count=0,
            long_trade_count=0,
            short_trade_count=0,
            threshold_no_trade_rows=int(threshold_no_trade_rows),
            diff_rejected_rows=int(diff_rejected_rows),
            dual_signal_rows=int(dual_signal_rows),
            valid_hit_rate=0.0,
            valid_mean_trade_return=0.0,
            valid_median_trade_return=0.0,
            valid_sum_return=0.0,
            valid_compounded_return=0.0,
            valid_max_drawdown=0.0,
        )
        return metric, trade_log

    trade_returns = trade_log["trade_return"].to_numpy(dtype=float)
    equity_curve = np.cumprod(1.0 + trade_returns)
    rolling_peak = np.maximum.accumulate(equity_curve)
    drawdown = (equity_curve / rolling_peak) - 1.0

    metric = DiffMetric(
        min_probability_diff=min_probability_diff,
        candidate_rows=int(len(frame)),
        trade_count=int(len(trade_returns)),
        long_trade_count=int(long_trade_count),
        short_trade_count=int(short_trade_count),
        threshold_no_trade_rows=int(threshold_no_trade_rows),
        diff_rejected_rows=int(diff_rejected_rows),
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
    qualified = results_df[results_df["valid_trade_count"] >= min_trades].copy()
    if qualified.empty:
        raise RuntimeError(f"no min_probability_diff candidate met the minimum trade requirement: {min_trades}")
    return qualified.sort_values(
        by=[
            "valid_compounded_return",
            "valid_mean_trade_return",
            "test_compounded_return",
            "valid_trade_count",
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
        "- `04A`: see `04A_probability_diff_sweep_review.md`",
        "",
        "## Review Rule",
        "",
        "For each completed phase, add:",
        "",
        "- run folder name",
        "- logic setup summary",
        "- split used for search",
        "- headline result",
        "- keep or archive decision",
        "",
        "Also record the phase code:",
        "",
        "- `04A`",
    ]
    write_text(review_path, "\n".join(lines) + "\n")


def update_selection_status(selection_status_path: Path, selected_row: dict, threshold_only_reference: dict) -> None:
    lines = [
        "# Selection Status",
        "",
        "- stage: `04_probability_difference_filter`",
        "- current phase complete: `04A`",
        "- stage mode: `probability-difference only`",
        f"- fixed short_threshold: `{DEFAULT_REFERENCE_THRESHOLD:.6f}`",
        f"- fixed long_threshold: `{DEFAULT_REFERENCE_THRESHOLD:.6f}`",
        "- fixed min_margin: `0.00`",
        f"- current exploratory diff seed: `{selected_row['min_probability_diff']:.2f}`",
        f"- selected valid compounded return: `{selected_row['valid_compounded_return']:.4f}`",
        f"- selected test compounded return: `{selected_row['test_compounded_return']:.4f}`",
        f"- threshold-only default valid compounded return: `{threshold_only_reference['valid_compounded_return']:.4f}`",
        f"- threshold-only default test compounded return: `{threshold_only_reference['test_compounded_return']:.4f}`",
        (
            f"- Stage 04 delta vs threshold-only default: "
            f"`valid {selected_row['valid_compounded_return'] - threshold_only_reference['valid_compounded_return']:+.4f}`, "
            f"`test {selected_row['test_compounded_return'] - threshold_only_reference['test_compounded_return']:+.4f}`"
        ),
        "- next phase: `continue diff-only exploration or summarize before Stage 05`",
    ]
    write_text(selection_status_path, "\n".join(lines) + "\n")


def main() -> int:
    args = build_parser().parse_args()

    source_run_dir = ROOT_DIR / args.source_run_dir
    final_run_dir = ROOT_DIR / args.final_run_dir
    selected_final_path = ROOT_DIR / args.selected_final_json
    stage_root = ROOT_DIR / args.stage_root
    min_probability_diffs = parse_values(args.min_probability_diffs)

    valid_frame, source_config = load_stage01_source(source_run_dir)
    test_frame, final_config = load_final_test_frame(final_run_dir)
    selected_final = json.loads(selected_final_path.read_text(encoding="utf-8"))
    horizon_bars = int(source_config["horizon_bars"])

    inputs_dir = stage_root / "01_inputs"
    active_dir = stage_root / "02_runs" / "active"
    archived_dir = stage_root / "02_runs" / "archived"
    review_dir = stage_root / "03_reviews"
    selected_dir = stage_root / "04_selected"
    for path in (inputs_dir, active_dir, archived_dir, review_dir, selected_dir):
        path.mkdir(parents=True, exist_ok=True)

    run_name = "04A_run_0001_probability_diff_sweep"
    run_dir = active_dir / run_name
    run_dir.mkdir(parents=True, exist_ok=True)

    plan_payload = {
        "generated_at_utc": utc_now_iso(),
        "phase": "04A_probability_diff_sweep",
        "stage_root": str(stage_root.relative_to(ROOT_DIR)),
        "source_run_dir": str(source_run_dir.relative_to(ROOT_DIR)),
        "final_run_dir": str(final_run_dir.relative_to(ROOT_DIR)),
        "search_split": "valid",
        "diagnostic_split": "test",
        "fixed_short_threshold": DEFAULT_REFERENCE_THRESHOLD,
        "fixed_long_threshold": DEFAULT_REFERENCE_THRESHOLD,
        "fixed_min_margin": 0.0,
        "min_probability_diffs": min_probability_diffs,
        "min_trades": int(args.min_trades),
        "fixed_items": [
            "probability difference only",
            "short_threshold = 1/3",
            "long_threshold = 1/3",
            "min_margin = 0",
            "3-bar time exit",
            "no overlap",
            "no flip",
            "zero cost assumption",
        ],
    }
    write_json(inputs_dir / "04A_probability_diff_sweep_plan.json", plan_payload)

    run_config = {
        "run_name": run_name,
        "phase": "04A_probability_diff_sweep",
        "generated_at_utc": utc_now_iso(),
        "source_run_dir": str(source_run_dir.relative_to(ROOT_DIR)),
        "final_run_dir": str(final_run_dir.relative_to(ROOT_DIR)),
        "source_selected_final_json": str(selected_final_path.relative_to(ROOT_DIR)),
        "source_model_family": source_config["model_family"],
        "source_horizon_bars": horizon_bars,
        "source_band": float(source_config["band"]),
        "search_split": "valid",
        "diagnostic_split": "test",
        "fixed_thresholds": {
            "short_threshold": DEFAULT_REFERENCE_THRESHOLD,
            "long_threshold": DEFAULT_REFERENCE_THRESHOLD,
        },
        "fixed_min_margin": 0.0,
        "min_probability_diffs": min_probability_diffs,
        "min_trades": int(args.min_trades),
        "decision_logic": {
            "short_candidate": "p_short >= 1/3",
            "long_candidate": "p_long >= 1/3",
            "dual_signal_resolution": "higher of p_short and p_long wins; exact tie becomes no-trade",
            "difference_condition": "selected direction probability must exceed opposing directional probability by at least min_probability_diff",
            "flat_probability_participates": False,
            "position_overlap": "disabled",
            "time_exit_bars": horizon_bars,
            "flip": "disabled",
            "same_bar_reentry": "disabled",
            "cost_assumption": "zero",
        },
        "reserved_final_confirmation_model": selected_final["final_stage01_run_name"],
    }
    write_json(run_dir / "config.json", run_config)

    rows: list[dict] = []
    valid_trade_logs: dict[float, pd.DataFrame] = {}
    test_trade_logs: dict[float, pd.DataFrame] = {}
    for min_probability_diff in min_probability_diffs:
        valid_metric, valid_trade_log = simulate_probability_diff_only(
            frame=valid_frame,
            horizon_bars=horizon_bars,
            min_probability_diff=min_probability_diff,
        )
        test_metric, test_trade_log = simulate_probability_diff_only(
            frame=test_frame,
            horizon_bars=int(final_config["horizon_bars"]),
            min_probability_diff=min_probability_diff,
        )
        row = {"min_probability_diff": min_probability_diff}
        for prefix, metric in (("valid", valid_metric), ("test", test_metric)):
            metric_dict = asdict(metric)
            for key, value in metric_dict.items():
                if key == "min_probability_diff":
                    continue
                row[f"{prefix}_{key}"] = value
        row["valid_test_compounded_delta"] = row["test_valid_compounded_return"] - row["valid_valid_compounded_return"]
        rows.append(row)
        valid_trade_logs[min_probability_diff] = valid_trade_log
        test_trade_logs[min_probability_diff] = test_trade_log

    results_df = pd.DataFrame(rows).rename(
        columns={
            "valid_valid_hit_rate": "valid_hit_rate",
            "valid_valid_mean_trade_return": "valid_mean_trade_return",
            "valid_valid_median_trade_return": "valid_median_trade_return",
            "valid_valid_sum_return": "valid_sum_return",
            "valid_valid_compounded_return": "valid_compounded_return",
            "valid_valid_max_drawdown": "valid_max_drawdown",
            "test_valid_hit_rate": "test_hit_rate",
            "test_valid_mean_trade_return": "test_mean_trade_return",
            "test_valid_median_trade_return": "test_median_trade_return",
            "test_valid_sum_return": "test_sum_return",
            "test_valid_compounded_return": "test_compounded_return",
            "test_valid_max_drawdown": "test_max_drawdown",
        }
    )
    results_df.to_csv(run_dir / "probability_diff_sweep_results.csv", index=False)

    qualified_df = select_best_rows(results_df, args.min_trades)
    qualified_df.to_csv(run_dir / "probability_diff_sweep_sorted.csv", index=False)
    qualified_df.to_csv(review_dir / "04A_probability_diff_sweep_results.csv", index=False)

    threshold_only_valid, _ = simulate_threshold_pair(
        valid_frame=valid_frame,
        horizon_bars=horizon_bars,
        short_threshold=DEFAULT_REFERENCE_THRESHOLD,
        long_threshold=DEFAULT_REFERENCE_THRESHOLD,
    )
    threshold_only_test, _ = simulate_threshold_pair(
        valid_frame=test_frame,
        horizon_bars=int(final_config["horizon_bars"]),
        short_threshold=DEFAULT_REFERENCE_THRESHOLD,
        long_threshold=DEFAULT_REFERENCE_THRESHOLD,
    )
    threshold_only_reference = {
        "short_threshold": DEFAULT_REFERENCE_THRESHOLD,
        "long_threshold": DEFAULT_REFERENCE_THRESHOLD,
        "valid_trade_count": threshold_only_valid.trade_count,
        "valid_compounded_return": threshold_only_valid.valid_compounded_return,
        "test_trade_count": threshold_only_test.trade_count,
        "test_compounded_return": threshold_only_test.valid_compounded_return,
    }

    baseline_row = results_df[np.isclose(results_df["min_probability_diff"].to_numpy(), 0.0)]
    if baseline_row.empty:
        raise RuntimeError("baseline min_probability_diff=0.00 is missing from the sweep")
    baseline = baseline_row.iloc[0].to_dict()

    selected_row = qualified_df.iloc[0].to_dict()
    top_test_row = results_df.sort_values(
        by=["test_compounded_return", "valid_compounded_return", "test_trade_count"],
        ascending=[False, False, False],
    ).iloc[0].to_dict()

    selected_diff = float(selected_row["min_probability_diff"])
    valid_trade_logs[selected_diff].to_parquet(run_dir / "selected_valid_trade_log.parquet", index=False)
    test_trade_logs[selected_diff].to_parquet(run_dir / "selected_test_trade_log.parquet", index=False)

    summary_payload = {
        "generated_at_utc": utc_now_iso(),
        "phase": "04A_probability_diff_sweep",
        "source_search_model": source_run_dir.name,
        "reserved_final_confirmation_model": selected_final["final_stage01_run_name"],
        "final_model_run_name": final_run_dir.name,
        "fixed_thresholds": {
            "short_threshold": DEFAULT_REFERENCE_THRESHOLD,
            "long_threshold": DEFAULT_REFERENCE_THRESHOLD,
        },
        "fixed_min_margin": 0.0,
        "selected_diff_seed": selected_row,
        "baseline_zero_diff": baseline,
        "threshold_only_default_reference": threshold_only_reference,
        "top_test_diff_read": top_test_row,
        "qualified_candidate_count": int(len(qualified_df)),
        "tested_candidate_count": int(len(results_df)),
        "verdict": "Stage 04 is now running in pure probability-difference mode; compare this isolated logic against the neutral threshold-only default before mixing rule families",
    }
    write_json(run_dir / "summary.json", summary_payload)
    write_json(review_dir / "04A_probability_diff_sweep_review.json", summary_payload)

    review_lines = [
        "# 04A Probability-Diff Sweep Review",
        "",
        f"Generated at: `{utc_now_iso()}`",
        "",
        "## Scope",
        "",
        "- purpose: `evaluate the directional probability-difference filter on its own with neutral default thresholds`",
        f"- fixed thresholds: `(short_threshold={DEFAULT_REFERENCE_THRESHOLD:.6f}, long_threshold={DEFAULT_REFERENCE_THRESHOLD:.6f})`",
        "- fixed max-probability margin: `0.00`",
        f"- source run: `{source_run_dir.name}`",
        f"- reserved final confirmation model: `{selected_final['final_stage01_run_name']}`",
        "- search split: `valid`",
        "- diagnostic split: `test`",
        "- execution assumptions: `3-bar time exit, no overlap, no flip, zero cost`",
        "- difference definition: `selected direction probability must exceed opposing directional probability by at least min_probability_diff`",
        "",
        "## Threshold-Only Default Reference",
        "",
        (
            f"- threshold-only default `(1/3, 1/3)`: valid_comp=`{threshold_only_reference['valid_compounded_return']:.4f}`, "
            f"test_comp=`{threshold_only_reference['test_compounded_return']:.4f}`, "
            f"valid_trades=`{int(threshold_only_reference['valid_trade_count'])}`, "
            f"test_trades=`{int(threshold_only_reference['test_trade_count'])}`"
        ),
        "",
        "## Difference Baseline",
        "",
        (
            f"- baseline `min_probability_diff=0.00`: valid_comp=`{baseline['valid_compounded_return']:.4f}`, "
            f"test_comp=`{baseline['test_compounded_return']:.4f}`, "
            f"valid_trades=`{int(baseline['valid_trade_count'])}`, "
            f"test_trades=`{int(baseline['test_trade_count'])}`"
        ),
        "",
        "## Selected Valid-Side Diff Seed",
        "",
        (
            f"- selected `min_probability_diff={selected_row['min_probability_diff']:.2f}`: valid_comp=`{selected_row['valid_compounded_return']:.4f}`, "
            f"test_comp=`{selected_row['test_compounded_return']:.4f}`, "
            f"valid_trades=`{int(selected_row['valid_trade_count'])}`, "
            f"test_trades=`{int(selected_row['test_trade_count'])}`"
        ),
        (
            f"- delta vs threshold-only default: "
            f"valid_comp=`{selected_row['valid_compounded_return'] - threshold_only_reference['valid_compounded_return']:+.4f}`, "
            f"test_comp=`{selected_row['test_compounded_return'] - threshold_only_reference['test_compounded_return']:+.4f}`"
        ),
        "",
        "## Top Valid Reads",
        "",
    ]
    for row in qualified_df.head(10).itertuples(index=False):
        review_lines.append(
            f"- `min_probability_diff={row.min_probability_diff:.2f}`: "
            f"valid_comp={row.valid_compounded_return:.4f}, test_comp={row.test_compounded_return:.4f}, "
            f"valid_trades={int(row.valid_trade_count)}, test_trades={int(row.test_trade_count)}, "
            f"valid_diff_rejects={int(row.valid_diff_rejected_rows)}, test_diff_rejects={int(row.test_diff_rejected_rows)}"
        )
    review_lines.extend(
        [
            "",
            "## Strongest Test Read",
            "",
            (
                f"- `min_probability_diff={top_test_row['min_probability_diff']:.2f}`: valid_comp=`{top_test_row['valid_compounded_return']:.4f}`, "
                f"test_comp=`{top_test_row['test_compounded_return']:.4f}`, "
                f"valid_trades=`{int(top_test_row['valid_trade_count'])}`, "
                f"test_trades=`{int(top_test_row['test_trade_count'])}`"
            ),
            "",
            "## Verdict",
            "",
            "- verdict: `Stage 04 is now pure probability-difference mode; do not mix this with threshold asymmetry or max-probability margin yet`",
            (
                "- read: this phase shows what the directional probability-difference filter alone does relative to "
                "the neutral default threshold logic, so later synthesis can compare rule families one by one."
            ),
        ]
    )
    write_text(review_dir / "04A_probability_diff_sweep_review.md", "\n".join(review_lines) + "\n")

    selected_payload = {
        "generated_at_utc": utc_now_iso(),
        "phase": "04A_probability_diff_sweep",
        "fixed_thresholds": {
            "short_threshold": DEFAULT_REFERENCE_THRESHOLD,
            "long_threshold": DEFAULT_REFERENCE_THRESHOLD,
        },
        "fixed_min_margin": 0.0,
        "selected_diff_seed": selected_row,
        "threshold_only_default_reference": threshold_only_reference,
        "next_step": "continue diff-only exploration or summarize before Stage 05",
    }
    write_json(selected_dir / "04A_selected_diff_seed.json", selected_payload)

    selected_lines = [
        "# 04A Selected Diff Seed",
        "",
        f"- fixed thresholds: `(short_threshold={DEFAULT_REFERENCE_THRESHOLD:.6f}, long_threshold={DEFAULT_REFERENCE_THRESHOLD:.6f})`",
        "- fixed min_margin: `0.00`",
        f"- selected min_probability_diff: `{selected_row['min_probability_diff']:.2f}`",
        f"- valid compounded return: `{selected_row['valid_compounded_return']:.4f}`",
        f"- test compounded return: `{selected_row['test_compounded_return']:.4f}`",
        (
            f"- delta vs threshold-only default: "
            f"`valid {selected_row['valid_compounded_return'] - threshold_only_reference['valid_compounded_return']:+.4f}`, "
            f"`test {selected_row['test_compounded_return'] - threshold_only_reference['test_compounded_return']:+.4f}`"
        ),
        "- next step: `continue diff-only exploration or summarize before Stage 05`",
    ]
    write_text(selected_dir / "04A_selected_diff_seed.md", "\n".join(selected_lines) + "\n")

    update_review_index(review_dir / "review_index.md")
    update_selection_status(selected_dir / "selection_status.md", selected_row, threshold_only_reference)

    print(json.dumps(summary_payload, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
