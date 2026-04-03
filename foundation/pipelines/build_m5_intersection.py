#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd


UTC = timezone.utc
DEFAULT_SYMBOLS = [
    "US100",
    "VIX",
    "US10YR",
    "USDX",
    "AAPL.xnas",
    "AMZN.xnas",
    "AMD.xnas",
    "GOOGL.xnas",
    "META.xnas",
    "MSFT.xnas",
    "NVDA.xnas",
    "TSLA.xnas",
]
VALUE_COLUMNS = ["open", "high", "low", "close", "tick_volume", "spread", "real_volume"]


def parse_utc(value: str) -> pd.Timestamp:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=UTC)
    else:
        parsed = parsed.astimezone(UTC)
    return pd.Timestamp(parsed)


def symbol_prefix(symbol: str) -> str:
    return symbol.lower().replace(".", "_")


def load_symbol_frame(root: Path, symbol: str, start: pd.Timestamp, end: pd.Timestamp) -> pd.DataFrame:
    symbol_root = root / symbol
    files = sorted(symbol_root.rglob("*.parquet"))
    if not files:
        raise FileNotFoundError(f"no parquet files found for symbol {symbol}: {symbol_root}")

    frames = []
    for path in files:
        df = pd.read_parquet(path, columns=["time_utc", *VALUE_COLUMNS])
        if df.empty:
            continue
        df["time_utc"] = pd.to_datetime(df["time_utc"], utc=True)
        df = df[(df["time_utc"] >= start) & (df["time_utc"] < end)]
        if not df.empty:
            frames.append(df)

    if not frames:
        raise RuntimeError(f"no rows found for symbol {symbol} in requested window")

    merged = pd.concat(frames, ignore_index=True)
    merged = merged.drop_duplicates(subset=["time_utc"]).sort_values("time_utc").reset_index(drop=True)

    prefix = symbol_prefix(symbol)
    rename_map = {column: f"{prefix}_{column}" for column in VALUE_COLUMNS}
    merged = merged.rename(columns=rename_map)
    return merged


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Build a timestamp intersection M5 dataset across MT5 symbols.")
    parser.add_argument(
        "--symbols",
        nargs="+",
        default=DEFAULT_SYMBOLS,
        help="Exact symbol list to align. Default is the FPMarkets v2 contract set.",
    )
    parser.add_argument("--start", default="2022-08-01T00:00:00Z", help="UTC ISO start timestamp, inclusive")
    parser.add_argument("--end", default="2026-03-01T00:00:00Z", help="UTC ISO end timestamp, exclusive")
    parser.add_argument("--raw-root", default="data/raw/mt5_bars/m5", help="Raw M5 parquet root")
    parser.add_argument(
        "--out-dir",
        default="data/processed/fpmarkets_v2/m5_intersection/extended_window",
        help="Output directory for aligned parquet and summary files",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    raw_root = Path(args.raw_root)
    out_dir = Path(args.out_dir)
    start = parse_utc(args.start)
    end = parse_utc(args.end)

    if start >= end:
        raise RuntimeError(f"invalid window: start={start.isoformat()} end={end.isoformat()}")

    symbol_frames: dict[str, pd.DataFrame] = {}
    summary = {
        "window_start_utc": start.isoformat(),
        "window_end_utc_exclusive": end.isoformat(),
        "symbols": args.symbols,
        "base_symbol": args.symbols[0],
        "per_symbol_rows": {},
        "join_steps": [],
    }

    for symbol in args.symbols:
        frame = load_symbol_frame(raw_root, symbol, start, end)
        symbol_frames[symbol] = frame
        summary["per_symbol_rows"][symbol] = int(len(frame))

    aligned = symbol_frames[args.symbols[0]].copy()
    for symbol in args.symbols[1:]:
        before_rows = len(aligned)
        aligned = aligned.merge(symbol_frames[symbol], on="time_utc", how="inner")
        after_rows = len(aligned)
        summary["join_steps"].append(
            {
                "symbol": symbol,
                "rows_before_join": int(before_rows),
                "rows_after_join": int(after_rows),
                "rows_removed": int(before_rows - after_rows),
            }
        )

    aligned = aligned.sort_values("time_utc").reset_index(drop=True)

    base_rows = len(symbol_frames[args.symbols[0]])
    summary["aligned_rows"] = int(len(aligned))
    summary["coverage_vs_base_pct"] = round((len(aligned) / base_rows) * 100, 6) if base_rows else 0.0
    summary["first_aligned_bar_utc"] = aligned.iloc[0]["time_utc"].isoformat() if len(aligned) else None
    summary["last_aligned_bar_utc"] = aligned.iloc[-1]["time_utc"].isoformat() if len(aligned) else None

    out_dir.mkdir(parents=True, exist_ok=True)
    start_tag = start.strftime("%Y-%m-%d")
    end_tag = (end - pd.Timedelta(minutes=5)).strftime("%Y-%m-%d")
    parquet_path = out_dir / f"fpmarkets_v2_m5_intersection_{start_tag}_{end_tag}.parquet"
    json_path = out_dir / f"fpmarkets_v2_m5_intersection_{start_tag}_{end_tag}_summary.json"

    aligned.to_parquet(parquet_path, index=False, compression="zstd")
    json_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    print(f"[done] aligned_rows={len(aligned)}")
    print(f"[done] coverage_vs_base_pct={summary['coverage_vs_base_pct']}")
    print(f"[done] first={summary['first_aligned_bar_utc']}")
    print(f"[done] last={summary['last_aligned_bar_utc']}")
    print(f"[done] parquet={parquet_path}")
    print(f"[done] summary={json_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
