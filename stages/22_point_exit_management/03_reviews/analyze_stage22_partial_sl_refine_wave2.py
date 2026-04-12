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

RUNS = {
    "22A": {
        "label": "baseline_time_exit",
        "run_dir": STAGE_DIR / "02_runs" / "active" / "22A_05dp_base_hold5_0001",
        "validation_attempt": "att_0002",
        "test_attempt": "att_0003",
        "runtime_id_test": "exp_22a_05dp_base_oos_2501_v1",
    },
    "22D": {
        "label": "psl45_half_h1",
        "run_dir": STAGE_DIR / "02_runs" / "active" / "22D_05dp_psl45_half_0001",
        "validation_attempt": "att_0002",
        "test_attempt": "att_0003",
        "runtime_id_test": "exp_22d_05dp_psl45_half_v1_oos_2501",
    },
    "22F": {
        "label": "psl45_qtr_h2",
        "run_dir": STAGE_DIR / "02_runs" / "active" / "22F_05dp_psl45_qtr_minhold2_0001",
        "validation_attempt": "att_0001",
        "test_attempt": "att_0002",
        "runtime_id_test": "exp_22f_05dp_psl45_qtr_h2_v1",
    },
    "22L": {
        "label": "psl45_p20_h2",
        "run_dir": STAGE_DIR / "02_runs" / "active" / "22L_05dp_psl45_p20_minhold2_0001",
        "validation_attempt": "att_0001",
        "test_attempt": "att_0002",
        "runtime_id_test": "exp_22l_05dp_psl45_p20_h2_v1",
    },
    "22M": {
        "label": "psl45_qtr_h3",
        "run_dir": STAGE_DIR / "02_runs" / "active" / "22M_05dp_psl45_qtr_minhold3_0001",
        "validation_attempt": "att_0001",
        "test_attempt": "att_0002",
        "runtime_id_test": "exp_22m_05dp_psl45_qtr_h3_v1",
    },
    "22N": {
        "label": "psl45_p20_h3",
        "run_dir": STAGE_DIR / "02_runs" / "active" / "22N_05dp_psl45_p20_minhold3_0001",
        "validation_attempt": "att_0001",
        "test_attempt": "att_0002",
        "runtime_id_test": "exp_22n_05dp_psl45_p20_h3_v1",
    },
    "22O": {
        "label": "psl45_p10_h3",
        "run_dir": STAGE_DIR / "02_runs" / "active" / "22O_05dp_psl45_p10_minhold3_0001",
        "validation_attempt": "att_0001",
        "test_attempt": "att_0002",
        "runtime_id_test": "exp_22o_05dp_psl45_p10_h3_v1",
    },
    "22P": {
        "label": "psl45_p30_h3",
        "run_dir": STAGE_DIR / "02_runs" / "active" / "22P_05dp_psl45_p30_minhold3_0001",
        "validation_attempt": "att_0001",
        "test_attempt": "att_0002",
        "runtime_id_test": "exp_22p_05dp_psl45_p30_h3_v1",
    },
}

COMMON_RUNTIME_DIR = Path.home() / "AppData" / "Roaming" / "MetaQuotes" / "Terminal" / "Common" / "Files" / "Project_Obsidian_Prime" / "runtime"


def load_summary(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_position_net_map(trade_path: Path) -> dict[str, float]:
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    with trade_path.open("r", encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            key = f"{row['entry_bar_time_server']}|{row['direction']}"
            grouped[key].append(row)

    return {
        key: round(sum(float((row["net_profit"] or "0").strip() or 0.0) for row in rows), 6)
        for key, rows in grouped.items()
    }


def load_partial_events(trade_path: Path, baseline_position_net: dict[str, float]) -> dict[str, Any]:
    hold_counter: Counter[int] = Counter()
    class_counter: Counter[str] = Counter()
    volume_counter: Counter[str] = Counter()

    with trade_path.open("r", encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            if row["close_reason"] != "PARTIAL_STOP_LOSS":
                continue
            key = f"{row['entry_bar_time_server']}|{row['direction']}"
            baseline_net = baseline_position_net[key]
            baseline_class = "winner" if baseline_net > 0 else "loser" if baseline_net < 0 else "flat"
            hold_counter[int((row["hold_bars"] or "0").strip() or 0)] += 1
            class_counter[baseline_class] += 1
            volume_counter[row["volume"]] += 1

    return {
        "event_count": sum(hold_counter.values()),
        "hold_distribution": dict(sorted(hold_counter.items())),
        "baseline_class_mix": dict(class_counter),
        "partial_close_volumes": dict(volume_counter),
    }


def compute_clip_metrics(
    baseline_position_net: dict[str, float],
    variant_position_net: dict[str, float],
) -> dict[str, float]:
    shared_keys = sorted(set(baseline_position_net) & set(variant_position_net))
    winner_clips: list[float] = []
    loser_mitigations: list[float] = []
    shared_delta = 0.0
    for key in shared_keys:
        base_value = baseline_position_net[key]
        variant_value = variant_position_net[key]
        shared_delta += variant_value - base_value
        if base_value > 0.0:
            winner_clips.append(max(0.0, (base_value - variant_value) / base_value))
        elif base_value < 0.0:
            loser_mitigations.append(max(0.0, (variant_value - base_value) / abs(base_value)))

    return {
        "shared_delta_vs_22A": round(shared_delta, 3),
        "mean_winner_clip_rate": round(sum(winner_clips) / len(winner_clips), 4) if winner_clips else 0.0,
        "mean_loser_mitigation_rate": round(sum(loser_mitigations) / len(loser_mitigations), 4) if loser_mitigations else 0.0,
    }


def headline_from_summary(summary: dict[str, Any]) -> dict[str, Any]:
    headline = summary["financial_metrics"]["headline"]
    return {
        "return_pct": round(headline["return_pct"], 3),
        "profit_factor": round(headline["profit_factor"], 4),
        "trade_count": headline["trade_count"],
        "max_dd_pct": round(headline["max_dd_pct"], 3),
    }


def main() -> int:
    baseline_validation = load_summary(
        RUNS["22A"]["run_dir"] / "mt5_attempts" / RUNS["22A"]["validation_attempt"] / "tester_attempt_summary.json"
    )
    baseline_test = load_summary(
        RUNS["22A"]["run_dir"] / "mt5_attempts" / RUNS["22A"]["test_attempt"] / "tester_attempt_summary.json"
    )
    baseline_position_net = load_position_net_map(
        COMMON_RUNTIME_DIR / RUNS["22A"]["runtime_id_test"] / "logs" / "att_0003_trades.csv"
    )

    results: dict[str, Any] = {"generated_at_utc": datetime.now(timezone.utc).isoformat(), "runs": {}}
    for code, config in RUNS.items():
        validation_summary = load_summary(
            config["run_dir"] / "mt5_attempts" / config["validation_attempt"] / "tester_attempt_summary.json"
        )
        test_summary = load_summary(
            config["run_dir"] / "mt5_attempts" / config["test_attempt"] / "tester_attempt_summary.json"
        )
        run_payload: dict[str, Any] = {
            "label": config["label"],
            "validation": headline_from_summary(validation_summary),
            "test": headline_from_summary(test_summary),
        }
        if code != "22A":
            trade_path = COMMON_RUNTIME_DIR / config["runtime_id_test"] / "logs" / f"{config['test_attempt']}_trades.csv"
            variant_position_net = load_position_net_map(trade_path)
            run_payload["test_partial_events"] = load_partial_events(trade_path, baseline_position_net)
            run_payload["test_position_comparison"] = compute_clip_metrics(baseline_position_net, variant_position_net)
        results["runs"][code] = run_payload

    alias_pairs = []
    if results["runs"]["22F"]["test"] == results["runs"]["22L"]["test"] and results["runs"]["22F"]["validation"] == results["runs"]["22L"]["validation"]:
        alias_pairs.append("22F == 22L")
    if results["runs"]["22M"]["test"] == results["runs"]["22N"]["test"] and results["runs"]["22M"]["validation"] == results["runs"]["22N"]["validation"]:
        alias_pairs.append("22M == 22N")
    results["alias_pairs"] = alias_pairs

    md_lines = [
        "# Stage 22 Partial Stop-Loss Refinement Wave 2",
        "",
        f"- reviewed on: `{datetime.now(timezone.utc).date().isoformat()}`",
        "- focus: `partial stop-loss refinement after 22F/22M follow-up and volume-step alias check`",
        "- note: `US100 fixed 0.1 lot means partial close fractions collapse onto broker volume steps`",
        "",
        "## Validation",
        "",
        "| run | return_pct | PF | trade_count | max_dd_pct |",
        "|---|---:|---:|---:|---:|",
    ]
    for code in ["22A", "22D", "22F", "22M", "22O", "22P"]:
        val = results["runs"][code]["validation"]
        md_lines.append(
            f"| `{code}` | `{val['return_pct']:.3f}` | `{val['profit_factor']:.4f}` | `{val['trade_count']}` | `{val['max_dd_pct']:.3f}` |"
        )

    md_lines.extend(
        [
            "",
            "## Test",
            "",
            "| run | return_pct | PF | trade_count | max_dd_pct | shared_delta_vs_22A | winner_clip | loser_mitigation | partial_events | partial_volume |",
            "|---|---:|---:|---:|---:|---:|---:|---:|---:|---|",
        ]
    )
    for code in ["22A", "22D", "22F", "22M", "22O", "22P"]:
        test = results["runs"][code]["test"]
        if code == "22A":
            md_lines.append(
                f"| `{code}` | `{test['return_pct']:.3f}` | `{test['profit_factor']:.4f}` | `{test['trade_count']}` | `{test['max_dd_pct']:.3f}` | `0.000` | `0.0000` | `0.0000` | `0` | `-` |"
            )
            continue
        comparison = results["runs"][code]["test_position_comparison"]
        events = results["runs"][code]["test_partial_events"]
        md_lines.append(
            f"| `{code}` | `{test['return_pct']:.3f}` | `{test['profit_factor']:.4f}` | `{test['trade_count']}` | `{test['max_dd_pct']:.3f}` | "
            f"`{comparison['shared_delta_vs_22A']:.3f}` | `{comparison['mean_winner_clip_rate']:.4f}` | `{comparison['mean_loser_mitigation_rate']:.4f}` | "
            f"`{events['event_count']}` | `{events['partial_close_volumes']}` |"
        )

    md_lines.extend(
        [
            "",
            "## Test Event Timing",
            "",
            f"- alias pairs: `{', '.join(alias_pairs) if alias_pairs else 'none'}`",
            f"- `22F`: holds `{results['runs']['22F']['test_partial_events']['hold_distribution']}`, class mix `{results['runs']['22F']['test_partial_events']['baseline_class_mix']}`",
            f"- `22M`: holds `{results['runs']['22M']['test_partial_events']['hold_distribution']}`, class mix `{results['runs']['22M']['test_partial_events']['baseline_class_mix']}`",
            f"- `22O`: holds `{results['runs']['22O']['test_partial_events']['hold_distribution']}`, class mix `{results['runs']['22O']['test_partial_events']['baseline_class_mix']}`",
            f"- `22P`: holds `{results['runs']['22P']['test_partial_events']['hold_distribution']}`, class mix `{results['runs']['22P']['test_partial_events']['baseline_class_mix']}`",
            "",
            "## Interpretation",
            "",
            "- `22L` and `22N` were not real new information. Because `0.1 lot` is quantized by broker volume step, both `20%` and `25%` partial closes resolved to the same `0.02 lot` close volume as their paired runs.",
            "- `22M` confirmed that delaying partial stop loss to `min_hold_bars=3` helps compared with `22F`: fewer events (`128 -> 118`) and lower winner contamination (`29 -> 22` winner-tagged events), with slightly better OOS return.",
            "- `22O` was the cleanest alpha-preserving containment candidate. It kept the cleaner `h3` timing from `22M`, but reduced the actual close size to `0.01 lot`. That cut shared-position drag to `-9.470`, the best among partial-stop variants tested here, and lifted OOS return to `66.680`.",
            "- `22P` showed the other side of the frontier. Raising the actual close size to `0.03 lot` improved containment more strongly than `22O`, but it also increased winner clipping and gave back more headline return.",
            "- None of the refinement variants beat `22A`. The current read is still `keep incumbent`, but if a containment challenger is worth carrying forward, `22O` is the most interesting trade-off after accounting for real broker volume quantization.",
        ]
    )

    json_path = REVIEW_DIR / "stage22_partial_sl_refine_wave2_20260408.json"
    md_path = REVIEW_DIR / "stage22_partial_sl_refine_wave2_20260408.md"
    json_path.write_text(json.dumps(results, indent=2), encoding="utf-8")
    md_path.write_text("\n".join(md_lines) + "\n", encoding="utf-8")
    print(f"[done] json={json_path}")
    print(f"[done] md={md_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
