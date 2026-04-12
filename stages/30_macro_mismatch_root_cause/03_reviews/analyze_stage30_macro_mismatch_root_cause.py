#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
from bisect import bisect_right
from collections import Counter, defaultdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import Iterable

import pandas as pd


ROOT_DIR = Path(__file__).resolve().parents[3]
STAGE_DIR = ROOT_DIR / "stages" / "30_macro_mismatch_root_cause"
OUTPUT_JSON = STAGE_DIR / "03_reviews" / "stage30_macro_mismatch_root_cause_20260412.json"
OUTPUT_MD = STAGE_DIR / "03_reviews" / "stage30_macro_mismatch_root_cause_20260412.md"
RAW_BARS_DIR = ROOT_DIR / "data" / "raw" / "mt5_bars" / "m5"
BAR_STEP = timedelta(minutes=5)

RUN_NAME = "29N_25o_sxh2_0001"
RUN_DIR = ROOT_DIR / "stages" / "29_fusion_long_repair" / "02_runs" / "active" / RUN_NAME
SUMMARY_PATHS = {
    "validation": RUN_DIR / "mt5_attempts" / "att_0001" / "tester_attempt_summary.json",
    "test": RUN_DIR / "mt5_attempts" / "att_0002" / "tester_attempt_summary.json",
    "hist_2024": RUN_DIR / "mt5_attempts" / "att_0003" / "tester_attempt_summary.json",
}
FOCUS_SYMBOLS = ["VIX", "US10YR", "AAPL.xnas", "USDX"]


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def parse_mt5_datetime(text: str) -> datetime:
    return datetime.strptime(text, "%Y.%m.%d %H:%M:%S")


def format_mt5_datetime(value: datetime) -> str:
    return value.strftime("%Y-%m-%d %H:%M")


def format_clock(minutes: int | None) -> str:
    if minutes is None:
        return "n/a"
    hours = minutes // 60
    mins = minutes % 60
    return f"{hours:02d}:{mins:02d}"


def top_items(counter: Counter, limit: int = 5) -> list[dict[str, object]]:
    return [{"key": key, "count": count} for key, count in counter.most_common(limit)]


def top_items_from_mapping(mapping: dict[str, int], limit: int = 5) -> list[dict[str, object]]:
    ordered = sorted(mapping.items(), key=lambda item: item[1], reverse=True)[:limit]
    return [{"key": key, "count": count} for key, count in ordered]


def quantile_as_int(values: list[int], q: float) -> int | None:
    if not values:
        return None
    return int(round(float(pd.Series(values).quantile(q))))


def load_shadow_rows(path: Path) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            row["bar_time_dt"] = parse_mt5_datetime(row["bar_time_server"])
            rows.append(row)
    return rows


def unique_base_times(rows: list[dict[str, object]]) -> list[datetime]:
    seen: set[datetime] = set()
    ordered: list[datetime] = []
    for row in rows:
        if row.get("cycle_tag") == "INIT_SMOKE":
            continue
        bar_time = row["bar_time_dt"]
        if bar_time in seen:
            continue
        seen.add(bar_time)
        ordered.append(bar_time)
    ordered.sort()
    return ordered


def month_span(start_dt: datetime, end_dt: datetime) -> Iterable[pd.Period]:
    start = pd.Timestamp(start_dt)
    end = pd.Timestamp(end_dt)
    return pd.period_range(start=start, end=end, freq="M")


def load_symbol_times(symbol: str, start_dt: datetime, end_dt: datetime) -> list[datetime]:
    frames: list[pd.DataFrame] = []
    for month in month_span(start_dt, end_dt):
        path = RAW_BARS_DIR / symbol / str(month.year) / f"{symbol}_m5_{month.strftime('%Y-%m')}.parquet"
        if not path.exists():
            continue
        frames.append(pd.read_parquet(path, columns=["time_utc"]))
    if not frames:
        return []

    merged = pd.concat(frames, ignore_index=True)
    series = pd.to_datetime(merged["time_utc"], utc=True).dt.tz_convert(None)
    filtered = series[(series >= pd.Timestamp(start_dt)) & (series <= pd.Timestamp(end_dt))]
    unique_sorted = filtered.drop_duplicates().sort_values()
    return [item.to_pydatetime() for item in unique_sorted]


def build_streaks(times: list[datetime]) -> list[dict[str, object]]:
    if not times:
        return []

    ordered = sorted(times)
    streaks: list[dict[str, object]] = []
    start = ordered[0]
    prev = ordered[0]
    length = 1
    for current in ordered[1:]:
        if current - prev == BAR_STEP:
            length += 1
        else:
            streaks.append({"start": start, "end": prev, "length": length})
            start = current
            length = 1
        prev = current
    streaks.append({"start": start, "end": prev, "length": length})
    return streaks


def summarize_streaks(times: list[datetime]) -> dict[str, object]:
    streaks = build_streaks(times)
    lengths = [int(item["length"]) for item in streaks]
    if not lengths:
        return {
            "streak_count": 0,
            "p50": None,
            "p90": None,
            "max": None,
            "single_share": None,
            "top_streaks": [],
        }

    top = sorted(streaks, key=lambda item: int(item["length"]), reverse=True)[:5]
    return {
        "streak_count": len(streaks),
        "p50": quantile_as_int(lengths, 0.50),
        "p90": quantile_as_int(lengths, 0.90),
        "max": max(lengths),
        "single_share": round(sum(1 for value in lengths if value == 1) / len(lengths), 4),
        "top_streaks": [
            {
                "start": format_mt5_datetime(item["start"]),
                "end": format_mt5_datetime(item["end"]),
                "length": int(item["length"]),
            }
            for item in top
        ],
    }


def summarize_temporal_shape(times: list[datetime]) -> dict[str, object]:
    if not times:
        return {
            "top_hours": [],
            "top_dates": [],
            "weekday_breakdown": [],
        }

    hours = Counter(item.hour for item in times)
    dates = Counter(item.date().isoformat() for item in times)
    weekdays = Counter(item.strftime("%a") for item in times)
    return {
        "top_hours": top_items(hours, limit=6),
        "top_dates": top_items(dates, limit=6),
        "weekday_breakdown": top_items(weekdays, limit=7),
    }


def summarize_daily_profile(times: list[datetime]) -> dict[str, object]:
    if not times:
        return {
            "trading_days": 0,
            "median_bars_per_day": None,
            "p10_bars_per_day": None,
            "p90_bars_per_day": None,
            "median_first_bar_utc": "n/a",
            "median_last_bar_utc": "n/a",
        }

    by_day: dict[str, list[datetime]] = defaultdict(list)
    for value in times:
        by_day[value.date().isoformat()].append(value)

    counts: list[int] = []
    first_minutes: list[int] = []
    last_minutes: list[int] = []
    for values in by_day.values():
        values.sort()
        counts.append(len(values))
        first_minutes.append(values[0].hour * 60 + values[0].minute)
        last_minutes.append(values[-1].hour * 60 + values[-1].minute)

    return {
        "trading_days": len(by_day),
        "median_bars_per_day": quantile_as_int(counts, 0.50),
        "p10_bars_per_day": quantile_as_int(counts, 0.10),
        "p90_bars_per_day": quantile_as_int(counts, 0.90),
        "median_first_bar_utc": format_clock(quantile_as_int(first_minutes, 0.50)),
        "median_last_bar_utc": format_clock(quantile_as_int(last_minutes, 0.50)),
    }


def raw_missing_profile(base_times: list[datetime], ext_times: list[datetime]) -> tuple[list[datetime], int]:
    ext_set = set(ext_times)
    missing: list[datetime] = []
    recoverable_stale1 = 0
    ordered_ext = sorted(ext_times)

    for base_time in base_times:
        if base_time in ext_set:
            continue
        missing.append(base_time)
        index = bisect_right(ordered_ext, base_time) - 1
        if index < 0:
            continue
        prev_time = ordered_ext[index]
        stale_bars = int((base_time - prev_time) / BAR_STEP)
        if stale_bars == 1 and prev_time.date() == base_time.date():
            recoverable_stale1 += 1

    return missing, recoverable_stale1


def recorded_mismatch_times(rows: list[dict[str, object]]) -> dict[str, list[datetime]]:
    by_symbol: dict[str, list[datetime]] = defaultdict(list)
    prefix = "EXTERNAL_TIMESTAMP_MISMATCH_"
    for row in rows:
        skip_reason = str(row.get("skip_reason", ""))
        if not skip_reason.startswith(prefix):
            continue
        by_symbol[skip_reason.replace(prefix, "")].append(row["bar_time_dt"])
    return by_symbol


def analyze_symbol(
    symbol: str,
    base_times: list[datetime],
    recorded_times: list[datetime],
    ext_times: list[datetime],
) -> dict[str, object]:
    raw_missing_times, stale1_recoverable = raw_missing_profile(base_times, ext_times)
    raw_missing_count = len(raw_missing_times)
    recorded_count = len(recorded_times)
    base_count = len(base_times)
    return {
        "recorded_mismatch_count": recorded_count,
        "recorded_mismatch_share_of_base": round(recorded_count / base_count, 6) if base_count else None,
        "recorded_temporal_shape": summarize_temporal_shape(recorded_times),
        "recorded_streaks": summarize_streaks(recorded_times),
        "raw_exact_missing_count": raw_missing_count,
        "raw_exact_missing_share_of_base": round(raw_missing_count / base_count, 6) if base_count else None,
        "recorded_share_of_raw_missing": round(recorded_count / raw_missing_count, 6) if raw_missing_count else None,
        "stale1_recoverable_count": stale1_recoverable,
        "stale1_recoverable_share_of_raw_missing": round(stale1_recoverable / raw_missing_count, 6)
        if raw_missing_count
        else None,
        "raw_missing_temporal_shape": summarize_temporal_shape(raw_missing_times),
        "raw_missing_streaks": summarize_streaks(raw_missing_times),
        "raw_daily_profile": summarize_daily_profile(ext_times),
    }


def analyze_split(split_name: str, summary_path: Path) -> dict[str, object]:
    summary = load_json(summary_path)
    shadow_path = Path(summary["csv_log_path"])
    rows = load_shadow_rows(shadow_path)
    base_times = unique_base_times(rows)
    recorded_by_symbol = recorded_mismatch_times(rows)
    symbols = sorted(set(FOCUS_SYMBOLS) | set(recorded_by_symbol))

    split_result = {
        "split_name": split_name,
        "summary_path": str(summary_path),
        "shadow_csv": str(shadow_path),
        "run_name": RUN_NAME,
        "base_bar_count": len(base_times),
        "date_window": summary.get("date_window", {}),
        "runtime_metrics": {
            "skip_rate": summary.get("governance_metrics", {}).get("latest_operational_skip_rate"),
            "external_skip_rate": summary.get("governance_metrics", {}).get("latest_external_skip_rate"),
            "external_mismatch_count": summary.get("metrics", {}).get("external_mismatch_count"),
            "top_skip_reasons": top_items_from_mapping(summary.get("metrics", {}).get("skip_reason_breakdown", {}), limit=8),
        },
        "symbols": {},
    }

    start_dt = base_times[0]
    end_dt = base_times[-1]
    for symbol in symbols:
        ext_times = load_symbol_times(symbol, start_dt, end_dt)
        split_result["symbols"][symbol] = analyze_symbol(
            symbol=symbol,
            base_times=base_times,
            recorded_times=recorded_by_symbol.get(symbol, []),
            ext_times=ext_times,
        )

    return split_result


def classify_symbol_overview(payload: dict, symbol: str) -> dict[str, object]:
    runtime_counts = {
        split_name: split_payload["symbols"].get(symbol, {}).get("recorded_mismatch_count", 0)
        for split_name, split_payload in payload["splits"].items()
    }
    stale_shares = [
        split_payload["symbols"][symbol]["stale1_recoverable_share_of_raw_missing"]
        for split_payload in payload["splits"].values()
        if symbol in split_payload["symbols"]
        and split_payload["symbols"][symbol]["stale1_recoverable_share_of_raw_missing"] is not None
    ]
    daily_bars = [
        split_payload["symbols"][symbol]["raw_daily_profile"]["median_bars_per_day"]
        for split_payload in payload["splits"].values()
        if symbol in split_payload["symbols"]
        and split_payload["symbols"][symbol]["raw_daily_profile"]["median_bars_per_day"] is not None
    ]
    p90_streaks = [
        split_payload["symbols"][symbol]["raw_missing_streaks"]["p90"]
        for split_payload in payload["splits"].values()
        if symbol in split_payload["symbols"] and split_payload["symbols"][symbol]["raw_missing_streaks"]["p90"] is not None
    ]
    top_split = max(runtime_counts.items(), key=lambda item: item[1])
    return {
        "top_runtime_split": top_split[0],
        "top_runtime_count": top_split[1],
        "mean_stale1_recoverable_share": round(sum(stale_shares) / len(stale_shares), 4) if stale_shares else None,
        "median_daily_bars_across_splits": quantile_as_int(daily_bars, 0.50) if daily_bars else None,
        "median_raw_p90_streak_across_splits": quantile_as_int(p90_streaks, 0.50) if p90_streaks else None,
    }


def build_interpretation(payload: dict) -> list[str]:
    overview = payload["symbol_overview"]
    vix = overview["VIX"]
    us10yr = overview["US10YR"]
    aapl = overview["AAPL.xnas"]
    usdx = overview["USDX"]
    return [
        (
            f"`VIX` is a real sparse-feed problem, not a one-off calendar glitch: its largest runtime pressure lands on "
            f"`{vix['top_runtime_split']}` with `{vix['top_runtime_count']}` recorded mismatches, while the raw missing "
            f"streak p90 stays around `{vix['median_raw_p90_streak_across_splits']}` bars across the analyzed windows."
        ),
        (
            f"`US10YR` becomes the main macro runtime pressure on `{us10yr['top_runtime_split']}` with "
            f"`{us10yr['top_runtime_count']}` recorded mismatches. The source shape is mostly short holes plus date-local "
            f"clusters, which fits holiday / feed-quality pockets better than a strategy-specific bug."
        ),
        (
            f"`AAPL.xnas` is structurally session-bound rather than mysteriously sparse: median bars per day stay around "
            f"`{aapl['median_daily_bars_across_splits']}`, far below the US100 base cadence, so its mismatches are expected "
            f"outside its narrower CFD session."
        ),
        (
            f"`USDX` looks like a scheduled closure artifact more than a macro anomaly: the raw missing streak p90 sits near "
            f"`{usdx['median_raw_p90_streak_across_splits']}` bars and repeats in the same overnight pocket."
        ),
        (
            f"A one-bar same-day stale fallback is symbol-specific rather than broadly safe: `VIX` only recovers about "
            f"`{vix['mean_stale1_recoverable_share']}` of raw exact misses on average, while `US10YR` sits nearer "
            f"`{us10yr['mean_stale1_recoverable_share']}`. That split is exactly why a whole-workspace relaxation story is "
            f"too blunt for the regular lane."
        ),
        (
            "Current read: keep `exact alignment + all-or-skip` as the operating contract, keep the old stale-bar branch "
            "closed as a promotion path, and treat any future relaxation as a tightly scoped diagnostic for `VIX` / "
            "`US10YR` only after separate feed-health evidence is gathered."
        ),
    ]


def render_split_table(split_payload: dict) -> list[str]:
    lines = [
        "| symbol | runtime mismatches | raw exact misses | runtime/raw | stale1 recoverable | stale1/raw | raw p90 streak | raw max streak | median bars/day | median first-last UTC |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    for symbol in FOCUS_SYMBOLS:
        metrics = split_payload["symbols"].get(symbol)
        if not metrics:
            continue
        daily = metrics["raw_daily_profile"]
        lines.append(
            "| `{}` | `{}` | `{}` | `{}` | `{}` | `{}` | `{}` | `{}` | `{}` | `{}` -> `{}` |".format(
                symbol,
                metrics["recorded_mismatch_count"],
                metrics["raw_exact_missing_count"],
                metrics["recorded_share_of_raw_missing"],
                metrics["stale1_recoverable_count"],
                metrics["stale1_recoverable_share_of_raw_missing"],
                metrics["raw_missing_streaks"]["p90"],
                metrics["raw_missing_streaks"]["max"],
                daily["median_bars_per_day"],
                daily["median_first_bar_utc"],
                daily["median_last_bar_utc"],
            )
        )
    return lines


def render_runtime_cluster_notes(split_payload: dict) -> list[str]:
    lines: list[str] = []
    for symbol in ["VIX", "US10YR", "AAPL.xnas", "USDX"]:
        metrics = split_payload["symbols"].get(symbol)
        if not metrics:
            continue
        top_dates = metrics["recorded_temporal_shape"]["top_dates"][:3]
        top_hours = metrics["recorded_temporal_shape"]["top_hours"][:4]
        top_streaks = metrics["recorded_streaks"]["top_streaks"][:3]
        lines.append(
            "- `{}` runtime clusters: top dates `{}`, top hours `{}`, top streaks `{}`".format(
                symbol,
                [(item["key"], item["count"]) for item in top_dates],
                [(item["key"], item["count"]) for item in top_hours],
                [(item["start"], item["end"], item["length"]) for item in top_streaks],
            )
        )
    return lines


def to_markdown(payload: dict) -> str:
    lines: list[str] = []
    lines.append("# Stage 30 Macro Mismatch Root-Cause Review")
    lines.append("")
    lines.append("- reviewed_on: `2026-04-12`")
    lines.append("- stage: `30_macro_mismatch_root_cause`")
    lines.append("- purpose: `diagnostic sidecar for clustered macro mismatch pressure; not a promotion lane`")
    lines.append(f"- analyzed_reference_run: `{RUN_NAME}`")
    lines.append("- operating contract reminder: `keep exact alignment + all-or-skip as the live rule unless a new contract hypothesis clears a separate diagnostic gate`")
    lines.append("")
    lines.append("## Setup")
    lines.append("")
    lines.append("- runtime evidence source: `29N` validation / test / hist_2024 shadow logs")
    lines.append("- raw evidence source: `data/raw/mt5_bars/m5/<symbol>` exact timestamp coverage against the Stage 29 base-bar timeline")
    lines.append("- focus symbols: `VIX`, `US10YR`, plus `AAPL.xnas` / `USDX` as structural context controls")
    lines.append("")

    for split_name in ["hist_2024", "validation", "test"]:
        split_payload = payload["splits"][split_name]
        lines.append(f"## {split_name}")
        lines.append("")
        lines.append(
            "- window: `{} -> {}`".format(
                split_payload["date_window"].get("from_date"),
                split_payload["date_window"].get("to_date"),
            )
        )
        lines.append(
            "- runtime headline: `base_bars={}`, `recorded_external_mismatches={}`".format(
                split_payload["base_bar_count"],
                split_payload["runtime_metrics"]["external_mismatch_count"],
            )
        )
        lines.append("")
        lines.extend(render_split_table(split_payload))
        lines.append("")
        lines.extend(render_runtime_cluster_notes(split_payload))
        lines.append("")

    lines.append("## Interpretation")
    lines.append("")
    for item in payload["interpretation"]:
        lines.append(f"- {item}")
    lines.append("")
    lines.append("## Decision")
    lines.append("")
    lines.append("- keep `exact alignment + all-or-skip` as the operating contract")
    lines.append("- keep broad stale-bar relaxation closed as a promotion path")
    lines.append("- if this branch reopens, scope it to a feed-health diagnostic on `VIX` / `US10YR`, not to a workspace-wide alignment relaxation")
    lines.append("- do not treat `AAPL.xnas` or `USDX` mismatches as evidence for macro stale fallback; they are structural session-shape controls")
    lines.append("")
    lines.append("## Report Refs")
    lines.append("")
    for split_name, split_payload in payload["splits"].items():
        lines.append(f"- `{split_name}` summary: `{split_payload['summary_path']}`")
        lines.append(f"- `{split_name}` shadow csv: `{split_payload['shadow_csv']}`")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    payload = {
        "reviewed_on": "2026-04-12",
        "stage": "30_macro_mismatch_root_cause",
        "reference_run": RUN_NAME,
        "splits": {
            split_name: analyze_split(split_name, path)
            for split_name, path in SUMMARY_PATHS.items()
        },
    }
    payload["symbol_overview"] = {
        symbol: classify_symbol_overview(payload, symbol)
        for symbol in FOCUS_SYMBOLS
    }
    payload["interpretation"] = build_interpretation(payload)

    OUTPUT_JSON.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    OUTPUT_MD.write_text(to_markdown(payload), encoding="utf-8")
    print(f"Wrote {OUTPUT_JSON}")
    print(f"Wrote {OUTPUT_MD}")


if __name__ == "__main__":
    main()
