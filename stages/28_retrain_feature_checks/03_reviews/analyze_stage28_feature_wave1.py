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
    "28A": {"folder": "28A_18e_full54_ph20_0001", "label": "full 17E feature reference under 18E PH20 overlay"},
    "28B": {"folder": "28B_18e_persist48_ph20_0001", "label": "persistence-only compact fork under 18E PH20 overlay"},
    "28C": {"folder": "28C_18e_sessionless50_ph20_0001", "label": "sessionless compact fork under 18E PH20 overlay"},
    "28D": {
        "folder": "28D_18e_extless44_ph20_0001",
        "label": "external-breadthless compact fork under 18E PH20 overlay",
    },
}

OUTPUT_JSON = REVIEW_DIR / "stage28_feature_wave1_20260409.json"
OUTPUT_MD = REVIEW_DIR / "stage28_feature_wave1_20260409.md"
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
            "mean_external_skip_rate": None,
            "mean_argmax_class_share": None,
            "mean_entropy": None,
            "mean_overlay_rate": None,
            "latest_state": None,
            "latest_reason": None,
        }
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        return {
            "row_count": 0,
            "mean_external_skip_rate": None,
            "mean_argmax_class_share": None,
            "mean_entropy": None,
            "mean_overlay_rate": None,
            "latest_state": None,
            "latest_reason": None,
        }

    def avg(values: list[float]) -> float | None:
        if not values:
            return None
        return sum(values) / len(values)

    ext = [value for value in (parse_float(row.get("external_skip_rate")) for row in rows) if value is not None]
    argmax = [value for value in (parse_float(row.get("max_argmax_class_share")) for row in rows) if value is not None]
    entropy = [value for value in (parse_float(row.get("avg_signal_entropy_norm")) for row in rows) if value is not None]
    overlay = [value for value in (parse_float(row.get("risk_overlay_rate")) for row in rows) if value is not None]
    latest = rows[-1]
    return {
        "row_count": len(rows),
        "mean_external_skip_rate": avg(ext),
        "mean_argmax_class_share": avg(argmax),
        "mean_entropy": avg(entropy),
        "mean_overlay_rate": avg(overlay),
        "latest_state": (latest.get("governance_state") or "").strip() or None,
        "latest_reason": (latest.get("governance_reason") or "").strip() or None,
    }


def simplify_split(summary: dict[str, Any]) -> dict[str, Any]:
    headline = summary["financial_metrics"]["headline"]
    risk = summary["financial_metrics"]["risk"]
    diagnostics = summary["financial_metrics"]["diagnostics"]
    metrics = summary["metrics"]
    governance = load_governance_stats(summary["governance_log_path"])
    return {
        "headline": headline,
        "risk": risk,
        "diagnostics": diagnostics,
        "execution": {
            "skip_rate": metrics["skip_row_count"] / metrics["row_count"] if metrics["row_count"] else None,
            "external_mismatch_count": metrics.get("external_mismatch_count"),
            "contract_skip_count": metrics.get("contract_skip_count"),
        },
        "governance": governance,
        "attempt_summary_path": summary["_summary_path"],
        "trade_ledger_path": summary["trade_ledger_path"],
        "shadow_log_path": summary["csv_log_path"],
        "governance_log_path": summary["governance_log_path"],
    }


def load_offline_metrics(run_dir: Path) -> dict[str, Any]:
    return json.loads((run_dir / "offline_metrics.json").read_text(encoding="utf-8"))


def pick_best_compact(results: dict[str, Any]) -> str:
    candidates = [code_name for code_name in results["runs"] if code_name != "28A"]
    return max(
        candidates,
        key=lambda code_name: (
            results["runs"][code_name]["test"]["headline"]["return_pct"] or float("-inf"),
            results["runs"][code_name]["test"]["headline"]["profit_factor"] or float("-inf"),
            -(results["runs"][code_name]["test"]["headline"]["max_dd_pct"] or float("inf")),
        ),
    )


def decide_lineage_status(results: dict[str, Any], best_compact: str) -> str:
    baseline = results["runs"]["28A"]
    compact = results["runs"][best_compact]
    if (
        (compact["test"]["headline"]["return_pct"] or float("-inf"))
        >= (baseline["test"]["headline"]["return_pct"] or float("-inf")) + 2.0
        and (compact["validation"]["headline"]["return_pct"] or float("-inf"))
        >= (baseline["validation"]["headline"]["return_pct"] or float("-inf")) - 10.0
        and (compact["hist_2024"]["headline"]["return_pct"] or float("-inf"))
        >= (baseline["hist_2024"]["headline"]["return_pct"] or float("-inf")) - 10.0
    ):
        return "reopen_lineage_followup"
    return "close_as_diagnostic"


def build_results() -> dict[str, Any]:
    runs: dict[str, Any] = {}
    for code_name, meta in RUNS.items():
        run_dir = ACTIVE_RUNS_DIR / meta["folder"]
        runs[code_name] = {
            "folder": meta["folder"],
            "label": meta["label"],
            "offline": load_offline_metrics(run_dir),
            "hist_2024": simplify_split(load_attempt_summary(run_dir, "hist_2024")),
            "validation": simplify_split(load_attempt_summary(run_dir, "validation")),
            "test": simplify_split(load_attempt_summary(run_dir, "test")),
        }

    base_results = {"runs": runs}
    best_compact_code = pick_best_compact(base_results)
    decision = decide_lineage_status(base_results, best_compact_code)
    return {
        "reviewed_on": "2026-04-09",
        "stage": "28_retrain_feature_checks",
        "wave": "feature_simplification_wave1",
        "inherited_lineage_reference": "18E_2501_17e_ph20_0001",
        "current_regular_reference_unchanged": "27A_26a_volref_0001",
        "best_compact_code": best_compact_code,
        "decision": decision,
        "runs": runs,
    }


def write_review_markdown(results: dict[str, Any]) -> None:
    baseline = results["runs"]["28A"]
    best_compact = results["runs"][results["best_compact_code"]]
    lines = [
        "# Stage 28 Feature Simplification Wave 1",
        "",
        f"- reviewed_on: {code(results['reviewed_on'])}",
        f"- purpose: {code('revisit Stage 16-style feature simplification on the stronger 17E/18E lineage without reopening calendar retraining yet')}",
        f"- lineage_reference: {code(results['inherited_lineage_reference'])}",
        f"- current_regular_reference_unchanged: {code(results['current_regular_reference_unchanged'])}",
        "",
        "## Scoreboard",
        "",
        *render_markdown_table(
            [
                "run",
                "features",
                "offline_valid_f1",
                "hist_return",
                "val_return",
                "test_return",
                "test_dd",
                "test_pf",
                "mean_ext_skip",
                "mean_entropy",
                "read",
            ],
            [
                [
                    code(code_name),
                    code(len(run["offline"]["feature_names"])),
                    code(run["offline"]["split_metrics"]["validation"]["macro_f1"], digits=4),
                    code(run["hist_2024"]["headline"]["return_pct"]),
                    code(run["validation"]["headline"]["return_pct"]),
                    code(run["test"]["headline"]["return_pct"]),
                    code(run["test"]["headline"]["max_dd_pct"]),
                    code(run["test"]["headline"]["profit_factor"], digits=4),
                    code(run["test"]["governance"]["mean_external_skip_rate"], digits=4),
                    code(run["test"]["governance"]["mean_entropy"], digits=4),
                    code(run["label"]),
                ]
                for code_name, run in results["runs"].items()
            ],
        ),
        "",
        "## Headline",
        "",
        f"- rebuilt full reference `28A`: {code({'hist': baseline['hist_2024']['headline']['return_pct'], 'val': baseline['validation']['headline']['return_pct'], 'test': baseline['test']['headline']['return_pct'], 'test_dd': baseline['test']['headline']['max_dd_pct'], 'test_pf': baseline['test']['headline']['profit_factor']})}",
        f"- best compact `{results['best_compact_code']}`: {code({'hist': best_compact['hist_2024']['headline']['return_pct'], 'val': best_compact['validation']['headline']['return_pct'], 'test': best_compact['test']['headline']['return_pct'], 'test_dd': best_compact['test']['headline']['max_dd_pct'], 'test_pf': best_compact['test']['headline']['profit_factor']})}",
        "",
        "## Risk",
        "",
        f"- rebuilt full OOS risk: {code({'ulcer': baseline['test']['risk']['ulcer_index'], 'worst_week': baseline['test']['risk']['worst_week'], 'consecutive_losses': baseline['test']['risk']['consecutive_losses']})}",
        f"- best compact OOS risk: {code({'ulcer': best_compact['test']['risk']['ulcer_index'], 'worst_week': best_compact['test']['risk']['worst_week'], 'consecutive_losses': best_compact['test']['risk']['consecutive_losses']})}",
        "",
        "## Diagnostics",
        "",
        f"- rebuilt full offline metrics: {code(baseline['offline']['split_metrics'])}",
        f"- best compact offline metrics: {code(best_compact['offline']['split_metrics'])}",
        f"- rebuilt full OOS diagnostics: {code({'long_count': baseline['test']['diagnostics']['long_count'], 'short_count': baseline['test']['diagnostics']['short_count'], 'avg_hold': baseline['test']['diagnostics']['avg_hold'], 'no_trade_rate': baseline['test']['diagnostics']['no_trade_rate']})}",
        f"- best compact OOS diagnostics: {code({'long_count': best_compact['test']['diagnostics']['long_count'], 'short_count': best_compact['test']['diagnostics']['short_count'], 'avg_hold': best_compact['test']['diagnostics']['avg_hold'], 'no_trade_rate': best_compact['test']['diagnostics']['no_trade_rate']})}",
        "",
        "## Execution",
        "",
        f"- rebuilt full governance read: {code(baseline['test']['governance'])}",
        f"- best compact governance read: {code(best_compact['test']['governance'])}",
        "",
        "## Decision",
        "",
        f"- lineage status: {code(results['decision'])}",
        "- this wave checks whether compact subsets help the 18E lineage internally; it does not replace the current `27A` operating reference by itself",
        "",
    ]
    write_markdown(OUTPUT_MD, lines)


def write_review_index(results: dict[str, Any]) -> None:
    lines = [
        "# Review Index",
        "",
        f"- latest_review: {code(OUTPUT_MD.name)}",
        f"- best_compact_code: {code(results['best_compact_code'])}",
        f"- lineage_status: {code(results['decision'])}",
        f"- current_regular_reference_unchanged: {code(results['current_regular_reference_unchanged'])}",
        "",
        "## Wave Reviews",
        "",
        f"- `wave1_feature_simplification`: `{OUTPUT_MD.name}`",
        "",
    ]
    write_markdown(REVIEW_INDEX_MD, lines)


def write_selection(results: dict[str, Any]) -> None:
    best_compact = results["runs"][results["best_compact_code"]]["folder"]
    lines = [
        "# Selection Status",
        "",
        f"- stage: {code(results['stage'])}",
        f"- wave: {code(results['wave'])}",
        f"- status: {code('completed')}",
        f"- lineage_reference: {code(results['inherited_lineage_reference'])}",
        f"- rebuilt_full_reference: {code(results['runs']['28A']['folder'])}",
        f"- best_compact_arm: {code(best_compact)}",
        f"- decision: {code(results['decision'])}",
        f"- operating_reference_unchanged: {code(results['current_regular_reference_unchanged'])}",
        "- interpretation: compact feature subsets were evaluated only as an internal 18E-lineage check; use this stage to decide whether the lineage deserves follow-up work, not to override the live regular lane directly",
        "",
    ]
    write_markdown(SELECTION_MD, lines)


def main() -> int:
    results = build_results()
    write_json(OUTPUT_JSON, results)
    write_review_markdown(results)
    write_review_index(results)
    write_selection(results)
    print(f"[done] review={OUTPUT_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
