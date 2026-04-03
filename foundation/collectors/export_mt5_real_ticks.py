#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Iterator

import MetaTrader5 as mt5
import pandas as pd


UTC = timezone.utc


@dataclass(frozen=True)
class Window:
    start: datetime
    end: datetime


def utc_now() -> datetime:
    return datetime.now(UTC)


def month_windows(start: datetime, end: datetime) -> Iterator[Window]:
    cursor = datetime(start.year, start.month, 1, tzinfo=UTC)
    while cursor < end:
        if cursor.month == 12:
            next_month = datetime(cursor.year + 1, 1, 1, tzinfo=UTC)
        else:
            next_month = datetime(cursor.year, cursor.month + 1, 1, tzinfo=UTC)
        yield Window(start=max(start, cursor), end=min(end, next_month))
        cursor = next_month


def tick_count(symbol: str, start: datetime, end: datetime) -> int:
    ticks = mt5.copy_ticks_range(symbol, start, end, mt5.COPY_TICKS_ALL)
    return 0 if ticks is None else len(ticks)


def first_tick_for_day(symbol: str, start: datetime) -> datetime:
    end = start + timedelta(days=1)
    ticks = mt5.copy_ticks_range(symbol, start, end, mt5.COPY_TICKS_ALL)
    if ticks is None or len(ticks) == 0:
        raise RuntimeError(f"no ticks found for day window starting {start.isoformat()}")
    return datetime.fromtimestamp(int(ticks[0]["time"]), tz=UTC)


def find_earliest_tick(symbol: str, year_start: int = 2000) -> datetime:
    now = utc_now()
    first_year = None

    for year in range(year_start, now.year + 1):
        start = datetime(year, 1, 1, tzinfo=UTC)
        end = datetime(year + 1, 1, 1, tzinfo=UTC) if year < now.year else now
        count = tick_count(symbol, start, end)
        print(f"[scan-year] {year}: {count}")
        if count:
            first_year = year
            break

    if first_year is None:
        raise RuntimeError(f"no tick history found for {symbol}")

    first_month = None
    for month in range(1, 13):
        start = datetime(first_year, month, 1, tzinfo=UTC)
        if month == 12:
            end = datetime(first_year + 1, 1, 1, tzinfo=UTC)
        else:
            end = datetime(first_year, month + 1, 1, tzinfo=UTC)
        count = tick_count(symbol, start, end)
        print(f"[scan-month] {start:%Y-%m}: {count}")
        if count:
            first_month = month
            break

    if first_month is None:
        raise RuntimeError(f"failed to refine first month for {symbol}")

    probe = datetime(first_year, first_month, 1, tzinfo=UTC)
    while True:
        day_count = tick_count(symbol, probe, probe + timedelta(days=1))
        print(f"[scan-day] {probe:%Y-%m-%d}: {day_count}")
        if day_count:
            return first_tick_for_day(symbol, probe)
        probe += timedelta(days=1)


def export_window(symbol: str, window: Window, out_file: Path) -> tuple[int, str | None, str | None]:
    ticks = mt5.copy_ticks_range(symbol, window.start, window.end, mt5.COPY_TICKS_ALL)
    if ticks is None:
        raise RuntimeError(f"copy_ticks_range returned None for {window.start.isoformat()}..{window.end.isoformat()}")

    if len(ticks) == 0:
        return 0, None, None

    df = pd.DataFrame(ticks)
    df.insert(0, "time_utc", pd.to_datetime(df["time_msc"], unit="ms", utc=True))

    out_file.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(out_file, index=False, compression="zstd")

    first_tick = df.iloc[0]["time_utc"].isoformat()
    last_tick = df.iloc[-1]["time_utc"].isoformat()
    return len(df), first_tick, last_tick


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Export MT5 broker real ticks to parquet files.")
    parser.add_argument("--symbol", default="US100", help="MT5 symbol name")
    parser.add_argument(
        "--out-dir",
        default="data/raw/us100/real_ticks",
        help="Directory where parquet files and manifest will be stored",
    )
    parser.add_argument(
        "--start",
        default=None,
        help="Optional UTC ISO timestamp override. If omitted, the script finds the earliest available tick.",
    )
    parser.add_argument(
        "--end",
        default=None,
        help="Optional UTC ISO timestamp override. If omitted, current UTC time is used.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing monthly parquet files",
    )
    return parser


def parse_utc(value: str | None) -> datetime | None:
    if value is None:
        return None
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=UTC)
    return parsed.astimezone(UTC)


def main() -> int:
    args = build_parser().parse_args()
    out_dir = Path(args.out_dir)

    if not mt5.initialize():
        raise RuntimeError(f"mt5.initialize failed: {mt5.last_error()}")

    try:
        if mt5.symbol_info(args.symbol) is None:
            raise RuntimeError(f"symbol not found: {args.symbol}")

        if not mt5.symbol_select(args.symbol, True):
            raise RuntimeError(f"symbol_select failed for {args.symbol}: {mt5.last_error()}")

        start = parse_utc(args.start) or find_earliest_tick(args.symbol)
        end = parse_utc(args.end) or utc_now()

        if start >= end:
            raise RuntimeError(f"invalid range: start={start.isoformat()} end={end.isoformat()}")

        manifest = {
            "symbol": args.symbol,
            "source": "MT5 real ticks via MetaTrader5.copy_ticks_range(COPY_TICKS_ALL)",
            "export_started_at_utc": utc_now().isoformat(),
            "requested_start_utc": start.isoformat(),
            "requested_end_utc": end.isoformat(),
            "chunks": [],
        }

        total_rows = 0
        earliest_exported = None
        latest_exported = None

        for window in month_windows(start, end):
            year_dir = out_dir / f"{window.start.year:04d}"
            out_file = year_dir / f"{args.symbol}_real_ticks_{window.start:%Y-%m}.parquet"
            label = f"{window.start:%Y-%m}"

            if out_file.exists() and not args.overwrite:
                print(f"[skip] {label} exists: {out_file}")
                continue

            count, first_tick, last_tick = export_window(args.symbol, window, out_file)
            manifest["chunks"].append(
                {
                    "month": label,
                    "start_utc": window.start.isoformat(),
                    "end_utc": window.end.isoformat(),
                    "rows": count,
                    "file": str(out_file.as_posix()),
                    "first_tick_utc": first_tick,
                    "last_tick_utc": last_tick,
                }
            )

            total_rows += count
            if first_tick and earliest_exported is None:
                earliest_exported = first_tick
            if last_tick:
                latest_exported = last_tick

            print(f"[export] {label}: rows={count} file={out_file}")

        manifest["total_rows"] = total_rows
        manifest["earliest_exported_tick_utc"] = earliest_exported
        manifest["latest_exported_tick_utc"] = latest_exported
        manifest["export_finished_at_utc"] = utc_now().isoformat()

        out_dir.mkdir(parents=True, exist_ok=True)
        manifest_path = out_dir / f"{args.symbol}_real_ticks_manifest.json"
        manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

        print(f"[done] rows={total_rows}")
        print(f"[done] earliest={earliest_exported}")
        print(f"[done] latest={latest_exported}")
        print(f"[done] manifest={manifest_path}")
        return 0
    finally:
        mt5.shutdown()


if __name__ == "__main__":
    raise SystemExit(main())
