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
from foundation.pipelines.run_stage02a_threshold_sweep import DEFAULT_REFERENCE_THRESHOLD


UTC = timezone.utc


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run Stage 03D margin extreme-bracket read.")
    parser.add_argument(
        "--source-results",
        default="stages/03_max_probability_margin/02_runs/active/03A_run_0001_margin_only_sweep/margin_only_sweep_results.csv",
        help="Stage 03A results CSV used as the source for the extreme-bracket read.",
    )
    parser.add_argument(
        "--stage-root",
        default="stages/03_max_probability_margin",
        help="Stage 03 root directory.",
    )
    parser.add_argument(
        "--low-min-margins",
        default="0.00,0.01,0.02,0.03",
        help="Comma-separated low-edge min_margin values.",
    )
    parser.add_argument(
        "--high-min-margins",
        default="0.07,0.08,0.09,0.10",
        help="Comma-separated high-edge min_margin values.",
    )
    return parser


def utc_now_iso() -> str:
    return datetime.now(tz=UTC).isoformat()


def parse_values(raw: str) -> list[float]:
    values = [float(item.strip()) for item in raw.split(",") if item.strip()]
    if not values:
        raise ValueError("value list is empty")
    return values


def fetch_rows(results_df: pd.DataFrame, values: list[float], edge: str) -> list[dict]:
    rows: list[dict] = []
    for value in values:
        match = results_df[np.isclose(results_df["min_margin"].to_numpy(dtype=float), value)]
        if match.empty:
            raise RuntimeError(f"missing min_margin={value:.4f} in source results")
        row = match.iloc[0].to_dict()
        row["edge"] = edge
        rows.append(row)
    return rows


def update_review_index(review_path: Path) -> None:
    lines = [
        "# Review Index",
        "",
        "## Current Entries",
        "",
        "- `03A`: see `03A_margin_only_sweep_review.md`",
        "- `03B`: see `03B_margin_local_probe_review.md` (`03B_run_0001_margin_local_probe`, review-only diagnostic, archived)",
        "- `03C`: see `03C_margin_stability_probe_review.md` (`03C_run_0001_margin_stability_probe`, review-only diagnostic, archived)",
        "- `03D`: see `03D_margin_extreme_bracket_review.md` (`03D_run_0001_margin_extreme_bracket`, review-only diagnostic, archived)",
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
        "- `03A`",
        "- `03B`",
        "- `03C`",
        "- `03D`",
    ]
    write_text(review_path, "\n".join(lines) + "\n")


def update_selection_status(selection_status_path: Path, high_edge_best: dict, low_edge_best_test: dict) -> None:
    lines = [
        "# Selection Status",
        "",
        "- stage: `03_max_probability_margin`",
        "- current phase complete: `03D`",
        "- stage mode: `margin only`",
        f"- fixed short_threshold: `{DEFAULT_REFERENCE_THRESHOLD:.6f}`",
        f"- fixed long_threshold: `{DEFAULT_REFERENCE_THRESHOLD:.6f}`",
        (
            f"- high-edge best blended read: `(min_margin={high_edge_best['min_margin']:.2f})`, "
            f"valid_comp=`{high_edge_best['valid_compounded_return']:.4f}`, "
            f"test_comp=`{high_edge_best['test_compounded_return']:.4f}`"
        ),
        (
            f"- low-edge strongest test read: `(min_margin={low_edge_best_test['min_margin']:.2f})`, "
            f"valid_comp=`{low_edge_best_test['valid_compounded_return']:.4f}`, "
            f"test_comp=`{low_edge_best_test['test_compounded_return']:.4f}`"
        ),
        "- latest extreme-range read: `only the high-margin edge keeps both valid and test positive`",
        "- exploratory margin bracket after extremes: `0.07-0.10`",
        "- next phase: `continue tiny probes inside the high-margin bracket or synthesize before Stage 04`",
    ]
    write_text(selection_status_path, "\n".join(lines) + "\n")


def main() -> int:
    args = build_parser().parse_args()

    source_results_path = ROOT_DIR / args.source_results
    stage_root = ROOT_DIR / args.stage_root
    low_values = parse_values(args.low_min_margins)
    high_values = parse_values(args.high_min_margins)

    results_df = pd.read_csv(source_results_path)

    archived_dir = stage_root / "02_runs" / "archived"
    review_dir = stage_root / "03_reviews"
    selected_dir = stage_root / "04_selected"
    for path in (archived_dir, review_dir, selected_dir):
        path.mkdir(parents=True, exist_ok=True)

    run_dir = archived_dir / "03D_run_0001_margin_extreme_bracket"
    run_dir.mkdir(parents=True, exist_ok=True)

    rows = fetch_rows(results_df, low_values, "low_edge") + fetch_rows(results_df, high_values, "high_edge")
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
    bracket_df.to_csv(run_dir / "margin_extreme_bracket_results.csv", index=False)

    sorted_df = bracket_df.sort_values(
        by=["both_positive", "avg_compounded_return", "test_compounded_return", "valid_compounded_return"],
        ascending=[False, False, False, False],
    ).reset_index(drop=True)
    sorted_df.to_csv(run_dir / "margin_extreme_bracket_sorted.csv", index=False)

    edge_summary: dict[str, dict] = {}
    edge_tables: dict[str, pd.DataFrame] = {}
    for edge in ("low_edge", "high_edge"):
        edge_df = sorted_df[sorted_df["edge"].eq(edge)].copy().reset_index(drop=True)
        edge_tables[edge] = edge_df
        edge_df.to_csv(run_dir / f"{edge}_sorted.csv", index=False)
        edge_summary[edge] = {
            "count": int(len(edge_df)),
            "both_positive_count": int(edge_df["both_positive"].sum()),
            "best_avg_row": edge_df.iloc[0].to_dict(),
            "best_test_row": edge_df.sort_values(
                by=["test_compounded_return", "avg_compounded_return"], ascending=[False, False]
            ).iloc[0].to_dict(),
        }

    high_edge_best = edge_summary["high_edge"]["best_avg_row"]
    low_edge_best_test = edge_summary["low_edge"]["best_test_row"]

    summary_payload = {
        "generated_at_utc": utc_now_iso(),
        "phase": "03D_margin_extreme_bracket",
        "source_results": str(source_results_path.relative_to(ROOT_DIR)),
        "fixed_thresholds": {
            "short_threshold": DEFAULT_REFERENCE_THRESHOLD,
            "long_threshold": DEFAULT_REFERENCE_THRESHOLD,
        },
        "low_min_margins": low_values,
        "high_min_margins": high_values,
        "edge_summary": edge_summary,
        "recommended_exploratory_bracket": {
            "min_margin": [0.07, 0.10],
        },
        "verdict": "extreme-value bracketing still favors the high-margin edge as the only clearly useful both-positive boundary zone",
    }
    write_json(run_dir / "summary.json", summary_payload)
    write_json(review_dir / "03D_margin_extreme_bracket_review.json", summary_payload)

    review_lines = [
        "# 03D Margin Extreme Bracket Review",
        "",
        f"Generated at: `{utc_now_iso()}`",
        "",
        "## Scope",
        "",
        "- purpose: `use low and high min_margin extremes to bracket the useful Stage 03 margin-only range without freezing a seed`",
        f"- fixed thresholds: `(short_threshold={DEFAULT_REFERENCE_THRESHOLD:.6f}, long_threshold={DEFAULT_REFERENCE_THRESHOLD:.6f})`",
        f"- low edge values: `{', '.join(f'{item:.2f}' for item in low_values)}`",
        f"- high edge values: `{', '.join(f'{item:.2f}' for item in high_values)}`",
        "- edges: `low_edge`, `high_edge`",
        "",
        "## Edge Reads",
        "",
        (
            f"- high-edge best avg: `(min_margin={high_edge_best['min_margin']:.2f})`, "
            f"valid_comp=`{high_edge_best['valid_compounded_return']:.4f}`, "
            f"test_comp=`{high_edge_best['test_compounded_return']:.4f}`, "
            f"avg_comp=`{high_edge_best['avg_compounded_return']:.4f}`"
        ),
        (
            f"- low-edge best test: `(min_margin={low_edge_best_test['min_margin']:.2f})`, "
            f"valid_comp=`{low_edge_best_test['valid_compounded_return']:.4f}`, "
            f"test_comp=`{low_edge_best_test['test_compounded_return']:.4f}`, "
            f"avg_comp=`{low_edge_best_test['avg_compounded_return']:.4f}`"
        ),
        "",
        "## Edge Counts",
        "",
    ]
    for edge, payload in edge_summary.items():
        review_lines.append(
            f"- `{edge}`: total=`{payload['count']}`, both_positive=`{payload['both_positive_count']}`"
        )
    review_lines.extend(
        [
            "",
            "## Top High-Edge Reads",
            "",
        ]
    )
    for row in edge_tables["high_edge"].head(8).itertuples(index=False):
        review_lines.append(
            f"- `min_margin={row.min_margin:.2f}`: "
            f"valid_comp={row.valid_compounded_return:.4f}, test_comp={row.test_compounded_return:.4f}, "
            f"avg_comp={row.avg_compounded_return:.4f}, gap={row.abs_valid_test_gap:.4f}"
        )
    review_lines.extend(
        [
            "",
            "## Top Low-Edge Reads",
            "",
        ]
    )
    for row in edge_tables["low_edge"].head(8).itertuples(index=False):
        review_lines.append(
            f"- `min_margin={row.min_margin:.2f}`: "
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
                "- read: among the extreme edges, only the high-margin side keeps both valid and test positive. "
                "The low-margin edge can spike on test, but it stays negative on valid and does not look stable enough "
                "to treat as the main Stage 03 pocket."
            ),
            "- exploratory bracket suggestion: `min_margin` roughly `0.07-0.10`.",
        ]
    )
    write_text(review_dir / "03D_margin_extreme_bracket_review.md", "\n".join(review_lines) + "\n")

    note_payload = {
        "generated_at_utc": utc_now_iso(),
        "phase": "03D_margin_extreme_bracket",
        "recommended_exploratory_bracket": {
            "min_margin": [0.07, 0.10],
        },
        "verdict": "margin-only exploration continues inside the high-margin bracket; no freeze",
    }
    write_json(selected_dir / "03D_margin_extreme_bracket.json", note_payload)

    note_lines = [
        "# 03D Margin Extreme Bracket",
        "",
        "- verdict: `margin-only exploration continues inside the high-margin bracket; no freeze`",
        "- recommended min_margin bracket: `0.07-0.10`",
    ]
    write_text(selected_dir / "03D_margin_extreme_bracket.md", "\n".join(note_lines) + "\n")

    update_review_index(review_dir / "review_index.md")
    update_selection_status(selected_dir / "selection_status.md", high_edge_best, low_edge_best_test)

    print(json.dumps(summary_payload, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
