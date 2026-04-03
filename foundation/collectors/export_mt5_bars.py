#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterator

import MetaTrader5 as mt5
import pandas as pd


UTC = timezone.utc
TIMEFRAME_MAP = {
    "M1": mt5.TIMEFRAME_M1,
    "M5": mt5.TIMEFRAME_M5,
    "M15": mt5.TIMEFRAME_M15,
    "M30": mt5.TIMEFRAME_M30,
    "H1": mt5.TIMEFRAME_H1,
    "H4": mt5.TIMEFRAME_H4,
    "D1": mt5.TIMEFRAME_D1,
}


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


def parse_utc(value: str | None) -> datetime | None:
    if value is None:
        return None
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=UTC)
    return parsed.astimezone(UTC)


def timeframe_value(label: str) -> int:
    key = label.upper()
    if key not in TIMEFRAME_MAP:
        raise ValueError(f"unsupported timeframe: {label}")
    return TIMEFRAME_MAP[key]


def timeframe_folder(label: str) -> str:
    return label.lower()


def find_earliest_bar(symbol: str, timeframe: int) -> datetime:
    # MT5 returns the first available bar when the requested range starts before history.
    probe_start = datetime(2000, 1, 1, tzinfo=UTC)
    probe_end = datetime(2000, 2, 1, tzinfo=UTC)
    rates = mt5.copy_rates_range(symbol, timeframe, probe_start, probe_end)
    if rates is None or len(rates) == 0:
        raise RuntimeError(f"no history returned for {symbol}")
    return datetime.fromtimestamp(int(rates[0]["time"]), tz=UTC)


def export_window(symbol: str, timeframe: int, window: Window, out_file: Path) -> tuple[int, str | None, str | None]:
    rates = mt5.copy_rates_range(symbol, timeframe, window.start, window.end)
    if rates is None:
        raise RuntimeError(
            f"copy_rates_range returned None for {symbol} {window.start.isoformat()}..{window.end.isoformat()}"
        )

    if len(rates) == 0:
        return 0, None, None

    df = pd.DataFrame(rates)
    df.insert(0, "time_utc", pd.to_datetime(df["time"], unit="s", utc=True))

    out_file.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(out_file, index=False, compression="zstd")

    first_bar = df.iloc[0]["time_utc"].isoformat()
    last_bar = df.iloc[-1]["time_utc"].isoformat()
    return len(df), first_bar, last_bar


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Export MT5 bars for one or more symbols.")
    parser.add_argument("--symbols", nargs="+", required=True, help="Exact MT5 symbol names")
    parser.add_argument("--timeframe", default="M5", help="Timeframe label, default: M5")
    parser.add_argument(
        "--out-dir",
        default="data/raw/mt5_bars",
        help="Root directory where symbol/timeframe parquet files and manifests will be stored",
    )
    parser.add_argument("--start", default=None, help="Optional UTC ISO timestamp override")
    parser.add_argument("--end", default=None, help="Optional UTC ISO timestamp override")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing monthly parquet files")
    return parser


def export_symbol(symbol: str, timeframe_label: str, timeframe: int, out_root: Path, start_override: datetime | None, end: datetime, overwrite: bool) -> dict:
    if mt5.symbol_info(symbol) is None:
        raise RuntimeError(f"symbol not found: {symbol}")
    if not mt5.symbol_select(symbol, True):
        raise RuntimeError(f"symbol_select failed for {symbol}: {mt5.last_error()}")

    earliest = find_earliest_bar(symbol, timeframe)
    start = max(start_override, earliest) if start_override else earliest
    if start >= end:
        raise RuntimeError(f"invalid range for {symbol}: start={start.isoformat()} end={end.isoformat()}")

    symbol_root = out_root / timeframe_folder(timeframe_label) / symbol
    manifest = {
        "symbol": symbol,
        "timeframe": timeframe_label.upper(),
        "source": "MT5 bars via MetaTrader5.copy_rates_range",
        "earliest_available_bar_utc": earliest.isoformat(),
        "export_started_at_utc": utc_now().isoformat(),
        "requested_start_utc": start.isoformat(),
        "requested_end_utc": end.isoformat(),
        "chunks": [],
    }

    total_rows = 0
    earliest_exported = None
    latest_exported = None

    for window in month_windows(start, end):
        year_dir = symbol_root / f"{window.start.year:04d}"
        out_file = year_dir / f"{symbol}_{timeframe_label.lower()}_{window.start:%Y-%m}.parquet"
        label = f"{window.start:%Y-%m}"

        if out_file.exists() and not overwrite:
            print(f"[skip] {symbol} {label} exists: {out_file}")
            continue

        count, first_bar, last_bar = export_window(symbol, timeframe, window, out_file)
        manifest["chunks"].append(
            {
                "month": label,
                "start_utc": window.start.isoformat(),
                "end_utc": window.end.isoformat(),
                "rows": count,
                "file": str(out_file.as_posix()) if count else None,
                "first_bar_utc": first_bar,
                "last_bar_utc": last_bar,
            }
        )

        total_rows += count
        if first_bar and earliest_exported is None:
            earliest_exported = first_bar
        if last_bar:
            latest_exported = last_bar

        print(f"[export] {symbol} {label}: rows={count} file={out_file if count else 'NO_FILE'}")

    manifest["total_rows"] = total_rows
    manifest["earliest_exported_bar_utc"] = earliest_exported
    manifest["latest_exported_bar_utc"] = latest_exported
    manifest["export_finished_at_utc"] = utc_now().isoformat()

    symbol_root.mkdir(parents=True, exist_ok=True)
    manifest_path = symbol_root / f"{symbol}_{timeframe_label.lower()}_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    print(f"[done] {symbol}: rows={total_rows} earliest={earliest_exported} latest={latest_exported}")
    return manifest


def main() -> int:
    args = build_parser().parse_args()
    out_root = Path(args.out_dir)
    timeframe_label = args.timeframe.upper()
    timeframe = timeframe_value(timeframe_label)
    start_override = parse_utc(args.start)
    end = parse_utc(args.end) or utc_now()

    if not mt5.initialize():
        raise RuntimeError(f"mt5.initialize failed: {mt5.last_error()}")

    try:
        manifests = []
        for symbol in args.symbols:
            manifests.append(
                export_symbol(
                    symbol=symbol,
                    timeframe_label=timeframe_label,
                    timeframe=timeframe,
                    out_root=out_root,
                    start_override=start_override,
                    end=end,
                    overwrite=args.overwrite,
                )
            )

        session_manifest = {
            "symbols": [m["symbol"] for m in manifests],
            "timeframe": timeframe_label,
            "export_finished_at_utc": utc_now().isoformat(),
        }
        session_manifest_path = out_root / timeframe_folder(timeframe_label) / f"session_manifest_{timeframe_label.lower()}.json"
        session_manifest_path.parent.mkdir(parents=True, exist_ok=True)
        session_manifest_path.write_text(json.dumps(session_manifest, indent=2), encoding="utf-8")
        print(f"[session] manifest={session_manifest_path}")
        return 0
    finally:
        mt5.shutdown()


if __name__ == "__main__":
    raise SystemExit(main())
