#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


ROOT_DIR = Path(__file__).resolve().parents[3]
STAGE_DIR = ROOT_DIR / "stages" / "36_outside_bar_localization_diagnostic"
RUN_DIRS = {
    "35A_34d_refcarry_0001": ROOT_DIR
    / "stages"
    / "35_candle_sidecar_simplification_check"
    / "02_runs"
    / "active"
    / "35A_34d_refcarry_0001",
    "35B_34b_simpleref_0001": ROOT_DIR
    / "stages"
    / "35_candle_sidecar_simplification_check"
    / "02_runs"
    / "active"
    / "35B_34b_simpleref_0001",
}
REFERENCE_RUN = "35A_34d_refcarry_0001"
SIMPLIFICATION_RUN = "35B_34b_simpleref_0001"
OUTPUT_JSON = STAGE_DIR / "03_reviews" / "stage36_outside_bar_localization_20260412.json"
OUTPUT_MD = STAGE_DIR / "03_reviews" / "stage36_outside_bar_localization_20260412.md"
SPLIT_ORDER = ["validation", "test", "hist_2024"]
NY_TZ = ZoneInfo("America/New_York")


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def parse_mt5_datetime(text: str) -> datetime:
    return datetime.strptime(text, "%Y.%m.%d %H:%M:%S")


def format_mt5_datetime(text: str | None) -> str:
    if not text:
        return "n/a"
    return parse_mt5_datetime(text).strftime("%Y-%m-%d %H:%M")


def fmt_num(value: float | int | None, digits: int = 2) -> str:
    if value is None:
        return "n/a"
    if isinstance(value, int):
        return str(value)
    return f"{value:.{digits}f}"


def entry_key(row: dict[str, object]) -> tuple[str, str, str]:
    return (
        str(row["entry_bar_time_server"]),
        str(row["direction"]),
        str(row["decision_at_entry"]),
    )


def argmax_label(p_short: float, p_flat: float, p_long: float) -> tuple[str, float]:
    pairs = [("short", p_short), ("flat", p_flat), ("long", p_long)]
    ordered = sorted(pairs, key=lambda item: item[1], reverse=True)
    margin = ordered[0][1] - ordered[1][1] if len(ordered) > 1 else 0.0
    return ordered[0][0], margin


def session_bucket(server_bar_time: str) -> str:
    ny_dt = parse_mt5_datetime(server_bar_time).replace(tzinfo=ZoneInfo("UTC")).astimezone(NY_TZ)
    minutes = ny_dt.hour * 60 + ny_dt.minute
    if minutes >= 16 * 60:
        return "ny_postcash"
    if minutes >= (9 * 60 + 30):
        return "ny_cash"
    return "other"


def weekday_name(server_bar_time: str) -> str:
    ny_dt = parse_mt5_datetime(server_bar_time).replace(tzinfo=ZoneInfo("UTC")).astimezone(NY_TZ)
    return ny_dt.strftime("%a")


def ny_time_label(server_bar_time: str) -> str:
    ny_dt = parse_mt5_datetime(server_bar_time).replace(tzinfo=ZoneInfo("UTC")).astimezone(NY_TZ)
    return ny_dt.strftime("%Y-%m-%d %H:%M")


def load_attempt_summaries(run_dir: Path) -> dict[str, dict]:
    out: dict[str, dict] = {}
    attempts_dir = run_dir / "mt5_attempts"
    for summary_path in sorted(attempts_dir.glob("att_*/tester_attempt_summary.json")):
        payload = load_json(summary_path)
        split_name = payload.get("split_name")
        if split_name:
            out[str(split_name)] = payload
    return out


def load_bundle_record(run_name: str, run_dir: Path) -> dict:
    bundle = load_json(run_dir / "experiment_bundle.json")
    return {
        "run_name": run_name,
        "experiment_id": bundle["identity"]["experiment_id"],
        "stage_id": bundle["identity"]["stage_id"],
        "results": bundle.get("results", {}).get("by_split", {}),
    }


def extract_split_metrics(bundle_record: dict, split_name: str) -> dict[str, float | int | None]:
    split = bundle_record["results"].get(split_name, {})
    headline = split.get("headline", {})
    risk = split.get("risk", {})
    diagnostics = split.get("diagnostics", {})
    return {
        "net_profit": headline.get("net_profit"),
        "return_pct": headline.get("return_pct"),
        "profit_factor": headline.get("profit_factor"),
        "max_dd_pct": risk.get("max_dd_pct"),
        "trade_count": headline.get("trade_count"),
        "long_expectancy": diagnostics.get("long_expectancy"),
        "short_expectancy": diagnostics.get("short_expectancy"),
    }


def load_trade_rows(path: Path) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            rows.append(
                {
                    "entry_bar_time_server": row["entry_bar_time_server"],
                    "exit_bar_time_server": row["exit_bar_time_server"],
                    "direction": row["direction"],
                    "decision_at_entry": row["decision_at_entry"],
                    "close_reason": row["close_reason"],
                    "hold_bars": int(row.get("hold_bars") or 0),
                    "volume": float(row.get("volume") or 0.0),
                    "exit_price": float(row.get("exit_price") or 0.0),
                    "risk_pct_multiplier_applied": float(row.get("risk_pct_multiplier_applied") or 0.0),
                    "initial_risk_amount": float(row.get("initial_risk_amount") or 0.0),
                    "net_profit": float(row.get("net_profit") or 0.0),
                }
            )
    return rows


def load_shadow_rows(path: Path) -> dict[str, dict[str, object]]:
    out: dict[str, dict[str, object]] = {}
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            p_short = float(row.get("p_short") or 0.0)
            p_flat = float(row.get("p_flat") or 0.0)
            p_long = float(row.get("p_long") or 0.0)
            argmax_class, argmax_margin = argmax_label(p_short, p_flat, p_long)
            out[row["bar_time_server"]] = {
                "bar_time_server": row["bar_time_server"],
                "decision_reason": row.get("decision_reason") or "",
                "trade_action_reason": row.get("trade_action_reason") or "",
                "floating_profit": float(row.get("floating_profit") or 0.0),
                "p_short": p_short,
                "p_flat": p_flat,
                "p_long": p_long,
                "argmax_class": argmax_class,
                "argmax_margin": argmax_margin,
            }
    return out


def pair_shifted_entries(
    only_a: list[dict[str, object]],
    only_b: list[dict[str, object]],
) -> tuple[list[dict[str, object]], list[dict[str, object]], list[dict[str, object]]]:
    paired: list[dict[str, object]] = []
    used_b: set[int] = set()

    for row_a in only_a:
        best_choice: tuple[tuple[float, int], int, dict[str, object]] | None = None
        row_a_dt = parse_mt5_datetime(str(row_a["entry_bar_time_server"]))
        for idx, row_b in enumerate(only_b):
            if idx in used_b or row_a["direction"] != row_b["direction"]:
                continue
            row_b_dt = parse_mt5_datetime(str(row_b["entry_bar_time_server"]))
            gap_minutes = abs((row_a_dt - row_b_dt).total_seconds()) / 60.0
            if gap_minutes > 5.0:
                continue
            sort_key = (gap_minutes, 0 if row_a["close_reason"] == row_b["close_reason"] else 1)
            if best_choice is None or sort_key < best_choice[0]:
                best_choice = (sort_key, idx, row_b)
        if best_choice is None:
            continue
        _, idx, row_b = best_choice
        used_b.add(idx)
        paired.append(
            {
                "direction": row_a["direction"],
                "entry_bar_time_35a": row_a["entry_bar_time_server"],
                "entry_bar_time_35b": row_b["entry_bar_time_server"],
                "close_reason_35a": row_a["close_reason"],
                "close_reason_35b": row_b["close_reason"],
                "net_profit_35a": row_a["net_profit"],
                "net_profit_35b": row_b["net_profit"],
                "net_profit_delta_35a_minus_35b": float(row_a["net_profit"]) - float(row_b["net_profit"]),
            }
        )

    paired_a_keys = {(item["entry_bar_time_35a"], item["direction"]) for item in paired}
    paired_b_keys = {(item["entry_bar_time_35b"], item["direction"]) for item in paired}
    rem_a = [row for row in only_a if (row["entry_bar_time_server"], row["direction"]) not in paired_a_keys]
    rem_b = [row for row in only_b if (row["entry_bar_time_server"], row["direction"]) not in paired_b_keys]
    return paired, rem_a, rem_b


def summarize_counter(items: list[dict[str, object]], field: str) -> dict[str, dict[str, float | int]]:
    grouped: dict[str, list[dict[str, object]]] = defaultdict(list)
    for item in items:
        grouped[str(item[field])].append(item)
    out: dict[str, dict[str, float | int]] = {}
    for key, rows in grouped.items():
        deltas = [float(row["net_profit_delta_35a_minus_35b"]) for row in rows]
        out[key] = {
            "count": len(rows),
            "positive_count": sum(delta > 0.0 for delta in deltas),
            "negative_count": sum(delta < 0.0 for delta in deltas),
            "net_profit_delta_35a_minus_35b": float(sum(deltas)),
        }
    return out


def build_split_analysis(
    split_name: str,
    ref_bundle: dict,
    simp_bundle: dict,
    ref_summary: dict,
    simp_summary: dict,
) -> dict[str, object]:
    ref_metrics = extract_split_metrics(ref_bundle, split_name)
    simp_metrics = extract_split_metrics(simp_bundle, split_name)
    ref_trade_rows = load_trade_rows(Path(ref_summary["trade_ledger_path"]))
    simp_trade_rows = load_trade_rows(Path(simp_summary["trade_ledger_path"]))
    ref_shadow_rows = load_shadow_rows(Path(ref_summary["csv_log_path"]))
    simp_shadow_rows = load_shadow_rows(Path(simp_summary["csv_log_path"]))

    ref_trade_map = {entry_key(row): row for row in ref_trade_rows}
    simp_trade_map = {entry_key(row): row for row in simp_trade_rows}
    common_keys = sorted(set(ref_trade_map) & set(simp_trade_map))

    structural_pairs: list[dict[str, object]] = []
    carry_pairs: list[dict[str, object]] = []
    pairs_by_simplification_exit_bar: dict[str, list[dict[str, object]]] = defaultdict(list)

    for key in common_keys:
        ref_row = ref_trade_map[key]
        simp_row = simp_trade_map[key]
        structural_changed = any(
            ref_row[field] != simp_row[field]
            for field in ["exit_bar_time_server", "close_reason", "hold_bars", "exit_price"]
        )
        pair = {
            "entry_bar_time_server": key[0],
            "direction": key[1],
            "ref": ref_row,
            "simp": simp_row,
            "net_profit_delta_35a_minus_35b": float(ref_row["net_profit"]) - float(simp_row["net_profit"]),
        }
        if structural_changed:
            structural_pairs.append(pair)
            pairs_by_simplification_exit_bar[str(simp_row["exit_bar_time_server"])].append(pair)
        elif float(ref_row["net_profit"]) != float(simp_row["net_profit"]):
            carry_pairs.append(pair)

    direct_events: list[dict[str, object]] = []
    for bar_time, shadow_row in sorted(ref_shadow_rows.items()):
        action_reason = str(shadow_row["trade_action_reason"])
        if "STATE_EXIT_SUPPRESSED_OUTSIDE_BAR" not in action_reason:
            continue
        candidate_pairs = [
            pair
            for pair in pairs_by_simplification_exit_bar.get(bar_time, [])
            if str(pair["ref"]["exit_bar_time_server"]) != bar_time
        ]
        if len(candidate_pairs) != 1:
            raise RuntimeError(f"expected exactly one direct event match for {split_name} {bar_time}, got {len(candidate_pairs)}")
        pair = candidate_pairs[0]
        ref_row = pair["ref"]
        simp_row = pair["simp"]
        direct_events.append(
            {
                "split": split_name,
                "direction": ref_row["direction"],
                "entry_bar_time_server": ref_row["entry_bar_time_server"],
                "suppressed_bar_time_server": bar_time,
                "suppressed_bar_time_ny": ny_time_label(bar_time),
                "weekday_ny": weekday_name(bar_time),
                "session_bucket_ny": session_bucket(bar_time),
                "decision_reason": shadow_row["decision_reason"],
                "trade_action_reason_35a": shadow_row["trade_action_reason"],
                "trade_action_reason_35b": simp_shadow_rows[bar_time]["trade_action_reason"],
                "floating_profit_at_suppression": shadow_row["floating_profit"],
                "argmax_class": shadow_row["argmax_class"],
                "argmax_margin": shadow_row["argmax_margin"],
                "p_short": shadow_row["p_short"],
                "p_flat": shadow_row["p_flat"],
                "p_long": shadow_row["p_long"],
                "exit_bar_time_35a": ref_row["exit_bar_time_server"],
                "exit_bar_time_35b": simp_row["exit_bar_time_server"],
                "exit_close_reason_35a": ref_row["close_reason"],
                "exit_close_reason_35b": simp_row["close_reason"],
                "hold_bars_35a": ref_row["hold_bars"],
                "hold_bars_35b": simp_row["hold_bars"],
                "later_exit_delay_bars": int(ref_row["hold_bars"]) - int(simp_row["hold_bars"]),
                "net_profit_35a": ref_row["net_profit"],
                "net_profit_35b": simp_row["net_profit"],
                "net_profit_delta_35a_minus_35b": pair["net_profit_delta_35a_minus_35b"],
            }
        )

    only_ref = [ref_trade_map[key] for key in sorted(set(ref_trade_map) - set(simp_trade_map))]
    only_simp = [simp_trade_map[key] for key in sorted(set(simp_trade_map) - set(ref_trade_map))]
    shifted_pairs, residual_ref, residual_simp = pair_shifted_entries(only_ref, only_simp)

    headline_delta_net = float(ref_metrics["net_profit"] or 0.0) - float(simp_metrics["net_profit"] or 0.0)
    direct_delta_net = float(sum(item["net_profit_delta_35a_minus_35b"] for item in direct_events))
    carry_delta_net = float(sum(item["net_profit_delta_35a_minus_35b"] for item in carry_pairs))
    shifted_delta_net = float(sum(item["net_profit_delta_35a_minus_35b"] for item in shifted_pairs))
    residual_unmatched_delta_net = float(sum(float(row["net_profit"]) for row in residual_ref) - sum(float(row["net_profit"]) for row in residual_simp))

    return {
        "split": split_name,
        "headline_delta_35a_minus_35b": {
            "net_profit": headline_delta_net,
            "return_pct": float(ref_metrics["return_pct"] or 0.0) - float(simp_metrics["return_pct"] or 0.0),
            "profit_factor": float(ref_metrics["profit_factor"] or 0.0) - float(simp_metrics["profit_factor"] or 0.0),
            "max_dd_pct": float(ref_metrics["max_dd_pct"] or 0.0) - float(simp_metrics["max_dd_pct"] or 0.0),
            "trade_count_delta": int(ref_metrics["trade_count"] or 0) - int(simp_metrics["trade_count"] or 0),
            "long_expectancy_delta": float(ref_metrics["long_expectancy"] or 0.0) - float(simp_metrics["long_expectancy"] or 0.0),
            "short_expectancy_delta": float(ref_metrics["short_expectancy"] or 0.0) - float(simp_metrics["short_expectancy"] or 0.0),
        },
        "decomposition": {
            "direct_suppression_event_count": len(direct_events),
            "direct_suppression_positive_count": sum(item["net_profit_delta_35a_minus_35b"] > 0.0 for item in direct_events),
            "direct_suppression_negative_count": sum(item["net_profit_delta_35a_minus_35b"] < 0.0 for item in direct_events),
            "direct_suppression_net_profit_delta_35a_minus_35b": direct_delta_net,
            "shifted_entry_count": len(shifted_pairs),
            "shifted_entry_net_profit_delta_35a_minus_35b": shifted_delta_net,
            "carry_drift_trade_count": len(carry_pairs),
            "carry_drift_net_profit_delta_35a_minus_35b": carry_delta_net,
            "residual_unmatched_net_profit_delta_35a_minus_35b": residual_unmatched_delta_net,
            "direct_share_of_headline_net_delta": None if abs(headline_delta_net) < 1e-9 else direct_delta_net / headline_delta_net,
        },
        "context_breakdowns": {
            "decision_reason": summarize_counter(direct_events, "decision_reason"),
            "session_bucket_ny": summarize_counter(direct_events, "session_bucket_ny"),
            "weekday_ny": summarize_counter(direct_events, "weekday_ny"),
            "exit_transition": summarize_counter(
                [
                    {
                        "exit_transition": f"{item['exit_close_reason_35b']} -> {item['exit_close_reason_35a']}",
                        "net_profit_delta_35a_minus_35b": item["net_profit_delta_35a_minus_35b"],
                    }
                    for item in direct_events
                ],
                "exit_transition",
            ),
        },
        "direct_events": sorted(direct_events, key=lambda item: abs(float(item["net_profit_delta_35a_minus_35b"])), reverse=True),
        "shifted_entry_pairs": shifted_pairs,
    }


def build_markdown(payload: dict) -> str:
    split_summaries = payload["split_summaries"]
    overall = payload["overall_localization"]
    lines = [
        "# Stage 36 Outside Bar Localization Review",
        "",
        f"- reviewed_on: `{payload['reviewed_on']}`",
        f"- stage: `36_outside_bar_localization_diagnostic`",
        f"- reference_line: `{payload['reference_run']}`",
        f"- simplification_shadow: `{payload['simplification_run']}`",
        "",
        "## Executive Read",
        "",
        "- the remaining `34D` edge is sparse and direct rather than broad and diffuse",
        f"- direct outside-bar suppressions fired only `{overall['direct_event_count']}` times across all three Stage 35 comparison splits",
        f"- all direct events were `{overall['direction_summary']}` and all held the trade exactly `{overall['delay_bar_summary']}` extra bar",
        f"- the current `test` window had `{split_summaries['test']['decomposition']['direct_suppression_event_count']}` qualifying events, so the sidecar did not shape the test read because it never fired there",
        f"- `hist_2024` carried the real value: direct suppressions explain `{fmt_num(split_summaries['hist_2024']['decomposition']['direct_suppression_net_profit_delta_35a_minus_35b'])}` of the `{fmt_num(split_summaries['hist_2024']['headline_delta_35a_minus_35b']['net_profit'])}` net-profit edge",
        "",
        "## Split Decomposition",
        "",
    ]

    for split_name in SPLIT_ORDER:
        split = split_summaries[split_name]
        headline = split["headline_delta_35a_minus_35b"]
        decomp = split["decomposition"]
        lines.append(f"### {split_name}")
        lines.append("")
        lines.append(
            f"- headline `35A minus 35B`: `net={fmt_num(headline['net_profit'])}` `return_pct={fmt_num(headline['return_pct'], 3)}` "
            f"`pf={fmt_num(headline['profit_factor'], 4)}` `dd_pct={fmt_num(headline['max_dd_pct'], 4)}`"
        )
        lines.append(
            f"- direct suppressions: `count={decomp['direct_suppression_event_count']}` "
            f"`net={fmt_num(decomp['direct_suppression_net_profit_delta_35a_minus_35b'])}` "
            f"`positive={decomp['direct_suppression_positive_count']}` `negative={decomp['direct_suppression_negative_count']}`"
        )
        lines.append(
            f"- residual path effects: `shifted_entry={fmt_num(decomp['shifted_entry_net_profit_delta_35a_minus_35b'])}` "
            f"`carry_drift={fmt_num(decomp['carry_drift_net_profit_delta_35a_minus_35b'])}` "
            f"`carry_trade_count={decomp['carry_drift_trade_count']}`"
        )
        if split["shifted_entry_pairs"]:
            shifted = split["shifted_entry_pairs"][0]
            lines.append(
                f"- shifted-entry note: `35B` re-entered `{shifted['direction']}` at `{format_mt5_datetime(shifted['entry_bar_time_35b'])}`, "
                f"while `35A` entered one bar later at `{format_mt5_datetime(shifted['entry_bar_time_35a'])}`"
            )
        lines.append("")

    lines.extend(
        [
            "## Direct Event Context",
            "",
            f"- decision reason breakdown: `DUAL_SIGNAL_TIE_OR_MARGIN_FAIL={overall['decision_reason_breakdown'].get('DUAL_SIGNAL_TIE_OR_MARGIN_FAIL', {}).get('count', 0)}` "
            f"`LONG_MARGIN_FAIL={overall['decision_reason_breakdown'].get('LONG_MARGIN_FAIL', {}).get('count', 0)}`",
            f"- session breakdown: `ny_cash={overall['session_breakdown'].get('ny_cash', {}).get('count', 0)}` "
            f"`ny_postcash={overall['session_breakdown'].get('ny_postcash', {}).get('count', 0)}`",
            f"- weekday breakdown: `Mon={overall['weekday_breakdown'].get('Mon', {}).get('count', 0)}` "
            f"`Tue={overall['weekday_breakdown'].get('Tue', {}).get('count', 0)}` "
            f"`Wed={overall['weekday_breakdown'].get('Wed', {}).get('count', 0)}` "
            f"`Thu={overall['weekday_breakdown'].get('Thu', {}).get('count', 0)}` "
            f"`Fri={overall['weekday_breakdown'].get('Fri', {}).get('count', 0)}`",
            f"- later-close shape: `STATE_EXIT_MARGIN -> STATE_EXIT_MARGIN={overall['exit_transition_breakdown'].get('STATE_EXIT_MARGIN -> STATE_EXIT_MARGIN', {}).get('count', 0)}` "
            f"`STATE_EXIT_MARGIN -> TIME_EXIT_NY_POSTCASH={overall['exit_transition_breakdown'].get('STATE_EXIT_MARGIN -> TIME_EXIT_NY_POSTCASH', {}).get('count', 0)}`",
            "",
            "## Highest-Impact Direct Events",
            "",
        ]
    )

    for event in payload["top_direct_events"]:
        lines.append(
            f"- `{event['split']}` `{format_mt5_datetime(event['suppressed_bar_time_server'])}` `{event['direction']}`: "
            f"`delta={fmt_num(event['net_profit_delta_35a_minus_35b'])}` "
            f"`35B_exit={event['exit_close_reason_35b']}` `35A_exit={event['exit_close_reason_35a']}` "
            f"`ny={event['weekday_ny']} {event['suppressed_bar_time_ny'].split(' ')[1]}`"
        )
    lines.append("")
    lines.extend(
        [
            "## Decision Bias",
            "",
            "- keep `34D` unchanged; the sidecar value is real even though it is sparse",
            "- do not reopen the closed `remove the sidecar entirely` simplification path; this stage shows exactly why the broad removal lost the older-window edge",
            "- if simplification reopens later, target a narrower filter around the long no-entry state-exit subset rather than day-of-week rules or a full sidecar rollback",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    bundle_records = {
        run_name: load_bundle_record(run_name, run_dir)
        for run_name, run_dir in RUN_DIRS.items()
    }
    attempt_summaries = {
        run_name: load_attempt_summaries(run_dir)
        for run_name, run_dir in RUN_DIRS.items()
    }

    split_summaries = {
        split_name: build_split_analysis(
            split_name,
            bundle_records[REFERENCE_RUN],
            bundle_records[SIMPLIFICATION_RUN],
            attempt_summaries[REFERENCE_RUN][split_name],
            attempt_summaries[SIMPLIFICATION_RUN][split_name],
        )
        for split_name in SPLIT_ORDER
    }

    all_direct_events = [
        event
        for split_name in SPLIT_ORDER
        for event in split_summaries[split_name]["direct_events"]
    ]
    all_delay_bars = sorted({int(event["later_exit_delay_bars"]) for event in all_direct_events})
    overall = {
        "direct_event_count": len(all_direct_events),
        "direction_summary": "/".join(sorted({str(event["direction"]) for event in all_direct_events})) if all_direct_events else "n/a",
        "delay_bar_summary": ", ".join(str(value) for value in all_delay_bars) if all_delay_bars else "n/a",
        "decision_reason_breakdown": summarize_counter(all_direct_events, "decision_reason"),
        "session_breakdown": summarize_counter(all_direct_events, "session_bucket_ny"),
        "weekday_breakdown": summarize_counter(all_direct_events, "weekday_ny"),
        "exit_transition_breakdown": summarize_counter(
            [
                {
                    "exit_transition": f"{event['exit_close_reason_35b']} -> {event['exit_close_reason_35a']}",
                    "net_profit_delta_35a_minus_35b": event["net_profit_delta_35a_minus_35b"],
                }
                for event in all_direct_events
            ],
            "exit_transition",
        ),
    }

    payload = {
        "reviewed_on": "2026-04-12",
        "reference_run": REFERENCE_RUN,
        "simplification_run": SIMPLIFICATION_RUN,
        "split_summaries": split_summaries,
        "overall_localization": overall,
        "top_direct_events": sorted(
            all_direct_events,
            key=lambda item: abs(float(item["net_profit_delta_35a_minus_35b"])),
            reverse=True,
        )[:5],
    }
    write_json(OUTPUT_JSON, payload)
    write_text(OUTPUT_MD, build_markdown(payload))
    print(f"[done] wrote={OUTPUT_JSON}")
    print(f"[done] wrote={OUTPUT_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
