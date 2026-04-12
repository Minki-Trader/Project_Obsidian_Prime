#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

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
    "25A": {
        "folder": "25A_24a_base_softctx_ref_0001",
        "label": "regular inherited baseline",
    },
    "25B": {
        "folder": "25B_24a_monshort_t050_m050_0001",
        "label": "Monday short soft suppressor",
    },
    "25C": {
        "folder": "25C_24a_postshort_t050_m030_0001",
        "label": "NY postcash short soft suppressor",
    },
    "25D": {
        "folder": "25D_24a_monpost_t050_m030_psh2_0001",
        "label": "combined short suppressor plus postcash short hold cut",
    },
}

OUTPUT_JSON = REVIEW_DIR / "stage25_soft_contextual_wave1_20260409.json"
OUTPUT_MD = REVIEW_DIR / "stage25_soft_contextual_wave1_20260409.md"
REVIEW_INDEX_MD = REVIEW_DIR / "review_index.md"
SELECTION_MD = SELECTED_DIR / "selection_status.md"
NY_TZ = ZoneInfo("America/New_York")


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


def parse_server_time_as_ny(value: str) -> datetime:
    return datetime.strptime(value, "%Y.%m.%d %H:%M:%S").replace(tzinfo=ZoneInfo("UTC")).astimezone(NY_TZ)


def load_context_trade_stats(trade_ledger_path: str) -> dict[str, Any]:
    monday_short_count = 0
    monday_short_net = 0.0
    postcash_short_count = 0
    postcash_short_net = 0.0
    postcash_short_time_exit_count = 0
    postcash_short_time_exit_net = 0.0
    short_total_count = 0
    short_total_net = 0.0

    with Path(trade_ledger_path).open("r", encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            if row.get("direction") != "SHORT":
                continue
            short_total_count += 1
            net_profit = float(row["net_profit"])
            short_total_net += net_profit
            entry_ny = parse_server_time_as_ny(row["entry_bar_time_server"])
            is_monday = (entry_ny.weekday() == 0)
            is_postcash = ((entry_ny.hour * 60) + entry_ny.minute) >= (16 * 60)

            if is_monday and not is_postcash:
                monday_short_count += 1
                monday_short_net += net_profit
            if is_postcash and not is_monday:
                postcash_short_count += 1
                postcash_short_net += net_profit
            if row.get("close_reason") == "TIME_EXIT_NY_POSTCASH":
                postcash_short_time_exit_count += 1
                postcash_short_time_exit_net += net_profit

    def avg(net: float, count: int) -> float | None:
        if count <= 0:
            return None
        return net / count

    return {
        "short_total_count": short_total_count,
        "short_total_net": short_total_net,
        "short_total_avg": avg(short_total_net, short_total_count),
        "monday_short_count": monday_short_count,
        "monday_short_net": monday_short_net,
        "monday_short_avg": avg(monday_short_net, monday_short_count),
        "postcash_short_count": postcash_short_count,
        "postcash_short_net": postcash_short_net,
        "postcash_short_avg": avg(postcash_short_net, postcash_short_count),
        "postcash_short_time_exit_count": postcash_short_time_exit_count,
        "postcash_short_time_exit_net": postcash_short_time_exit_net,
        "postcash_short_time_exit_avg": avg(postcash_short_time_exit_net, postcash_short_time_exit_count),
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
        },
        "context": load_context_trade_stats(summary["trade_ledger_path"]),
        "attempt_summary_path": summary["_summary_path"],
        "trade_ledger_path": summary["trade_ledger_path"],
        "shadow_log_path": summary["csv_log_path"],
    }


def pick_shadow_challenger(results: dict[str, Any]) -> str:
    candidates = [code_name for code_name in results["runs"] if code_name != "25A"]
    return max(
        candidates,
        key=lambda code_name: (
            results["runs"][code_name]["test"]["headline"]["return_pct"] or float("-inf"),
            -(results["runs"][code_name]["test"]["headline"]["max_dd_pct"] or float("inf")),
        ),
    )


def pick_best_from_codes(results: dict[str, Any], codes: list[str]) -> str:
    return max(
        codes,
        key=lambda code_name: (
            results["runs"][code_name]["test"]["headline"]["return_pct"] or float("-inf"),
            -(results["runs"][code_name]["test"]["headline"]["max_dd_pct"] or float("inf")),
        ),
    )


def decide_incumbent(results: dict[str, Any], challenger_code: str) -> str:
    baseline = results["runs"]["25A"]
    challenger = results["runs"][challenger_code]
    if (
        (challenger["test"]["headline"]["return_pct"] or float("-inf")) > (baseline["test"]["headline"]["return_pct"] or float("-inf"))
        and (challenger["test"]["headline"]["max_dd_pct"] or float("inf")) <= (baseline["test"]["headline"]["max_dd_pct"] or float("inf")) + 1.0
        and (challenger["validation"]["headline"]["return_pct"] or float("-inf")) >= (baseline["validation"]["headline"]["return_pct"] or float("-inf")) - 15.0
        and (challenger["hist_2024"]["headline"]["return_pct"] or float("-inf")) >= (baseline["hist_2024"]["headline"]["return_pct"] or float("-inf")) - 15.0
    ):
        return "replace_incumbent"
    return "keep_incumbent"


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
            "hist_2024": simplify_split(hist_summary),
            "validation": simplify_split(val_summary),
            "test": simplify_split(test_summary),
        }

    base_results = {"runs": runs}
    best_challenger_code = pick_shadow_challenger(base_results)
    decision = decide_incumbent(base_results, best_challenger_code)
    if decision == "replace_incumbent":
        regular_incumbent = runs[best_challenger_code]["folder"]
        remaining = [code_name for code_name in runs if code_name not in {"25A", best_challenger_code}]
        regular_shadow_code = pick_best_from_codes(base_results, remaining) if remaining else "25A"
        inherited_reference = "24A_23a_base_gate_ref_0001"
    else:
        regular_incumbent = "25A_24a_base_softctx_ref_0001"
        regular_shadow_code = best_challenger_code
        inherited_reference = "24A_23a_base_gate_ref_0001"
    return {
        "reviewed_on": "2026-04-09",
        "stage": "25_soft_contextual_control",
        "roadmap_anchor": "Claude + GPT soft contextual threshold and hold-control wave",
        "inherited_regular_reference": inherited_reference,
        "regular_incumbent": regular_incumbent,
        "regular_shadow_challenger": runs[regular_shadow_code]["folder"],
        "regular_shadow_code": regular_shadow_code,
        "best_challenger_code": best_challenger_code,
        "best_challenger_folder": runs[best_challenger_code]["folder"],
        "decision": decision,
        "runs": runs,
    }


def write_review_markdown(results: dict[str, Any]) -> None:
    baseline = results["runs"]["25A"]
    promoted = results["runs"][results["best_challenger_code"]]
    challenger = results["runs"][results["regular_shadow_code"]]

    lines = [
        "# Stage 25 Soft Contextual Thresholds and Hold Control Wave 1",
        "",
        f"- reviewed_on: {code(results['reviewed_on'])}",
        f"- purpose: {code('softly penalize weak short contexts instead of reviving hard detector blocks')}",
        f"- operating_seed: {code('24A_23a_base_gate_ref_0001')}",
        f"- roadmap_anchor: {code(results['roadmap_anchor'])}",
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
                "test_short_count",
                "test_monshort_net",
                "test_postshort_net",
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
                    code(run["test"]["diagnostics"]["short_count"]),
                    code(run["test"]["context"]["monday_short_net"]),
                    code(run["test"]["context"]["postcash_short_net"]),
                    code(run["label"]),
                ]
                for code_name, run in results["runs"].items()
            ],
        ),
        "",
        "## Headline",
        "",
        f"- inherited `25A` reference: {code({'hist': baseline['hist_2024']['headline']['return_pct'], 'val': baseline['validation']['headline']['return_pct'], 'test': baseline['test']['headline']['return_pct'], 'test_dd': baseline['test']['headline']['max_dd_pct'], 'test_pf': baseline['test']['headline']['profit_factor']})}",
        f"- promoted candidate `{results['best_challenger_code']}`: {code({'hist': promoted['hist_2024']['headline']['return_pct'], 'val': promoted['validation']['headline']['return_pct'], 'test': promoted['test']['headline']['return_pct'], 'test_dd': promoted['test']['headline']['max_dd_pct'], 'test_pf': promoted['test']['headline']['profit_factor']})}",
        "",
        "## Risk",
        "",
        f"- inherited reference OOS risk read: {code({'worst_week': baseline['test']['risk']['worst_week'], 'ulcer': baseline['test']['risk']['ulcer_index'], 'consecutive_losses': baseline['test']['risk']['consecutive_losses']})}",
        f"- promoted candidate OOS risk read: {code({'worst_week': promoted['test']['risk']['worst_week'], 'ulcer': promoted['test']['risk']['ulcer_index'], 'consecutive_losses': promoted['test']['risk']['consecutive_losses']})}",
        "",
        "## Diagnostics",
        "",
        f"- inherited reference short pockets: {code({'monday_short_net': baseline['test']['context']['monday_short_net'], 'postcash_short_net': baseline['test']['context']['postcash_short_net'], 'postcash_short_time_exit_net': baseline['test']['context']['postcash_short_time_exit_net']})}",
        f"- promoted candidate short pockets: {code({'monday_short_net': promoted['test']['context']['monday_short_net'], 'postcash_short_net': promoted['test']['context']['postcash_short_net'], 'postcash_short_time_exit_net': promoted['test']['context']['postcash_short_time_exit_net']})}",
        f"- this wave should be read as a `contextual short cleanup` experiment, so `Monday short` and `NY postcash short` nets matter as much as raw test return.",
        "",
        "## Execution",
        "",
        f"- execution path is unchanged: {code('same exact-alignment runtime, same feature contract, same risk_pct execution; only contextual filter penalties and one optional postcash short hold cut changed')}",
        f"- inherited reference test execution: {code({'skip_rate': baseline['test']['execution']['skip_rate'], 'external_mismatch_count': baseline['test']['execution']['external_mismatch_count']})}",
        f"- promoted candidate test execution: {code({'skip_rate': promoted['test']['execution']['skip_rate'], 'external_mismatch_count': promoted['test']['execution']['external_mismatch_count']})}",
        "",
        "## Decision",
        "",
        f"- inherited_regular_reference: {code(results['inherited_regular_reference'])}",
        f"- regular incumbent: {code(results['regular_incumbent'])}",
        f"- regular shadow challenger: {code(results['regular_shadow_challenger'])}",
        f"- decision: {code(results['decision'])}",
        f"- why: {code('replace only if the contextual cleanup helps the regular OOS read without obvious non-OOS damage or obvious short-book starvation')}",
    ]
    write_markdown(OUTPUT_MD, lines)


def write_selection_markdown(results: dict[str, Any]) -> None:
    shadow_code = results["regular_shadow_code"]
    shadow_run = results["runs"][shadow_code]
    lines = [
        "# Stage 25 Selection Status",
        "",
        f"- reviewed_on: {code(results['reviewed_on'])}",
        f"- stage: {code(results['stage'])}",
        f"- roadmap_anchor: {code(results['roadmap_anchor'])}",
        f"- inherited_regular_reference: {code(results['inherited_regular_reference'])}",
        "",
        "## Current Read",
        "",
        f"- regular incumbent: {code(results['regular_incumbent'])}",
        f"- regular shadow challenger: {code(shadow_run['folder'])}",
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
                "test_monshort_net",
                "test_postshort_net",
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
                    code(run["test"]["context"]["monday_short_net"]),
                    code(run["test"]["context"]["postcash_short_net"]),
                    code(run["label"]),
                ]
                for code_name, run in results["runs"].items()
            ],
        ),
        "",
        "## Diagnostics",
        "",
        f"- shadow contextual short read `{shadow_code}`: {code(shadow_run['test']['context'])}",
        "",
        "## Decision",
        "",
        f"- decision: {code(results['decision'])}",
        f"- regular incumbent: {code(results['regular_incumbent'])}",
        f"- regular shadow challenger: {code(shadow_run['folder'])}",
        "",
        "## Follow-Up Bias",
        "",
        "- keep the contextual overlay line only if it improves the OOS short pockets without obvious book starvation",
        "- read the postcash short hold-cut arm as containment logic first, not as a headline-return trick",
        "",
        "## Report Refs",
        "",
        f"- {code('03_reviews/stage25_soft_contextual_wave1_20260409.md')}",
    ]
    write_markdown(SELECTION_MD, lines)


def write_review_index(results: dict[str, Any]) -> None:
    lines = [
        "# Stage 25 Review Index",
        "",
        f"- updated_on: {code(results['reviewed_on'])}",
        f"- regular_decision: {code('wave 1 soft contextual threshold review complete')}",
        f"- roadmap_anchor: {code(results['roadmap_anchor'])}",
        "",
        "## Latest Review",
        "",
        f"- {code('stage25_soft_contextual_wave1_20260409.md')}",
        "",
        "## Current Selected Read",
        "",
        f"- incumbent: {code(results['regular_incumbent'])}",
        f"- shadow_challenger: {code(results['regular_shadow_challenger'])}",
        f"- decision: {code(results['decision'])}",
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
    print(f"[done] review_index={REVIEW_INDEX_MD}")
    print(f"[done] selection={SELECTION_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
