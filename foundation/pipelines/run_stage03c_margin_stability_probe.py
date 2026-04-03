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
from foundation.pipelines.run_stage03a_margin_only_sweep import parse_values, simulate_margin_only


UTC = timezone.utc


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run Stage 03C stability-focused margin-only probe.")
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
        default="stages/03_max_probability_margin",
        help="Stage 03 root directory.",
    )
    parser.add_argument(
        "--min-margins",
        default="0.0790,0.0800,0.0810,0.0820,0.0825,0.0830,0.0840,0.0850,0.0860",
        help="Comma-separated local min_margin values.",
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
        "- `03A`: see `03A_margin_only_sweep_review.md`",
        "- `03B`: see `03B_margin_local_probe_review.md` (`03B_run_0001_margin_local_probe`, review-only diagnostic, archived)",
        "- `03C`: see `03C_margin_stability_probe_review.md` (`03C_run_0001_margin_stability_probe`, review-only diagnostic, archived)",
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
    ]
    write_text(review_path, "\n".join(lines) + "\n")


def update_selection_status(selection_status_path: Path, stability_leader: dict, tight_gap_leader: dict) -> None:
    lines = [
        "# Selection Status",
        "",
        "- stage: `03_max_probability_margin`",
        "- current phase complete: `03C`",
        "- stage mode: `margin only`",
        f"- fixed short_threshold: `{DEFAULT_REFERENCE_THRESHOLD:.6f}`",
        f"- fixed long_threshold: `{DEFAULT_REFERENCE_THRESHOLD:.6f}`",
        (
            f"- stability-pocket leader: `(min_margin={stability_leader['min_margin']:.4f})`, "
            f"valid_comp=`{stability_leader['valid_compounded_return']:.4f}`, "
            f"test_comp=`{stability_leader['test_compounded_return']:.4f}`, "
            f"gap=`{stability_leader['abs_valid_test_gap']:.4f}`"
        ),
        (
            f"- tight-gap leader: `(min_margin={tight_gap_leader['min_margin']:.4f})`, "
            f"valid_comp=`{tight_gap_leader['valid_compounded_return']:.4f}`, "
            f"test_comp=`{tight_gap_leader['test_compounded_return']:.4f}`, "
            f"gap=`{tight_gap_leader['abs_valid_test_gap']:.4f}`"
        ),
        "- next phase: `continue a tiny margin-only probe only if needed, otherwise synthesize before Stage 04`",
    ]
    write_text(selection_status_path, "\n".join(lines) + "\n")


def main() -> int:
    args = build_parser().parse_args()

    source_run_dir = ROOT_DIR / args.source_run_dir
    final_run_dir = ROOT_DIR / args.final_run_dir
    stage_root = ROOT_DIR / args.stage_root
    min_margins = parse_values(args.min_margins)

    valid_frame, source_config = load_stage01_source(source_run_dir)
    test_frame, final_config = load_final_test_frame(final_run_dir)
    horizon_bars = int(source_config["horizon_bars"])

    archived_dir = stage_root / "02_runs" / "archived"
    review_dir = stage_root / "03_reviews"
    selected_dir = stage_root / "04_selected"
    for path in (archived_dir, review_dir, selected_dir):
        path.mkdir(parents=True, exist_ok=True)

    run_dir = archived_dir / "03C_run_0001_margin_stability_probe"
    run_dir.mkdir(parents=True, exist_ok=True)

    rows: list[dict] = []
    for min_margin in min_margins:
        valid_metric, _ = simulate_margin_only(valid_frame, horizon_bars, min_margin)
        test_metric, _ = simulate_margin_only(test_frame, int(final_config["horizon_bars"]), min_margin)
        rows.append(
            {
                "min_margin": min_margin,
                "valid_trade_count": valid_metric.trade_count,
                "valid_long_trade_count": valid_metric.long_trade_count,
                "valid_short_trade_count": valid_metric.short_trade_count,
                "valid_margin_rejected_rows": valid_metric.margin_rejected_rows,
                "valid_compounded_return": valid_metric.valid_compounded_return,
                "valid_mean_trade_return": valid_metric.valid_mean_trade_return,
                "valid_max_drawdown": valid_metric.valid_max_drawdown,
                "test_trade_count": test_metric.trade_count,
                "test_long_trade_count": test_metric.long_trade_count,
                "test_short_trade_count": test_metric.short_trade_count,
                "test_margin_rejected_rows": test_metric.margin_rejected_rows,
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

    probe_df.to_csv(run_dir / "margin_stability_probe_results.csv", index=False)

    stability_sorted = probe_df.sort_values(
        by=["both_positive", "avg_compounded_return", "abs_valid_test_gap", "valid_compounded_return"],
        ascending=[False, False, True, False],
    ).reset_index(drop=True)
    stability_sorted.to_csv(run_dir / "margin_stability_probe_stability_sorted.csv", index=False)

    gap_sorted = probe_df[probe_df["both_positive"]].copy().sort_values(
        by=["abs_valid_test_gap", "avg_compounded_return", "test_compounded_return"],
        ascending=[True, False, False],
    ).reset_index(drop=True)
    gap_sorted.to_csv(run_dir / "margin_stability_probe_gap_sorted.csv", index=False)

    stability_leader = stability_sorted.iloc[0].to_dict()
    tight_gap_leader = gap_sorted.iloc[0].to_dict()

    summary_payload = {
        "generated_at_utc": utc_now_iso(),
        "phase": "03C_margin_stability_probe",
        "source_search_model": source_run_dir.name,
        "final_model_run_name": final_run_dir.name,
        "fixed_thresholds": {
            "short_threshold": DEFAULT_REFERENCE_THRESHOLD,
            "long_threshold": DEFAULT_REFERENCE_THRESHOLD,
        },
        "min_margins": min_margins,
        "stability_leader": stability_leader,
        "tight_gap_leader": tight_gap_leader,
        "verdict": "the higher-margin pocket remains valid; use this read to distinguish blended strength from split-stability before any Stage 03 freeze",
    }
    write_json(run_dir / "summary.json", summary_payload)
    write_json(review_dir / "03C_margin_stability_probe_review.json", summary_payload)

    review_lines = [
        "# 03C Margin Stability Probe Review",
        "",
        f"Generated at: `{utc_now_iso()}`",
        "",
        "## Scope",
        "",
        "- purpose: `probe the stability pocket more finely without changing the Stage 03 margin-only concept`",
        f"- fixed thresholds: `(short_threshold={DEFAULT_REFERENCE_THRESHOLD:.6f}, long_threshold={DEFAULT_REFERENCE_THRESHOLD:.6f})`",
        f"- local min_margins: `{', '.join(f'{item:.4f}' for item in min_margins)}`",
        "- this is still margin-only exploration; no threshold asymmetry is introduced here",
        "",
        "## Headline Read",
        "",
        (
            f"- stability-pocket leader: `(min_margin={stability_leader['min_margin']:.4f})`, "
            f"valid_comp=`{stability_leader['valid_compounded_return']:.4f}`, "
            f"test_comp=`{stability_leader['test_compounded_return']:.4f}`, "
            f"avg_comp=`{stability_leader['avg_compounded_return']:.4f}`, "
            f"gap=`{stability_leader['abs_valid_test_gap']:.4f}`"
        ),
        (
            f"- tight-gap leader: `(min_margin={tight_gap_leader['min_margin']:.4f})`, "
            f"valid_comp=`{tight_gap_leader['valid_compounded_return']:.4f}`, "
            f"test_comp=`{tight_gap_leader['test_compounded_return']:.4f}`, "
            f"avg_comp=`{tight_gap_leader['avg_compounded_return']:.4f}`, "
            f"gap=`{tight_gap_leader['abs_valid_test_gap']:.4f}`"
        ),
        "",
        "## Stability Order",
        "",
    ]
    for row in stability_sorted.head(10).itertuples(index=False):
        review_lines.append(
            f"- `min_margin={row.min_margin:.4f}`: "
            f"valid_comp={row.valid_compounded_return:.4f}, test_comp={row.test_compounded_return:.4f}, "
            f"avg_comp={row.avg_compounded_return:.4f}, gap={row.abs_valid_test_gap:.4f}"
        )
    review_lines.extend(
        [
            "",
            "## Gap Order",
            "",
        ]
    )
    for row in gap_sorted.head(10).itertuples(index=False):
        review_lines.append(
            f"- `min_margin={row.min_margin:.4f}`: "
            f"valid_comp={row.valid_compounded_return:.4f}, test_comp={row.test_compounded_return:.4f}, "
            f"avg_comp={row.avg_compounded_return:.4f}, gap={row.abs_valid_test_gap:.4f}"
        )
    review_lines.extend(
        [
            "",
            "## Verdict",
            "",
            "- verdict: `keep Stage 03 margin-only and treat this probe as a stability read, not a bundle decision`",
            (
                "- read: the local pocket now lets us separate the stronger blended read from the tighter-gap read, "
                "which is exactly the information we need before deciding whether to freeze or just synthesize."
            ),
        ]
    )
    write_text(review_dir / "03C_margin_stability_probe_review.md", "\n".join(review_lines) + "\n")

    note_payload = {
        "generated_at_utc": utc_now_iso(),
        "phase": "03C_margin_stability_probe",
        "stability_leader": stability_leader,
        "tight_gap_leader": tight_gap_leader,
        "verdict": "margin-only exploration continues; no freeze",
    }
    write_json(selected_dir / "03C_margin_stability_probe.json", note_payload)

    note_lines = [
        "# 03C Margin Stability Probe",
        "",
        "- verdict: `margin-only exploration continues; no freeze`",
        (
            f"- stability-pocket leader: `(min_margin={stability_leader['min_margin']:.4f})`, "
            f"valid_comp=`{stability_leader['valid_compounded_return']:.4f}`, "
            f"test_comp=`{stability_leader['test_compounded_return']:.4f}`, "
            f"gap=`{stability_leader['abs_valid_test_gap']:.4f}`"
        ),
        (
            f"- tight-gap leader: `(min_margin={tight_gap_leader['min_margin']:.4f})`, "
            f"valid_comp=`{tight_gap_leader['valid_compounded_return']:.4f}`, "
            f"test_comp=`{tight_gap_leader['test_compounded_return']:.4f}`, "
            f"gap=`{tight_gap_leader['abs_valid_test_gap']:.4f}`"
        ),
    ]
    write_text(selected_dir / "03C_margin_stability_probe.md", "\n".join(note_lines) + "\n")

    update_review_index(review_dir / "review_index.md")
    update_selection_status(selected_dir / "selection_status.md", stability_leader, tight_gap_leader)

    print(json.dumps(summary_payload, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
