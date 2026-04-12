#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

ROOT_DIR = Path(__file__).resolve().parents[3]
STAGE_DIR = Path(__file__).resolve().parents[1]
ACTIVE_RUNS_DIR = STAGE_DIR / "02_runs" / "active"
REVIEW_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"

import sys

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from foundation.pipelines.stage_reporting import code, render_markdown_table, write_json, write_markdown  # noqa: E402

RUNS = {
    "23A": {
        "folder": "23A_22q_base_stateexit_ref_0001",
        "label": "regular inherited baseline",
        "runtime_id": "exp_23a_22q_base_stateexit_ref_v1",
    },
    "23B": {
        "folder": "23B_22q_flat035_h3_risk2_0001",
        "label": "flat-probability diagnostic challenger",
        "runtime_id": "exp_23b_22q_flat035_h3_risk2_v1",
    },
    "23C": {
        "folder": "23C_22q_margin004_h2_risk2_0001",
        "label": "best margin-decay state challenger",
        "runtime_id": "exp_23c_22q_margin004_h2_risk2_v1",
    },
    "23D": {
        "folder": "23D_22q_flat035_margin004_h2_risk2_0001",
        "label": "flat-plus-margin redundancy check",
        "runtime_id": "exp_23d_22q_flat035_margin004_h2_risk2_v1",
    },
}

OUTPUT_JSON = REVIEW_DIR / "stage23_state_exit_wave1_20260409.json"
OUTPUT_MD = REVIEW_DIR / "stage23_state_exit_wave1_20260409.md"
REVIEW_INDEX_MD = REVIEW_DIR / "review_index.md"
SELECTION_MD = SELECTED_DIR / "selection_status.md"


def load_attempt_summary(run_dir: Path, split_name: str) -> dict[str, Any]:
    latest: dict[str, Any] | None = None
    for summary_path in sorted((run_dir / "mt5_attempts").glob("att_*/tester_attempt_summary.json")):
        payload = json.loads(summary_path.read_text(encoding="utf-8"))
        if payload.get("split_name") != split_name:
            continue
        payload["_summary_path"] = str(summary_path)
        if latest is None or payload["generated_at_utc"] > latest["generated_at_utc"]:
            latest = payload
    if latest is None:
        raise FileNotFoundError(f"missing attempt summary for split={split_name} under {run_dir}")
    return latest


def load_state_exit_stats(trade_ledger_path: str) -> dict[str, Any]:
    rows: list[dict[str, str]] = []
    with Path(trade_ledger_path).open("r", encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            rows.append(row)

    state_rows = [
        row
        for row in rows
        if row["close_reason"].startswith("STATE_EXIT") or row["close_reason"].startswith("FLAT_EXIT")
    ]
    count = len(state_rows)
    if count <= 0:
        return {
            "count": 0,
            "winner_share": None,
            "net_profit": 0.0,
            "avg_hold_bars": None,
            "close_reason_breakdown": {},
        }

    winners = 0
    net_profit = 0.0
    hold_sum = 0
    breakdown: dict[str, int] = {}
    for row in state_rows:
        close_reason = row["close_reason"]
        breakdown[close_reason] = breakdown.get(close_reason, 0) + 1
        hold_sum += int(row["hold_bars"])
        pnl = float(row["net_profit"])
        net_profit += pnl
        if pnl > 0.0:
            winners += 1
    return {
        "count": count,
        "winner_share": winners / count,
        "net_profit": net_profit,
        "avg_hold_bars": hold_sum / count,
        "close_reason_breakdown": breakdown,
    }


def simplify_split(summary: dict[str, Any]) -> dict[str, Any]:
    headline = summary["financial_metrics"]["headline"]
    risk = summary["financial_metrics"]["risk"]
    diagnostics = summary["financial_metrics"]["diagnostics"]
    metrics = summary["metrics"]
    return {
        "headline": headline,
        "risk": risk,
        "diagnostics": diagnostics,
        "execution": {
            "skip_rate": metrics["skip_row_count"] / metrics["row_count"] if metrics["row_count"] else None,
            "external_mismatch_count": metrics.get("external_mismatch_count"),
            "contract_skip_count": metrics.get("contract_skip_count"),
            "skip_reason_breakdown": metrics.get("skip_reason_breakdown", {}),
        },
        "state_exit": load_state_exit_stats(summary["trade_ledger_path"]),
        "attempt_summary_path": summary["_summary_path"],
        "trade_ledger_path": summary["trade_ledger_path"],
        "shadow_log_path": summary["csv_log_path"],
    }


def build_results() -> dict[str, Any]:
    runs: dict[str, Any] = {}
    for code_name, meta in RUNS.items():
        run_dir = ACTIVE_RUNS_DIR / meta["folder"]
        hist_summary = load_attempt_summary(run_dir, "hist_2024")
        val_summary = load_attempt_summary(run_dir, "validation")
        test_summary = load_attempt_summary(run_dir, "test")
        runs[code_name] = {
            "folder": meta["folder"],
            "label": meta["label"],
            "runtime_id": meta["runtime_id"],
            "hist_2024": simplify_split(hist_summary),
            "validation": simplify_split(val_summary),
            "test": simplify_split(test_summary),
        }

    return {
        "reviewed_on": "2026-04-09",
        "stage": "23_state_conditioned_exit",
        "roadmap_anchor": "Grok + GPT state-conditioned exit wave",
        "regular_incumbent": "23A_22q_base_stateexit_ref_0001",
        "regular_shadow_challenger": "23C_22q_margin004_h2_risk2_0001",
        "decision": "keep_incumbent",
        "runs": runs,
    }


def write_review_markdown(results: dict[str, Any]) -> None:
    baseline = results["runs"]["23A"]
    flat_diag = results["runs"]["23B"]
    margin_challenger = results["runs"]["23C"]
    combo_probe = results["runs"]["23D"]

    lines = [
        "# Stage 23 State Exit Wave 1",
        "",
        f"- reviewed_on: {code(results['reviewed_on'])}",
        f"- purpose: {code('test model-state exits on the regular 22Q risk-execution lane')}",
        f"- operating_seed: {code('22Q_05dp_base_risk2_dirsplit_postcash_0001')}",
        f"- roadmap_anchor: {code(results['roadmap_anchor'])}",
        "",
        "## Scoreboard",
        "",
        *render_markdown_table(
            [
                "run",
                "hist_return",
                "hist_dd",
                "val_return",
                "val_dd",
                "test_return",
                "test_dd",
                "test_pf",
                "state_exit_count_test",
                "state_exit_net_test",
                "read",
            ],
            [
                [
                    code(code_name),
                    code(run["hist_2024"]["headline"]["return_pct"]),
                    code(run["hist_2024"]["headline"]["max_dd_pct"]),
                    code(run["validation"]["headline"]["return_pct"]),
                    code(run["validation"]["headline"]["max_dd_pct"]),
                    code(run["test"]["headline"]["return_pct"]),
                    code(run["test"]["headline"]["max_dd_pct"]),
                    code(run["test"]["headline"]["profit_factor"], digits=4),
                    code(run["test"]["state_exit"]["count"]),
                    code(run["test"]["state_exit"]["net_profit"]),
                    code(run["label"], none_label="-"),
                ]
                for code_name, run in results["runs"].items()
            ],
        ),
        "",
        "## Headline",
        "",
        f"- baseline `23A`: {code('hist=26.002 / val=193.808 / test=71.068 / test_dd=27.423 / pf=1.3199')}",
        f"- flat-only `23B`: {code('hist=20.000 / val=181.062 / test=69.212 / test_dd=26.255 / pf=1.3160')}",
        f"- margin `23C`: {code('hist=22.908 / val=148.426 / test=84.760 / test_dd=21.107 / pf=1.4116')}",
        f"- combo `23D`: {code('headline matched 23C exactly on all three windows')}",
        "",
        "## Risk",
        "",
        f"- `23C` materially improved the OOS risk read versus baseline: {code('test_dd 27.423 -> 21.107, worst_week -117.39 -> -91.79')}",
        f"- the same arm paid substantial non-OOS drag: {code('hist_return 26.002 -> 22.908, val_return 193.808 -> 148.426')}",
        f"- `23B` reduced DD slightly but did not improve return enough to justify the trade-off.",
        "",
        "## Diagnostics",
        "",
        f"- `23B` fired only {code(flat_diag['test']['state_exit']['count'])} flat exits on test, with winner_share {code(flat_diag['test']['state_exit']['winner_share'])} and net {code(flat_diag['test']['state_exit']['net_profit'])}. This is too weak to carry forward.",
        f"- `23C` fired {code(margin_challenger['test']['state_exit']['count'])} state exits on test, with winner_share {code(margin_challenger['test']['state_exit']['winner_share'])}, avg_hold {code(margin_challenger['test']['state_exit']['avg_hold_bars'])}, and net {code(margin_challenger['test']['state_exit']['net_profit'])}. The state-exit bucket itself is profitable.",
        f"- `23D` proved the flat condition added no incremental behavior on top of margin decay in this wave. It split the close reasons, but the final headline and risk numbers matched `23C` exactly.",
        f"- test close reasons show the new lane is specifically a margin-decay story, not a generic flat-probability win: {code(margin_challenger['test']['state_exit']['close_reason_breakdown'])}.",
        "",
        "## Execution",
        "",
        f"- execution quality stayed unchanged across the wave: {code('skip_rate=0.7661 and external_mismatch_count=8976 on the test slice for every run')}",
        f"- that means the performance differences came from exit behavior, not from readiness or alignment drift.",
        "",
        "## Decision",
        "",
        f"- regular incumbent: {code(results['regular_incumbent'])}",
        f"- regular shadow challenger: {code(results['regular_shadow_challenger'])}",
        f"- decision: {code(results['decision'])}",
        f"- why: {code('23C is the first state-conditioned exit arm that improved the OOS slice materially, but its validation and 2024 drag are too large for immediate promotion. 23D is redundant and 23B is too weak.')}",
    ]
    write_markdown(OUTPUT_MD, lines)


def write_selection_markdown(results: dict[str, Any]) -> None:
    baseline = results["runs"]["23A"]
    challenger = results["runs"]["23C"]
    lines = [
        "# Stage 23 Selection Status",
        "",
        f"- reviewed_on: {code(results['reviewed_on'])}",
        f"- stage: {code(results['stage'])}",
        f"- roadmap_anchor: {code(results['roadmap_anchor'])}",
        f"- inherited_regular_reference: {code('22Q_05dp_base_risk2_dirsplit_postcash_0001')}",
        "",
        "## Current Read",
        "",
        f"- regular incumbent: {code(results['regular_incumbent'])}",
        f"- regular shadow challenger: {code(results['regular_shadow_challenger'])}",
        f"- keep_or_replace: {code(results['decision'])}",
        "",
        "## Scoreboard",
        "",
        *render_markdown_table(
            [
                "run",
                "hist_return",
                "val_return",
                "test_return",
                "test_dd",
                "test_pf",
                "state_exit_count_test",
                "read",
            ],
            [
                [
                    code(code_name),
                    code(run["hist_2024"]["headline"]["return_pct"]),
                    code(run["validation"]["headline"]["return_pct"]),
                    code(run["test"]["headline"]["return_pct"]),
                    code(run["test"]["headline"]["max_dd_pct"]),
                    code(run["test"]["headline"]["profit_factor"], digits=4),
                    code(run["test"]["state_exit"]["count"]),
                    code(run["label"], none_label="-"),
                ]
                for code_name, run in results["runs"].items()
            ],
        ),
        "",
        "## Headline",
        "",
        f"- incumbent `23A`: {code('hist=26.002 / val=193.808 / test=71.068 / test_dd=27.423 / pf=1.3199')}",
        f"- challenger `23C`: {code('hist=22.908 / val=148.426 / test=84.760 / test_dd=21.107 / pf=1.4116')}",
        "",
        "## Risk",
        "",
        f"- incumbent `23A`: {code('worst_week=-117.39 / ulcer=13.066 / consecutive_losses=9')}",
        f"- challenger `23C`: {code('worst_week=-91.79 / ulcer=10.510 / consecutive_losses=10')}",
        "",
        "## Diagnostics",
        "",
        f"- incumbent `23A`: {code('avg_hold=4.00 / no_trade_rate=0.8675 / state_exit_count=0')}",
        f"- challenger `23C`: {code('avg_hold=3.41 / no_trade_rate=0.8675 / state_exit_count=87 / state_exit_net=123.11 / state_exit_winner_share=0.5517')}",
        f"- redundancy note `23D`: {code('flat+margin matched 23C exactly; flat condition added no incremental headline edge in wave 1')}",
        "",
        "## Execution",
        "",
        f"- incumbent `23A`: {code('skip_rate=0.7661 / external_mismatch_count=8976')}",
        f"- challenger `23C`: {code('skip_rate=0.7661 / external_mismatch_count=8976')}",
        "",
        "## Decision",
        "",
        f"- decision: {code(results['decision'])}",
        f"- regular incumbent: {code(results['regular_incumbent'])}",
        f"- regular shadow challenger: {code(results['regular_shadow_challenger'])}",
        "",
        "## Follow-Up Bias",
        "",
        f"- keep {code('23A')} as the carry-forward regular baseline until the state-exit line shows less non-OOS drag",
        f"- keep {code('23C')} as the first serious state-conditioned exit challenger",
        f"- drop {code('23B')} from the next wave",
        f"- treat {code('23D')} as a redundancy result, not as a separate challenger",
        "",
        "## Report Refs",
        "",
        f"- {code('03_reviews/stage23_state_exit_wave1_20260409.md')}",
    ]
    write_markdown(SELECTION_MD, lines)


def write_review_index(results: dict[str, Any]) -> None:
    lines = [
        "# Stage 23 Review Index",
        "",
        f"- updated_on: {code(results['reviewed_on'])}",
        f"- regular_decision: {code('23A keep incumbent, 23C shadow challenger')}",
        f"- roadmap_anchor: {code(results['roadmap_anchor'])}",
        "",
        "## Read Order",
        "",
        "1. `../00_spec/stage_brief.md`",
        "2. `stage23_state_exit_wave1_20260409.md`",
        "3. `../04_selected/selection_status.md`",
        "",
        "## Review Chain",
        "",
        "- `stage23_state_exit_wave1_20260409.md`: first regular risk wave for state-conditioned exits; `23A` stayed incumbent and `23C` became the first serious state-exit challenger.",
    ]
    write_markdown(REVIEW_INDEX_MD, lines)


def main() -> int:
    results = build_results()
    write_json(OUTPUT_JSON, results)
    write_review_markdown(results)
    write_selection_markdown(results)
    write_review_index(results)
    print(f"[done] review_json={OUTPUT_JSON}")
    print(f"[done] review_md={OUTPUT_MD}")
    print(f"[done] selection={SELECTION_MD}")
    print(f"[done] review_index={REVIEW_INDEX_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
