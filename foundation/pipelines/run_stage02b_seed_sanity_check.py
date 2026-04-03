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


UTC = timezone.utc
BALANCED_MIN_DIRECTION_TRADES = 100
BALANCED_MIN_DIRECTION_SHARE = 0.20
PROMOTION_MIN_RETURN_RATIO = 0.85


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run Stage 02B selected-threshold sanity check.")
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
        "--stage-root",
        default="stages/02_individual_thresholds",
        help="Stage 02 root directory.",
    )
    return parser


def utc_now_iso() -> str:
    return datetime.now(tz=UTC).isoformat()


def add_balance_columns(frame: pd.DataFrame) -> pd.DataFrame:
    out = frame.copy()
    out["long_share"] = out["long_trade_count"] / out["trade_count"]
    out["short_share"] = out["short_trade_count"] / out["trade_count"]
    out["minority_share"] = out[["long_share", "short_share"]].min(axis=1)
    out["direction_trade_gap"] = (out["long_trade_count"] - out["short_trade_count"]).abs()
    return out


def balanced_subset(frame: pd.DataFrame) -> pd.DataFrame:
    return frame[
        (frame["long_trade_count"] >= BALANCED_MIN_DIRECTION_TRADES)
        & (frame["short_trade_count"] >= BALANCED_MIN_DIRECTION_TRADES)
        & (frame["minority_share"] >= BALANCED_MIN_DIRECTION_SHARE)
    ].copy()


def top_table(frame: pd.DataFrame, limit: int = 12) -> pd.DataFrame:
    columns = [
        "short_threshold",
        "long_threshold",
        "trade_count",
        "long_trade_count",
        "short_trade_count",
        "long_share",
        "short_share",
        "minority_share",
        "valid_compounded_return",
        "valid_mean_trade_return",
        "valid_max_drawdown",
    ]
    return frame.loc[:, columns].head(limit).copy()


def update_review_index(review_path: Path) -> None:
    lines = [
        "# Review Index",
        "",
        "## Current Entries",
        "",
        "- `02A`: see `02A_threshold_sweep_review.md`",
        "- `02B`: see `02B_seed_sanity_check_review.md` (`02B_run_0001_seed_sanity_check`, review-only diagnostic, archived)",
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
    ]
    write_text(review_path, "\n".join(lines) + "\n")


def update_selection_status(
    selection_status_path: Path,
    selected_seed: dict,
    balanced_challenger: dict | None,
    verdict: str,
) -> None:
    lines = [
        "# Selection Status",
        "",
        "- stage: `02_individual_thresholds`",
        "- current phase complete: `02B`",
        "- current preferred threshold seed: `02A_run_0001_threshold_sweep`",
        "- search source model: `01C_run_0001_h03_band000125_logreg`",
        "- reserved final confirmation model: `01D_run_0001_final_h03_band000125_logreg`",
        f"- selected short_threshold: `{selected_seed['short_threshold']:.2f}`",
        f"- selected long_threshold: `{selected_seed['long_threshold']:.2f}`",
        f"- seed sanity verdict: `{verdict}`",
    ]
    if balanced_challenger is not None:
        lines.extend(
            [
                (
                    f"- balanced challenger: `(short_threshold={balanced_challenger['short_threshold']:.2f}, "
                    f"long_threshold={balanced_challenger['long_threshold']:.2f})`"
                ),
                (
                    f"- balanced challenger compounded return: "
                    f"`{balanced_challenger['valid_compounded_return']:.4f}`"
                ),
            ]
        )
    lines.append("- next phase: `later confirmation or carry-forward`")
    write_text(selection_status_path, "\n".join(lines) + "\n")


def main() -> int:
    args = build_parser().parse_args()

    results_path = ROOT_DIR / args.threshold_results
    selected_path = ROOT_DIR / args.selected_threshold_json
    stage_root = ROOT_DIR / args.stage_root

    results_df = pd.read_csv(results_path)
    results_df = add_balance_columns(results_df)
    selected_payload = json.loads(selected_path.read_text(encoding="utf-8"))
    selected_seed = dict(selected_payload["selected_threshold_seed"])
    overall_best = results_df.iloc[0].to_dict()

    archived_dir = stage_root / "02_runs" / "archived"
    review_dir = stage_root / "03_reviews"
    selected_dir = stage_root / "04_selected"
    for path in (archived_dir, review_dir, selected_dir):
        path.mkdir(parents=True, exist_ok=True)

    run_dir = archived_dir / "02B_run_0001_seed_sanity_check"
    run_dir.mkdir(parents=True, exist_ok=True)

    balanced_df = balanced_subset(results_df).sort_values(
        by=["valid_compounded_return", "valid_mean_trade_return", "trade_count"],
        ascending=[False, False, False],
    )
    balanced_candidate = balanced_df.iloc[0].to_dict() if not balanced_df.empty else None

    performance_ratio = None
    should_promote_balanced = False
    if balanced_candidate is not None and float(overall_best["valid_compounded_return"]) != 0.0:
        performance_ratio = float(balanced_candidate["valid_compounded_return"]) / float(
            overall_best["valid_compounded_return"]
        )
        should_promote_balanced = performance_ratio >= PROMOTION_MIN_RETURN_RATIO

    verdict = (
        "keep current 02A seed; balanced challenger stays as reference"
        if not should_promote_balanced
        else "promote balanced challenger over the raw-return leader"
    )

    top_overall = top_table(results_df, limit=12)
    top_balanced = top_table(balanced_df, limit=8) if balanced_candidate is not None else pd.DataFrame()
    top_overall.to_csv(run_dir / "overall_shortlist.csv", index=False)
    if not top_balanced.empty:
        top_balanced.to_csv(run_dir / "balanced_shortlist.csv", index=False)

    summary_payload = {
        "generated_at_utc": utc_now_iso(),
        "phase": "02B_seed_sanity_check",
        "source_selected_seed_json": str(selected_path.relative_to(ROOT_DIR)),
        "source_threshold_results_csv": str(results_path.relative_to(ROOT_DIR)),
        "balance_guardrail": {
            "min_direction_trades": BALANCED_MIN_DIRECTION_TRADES,
            "min_direction_share": BALANCED_MIN_DIRECTION_SHARE,
            "promotion_min_return_ratio": PROMOTION_MIN_RETURN_RATIO,
        },
        "overall_best": overall_best,
        "balanced_challenger": balanced_candidate,
        "balanced_candidate_return_ratio_vs_overall": performance_ratio,
        "should_promote_balanced": should_promote_balanced,
        "verdict": verdict,
    }
    write_json(run_dir / "summary.json", summary_payload)
    write_json(review_dir / "02B_seed_sanity_check_review.json", summary_payload)

    review_lines = [
        "# 02B Seed Sanity Check Review",
        "",
        f"Generated at: `{utc_now_iso()}`",
        "",
        "## Scope",
        "",
        "- purpose: `sanity-check whether the selected 02A threshold seed is too directionally collapsed to carry forward blindly`",
        "- method: `compare the raw-return leader against a balanced challenger drawn from the existing 02A result table`",
        "- this stays inside threshold-only logic; no margin rule or probability-gap rule is introduced here",
        "",
        "## Guardrail",
        "",
        f"- balanced challenger minimum direction trades: `{BALANCED_MIN_DIRECTION_TRADES}`",
        f"- balanced challenger minimum minority share: `{BALANCED_MIN_DIRECTION_SHARE:.2f}`",
        f"- promotion threshold: keep at least `{PROMOTION_MIN_RETURN_RATIO:.0%}` of the raw-return leader compounded return",
        "",
        "## Overall Best",
        "",
        (
            f"- `(Ts={overall_best['short_threshold']:.2f}, Tl={overall_best['long_threshold']:.2f})`: "
            f"compounded_return=`{overall_best['valid_compounded_return']:.4f}`, "
            f"trades=`{int(overall_best['trade_count'])}`, "
            f"longs=`{int(overall_best['long_trade_count'])}`, "
            f"shorts=`{int(overall_best['short_trade_count'])}`, "
            f"minority_share=`{overall_best['minority_share']:.3f}`"
        ),
    ]
    if balanced_candidate is not None:
        review_lines.extend(
            [
                "",
                "## Balanced Challenger",
                "",
                (
                    f"- `(Ts={balanced_candidate['short_threshold']:.2f}, Tl={balanced_candidate['long_threshold']:.2f})`: "
                    f"compounded_return=`{balanced_candidate['valid_compounded_return']:.4f}`, "
                    f"trades=`{int(balanced_candidate['trade_count'])}`, "
                    f"longs=`{int(balanced_candidate['long_trade_count'])}`, "
                    f"shorts=`{int(balanced_candidate['short_trade_count'])}`, "
                    f"minority_share=`{balanced_candidate['minority_share']:.3f}`"
                ),
                (
                    f"- balanced challenger return ratio vs raw-return leader: "
                    f"`{performance_ratio:.3f}`"
                ),
            ]
        )
    review_lines.extend(
        [
            "",
            "## Verdict",
            "",
            f"- verdict: `{verdict}`",
        ]
    )
    if not should_promote_balanced and balanced_candidate is not None:
        review_lines.extend(
            [
                (
                    "- read: the selected seed is highly long-skewed, but the best genuinely two-sided challenger "
                    "gives up too much compounded return to replace it at this stage."
                ),
                (
                    "- carry-forward implication: keep the current 02A seed as the preferred raw threshold seed, "
                    "but preserve the balanced challenger as the main alternate if later confirmation penalizes "
                    "one-sided behavior."
                ),
            ]
        )
    review_lines.extend(
        [
            "",
            "## Shortlist",
            "",
        ]
    )
    for row in top_overall.itertuples(index=False):
        review_lines.append(
            f"- overall `(Ts={row.short_threshold:.2f}, Tl={row.long_threshold:.2f})`: "
            f"compounded_return={row.valid_compounded_return:.4f}, "
            f"trades={int(row.trade_count)}, longs={int(row.long_trade_count)}, shorts={int(row.short_trade_count)}, "
            f"minority_share={row.minority_share:.3f}, max_drawdown={row.valid_max_drawdown:.4f}"
        )
    write_text(review_dir / "02B_seed_sanity_check_review.md", "\n".join(review_lines) + "\n")

    selected_note_payload = {
        "generated_at_utc": utc_now_iso(),
        "phase": "02B_seed_sanity_check",
        "current_preferred_seed": {
            "short_threshold": float(overall_best["short_threshold"]),
            "long_threshold": float(overall_best["long_threshold"]),
            "valid_compounded_return": float(overall_best["valid_compounded_return"]),
        },
        "balanced_challenger": balanced_candidate,
        "verdict": verdict,
    }
    write_json(selected_dir / "02B_seed_sanity_check.json", selected_note_payload)

    selected_lines = [
        "# 02B Seed Sanity Check",
        "",
        f"- verdict: `{verdict}`",
        (
            f"- current preferred seed: `(short_threshold={overall_best['short_threshold']:.2f}, "
            f"long_threshold={overall_best['long_threshold']:.2f})`"
        ),
        f"- current preferred compounded return: `{overall_best['valid_compounded_return']:.4f}`",
    ]
    if balanced_candidate is not None:
        selected_lines.extend(
            [
                (
                    f"- balanced challenger: `(short_threshold={balanced_candidate['short_threshold']:.2f}, "
                    f"long_threshold={balanced_candidate['long_threshold']:.2f})`"
                ),
                f"- balanced challenger compounded return: `{balanced_candidate['valid_compounded_return']:.4f}`",
            ]
        )
    write_text(selected_dir / "02B_seed_sanity_check.md", "\n".join(selected_lines) + "\n")

    update_review_index(review_dir / "review_index.md")
    update_selection_status(
        selection_status_path=selected_dir / "selection_status.md",
        selected_seed=overall_best,
        balanced_challenger=balanced_candidate,
        verdict=verdict,
    )

    print(json.dumps(summary_payload, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
