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
STAGE_DIR = ROOT_DIR / "stages" / "31_impulse_candle_exit_diagnostic"
RUN_DIR = ROOT_DIR / "stages" / "29_fusion_long_repair" / "02_runs" / "active" / "29N_25o_sxh2_0001"
RAW_BARS_DIR = ROOT_DIR / "data" / "raw" / "mt5_bars" / "m5" / "US100"
OUTPUT_JSON = STAGE_DIR / "03_reviews" / "stage31_impulse_candle_exit_20260412.json"
OUTPUT_MD = STAGE_DIR / "03_reviews" / "stage31_impulse_candle_exit_20260412.md"
SUMMARY_PATHS = {
    "validation": RUN_DIR / "mt5_attempts" / "att_0001" / "tester_attempt_summary.json",
    "test": RUN_DIR / "mt5_attempts" / "att_0002" / "tester_attempt_summary.json",
    "hist_2024": RUN_DIR / "mt5_attempts" / "att_0003" / "tester_attempt_summary.json",
}
IMPULSE_THRESHOLDS = [1.25, 1.50, 2.00]
MAIN_THRESHOLD = 1.50
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


def format_pct(value: float | None) -> str:
    if value is None:
        return "n/a"
    return f"{value * 100.0:.1f}%"


def threshold_key(value: float) -> str:
    return f"atr_{str(value).replace('.', '_')}"


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
    bars["body_abs"] = (bars["close"] - bars["open"]).abs()
    bars["body_dir"] = 0
    bars.loc[bars["close"] > bars["open"], "body_dir"] = 1
    bars.loc[bars["close"] < bars["open"], "body_dir"] = -1

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


def adverse_direction_matches(direction: str, body_dir: int) -> bool:
    return (direction == "LONG" and body_dir < 0) or (direction == "SHORT" and body_dir > 0)


def closing_price_from_bar(bar_row: pd.Series, direction: str) -> float:
    if direction == "LONG":
        return float(bar_row["close"])
    return float(bar_row["close"]) + (float(bar_row["spread"]) * POINT_SIZE)


def delta_net_from_actual_exit(actual_exit_price: float, counterfactual_exit_price: float, direction: str, volume: float) -> float:
    sign = 1.0 if direction == "LONG" else -1.0
    return sign * (counterfactual_exit_price - actual_exit_price) * volume


def incremental_excursions(future_bars: pd.DataFrame, actual_exit_price: float, direction: str, volume: float) -> tuple[float, float]:
    if future_bars.empty:
        return 0.0, 0.0
    if direction == "LONG":
        worst = float(((future_bars["low"] - actual_exit_price) * volume).min())
        best = float(((future_bars["high"] - actual_exit_price) * volume).max())
        return worst, best
    ask_high = future_bars["high"] + (future_bars["spread"] * POINT_SIZE)
    ask_low = future_bars["low"] + (future_bars["spread"] * POINT_SIZE)
    worst = float(((actual_exit_price - ask_high) * volume).min())
    best = float(((actual_exit_price - ask_low) * volume).max())
    return worst, best


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
        "body_atr_ratio": case["body_atr_ratio"],
        "policy_extension_bars": case["policy_extension_bars"],
        "policy_delta_net": case["policy_delta_net"],
        "probe_3bar_delta_net": case["probe_3bar_delta_net"],
        "policy_worst_incremental_mae": case["policy_worst_incremental_mae"],
        "policy_best_incremental_mfe": case["policy_best_incremental_mfe"],
    }


def analyze_split(split_name: str, summary_path: Path, hold_cfg: dict[str, int]) -> dict[str, object]:
    summary = load_json(summary_path)
    trade_ledger_path = Path(summary["trade_ledger_path"])
    trades = load_trade_rows(trade_ledger_path)
    bars = load_us100_bars(
        min(trade["entry_bar_time"] for trade in trades),
        max(trade["exit_bar_time"] for trade in trades),
    )
    bars_by_close = bars.set_index("bar_close")
    state_exit_count = sum(str(trade["close_reason"]).startswith("STATE_EXIT") for trade in trades)

    threshold_payloads: dict[str, object] = {}
    threshold_cases: dict[str, list[dict[str, object]]] = {}

    for threshold in IMPULSE_THRESHOLDS:
        reason_counts: Counter[str] = Counter()
        cases: list[dict[str, object]] = []

        for trade in trades:
            exit_bar_time = trade["exit_bar_time"]
            if exit_bar_time not in bars_by_close.index:
                continue
            exit_bar = bars_by_close.loc[exit_bar_time]
            atr14_prev = exit_bar["atr14_prev"]
            if pd.isna(atr14_prev) or float(atr14_prev) <= 0.0:
                continue
            body_ratio = float(exit_bar["body_abs"]) / float(atr14_prev)
            if body_ratio < threshold:
                continue
            if not adverse_direction_matches(str(trade["direction"]), int(exit_bar["body_dir"])):
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
            worst_mae = None
            best_mfe = None

            if policy_exit_bar_time in bars_by_close.index:
                policy_price = closing_price_from_bar(bars_by_close.loc[policy_exit_bar_time], str(trade["direction"]))
                policy_delta = delta_net_from_actual_exit(
                    float(trade["exit_price"]),
                    policy_price,
                    str(trade["direction"]),
                    float(trade["volume"]),
                )
                future_policy = bars[
                    (bars["bar_close"] > pd.Timestamp(exit_bar_time)) &
                    (bars["bar_close"] <= pd.Timestamp(policy_exit_bar_time))
                ]
                worst_mae, best_mfe = incremental_excursions(
                    future_policy,
                    float(trade["exit_price"]),
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
                    "body_atr_ratio": body_ratio,
                    "policy_extension_bars": int((policy_exit_bar_time - trade["exit_bar_time"]) / TIME_STEP),
                    "policy_delta_net": policy_delta,
                    "probe_3bar_delta_net": probe_delta,
                    "policy_worst_incremental_mae": worst_mae,
                    "policy_best_incremental_mfe": best_mfe,
                }
            )

        key = threshold_key(threshold)
        threshold_payloads[key] = {
            "threshold_atr_multiple": threshold,
            "adverse_any_exit_count": int(sum(reason_counts.values())),
            "adverse_any_exit_reason_counts": dict(reason_counts),
            "adverse_state_exit_count": len(cases),
            "adverse_state_exit_share_of_state_exits": (len(cases) / state_exit_count) if state_exit_count else None,
            "policy_hold_summary": summarize_deltas(cases, "policy_delta_net"),
            "probe_3bar_summary": summarize_deltas(cases, "probe_3bar_delta_net"),
            "policy_worst_incremental_mae": min(
                (float(case["policy_worst_incremental_mae"]) for case in cases if case["policy_worst_incremental_mae"] is not None),
                default=None,
            ),
            "policy_best_incremental_mfe": max(
                (float(case["policy_best_incremental_mfe"]) for case in cases if case["policy_best_incremental_mfe"] is not None),
                default=None,
            ),
        }
        threshold_cases[key] = cases

    return {
        "split": split_name,
        "trade_count": len(trades),
        "state_exit_count": state_exit_count,
        "trade_ledger_path": str(trade_ledger_path),
        "tester_from_date": summary.get("tester_from_date"),
        "tester_to_date": summary.get("tester_to_date"),
        "thresholds": threshold_payloads,
        "_cases": threshold_cases,
    }


def build_overall(splits: dict[str, object]) -> dict[str, object]:
    overall: dict[str, object] = {
        "trade_count": sum(int(payload["trade_count"]) for payload in splits.values()),
        "state_exit_count": sum(int(payload["state_exit_count"]) for payload in splits.values()),
        "thresholds": {},
    }
    for threshold in IMPULSE_THRESHOLDS:
        key = threshold_key(threshold)
        reason_counts: Counter[str] = Counter()
        cases: list[dict[str, object]] = []
        for payload in splits.values():
            reason_counts.update(payload["thresholds"][key]["adverse_any_exit_reason_counts"])
            cases.extend(payload["_cases"][key])

        positive_cases = [case for case in cases if (case.get("policy_delta_net") or 0.0) > 0.0]
        negative_cases = [case for case in cases if (case.get("policy_delta_net") or 0.0) < 0.0]

        overall["thresholds"][key] = {
            "threshold_atr_multiple": threshold,
            "adverse_any_exit_count": int(sum(reason_counts.values())),
            "adverse_any_exit_reason_counts": dict(reason_counts),
            "adverse_state_exit_count": len(cases),
            "adverse_state_exit_share_of_state_exits": (len(cases) / overall["state_exit_count"]) if overall["state_exit_count"] else None,
            "policy_hold_sum_delta_net": summarize_deltas(cases, "policy_delta_net")["sum_delta_net"],
            "policy_hold_positive_count": summarize_deltas(cases, "policy_delta_net")["positive_count"],
            "policy_hold_negative_count": summarize_deltas(cases, "policy_delta_net")["negative_count"],
            "probe_3bar_sum_delta_net": summarize_deltas(cases, "probe_3bar_delta_net")["sum_delta_net"],
            "probe_3bar_positive_count": summarize_deltas(cases, "probe_3bar_delta_net")["positive_count"],
            "probe_3bar_negative_count": summarize_deltas(cases, "probe_3bar_delta_net")["negative_count"],
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
    main = overall["thresholds"][threshold_key(MAIN_THRESHOLD)]
    lines = [
        "# Stage 31 Impulse Candle Exit Diagnostic",
        "",
        f"- reviewed_on: `{payload['reviewed_on']}`",
        f"- run_anchor: `{payload['run_name']}`",
        f"- main_threshold: `{MAIN_THRESHOLD:.2f} x ATR14` adverse real-body impulse",
        f"- probe_hold: `+{PROBE_BARS} bars` relaxed diagnostic",
        "",
        "## Headline",
        "",
        f"- adverse impulse exits at the main threshold: `{main['adverse_any_exit_count']}` total",
        f"- adverse impulse `STATE_EXIT` subset: `{main['adverse_state_exit_count']} / {overall['state_exit_count']}` state exits, `{format_pct(main['adverse_state_exit_share_of_state_exits'])}`",
        f"- adverse impulse `BROKER_SL` subset: `{main['adverse_any_exit_reason_counts'].get('BROKER_SL', 0)}`",
        f"- policy-consistent `state_exit` counterfactual: `approx +{format_money(main['policy_hold_sum_delta_net'])}`",
        f"- relaxed `+{PROBE_BARS} bar` probe: `approx +{format_money(main['probe_3bar_sum_delta_net'])}`",
        "- read: the effect exists, but it is sparse and not yet strong enough to justify a broad runtime rewrite",
        "",
        "## Split Read",
        "",
    ]

    for split_name in ("hist_2024", "validation", "test"):
        split_payload = payload["splits"][split_name]
        main_split = split_payload["thresholds"][threshold_key(MAIN_THRESHOLD)]
        lines.extend(
            [
                f"### {split_name}",
                "",
                f"- state exits: `{split_payload['state_exit_count']}`",
                f"- adverse impulse exits at `{MAIN_THRESHOLD:.2f} x ATR14`: `{main_split['adverse_any_exit_count']}` total, reason mix `{main_split['adverse_any_exit_reason_counts']}`",
                f"- adverse impulse `STATE_EXIT` subset: `{main_split['adverse_state_exit_count']}` (`{format_pct(main_split['adverse_state_exit_share_of_state_exits'])}` of state exits)",
                f"- policy-consistent hold: `sum_delta_net={format_money(main_split['policy_hold_summary']['sum_delta_net'])}`, `pos={main_split['policy_hold_summary']['positive_count']}`, `neg={main_split['policy_hold_summary']['negative_count']}`",
                f"- relaxed +{PROBE_BARS} bars: `sum_delta_net={format_money(main_split['probe_3bar_summary']['sum_delta_net'])}`, `pos={main_split['probe_3bar_summary']['positive_count']}`, `neg={main_split['probe_3bar_summary']['negative_count']}`",
                f"- worst extra adverse excursion under policy hold: `{format_money(main_split['policy_worst_incremental_mae'])}`",
                "",
            ]
        )

    lines.extend(
        [
            "## Threshold Ladder",
            "",
            "| threshold | adverse state exits | state-exit share | policy delta | probe +3 bars |",
            "| --- | ---: | ---: | ---: | ---: |",
        ]
    )
    for threshold in IMPULSE_THRESHOLDS:
        ladder = overall["thresholds"][threshold_key(threshold)]
        lines.append(
            f"| {threshold:.2f} x ATR14 | {ladder['adverse_state_exit_count']} | "
            f"{format_pct(ladder['adverse_state_exit_share_of_state_exits'])} | "
            f"{format_money(ladder['policy_hold_sum_delta_net'])} | "
            f"{format_money(ladder['probe_3bar_sum_delta_net'])} |"
        )

    lines.extend(["", "## Top Cases", "", "### Missed Profit Candidates", ""])
    for case in main["top_policy_missed_profit_cases"]:
        lines.append(
            "- "
            f"`{case['split']}` `{case['direction']}` "
            f"`exit={case['exit_bar_time']}` "
            f"`body_atr={case['body_atr_ratio']:.2f}` "
            f"`policy_delta={format_money(case['policy_delta_net'])}` "
            f"`probe3_delta={format_money(case['probe_3bar_delta_net'])}` "
            f"`extra_mae={format_money(case['policy_worst_incremental_mae'])}`"
        )

    lines.extend(["", "### Saved Loss Candidates", ""])
    for case in main["top_policy_saved_loss_cases"]:
        lines.append(
            "- "
            f"`{case['split']}` `{case['direction']}` "
            f"`exit={case['exit_bar_time']}` "
            f"`body_atr={case['body_atr_ratio']:.2f}` "
            f"`policy_delta={format_money(case['policy_delta_net'])}` "
            f"`probe3_delta={format_money(case['probe_3bar_delta_net'])}` "
            f"`extra_mae={format_money(case['policy_worst_incremental_mae'])}`"
        )

    lines.extend(
        [
            "",
            "## Decision",
            "",
            "- keep this as a diagnostic sidecar only",
            "- if the impulse topic reopens, compare a targeted `state-exit-only` suppression with a stop-side sensitivity read before attempting full candle neutralization",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    hold_cfg = load_hold_config(RUN_DIR / "experiment_bundle.json")
    splits = {split_name: analyze_split(split_name, summary_path, hold_cfg) for split_name, summary_path in SUMMARY_PATHS.items()}
    payload = {
        "reviewed_on": "2026-04-12",
        "run_name": "29N_25o_sxh2_0001",
        "main_threshold_atr_multiple": MAIN_THRESHOLD,
        "probe_bars": PROBE_BARS,
        "hold_config": hold_cfg,
        "splits": splits,
    }
    payload["overall"] = build_overall(splits)
    write_json(OUTPUT_JSON, payload)
    write_text(OUTPUT_MD, render_markdown(payload))
    print(f"[done] json={OUTPUT_JSON}")
    print(f"[done] md={OUTPUT_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
