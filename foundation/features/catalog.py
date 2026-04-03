from __future__ import annotations

from pathlib import Path


FEATURE_ORDER = [
    "log_return_1",
    "log_return_3",
    "hl_range",
    "close_open_ratio",
    "gap_percent",
    "close_prev_close_ratio",
    "return_zscore_20",
    "hl_zscore_50",
    "overnight_return",
    "return_1_over_atr_14",
    "close_ema20_ratio",
    "close_ema50_ratio",
    "ema9_ema20_diff",
    "ema20_ema50_diff",
    "ema50_ema200_diff",
    "ema20_ema50_spread_zscore_50",
    "sma50_sma200_ratio",
    "rsi_14",
    "rsi_50",
    "rsi_14_slope_3",
    "rsi_14_minus_50",
    "stoch_kd_diff",
    "stochrsi_kd_diff",
    "ppo_hist_12_26_9",
    "roc_12",
    "trix_15",
    "atr_14",
    "atr_50",
    "atr_14_over_atr_50",
    "bollinger_width_20",
    "bb_position_20",
    "bb_squeeze",
    "historical_vol_20",
    "historical_vol_5_over_20",
    "adx_14",
    "di_spread_14",
    "supertrend_10_3",
    "vortex_indicator",
    "is_us_cash_open",
    "minutes_from_cash_open",
    "is_first_30m_after_open",
    "is_last_30m_before_cash_close",
    "vix_change_1",
    "vix_zscore_20",
    "us10yr_change_1",
    "us10yr_zscore_20",
    "usdx_change_1",
    "usdx_zscore_20",
    "nvda_xnas_log_return_1",
    "aapl_xnas_log_return_1",
    "msft_xnas_log_return_1",
    "amzn_xnas_log_return_1",
    "mega8_equal_return_1",
    "top3_weighted_return_1",
    "mega8_pos_breadth_1",
    "mega8_dispersion_5",
    "us100_minus_mega8_equal_return_1",
    "us100_minus_top3_weighted_return_1",
]

MEGA8_CLOSE_COLUMNS = [
    "aapl_xnas_close",
    "amzn_xnas_close",
    "amd_xnas_close",
    "googl_xnas_close",
    "meta_xnas_close",
    "msft_xnas_close",
    "nvda_xnas_close",
    "tsla_xnas_close",
]

TOP3_CLOSE_COLUMNS = [
    "msft_xnas_close",
    "nvda_xnas_close",
    "aapl_xnas_close",
]

TOP3_WEIGHT_COLUMNS = [
    "msft_xnas_weight",
    "nvda_xnas_weight",
    "aapl_xnas_weight",
]

BARS_PER_YEAR_5M = 252 * 288
DEFAULT_TOP3_WEIGHTS_PATH = Path("foundation/config/top3_monthly_weights_fpmarkets_v2.csv")
DEFAULT_RAW_BARS_ROOT = Path("data/raw/mt5_bars/m5")
DEFAULT_INTERSECTION_PATH = Path(
    "data/processed/fpmarkets_v2/m5_intersection/extended_window/fpmarkets_v2_m5_intersection_2022-08-01_2026-02-28.parquet"
)
