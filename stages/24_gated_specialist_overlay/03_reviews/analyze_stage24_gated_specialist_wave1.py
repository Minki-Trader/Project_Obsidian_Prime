#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
from pathlib import Path
from statistics import median
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
    "24A": {
        "folder": "24A_23a_base_gate_ref_0001",
        "label": "regular inherited baseline",
    },
    "24B": {
        "folder": "24B_23a_17csg040_gate_0001",
        "label": "mild short specialist gate",
    },
    "24C": {
        "folder": "24C_23a_17csg045_gate_0001",
        "label": "medium short specialist gate",
    },
    "24D": {
        "folder": "24D_23a_17csg050_gate_0001",
        "label": "aggressive short specialist gate",
    },
}

OUTPUT_JSON = REVIEW_DIR / "stage24_gated_specialist_wave1_20260409.json"
OUTPUT_MD = REVIEW_DIR / "stage24_gated_specialist_wave1_20260409.md"
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


def _safe_float(value: str | None) -> float | None:
    if value is None:
        return None
    value = value.strip()
    if value == "":
        return None
    return float(value)


def load_gate_stats(shadow_log_path: str) -> dict[str, Any]:
    rows = list(csv.DictReader(Path(shadow_log_path).open("r", encoding="utf-8-sig", newline="")))
    active_rows = [row for row in rows if row.get("aux_gate_active", "").lower() == "true"]
    passed_rows = [row for row in active_rows if row.get("aux_gate_passed", "").lower() == "true"]
    rejected_rows = [row for row in active_rows if row.get("aux_gate_passed", "").lower() != "true"]
    reject_reason_counts: dict[str, int] = {}
    aux_short_values: list[float] = []
    for row in active_rows:
        aux_short = _safe_float(row.get("aux_p_short"))
        if aux_short is not None:
            aux_short_values.append(aux_short)
    for row in rejected_rows:
        reason = row.get("aux_gate_reason", "") or row.get("decision_reason", "")
        reject_reason_counts[reason] = reject_reason_counts.get(reason, 0) + 1
    return {
        "active_count": len(active_rows),
        "passed_count": len(passed_rows),
        "rejected_count": len(rejected_rows),
        "pass_rate": (len(passed_rows) / len(active_rows)) if active_rows else None,
        "aux_short_median": median(aux_short_values) if aux_short_values else None,
        "aux_short_p90": sorted(aux_short_values)[int(0.9 * (len(aux_short_values) - 1))] if aux_short_values else None,
        "reject_reason_counts": reject_reason_counts,
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
        "gate": load_gate_stats(summary["csv_log_path"]),
        "attempt_summary_path": summary["_summary_path"],
        "trade_ledger_path": summary["trade_ledger_path"],
        "shadow_log_path": summary["csv_log_path"],
    }


def pick_shadow_challenger(results: dict[str, Any]) -> str:
    candidates = [code_name for code_name in results["runs"] if code_name != "24A"]
    return max(
        candidates,
        key=lambda code_name: (
            results["runs"][code_name]["test"]["headline"]["return_pct"] or float("-inf"),
            -(results["runs"][code_name]["test"]["headline"]["max_dd_pct"] or float("inf")),
        ),
    )


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

    shadow_code = pick_shadow_challenger({"runs": runs})
    return {
        "reviewed_on": "2026-04-09",
        "stage": "24_gated_specialist_overlay",
        "roadmap_anchor": "Claude gated specialist overlay wave",
        "regular_incumbent": "24A_23a_base_gate_ref_0001",
        "regular_shadow_challenger": f"{shadow_code}_{runs[shadow_code]['folder'].split('_', 1)[1]}",
        "regular_shadow_code": shadow_code,
        "decision": "keep_incumbent",
        "runs": runs,
    }


def write_review_markdown(results: dict[str, Any]) -> None:
    baseline = results["runs"]["24A"]
    challenger = results["runs"][results["regular_shadow_code"]]
    baseline_headline = (
        f"hist={baseline['hist_2024']['headline']['return_pct']} / "
        f"val={baseline['validation']['headline']['return_pct']} / "
        f"test={baseline['test']['headline']['return_pct']} / "
        f"test_dd={baseline['test']['headline']['max_dd_pct']} / "
        f"pf={baseline['test']['headline']['profit_factor']}"
    )
    challenger_headline = (
        f"hist={challenger['hist_2024']['headline']['return_pct']} / "
        f"val={challenger['validation']['headline']['return_pct']} / "
        f"test={challenger['test']['headline']['return_pct']} / "
        f"test_dd={challenger['test']['headline']['max_dd_pct']} / "
        f"pf={challenger['test']['headline']['profit_factor']}"
    )
    baseline_risk = (
        f"worst_week={baseline['test']['risk']['worst_week']} / "
        f"ulcer={baseline['test']['risk']['ulcer_index']} / "
        f"consecutive_losses={baseline['test']['risk']['consecutive_losses']}"
    )
    challenger_risk = (
        f"worst_week={challenger['test']['risk']['worst_week']} / "
        f"ulcer={challenger['test']['risk']['ulcer_index']} / "
        f"consecutive_losses={challenger['test']['risk']['consecutive_losses']}"
    )
    baseline_execution = (
        f"skip_rate={baseline['test']['execution']['skip_rate']} / "
        f"external_mismatch_count={baseline['test']['execution']['external_mismatch_count']}"
    )
    challenger_execution = (
        f"skip_rate={challenger['test']['execution']['skip_rate']} / "
        f"external_mismatch_count={challenger['test']['execution']['external_mismatch_count']}"
    )

    lines = [
        "# Stage 24 Gated Specialist Overlay Wave 1",
        "",
        f"- reviewed_on: {code(results['reviewed_on'])}",
        f"- purpose: {code('test 17C short specialist as a short-entry gate on the 23A regular baseline')}",
        f"- operating_seed: {code('23A_22q_base_stateexit_ref_0001')}",
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
                "test_gate_rejects",
                "test_gate_pass_rate",
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
                    code(run["test"]["gate"]["rejected_count"]),
                    code(run["test"]["gate"]["pass_rate"]),
                    code(run["label"]),
                ]
                for code_name, run in results["runs"].items()
            ],
        ),
        "",
        "## Headline",
        "",
        f"- incumbent `24A`: {code(baseline_headline)}",
        f"- best challenger `{results['regular_shadow_code']}`: {code(challenger_headline)}",
        "",
        "## Risk",
        "",
        f"- baseline OOS risk read: {code(baseline_risk)}",
        f"- challenger OOS risk read: {code(challenger_risk)}",
        "",
        "## Diagnostics",
        "",
        f"- baseline test short_count: {code(baseline['test']['diagnostics']['short_count'])}",
        f"- challenger test short_count: {code(challenger['test']['diagnostics']['short_count'])}",
        f"- challenger gate stats: {code(challenger['test']['gate'])}",
        f"- this wave should be read as a `short suppression` experiment, so short_count compression and gate reject counts matter as much as headline return.",
        "",
        "## Execution",
        "",
        f"- execution quality should remain unchanged if the gate is behaving as designed: {code('same data path, same feature contract, same exact-alignment runtime; only short entry permission changes')}",
        f"- baseline test execution: {code(baseline_execution)}",
        f"- challenger test execution: {code(challenger_execution)}",
        "",
        "## Decision",
        "",
        f"- regular incumbent: {code(results['regular_incumbent'])}",
        f"- regular shadow challenger: {code(results['runs'][results['regular_shadow_code']]['folder'])}",
        f"- decision: {code(results['decision'])}",
        f"- why: {code('wave 1 is meant to measure whether short specialist gating is alive at all; keep the incumbent unless a challenger improves the regular OOS read without obvious non-OOS damage')}",
    ]
    write_markdown(OUTPUT_MD, lines)


def write_selection_markdown(results: dict[str, Any]) -> None:
    shadow_code = results["regular_shadow_code"]
    shadow_run = results["runs"][shadow_code]
    lines = [
        "# Stage 24 Selection Status",
        "",
        f"- reviewed_on: {code(results['reviewed_on'])}",
        f"- stage: {code(results['stage'])}",
        f"- roadmap_anchor: {code(results['roadmap_anchor'])}",
        f"- inherited_regular_reference: {code('23A_22q_base_stateexit_ref_0001')}",
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
                "test_short_count",
                "test_gate_rejects",
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
                    code(run["test"]["gate"]["rejected_count"]),
                    code(run["label"]),
                ]
                for code_name, run in results["runs"].items()
            ],
        ),
        "",
        "## Diagnostics",
        "",
        f"- shadow gate stats `{shadow_code}`: {code(shadow_run['test']['gate'])}",
        "",
        "## Decision",
        "",
        f"- decision: {code(results['decision'])}",
        f"- regular incumbent: {code(results['regular_incumbent'])}",
        f"- regular shadow challenger: {code(shadow_run['folder'])}",
        "",
        "## Follow-Up Bias",
        "",
        f"- keep the current regular incumbent unless the gate line shows a cleaner OOS plus non-OOS balance",
        f"- use gate reject counts and short_count compression to decide whether the specialist is adding signal or just starving the book",
        "",
        "## Report Refs",
        "",
        f"- {code('03_reviews/stage24_gated_specialist_wave1_20260409.md')}",
    ]
    write_markdown(SELECTION_MD, lines)


def write_review_index(results: dict[str, Any]) -> None:
    lines = [
        "# Stage 24 Review Index",
        "",
        f"- updated_on: {code(results['reviewed_on'])}",
        f"- regular_decision: {code('wave 1 gated specialist overlay review complete')}",
        f"- roadmap_anchor: {code(results['roadmap_anchor'])}",
        "",
        "## Read Order",
        "",
        "1. `../00_spec/stage_brief.md`",
        "2. `stage24_gated_specialist_wave1_20260409.md`",
        "3. `../04_selected/selection_status.md`",
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
