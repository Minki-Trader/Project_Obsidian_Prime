from __future__ import annotations

import csv
import json
from collections import Counter, defaultdict
from dataclasses import dataclass
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
    },
    "22B": {
        "label": "break_even",
        "run_dir": STAGE_DIR / "02_runs" / "active" / "22B_05dp_be50_lock10_0001",
    },
    "22C": {
        "label": "trailing_stop",
        "run_dir": STAGE_DIR / "02_runs" / "active" / "22C_05dp_trail60_dist35_0001",
    },
    "22D": {
        "label": "partial_stop_loss",
        "run_dir": STAGE_DIR / "02_runs" / "active" / "22D_05dp_psl45_half_0001",
    },
    "22E": {
        "label": "partial_take_profit",
        "run_dir": STAGE_DIR / "02_runs" / "active" / "22E_05dp_ptp60_half_0001",
    },
}

SPLITS = {
    "hist_2024": "2024 historical",
    "val_2501": "2025 validation Jan-Sep",
    "oos_2501": "2501 OOS",
}

POSITION_EVENT_REASONS = {
    "22B": "BREAK_EVEN_STOP",
    "22C": "TRAIL_STOP",
    "22D": "PARTIAL_STOP_LOSS",
    "22E": "PARTIAL_TAKE_PROFIT",
}


def parse_float(value: str) -> float | None:
    if value is None:
        return None
    text = value.strip()
    if not text:
        return None
    try:
        return float(text)
    except ValueError:
        return None


def parse_int(value: str) -> int | None:
    if value is None:
        return None
    text = value.strip()
    if not text:
        return None
    try:
        return int(text)
    except ValueError:
        return None


def percentile(sorted_values: list[float], quantile: float) -> float | None:
    if not sorted_values:
        return None
    if len(sorted_values) == 1:
        return sorted_values[0]
    pos = (len(sorted_values) - 1) * quantile
    lower = int(pos)
    upper = min(lower + 1, len(sorted_values) - 1)
    frac = pos - lower
    return sorted_values[lower] + (sorted_values[upper] - sorted_values[lower]) * frac


def sum_ignore_none(values: list[float | None]) -> float:
    return sum(v for v in values if v is not None)


@dataclass
class PositionRecord:
    position_id: str
    match_key: str
    direction: str
    entry_bar_time_server: str
    entry_time_server: str
    exit_bar_time_server: str
    exit_time_server: str
    hold_bars: int
    row_count: int
    closed_volume: float
    total_net_profit: float
    total_gross_profit: float
    max_row_max_floating_profit: float | None
    min_row_min_floating_profit: float | None
    close_reason_path: list[str]
    close_reason_counts: dict[str, int]
    has_break_even_stop: bool
    has_trail_stop: bool
    has_partial_stop_loss: bool
    has_partial_take_profit: bool

    @property
    def has_partial_event(self) -> bool:
        return self.has_partial_stop_loss or self.has_partial_take_profit


def load_attempt_summaries(run_dir: Path) -> dict[str, dict[str, Any]]:
    summaries: dict[str, dict[str, Any]] = {}
    for path in sorted((run_dir / "mt5_attempts").glob("att_*/*tester_attempt_summary.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        split_name = data.get("split_name")
        if split_name not in SPLITS:
            continue
        current = summaries.get(split_name)
        if current is None or path.name > current["_summary_path"].name:
            data["_summary_path"] = path
            summaries[split_name] = data
    missing = [split for split in SPLITS if split not in summaries]
    if missing:
        raise FileNotFoundError(f"missing stage22 attempt summaries for {run_dir}: {missing}")
    return summaries


def load_positions(trade_ledger_path: Path) -> dict[str, PositionRecord]:
    grouped_rows: dict[str, list[dict[str, str]]] = defaultdict(list)
    with trade_ledger_path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            position_id = row["position_identifier"] or row["position_ticket"]
            grouped_rows[position_id].append(row)

    positions: dict[str, PositionRecord] = {}
    for position_id, rows in grouped_rows.items():
        rows.sort(
            key=lambda row: (
                row["exit_time_server"],
                row["event_timestamp_gmt"],
                row["close_reason"],
            )
        )
        first = rows[0]
        last = rows[-1]
        reason_counter = Counter(row["close_reason"] for row in rows)
        close_reason_path = [row["close_reason"] for row in rows]
        entry_bar_time = first["entry_bar_time_server"]
        direction = first["direction"]
        match_key = f"{entry_bar_time}|{direction}"
        max_float_values = [parse_float(row["max_floating_profit"]) for row in rows]
        min_float_values = [parse_float(row["min_floating_profit"]) for row in rows]
        positions[match_key] = PositionRecord(
            position_id=position_id,
            match_key=match_key,
            direction=direction,
            entry_bar_time_server=entry_bar_time,
            entry_time_server=first["entry_time_server"],
            exit_bar_time_server=last["exit_bar_time_server"],
            exit_time_server=last["exit_time_server"],
            hold_bars=parse_int(last["hold_bars"]) or 0,
            row_count=len(rows),
            closed_volume=sum_ignore_none([parse_float(row["volume"]) for row in rows]),
            total_net_profit=sum_ignore_none([parse_float(row["net_profit"]) for row in rows]),
            total_gross_profit=sum_ignore_none([parse_float(row["gross_profit"]) for row in rows]),
            max_row_max_floating_profit=max(
                (value for value in max_float_values if value is not None),
                default=None,
            ),
            min_row_min_floating_profit=min(
                (value for value in min_float_values if value is not None),
                default=None,
            ),
            close_reason_path=close_reason_path,
            close_reason_counts=dict(reason_counter),
            has_break_even_stop="BREAK_EVEN_STOP" in reason_counter,
            has_trail_stop="TRAIL_STOP" in reason_counter,
            has_partial_stop_loss="PARTIAL_STOP_LOSS" in reason_counter,
            has_partial_take_profit="PARTIAL_TAKE_PROFIT" in reason_counter,
        )
    return positions


def q75_positive(values: list[float]) -> float | None:
    positives = sorted(value for value in values if value > 0.0)
    return percentile(positives, 0.75)


def q25_negative(values: list[float]) -> float | None:
    negatives = sorted(value for value in values if value < 0.0)
    return percentile(negatives, 0.25)


def summarize_positions(positions: dict[str, PositionRecord]) -> dict[str, Any]:
    position_list = list(positions.values())
    close_reason_counter = Counter()
    for position in position_list:
        close_reason_counter.update(position.close_reason_counts)
    return {
        "position_count": len(position_list),
        "ledger_row_count": sum(position.row_count for position in position_list),
        "position_level_net_profit": round(sum(position.total_net_profit for position in position_list), 3),
        "position_level_gross_profit": round(sum(position.total_gross_profit for position in position_list), 3),
        "mean_hold_bars": round(
            sum(position.hold_bars for position in position_list) / len(position_list), 4
        )
        if position_list
        else None,
        "partial_affected_positions": sum(1 for position in position_list if position.has_partial_event),
        "break_even_positions": sum(1 for position in position_list if position.has_break_even_stop),
        "trail_positions": sum(1 for position in position_list if position.has_trail_stop),
        "close_reason_breakdown": dict(close_reason_counter),
    }


def compare_variant_to_baseline(
    baseline_positions: dict[str, PositionRecord],
    variant_positions: dict[str, PositionRecord],
    variant_code: str,
) -> dict[str, Any]:
    baseline_keys = set(baseline_positions)
    variant_keys = set(variant_positions)
    matched_keys = sorted(baseline_keys & variant_keys)
    baseline_only_keys = sorted(baseline_keys - variant_keys)
    variant_only_keys = sorted(variant_keys - baseline_keys)

    baseline_profit_values = [position.total_net_profit for position in baseline_positions.values()]
    baseline_big_winner_threshold = q75_positive(baseline_profit_values)
    baseline_deep_loser_threshold = q25_negative(baseline_profit_values)

    event_reason = POSITION_EVENT_REASONS.get(variant_code)

    matched_delta_values: list[float] = []
    improved_count = 0
    worsened_count = 0
    unchanged_count = 0
    baseline_winner_count = 0
    baseline_loser_count = 0
    winner_clip_count = 0
    winner_flip_to_loss_count = 0
    loser_mitigated_count = 0
    loser_flip_to_profit_count = 0
    big_winner_count = 0
    big_winner_clip_count = 0
    deep_loser_count = 0
    deep_loser_mitigated_count = 0
    event_position_count = 0
    event_on_baseline_winner_count = 0
    event_on_baseline_loser_count = 0

    for match_key in matched_keys:
        baseline_position = baseline_positions[match_key]
        variant_position = variant_positions[match_key]
        delta = variant_position.total_net_profit - baseline_position.total_net_profit
        matched_delta_values.append(delta)

        if delta > 0.01:
            improved_count += 1
        elif delta < -0.01:
            worsened_count += 1
        else:
            unchanged_count += 1

        is_winner = baseline_position.total_net_profit > 0.0
        is_loser = baseline_position.total_net_profit < 0.0
        if is_winner:
            baseline_winner_count += 1
            if delta < -0.01:
                winner_clip_count += 1
            if variant_position.total_net_profit <= 0.0:
                winner_flip_to_loss_count += 1
        if is_loser:
            baseline_loser_count += 1
            if delta > 0.01:
                loser_mitigated_count += 1
            if variant_position.total_net_profit >= 0.0:
                loser_flip_to_profit_count += 1

        if baseline_big_winner_threshold is not None and baseline_position.total_net_profit >= baseline_big_winner_threshold:
            big_winner_count += 1
            if delta < -0.01:
                big_winner_clip_count += 1

        if baseline_deep_loser_threshold is not None and baseline_position.total_net_profit <= baseline_deep_loser_threshold:
            deep_loser_count += 1
            if delta > 0.01:
                deep_loser_mitigated_count += 1

        if event_reason and event_reason in variant_position.close_reason_counts:
            event_position_count += 1
            if is_winner:
                event_on_baseline_winner_count += 1
            if is_loser:
                event_on_baseline_loser_count += 1

    matched_baseline_profit = sum(baseline_positions[key].total_net_profit for key in matched_keys)
    matched_variant_profit = sum(variant_positions[key].total_net_profit for key in matched_keys)
    baseline_only_profit = sum(baseline_positions[key].total_net_profit for key in baseline_only_keys)
    variant_only_profit = sum(variant_positions[key].total_net_profit for key in variant_only_keys)

    return {
        "matched_position_count": len(matched_keys),
        "baseline_overlap_rate": round(len(matched_keys) / len(baseline_keys), 4) if baseline_keys else None,
        "variant_overlap_rate": round(len(matched_keys) / len(variant_keys), 4) if variant_keys else None,
        "baseline_only_position_count": len(baseline_only_keys),
        "variant_only_position_count": len(variant_only_keys),
        "matched_profit_delta": round(matched_variant_profit - matched_baseline_profit, 3),
        "baseline_only_profit": round(baseline_only_profit, 3),
        "variant_only_profit": round(variant_only_profit, 3),
        "net_delta_vs_baseline": round(
            (matched_variant_profit - matched_baseline_profit) + variant_only_profit - baseline_only_profit,
            3,
        ),
        "improved_count": improved_count,
        "worsened_count": worsened_count,
        "unchanged_count": unchanged_count,
        "winner_clip_rate": round(winner_clip_count / baseline_winner_count, 4) if baseline_winner_count else None,
        "winner_flip_to_loss_rate": round(winner_flip_to_loss_count / baseline_winner_count, 4)
        if baseline_winner_count
        else None,
        "loser_mitigation_rate": round(loser_mitigated_count / baseline_loser_count, 4)
        if baseline_loser_count
        else None,
        "loser_flip_to_profit_rate": round(loser_flip_to_profit_count / baseline_loser_count, 4)
        if baseline_loser_count
        else None,
        "big_winner_threshold": round(baseline_big_winner_threshold, 3) if baseline_big_winner_threshold is not None else None,
        "big_winner_count": big_winner_count,
        "big_winner_clip_rate": round(big_winner_clip_count / big_winner_count, 4) if big_winner_count else None,
        "deep_loser_threshold": round(baseline_deep_loser_threshold, 3) if baseline_deep_loser_threshold is not None else None,
        "deep_loser_count": deep_loser_count,
        "deep_loser_mitigation_rate": round(deep_loser_mitigated_count / deep_loser_count, 4)
        if deep_loser_count
        else None,
        "mean_matched_profit_delta": round(sum(matched_delta_values) / len(matched_delta_values), 4)
        if matched_delta_values
        else None,
        "event_position_count": event_position_count,
        "event_position_share": round(event_position_count / len(matched_keys), 4) if matched_keys else None,
        "event_on_baseline_winner_share": round(event_on_baseline_winner_count / event_position_count, 4)
        if event_position_count
        else None,
        "event_on_baseline_loser_share": round(event_on_baseline_loser_count / event_position_count, 4)
        if event_position_count
        else None,
    }


def build_analysis() -> dict[str, Any]:
    split_results: dict[str, Any] = {}
    aggregate_bucket: dict[str, list[dict[str, Any]]] = defaultdict(list)

    loaded_runs: dict[str, dict[str, Any]] = {}
    for run_code, run_info in RUNS.items():
        summaries = load_attempt_summaries(run_info["run_dir"])
        split_data: dict[str, Any] = {}
        for split_name, summary in summaries.items():
            trade_ledger_path = Path(summary["trade_ledger_path"])
            positions = load_positions(trade_ledger_path)
            split_data[split_name] = {
                "summary_path": str(summary["_summary_path"]),
                "trade_ledger_path": str(trade_ledger_path),
                "summary": summary,
                "positions": positions,
            }
        loaded_runs[run_code] = split_data

    for split_name, split_label in SPLITS.items():
        baseline_data = loaded_runs["22A"][split_name]
        baseline_positions = baseline_data["positions"]
        split_payload = {
            "label": split_label,
            "baseline": {
                "run_code": "22A",
                "run_label": RUNS["22A"]["label"],
                "summary_path": baseline_data["summary_path"],
                "trade_ledger_path": baseline_data["trade_ledger_path"],
                "headline": baseline_data["summary"]["financial_metrics"]["headline"],
                "position_summary": summarize_positions(baseline_positions),
            },
            "variants": {},
        }

        for variant_code in ("22B", "22C", "22D", "22E"):
            variant_data = loaded_runs[variant_code][split_name]
            variant_positions = variant_data["positions"]
            comparison = compare_variant_to_baseline(
                baseline_positions=baseline_positions,
                variant_positions=variant_positions,
                variant_code=variant_code,
            )
            payload = {
                "run_code": variant_code,
                "run_label": RUNS[variant_code]["label"],
                "summary_path": variant_data["summary_path"],
                "trade_ledger_path": variant_data["trade_ledger_path"],
                "headline": variant_data["summary"]["financial_metrics"]["headline"],
                "position_summary": summarize_positions(variant_positions),
                "comparison_to_22A": comparison,
            }
            split_payload["variants"][variant_code] = payload
            aggregate_bucket[variant_code].append(payload)

        split_results[split_name] = split_payload

    aggregate_results: dict[str, Any] = {}
    for variant_code, payloads in aggregate_bucket.items():
        metric_names = (
            "net_delta_vs_baseline",
            "winner_clip_rate",
            "loser_mitigation_rate",
            "big_winner_clip_rate",
            "deep_loser_mitigation_rate",
            "baseline_overlap_rate",
            "variant_overlap_rate",
            "event_position_share",
        )
        aggregate_metrics: dict[str, float | None] = {}
        for metric_name in metric_names:
            values = [
                payload["comparison_to_22A"][metric_name]
                for payload in payloads
                if payload["comparison_to_22A"][metric_name] is not None
            ]
            aggregate_metrics[metric_name] = round(sum(values) / len(values), 4) if values else None
        aggregate_results[variant_code] = {
            "run_label": RUNS[variant_code]["label"],
            "mean_metrics": aggregate_metrics,
        }

    return {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "methodology": {
            "baseline_run": "22A",
            "comparison_runs": ["22B", "22C", "22D", "22E"],
            "split_names": SPLITS,
            "position_reconstruction": "group trade ledger rows by position_identifier, then compare positions by entry_bar_time_server + direction",
            "winner_definition": "baseline position net_profit > 0",
            "big_winner_definition": "baseline position net_profit >= 75th percentile of positive baseline position net_profit for that split",
            "loser_definition": "baseline position net_profit < 0",
            "deep_loser_definition": "baseline position net_profit <= 25th percentile of negative baseline position net_profit for that split",
        },
        "splits": split_results,
        "aggregate": aggregate_results,
    }


def render_markdown(analysis: dict[str, Any]) -> str:
    lines: list[str] = []
    lines.append("# Stage 22 Ledger Postmortem Review")
    lines.append("")
    lines.append(f"Generated at: `{analysis['generated_at_utc']}`")
    lines.append("")
    lines.append("## Method")
    lines.append("")
    lines.append("- baseline: `22A baseline_time_exit`")
    lines.append("- comparison set: `22B break_even`, `22C trailing_stop`, `22D partial_stop_loss`, `22E partial_take_profit`")
    lines.append("- unit of analysis: `position_identifier` grouped back into one logical position before comparison")
    lines.append("- match key across runs: `entry_bar_time_server + direction`")
    lines.append("- note: partial variants inflate ledger rows because one position can emit both a partial close row and a final close row")
    lines.append("")
    lines.append("## Aggregate Read")
    lines.append("")
    lines.append("| variant | mean net delta vs 22A | mean winner clip rate | mean loser mitigation rate | mean big-winner clip rate | mean overlap vs 22A |")
    lines.append("|---|---:|---:|---:|---:|---:|")
    for variant_code in ("22B", "22C", "22D", "22E"):
        metrics = analysis["aggregate"][variant_code]["mean_metrics"]
        lines.append(
            "| {variant} | {net_delta:.3f} | {winner_clip:.3f} | {loser_mitigate:.3f} | {big_clip:.3f} | {overlap:.3f} |".format(
                variant=variant_code,
                net_delta=metrics["net_delta_vs_baseline"] or 0.0,
                winner_clip=metrics["winner_clip_rate"] or 0.0,
                loser_mitigate=metrics["loser_mitigation_rate"] or 0.0,
                big_clip=metrics["big_winner_clip_rate"] or 0.0,
                overlap=metrics["baseline_overlap_rate"] or 0.0,
            )
        )
    lines.append("")

    for split_name, split_payload in analysis["splits"].items():
        lines.append(f"## {split_payload['label']}")
        lines.append("")
        baseline_headline = split_payload["baseline"]["headline"]
        baseline_positions = split_payload["baseline"]["position_summary"]
        lines.append(
            "- baseline `22A`: return_pct `{return_pct:.3f}`, PF `{profit_factor:.4f}`, summary trade_count `{trade_count}`, position_count `{position_count}`, max_dd_pct `{max_dd_pct:.3f}`".format(
                return_pct=baseline_headline["return_pct"],
                profit_factor=baseline_headline["profit_factor"],
                trade_count=baseline_headline["trade_count"],
                position_count=baseline_positions["position_count"],
                max_dd_pct=baseline_headline["max_dd_pct"],
            )
        )
        lines.append("")
        lines.append("| variant | return_pct | summary trade_count | position_count | ledger rows | net delta vs 22A | winner clip rate | loser mitigation rate | variant-only positions | event share |")
        lines.append("|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
        for variant_code in ("22B", "22C", "22D", "22E"):
            payload = split_payload["variants"][variant_code]
            headline = payload["headline"]
            position_summary = payload["position_summary"]
            comp = payload["comparison_to_22A"]
            lines.append(
                "| {variant} | {return_pct:.3f} | {trade_count} | {position_count} | {ledger_rows} | {net_delta:.3f} | {winner_clip:.3f} | {loser_mitigate:.3f} | {variant_only} | {event_share:.3f} |".format(
                    variant=variant_code,
                    return_pct=headline["return_pct"],
                    trade_count=headline["trade_count"],
                    position_count=position_summary["position_count"],
                    ledger_rows=position_summary["ledger_row_count"],
                    net_delta=comp["net_delta_vs_baseline"],
                    winner_clip=comp["winner_clip_rate"] or 0.0,
                    loser_mitigate=comp["loser_mitigation_rate"] or 0.0,
                    variant_only=comp["variant_only_position_count"],
                    event_share=comp["event_position_share"] or 0.0,
                )
            )
        lines.append("")
        for variant_code in ("22B", "22C", "22D", "22E"):
            payload = split_payload["variants"][variant_code]
            comp = payload["comparison_to_22A"]
            position_summary = payload["position_summary"]
            lines.append(
                "- `{variant_code}` `{label}`: matched `{matched}`, baseline_only `{base_only}`, variant_only `{variant_only}`, shared delta `{shared_delta:.3f}`, baseline_only_profit `{base_only_profit:.3f}`, variant_only_profit `{variant_only_profit:.3f}`, close_reasons `{close_reasons}`".format(
                    variant_code=variant_code,
                    label=payload["run_label"],
                    matched=comp["matched_position_count"],
                    base_only=comp["baseline_only_position_count"],
                    variant_only=comp["variant_only_position_count"],
                    shared_delta=comp["matched_profit_delta"],
                    base_only_profit=comp["baseline_only_profit"],
                    variant_only_profit=comp["variant_only_profit"],
                    close_reasons=position_summary["close_reason_breakdown"],
                )
            )
        lines.append("")

    lines.append("## Working Conclusion")
    lines.append("")
    lines.append("- `22B break_even` is the clearest winner-clipping candidate when judged against matched baseline winners.")
    lines.append("- `22C trailing_stop` changes relatively few positions but still gives away too much shared-position profit when it fires.")
    lines.append("- `22D partial_stop_loss` is the strongest risk-control read: it helps more baseline losers than the other variants, but its row inflation and added churn mean it should be framed as containment rather than alpha.")
    lines.append("- `22E partial_take_profit` adds bookkeeping churn and clips winners without enough loser relief to justify a rerun as a simple fixed-point rule.")
    return "\n".join(lines) + "\n"


def main() -> None:
    REVIEW_DIR.mkdir(parents=True, exist_ok=True)
    analysis = build_analysis()
    json_path = REVIEW_DIR / "stage22_ledger_postmortem_20260408.json"
    md_path = REVIEW_DIR / "stage22_ledger_postmortem_20260408.md"
    json_path.write_text(json.dumps(analysis, ensure_ascii=False, indent=2), encoding="utf-8")
    md_path.write_text(render_markdown(analysis), encoding="utf-8-sig")
    print(json_path)
    print(md_path)


if __name__ == "__main__":
    main()
