from __future__ import annotations

import csv
import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[3]
STAGE_DIR = PROJECT_ROOT / "stages" / "22_point_exit_management"
REVIEW_DIR = STAGE_DIR / "03_reviews"
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


def load_summary(run_code: str, attempt_id: str) -> dict[str, Any]:
    path = STAGE_DIR / "02_runs" / "active" / RUNS[run_code]["folder"] / "mt5_attempts" / attempt_id / "tester_attempt_summary.json"
    return json.loads(path.read_text(encoding="utf-8"))


def headline(summary: dict[str, Any]) -> dict[str, Any]:
    h = summary["financial_metrics"]["headline"]
    r = summary["financial_metrics"]["risk"]
    return {
        "return_pct": round(h["return_pct"], 3),
        "profit_factor": round(h["profit_factor"], 4),
        "trade_count": h["trade_count"],
        "max_dd_pct": round(h["max_dd_pct"], 3),
        "worst_week": round(r["worst_week"], 3) if r.get("worst_week") is not None else None,
        "ulcer_index": round(r["ulcer_index"], 3) if r.get("ulcer_index") is not None else None,
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
        "avg_initial_risk_amount": round(sum(initial_risks) / len(initial_risks), 3) if initial_risks else None,
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
        "shared_delta_vs_baseline": round(shared_delta, 3),
        "mean_winner_clip_rate": round(sum(winner_clips) / len(winner_clips), 4) if winner_clips else 0.0,
        "mean_loser_mitigation_rate": round(sum(loser_mitigations) / len(loser_mitigations), 4) if loser_mitigations else 0.0,
    }


def main() -> int:
    reviewed_on = datetime.now().astimezone().date().isoformat()
    results: dict[str, Any] = {"generated_at_utc": datetime.now(timezone.utc).isoformat(), "runs": {}}

    baseline_hist_rows = load_position_rows(COMMON_RUNTIME_DIR / RUNS["22Q"]["runtime_id"] / "logs" / "att_0003_trades.csv")
    baseline_test_rows = load_position_rows(COMMON_RUNTIME_DIR / RUNS["22Q"]["runtime_id"] / "logs" / "att_0002_trades.csv")
    baseline_hist_map = position_net_map(baseline_hist_rows)
    baseline_test_map = position_net_map(baseline_test_rows)

    for code, config in RUNS.items():
        hist_summary = load_summary(code, config["hist_attempt"])
        validation_summary = load_summary(code, config["validation_attempt"])
        test_summary = load_summary(code, config["test_attempt"])

        test_rows = load_position_rows(COMMON_RUNTIME_DIR / config["runtime_id"] / "logs" / "att_0002_trades.csv")
        hist_rows = load_position_rows(COMMON_RUNTIME_DIR / config["runtime_id"] / "logs" / "att_0003_trades.csv")
        payload = {
            "label": config["label"],
            "hist_2024": headline(hist_summary),
            "validation": headline(validation_summary),
            "test": headline(test_summary),
            "test_risk_context": risk_context_snapshot(test_rows),
        }
        if code != "22Q":
            payload["test_position_comparison"] = compare_positions(baseline_test_map, position_net_map(test_rows))
            payload["hist_position_comparison"] = compare_positions(baseline_hist_map, position_net_map(hist_rows))
        results["runs"][code] = payload

    md_lines = [
        "# Stage 22 Risk Overlay Wave 1",
        "",
        f"- reviewed on: `{reviewed_on}`",
        "- purpose: `return the Stage 22 family to regular risk-based execution instead of fixed 0.1 lot comparison`",
        "- risk overlay: `risk_pct=2.0, balance base, ATR14 broker-native SL, direction_split(long=1.4, short=2.0), monday=0.75, ny_postcash=0.70, hold_cap=3`",
        "",
        "## Cross-Split Headline",
        "",
        "| run | hist_return | hist_dd | val_return | val_dd | test_return | test_dd | test_pf |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for code in ["22Q", "22R", "22S", "22T"]:
        hist = results["runs"][code]["hist_2024"]
        val = results["runs"][code]["validation"]
        test = results["runs"][code]["test"]
        md_lines.append(
            f"| `{code}` | `{hist['return_pct']:.3f}` | `{hist['max_dd_pct']:.3f}` | "
            f"`{val['return_pct']:.3f}` | `{val['max_dd_pct']:.3f}` | "
            f"`{test['return_pct']:.3f}` | `{test['max_dd_pct']:.3f}` | `{test['profit_factor']:.4f}` |"
        )

    md_lines.extend(
        [
            "",
            "## Test Position Read",
            "",
            "| run | shared_delta_vs_22Q | winner_clip | loser_mitigation | position_count | risk_contexts | partial_volumes |",
            "|---|---:|---:|---:|---:|---|---|",
        ]
    )

    baseline_context = results["runs"]["22Q"]["test_risk_context"]
    md_lines.append(
        f"| `22Q` | `0.000` | `0.0000` | `0.0000` | `{baseline_context['position_count']}` | "
        f"`{baseline_context['risk_context_counts']}` | `-` |"
    )
    for code in ["22R", "22S", "22T"]:
        comparison = results["runs"][code]["test_position_comparison"]
        context = results["runs"][code]["test_risk_context"]
        md_lines.append(
            f"| `{code}` | `{comparison['shared_delta_vs_baseline']:.3f}` | `{comparison['mean_winner_clip_rate']:.4f}` | "
            f"`{comparison['mean_loser_mitigation_rate']:.4f}` | `{context['position_count']}` | "
            f"`{context['risk_context_counts']}` | `{context['partial_close_volumes']}` |"
        )

    md_lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- `22Q` established the proper regular baseline: once Stage 22 is put back on risk-based execution, the headline profile changes materially from the earlier fixed-lot probe. That fixed-lot read should be treated as structural scouting, not as the final operating verdict.",
            "- `22R` and `22T` were the only challengers that improved the risk-sized OOS slice at all. Both preserved the same `302` test positions as baseline and produced a small positive shared-position delta versus `22Q`.",
            "- `22S` was too gentle. Its smaller partials reduced winner clipping the most, but the loser relief was not strong enough and the OOS result fell behind baseline.",
            "- `22T` gave the best OOS drawdown and almost the same OOS return uplift as `22R`, but it paid a bit more validation and historical drag. `22R` was the cleaner compromise across the three windows.",
            "- Promotion is still too early. `22Q` keeps the best multi-window stability overall, while `22R` is now the best risk-sized containment challenger worth carrying forward.",
        ]
    )

    json_path = REVIEW_DIR / "stage22_risk_overlay_wave1_20260409.json"
    md_path = REVIEW_DIR / "stage22_risk_overlay_wave1_20260409.md"
    json_path.write_text(json.dumps(results, indent=2), encoding="utf-8")
    md_path.write_text("\n".join(md_lines) + "\n", encoding="utf-8")
    print(f"[done] json={json_path}")
    print(f"[done] md={md_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
