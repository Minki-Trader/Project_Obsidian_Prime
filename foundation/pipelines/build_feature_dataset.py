#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

import numpy as np
import pandas as pd

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from foundation.features.catalog import (
    BARS_PER_YEAR_5M,
    DEFAULT_RAW_BARS_ROOT,
    DEFAULT_TOP3_WEIGHTS_PATH,
    FEATURE_ORDER,
    MEGA8_CLOSE_COLUMNS,
    TOP3_CLOSE_COLUMNS,
    TOP3_WEIGHT_COLUMNS,
)
from foundation.features.indicators import (
    adx,
    atr,
    ema,
    ppo_histogram,
    rolling_std,
    rolling_zscore,
    rsi,
    safe_divide,
    sma,
    stochastic_kd_diff,
    stochrsi_kd_diff,
    supertrend_state,
    trix,
    vortex_indicator,
)


UTC = timezone.utc
NY = ZoneInfo("America/New_York")
PARSER_VERSION = "fpmarkets_v2_feature_parser_v2"
REQUIRED_SYMBOLS = [
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


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Build FPMarkets v2 feature dataset from raw MT5 M5 bars.")
    parser.add_argument("--raw-root", default=str(DEFAULT_RAW_BARS_ROOT), help="Raw MT5 M5 parquet root")
    parser.add_argument("--weight-file", default=str(DEFAULT_TOP3_WEIGHTS_PATH), help="Monthly frozen top3 weights CSV")
    parser.add_argument("--start", default="2022-08-01T00:00:00Z", help="UTC ISO start timestamp, inclusive")
    parser.add_argument("--end", default="2026-03-01T00:00:00Z", help="UTC ISO end timestamp, exclusive")
    parser.add_argument(
        "--preload-days",
        type=int,
        default=60,
        help="Extra history window before start to stabilize rolling indicators",
    )
    parser.add_argument(
        "--out-dir",
        default="data/processed/fpmarkets_v2/features/extended_window",
        help="Directory for feature parquet, validity parquet, and summary JSON",
    )
    return parser


def parse_utc(value: str) -> pd.Timestamp:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=UTC)
    else:
        parsed = parsed.astimezone(UTC)
    return pd.Timestamp(parsed)


def load_symbol_ohlc(raw_root: Path, symbol: str, start: pd.Timestamp, end: pd.Timestamp) -> pd.DataFrame:
    symbol_root = raw_root / symbol
    files = sorted(symbol_root.rglob("*.parquet"))
    if not files:
        raise FileNotFoundError(f"missing raw parquet files for {symbol}: {symbol_root}")

    frames = []
    for path in files:
        df = pd.read_parquet(path, columns=["time_utc", "open", "high", "low", "close", "tick_volume", "spread", "real_volume"])
        if df.empty:
            continue
        df["time_utc"] = pd.to_datetime(df["time_utc"], utc=True)
        df = df[(df["time_utc"] >= start) & (df["time_utc"] < end)]
        if not df.empty:
            frames.append(df)

    if not frames:
        raise RuntimeError(f"no rows found for {symbol} in {start.isoformat()}..{end.isoformat()}")

    frame = pd.concat(frames, ignore_index=True)
    frame = frame.drop_duplicates(subset=["time_utc"]).sort_values("time_utc").reset_index(drop=True)
    frame["timestamp"] = frame["time_utc"] + pd.Timedelta(minutes=5)
    return frame


def load_weights(path: Path, months: pd.Series) -> pd.DataFrame:
    weights = pd.read_csv(path)
    expected = {"month", *TOP3_WEIGHT_COLUMNS}
    missing = expected.difference(weights.columns)
    if missing:
        raise RuntimeError(f"missing columns in {path}: {sorted(missing)}")

    month_frame = pd.DataFrame({"month": months.astype(str)})
    merged = month_frame.merge(weights, on="month", how="left")
    if merged[TOP3_WEIGHT_COLUMNS].isna().any().any():
        missing_months = sorted(merged.loc[merged[TOP3_WEIGHT_COLUMNS].isna().any(axis=1), "month"].unique().tolist())
        raise RuntimeError(f"missing top3 weights for months: {missing_months}")
    return merged[TOP3_WEIGHT_COLUMNS]


def merge_external_feature(base: pd.DataFrame, external: pd.DataFrame) -> pd.DataFrame:
    return base.merge(external, on="timestamp", how="left")


def build_base_us100_features(base: pd.DataFrame) -> pd.DataFrame:
    frame = base.copy()
    close = frame["us100_close"]
    open_ = frame["us100_open"]
    high = frame["us100_high"]
    low = frame["us100_low"]

    log_return_1 = np.log(close / close.shift(1))
    log_return_3 = np.log(close / close.shift(3))
    hl_range = safe_divide(high - low, close)
    atr_14 = atr(high, low, close, 14)
    atr_50 = atr(high, low, close, 50)
    atr_20 = atr(high, low, close, 20)

    ema9 = ema(close, 9)
    ema20 = ema(close, 20)
    ema50 = ema(close, 50)
    ema200 = ema(close, 200)
    sma50 = sma(close, 50)
    sma200 = sma(close, 200)
    rsi_14 = rsi(close, 14)
    rsi_50 = rsi(close, 50)
    adx_14, plus_di_14, minus_di_14 = adx(high, low, close, 14)

    bb_mid_20 = sma(close, 20)
    bb_std_20 = rolling_std(close, 20)
    bb_upper = bb_mid_20 + (2 * bb_std_20)
    bb_lower = bb_mid_20 - (2 * bb_std_20)
    kc_mid_20 = ema20
    kc_upper = kc_mid_20 + (1.5 * atr_20)
    kc_lower = kc_mid_20 - (1.5 * atr_20)

    historical_vol_20 = rolling_std(log_return_1, 20) * np.sqrt(BARS_PER_YEAR_5M)
    historical_vol_5 = rolling_std(log_return_1, 5) * np.sqrt(BARS_PER_YEAR_5M)

    frame["timestamp_ny"] = frame["timestamp"].dt.tz_convert(NY)
    frame["bar_open_ny"] = frame["time_utc"].dt.tz_convert(NY)
    frame["ny_date"] = frame["timestamp_ny"].dt.strftime("%Y-%m-%d")

    close_minutes = frame["timestamp_ny"].dt.hour * 60 + frame["timestamp_ny"].dt.minute
    minutes_from_open = close_minutes - (9 * 60 + 30)
    minutes_to_close = (16 * 60) - close_minutes

    frame["is_us_cash_open"] = ((minutes_from_open > 0) & (minutes_to_close >= 0)).astype(float)
    frame["minutes_from_cash_open"] = minutes_from_open.astype(float)
    frame["is_first_30m_after_open"] = ((minutes_from_open > 0) & (minutes_from_open <= 30)).astype(float)
    frame["is_last_30m_before_cash_close"] = ((minutes_to_close > 0) & (minutes_to_close <= 30)).astype(float)

    cash_open_rows = frame[frame["bar_open_ny"].dt.strftime("%H:%M").eq("09:30")]
    cash_close_rows = frame[frame["timestamp_ny"].dt.strftime("%H:%M").eq("16:00")]
    cash_open_by_date = cash_open_rows.groupby("ny_date")["us100_open"].first()
    cash_close_by_date = cash_close_rows.groupby("ny_date")["us100_close"].last()
    prev_cash_close = cash_close_by_date.shift(1)
    overnight_by_date = safe_divide(cash_open_by_date, prev_cash_close) - 1
    frame["overnight_return"] = frame["ny_date"].map(overnight_by_date)

    frame["log_return_1"] = log_return_1
    frame["log_return_3"] = log_return_3
    frame["hl_range"] = hl_range
    frame["close_open_ratio"] = safe_divide(close, open_)
    frame["gap_percent"] = safe_divide(open_, close.shift(1)) - 1
    frame["close_prev_close_ratio"] = safe_divide(close, close.shift(1))
    frame["return_zscore_20"] = rolling_zscore(log_return_1, 20)
    frame["hl_zscore_50"] = rolling_zscore(hl_range, 50)
    frame["return_1_over_atr_14"] = safe_divide((safe_divide(close, close.shift(1)) - 1), safe_divide(atr_14, close))
    frame["close_ema20_ratio"] = safe_divide(close, ema20)
    frame["close_ema50_ratio"] = safe_divide(close, ema50)
    frame["ema9_ema20_diff"] = ema9 - ema20
    frame["ema20_ema50_diff"] = ema20 - ema50
    frame["ema50_ema200_diff"] = ema50 - ema200
    frame["ema20_ema50_spread_zscore_50"] = rolling_zscore(frame["ema20_ema50_diff"], 50)
    frame["sma50_sma200_ratio"] = safe_divide(sma50, sma200)
    frame["rsi_14"] = rsi_14
    frame["rsi_50"] = rsi_50
    frame["rsi_14_slope_3"] = (rsi_14 - rsi_14.shift(3)) / 3
    frame["rsi_14_minus_50"] = rsi_14 - 50
    frame["stoch_kd_diff"] = stochastic_kd_diff(high, low, close)
    frame["stochrsi_kd_diff"] = stochrsi_kd_diff(close)
    frame["ppo_hist_12_26_9"] = ppo_histogram(close)
    frame["roc_12"] = safe_divide(close, close.shift(12)) - 1
    frame["trix_15"] = trix(close, 15)
    frame["atr_14"] = atr_14
    frame["atr_50"] = atr_50
    frame["atr_14_over_atr_50"] = safe_divide(atr_14, atr_50)
    frame["bollinger_width_20"] = safe_divide(bb_upper - bb_lower, bb_mid_20)
    frame["bb_position_20"] = safe_divide(close - bb_lower, bb_upper - bb_lower)
    squeeze_valid = bb_upper.notna() & bb_lower.notna() & kc_upper.notna() & kc_lower.notna()
    frame["bb_squeeze"] = ((bb_upper <= kc_upper) & (bb_lower >= kc_lower)).astype(float).mask(~squeeze_valid)
    frame["historical_vol_20"] = historical_vol_20
    frame["historical_vol_5_over_20"] = safe_divide(historical_vol_5, historical_vol_20)
    frame["adx_14"] = adx_14
    frame["di_spread_14"] = plus_di_14 - minus_di_14
    frame["supertrend_10_3"] = supertrend_state(high, low, close, 10, 3.0)
    frame["vortex_indicator"] = vortex_indicator(high, low, close, 14)
    frame["us100_simple_return_1"] = safe_divide(close, close.shift(1)) - 1
    return frame


def build_external_frames(raw_root: Path, preload_start: pd.Timestamp, end: pd.Timestamp) -> dict[str, pd.DataFrame]:
    frames: dict[str, pd.DataFrame] = {}

    risk_map = {
        "VIX": ("vix_change_1", "vix_zscore_20", "vix_close"),
        "US10YR": ("us10yr_change_1", "us10yr_zscore_20", "us10yr_close"),
        "USDX": ("usdx_change_1", "usdx_zscore_20", "usdx_close"),
    }
    for symbol, (change_col, zscore_col, close_col) in risk_map.items():
        raw = load_symbol_ohlc(raw_root, symbol, preload_start, end)
        out = raw[["timestamp"]].copy()
        out[change_col] = safe_divide(raw["close"], raw["close"].shift(1)) - 1
        out[zscore_col] = rolling_zscore(raw["close"], 20)
        out[close_col] = raw["close"]
        frames[symbol] = out

    stock_symbols = [
        "AAPL.xnas",
        "AMZN.xnas",
        "AMD.xnas",
        "GOOGL.xnas",
        "META.xnas",
        "MSFT.xnas",
        "NVDA.xnas",
        "TSLA.xnas",
    ]
    for symbol in stock_symbols:
        raw = load_symbol_ohlc(raw_root, symbol, preload_start, end)
        prefix = symbol.lower().replace(".", "_")
        out = raw[["timestamp"]].copy()
        out[f"{prefix}_close"] = raw["close"]
        out[f"{prefix}_simple_return_1"] = safe_divide(raw["close"], raw["close"].shift(1)) - 1
        out[f"{prefix}_simple_return_5"] = safe_divide(raw["close"], raw["close"].shift(5)) - 1
        if symbol in {"AAPL.xnas", "AMZN.xnas", "MSFT.xnas", "NVDA.xnas"}:
            out[f"{prefix}_log_return_1"] = np.log(raw["close"] / raw["close"].shift(1))
        frames[symbol] = out

    return frames


def assemble_feature_frame(raw_root: Path, weight_file: Path, start: pd.Timestamp, end: pd.Timestamp, preload_days: int) -> tuple[pd.DataFrame, pd.DataFrame]:
    preload_start = start - pd.Timedelta(days=preload_days)

    us100_raw = load_symbol_ohlc(raw_root, "US100", preload_start, end)
    base = us100_raw.rename(
        columns={
            "open": "us100_open",
            "high": "us100_high",
            "low": "us100_low",
            "close": "us100_close",
            "tick_volume": "us100_tick_volume",
            "spread": "us100_spread",
            "real_volume": "us100_real_volume",
        }
    )
    base = build_base_us100_features(base)

    external_frames = build_external_frames(raw_root, preload_start, end)
    for frame in external_frames.values():
        base = merge_external_feature(base, frame)

    weights = load_weights(weight_file, base["timestamp"].dt.strftime("%Y-%m"))
    base[TOP3_WEIGHT_COLUMNS] = weights

    mega8_returns_1 = pd.DataFrame({column: base[f"{column.replace('_close', '')}_simple_return_1"] for column in MEGA8_CLOSE_COLUMNS})
    mega8_returns_5 = pd.DataFrame({column: base[f"{column.replace('_close', '')}_simple_return_5"] for column in MEGA8_CLOSE_COLUMNS})

    base["vix_change_1"] = base["vix_change_1"]
    base["vix_zscore_20"] = base["vix_zscore_20"]
    base["us10yr_change_1"] = base["us10yr_change_1"]
    base["us10yr_zscore_20"] = base["us10yr_zscore_20"]
    base["usdx_change_1"] = base["usdx_change_1"]
    base["usdx_zscore_20"] = base["usdx_zscore_20"]

    base["nvda_xnas_log_return_1"] = base["nvda_xnas_log_return_1"]
    base["aapl_xnas_log_return_1"] = base["aapl_xnas_log_return_1"]
    base["msft_xnas_log_return_1"] = base["msft_xnas_log_return_1"]
    base["amzn_xnas_log_return_1"] = base["amzn_xnas_log_return_1"]
    base["mega8_equal_return_1"] = mega8_returns_1.mean(axis=1, skipna=False)
    base["top3_weighted_return_1"] = (
        (base["msft_xnas_simple_return_1"] * base["msft_xnas_weight"])
        + (base["nvda_xnas_simple_return_1"] * base["nvda_xnas_weight"])
        + (base["aapl_xnas_simple_return_1"] * base["aapl_xnas_weight"])
    )
    base["mega8_pos_breadth_1"] = mega8_returns_1.gt(0).mean(axis=1, skipna=False)
    base["mega8_dispersion_5"] = mega8_returns_5.std(axis=1, ddof=0, skipna=False)
    base["us100_minus_mega8_equal_return_1"] = base["us100_simple_return_1"] - base["mega8_equal_return_1"]
    base["us100_minus_top3_weighted_return_1"] = base["us100_simple_return_1"] - base["top3_weighted_return_1"]

    trimmed = base[(base["time_utc"] >= start) & (base["time_utc"] < end)].copy()
    output = trimmed[["timestamp"]].copy()
    output.insert(1, "symbol", "US100")
    output[FEATURE_ORDER] = trimmed[FEATURE_ORDER]

    invalid_feature_count = output[FEATURE_ORDER].isna().sum(axis=1)
    validity = pd.DataFrame(
        {
            "timestamp": output["timestamp"],
            "symbol": output["symbol"],
            "is_feature_row_valid": invalid_feature_count.eq(0),
            "invalid_feature_count": invalid_feature_count.astype("int32"),
        }
    )

    output[FEATURE_ORDER] = output[FEATURE_ORDER].astype("float32")
    return output, validity


def main() -> int:
    args = build_parser().parse_args()
    raw_root = Path(args.raw_root)
    weight_path = Path(args.weight_file)
    start = parse_utc(args.start)
    end = parse_utc(args.end)
    out_dir = Path(args.out_dir)

    features, validity = assemble_feature_frame(
        raw_root=raw_root,
        weight_file=weight_path,
        start=start,
        end=end,
        preload_days=args.preload_days,
    )

    out_dir.mkdir(parents=True, exist_ok=True)
    features_path = out_dir / "feature_matrix.parquet"
    validity_path = out_dir / "feature_validity.parquet"
    summary_path = out_dir / "feature_build_summary.json"

    features.to_parquet(features_path, index=False, compression="zstd")
    validity.to_parquet(validity_path, index=False, compression="zstd")

    valid_mask = validity["is_feature_row_valid"]
    summary = {
        "parser_version": PARSER_VERSION,
        "raw_root": str(raw_root.as_posix()),
        "weights_path": str(weight_path.as_posix()),
        "window_start_utc": start.isoformat(),
        "window_end_utc_exclusive": end.isoformat(),
        "output_features_path": str(features_path.as_posix()),
        "output_validity_path": str(validity_path.as_posix()),
        "feature_count": len(FEATURE_ORDER),
        "feature_order_hash_sha256": hashlib.sha256(",".join(FEATURE_ORDER).encode("utf-8")).hexdigest(),
        "row_count": int(len(features)),
        "valid_row_count": int(valid_mask.sum()),
        "invalid_row_count": int((~valid_mask).sum()),
        "first_timestamp_utc": features["timestamp"].iloc[0].isoformat() if len(features) else None,
        "last_timestamp_utc": features["timestamp"].iloc[-1].isoformat() if len(features) else None,
        "first_valid_timestamp_utc": features.loc[valid_mask, "timestamp"].iloc[0].isoformat() if valid_mask.any() else None,
        "top3_weights_note": "Static monthly frozen table supplied locally. Current file uses equal weights for MSFT/NVDA/AAPL as a placeholder contract artifact.",
        "generated_at_utc": datetime.now(UTC).isoformat(),
    }
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    print(f"[done] rows={summary['row_count']}")
    print(f"[done] valid_rows={summary['valid_row_count']}")
    print(f"[done] first_valid_timestamp={summary['first_valid_timestamp_utc']}")
    print(f"[done] features={features_path}")
    print(f"[done] validity={validity_path}")
    print(f"[done] summary={summary_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
