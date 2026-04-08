#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import math
from collections import Counter, defaultdict
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[3]
OUTPUT_JSON = ROOT_DIR / "stages" / "22_point_exit_management" / "03_reviews" / "stage22_alignment_ablation_20260408.json"
OUTPUT_MD = ROOT_DIR / "stages" / "22_point_exit_management" / "03_reviews" / "stage22_alignment_ablation_20260408.md"

RUN_SPECS = [
    {
        "label": "22A_exact",
        "run_name": "22A_05dp_base_hold5_0001",
        "runtime_id_validation": "exp_22a_05dp_base_val_2501_v1",
        "runtime_id_test": "exp_22a_05dp_base_oos_2501_v1",
        "attempt_validation": "att_0002",
        "attempt_test": "att_0003",
        "summary_validation": ROOT_DIR / "stages" / "22_point_exit_management" / "02_runs" / "active" / "22A_05dp_base_hold5_0001" / "mt5_attempts" / "att_0002" / "tester_attempt_summary.json",
        "summary_test": ROOT_DIR / "stages" / "22_point_exit_management" / "02_runs" / "active" / "22A_05dp_base_hold5_0001" / "mt5_attempts" / "att_0003" / "tester_attempt_summary.json",
    },
    {
        "label": "22I_breadth_stale1",
        "run_name": "22I_05dp_breadth_stale1_0001",
        "runtime_id_validation": "exp_22i_05dp_breadth_stale1_v1",
        "runtime_id_test": "exp_22i_05dp_breadth_stale1_v1",
        "attempt_validation": "att_0001",
        "attempt_test": "att_0002",
        "summary_validation": ROOT_DIR / "stages" / "22_point_exit_management" / "02_runs" / "active" / "22I_05dp_breadth_stale1_0001" / "mt5_attempts" / "att_0001" / "tester_attempt_summary.json",
        "summary_test": ROOT_DIR / "stages" / "22_point_exit_management" / "02_runs" / "active" / "22I_05dp_breadth_stale1_0001" / "mt5_attempts" / "att_0002" / "tester_attempt_summary.json",
    },
    {
        "label": "22J_macro_stale1",
        "run_name": "22J_05dp_macro_stale1_0001",
        "runtime_id_validation": "exp_22j_05dp_macro_stale1_v1",
        "runtime_id_test": "exp_22j_05dp_macro_stale1_v1",
        "attempt_validation": "att_0001",
        "attempt_test": "att_0002",
        "summary_validation": ROOT_DIR / "stages" / "22_point_exit_management" / "02_runs" / "active" / "22J_05dp_macro_stale1_0001" / "mt5_attempts" / "att_0001" / "tester_attempt_summary.json",
        "summary_test": ROOT_DIR / "stages" / "22_point_exit_management" / "02_runs" / "active" / "22J_05dp_macro_stale1_0001" / "mt5_attempts" / "att_0002" / "tester_attempt_summary.json",
    },
    {
        "label": "22K_all_stale1",
        "run_name": "22K_05dp_all_stale1_0001",
        "runtime_id_validation": "exp_22k_05dp_all_stale1_v1",
        "runtime_id_test": "exp_22k_05dp_all_stale1_v1",
        "attempt_validation": "att_0001",
        "attempt_test": "att_0002",
        "summary_validation": ROOT_DIR / "stages" / "22_point_exit_management" / "02_runs" / "active" / "22K_05dp_all_stale1_0001" / "mt5_attempts" / "att_0001" / "tester_attempt_summary.json",
        "summary_test": ROOT_DIR / "stages" / "22_point_exit_management" / "02_runs" / "active" / "22K_05dp_all_stale1_0001" / "mt5_attempts" / "att_0002" / "tester_attempt_summary.json",
    },
]


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def load_shadow_rows(runtime_id: str, attempt_id: str) -> list[dict[str, str]]:
    path = (
        Path.home()
        / "AppData"
        / "Roaming"
        / "MetaQuotes"
        / "Terminal"
        / "Common"
        / "Files"
        / "Project_Obsidian_Prime"
        / "runtime"
        / runtime_id
        / "logs"
        / f"{attempt_id}_shadow.csv"
    )
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def normalized_entropy(p_short: float, p_flat: float, p_long: float) -> float:
    probs = [max(p_short, 1e-12), max(p_flat, 1e-12), max(p_long, 1e-12)]
    total = sum(probs)
    probs = [value / total for value in probs]
    entropy = -sum(value * math.log(value) for value in probs)
    return entropy / math.log(3.0)


def parse_fallback_details(detail_text: str) -> Counter[str]:
    counter: Counter[str] = Counter()
    if not detail_text:
      return counter
    for token in detail_text.split("|"):
        if ":" not in token:
            continue
        symbol, stale = token.split(":", 1)
        counter[symbol] += 1
    return counter


def analyze_rows(rows: list[dict[str, str]], baseline_external_skip_map: dict[str, str] | None) -> dict:
    ready_rows = [row for row in rows if row.get("row_ready", "").lower() == "true"]
    skip_rows = [row for row in rows if row.get("row_ready", "").lower() != "true"]

    decision_counter = Counter(row.get("decision", "") for row in ready_rows)
    skip_counter = Counter(row.get("skip_reason", "") for row in skip_rows if row.get("skip_reason", ""))

    entropy_values: list[float] = []
    argmax_counter: Counter[str] = Counter()
    extreme_confidence = 0
    fallback_rows = 0
    fallback_events = 0
    fallback_symbols: Counter[str] = Counter()
    recovered_external_ready_rows = 0
    recovered_external_signal_rows = 0

    for row in ready_rows:
        p_short = float(row.get("p_short", "0") or 0.0)
        p_flat = float(row.get("p_flat", "0") or 0.0)
        p_long = float(row.get("p_long", "0") or 0.0)
        probs = {"SHORT": p_short, "NO_TRADE": p_flat, "LONG": p_long}
        argmax_label = max(probs, key=probs.get)
        argmax_counter[argmax_label] += 1
        entropy = normalized_entropy(p_short, p_flat, p_long)
        entropy_values.append(entropy)
        if max(p_short, p_flat, p_long) >= 0.97:
            extreme_confidence += 1

        fallback_used = row.get("external_fallback_used", "").lower() == "true"
        if fallback_used:
            fallback_rows += 1
            fallback_events += int(row.get("external_fallback_count", "0") or 0)
            fallback_symbols.update(parse_fallback_details(row.get("external_fallback_details", "")))

        if baseline_external_skip_map is not None:
            baseline_skip = baseline_external_skip_map.get(row.get("bar_time_server", ""))
            if baseline_skip and baseline_skip.startswith("EXTERNAL_TIMESTAMP_MISMATCH_"):
                recovered_external_ready_rows += 1
                if row.get("decision", "") in {"LONG", "SHORT"}:
                    recovered_external_signal_rows += 1

    max_argmax_share = 0.0
    if ready_rows:
        max_argmax_share = max(argmax_counter.values()) / len(ready_rows)

    return {
        "row_count": len(rows),
        "ready_row_count": len(ready_rows),
        "skip_row_count": len(skip_rows),
        "ready_rate": (len(ready_rows) / len(rows)) if rows else 0.0,
        "long_signal_count": decision_counter.get("LONG", 0),
        "short_signal_count": decision_counter.get("SHORT", 0),
        "no_trade_count": decision_counter.get("NO_TRADE", 0),
        "no_trade_rate": (decision_counter.get("NO_TRADE", 0) / len(ready_rows)) if ready_rows else 1.0,
        "skip_reason_breakdown": dict(skip_counter),
        "external_mismatch_count": sum(
            count for reason, count in skip_counter.items() if reason.startswith("EXTERNAL_TIMESTAMP_MISMATCH_")
        ),
        "argmax_share": {key: value / len(ready_rows) for key, value in argmax_counter.items()} if ready_rows else {},
        "max_argmax_share": max_argmax_share,
        "avg_entropy_norm": (sum(entropy_values) / len(entropy_values)) if entropy_values else None,
        "extreme_confidence_rate": (extreme_confidence / len(ready_rows)) if ready_rows else None,
        "fallback_rows": fallback_rows,
        "fallback_events": fallback_events,
        "fallback_symbol_breakdown": dict(fallback_symbols),
        "recovered_external_ready_rows": recovered_external_ready_rows,
        "recovered_external_signal_rows": recovered_external_signal_rows,
    }


def summarize_run(label: str, split_name: str, summary_path: Path, runtime_id: str, attempt_id: str, baseline_external_skip_map: dict[str, str] | None) -> dict:
    summary = load_json(summary_path)
    rows = load_shadow_rows(runtime_id, attempt_id)
    row_metrics = analyze_rows(rows, baseline_external_skip_map)
    headline = summary["financial_metrics"]["headline"]
    diagnostics_extra = summary["financial_metrics"]["diagnostics"]["extra"]
    return {
        "label": label,
        "split": split_name,
        "summary_path": str(summary_path),
        "headline": {
            "return_pct": headline["return_pct"],
            "profit_factor": headline["profit_factor"],
            "trade_count": headline["trade_count"],
            "max_dd_pct": headline["max_dd_pct"],
        },
        "trade_close_reason_breakdown": diagnostics_extra.get("trade_close_reason_breakdown", {}),
        "row_metrics": row_metrics,
    }


def build_baseline_skip_map(runtime_id: str, attempt_id: str) -> dict[str, str]:
    rows = load_shadow_rows(runtime_id, attempt_id)
    return {row.get("bar_time_server", ""): row.get("skip_reason", "") for row in rows}


def to_md(payload: dict) -> str:
    lines: list[str] = []
    lines.append("# Stage 22 Alignment Ablation Review")
    lines.append("")
    lines.append("- reviewed on: `2026-04-08`")
    lines.append("- purpose: `curiosity ablation` for external timestamp mismatch handling")
    lines.append("- baseline contract remains `exact alignment + all-or-skip`; these runs are diagnostic only")
    lines.append("")
    lines.append("## Setup")
    lines.append("")
    lines.append("- `22I`: breadth-only `stale_closed_bar`, max stale `1`")
    lines.append("- `22J`: macro-only `stale_closed_bar`, max stale `1`")
    lines.append("- `22K`: all externals `stale_closed_bar`, max stale `1`")
    lines.append("- guardrails: `future disallowed`, `date-cross carry disallowed`")
    lines.append("")

    for split_name in ["validation", "test"]:
        lines.append(f"## {split_name.title()}")
        lines.append("")
        lines.append("| run | return_pct | PF | trades | max_dd_pct | ready_rows | ext_mismatch_skips | fallback_rows | recovered_ready | recovered_signals |")
        lines.append("|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
        for row in payload["results"][split_name]:
            lines.append(
                "| `{}` | `{:.3f}` | `{:.4f}` | `{}` | `{:.3f}` | `{}` | `{}` | `{}` | `{}` | `{}` |".format(
                    row["label"],
                    row["headline"]["return_pct"],
                    row["headline"]["profit_factor"],
                    row["headline"]["trade_count"],
                    row["headline"]["max_dd_pct"],
                    row["row_metrics"]["ready_row_count"],
                    row["row_metrics"]["external_mismatch_count"],
                    row["row_metrics"]["fallback_rows"],
                    row["row_metrics"]["recovered_external_ready_rows"],
                    row["row_metrics"]["recovered_external_signal_rows"],
                )
            )
        lines.append("")

    lines.append("## KPI Notes")
    lines.append("")
    for split_name in ["validation", "test"]:
        lines.append(f"### {split_name.title()}")
        for row in payload["results"][split_name]:
            metrics = row["row_metrics"]
            lines.append(
                "- `{}`: no-trade `{:.4f}`, max argmax share `{:.4f}`, avg entropy `{:.4f}`, extreme confidence `{:.4f}`, fallback symbols `{}`".format(
                    row["label"],
                    metrics["no_trade_rate"],
                    metrics["max_argmax_share"],
                    metrics["avg_entropy_norm"] if metrics["avg_entropy_norm"] is not None else 0.0,
                    metrics["extreme_confidence_rate"] if metrics["extreme_confidence_rate"] is not None else 0.0,
                    metrics["fallback_symbol_breakdown"],
                )
            )
        lines.append("")

    lines.append("## Interpretation")
    lines.append("")
    lines.extend(payload["interpretation"])
    lines.append("")
    return "\n".join(lines)


def find_result(results: dict[str, list[dict]], split_name: str, label: str) -> dict:
    for row in results[split_name]:
        if row["label"] == label:
            return row
    raise KeyError(f"missing result for split={split_name} label={label}")


def main() -> int:
    baseline_validation_skip_map = build_baseline_skip_map("exp_22a_05dp_base_val_2501_v1", "att_0002")
    baseline_test_skip_map = build_baseline_skip_map("exp_22a_05dp_base_oos_2501_v1", "att_0003")

    results: dict[str, list[dict]] = defaultdict(list)
    for spec in RUN_SPECS:
        results["validation"].append(
            summarize_run(
                spec["label"],
                "validation",
                spec["summary_validation"],
                spec["runtime_id_validation"],
                spec["attempt_validation"],
                baseline_validation_skip_map,
            )
        )
        results["test"].append(
            summarize_run(
                spec["label"],
                "test",
                spec["summary_test"],
                spec["runtime_id_test"],
                spec["attempt_test"],
                baseline_test_skip_map,
            )
        )

    base_test = find_result(results, "test", "22A_exact")
    breadth_test = find_result(results, "test", "22I_breadth_stale1")
    macro_test = find_result(results, "test", "22J_macro_stale1")
    all_test = find_result(results, "test", "22K_all_stale1")
    breadth_val = find_result(results, "validation", "22I_breadth_stale1")
    macro_val = find_result(results, "validation", "22J_macro_stale1")
    all_val = find_result(results, "validation", "22K_all_stale1")

    interpretation = [
        (
            "- `22I breadth-only stale1` recovered `{}` validation rows and `{}` test rows, "
            "but only produced `{}` recovered signal rows on validation and `{}` on test. "
            "Test PnL was unchanged versus baseline, so breadth mismatches do not look like "
            "a large hidden pool of missed trades."
        ).format(
            breadth_val["row_metrics"]["recovered_external_ready_rows"],
            breadth_test["row_metrics"]["recovered_external_ready_rows"],
            breadth_val["row_metrics"]["recovered_external_signal_rows"],
            breadth_test["row_metrics"]["recovered_external_signal_rows"],
        ).replace("\n", " "),
        (
            "- `22J macro-only stale1` was the only arm that moved OOS headline meaningfully: test return `68.574 -> {:.3f}`, trades `275 -> {}`, with DD `19.394 -> {:.3f}`. The gain is real but modest, and it came with slightly worse no-trade/argmax concentration KPIs."
        ).format(
            macro_test["headline"]["return_pct"],
            macro_test["headline"]["trade_count"],
            macro_test["headline"]["max_dd_pct"],
        ),
        (
            "- `22K all stale1` recovered the most rows, but its test headline matched `22J` exactly. That means the extra breadth relaxation on top of macro did not add incremental OOS alpha in this slice."
        ),
        (
            "- Curiosity verdict: exact alignment is probably not hiding a huge missed-opportunity reservoir. If there is any upside to relaxing mismatch handling, it appears concentrated in macro externals and it is small enough that contract drift risk still matters."
        ),
    ]

    payload = {
        "generated_at": "2026-04-08",
        "results": results,
        "interpretation": interpretation,
    }
    OUTPUT_JSON.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    OUTPUT_MD.write_text(to_md(payload), encoding="utf-8")
    print(f"[done] json={OUTPUT_JSON}")
    print(f"[done] md={OUTPUT_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
