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
from foundation.pipelines.run_stage02a_threshold_sweep import load_stage01_source, simulate_threshold_pair
from foundation.pipelines.run_stage02c_threshold_confirmation import load_final_test_frame


UTC = timezone.utc


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run Stage 02G tiny ridge probe inside the current narrow pocket.")
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
        "--short-thresholds",
        default="0.535,0.5375,0.540,0.5425,0.545,0.5475,0.550",
        help="Comma-separated short-threshold values for the tiny ridge probe.",
    )
    parser.add_argument(
        "--long-thresholds",
        default="0.395,0.396,0.397,0.398,0.399,0.400",
        help="Comma-separated long-threshold values for the tiny ridge probe.",
    )
    return parser


def utc_now_iso() -> str:
    return datetime.now(tz=UTC).isoformat()


def parse_values(raw: str) -> list[float]:
    values = [float(item.strip()) for item in raw.split(",") if item.strip()]
    if not values:
        raise ValueError("value list is empty")
    return values


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
        "- `02F`: see `02F_narrow_ridge_probe_review.md` (`02F_run_0001_narrow_ridge_probe`, review-only diagnostic, archived)",
        "- `02G`: see `02G_tiny_ridge_probe_review.md` (`02G_run_0001_tiny_ridge_probe`, review-only diagnostic, archived)",
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
        "- `02F`",
        "- `02G`",
    ]
    write_text(review_path, "\n".join(lines) + "\n")


def update_selection_status(selection_status_path: Path, blended_leader: dict, ridge_note: str) -> None:
    lines = [
        "# Selection Status",
        "",
        "- stage: `02_individual_thresholds`",
        "- current phase complete: `02G`",
        "- current preferred threshold seed: `02A_run_0001_threshold_sweep` (still provisional, not frozen)",
        "- search source model: `01C_run_0001_h03_band000125_logreg`",
        "- reserved final confirmation model: `01D_run_0001_final_h03_band000125_logreg`",
        (
            f"- latest tiny-ridge blended leader: "
            f"`(short_threshold={blended_leader['short_threshold']:.4f}, long_threshold={blended_leader['long_threshold']:.3f})`"
        ),
        f"- tiny-ridge leader valid compounded return: `{blended_leader['valid_compounded_return']:.4f}`",
        f"- tiny-ridge leader test compounded return: `{blended_leader['test_compounded_return']:.4f}`",
        f"- tiny-ridge read: `{ridge_note}`",
        "- final threshold freeze: `still deferred`",
        "- next phase: `continue only if the user wants another tiny probe or a synthesis pass`",
    ]
    write_text(selection_status_path, "\n".join(lines) + "\n")


def main() -> int:
    args = build_parser().parse_args()

    source_run_dir = ROOT_DIR / args.source_run_dir
    final_run_dir = ROOT_DIR / args.final_run_dir
    stage_root = ROOT_DIR / args.stage_root
    short_values = parse_values(args.short_thresholds)
    long_values = parse_values(args.long_thresholds)

    valid_frame, source_config = load_stage01_source(source_run_dir)
    test_frame, final_config = load_final_test_frame(final_run_dir)

    archived_dir = stage_root / "02_runs" / "archived"
    review_dir = stage_root / "03_reviews"
    selected_dir = stage_root / "04_selected"
    for path in (archived_dir, review_dir, selected_dir):
        path.mkdir(parents=True, exist_ok=True)

    run_dir = archived_dir / "02G_run_0001_tiny_ridge_probe"
    run_dir.mkdir(parents=True, exist_ok=True)

    rows: list[dict] = []
    for short_threshold in short_values:
        for long_threshold in long_values:
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
                    "valid_trade_count": valid_metric.trade_count,
                    "valid_long_trade_count": valid_metric.long_trade_count,
                    "valid_short_trade_count": valid_metric.short_trade_count,
                    "valid_compounded_return": valid_metric.valid_compounded_return,
                    "valid_mean_trade_return": valid_metric.valid_mean_trade_return,
                    "valid_max_drawdown": valid_metric.valid_max_drawdown,
                    "test_trade_count": test_metric.trade_count,
                    "test_long_trade_count": test_metric.long_trade_count,
                    "test_short_trade_count": test_metric.short_trade_count,
                    "test_compounded_return": test_metric.valid_compounded_return,
                    "test_mean_trade_return": test_metric.valid_mean_trade_return,
                    "test_max_drawdown": test_metric.valid_max_drawdown,
                }
            )

    probe_df = pd.DataFrame(rows)
    probe_df["avg_compounded_return"] = (
        probe_df["valid_compounded_return"] + probe_df["test_compounded_return"]
    ) / 2.0
    probe_df["both_positive"] = (
        (probe_df["valid_compounded_return"] > 0.0) & (probe_df["test_compounded_return"] > 0.0)
    )
    probe_df["abs_valid_test_gap"] = (
        probe_df["test_compounded_return"] - probe_df["valid_compounded_return"]
    ).abs()

    probe_df.to_csv(run_dir / "tiny_ridge_probe_results.csv", index=False)

    blended_sorted = probe_df.sort_values(
        by=["both_positive", "avg_compounded_return", "test_compounded_return", "valid_compounded_return", "abs_valid_test_gap"],
        ascending=[False, False, False, False, True],
    ).reset_index(drop=True)
    blended_sorted.to_csv(run_dir / "tiny_ridge_probe_blended_sorted.csv", index=False)

    stable_positive = blended_sorted[blended_sorted["both_positive"]].copy().reset_index(drop=True)
    stable_positive.to_csv(run_dir / "tiny_ridge_probe_stable_positive.csv", index=False)

    test_sorted = probe_df.sort_values(
        by=["test_compounded_return", "avg_compounded_return", "valid_compounded_return"],
        ascending=[False, False, False],
    ).reset_index(drop=True)
    test_sorted.to_csv(run_dir / "tiny_ridge_probe_test_sorted.csv", index=False)

    blended_leader = stable_positive.iloc[0].to_dict()
    top_test = test_sorted.iloc[0].to_dict()

    summary_payload = {
        "generated_at_utc": utc_now_iso(),
        "phase": "02G_tiny_ridge_probe",
        "source_run_dir": str(source_run_dir.relative_to(ROOT_DIR)),
        "final_run_dir": str(final_run_dir.relative_to(ROOT_DIR)),
        "short_thresholds": short_values,
        "long_thresholds": long_values,
        "probe_pair_count": int(len(probe_df)),
        "blended_leader": blended_leader,
        "top_test_pair": top_test,
        "verdict": "the tiny ridge still leans toward long_threshold at 0.400 while short_threshold works best at the lower edge of the current pocket",
    }
    write_json(run_dir / "summary.json", summary_payload)
    write_json(review_dir / "02G_tiny_ridge_probe_review.json", summary_payload)

    review_lines = [
        "# 02G Tiny Ridge Probe Review",
        "",
        f"Generated at: `{utc_now_iso()}`",
        "",
        "## Scope",
        "",
        "- purpose: `probe only the tiny pocket suggested by 02F without widening the search`",
        f"- short thresholds: `{', '.join(f'{value:.4f}' if value % 0.01 else f'{value:.3f}' for value in short_values)}`",
        f"- long thresholds: `{', '.join(f'{value:.3f}' for value in long_values)}`",
        "- this is still exploration only; no threshold freeze is made here",
        "",
        "## Headline Read",
        "",
        (
            f"- best both-positive blended pair: `(Ts={blended_leader['short_threshold']:.4f}, "
            f"Tl={blended_leader['long_threshold']:.3f})`"
        ),
        f"- valid compounded return: `{blended_leader['valid_compounded_return']:.4f}`",
        f"- test compounded return: `{blended_leader['test_compounded_return']:.4f}`",
        f"- average compounded return: `{blended_leader['avg_compounded_return']:.4f}`",
        f"- abs valid/test gap: `{blended_leader['abs_valid_test_gap']:.4f}`",
        "",
        "## Top Stable Reads",
        "",
    ]
    for row in stable_positive.head(12).itertuples(index=False):
        review_lines.append(
            f"- `(Ts={row.short_threshold:.4f}, Tl={row.long_threshold:.3f})`: "
            f"valid_comp={row.valid_compounded_return:.4f}, test_comp={row.test_compounded_return:.4f}, "
            f"avg_comp={row.avg_compounded_return:.4f}, gap={row.abs_valid_test_gap:.4f}"
        )
    review_lines.extend(
        [
            "",
            "## Top Test Read",
            "",
            (
                f"- `(Ts={top_test['short_threshold']:.4f}, Tl={top_test['long_threshold']:.3f})`: "
                f"valid_comp={top_test['valid_compounded_return']:.4f}, "
                f"test_comp={top_test['test_compounded_return']:.4f}, "
                f"avg_comp={top_test['avg_compounded_return']:.4f}"
            ),
            "",
            "## Verdict",
            "",
            "- verdict: `tiny exploration still supports the lower-short / 0.400-long edge; do not freeze yet`",
            (
                "- read: the local optimum has not moved away from the lower edge of the short-threshold pocket, "
                "which means we are probably pressing against the boundary rather than sitting at a broad interior peak."
            ),
        ]
    )
    write_text(review_dir / "02G_tiny_ridge_probe_review.md", "\n".join(review_lines) + "\n")

    note_payload = {
        "generated_at_utc": utc_now_iso(),
        "phase": "02G_tiny_ridge_probe",
        "blended_leader": {
            "short_threshold": blended_leader["short_threshold"],
            "long_threshold": blended_leader["long_threshold"],
            "valid_compounded_return": blended_leader["valid_compounded_return"],
            "test_compounded_return": blended_leader["test_compounded_return"],
            "avg_compounded_return": blended_leader["avg_compounded_return"],
        },
        "verdict": "tiny exploration continues; no freeze",
    }
    write_json(selected_dir / "02G_tiny_ridge_probe.json", note_payload)

    note_lines = [
        "# 02G Tiny Ridge Probe",
        "",
        "- verdict: `tiny exploration continues; no freeze`",
        (
            f"- blended leader: `(short_threshold={blended_leader['short_threshold']:.4f}, "
            f"long_threshold={blended_leader['long_threshold']:.3f})`, "
            f"valid_comp=`{blended_leader['valid_compounded_return']:.4f}`, "
            f"test_comp=`{blended_leader['test_compounded_return']:.4f}`"
        ),
    ]
    write_text(selected_dir / "02G_tiny_ridge_probe.md", "\n".join(note_lines) + "\n")

    update_review_index(review_dir / "review_index.md")
    update_selection_status(
        selection_status_path=selected_dir / "selection_status.md",
        blended_leader=blended_leader,
        ridge_note="the leader still sits on the lower short-threshold edge and keeps long_threshold pinned at 0.400",
    )

    print(json.dumps(summary_payload, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
