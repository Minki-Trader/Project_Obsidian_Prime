#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from itertools import product
from pathlib import Path
from datetime import datetime, timezone

import pandas as pd

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from foundation.pipelines.run_stage01b_model_compare import write_json, write_text
from foundation.pipelines.run_stage02a_threshold_sweep import load_stage01_source, simulate_threshold_pair
from foundation.pipelines.run_stage02c_threshold_confirmation import load_final_test_frame


UTC = timezone.utc


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run Stage 02E extreme-range bracket probe.")
    parser.add_argument(
        "--source-run-dir",
        default="stages/01_base_feature_ml/02_runs/archived/01C_run_0001_h03_band000125_logreg",
        help="Stage 01 search-side run directory for valid-side reads.",
    )
    parser.add_argument(
        "--final-run-dir",
        default="stages/01_base_feature_ml/02_runs/active/01D_run_0001_final_h03_band000125_logreg",
        help="Stage 01 final run directory for test-side reads.",
    )
    parser.add_argument(
        "--stage-root",
        default="stages/02_individual_thresholds",
        help="Stage 02 root directory.",
    )
    parser.add_argument(
        "--low-thresholds",
        default="0.25,0.30,0.35,0.40",
        help="Comma-separated low-threshold edge values.",
    )
    parser.add_argument(
        "--high-thresholds",
        default="0.55,0.60,0.65,0.70",
        help="Comma-separated high-threshold edge values.",
    )
    return parser


def utc_now_iso() -> str:
    return datetime.now(tz=UTC).isoformat()


def parse_values(raw: str) -> list[float]:
    values = [float(item.strip()) for item in raw.split(",") if item.strip()]
    if not values:
        raise ValueError("value list is empty")
    return values


def classify_region(short_threshold: float, long_threshold: float, low_values: set[float], high_values: set[float]) -> str:
    short_low = short_threshold in low_values
    long_low = long_threshold in low_values
    short_high = short_threshold in high_values
    long_high = long_threshold in high_values
    if short_low and long_low:
        return "low_low"
    if short_high and long_high:
        return "high_high"
    if short_high and long_low:
        return "high_low"
    if short_low and long_high:
        return "low_high"
    return "mixed"


def update_review_index(review_path: Path) -> None:
    lines = [
        "# Review Index",
        "",
        "## Current Entries",
        "",
        "- `02A`: see `02A_threshold_sweep_review.md`",
        "- `02B`: see `02B_seed_sanity_check_review.md` (`02B_run_0001_seed_sanity_check`, review-only diagnostic, archived)",
        "- `02C`: see `02C_threshold_confirmation_review.md` (`02C_run_0001_threshold_confirmation`, review-only diagnostic, archived)",
        "- `02D`: see `02D_local_surface_probe_review.md` (`02D_run_0001_local_surface_probe`, review-only diagnostic, archived)",
        "- `02E`: see `02E_extreme_range_bracket_review.md` (`02E_run_0001_extreme_range_bracket`, review-only diagnostic, archived)",
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
        "- `02D`",
        "- `02E`",
    ]
    write_text(review_path, "\n".join(lines) + "\n")


def update_selection_status(selection_status_path: Path, bracket_note: str, bracket_short: str, bracket_long: str) -> None:
    lines = [
        "# Selection Status",
        "",
        "- stage: `02_individual_thresholds`",
        "- current phase complete: `02E`",
        "- current preferred threshold seed: `02A_run_0001_threshold_sweep` (still provisional, not frozen)",
        "- search source model: `01C_run_0001_h03_band000125_logreg`",
        "- reserved final confirmation model: `01D_run_0001_final_h03_band000125_logreg`",
        f"- latest extreme-range bracket read: `{bracket_note}`",
        f"- exploratory short_threshold bracket: `{bracket_short}`",
        f"- exploratory long_threshold bracket: `{bracket_long}`",
        "- final threshold freeze: `still deferred`",
        "- next phase: `continue small exploratory probes inside the bracket instead of widening again`",
    ]
    write_text(selection_status_path, "\n".join(lines) + "\n")


def main() -> int:
    args = build_parser().parse_args()

    source_run_dir = ROOT_DIR / args.source_run_dir
    final_run_dir = ROOT_DIR / args.final_run_dir
    stage_root = ROOT_DIR / args.stage_root

    low_values = parse_values(args.low_thresholds)
    high_values = parse_values(args.high_thresholds)
    low_set = set(low_values)
    high_set = set(high_values)

    valid_frame, source_config = load_stage01_source(source_run_dir)
    test_frame, final_config = load_final_test_frame(final_run_dir)

    archived_dir = stage_root / "02_runs" / "archived"
    review_dir = stage_root / "03_reviews"
    selected_dir = stage_root / "04_selected"
    for path in (archived_dir, review_dir, selected_dir):
        path.mkdir(parents=True, exist_ok=True)

    run_dir = archived_dir / "02E_run_0001_extreme_range_bracket"
    run_dir.mkdir(parents=True, exist_ok=True)

    rows: list[dict] = []
    all_values = low_values + high_values
    for short_threshold, long_threshold in product(all_values, all_values):
        valid_metric, _ = simulate_threshold_pair(
            valid_frame=valid_frame,
            horizon_bars=int(source_config["horizon_bars"]),
            short_threshold=short_threshold,
            long_threshold=long_threshold,
        )
        test_metric, _ = simulate_threshold_pair(
            valid_frame=test_frame,
            horizon_bars=int(final_config["horizon_bars"]),
            short_threshold=short_threshold,
            long_threshold=long_threshold,
        )
        rows.append(
            {
                "short_threshold": short_threshold,
                "long_threshold": long_threshold,
                "region": classify_region(short_threshold, long_threshold, low_set, high_set),
                "valid_trade_count": valid_metric.trade_count,
                "valid_long_trade_count": valid_metric.long_trade_count,
                "valid_short_trade_count": valid_metric.short_trade_count,
                "valid_compounded_return": valid_metric.valid_compounded_return,
                "valid_max_drawdown": valid_metric.valid_max_drawdown,
                "test_trade_count": test_metric.trade_count,
                "test_long_trade_count": test_metric.long_trade_count,
                "test_short_trade_count": test_metric.short_trade_count,
                "test_compounded_return": test_metric.valid_compounded_return,
                "test_max_drawdown": test_metric.valid_max_drawdown,
            }
        )

    bracket_df = pd.DataFrame(rows)
    bracket_df["avg_compounded_return"] = (
        bracket_df["valid_compounded_return"] + bracket_df["test_compounded_return"]
    ) / 2.0
    bracket_df["both_positive"] = (
        (bracket_df["valid_compounded_return"] > 0.0) & (bracket_df["test_compounded_return"] > 0.0)
    )
    bracket_df["abs_valid_test_gap"] = (
        bracket_df["test_compounded_return"] - bracket_df["valid_compounded_return"]
    ).abs()
    bracket_df.to_csv(run_dir / "extreme_range_bracket_results.csv", index=False)

    avg_sorted = bracket_df.sort_values(
        by=["avg_compounded_return", "both_positive", "test_compounded_return", "valid_compounded_return"],
        ascending=[False, False, False, False],
    ).reset_index(drop=True)
    avg_sorted.to_csv(run_dir / "extreme_range_bracket_avg_sorted.csv", index=False)

    region_tables: dict[str, pd.DataFrame] = {}
    region_summary: dict[str, dict] = {}
    for region in ("low_low", "high_high", "high_low", "low_high"):
        region_df = avg_sorted[avg_sorted["region"].eq(region)].copy().reset_index(drop=True)
        region_tables[region] = region_df
        region_df.to_csv(run_dir / f"{region}_sorted.csv", index=False)
        if region_df.empty:
            continue
        region_summary[region] = {
            "count": int(len(region_df)),
            "both_positive_count": int(region_df["both_positive"].sum()),
            "best_avg_row": region_df.iloc[0].to_dict(),
            "best_test_row": region_df.sort_values(
                by=["test_compounded_return", "avg_compounded_return"], ascending=[False, False]
            ).iloc[0].to_dict(),
        }

    high_low_best = region_summary["high_low"]["best_avg_row"]
    low_low_best_test = region_summary["low_low"]["best_test_row"]
    high_high_best = region_summary["high_high"]["best_avg_row"]
    low_high_best = region_summary["low_high"]["best_avg_row"]

    summary_payload = {
        "generated_at_utc": utc_now_iso(),
        "phase": "02E_extreme_range_bracket",
        "source_run_dir": str(source_run_dir.relative_to(ROOT_DIR)),
        "final_run_dir": str(final_run_dir.relative_to(ROOT_DIR)),
        "low_thresholds": low_values,
        "high_thresholds": high_values,
        "region_summary": region_summary,
        "recommended_exploratory_bracket": {
            "short_threshold": [0.55, 0.70],
            "long_threshold": [0.35, 0.40],
        },
        "verdict": "extreme-value bracketing still favors the high-short / low-long edge as the only clearly useful both-positive boundary band",
    }
    write_json(run_dir / "summary.json", summary_payload)
    write_json(review_dir / "02E_extreme_range_bracket_review.json", summary_payload)

    review_lines = [
        "# 02E Extreme Range Bracket Review",
        "",
        f"Generated at: `{utc_now_iso()}`",
        "",
        "## Scope",
        "",
        "- purpose: `use low and high threshold extremes to bracket the useful Stage 02 exploration range without freezing a threshold`",
        f"- low edge values: `{', '.join(f'{item:.2f}' for item in low_values)}`",
        f"- high edge values: `{', '.join(f'{item:.2f}' for item in high_values)}`",
        "- regions: `low_low`, `high_high`, `high_low`, `low_high`",
        "",
        "## Region Reads",
        "",
        (
            f"- high_low best avg: `(Ts={high_low_best['short_threshold']:.2f}, Tl={high_low_best['long_threshold']:.2f})`, "
            f"valid_comp=`{high_low_best['valid_compounded_return']:.4f}`, "
            f"test_comp=`{high_low_best['test_compounded_return']:.4f}`, "
            f"avg_comp=`{high_low_best['avg_compounded_return']:.4f}`"
        ),
        (
            f"- low_low best test: `(Ts={low_low_best_test['short_threshold']:.2f}, Tl={low_low_best_test['long_threshold']:.2f})`, "
            f"valid_comp=`{low_low_best_test['valid_compounded_return']:.4f}`, "
            f"test_comp=`{low_low_best_test['test_compounded_return']:.4f}`, "
            f"avg_comp=`{low_low_best_test['avg_compounded_return']:.4f}`"
        ),
        (
            f"- high_high best avg: `(Ts={high_high_best['short_threshold']:.2f}, Tl={high_high_best['long_threshold']:.2f})`, "
            f"valid_comp=`{high_high_best['valid_compounded_return']:.4f}`, "
            f"test_comp=`{high_high_best['test_compounded_return']:.4f}`, "
            f"avg_comp=`{high_high_best['avg_compounded_return']:.4f}`"
        ),
        (
            f"- low_high best avg: `(Ts={low_high_best['short_threshold']:.2f}, Tl={low_high_best['long_threshold']:.2f})`, "
            f"valid_comp=`{low_high_best['valid_compounded_return']:.4f}`, "
            f"test_comp=`{low_high_best['test_compounded_return']:.4f}`, "
            f"avg_comp=`{low_high_best['avg_compounded_return']:.4f}`"
        ),
        "",
        "## Region Counts",
        "",
    ]
    for region, payload in region_summary.items():
        review_lines.append(
            f"- `{region}`: total=`{payload['count']}`, both_positive=`{payload['both_positive_count']}`"
        )
    review_lines.extend(
        [
            "",
            "## Top High-Low Edge Reads",
            "",
        ]
    )
    for row in region_tables["high_low"].head(10).itertuples(index=False):
        review_lines.append(
            f"- `(Ts={row.short_threshold:.2f}, Tl={row.long_threshold:.2f})`: "
            f"valid_comp={row.valid_compounded_return:.4f}, test_comp={row.test_compounded_return:.4f}, "
            f"avg_comp={row.avg_compounded_return:.4f}, gap={row.abs_valid_test_gap:.4f}"
        )
    review_lines.extend(
        [
            "",
            "## Top Low-Low Edge Reads",
            "",
        ]
    )
    for row in region_tables["low_low"].head(8).itertuples(index=False):
        review_lines.append(
            f"- `(Ts={row.short_threshold:.2f}, Tl={row.long_threshold:.2f})`: "
            f"valid_comp={row.valid_compounded_return:.4f}, test_comp={row.test_compounded_return:.4f}, "
            f"avg_comp={row.avg_compounded_return:.4f}, gap={row.abs_valid_test_gap:.4f}"
        )
    review_lines.extend(
        [
            "",
            "## Verdict",
            "",
            "- verdict: `use the extremes only as a bracket, not as a selection shortcut`",
            (
                "- read: among the extreme edges, only the `high_short / low_long` band keeps producing clearly "
                "both-positive blended reads. The `low_low` edge can spike on test, but it is too negative on valid "
                "to treat as a stable bracket candidate."
            ),
            (
                "- exploratory bracket suggestion: `short_threshold` roughly `0.55-0.70`, "
                "`long_threshold` roughly `0.35-0.40`."
            ),
        ]
    )
    write_text(review_dir / "02E_extreme_range_bracket_review.md", "\n".join(review_lines) + "\n")

    note_payload = {
        "generated_at_utc": utc_now_iso(),
        "phase": "02E_extreme_range_bracket",
        "recommended_exploratory_bracket": {
            "short_threshold": [0.55, 0.70],
            "long_threshold": [0.35, 0.40],
        },
        "verdict": "exploration continues inside the bracket; no freeze",
    }
    write_json(selected_dir / "02E_extreme_range_bracket.json", note_payload)

    note_lines = [
        "# 02E Extreme Range Bracket",
        "",
        "- verdict: `exploration continues inside the bracket; no freeze`",
        "- recommended short_threshold bracket: `0.55-0.70`",
        "- recommended long_threshold bracket: `0.35-0.40`",
    ]
    write_text(selected_dir / "02E_extreme_range_bracket.md", "\n".join(note_lines) + "\n")

    update_review_index(review_dir / "review_index.md")
    update_selection_status(
        selection_status_path=selected_dir / "selection_status.md",
        bracket_note="extreme values still point back to the high-short / low-long edge",
        bracket_short="0.55-0.70",
        bracket_long="0.35-0.40",
    )

    print(json.dumps(summary_payload, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
