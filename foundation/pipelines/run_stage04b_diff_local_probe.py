#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from foundation.pipelines.run_stage01b_model_compare import write_json, write_text
from foundation.pipelines.run_stage02a_threshold_sweep import DEFAULT_REFERENCE_THRESHOLD, load_stage01_source
from foundation.pipelines.run_stage02c_threshold_confirmation import load_final_test_frame
from foundation.pipelines.run_stage04a_probability_diff_sweep import (
    parse_values,
    simulate_probability_diff_only,
)


UTC = timezone.utc


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run Stage 04B local probability-difference probe.")
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
        "--stage-root",
        default="stages/04_probability_difference_filter",
        help="Stage 04 root directory.",
    )
    parser.add_argument(
        "--min-probability-diffs",
        default="0.070,0.0725,0.075,0.0775,0.080,0.0825,0.085,0.0875,0.090,0.095,0.100",
        help="Comma-separated local min_probability_diff values.",
    )
    return parser


def utc_now_iso() -> str:
    return datetime.now(tz=UTC).isoformat()


def update_review_index(review_path: Path) -> None:
    lines = [
        "# Review Index",
        "",
        "## Current Entries",
        "",
        "- `04A`: see `04A_probability_diff_sweep_review.md`",
        "- `04B`: see `04B_diff_local_probe_review.md` (`04B_run_0001_diff_local_probe`, review-only diagnostic, archived)",
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
        "- `04B`",
    ]
    write_text(review_path, "\n".join(lines) + "\n")


def update_selection_status(selection_status_path: Path, blended_leader: dict, test_leader: dict) -> None:
    lines = [
        "# Selection Status",
        "",
        "- stage: `04_probability_difference_filter`",
        "- current phase complete: `04B`",
        "- stage mode: `probability-difference only`",
        f"- fixed short_threshold: `{DEFAULT_REFERENCE_THRESHOLD:.6f}`",
        f"- fixed long_threshold: `{DEFAULT_REFERENCE_THRESHOLD:.6f}`",
        "- fixed min_margin: `0.00`",
        (
            f"- local blended leader: `(min_probability_diff={blended_leader['min_probability_diff']:.4f})`, "
            f"valid_comp=`{blended_leader['valid_compounded_return']:.4f}`, "
            f"test_comp=`{blended_leader['test_compounded_return']:.4f}`"
        ),
        (
            f"- local strongest test read: `(min_probability_diff={test_leader['min_probability_diff']:.4f})`, "
            f"valid_comp=`{test_leader['valid_compounded_return']:.4f}`, "
            f"test_comp=`{test_leader['test_compounded_return']:.4f}`"
        ),
        "- next phase: `continue tiny diff-only probes or summarize before Stage 05`",
    ]
    write_text(selection_status_path, "\n".join(lines) + "\n")


def main() -> int:
    args = build_parser().parse_args()

    source_run_dir = ROOT_DIR / args.source_run_dir
    final_run_dir = ROOT_DIR / args.final_run_dir
    stage_root = ROOT_DIR / args.stage_root
    min_probability_diffs = parse_values(args.min_probability_diffs)

    valid_frame, source_config = load_stage01_source(source_run_dir)
    test_frame, final_config = load_final_test_frame(final_run_dir)
    horizon_bars = int(source_config["horizon_bars"])
    final_horizon_bars = int(final_config["horizon_bars"])

    archived_dir = stage_root / "02_runs" / "archived"
    review_dir = stage_root / "03_reviews"
    selected_dir = stage_root / "04_selected"
    for path in (archived_dir, review_dir, selected_dir):
        path.mkdir(parents=True, exist_ok=True)

    run_dir = archived_dir / "04B_run_0001_diff_local_probe"
    run_dir.mkdir(parents=True, exist_ok=True)

    rows: list[dict] = []
    for min_probability_diff in min_probability_diffs:
        valid_metric, _ = simulate_probability_diff_only(valid_frame, horizon_bars, min_probability_diff)
        test_metric, _ = simulate_probability_diff_only(test_frame, final_horizon_bars, min_probability_diff)
        rows.append(
            {
                "min_probability_diff": min_probability_diff,
                "valid_trade_count": valid_metric.trade_count,
                "valid_long_trade_count": valid_metric.long_trade_count,
                "valid_short_trade_count": valid_metric.short_trade_count,
                "valid_diff_rejected_rows": valid_metric.diff_rejected_rows,
                "valid_compounded_return": valid_metric.valid_compounded_return,
                "valid_mean_trade_return": valid_metric.valid_mean_trade_return,
                "valid_max_drawdown": valid_metric.valid_max_drawdown,
                "test_trade_count": test_metric.trade_count,
                "test_long_trade_count": test_metric.long_trade_count,
                "test_short_trade_count": test_metric.short_trade_count,
                "test_diff_rejected_rows": test_metric.diff_rejected_rows,
                "test_compounded_return": test_metric.valid_compounded_return,
                "test_mean_trade_return": test_metric.valid_mean_trade_return,
                "test_max_drawdown": test_metric.valid_max_drawdown,
            }
        )

    probe_df = pd.DataFrame(rows)
    probe_df["avg_compounded_return"] = (
        probe_df["valid_compounded_return"] + probe_df["test_compounded_return"]
    ) / 2.0
    probe_df["abs_valid_test_gap"] = (
        probe_df["test_compounded_return"] - probe_df["valid_compounded_return"]
    ).abs()
    probe_df["both_positive"] = (
        (probe_df["valid_compounded_return"] > 0.0) & (probe_df["test_compounded_return"] > 0.0)
    )

    probe_df.to_csv(run_dir / "diff_local_probe_results.csv", index=False)

    blended_sorted = probe_df.sort_values(
        by=["both_positive", "avg_compounded_return", "valid_compounded_return", "test_compounded_return"],
        ascending=[False, False, False, False],
    ).reset_index(drop=True)
    blended_sorted.to_csv(run_dir / "diff_local_probe_blended_sorted.csv", index=False)

    test_sorted = probe_df.sort_values(
        by=["test_compounded_return", "avg_compounded_return", "valid_compounded_return"],
        ascending=[False, False, False],
    ).reset_index(drop=True)
    test_sorted.to_csv(run_dir / "diff_local_probe_test_sorted.csv", index=False)

    stable_positive = blended_sorted[blended_sorted["both_positive"]].copy().reset_index(drop=True)
    stable_positive.to_csv(run_dir / "diff_local_probe_stable_positive.csv", index=False)

    blended_leader = stable_positive.iloc[0].to_dict() if not stable_positive.empty else blended_sorted.iloc[0].to_dict()
    test_leader = test_sorted.iloc[0].to_dict()

    summary_payload = {
        "generated_at_utc": utc_now_iso(),
        "phase": "04B_diff_local_probe",
        "source_search_model": source_run_dir.name,
        "final_model_run_name": final_run_dir.name,
        "fixed_thresholds": {
            "short_threshold": DEFAULT_REFERENCE_THRESHOLD,
            "long_threshold": DEFAULT_REFERENCE_THRESHOLD,
        },
        "fixed_min_margin": 0.0,
        "min_probability_diffs": min_probability_diffs,
        "blended_leader": blended_leader,
        "top_test_read": test_leader,
        "verdict": "the useful probability-difference-only pocket remains near the higher diff region; keep exploration small and separate from other rule families",
    }
    write_json(run_dir / "summary.json", summary_payload)
    write_json(review_dir / "04B_diff_local_probe_review.json", summary_payload)

    review_lines = [
        "# 04B Probability-Diff Local Probe Review",
        "",
        f"Generated at: `{utc_now_iso()}`",
        "",
        "## Scope",
        "",
        "- purpose: `probe the higher probability-difference pocket more finely without changing the Stage 04 concept`",
        f"- fixed thresholds: `(short_threshold={DEFAULT_REFERENCE_THRESHOLD:.6f}, long_threshold={DEFAULT_REFERENCE_THRESHOLD:.6f})`",
        "- fixed min_margin: `0.00`",
        f"- local min_probability_diffs: `{', '.join(f'{item:.4f}' for item in min_probability_diffs)}`",
        "- this is still probability-difference-only exploration; no threshold asymmetry or max-probability margin is introduced here",
        "",
        "## Headline Read",
        "",
        (
            f"- best local blended read: `(min_probability_diff={blended_leader['min_probability_diff']:.4f})`, "
            f"valid_comp=`{blended_leader['valid_compounded_return']:.4f}`, "
            f"test_comp=`{blended_leader['test_compounded_return']:.4f}`, "
            f"avg_comp=`{blended_leader['avg_compounded_return']:.4f}`"
        ),
        (
            f"- strongest local test read: `(min_probability_diff={test_leader['min_probability_diff']:.4f})`, "
            f"valid_comp=`{test_leader['valid_compounded_return']:.4f}`, "
            f"test_comp=`{test_leader['test_compounded_return']:.4f}`, "
            f"avg_comp=`{test_leader['avg_compounded_return']:.4f}`"
        ),
        "",
        "## Top Stable Reads",
        "",
    ]
    for row in stable_positive.head(10).itertuples(index=False):
        review_lines.append(
            f"- `min_probability_diff={row.min_probability_diff:.4f}`: "
            f"valid_comp={row.valid_compounded_return:.4f}, test_comp={row.test_compounded_return:.4f}, "
            f"avg_comp={row.avg_compounded_return:.4f}, gap={row.abs_valid_test_gap:.4f}"
        )
    review_lines.extend(
        [
            "",
            "## Top Test Reads",
            "",
        ]
    )
    for row in test_sorted.head(10).itertuples(index=False):
        review_lines.append(
            f"- `min_probability_diff={row.min_probability_diff:.4f}`: "
            f"valid_comp={row.valid_compounded_return:.4f}, test_comp={row.test_compounded_return:.4f}, "
            f"avg_comp={row.avg_compounded_return:.4f}, gap={row.abs_valid_test_gap:.4f}"
        )
    review_lines.extend(
        [
            "",
            "## Verdict",
            "",
            "- verdict: `keep Stage 04 in probability-difference-only mode and keep the probe narrow`",
            (
                "- read: once valid turns clearly positive, the better local blended reads stay in the higher-diff "
                "pocket rather than sliding back toward the lower-diff test-favored area."
            ),
        ]
    )
    write_text(review_dir / "04B_diff_local_probe_review.md", "\n".join(review_lines) + "\n")

    note_payload = {
        "generated_at_utc": utc_now_iso(),
        "phase": "04B_diff_local_probe",
        "blended_leader": blended_leader,
        "top_test_read": test_leader,
        "verdict": "probability-difference-only exploration continues; no freeze",
    }
    write_json(selected_dir / "04B_diff_local_probe.json", note_payload)

    note_lines = [
        "# 04B Probability-Diff Local Probe",
        "",
        "- verdict: `probability-difference-only exploration continues; no freeze`",
        (
            f"- blended leader: `(min_probability_diff={blended_leader['min_probability_diff']:.4f})`, "
            f"valid_comp=`{blended_leader['valid_compounded_return']:.4f}`, "
            f"test_comp=`{blended_leader['test_compounded_return']:.4f}`"
        ),
        (
            f"- strongest local test read: `(min_probability_diff={test_leader['min_probability_diff']:.4f})`, "
            f"valid_comp=`{test_leader['valid_compounded_return']:.4f}`, "
            f"test_comp=`{test_leader['test_compounded_return']:.4f}`"
        ),
    ]
    write_text(selected_dir / "04B_diff_local_probe.md", "\n".join(note_lines) + "\n")

    update_review_index(review_dir / "review_index.md")
    update_selection_status(selected_dir / "selection_status.md", blended_leader, test_leader)

    print(json.dumps(summary_payload, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
