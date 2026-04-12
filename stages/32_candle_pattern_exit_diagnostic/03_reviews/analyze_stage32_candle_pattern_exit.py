#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
from collections import Counter
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

import pandas as pd


ROOT_DIR = Path(__file__).resolve().parents[3]
STAGE_DIR = ROOT_DIR / "stages" / "32_candle_pattern_exit_diagnostic"
RUN_DIR = ROOT_DIR / "stages" / "29_fusion_long_repair" / "02_runs" / "active" / "29N_25o_sxh2_0001"
RAW_BARS_DIR = ROOT_DIR / "data" / "raw" / "mt5_bars" / "m5" / "US100"
OUTPUT_JSON = STAGE_DIR / "03_reviews" / "stage32_candle_pattern_exit_20260412.json"
OUTPUT_MD = STAGE_DIR / "03_reviews" / "stage32_candle_pattern_exit_20260412.md"
SUMMARY_PATHS = {
    "validation": RUN_DIR / "mt5_attempts" / "att_0001" / "tester_attempt_summary.json",
    "test": RUN_DIR / "mt5_attempts" / "att_0002" / "tester_attempt_summary.json",
    "hist_2024": RUN_DIR / "mt5_attempts" / "att_0003" / "tester_attempt_summary.json",
}
PATTERN_ORDER = ["outside_adverse_bar", "rejection_tail", "wide_range_doji"]
PATTERN_LABELS = {
    "outside_adverse_bar": "Outside Adverse Bar",
    "rejection_tail": "Rejection Tail",
    "wide_range_doji": "Wide-Range Doji",
}
PROBE_BARS = 3
TIME_STEP = timedelta(minutes=5)
POINT_SIZE = 0.01
NY_TZ = ZoneInfo("America/New_York")


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False, default=str), encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def parse_mt5_datetime(text: str) -> datetime:
    return datetime.strptime(text, "%Y.%m.%d %H:%M:%S")


def format_mt5_datetime(value: datetime | None) -> str:
    if value is None:
        return "n/a"
    return value.strftime("%Y-%m-%d %H:%M")


def format_money(value: float | None) -> str:
    if value is None:
        return "n/a"
    return f"{value:.2f}"


def month_span(start_dt: datetime, end_dt: datetime):
    return pd.period_range(start=pd.Timestamp(start_dt), end=pd.Timestamp(end_dt), freq="M")


def load_trade_rows(path: Path) -> list[dict[str, object]]:
    trades: list[dict[str, object]] = []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            trades.append(
                {
                    "direction": (row.get("direction") or "").strip().upper(),
                    "volume": float(row.get("volume") or 0.0),
                    "entry_bar_time": parse_mt5_datetime(row["entry_bar_time_server"]),
                    "exit_bar_time": parse_mt5_datetime(row["exit_bar_time_server"]),
                    "entry_price": float(row.get("entry_price") or 0.0),
                    "exit_price": float(row.get("exit_price") or 0.0),
                    "hold_bars": int(row.get("hold_bars") or 0),
                    "close_reason": row.get("close_reason") or "",
                    "net_profit": float(row.get("net_profit") or 0.0),
                }
            )
    return trades


def load_us100_bars(start_dt: datetime, end_dt: datetime) -> pd.DataFrame:
    frames: list[pd.DataFrame] = []
    for month in month_span(start_dt, end_dt):
        path = RAW_BARS_DIR / str(month.year) / f"US100_m5_{month.strftime('%Y-%m')}.parquet"
        if path.exists():
            frames.append(pd.read_parquet(path))
    if not frames:
        raise FileNotFoundError(f"no raw US100 bars for {start_dt}..{end_dt}")

    bars = pd.concat(frames, ignore_index=True)
    bars["bar_open"] = pd.to_datetime(bars["time_utc"], utc=True).dt.tz_convert(None)
    bars = bars.sort_values("bar_open").reset_index(drop=True)
    bars["bar_close"] = bars["bar_open"] + pd.Timedelta(minutes=5)

    prev_close = bars["close"].shift(1)
    true_range = pd.concat(
        [
            bars["high"] - bars["low"],
            (bars["high"] - prev_close).abs(),
            (bars["low"] - prev_close).abs(),
        ],
        axis=1,
    ).max(axis=1)
    bars["atr14"] = true_range.ewm(alpha=1.0 / 14.0, adjust=False).mean()
    bars["atr14_prev"] = bars["atr14"].shift(1)

    bars["range_abs"] = bars["high"] - bars["low"]
    bars["body_abs"] = (bars["close"] - bars["open"]).abs()
    bars["body_dir"] = 0
    bars.loc[bars["close"] > bars["open"], "body_dir"] = 1
    bars.loc[bars["close"] < bars["open"], "body_dir"] = -1
    bars["upper_wick"] = bars["high"] - bars[["open", "close"]].max(axis=1)
    bars["lower_wick"] = bars[["open", "close"]].min(axis=1) - bars["low"]
    bars["prev_high"] = bars["high"].shift(1)
    bars["prev_low"] = bars["low"].shift(1)

    start = pd.Timestamp(start_dt) - pd.Timedelta(days=2)
    end = pd.Timestamp(end_dt) + pd.Timedelta(days=2)
    return bars[(bars["bar_close"] >= start) & (bars["bar_close"] <= end)].copy()


def load_hold_config(bundle_path: Path) -> dict[str, int]:
    payload = load_json(bundle_path)
    base_hold = 5
    for rule in payload["rule_stack"]["exit"]:
        if rule.get("enabled") and rule.get("type") == "time_exit":
            base_hold = int(rule.get("params", {}).get("max_hold_bars", 5))
            break
    extra = payload.get("runtime_snapshot", {}).get("extra", {})
    return {
        "base_max_hold_bars": base_hold,
        "monday_long_hold_cap_bars": int(extra.get("monday_long_hold_cap_bars", 0) or 0),
        "monday_short_hold_cap_bars": int(extra.get("monday_short_hold_cap_bars", 0) or 0),
        "ny_postcash_hold_cap_bars": int(extra.get("ny_postcash_hold_cap_bars", 0) or 0),
        "ny_postcash_long_hold_cap_bars": int(extra.get("ny_postcash_long_hold_cap_bars", 0) or 0),
        "ny_postcash_short_hold_cap_bars": int(extra.get("ny_postcash_short_hold_cap_bars", 0) or 0),
    }


def resolve_new_york_context(bar_close_time: datetime) -> tuple[bool, bool]:
    ny_time = bar_close_time.replace(tzinfo=ZoneInfo("UTC")).astimezone(NY_TZ)
    minutes = ny_time.hour * 60 + ny_time.minute
    return ny_time.weekday() == 0, minutes >= (16 * 60)


def resolve_dynamic_hold_cap(bar_close_time: datetime, direction: str, hold_cfg: dict[str, int]) -> tuple[int, str]:
    resolved = hold_cfg["base_max_hold_bars"]
    label = "BASE"
    is_monday, is_postcash = resolve_new_york_context(bar_close_time)

    if is_monday:
        if direction == "LONG" and 0 < hold_cfg["monday_long_hold_cap_bars"] < resolved:
            resolved = hold_cfg["monday_long_hold_cap_bars"]
            label = "MONDAY_LONG"
        elif direction == "SHORT" and 0 < hold_cfg["monday_short_hold_cap_bars"] < resolved:
            resolved = hold_cfg["monday_short_hold_cap_bars"]
            label = "MONDAY_SHORT"

    if is_postcash and 0 < hold_cfg["ny_postcash_hold_cap_bars"] < resolved:
        resolved = hold_cfg["ny_postcash_hold_cap_bars"]
        label = "NY_POSTCASH"

    if is_postcash:
        if direction == "LONG" and 0 < hold_cfg["ny_postcash_long_hold_cap_bars"] < resolved:
            resolved = hold_cfg["ny_postcash_long_hold_cap_bars"]
            label = "NY_POSTCASH_LONG"
        elif direction == "SHORT" and 0 < hold_cfg["ny_postcash_short_hold_cap_bars"] < resolved:
            resolved = hold_cfg["ny_postcash_short_hold_cap_bars"]
            label = "NY_POSTCASH_SHORT"

    return resolved, label


def resolve_policy_exit_bar(entry_bar_time: datetime, direction: str, hold_cfg: dict[str, int]) -> tuple[datetime, str]:
    for step in range(1, hold_cfg["base_max_hold_bars"] + 3):
        bar_close = entry_bar_time + (TIME_STEP * step)
        resolved, label = resolve_dynamic_hold_cap(bar_close, direction, hold_cfg)
        if step >= resolved:
            return bar_close, label
    return entry_bar_time + (TIME_STEP * hold_cfg["base_max_hold_bars"]), "BASE"


def closing_price_from_bar(bar_row: pd.Series, direction: str) -> float:
    if direction == "LONG":
        return float(bar_row["close"])
    return float(bar_row["close"]) + (float(bar_row["spread"]) * POINT_SIZE)


def delta_net_from_actual_exit(actual_exit_price: float, counterfactual_exit_price: float, direction: str, volume: float) -> float:
    sign = 1.0 if direction == "LONG" else -1.0
    return sign * (counterfactual_exit_price - actual_exit_price) * volume


def pattern_outside_adverse_bar(bar: pd.Series, direction: str) -> bool:
    adverse_close = (direction == "LONG" and int(bar["body_dir"]) < 0) or (direction == "SHORT" and int(bar["body_dir"]) > 0)
    if not adverse_close:
        return False
    if pd.isna(bar["prev_high"]) or pd.isna(bar["prev_low"]):
        return False
    return float(bar["high"]) > float(bar["prev_high"]) and float(bar["low"]) < float(bar["prev_low"])


def pattern_rejection_tail(bar: pd.Series, direction: str) -> bool:
    if pd.isna(bar["atr14_prev"]) or float(bar["atr14_prev"]) <= 0.0:
        return False
    if float(bar["range_abs"]) / float(bar["atr14_prev"]) < 1.0:
        return False

    if direction == "LONG":
        favorable_wick = float(bar["lower_wick"])
        opposite_wick = float(bar["upper_wick"])
        adverse_close = int(bar["body_dir"]) < 0
    else:
        favorable_wick = float(bar["upper_wick"])
        opposite_wick = float(bar["lower_wick"])
        adverse_close = int(bar["body_dir"]) > 0

    return adverse_close and favorable_wick >= max(float(bar["body_abs"]) * 1.5, float(bar["range_abs"]) * 0.4) and favorable_wick > opposite_wick


def pattern_wide_range_doji(bar: pd.Series, _direction: str) -> bool:
    if pd.isna(bar["atr14_prev"]) or float(bar["atr14_prev"]) <= 0.0:
        return False
    range_abs = float(bar["range_abs"])
    if range_abs <= 0.0:
        return False
    return (float(bar["body_abs"]) / range_abs <= 0.2) and (range_abs / float(bar["atr14_prev"]) >= 1.25)


PATTERN_FUNCS = {
    "outside_adverse_bar": pattern_outside_adverse_bar,
    "rejection_tail": pattern_rejection_tail,
    "wide_range_doji": pattern_wide_range_doji,
}


def summarize_deltas(cases: list[dict[str, object]], key: str) -> dict[str, object]:
    values = [float(case[key]) for case in cases if case.get(key) is not None]
    if not values:
        return {"count": 0, "positive_count": 0, "negative_count": 0, "sum_delta_net": None}
    return {
        "count": len(values),
        "positive_count": sum(value > 0.0 for value in values),
        "negative_count": sum(value < 0.0 for value in values),
        "sum_delta_net": float(sum(values)),
    }


def trim_case(case: dict[str, object]) -> dict[str, object]:
    return {
        "split": case["split"],
        "direction": case["direction"],
        "entry_bar_time": format_mt5_datetime(case["entry_bar_time"]),
        "exit_bar_time": format_mt5_datetime(case["exit_bar_time"]),
        "policy_exit_bar_time": format_mt5_datetime(case["policy_exit_bar_time"]),
        "policy_hold_context": case["policy_hold_context"],
        "hold_bars": case["hold_bars"],
        "close_reason": case["close_reason"],
        "net_profit": case["net_profit"],
        "policy_delta_net": case["policy_delta_net"],
        "probe_3bar_delta_net": case["probe_3bar_delta_net"],
        "pattern_score": case["pattern_score"],
    }


def analyze_split(split_name: str, summary_path: Path, hold_cfg: dict[str, int]) -> tuple[dict[str, object], dict[str, list[dict[str, object]]]]:
    summary = load_json(summary_path)
    trade_ledger_path = Path(summary["trade_ledger_path"])
    trades = load_trade_rows(trade_ledger_path)
    bars = load_us100_bars(
        min(trade["entry_bar_time"] for trade in trades),
        max(trade["exit_bar_time"] for trade in trades),
    )
    bars_by_close = bars.set_index("bar_close")
    state_exit_count = sum(str(trade["close_reason"]).startswith("STATE_EXIT") for trade in trades)

    split_summary: dict[str, object] = {
        "split": split_name,
        "trade_count": len(trades),
        "state_exit_count": state_exit_count,
        "trade_ledger_path": str(trade_ledger_path),
        "tester_from_date": summary.get("tester_from_date"),
        "tester_to_date": summary.get("tester_to_date"),
        "patterns": {},
    }
    split_cases: dict[str, list[dict[str, object]]] = {}

    for pattern_name in PATTERN_ORDER:
        func = PATTERN_FUNCS[pattern_name]
        reason_counts: Counter[str] = Counter()
        cases: list[dict[str, object]] = []

        for trade in trades:
            exit_bar_time = trade["exit_bar_time"]
            if exit_bar_time not in bars_by_close.index:
                continue
            exit_bar = bars_by_close.loc[exit_bar_time]
            if not func(exit_bar, str(trade["direction"])):
                continue

            reason_counts[str(trade["close_reason"])] += 1
            if not str(trade["close_reason"]).startswith("STATE_EXIT"):
                continue

            policy_exit_bar_time, hold_label = resolve_policy_exit_bar(
                trade["entry_bar_time"],
                str(trade["direction"]),
                hold_cfg,
            )
            policy_delta = None
            probe_delta = None

            if policy_exit_bar_time in bars_by_close.index:
                policy_price = closing_price_from_bar(bars_by_close.loc[policy_exit_bar_time], str(trade["direction"]))
                policy_delta = delta_net_from_actual_exit(
                    float(trade["exit_price"]),
                    policy_price,
                    str(trade["direction"]),
                    float(trade["volume"]),
                )

            probe_exit_bar_time = trade["exit_bar_time"] + (TIME_STEP * PROBE_BARS)
            if probe_exit_bar_time in bars_by_close.index:
                probe_price = closing_price_from_bar(bars_by_close.loc[probe_exit_bar_time], str(trade["direction"]))
                probe_delta = delta_net_from_actual_exit(
                    float(trade["exit_price"]),
                    probe_price,
                    str(trade["direction"]),
                    float(trade["volume"]),
                )

            cases.append(
                {
                    "split": split_name,
                    "direction": trade["direction"],
                    "entry_bar_time": trade["entry_bar_time"],
                    "exit_bar_time": trade["exit_bar_time"],
                    "policy_exit_bar_time": policy_exit_bar_time,
                    "policy_hold_context": hold_label,
                    "hold_bars": trade["hold_bars"],
                    "close_reason": trade["close_reason"],
                    "net_profit": trade["net_profit"],
                    "policy_delta_net": policy_delta,
                    "probe_3bar_delta_net": probe_delta,
                    "pattern_score": float(exit_bar["range_abs"] / exit_bar["atr14_prev"]) if pd.notna(exit_bar["atr14_prev"]) and float(exit_bar["atr14_prev"]) > 0.0 else None,
                }
            )

        split_summary["patterns"][pattern_name] = {
            "label": PATTERN_LABELS[pattern_name],
            "total_exit_count": int(sum(reason_counts.values())),
            "state_exit_count": len(cases),
            "broker_sl_count": int(reason_counts.get("BROKER_SL", 0)),
            "exit_reason_counts": dict(reason_counts),
            "state_exit_share_of_state_exits": (len(cases) / state_exit_count) if state_exit_count else None,
            "policy_hold_summary": summarize_deltas(cases, "policy_delta_net"),
            "probe_3bar_summary": summarize_deltas(cases, "probe_3bar_delta_net"),
        }
        split_cases[pattern_name] = cases

    return split_summary, split_cases


def build_overall(split_summaries: dict[str, object], split_cases: dict[str, dict[str, list[dict[str, object]]]]) -> dict[str, object]:
    overall: dict[str, object] = {
        "trade_count": sum(int(payload["trade_count"]) for payload in split_summaries.values()),
        "state_exit_count": sum(int(payload["state_exit_count"]) for payload in split_summaries.values()),
        "patterns": {},
    }

    for pattern_name in PATTERN_ORDER:
        reason_counts: Counter[str] = Counter()
        cases: list[dict[str, object]] = []

        for split_name in split_summaries:
            reason_counts.update(split_summaries[split_name]["patterns"][pattern_name]["exit_reason_counts"])
            cases.extend(split_cases[split_name][pattern_name])

        positive_cases = [case for case in cases if (case.get("policy_delta_net") or 0.0) > 0.0]
        negative_cases = [case for case in cases if (case.get("policy_delta_net") or 0.0) < 0.0]
        policy_summary = summarize_deltas(cases, "policy_delta_net")
        probe_summary = summarize_deltas(cases, "probe_3bar_delta_net")

        overall["patterns"][pattern_name] = {
            "label": PATTERN_LABELS[pattern_name],
            "total_exit_count": int(sum(reason_counts.values())),
            "state_exit_count": len(cases),
            "broker_sl_count": int(reason_counts.get("BROKER_SL", 0)),
            "exit_reason_counts": dict(reason_counts),
            "state_exit_share_of_state_exits": (len(cases) / overall["state_exit_count"]) if overall["state_exit_count"] else None,
            "policy_hold_summary": policy_summary,
            "probe_3bar_summary": probe_summary,
            "top_policy_missed_profit_cases": [
                trim_case(case)
                for case in sorted(positive_cases, key=lambda item: float(item["policy_delta_net"] or 0.0), reverse=True)[:5]
            ],
            "top_policy_saved_loss_cases": [
                trim_case(case)
                for case in sorted(negative_cases, key=lambda item: float(item["policy_delta_net"] or 0.0))[:5]
            ],
        }

    return overall


def render_markdown(payload: dict) -> str:
    overall = payload["overall"]
    lines = [
        "# Stage 32 Candle Pattern Exit Diagnostic",
        "",
        f"- reviewed_on: `{payload['reviewed_on']}`",
        f"- run_anchor: `{payload['run_name']}`",
        f"- probe_hold: `+{PROBE_BARS} bars` relaxed diagnostic",
        "",
        "## Headline",
        "",
    ]

    for pattern_name in PATTERN_ORDER:
        pattern = overall["patterns"][pattern_name]
        lines.append(
            "- "
            f"`{pattern_name}` "
            f"`total={pattern['total_exit_count']}` "
            f"`state_exit={pattern['state_exit_count']}` "
            f"`broker_sl={pattern['broker_sl_count']}` "
            f"`policy_delta={format_money(pattern['policy_hold_summary']['sum_delta_net'])}`"
        )

    lines.extend(
        [
            "",
            "## Split Read",
            "",
        ]
    )

    for split_name in ("hist_2024", "validation", "test"):
        split = payload["splits"][split_name]
        lines.append(f"### {split_name}")
        lines.append("")
        for pattern_name in PATTERN_ORDER:
            pattern = split["patterns"][pattern_name]
            lines.append(
                "- "
                f"`{pattern_name}` "
                f"`total={pattern['total_exit_count']}` "
                f"`state_exit={pattern['state_exit_count']}` "
                f"`broker_sl={pattern['broker_sl_count']}` "
                f"`policy_delta={format_money(pattern['policy_hold_summary']['sum_delta_net'])}`"
            )
        lines.append("")

    lines.extend(
        [
            "## Pattern Ladder",
            "",
            "| pattern | total exits | state exits | broker SL | policy hold delta | probe +3 bars |",
            "| --- | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for pattern_name in PATTERN_ORDER:
        pattern = overall["patterns"][pattern_name]
        lines.append(
            f"| {pattern_name} | {pattern['total_exit_count']} | {pattern['state_exit_count']} | "
            f"{pattern['broker_sl_count']} | {format_money(pattern['policy_hold_summary']['sum_delta_net'])} | "
            f"{format_money(pattern['probe_3bar_summary']['sum_delta_net'])} |"
        )

    best = overall["patterns"]["outside_adverse_bar"]
    lines.extend(
        [
            "",
            "## Best Candidate",
            "",
            f"- `outside_adverse_bar` is the only pattern with a clean first-pass read: `total={best['total_exit_count']}`, `state_exit={best['state_exit_count']}`, `policy_hold_delta={format_money(best['policy_hold_summary']['sum_delta_net'])}`",
            f"- `rejection_tail` is mixed because its validation read is weak even though its overall total stays positive",
            f"- `wide_range_doji` is not attractive because it fires often but its state-exit counterfactual is negative overall",
            "",
            "## Top Outside-Bar Cases",
            "",
            "### Missed Profit Candidates",
            "",
        ]
    )
    for case in best["top_policy_missed_profit_cases"]:
        lines.append(
            "- "
            f"`{case['split']}` `{case['direction']}` "
            f"`exit={case['exit_bar_time']}` "
            f"`policy_delta={format_money(case['policy_delta_net'])}` "
            f"`probe3_delta={format_money(case['probe_3bar_delta_net'])}` "
            f"`range_atr={case['pattern_score']:.2f}`"
        )

    lines.extend(["", "### Saved Loss Candidates", ""])
    for case in best["top_policy_saved_loss_cases"]:
        lines.append(
            "- "
            f"`{case['split']}` `{case['direction']}` "
            f"`exit={case['exit_bar_time']}` "
            f"`policy_delta={format_money(case['policy_delta_net'])}` "
            f"`probe3_delta={format_money(case['probe_3bar_delta_net'])}` "
            f"`range_atr={case['pattern_score']:.2f}`"
        )

    lines.extend(
        [
            "",
            "## Decision",
            "",
            "- keep this as a diagnostic sidecar only",
            "- if the candle-shape topic reopens, start with `outside_adverse_bar` only",
            "- do not spend follow-up time on `wide_range_doji`",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    hold_cfg = load_hold_config(RUN_DIR / "experiment_bundle.json")
    split_summaries: dict[str, object] = {}
    split_cases: dict[str, dict[str, list[dict[str, object]]]] = {}

    for split_name, summary_path in SUMMARY_PATHS.items():
        summary, cases = analyze_split(split_name, summary_path, hold_cfg)
        split_summaries[split_name] = summary
        split_cases[split_name] = cases

    payload = {
        "reviewed_on": "2026-04-12",
        "run_name": "29N_25o_sxh2_0001",
        "probe_bars": PROBE_BARS,
        "hold_config": hold_cfg,
        "splits": split_summaries,
    }
    payload["overall"] = build_overall(split_summaries, split_cases)

    write_json(OUTPUT_JSON, payload)
    write_text(OUTPUT_MD, render_markdown(payload))
    print(f"[done] json={OUTPUT_JSON}")
    print(f"[done] md={OUTPUT_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
