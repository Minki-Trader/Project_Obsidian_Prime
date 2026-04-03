from __future__ import annotations

from foundation.features.catalog import FEATURE_ORDER


SECTOR_MAP: dict[str, list[str]] = {
    "price_return": [
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
    ],
    "moving_average_trend": [
        "close_ema20_ratio",
        "close_ema50_ratio",
        "ema9_ema20_diff",
        "ema20_ema50_diff",
        "ema50_ema200_diff",
        "ema20_ema50_spread_zscore_50",
        "sma50_sma200_ratio",
    ],
    "momentum_oscillator": [
        "rsi_14",
        "rsi_50",
        "rsi_14_slope_3",
        "rsi_14_minus_50",
        "stoch_kd_diff",
        "stochrsi_kd_diff",
        "ppo_hist_12_26_9",
        "roc_12",
        "trix_15",
    ],
    "volatility_band": [
        "atr_14",
        "atr_50",
        "atr_14_over_atr_50",
        "bollinger_width_20",
        "bb_position_20",
        "bb_squeeze",
        "historical_vol_20",
        "historical_vol_5_over_20",
    ],
    "trend_strength": [
        "adx_14",
        "di_spread_14",
        "supertrend_10_3",
        "vortex_indicator",
    ],
    "session_context": [
        "is_us_cash_open",
        "minutes_from_cash_open",
        "is_first_30m_after_open",
        "is_last_30m_before_cash_close",
    ],
    "risk_proxy": [
        "vix_change_1",
        "vix_zscore_20",
        "us10yr_change_1",
        "us10yr_zscore_20",
        "usdx_change_1",
        "usdx_zscore_20",
    ],
    "leader_relative": [
        "nvda_xnas_log_return_1",
        "aapl_xnas_log_return_1",
        "msft_xnas_log_return_1",
        "amzn_xnas_log_return_1",
        "mega8_equal_return_1",
        "top3_weighted_return_1",
        "us100_minus_mega8_equal_return_1",
        "us100_minus_top3_weighted_return_1",
    ],
    "breadth_dispersion": [
        "mega8_pos_breadth_1",
        "mega8_dispersion_5",
    ],
}


def validate_sector_map() -> None:
    flattened = [feature for features in SECTOR_MAP.values() for feature in features]
    if len(flattened) != len(set(flattened)):
        raise ValueError("sector map contains duplicated features")
    if set(flattened) != set(FEATURE_ORDER):
        missing = sorted(set(FEATURE_ORDER) - set(flattened))
        extra = sorted(set(flattened) - set(FEATURE_ORDER))
        raise ValueError(f"sector map mismatch missing={missing} extra={extra}")


def feature_order_without_sectors(removed_sectors: list[str] | tuple[str, ...]) -> list[str]:
    missing = [name for name in removed_sectors if name not in SECTOR_MAP]
    if missing:
        raise ValueError(f"unknown sector names: {missing}")

    removed_features = {feature for sector in removed_sectors for feature in SECTOR_MAP[sector]}
    active_features = [feature for feature in FEATURE_ORDER if feature not in removed_features]
    if not active_features:
        raise ValueError("active feature set is empty after removing requested sectors")
    return active_features
