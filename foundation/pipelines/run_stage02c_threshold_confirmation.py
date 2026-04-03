#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
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
    simulate_threshold_pair,
)


UTC = timezone.utc


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run Stage 02C threshold confirmation review.")
    parser.add_argument(
        "--threshold-results",
        default="stages/02_individual_thresholds/02_runs/active/02A_run_0001_threshold_sweep/threshold_sweep_sorted.csv",
        help="Sorted Stage 02A threshold results CSV.",
    )
    parser.add_argument(
        "--selected-threshold-json",
        default="stages/02_individual_thresholds/04_selected/02A_selected_threshold_seed.json",
        help="Stage 02A selected threshold seed JSON.",
    )
    parser.add_argument(
        "--seed-sanity-json",
        default="stages/02_individual_thresholds/04_selected/02B_seed_sanity_check.json",
        help="Stage 02B sanity-check JSON.",
    )
    parser.add_argument(
        "--final-run-dir",
        default="stages/01_base_feature_ml/02_runs/active/01D_run_0001_final_h03_band000125_logreg",
        help="Stage 01 final run directory with test predictions.",
    )
    parser.add_argument(
        "--stage-root",
        default="stages/02_individual_thresholds",
        help="Stage 02 root directory.",
    )
    return parser


def utc_now_iso() -> str:
    return datetime.now(tz=UTC).isoformat()


def load_final_test_frame(final_run_dir: Path) -> tuple[pd.DataFrame, dict]:
    config_path = final_run_dir / "config.json"
    predictions_path = final_run_dir / "test_predictions.parquet"
    if not config_path.exists():
        raise FileNotFoundError(f"missing final run config: {config_path}")
    if not predictions_path.exists():
        raise FileNotFoundError(f"missing final test predictions: {predictions_path}")

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

    test_dataset = dataset[dataset["split"].eq("test")].copy()
    merged = test_dataset.merge(predictions, on=["timestamp", "split", "forward_return"], how="inner")
    merged = merged.sort_values("timestamp").reset_index(drop=True)

    if len(merged) != len(predictions):
        raise RuntimeError("test prediction rows do not align cleanly with the final dataset")
    if not merged["label"].equals(merged["label_true"]):
        raise RuntimeError("label mismatch between final dataset and test predictions")

    return merged, config


def rank_value(sorted_frame: pd.DataFrame, short_threshold: float, long_threshold: float) -> int | None:
    match = sorted_frame[
        np.isclose(sorted_frame["short_threshold"].to_numpy(), short_threshold)
        & np.isclose(sorted_frame["long_threshold"].to_numpy(), long_threshold)
    ]
    if match.empty:
        return None
    return int(match.index[0] + 1)


def update_review_index(review_path: Path) -> None:
    lines = [
        "# Review Index",
        "",
        "## Current Entries",
        "",
        "- `02A`: see `02A_threshold_sweep_review.md`",
        "- `02B`: see `02B_seed_sanity_check_review.md` (`02B_run_0001_seed_sanity_check`, review-only diagnostic, archived)",
        "- `02C`: see `02C_threshold_confirmation_review.md` (`02C_run_0001_threshold_confirmation`, review-only diagnostic, archived)",
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
        "- `02B`",
        "- `02C`",
    ]
    write_text(review_path, "\n".join(lines) + "\n")


def update_selection_status(
    selection_status_path: Path,
    preferred_seed: dict,
    balanced_challenger: dict | None,
    top_test_pair: dict,
    preferred_rank: int | None,
    balanced_rank: int | None,
    verdict: str,
) -> None:
    lines = [
        "# Selection Status",
        "",
        "- stage: `02_individual_thresholds`",
        "- current phase complete: `02C`",
        "- current preferred threshold seed: `02A_run_0001_threshold_sweep` (provisional, not frozen)",
        "- search source model: `01C_run_0001_h03_band000125_logreg`",
        "- reserved final confirmation model: `01D_run_0001_final_h03_band000125_logreg`",
        f"- preferred seed short_threshold: `{preferred_seed['short_threshold']:.2f}`",
        f"- preferred seed long_threshold: `{preferred_seed['long_threshold']:.2f}`",
        f"- preferred seed test compounded return: `{preferred_seed['test_compounded_return']:.4f}`",
        f"- preferred seed test rank within current 02A grid: `{preferred_rank}`",
    ]
    if balanced_challenger is not None:
        lines.extend(
            [
                (
                    f"- balanced challenger: `(short_threshold={balanced_challenger['short_threshold']:.2f}, "
                    f"long_threshold={balanced_challenger['long_threshold']:.2f})`"
                ),
                f"- balanced challenger test compounded return: `{balanced_challenger['test_compounded_return']:.4f}`",
                f"- balanced challenger test rank within current 02A grid: `{balanced_rank}`",
            ]
        )
    lines.extend(
        [
            (
                f"- strongest test read inside current 02A grid: "
                f"`(short_threshold={top_test_pair['short_threshold']:.2f}, long_threshold={top_test_pair['long_threshold']:.2f})`"
            ),
            f"- strongest test-grid compounded return: `{top_test_pair['test_compounded_return']:.4f}`",
            f"- confirmation verdict: `{verdict}`",
            "- final threshold freeze: `deferred by user`",
            "- next phase: `decide how to handle the valid-test rank mismatch before freezing`",
        ]
    )
    write_text(selection_status_path, "\n".join(lines) + "\n")


def main() -> int:
    args = build_parser().parse_args()

    results_path = ROOT_DIR / args.threshold_results
    selected_path = ROOT_DIR / args.selected_threshold_json
    sanity_path = ROOT_DIR / args.seed_sanity_json
    final_run_dir = ROOT_DIR / args.final_run_dir
    stage_root = ROOT_DIR / args.stage_root

    valid_results = pd.read_csv(results_path)
    selected_payload = json.loads(selected_path.read_text(encoding="utf-8"))
    sanity_payload = json.loads(sanity_path.read_text(encoding="utf-8"))
    test_frame, final_config = load_final_test_frame(final_run_dir)

    archived_dir = stage_root / "02_runs" / "archived"
    review_dir = stage_root / "03_reviews"
    selected_dir = stage_root / "04_selected"
    for path in (archived_dir, review_dir, selected_dir):
        path.mkdir(parents=True, exist_ok=True)

    run_dir = archived_dir / "02C_run_0001_threshold_confirmation"
    run_dir.mkdir(parents=True, exist_ok=True)

    test_rows: list[dict] = []
    for row in valid_results.itertuples(index=False):
        metric, _ = simulate_threshold_pair(
            valid_frame=test_frame,
            horizon_bars=int(final_config["horizon_bars"]),
            short_threshold=float(row.short_threshold),
            long_threshold=float(row.long_threshold),
        )
        payload = row._asdict()
        payload.update(
            {
                "test_trade_count": metric.trade_count,
                "test_long_trade_count": metric.long_trade_count,
                "test_short_trade_count": metric.short_trade_count,
                "test_no_trade_rows": metric.no_trade_rows,
                "test_dual_signal_rows": metric.dual_signal_rows,
                "test_hit_rate": metric.valid_hit_rate,
                "test_mean_trade_return": metric.valid_mean_trade_return,
                "test_median_trade_return": metric.valid_median_trade_return,
                "test_sum_return": metric.valid_sum_return,
                "test_compounded_return": metric.valid_compounded_return,
                "test_max_drawdown": metric.valid_max_drawdown,
            }
        )
        test_rows.append(payload)

    confirmation_df = pd.DataFrame(test_rows)
    confirmation_df["valid_test_compounded_delta"] = (
        confirmation_df["test_compounded_return"] - confirmation_df["valid_compounded_return"]
    )
    confirmation_df["valid_test_trade_delta"] = confirmation_df["test_trade_count"] - confirmation_df["trade_count"]
    confirmation_df.to_csv(run_dir / "threshold_confirmation_results.csv", index=False)

    sorted_test_df = confirmation_df.sort_values(
        by=["test_compounded_return", "test_mean_trade_return", "test_trade_count"],
        ascending=[False, False, False],
    ).reset_index(drop=True)
    sorted_test_df.to_csv(run_dir / "threshold_confirmation_sorted.csv", index=False)
    sorted_test_df.head(20).to_csv(review_dir / "02C_threshold_confirmation_results.csv", index=False)

    preferred_seed = dict(selected_payload["selected_threshold_seed"])
    preferred_test = sorted_test_df[
        np.isclose(sorted_test_df["short_threshold"].to_numpy(), float(preferred_seed["short_threshold"]))
        & np.isclose(sorted_test_df["long_threshold"].to_numpy(), float(preferred_seed["long_threshold"]))
    ]
    if preferred_test.empty:
        raise RuntimeError("preferred seed is missing from the confirmation grid")
    preferred_test_row = preferred_test.iloc[0].to_dict()

    balanced_challenger = sanity_payload.get("balanced_challenger")
    balanced_test_row = None
    if balanced_challenger is not None:
        balanced_match = sorted_test_df[
            np.isclose(sorted_test_df["short_threshold"].to_numpy(), float(balanced_challenger["short_threshold"]))
            & np.isclose(sorted_test_df["long_threshold"].to_numpy(), float(balanced_challenger["long_threshold"]))
        ]
        if not balanced_match.empty:
            balanced_test_row = balanced_match.iloc[0].to_dict()

    default_metric, _ = simulate_threshold_pair(
        valid_frame=test_frame,
        horizon_bars=int(final_config["horizon_bars"]),
        short_threshold=DEFAULT_REFERENCE_THRESHOLD,
        long_threshold=DEFAULT_REFERENCE_THRESHOLD,
    )
    default_reference = {
        "short_threshold": DEFAULT_REFERENCE_THRESHOLD,
        "long_threshold": DEFAULT_REFERENCE_THRESHOLD,
        "test_trade_count": default_metric.trade_count,
        "test_long_trade_count": default_metric.long_trade_count,
        "test_short_trade_count": default_metric.short_trade_count,
        "test_hit_rate": default_metric.valid_hit_rate,
        "test_mean_trade_return": default_metric.valid_mean_trade_return,
        "test_sum_return": default_metric.valid_sum_return,
        "test_compounded_return": default_metric.valid_compounded_return,
        "test_max_drawdown": default_metric.valid_max_drawdown,
    }

    top_test_pair = sorted_test_df.iloc[0].to_dict()
    preferred_rank = rank_value(
        sorted_test_df, float(preferred_seed["short_threshold"]), float(preferred_seed["long_threshold"])
    )
    balanced_rank = (
        rank_value(
            sorted_test_df,
            float(balanced_challenger["short_threshold"]),
            float(balanced_challenger["long_threshold"]),
        )
        if balanced_challenger is not None
        else None
    )

    valid_test_corr = float(
        confirmation_df["valid_compounded_return"].corr(confirmation_df["test_compounded_return"], method="spearman")
    )

    verdict = (
        "do not freeze Stage 02 threshold yet; confirmation shows a material valid-test rank mismatch"
    )

    summary_payload = {
        "generated_at_utc": utc_now_iso(),
        "phase": "02C_threshold_confirmation",
        "source_threshold_results_csv": str(results_path.relative_to(ROOT_DIR)),
        "source_selected_threshold_json": str(selected_path.relative_to(ROOT_DIR)),
        "source_seed_sanity_json": str(sanity_path.relative_to(ROOT_DIR)),
        "final_model_run_dir": str(final_run_dir.relative_to(ROOT_DIR)),
        "preferred_seed_test_read": preferred_test_row,
        "preferred_seed_test_rank_within_02A_grid": preferred_rank,
        "balanced_challenger_test_read": balanced_test_row,
        "balanced_challenger_test_rank_within_02A_grid": balanced_rank,
        "default_reference_test_read": default_reference,
        "top_test_pair_within_02A_grid": top_test_pair,
        "valid_test_spearman_on_compounded_return": valid_test_corr,
        "verdict": verdict,
    }
    write_json(run_dir / "summary.json", summary_payload)
    write_json(review_dir / "02C_threshold_confirmation_review.json", summary_payload)

    review_lines = [
        "# 02C Threshold Confirmation Review",
        "",
        f"Generated at: `{utc_now_iso()}`",
        "",
        "## Scope",
        "",
        "- purpose: `confirm how the Stage 02 threshold candidates behave on the untouched Stage 01 final-model test split`",
        "- status: `review-only confirmation; final threshold freeze intentionally deferred`",
        "- execution assumptions: `min_margin=0, no overlap, no flip, 3-bar time exit, zero cost`",
        "",
        "## Preferred Seed On Test",
        "",
        (
            f"- preferred seed `(Ts={preferred_test_row['short_threshold']:.2f}, Tl={preferred_test_row['long_threshold']:.2f})`: "
            f"test_compounded_return=`{preferred_test_row['test_compounded_return']:.4f}`, "
            f"test_trades=`{int(preferred_test_row['test_trade_count'])}`, "
            f"test_longs=`{int(preferred_test_row['test_long_trade_count'])}`, "
            f"test_shorts=`{int(preferred_test_row['test_short_trade_count'])}`, "
            f"test_rank_within_02A_grid=`{preferred_rank}`"
        ),
    ]
    if balanced_test_row is not None:
        review_lines.extend(
            [
                "",
                "## Balanced Challenger On Test",
                "",
                (
                    f"- balanced challenger `(Ts={balanced_test_row['short_threshold']:.2f}, Tl={balanced_test_row['long_threshold']:.2f})`: "
                    f"test_compounded_return=`{balanced_test_row['test_compounded_return']:.4f}`, "
                    f"test_trades=`{int(balanced_test_row['test_trade_count'])}`, "
                    f"test_longs=`{int(balanced_test_row['test_long_trade_count'])}`, "
                    f"test_shorts=`{int(balanced_test_row['test_short_trade_count'])}`, "
                    f"test_rank_within_02A_grid=`{balanced_rank}`"
                ),
            ]
        )
    review_lines.extend(
        [
            "",
            "## Reference Reads",
            "",
            (
                f"- default reference `(1/3, 1/3)`: test_compounded_return=`{default_reference['test_compounded_return']:.4f}`, "
                f"test_trades=`{default_reference['test_trade_count']}`"
            ),
            (
                f"- strongest test pair inside current 02A grid: "
                f"`(Ts={top_test_pair['short_threshold']:.2f}, Tl={top_test_pair['long_threshold']:.2f})`, "
                f"test_compounded_return=`{top_test_pair['test_compounded_return']:.4f}`"
            ),
            f"- valid/test spearman over compounded-return ranking: `{valid_test_corr:.3f}`",
            "",
            "## Top Test Reads",
            "",
        ]
    )
    for row in sorted_test_df.head(12).itertuples(index=False):
        review_lines.append(
            f"- `(Ts={row.short_threshold:.2f}, Tl={row.long_threshold:.2f})`: "
            f"test_compounded_return={row.test_compounded_return:.4f}, "
            f"valid_compounded_return={row.valid_compounded_return:.4f}, "
            f"test_trades={int(row.test_trade_count)}, "
            f"test_longs={int(row.test_long_trade_count)}, test_shorts={int(row.test_short_trade_count)}, "
            f"test_max_drawdown={row.test_max_drawdown:.4f}"
        )
    review_lines.extend(
        [
            "",
            "## Verdict",
            "",
            f"- verdict: `{verdict}`",
            (
                "- read: the currently preferred valid-side seed stays profitable on test, but it is not the "
                "top-ranked test pair, and the test ranking differs materially from the valid ranking."
            ),
            (
                "- implication: keep the preferred seed provisional, preserve the balanced challenger, and defer "
                "the final threshold freeze until we decide how to handle this rank mismatch."
            ),
        ]
    )
    write_text(review_dir / "02C_threshold_confirmation_review.md", "\n".join(review_lines) + "\n")

    note_payload = {
        "generated_at_utc": utc_now_iso(),
        "phase": "02C_threshold_confirmation",
        "preferred_seed_test_rank_within_02A_grid": preferred_rank,
        "preferred_seed_test_compounded_return": preferred_test_row["test_compounded_return"],
        "balanced_challenger_test_rank_within_02A_grid": balanced_rank,
        "balanced_challenger_test_compounded_return": (
            balanced_test_row["test_compounded_return"] if balanced_test_row is not None else None
        ),
        "top_test_pair_within_02A_grid": {
            "short_threshold": top_test_pair["short_threshold"],
            "long_threshold": top_test_pair["long_threshold"],
            "test_compounded_return": top_test_pair["test_compounded_return"],
        },
        "verdict": verdict,
    }
    write_json(selected_dir / "02C_threshold_confirmation.json", note_payload)

    selected_lines = [
        "# 02C Threshold Confirmation",
        "",
        f"- verdict: `{verdict}`",
        (
            f"- preferred seed on test: `(short_threshold={preferred_test_row['short_threshold']:.2f}, "
            f"long_threshold={preferred_test_row['long_threshold']:.2f})`, "
            f"compounded_return=`{preferred_test_row['test_compounded_return']:.4f}`, "
            f"rank=`{preferred_rank}`"
        ),
    ]
    if balanced_test_row is not None:
        selected_lines.append(
            (
                f"- balanced challenger on test: `(short_threshold={balanced_test_row['short_threshold']:.2f}, "
                f"long_threshold={balanced_test_row['long_threshold']:.2f})`, "
                f"compounded_return=`{balanced_test_row['test_compounded_return']:.4f}`, "
                f"rank=`{balanced_rank}`"
            )
        )
    selected_lines.append(
        (
            f"- strongest current-grid test pair: `(short_threshold={top_test_pair['short_threshold']:.2f}, "
            f"long_threshold={top_test_pair['long_threshold']:.2f})`, "
            f"compounded_return=`{top_test_pair['test_compounded_return']:.4f}`"
        )
    )
    selected_lines.append("- final threshold freeze remains deferred.")
    write_text(selected_dir / "02C_threshold_confirmation.md", "\n".join(selected_lines) + "\n")

    update_review_index(review_dir / "review_index.md")
    update_selection_status(
        selection_status_path=selected_dir / "selection_status.md",
        preferred_seed=preferred_test_row,
        balanced_challenger=balanced_test_row,
        top_test_pair=top_test_pair,
        preferred_rank=preferred_rank,
        balanced_rank=balanced_rank,
        verdict=verdict,
    )

    print(json.dumps(summary_payload, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
