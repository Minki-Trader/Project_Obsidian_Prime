from __future__ import annotations

import csv
import json
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from foundation.pipelines.stage_reporting import code, render_markdown_table, write_json, write_markdown


STAGE_DIR = PROJECT_ROOT / "stages" / "22_point_exit_management"
REVIEW_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"
COMMON_RUNTIME_DIR = Path.home() / "AppData" / "Roaming" / "MetaQuotes" / "Terminal" / "Common" / "Files" / "Project_Obsidian_Prime" / "runtime"

RUNS = {
    "22Q": {
        "label": "risk_baseline_time_exit",
        "folder": "22Q_05dp_base_risk2_dirsplit_postcash_0001",
        "runtime_id": "exp_22q_05dp_base_risk2_dirsplit_postcash_v1",
        "hist_attempt": "att_0003",
        "validation_attempt": "att_0001",
        "test_attempt": "att_0002",
    },
    "22R": {
        "label": "risk_psl45_qtr_h3",
        "folder": "22R_05dp_psl45_qtr_h3_risk2_0001",
        "runtime_id": "exp_22r_05dp_psl45_qtr_h3_risk2_v1",
        "hist_attempt": "att_0003",
        "validation_attempt": "att_0001",
        "test_attempt": "att_0002",
    },
    "22S": {
        "label": "risk_psl45_p10_h3",
        "folder": "22S_05dp_psl45_p10_h3_risk2_0001",
        "runtime_id": "exp_22s_05dp_psl45_p10_h3_risk2_v1",
        "hist_attempt": "att_0003",
        "validation_attempt": "att_0001",
        "test_attempt": "att_0002",
    },
    "22T": {
        "label": "risk_psl45_p30_h3",
        "folder": "22T_05dp_psl45_p30_h3_risk2_0001",
        "runtime_id": "exp_22t_05dp_psl45_p30_h3_risk2_v1",
        "hist_attempt": "att_0003",
        "validation_attempt": "att_0001",
        "test_attempt": "att_0002",
    },
}

STRUCTURAL_SCOUT_PATH = REVIEW_DIR / "stage22_partial_sl_refine_wave2_20260408.json"
OUTPUT_JSON = REVIEW_DIR / "stage22_risk_overlay_wave1_20260409.json"
OUTPUT_MD = REVIEW_DIR / "stage22_risk_overlay_wave1_20260409.md"
SELECTION_MD = SELECTED_DIR / "selection_status.md"
REVIEW_INDEX_MD = REVIEW_DIR / "review_index.md"


def rounded(value: Any, digits: int = 3) -> Any:
    if value is None:
        return None
    if isinstance(value, float):
        return round(value, digits)
    return value


def display(value: Any) -> str:
    return "n/a" if value is None else str(value)


def load_summary(run_code: str, attempt_id: str) -> dict[str, Any]:
    path = STAGE_DIR / "02_runs" / "active" / RUNS[run_code]["folder"] / "mt5_attempts" / attempt_id / "tester_attempt_summary.json"
    return json.loads(path.read_text(encoding="utf-8"))


def headline(summary: dict[str, Any]) -> dict[str, Any]:
    h = summary["financial_metrics"]["headline"]
    r = summary["financial_metrics"]["risk"]
    return {
        "return_pct": rounded(h["return_pct"]),
        "profit_factor": rounded(h["profit_factor"], 4),
        "trade_count": h["trade_count"],
        "max_dd_pct": rounded(h["max_dd_pct"]),
        "worst_week": rounded(r.get("worst_week")),
        "ulcer_index": rounded(r.get("ulcer_index")),
    }


def risk_layer(summary: dict[str, Any]) -> dict[str, Any]:
    risk = summary["financial_metrics"]["risk"]
    return {
        "ulcer_index": rounded(risk.get("ulcer_index")),
        "worst_week": rounded(risk.get("worst_week")),
        "consecutive_losses": risk.get("consecutive_losses"),
        "min_free_margin": rounded(risk.get("min_free_margin"), 2),
        "time_under_water": rounded(risk.get("time_under_water"), 1),
    }


def diagnostics_layer(summary: dict[str, Any]) -> dict[str, Any]:
    diagnostics = summary["financial_metrics"]["diagnostics"]
    return {
        "no_trade_rate": rounded(diagnostics.get("no_trade_rate"), 4),
        "long_count": diagnostics.get("long_count"),
        "short_count": diagnostics.get("short_count"),
        "long_expectancy": rounded(diagnostics.get("long_expectancy")),
        "short_expectancy": rounded(diagnostics.get("short_expectancy")),
        "avg_hold": rounded(diagnostics.get("avg_hold"), 2),
    }


def execution_layer(summary: dict[str, Any]) -> dict[str, Any]:
    metrics = summary.get("metrics", {})
    execution = summary["financial_metrics"]["execution"]
    return {
        "skip_rate": rounded(
            (metrics.get("skip_row_count", 0) / metrics.get("row_count")) if metrics.get("row_count") else None,
            4,
        ),
        "external_mismatch_count": metrics.get("external_mismatch_count"),
        "fill_rate": rounded(execution.get("fill_rate"), 4),
        "data_readiness_failures": metrics.get("data_readiness_failures"),
        "broker_constraint_events": execution.get("broker_constraint_events"),
        "contract_skip_count": metrics.get("contract_skip_count", execution.get("contract_skip_count")),
    }


def load_position_rows(csv_path: Path) -> dict[str, list[dict[str, str]]]:
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    with csv_path.open("r", encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            grouped[row["position_identifier"]].append(row)
    return grouped


def position_net_map(grouped_rows: dict[str, list[dict[str, str]]]) -> dict[str, float]:
    output: dict[str, float] = {}
    for rows in grouped_rows.values():
        rows.sort(key=lambda row: (row["exit_time_server"], row["event_timestamp_gmt"], row["close_reason"]))
        first = rows[0]
        key = f"{first['entry_bar_time_server']}|{first['direction']}"
        output[key] = round(sum(float((row["net_profit"] or "0").strip() or 0.0) for row in rows), 6)
    return output


def risk_context_snapshot(grouped_rows: dict[str, list[dict[str, str]]]) -> dict[str, Any]:
    context_counter: Counter[str] = Counter()
    multiplier_counter: Counter[str] = Counter()
    close_reason_counter: Counter[str] = Counter()
    partial_volume_counter: Counter[str] = Counter()
    initial_risks: list[float] = []

    for rows in grouped_rows.values():
        rows.sort(key=lambda row: (row["exit_time_server"], row["event_timestamp_gmt"], row["close_reason"]))
        first = rows[0]
        context_counter[first["risk_context"]] += 1
        multiplier_counter[first["risk_pct_multiplier_applied"]] += 1
        if first["initial_risk_amount"]:
            initial_risks.append(float(first["initial_risk_amount"]))
        for row in rows:
            close_reason_counter[row["close_reason"]] += 1
            if row["close_reason"] == "PARTIAL_STOP_LOSS":
                partial_volume_counter[row["volume"]] += 1

    return {
        "position_count": len(grouped_rows),
        "avg_initial_risk_amount": rounded(sum(initial_risks) / len(initial_risks), 3) if initial_risks else None,
        "risk_context_counts": dict(context_counter),
        "risk_multiplier_counts": dict(multiplier_counter),
        "close_reason_counts": dict(close_reason_counter),
        "partial_close_volumes": dict(partial_volume_counter),
    }


def compare_positions(base_map: dict[str, float], variant_map: dict[str, float]) -> dict[str, Any]:
    shared_keys = sorted(set(base_map) & set(variant_map))
    winner_clips: list[float] = []
    loser_mitigations: list[float] = []
    shared_delta = 0.0
    for key in shared_keys:
        base_value = base_map[key]
        variant_value = variant_map[key]
        shared_delta += variant_value - base_value
        if base_value > 0.0:
            winner_clips.append(max(0.0, (base_value - variant_value) / base_value))
        elif base_value < 0.0:
            loser_mitigations.append(max(0.0, (variant_value - base_value) / abs(base_value)))

    return {
        "shared_position_count": len(shared_keys),
        "base_only_positions": len(set(base_map) - set(variant_map)),
        "variant_only_positions": len(set(variant_map) - set(base_map)),
        "shared_delta_vs_baseline": rounded(shared_delta),
        "mean_winner_clip_rate": rounded(sum(winner_clips) / len(winner_clips), 4) if winner_clips else 0.0,
        "mean_loser_mitigation_rate": rounded(sum(loser_mitigations) / len(loser_mitigations), 4) if loser_mitigations else 0.0,
    }


def load_structural_scout() -> dict[str, Any]:
    payload = json.loads(STRUCTURAL_SCOUT_PATH.read_text(encoding="utf-8"))
    scout_runs: dict[str, Any] = {}
    for code_name in ["22A", "22O", "22P"]:
        run_payload = payload["runs"][code_name]
        scout_runs[code_name] = {
            "label": run_payload["label"],
            "validation": run_payload["validation"],
            "test": run_payload["test"],
            "test_position_comparison": run_payload.get(
                "test_position_comparison",
                {
                    "shared_delta_vs_22A": 0.0,
                    "mean_winner_clip_rate": 0.0,
                    "mean_loser_mitigation_rate": 0.0,
                },
            ),
            "test_partial_events": run_payload.get("test_partial_events", {}),
        }
    return scout_runs


def build_review_markdown(reviewed_on: str, results: dict[str, Any], structural_scout: dict[str, Any]) -> list[str]:
    lines = [
        "# Stage 22 Risk Overlay Wave 1",
        "",
        f"- reviewed_on: `{reviewed_on}`",
        "- purpose: `return the Stage 22 family to regular risk-based execution instead of fixed 0.1 lot comparison`",
        "- regular_risk_overlay: `risk_pct=2.0, balance base, ATR14 broker-native SL, direction_split(long=1.4, short=2.0), monday=0.75, ny_postcash=0.70, hold_cap=3`",
        "- structural_scout_reference: `fixed_lot=0.1 scout board is kept as context only; promotion comes from the regular scoreboard`",
        "",
        "## Structural Scout Scoreboard",
        "",
    ]

    structural_rows = [
        [
            code("22A"),
            code(structural_scout["22A"]["validation"]["return_pct"]),
            code(structural_scout["22A"]["validation"]["max_dd_pct"]),
            code(structural_scout["22A"]["test"]["return_pct"]),
            code(structural_scout["22A"]["test"]["max_dd_pct"]),
            code(0.0),
            code(0.0, digits=4),
            code(0.0, digits=4),
            code("scout incumbent"),
        ],
        [
            code("22O"),
            code(structural_scout["22O"]["validation"]["return_pct"]),
            code(structural_scout["22O"]["validation"]["max_dd_pct"]),
            code(structural_scout["22O"]["test"]["return_pct"]),
            code(structural_scout["22O"]["test"]["max_dd_pct"]),
            code(structural_scout["22O"]["test_position_comparison"]["shared_delta_vs_22A"]),
            code(structural_scout["22O"]["test_position_comparison"]["mean_winner_clip_rate"], digits=4),
            code(structural_scout["22O"]["test_position_comparison"]["mean_loser_mitigation_rate"], digits=4),
            code("best scout containment challenger"),
        ],
        [
            code("22P"),
            code(structural_scout["22P"]["validation"]["return_pct"]),
            code(structural_scout["22P"]["validation"]["max_dd_pct"]),
            code(structural_scout["22P"]["test"]["return_pct"]),
            code(structural_scout["22P"]["test"]["max_dd_pct"]),
            code(structural_scout["22P"]["test_position_comparison"]["shared_delta_vs_22A"]),
            code(structural_scout["22P"]["test_position_comparison"]["mean_winner_clip_rate"], digits=4),
            code(structural_scout["22P"]["test_position_comparison"]["mean_loser_mitigation_rate"], digits=4),
            code("stronger containment, more clipping"),
        ],
    ]
    lines.extend(
        render_markdown_table(
            [
                "run",
                "val_return",
                "val_dd",
                "test_return",
                "test_dd",
                "shared_delta_vs_22A",
                "winner_clip",
                "loser_mitigation",
                "read",
            ],
            structural_rows,
        )
    )

    lines.extend(
        [
            "",
            "## Regular Risk Execution Scoreboard",
            "",
        ]
    )
    regular_rows: list[list[str]] = []
    read_map = {
        "22Q": "regular incumbent",
        "22R": "best regular containment challenger",
        "22S": "too gentle",
        "22T": "stronger containment, more non-OOS drag",
    }
    for code_name in ["22Q", "22R", "22S", "22T"]:
        run = results["runs"][code_name]
        comparison = run.get("test_position_comparison", {})
        regular_rows.append(
            [
                code(code_name),
                code(run["hist_2024"]["return_pct"]),
                code(run["hist_2024"]["max_dd_pct"]),
                code(run["validation"]["return_pct"]),
                code(run["validation"]["max_dd_pct"]),
                code(run["test"]["return_pct"]),
                code(run["test"]["max_dd_pct"]),
                code(run["test"]["profit_factor"], digits=4),
                code(comparison.get("shared_delta_vs_baseline", 0.0)),
                code(comparison.get("mean_winner_clip_rate", 0.0), digits=4),
                code(comparison.get("mean_loser_mitigation_rate", 0.0), digits=4),
                code(read_map[code_name]),
            ]
        )
    lines.extend(
        render_markdown_table(
            [
                "run",
                "hist_return",
                "hist_dd",
                "val_return",
                "val_dd",
                "test_return",
                "test_dd",
                "test_pf",
                "shared_delta_vs_22Q",
                "winner_clip",
                "loser_mitigation",
                "read",
            ],
            regular_rows,
        )
    )

    incumbent = results["runs"]["22Q"]
    challenger = results["runs"]["22R"]
    lines.extend(
        [
            "",
            "## Current Regular Read",
            "",
            f"- incumbent: `22Q_05dp_base_risk2_dirsplit_postcash_0001`",
            f"- shadow challenger: `22R_05dp_psl45_qtr_h3_risk2_0001`",
            f"- why: `22Q` keeps the best multi-window stability, while `22R` is the cleanest containment challenger with a small positive shared-position delta and limited additional clipping.",
            "",
            "## Current Incumbent Snapshot",
            "",
            f"- headline_test: `return_pct={incumbent['test']['return_pct']}`, `pf={incumbent['test']['profit_factor']}`, `max_dd_pct={incumbent['test']['max_dd_pct']}`, `trades={incumbent['test']['trade_count']}`",
            f"- risk_test: `ulcer_index={incumbent['test_risk']['ulcer_index']}`, `worst_week={incumbent['test_risk']['worst_week']}`, `consecutive_losses={incumbent['test_risk']['consecutive_losses']}`",
            f"- diagnostics_test: `no_trade_rate={incumbent['test_diagnostics']['no_trade_rate']}`, `long_short={incumbent['test_diagnostics']['long_count']}/{incumbent['test_diagnostics']['short_count']}`, `avg_hold={incumbent['test_diagnostics']['avg_hold']}`",
            f"- execution_test: `skip_rate={display(incumbent['test_execution']['skip_rate'])}`, `external_mismatch_count={display(incumbent['test_execution']['external_mismatch_count'])}`, `fill_rate={display(incumbent['test_execution']['fill_rate'])}`",
            "",
            "## Shadow Challenger Snapshot",
            "",
            f"- headline_test: `return_pct={challenger['test']['return_pct']}`, `pf={challenger['test']['profit_factor']}`, `max_dd_pct={challenger['test']['max_dd_pct']}`, `trades={challenger['test']['trade_count']}`",
            f"- risk_test: `ulcer_index={challenger['test_risk']['ulcer_index']}`, `worst_week={challenger['test_risk']['worst_week']}`, `consecutive_losses={challenger['test_risk']['consecutive_losses']}`",
            f"- diagnostics_test: `no_trade_rate={challenger['test_diagnostics']['no_trade_rate']}`, `long_short={challenger['test_diagnostics']['long_count']}/{challenger['test_diagnostics']['short_count']}`, `avg_hold={challenger['test_diagnostics']['avg_hold']}`",
            f"- execution_test: `skip_rate={display(challenger['test_execution']['skip_rate'])}`, `external_mismatch_count={display(challenger['test_execution']['external_mismatch_count'])}`, `fill_rate={display(challenger['test_execution']['fill_rate'])}`",
            f"- position_read: `shared_delta_vs_22Q={challenger['test_position_comparison']['shared_delta_vs_baseline']}`, `winner_clip={challenger['test_position_comparison']['mean_winner_clip_rate']}`, `loser_mitigation={challenger['test_position_comparison']['mean_loser_mitigation_rate']}`",
            "",
            "## Interpretation",
            "",
            "- `22Q` established the proper regular baseline: once Stage 22 is put back on risk-based execution, the headline profile changes materially from the earlier fixed-lot probe. That fixed-lot read should be treated as structural scouting, not as the final operating verdict.",
            "- `22R` and `22T` were the only challengers that improved the risk-sized OOS slice at all. Both preserved the same test position universe as baseline and produced a small positive shared-position delta versus `22Q`.",
            "- `22S` was too gentle. Its smaller partials reduced winner clipping the most, but the loser relief was not strong enough and the OOS result fell behind baseline.",
            "- `22T` gave the best OOS drawdown and almost the same OOS return uplift as `22R`, but it paid a bit more validation and historical drag. `22R` was the cleaner compromise across the three windows.",
            "- Promotion is still too early. `22Q` keeps the best multi-window stability overall, while `22R` is now the best risk-sized containment challenger worth carrying forward.",
        ]
    )
    return lines


def build_selection_markdown(reviewed_on: str, results: dict[str, Any], structural_scout: dict[str, Any]) -> list[str]:
    incumbent = results["runs"]["22Q"]
    challenger = results["runs"]["22R"]
    lines = [
        "# Stage 22 Selection Status",
        "",
        f"- reviewed_on: `{reviewed_on}`",
        "- structural_scout_mode: `fixed_lot=0.1, point-exit behavior read only`",
        "- regular_experiment_mode: `risk_pct=2.0 with direction-split ATR broker-native stops and monday/postcash overlay`",
        "- closed_diagnostic_branch: `external_mismatch curiosity ablation reviewed; not promoted into regular experiment line`",
        "",
        "## Current Read",
        "",
        "- structural scout incumbent: `22A_05dp_base_hold5_0001`",
        "- structural scout containment challenger: `22O_05dp_psl45_p10_h3_0001`",
        "- regular incumbent: `22Q_05dp_base_risk2_dirsplit_postcash_0001`",
        "- regular shadow challenger: `22R_05dp_psl45_qtr_h3_risk2_0001`",
        "- keep_or_replace: `keep_incumbent`",
        "",
        "## Promotion Gates",
        "",
        "- Do not promote from the structural scout board alone.",
        "- A regular challenger must improve the OOS slice without paying disproportionate historical and validation drag.",
        "- Shared-position delta, winner clipping, and loser mitigation must all stay directionally healthy; raw OOS return alone is not enough.",
        "- Closed diagnostic branches such as mismatch relaxation stay outside the regular promotion path unless a new contract hypothesis appears.",
        "",
        "## Scoreboards",
        "",
        "### Structural Scout",
        "",
    ]
    lines.extend(
        render_markdown_table(
            [
                "run",
                "val_return",
                "val_dd",
                "test_return",
                "test_dd",
                "shared_delta_vs_22A",
                "winner_clip",
                "loser_mitigation",
                "read",
            ],
            [
                [
                    code("22A"),
                    code(structural_scout["22A"]["validation"]["return_pct"]),
                    code(structural_scout["22A"]["validation"]["max_dd_pct"]),
                    code(structural_scout["22A"]["test"]["return_pct"]),
                    code(structural_scout["22A"]["test"]["max_dd_pct"]),
                    code(0.0),
                    code(0.0, digits=4),
                    code(0.0, digits=4),
                    code("scout incumbent"),
                ],
                [
                    code("22O"),
                    code(structural_scout["22O"]["validation"]["return_pct"]),
                    code(structural_scout["22O"]["validation"]["max_dd_pct"]),
                    code(structural_scout["22O"]["test"]["return_pct"]),
                    code(structural_scout["22O"]["test"]["max_dd_pct"]),
                    code(structural_scout["22O"]["test_position_comparison"]["shared_delta_vs_22A"]),
                    code(structural_scout["22O"]["test_position_comparison"]["mean_winner_clip_rate"], digits=4),
                    code(structural_scout["22O"]["test_position_comparison"]["mean_loser_mitigation_rate"], digits=4),
                    code("best scout containment challenger"),
                ],
                [
                    code("22P"),
                    code(structural_scout["22P"]["validation"]["return_pct"]),
                    code(structural_scout["22P"]["validation"]["max_dd_pct"]),
                    code(structural_scout["22P"]["test"]["return_pct"]),
                    code(structural_scout["22P"]["test"]["max_dd_pct"]),
                    code(structural_scout["22P"]["test_position_comparison"]["shared_delta_vs_22A"]),
                    code(structural_scout["22P"]["test_position_comparison"]["mean_winner_clip_rate"], digits=4),
                    code(structural_scout["22P"]["test_position_comparison"]["mean_loser_mitigation_rate"], digits=4),
                    code("more containment, more clipping"),
                ],
            ],
        )
    )
    lines.extend(
        [
            "",
            "### Regular Risk Execution",
            "",
        ]
    )
    regular_rows = []
    for code_name in ["22Q", "22R", "22S", "22T"]:
        run = results["runs"][code_name]
        comparison = run.get("test_position_comparison", {})
        read_note = {
            "22Q": "regular incumbent",
            "22R": "shadow challenger",
            "22S": "too gentle",
            "22T": "more drag than 22R",
        }[code_name]
        regular_rows.append(
            [
                code(code_name),
                code(run["hist_2024"]["return_pct"]),
                code(run["hist_2024"]["max_dd_pct"]),
                code(run["validation"]["return_pct"]),
                code(run["validation"]["max_dd_pct"]),
                code(run["test"]["return_pct"]),
                code(run["test"]["max_dd_pct"]),
                code(comparison.get("shared_delta_vs_baseline", 0.0)),
                code(comparison.get("mean_winner_clip_rate", 0.0), digits=4),
                code(comparison.get("mean_loser_mitigation_rate", 0.0), digits=4),
                code(read_note),
            ]
        )
    lines.extend(
        render_markdown_table(
            [
                "run",
                "hist_return",
                "hist_dd",
                "val_return",
                "val_dd",
                "test_return",
                "test_dd",
                "shared_delta_vs_22Q",
                "winner_clip",
                "loser_mitigation",
                "read",
            ],
            regular_rows,
        )
    )
    lines.extend(
        [
            "",
            "## Headline",
            "",
            f"- incumbent `22Q`: `hist_return={incumbent['hist_2024']['return_pct']}`, `val_return={incumbent['validation']['return_pct']}`, `test_return={incumbent['test']['return_pct']}`, `test_pf={incumbent['test']['profit_factor']}`, `test_dd={incumbent['test']['max_dd_pct']}`",
            f"- challenger `22R`: `hist_return={challenger['hist_2024']['return_pct']}`, `val_return={challenger['validation']['return_pct']}`, `test_return={challenger['test']['return_pct']}`, `test_pf={challenger['test']['profit_factor']}`, `test_dd={challenger['test']['max_dd_pct']}`",
            "",
            "## Risk",
            "",
            f"- incumbent `22Q`: `ulcer={incumbent['test_risk']['ulcer_index']}`, `worst_week={incumbent['test_risk']['worst_week']}`, `consecutive_losses={incumbent['test_risk']['consecutive_losses']}`, `min_free_margin={incumbent['test_risk']['min_free_margin']}`",
            f"- challenger `22R`: `ulcer={challenger['test_risk']['ulcer_index']}`, `worst_week={challenger['test_risk']['worst_week']}`, `consecutive_losses={challenger['test_risk']['consecutive_losses']}`, `min_free_margin={challenger['test_risk']['min_free_margin']}`",
            "",
            "## Diagnostics",
            "",
            f"- incumbent `22Q`: `no_trade_rate={incumbent['test_diagnostics']['no_trade_rate']}`, `long_short={incumbent['test_diagnostics']['long_count']}/{incumbent['test_diagnostics']['short_count']}`, `avg_hold={incumbent['test_diagnostics']['avg_hold']}`, `risk_contexts={incumbent['test_risk_context']['risk_context_counts']}`",
            f"- challenger `22R`: `no_trade_rate={challenger['test_diagnostics']['no_trade_rate']}`, `long_short={challenger['test_diagnostics']['long_count']}/{challenger['test_diagnostics']['short_count']}`, `avg_hold={challenger['test_diagnostics']['avg_hold']}`, `shared_delta={challenger['test_position_comparison']['shared_delta_vs_baseline']}`, `winner_clip={challenger['test_position_comparison']['mean_winner_clip_rate']}`, `loser_mitigation={challenger['test_position_comparison']['mean_loser_mitigation_rate']}`",
            "",
            "## Execution",
            "",
            f"- incumbent `22Q`: `skip_rate={display(incumbent['test_execution']['skip_rate'])}`, `external_mismatch_count={display(incumbent['test_execution']['external_mismatch_count'])}`, `fill_rate={display(incumbent['test_execution']['fill_rate'])}`, `contract_skip_count={display(incumbent['test_execution']['contract_skip_count'])}`",
            f"- challenger `22R`: `skip_rate={display(challenger['test_execution']['skip_rate'])}`, `external_mismatch_count={display(challenger['test_execution']['external_mismatch_count'])}`, `fill_rate={display(challenger['test_execution']['fill_rate'])}`, `contract_skip_count={display(challenger['test_execution']['contract_skip_count'])}`",
            "- regular line uses the intended risk stack; mismatch-relaxation runs remain outside the regular decision lane.",
            "",
            "## Decision",
            "",
            "- decision: `keep_incumbent`",
            "- regular incumbent: `22Q_05dp_base_risk2_dirsplit_postcash_0001`",
            "- regular shadow challenger: `22R_05dp_psl45_qtr_h3_risk2_0001`",
            "",
            "## Follow-Up Bias",
            "",
            "- keep `22Q` as the regular Stage 22 reference",
            "- keep `22R` as the shadow containment challenger",
            "- treat `22A` and `22O` as structural-scout context, not as the operating scoreboard",
            "- do not advance mismatch-relaxation experiments into the regular line unless a new contract hypothesis appears",
            "",
            "## Report Refs",
            "",
            "- `03_reviews/stage22_ledger_postmortem_20260408.md`",
            "- `03_reviews/stage22_trigger_zone_review_20260408.md`",
            "- `03_reviews/stage22_followup_execution_review_20260408.md`",
            "- `03_reviews/stage22_partial_sl_refine_wave2_20260408.md`",
            "- `03_reviews/stage22_alignment_ablation_20260408.md`",
            "- `03_reviews/stage22_risk_overlay_wave1_20260409.md`",
        ]
    )
    return lines


def build_review_index_markdown(reviewed_on: str) -> list[str]:
    return [
        "# Stage 22 Review Index",
        "",
        f"- updated_on: `{reviewed_on}`",
        "- regular_decision: `22Q keep incumbent, 22R shadow containment challenger`",
        "- structural_scout_decision: `22A keep scout incumbent, 22O best scout containment challenger`",
        "- closed_diagnostic_branch: `alignment relaxation / mismatch curiosity stays closed outside the regular line`",
        "",
        "## Read Order",
        "",
        "1. `../00_spec/stage_brief.md`",
        "2. `stage22_ledger_postmortem_20260408.md`",
        "3. `stage22_trigger_zone_review_20260408.md`",
        "4. `stage22_followup_execution_review_20260408.md`",
        "5. `stage22_partial_sl_refine_wave2_20260408.md`",
        "6. `stage22_risk_overlay_wave1_20260409.md`",
        "7. `../04_selected/selection_status.md`",
        "",
        "## Review Chain",
        "",
        "- `stage22_review.md`: original fixed-lot single-rule screen; baseline kept.",
        "- `stage22_ledger_postmortem_20260408.md`: position-level winner-clip / loser-relief read.",
        "- `stage22_trigger_zone_review_20260408.md`: trigger-zone gap analysis for winners and losers.",
        "- `stage22_followup_execution_review_20260408.md`: runtime restoration and follow-up execution reproduction.",
        "- `stage22_partial_sl_refine_wave2_20260408.md`: structural scout refinement after volume-step discovery; `22O` became the best scout containment challenger.",
        "- `stage22_alignment_ablation_20260408.md`: curiosity-only mismatch ablation; explicitly closed from the regular experiment lane.",
        "- `stage22_risk_overlay_wave1_20260409.md`: regular risk execution scoreboard; `22Q` stayed incumbent and `22R` became the best regular containment challenger.",
    ]


def main() -> int:
    reviewed_on = datetime.now().astimezone().date().isoformat()
    results: dict[str, Any] = {"generated_at_utc": datetime.now(timezone.utc).isoformat(), "runs": {}}

    baseline_hist_rows = load_position_rows(COMMON_RUNTIME_DIR / RUNS["22Q"]["runtime_id"] / "logs" / "att_0003_trades.csv")
    baseline_test_rows = load_position_rows(COMMON_RUNTIME_DIR / RUNS["22Q"]["runtime_id"] / "logs" / "att_0002_trades.csv")
    baseline_hist_map = position_net_map(baseline_hist_rows)
    baseline_test_map = position_net_map(baseline_test_rows)

    for code_name, config in RUNS.items():
        hist_summary = load_summary(code_name, config["hist_attempt"])
        validation_summary = load_summary(code_name, config["validation_attempt"])
        test_summary = load_summary(code_name, config["test_attempt"])

        test_rows = load_position_rows(COMMON_RUNTIME_DIR / config["runtime_id"] / "logs" / "att_0002_trades.csv")
        hist_rows = load_position_rows(COMMON_RUNTIME_DIR / config["runtime_id"] / "logs" / "att_0003_trades.csv")
        payload = {
            "label": config["label"],
            "hist_2024": headline(hist_summary),
            "validation": headline(validation_summary),
            "test": headline(test_summary),
            "test_risk": risk_layer(test_summary),
            "test_diagnostics": diagnostics_layer(test_summary),
            "test_execution": execution_layer(test_summary),
            "test_risk_context": risk_context_snapshot(test_rows),
        }
        if code_name != "22Q":
            payload["test_position_comparison"] = compare_positions(baseline_test_map, position_net_map(test_rows))
            payload["hist_position_comparison"] = compare_positions(baseline_hist_map, position_net_map(hist_rows))
        results["runs"][code_name] = payload

    structural_scout = load_structural_scout()
    output_payload = {
        "generated_at_utc": results["generated_at_utc"],
        "reviewed_on": reviewed_on,
        "structural_scout": structural_scout,
        "regular_risk_execution": results["runs"],
        "current_read": {
            "structural_scout_incumbent": "22A_05dp_base_hold5_0001",
            "structural_scout_challenger": "22O_05dp_psl45_p10_h3_0001",
            "regular_incumbent": "22Q_05dp_base_risk2_dirsplit_postcash_0001",
            "regular_shadow_challenger": "22R_05dp_psl45_qtr_h3_risk2_0001",
            "decision": "keep_incumbent",
        },
    }

    write_json(OUTPUT_JSON, output_payload)
    write_markdown(OUTPUT_MD, build_review_markdown(reviewed_on, results, structural_scout))
    write_markdown(SELECTION_MD, build_selection_markdown(reviewed_on, results, structural_scout))
    write_markdown(REVIEW_INDEX_MD, build_review_index_markdown(reviewed_on))
    print(f"[done] json={OUTPUT_JSON}")
    print(f"[done] md={OUTPUT_MD}")
    print(f"[done] selection={SELECTION_MD}")
    print(f"[done] review_index={REVIEW_INDEX_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
