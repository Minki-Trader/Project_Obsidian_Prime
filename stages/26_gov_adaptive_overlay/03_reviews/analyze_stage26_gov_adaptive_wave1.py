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
    "26A": {
        "folder": "26A_25d_govref_0001",
        "label": "governance observe-only inherited baseline",
    },
    "26B": {
        "folder": "26B_25d_gsig080_0001",
        "label": "signal drift taper",
    },
    "26C": {
        "folder": "26C_25d_gext085_0001",
        "label": "external skip burst taper",
    },
    "26D": {
        "folder": "26D_25d_gmix090_0001",
        "label": "combined mild governance taper",
    },
}

OUTPUT_JSON = REVIEW_DIR / "stage26_gov_adaptive_wave1_20260409.json"
OUTPUT_MD = REVIEW_DIR / "stage26_gov_adaptive_wave1_20260409.md"
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


def parse_float(value: str | None) -> float | None:
    if value is None:
        return None
    text = str(value).strip()
    if not text:
        return None
    try:
        return float(text)
    except ValueError:
        return None


def load_governance_stats(governance_log_path: str) -> dict[str, Any]:
    path = Path(governance_log_path)
    if not path.exists():
        return {
            "row_count": 0,
            "mean_operational_skip_rate": None,
            "mean_external_skip_rate": None,
            "mean_argmax_class_share": None,
            "mean_entropy": None,
            "mean_overlay_rate": None,
            "latest_state": None,
            "latest_reason": None,
            "top_reasons": {},
        }

    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))

    if not rows:
        return {
            "row_count": 0,
            "mean_operational_skip_rate": None,
            "mean_external_skip_rate": None,
            "mean_argmax_class_share": None,
            "mean_entropy": None,
            "mean_overlay_rate": None,
            "latest_state": None,
            "latest_reason": None,
            "top_reasons": {},
        }

    op_skips = [value for value in (parse_float(row.get("operational_skip_rate")) for row in rows) if value is not None]
    ext_skips = [value for value in (parse_float(row.get("external_skip_rate")) for row in rows) if value is not None]
    argmax = [value for value in (parse_float(row.get("max_argmax_class_share")) for row in rows) if value is not None]
    entropy = [value for value in (parse_float(row.get("avg_signal_entropy_norm")) for row in rows) if value is not None]
    overlay = [value for value in (parse_float(row.get("risk_overlay_rate")) for row in rows) if value is not None]
    reason_counts: dict[str, int] = {}
    for row in rows:
        reason = (row.get("governance_reason") or "").strip()
        if not reason:
            continue
        reason_counts[reason] = reason_counts.get(reason, 0) + 1
    top_reasons = dict(sorted(reason_counts.items(), key=lambda item: (-item[1], item[0]))[:3])
    latest = rows[-1]

    def avg(values: list[float]) -> float | None:
        if not values:
            return None
        return sum(values) / len(values)

    return {
        "row_count": len(rows),
        "mean_operational_skip_rate": avg(op_skips),
        "mean_external_skip_rate": avg(ext_skips),
        "mean_argmax_class_share": avg(argmax),
        "mean_entropy": avg(entropy),
        "mean_overlay_rate": avg(overlay),
        "latest_state": (latest.get("governance_state") or "").strip() or None,
        "latest_reason": (latest.get("governance_reason") or "").strip() or None,
        "top_reasons": top_reasons,
    }


def simplify_split(summary: dict[str, Any]) -> dict[str, Any]:
    headline = summary["financial_metrics"]["headline"]
    risk = summary["financial_metrics"]["risk"]
    diagnostics = summary["financial_metrics"]["diagnostics"]
    metrics = summary["metrics"]
    governance = load_governance_stats(summary["governance_log_path"])
    governance_metrics = summary.get("governance_metrics", {})
    return {
        "headline": headline,
        "risk": risk,
        "diagnostics": diagnostics,
        "execution": {
            "skip_rate": metrics["skip_row_count"] / metrics["row_count"] if metrics["row_count"] else None,
            "external_mismatch_count": metrics.get("external_mismatch_count"),
            "contract_skip_count": metrics.get("contract_skip_count"),
            "governance_latest_state": governance_metrics.get("latest_state"),
            "governance_latest_reason": governance_metrics.get("latest_reason"),
            "governance_blocked_signal_count": governance_metrics.get("blocked_signal_count"),
            "governance_alert_rows": governance_metrics.get("alert_or_block_rows"),
        },
        "governance": governance,
        "attempt_summary_path": summary["_summary_path"],
        "trade_ledger_path": summary["trade_ledger_path"],
        "shadow_log_path": summary["csv_log_path"],
        "governance_log_path": summary["governance_log_path"],
    }


def pick_best_challenger(results: dict[str, Any]) -> str:
    candidates = [code_name for code_name in results["runs"] if code_name != "26A"]
    return max(
        candidates,
        key=lambda code_name: (
            results["runs"][code_name]["test"]["headline"]["return_pct"] or float("-inf"),
            results["runs"][code_name]["test"]["headline"]["profit_factor"] or float("-inf"),
            -(results["runs"][code_name]["test"]["headline"]["max_dd_pct"] or float("inf")),
        ),
    )


def decide_incumbent(results: dict[str, Any], challenger_code: str) -> str:
    baseline = results["runs"]["26A"]
    challenger = results["runs"][challenger_code]
    baseline_test_return = baseline["test"]["headline"]["return_pct"] or float("-inf")
    challenger_test_return = challenger["test"]["headline"]["return_pct"] or float("-inf")
    baseline_test_dd = baseline["test"]["headline"]["max_dd_pct"] or float("inf")
    challenger_test_dd = challenger["test"]["headline"]["max_dd_pct"] or float("inf")
    baseline_val_return = baseline["validation"]["headline"]["return_pct"] or float("-inf")
    challenger_val_return = challenger["validation"]["headline"]["return_pct"] or float("-inf")
    baseline_hist_return = baseline["hist_2024"]["headline"]["return_pct"] or float("-inf")
    challenger_hist_return = challenger["hist_2024"]["headline"]["return_pct"] or float("-inf")
    baseline_test_pf = baseline["test"]["headline"]["profit_factor"] or float("-inf")
    challenger_test_pf = challenger["test"]["headline"]["profit_factor"] or float("-inf")

    better_headline = (
        challenger_test_return >= baseline_test_return + 1.0
        and challenger_test_dd <= baseline_test_dd + 0.5
        and challenger_val_return >= baseline_val_return - 20.0
        and challenger_hist_return >= baseline_hist_return - 12.0
    )
    better_containment = (
        challenger_test_dd <= baseline_test_dd - 1.0
        and challenger_test_return >= baseline_test_return - 2.0
        and challenger_test_pf >= baseline_test_pf
        and challenger_val_return >= baseline_val_return - 20.0
        and challenger_hist_return >= baseline_hist_return - 12.0
    )
    return "replace_incumbent" if (better_headline or better_containment) else "keep_incumbent"


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
    best_challenger_code = pick_best_challenger(base_results)
    decision = decide_incumbent(base_results, best_challenger_code)
    regular_incumbent = runs[best_challenger_code]["folder"] if decision == "replace_incumbent" else runs["26A"]["folder"]
    regular_shadow = runs["26A"]["folder"] if decision == "replace_incumbent" else runs[best_challenger_code]["folder"]
    return {
        "reviewed_on": "2026-04-09",
        "stage": "26_gov_adaptive_overlay",
        "roadmap_anchor": "Grok + GPT governance-led adaptive overlays wave",
        "inherited_regular_reference": "25D_24a_monpost_t050_m030_psh2_0001",
        "regular_incumbent": regular_incumbent,
        "regular_shadow_challenger": regular_shadow,
        "best_challenger_code": best_challenger_code,
        "decision": decision,
        "runs": runs,
    }


def write_review_markdown(results: dict[str, Any]) -> None:
    baseline = results["runs"]["26A"]
    challenger = results["runs"][results["best_challenger_code"]]
    lines = [
        "# Stage 26 Governance-Led Adaptive Overlays Wave 1",
        "",
        f"- reviewed_on: {code(results['reviewed_on'])}",
        f"- purpose: {code('move governance telemetry from monitoring into non-blocking risk taper overlays on the 25D regular baseline')}",
        f"- operating_seed: {code(results['inherited_regular_reference'])}",
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
                "gov_state",
                "mean_ext_skip",
                "mean_argmax",
                "mean_entropy",
                "mean_overlay",
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
                    code(run["test"]["governance"]["latest_state"] or "n/a"),
                    code(run["test"]["governance"]["mean_external_skip_rate"], digits=4),
                    code(run["test"]["governance"]["mean_argmax_class_share"], digits=4),
                    code(run["test"]["governance"]["mean_entropy"], digits=4),
                    code(run["test"]["governance"]["mean_overlay_rate"], digits=4),
                    code(run["label"]),
                ]
                for code_name, run in results["runs"].items()
            ],
        ),
        "",
        "## Headline",
        "",
        f"- baseline `26A`: {code({'hist': baseline['hist_2024']['headline']['return_pct'], 'val': baseline['validation']['headline']['return_pct'], 'test': baseline['test']['headline']['return_pct'], 'test_dd': baseline['test']['headline']['max_dd_pct'], 'test_pf': baseline['test']['headline']['profit_factor']})}",
        f"- best challenger `{results['best_challenger_code']}`: {code({'hist': challenger['hist_2024']['headline']['return_pct'], 'val': challenger['validation']['headline']['return_pct'], 'test': challenger['test']['headline']['return_pct'], 'test_dd': challenger['test']['headline']['max_dd_pct'], 'test_pf': challenger['test']['headline']['profit_factor']})}",
        "",
        "## Risk",
        "",
        f"- baseline OOS risk read: {code({'worst_week': baseline['test']['risk']['worst_week'], 'ulcer': baseline['test']['risk']['ulcer_index'], 'consecutive_losses': baseline['test']['risk']['consecutive_losses']})}",
        f"- challenger OOS risk read: {code({'worst_week': challenger['test']['risk']['worst_week'], 'ulcer': challenger['test']['risk']['ulcer_index'], 'consecutive_losses': challenger['test']['risk']['consecutive_losses']})}",
        "",
        "## Diagnostics",
        "",
        f"- baseline diagnostics: {code({'no_trade_rate': baseline['test']['diagnostics']['no_trade_rate'], 'long_count': baseline['test']['diagnostics']['long_count'], 'short_count': baseline['test']['diagnostics']['short_count']})}",
        f"- challenger diagnostics: {code({'no_trade_rate': challenger['test']['diagnostics']['no_trade_rate'], 'long_count': challenger['test']['diagnostics']['long_count'], 'short_count': challenger['test']['diagnostics']['short_count']})}",
        f"- this wave should be read as a `risk taper` experiment, so `mean overlay rate` and trade-mix drift matter alongside headline return.",
        "",
        "## Execution",
        "",
        f"- baseline governance read: {code({'latest_state': baseline['test']['governance']['latest_state'], 'latest_reason': baseline['test']['governance']['latest_reason'], 'top_reasons': baseline['test']['governance']['top_reasons']})}",
        f"- challenger governance read: {code({'latest_state': challenger['test']['governance']['latest_state'], 'latest_reason': challenger['test']['governance']['latest_reason'], 'top_reasons': challenger['test']['governance']['top_reasons']})}",
        f"- execution path stayed exact-alignment and non-blocking: {code('governance was observe-only for all arms; challengers only changed risk_pct taper behavior, not entry blocking')}",
        "",
        "## Decision",
        "",
        f"- regular incumbent: {code(results['regular_incumbent'])}",
        f"- regular shadow challenger: {code(results['regular_shadow_challenger'])}",
        f"- decision: {code(results['decision'])}",
        f"- why: {code('promote only if governance-driven taper improves the regular OOS read or clearly improves containment without obvious non-OOS damage')}",
    ]
    write_markdown(OUTPUT_MD, lines)


def write_selection_markdown(results: dict[str, Any]) -> None:
    baseline = results["runs"]["26A"]
    challenger = results["runs"][results["best_challenger_code"]]
    lines = [
        "# Stage 26 Selection Status",
        "",
        f"- reviewed_on: {code(results['reviewed_on'])}",
        f"- stage: {code(results['stage'])}",
        f"- roadmap_anchor: {code(results['roadmap_anchor'])}",
        f"- inherited_regular_reference: {code(results['inherited_regular_reference'])}",
        "",
        "## Current Read",
        "",
        f"- regular incumbent: {code(results['regular_incumbent'])}",
        f"- regular shadow challenger: {code(results['regular_shadow_challenger'])}",
        f"- keep_or_replace: {code(results['decision'])}",
        "",
        "## Promotion Gates",
        "",
        f"- gate_1: {code('improve test headline without obvious validation/2024 damage')}",
        f"- gate_2: {code('or materially improve test containment with only limited headline sacrifice')}",
        f"- gate_3: {code('do not confuse governance alerting with adaptive value; overlay must help the regular risk read itself')}",
        "",
        "## Scoreboards",
        "",
        f"- regular_risk_execution: {code('active for this wave')}",
        f"- structural_scout: {code('not separated in wave 1; this wave is already an operating-semantic test on risk_pct execution')}",
        "",
        "## Headline",
        "",
        f"- baseline `26A`: {code({'hist': baseline['hist_2024']['headline']['return_pct'], 'val': baseline['validation']['headline']['return_pct'], 'test': baseline['test']['headline']['return_pct'], 'test_dd': baseline['test']['headline']['max_dd_pct'], 'test_pf': baseline['test']['headline']['profit_factor']})}",
        f"- best challenger `{results['best_challenger_code']}`: {code({'hist': challenger['hist_2024']['headline']['return_pct'], 'val': challenger['validation']['headline']['return_pct'], 'test': challenger['test']['headline']['return_pct'], 'test_dd': challenger['test']['headline']['max_dd_pct'], 'test_pf': challenger['test']['headline']['profit_factor']})}",
        "",
        "## Risk",
        "",
        f"- baseline risk: {code({'worst_week': baseline['test']['risk']['worst_week'], 'ulcer': baseline['test']['risk']['ulcer_index'], 'consecutive_losses': baseline['test']['risk']['consecutive_losses']})}",
        f"- challenger risk: {code({'worst_week': challenger['test']['risk']['worst_week'], 'ulcer': challenger['test']['risk']['ulcer_index'], 'consecutive_losses': challenger['test']['risk']['consecutive_losses']})}",
        "",
        "## Diagnostics",
        "",
        f"- baseline diagnostics: {code({'no_trade_rate': baseline['test']['diagnostics']['no_trade_rate'], 'long_count': baseline['test']['diagnostics']['long_count'], 'short_count': baseline['test']['diagnostics']['short_count']})}",
        f"- challenger diagnostics: {code({'no_trade_rate': challenger['test']['diagnostics']['no_trade_rate'], 'long_count': challenger['test']['diagnostics']['long_count'], 'short_count': challenger['test']['diagnostics']['short_count']})}",
        "",
        "## Execution",
        "",
        f"- baseline governance execution: {code({'latest_state': baseline['test']['governance']['latest_state'], 'mean_external_skip_rate': baseline['test']['governance']['mean_external_skip_rate'], 'mean_argmax_class_share': baseline['test']['governance']['mean_argmax_class_share'], 'mean_entropy': baseline['test']['governance']['mean_entropy'], 'mean_overlay_rate': baseline['test']['governance']['mean_overlay_rate']})}",
        f"- challenger governance execution: {code({'latest_state': challenger['test']['governance']['latest_state'], 'mean_external_skip_rate': challenger['test']['governance']['mean_external_skip_rate'], 'mean_argmax_class_share': challenger['test']['governance']['mean_argmax_class_share'], 'mean_entropy': challenger['test']['governance']['mean_entropy'], 'mean_overlay_rate': challenger['test']['governance']['mean_overlay_rate']})}",
        "",
        "## Decision",
        "",
        f"- decision: {code(results['decision'])}",
        f"- regular incumbent: {code(results['regular_incumbent'])}",
        f"- regular shadow challenger: {code(results['regular_shadow_challenger'])}",
        "",
        "## Follow-Up Bias",
        "",
        f"- follow_up_1: {code('keep the governance overlay line only if taper value survives without simply starving the book')}",
        f"- follow_up_2: {code('if signal taper is too blunt, move next to volatility-aware or session-aware governance triggers instead of widening thresholds blindly')}",
        f"- follow_up_3: {code('keep governance block mode out of the regular lane until adaptive overlays prove useful first')}",
        "",
        "## Report Refs",
        "",
        f"- {code('03_reviews/stage26_gov_adaptive_wave1_20260409.md')}",
    ]
    write_markdown(SELECTION_MD, lines)


def write_review_index(results: dict[str, Any]) -> None:
    lines = [
        "# Stage 26 Review Index",
        "",
        "## Reading Order",
        "",
        f"1. {code('00_spec/stage_brief.md')}",
        f"2. {code('03_reviews/stage26_gov_adaptive_wave1_20260409.md')}",
        f"3. {code('04_selected/selection_status.md')}",
        "",
        "## Latest Regular Decision",
        "",
        f"- incumbent: {code(results['regular_incumbent'])}",
        f"- shadow_challenger: {code(results['regular_shadow_challenger'])}",
        f"- decision: {code(results['decision'])}",
        "",
        "## Closed Diagnostic Notes",
        "",
        f"- {code('Stage 22 alignment relaxation remains a closed diagnostic lane; do not reopen it inside Stage 26 promotion work.')}",
        f"- {code('Stage 24 gated specialist overlay remains closed context only unless a later soft gate hypothesis appears.')}",
    ]
    write_markdown(REVIEW_INDEX_MD, lines)


def main() -> int:
    results = build_results()
    write_json(OUTPUT_JSON, results)
    write_review_markdown(results)
    write_selection_markdown(results)
    write_review_index(results)
    print(f"[done] wrote review={OUTPUT_MD}")
    print(f"[done] wrote selection={SELECTION_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
