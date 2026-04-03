from __future__ import annotations


TREND_PROXY_REPLACEMENT_NAME = "trend_proxy_regime"

TREND_PROXY_REPLACEMENT_COMPONENT_GROUPS: dict[str, list[str]] = {
    "trend_proxy_persistence": [
        "ema20_ema50_diff",
        "ema50_ema200_diff",
        "trix_15",
    ],
    "trend_proxy_volatility_regime": [
        "atr_14_over_atr_50",
        "historical_vol_5_over_20",
        "bb_squeeze",
    ],
    "trend_proxy_breakout_pressure": [
        "log_return_1",
        "return_1_over_atr_14",
        "hl_range",
    ],
    "trend_proxy_breadth_confirmation": [
        "top3_weighted_return_1",
        "mega8_pos_breadth_1",
        "mega8_dispersion_5",
    ],
    "trend_proxy_downside_pressure": [
        "close_ema20_ratio",
        "close_ema50_ratio",
        "overnight_return",
        "return_1_over_atr_14",
        "us100_minus_mega8_equal_return_1",
        "us100_minus_top3_weighted_return_1",
    ],
    "trend_proxy_risk_off_confirmation": [
        "vix_change_1",
        "vix_zscore_20",
        "us10yr_change_1",
        "us10yr_zscore_20",
        "usdx_change_1",
        "usdx_zscore_20",
    ],
    "trend_proxy_leader_drag": [
        "nvda_xnas_log_return_1",
        "aapl_xnas_log_return_1",
        "msft_xnas_log_return_1",
        "amzn_xnas_log_return_1",
        "mega8_equal_return_1",
        "mega8_pos_breadth_1",
        "mega8_dispersion_5",
    ],
    "trend_proxy_session_pressure": [
        "minutes_from_cash_open",
        "is_first_30m_after_open",
        "is_last_30m_before_cash_close",
        "overnight_return",
        "gap_percent",
    ],
}


def parse_replacement_component_groups(raw_value: str) -> list[str]:
    group_names = [item.strip() for item in raw_value.split(",") if item.strip()]
    missing = [name for name in group_names if name not in TREND_PROXY_REPLACEMENT_COMPONENT_GROUPS]
    if missing:
        raise ValueError(f"unknown replacement component groups: {missing}")
    return group_names


def resolve_replacement_component_groups(selected_groups: list[str] | tuple[str, ...] | None = None) -> dict[str, list[str]]:
    if not selected_groups:
        return dict(TREND_PROXY_REPLACEMENT_COMPONENT_GROUPS)
    return {name: TREND_PROXY_REPLACEMENT_COMPONENT_GROUPS[name] for name in selected_groups}


def replacement_source_features() -> list[str]:
    ordered: list[str] = []
    for features in TREND_PROXY_REPLACEMENT_COMPONENT_GROUPS.values():
        for feature in features:
            if feature not in ordered:
                ordered.append(feature)
    return ordered
