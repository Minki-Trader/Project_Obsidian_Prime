#!/usr/bin/env python3
from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[3]
STAGE_DIR = ROOT_DIR / "stages" / "38_prelive_evidence_pack"
STAGE38_JSON = STAGE_DIR / "03_reviews" / "stage38_prelive_evidence_20260413.json"
STAGE39_JSON = ROOT_DIR / "stages" / "39_window_extension_mt5_validation" / "03_reviews" / "stage39_extended_validation_20260413.json"
OUTPUT_JSON = STAGE_DIR / "03_reviews" / "stage38_visual_panels_20260413.json"
OUTPUT_MD = STAGE_DIR / "03_reviews" / "stage38_visual_panels_20260413.md"
SPLIT_ORDER = ["hist_2024", "validation", "test"]


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def fmt_num(value: float | int | None, digits: int = 3) -> str:
    if value is None:
        return "n/a"
    if isinstance(value, int):
        return str(value)
    return f"{value:.{digits}f}"


def summarize_events(events: list[dict]) -> tuple[dict[str, dict[str, float | int]], dict[str, dict[str, float | int]], dict[str, int]]:
    split_summary: dict[str, dict[str, float | int]] = defaultdict(lambda: {"count": 0, "net_delta": 0.0})
    session_summary: dict[str, dict[str, float | int]] = defaultdict(lambda: {"count": 0, "net_delta": 0.0})
    reason_counts: dict[str, int] = defaultdict(int)
    for event in events:
        delta = float(event["net_profit_delta_35a_minus_35b"])
        split_summary[event["split"]]["count"] += 1
        split_summary[event["split"]]["net_delta"] += delta
        session_summary[event["session_bucket_ny"]]["count"] += 1
        session_summary[event["session_bucket_ny"]]["net_delta"] += delta
        reason_counts[event["decision_reason"]] += 1
    return dict(split_summary), dict(session_summary), dict(reason_counts)


def build_critical_event_rows(events: list[dict]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for rank, event in enumerate(
        sorted(events, key=lambda item: abs(float(item["net_profit_delta_35a_minus_35b"])), reverse=True),
        start=1,
    ):
        context = event["feature_context_at_trigger_bar"]
        trigger = event["trigger_bar_shape"]
        rows.append(
            {
                "rank": rank,
                "split": event["split"],
                "suppressed_bar_time_server": event["suppressed_bar_time_server"],
                "trigger_bar_time_server": event["trigger_bar_time_server"],
                "delta_34d_minus_34b": float(event["net_profit_delta_35a_minus_35b"]),
                "decision_reason": event["decision_reason"],
                "session_bucket_ny": event["session_bucket_ny"],
                "atr_bucket": event["atr_bucket"],
                "atr_ratio": context.get("atr_14_over_atr_50"),
                "vix_change_1": context.get("vix_change_1"),
                "us10yr_change_1": context.get("us10yr_change_1"),
                "float_at_suppression": event["floating_profit_at_suppression"],
                "trigger_range_points": trigger.get("range_points"),
                "trigger_body_points": trigger.get("body_points"),
                "trigger_body_to_range": trigger.get("body_to_range"),
                "outside_prev": trigger.get("outside_prev"),
                "direction": trigger.get("direction"),
                "external_exact_match_at_trigger_bar": event["external_exact_match_at_trigger_bar"],
            }
        )
    return rows


def build_delta_explanation(stage38: dict, stage39: dict) -> dict[str, object]:
    stage34 = stage38["value_attribution"]["stage34_decomposition"]["by_split"]
    stage35_36 = stage38["value_attribution"]["stage35_and_36"]["by_split"]
    stage37 = stage38["value_attribution"]["stage37_continuity"]
    stage39_delta = stage39["delta"]
    return {
        "stage34_decomposition": stage34,
        "stage35_36_split_reset": stage35_36,
        "stage37_continuous_bridge": {
            "bridge_window": stage37["bridge_window"],
            "bridge_delta": stage37["bridge_delta"],
            "year_buckets": stage37["year_buckets"],
        },
        "stage39_extended_bridge": {
            "extended_window": stage39["extended_window"],
            "bridge_delta": stage39_delta,
        },
        "operating_message": [
            "34B explains the governance-only carry in the current windows.",
            "34C explains the older-window rescue driven by the long outside-bar pocket.",
            "34D stays ahead because it keeps both pieces without widening trade count.",
        ],
    }


def build_payload(stage38: dict, stage39: dict) -> dict[str, object]:
    events = stage38["event_evidence"]["events"]
    split_summary, session_summary, reason_counts = summarize_events(events)
    critical_rows = build_critical_event_rows(events)
    return {
        "reviewed_on": stage39["reviewed_on"],
        "critical_protection_panel": {
            "headline": {
                "direct_event_count": stage38["event_evidence"]["direct_event_count"],
                "direct_net_profit_delta_total": stage38["event_evidence"]["direct_net_profit_delta_total"],
                "headline_net_profit_delta_total": stage38["event_evidence"]["headline_net_profit_delta_total"],
                "direct_share_of_headline_net_delta_total": stage38["event_evidence"]["direct_share_of_headline_net_delta_total"],
            },
            "split_summary": split_summary,
            "session_summary": session_summary,
            "decision_reason_counts": reason_counts,
            "ranked_events": critical_rows,
        },
        "delta_explanation_panel": build_delta_explanation(stage38, stage39),
        "report_inputs": {
            "stage38_review": str(STAGE38_JSON),
            "stage39_review": str(STAGE39_JSON),
        },
    }


def build_markdown(payload: dict) -> str:
    critical = payload["critical_protection_panel"]
    delta = payload["delta_explanation_panel"]
    lines = [
        "# Stage 38 Visual Panels",
        "",
        f"- reviewed_on: `{payload['reviewed_on']}`",
        "- stage: `38_prelive_evidence_pack`",
        "- purpose: `copy_ready_panels_for_live_packet_or_external_model_briefing`",
        "",
        "## Panel 1. Critical Protection Events",
        "",
        "1. Headline concentration.",
        f"- `events={critical['headline']['direct_event_count']}` `direct_net={fmt_num(critical['headline']['direct_net_profit_delta_total'])}` "
        f"`headline_net={fmt_num(critical['headline']['headline_net_profit_delta_total'])}` "
        f"`share={fmt_num(critical['headline']['direct_share_of_headline_net_delta_total'], 4)}`",
        "2. Split concentration.",
    ]
    for split_name in SPLIT_ORDER:
        summary = critical["split_summary"].get(split_name, {"count": 0, "net_delta": 0.0})
        lines.append(
            f"- `{split_name}` `count={summary['count']}` `net_delta={fmt_num(summary['net_delta'])}`"
        )
    lines.extend(
        [
            "3. Session concentration.",
            f"- `ny_cash` `count={critical['session_summary'].get('ny_cash', {}).get('count', 0)}` "
            f"`net_delta={fmt_num(critical['session_summary'].get('ny_cash', {}).get('net_delta'))}`",
            f"- `ny_postcash` `count={critical['session_summary'].get('ny_postcash', {}).get('count', 0)}` "
            f"`net_delta={fmt_num(critical['session_summary'].get('ny_postcash', {}).get('net_delta'))}`",
            "4. Trigger reasons.",
        ]
    )
    for reason, count in sorted(critical["decision_reason_counts"].items(), key=lambda item: (-item[1], item[0])):
        lines.append(f"- `{reason}` `count={count}`")
    lines.append("5. Ranked critical bars.")
    for event in critical["ranked_events"]:
        exact = event["external_exact_match_at_trigger_bar"]
        lines.append(
            f"- `{event['rank']}` `{event['split']}` `{event['suppressed_bar_time_server']}` "
            f"`delta={fmt_num(event['delta_34d_minus_34b'])}` `reason={event['decision_reason']}` "
            f"`session={event['session_bucket_ny']}` `atr_ratio={fmt_num(event['atr_ratio'], 4)}` "
            f"`range={fmt_num(event['trigger_range_points'], 2)}` `body={fmt_num(event['trigger_body_points'], 2)}` "
            f"`float={fmt_num(event['float_at_suppression'], 3)}`"
        )
        lines.append(
            f"- trigger `outside_prev={event['outside_prev']}` `direction={event['direction']}` "
            f"`VIX={exact.get('VIX')}` `US10YR={exact.get('US10YR')}` `USDX={exact.get('USDX')}`"
        )
    lines.extend(
        [
            "",
            "## Panel 2. 34B vs 34D Delta Explanation",
            "",
            "1. Stage 34 decomposition.",
        ]
    )
    for split_name in ["validation", "test", "hist_2024"]:
        item = delta["stage34_decomposition"][split_name]
        lines.append(
            f"- `{split_name}` `34B-29N={fmt_num(item['governance_only_return_delta_34b_minus_29n'])}` "
            f"`34C-29N={fmt_num(item['outbar_only_return_delta_34c_minus_29n'])}` "
            f"`34D-29N={fmt_num(item['combined_return_delta_34d_minus_29n'])}` "
            f"`34D-34B={fmt_num(item['incremental_outbar_on_governance_34d_minus_34b'])}`"
        )
    lines.append("2. Stage 35 and Stage 36 split-reset attribution.")
    for split_name in ["validation", "test", "hist_2024"]:
        item = delta["stage35_36_split_reset"][split_name]
        lines.append(
            f"- `{split_name}` `return_delta={fmt_num(item['return_pct_delta_34d_minus_34b'])}` "
            f"`pf_delta={fmt_num(item['profit_factor_delta_34d_minus_34b'], 4)}` "
            f"`dd_delta={fmt_num(item['max_dd_pct_delta_34d_minus_34b'], 4)}` "
            f"`direct_events={item['direct_suppression_event_count']}` "
            f"`direct_net={fmt_num(item['direct_suppression_net_profit_delta_34d_minus_34b'])}`"
        )
    stage37 = delta["stage37_continuous_bridge"]
    lines.append("3. Stage 37 continuous bridge.")
    lines.append(
        f"- window `{stage37['bridge_window']}` "
        f"`net={fmt_num(stage37['bridge_delta']['net_profit_delta_34d_minus_34b'])}` "
        f"`return_pct={fmt_num(stage37['bridge_delta']['return_pct_delta_34d_minus_34b'])}` "
        f"`pf={fmt_num(stage37['bridge_delta']['profit_factor_delta_34d_minus_34b'], 4)}` "
        f"`dd_pct={fmt_num(stage37['bridge_delta']['max_dd_pct_delta_34d_minus_34b'], 4)}` "
        f"`ulcer={fmt_num(stage37['bridge_delta']['ulcer_index_delta_34d_minus_34b'], 4)}`"
    )
    for year_name in ["2024", "2025", "2026_ytd"]:
        bucket = stage37["year_buckets"][year_name]
        lines.append(
            f"- `{year_name}` `net_delta={fmt_num(bucket['net_profit_delta'])}` `trade_delta={bucket['trade_count_delta']}`"
        )
    stage39 = delta["stage39_extended_bridge"]
    lines.append("4. Stage 39 extended bridge.")
    lines.append(
        f"- window `{stage39['extended_window']}` `net={fmt_num(stage39['bridge_delta']['net_profit_delta'])}` "
        f"`return_pct={fmt_num(stage39['bridge_delta']['return_pct_delta'])}` "
        f"`pf={fmt_num(stage39['bridge_delta']['profit_factor_delta'], 4)}` "
        f"`dd_pct={fmt_num(stage39['bridge_delta']['max_dd_pct_delta'], 4)}` "
        f"`ulcer={fmt_num(stage39['bridge_delta']['ulcer_index_delta'], 4)}`"
    )
    for year_name in ["2024", "2025", "2026_ytd"]:
        bucket = stage39["bridge_delta"]["year_buckets"][year_name]
        lines.append(
            f"- `{year_name}` `net_delta={fmt_num(bucket['net_profit_delta'])}` `trade_delta={bucket['trade_count_delta']}`"
        )
    lines.append("5. Operating message.")
    for sentence in delta["operating_message"]:
        lines.append(f"- {sentence}")
    return "\n".join(lines) + "\n"


def main() -> None:
    stage38 = load_json(STAGE38_JSON)
    stage39 = load_json(STAGE39_JSON)
    payload = build_payload(stage38, stage39)
    write_json(OUTPUT_JSON, payload)
    write_text(OUTPUT_MD, build_markdown(payload))


if __name__ == "__main__":
    main()
