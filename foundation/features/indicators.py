from __future__ import annotations

import numpy as np
import pandas as pd


def safe_divide(numerator: pd.Series, denominator: pd.Series) -> pd.Series:
    result = numerator / denominator
    return result.mask(denominator.eq(0))


def rolling_zscore(series: pd.Series, window: int) -> pd.Series:
    mean = series.rolling(window, min_periods=window).mean()
    std = series.rolling(window, min_periods=window).std(ddof=0)
    result = (series - mean) / std
    zero_mask = std.eq(0) & std.notna()
    return result.mask(zero_mask, 0.0)


def ema(series: pd.Series, period: int) -> pd.Series:
    return series.ewm(span=period, adjust=False, min_periods=period).mean()


def sma(series: pd.Series, period: int) -> pd.Series:
    return series.rolling(period, min_periods=period).mean()


def rolling_std(series: pd.Series, period: int) -> pd.Series:
    return series.rolling(period, min_periods=period).std(ddof=0)


def wilder_smooth(series: pd.Series, period: int) -> pd.Series:
    values = series.astype(float).to_numpy()
    out = np.full(len(values), np.nan)

    first_end = None
    for end_idx in range(period - 1, len(values)):
        window = values[end_idx - period + 1 : end_idx + 1]
        if np.isfinite(window).all():
            first_end = end_idx
            out[end_idx] = window.mean()
            break

    if first_end is None:
        return pd.Series(out, index=series.index, dtype=float)

    for idx in range(first_end + 1, len(values)):
        value = values[idx]
        prev = out[idx - 1]
        if np.isnan(value) or np.isnan(prev):
            out[idx] = np.nan
        else:
            out[idx] = ((prev * (period - 1)) + value) / period

    return pd.Series(out, index=series.index, dtype=float)


def true_range(high: pd.Series, low: pd.Series, close: pd.Series) -> pd.Series:
    prev_close = close.shift(1)
    return pd.concat(
        [
            high - low,
            (high - prev_close).abs(),
            (low - prev_close).abs(),
        ],
        axis=1,
    ).max(axis=1)


def atr(high: pd.Series, low: pd.Series, close: pd.Series, period: int) -> pd.Series:
    tr = true_range(high, low, close)
    return wilder_smooth(tr, period)


def rsi(close: pd.Series, period: int) -> pd.Series:
    delta = close.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = wilder_smooth(gain, period)
    avg_loss = wilder_smooth(loss, period)

    rs = avg_gain / avg_loss
    result = 100 - (100 / (1 + rs))

    both_zero = avg_gain.eq(0) & avg_loss.eq(0)
    loss_zero = avg_loss.eq(0) & avg_gain.gt(0)

    result = result.mask(both_zero, 50.0)
    result = result.mask(loss_zero, 100.0)
    return result


def stochastic_kd_diff(high: pd.Series, low: pd.Series, close: pd.Series, period: int = 14, smooth_k: int = 3, smooth_d: int = 3) -> pd.Series:
    lowest_low = low.rolling(period, min_periods=period).min()
    highest_high = high.rolling(period, min_periods=period).max()
    raw_k = safe_divide((close - lowest_low) * 100, highest_high - lowest_low)
    k = raw_k.rolling(smooth_k, min_periods=smooth_k).mean()
    d = k.rolling(smooth_d, min_periods=smooth_d).mean()
    return k - d


def stochrsi_kd_diff(close: pd.Series) -> pd.Series:
    rsi_14 = rsi(close, 14)
    rsi_low = rsi_14.rolling(14, min_periods=14).min()
    rsi_high = rsi_14.rolling(14, min_periods=14).max()
    raw_k = safe_divide((rsi_14 - rsi_low) * 100, rsi_high - rsi_low)
    k = raw_k.rolling(3, min_periods=3).mean()
    d = k.rolling(3, min_periods=3).mean()
    return k - d


def ppo_histogram(close: pd.Series) -> pd.Series:
    ema12 = ema(close, 12)
    ema26 = ema(close, 26)
    ppo = safe_divide((ema12 - ema26) * 100, ema26)
    signal = ema(ppo, 9)
    return ppo - signal


def trix(close: pd.Series, period: int = 15) -> pd.Series:
    ema1 = ema(close, period)
    ema2 = ema(ema1, period)
    ema3 = ema(ema2, period)
    return safe_divide(ema3, ema3.shift(1)) - 1


def adx(high: pd.Series, low: pd.Series, close: pd.Series, period: int = 14) -> tuple[pd.Series, pd.Series, pd.Series]:
    up_move = high.diff()
    down_move = -low.diff()

    plus_dm = up_move.where((up_move > down_move) & (up_move > 0), 0.0)
    minus_dm = down_move.where((down_move > up_move) & (down_move > 0), 0.0)

    tr = true_range(high, low, close)
    tr_smooth = wilder_smooth(tr, period)
    plus_dm_smooth = wilder_smooth(plus_dm, period)
    minus_dm_smooth = wilder_smooth(minus_dm, period)

    plus_di = safe_divide(plus_dm_smooth * 100, tr_smooth)
    minus_di = safe_divide(minus_dm_smooth * 100, tr_smooth)
    dx = safe_divide((plus_di - minus_di).abs() * 100, plus_di + minus_di)
    adx_series = wilder_smooth(dx, period)
    return adx_series, plus_di, minus_di


def vortex_indicator(high: pd.Series, low: pd.Series, close: pd.Series, period: int = 14) -> pd.Series:
    tr = true_range(high, low, close).rolling(period, min_periods=period).sum()
    vm_plus = (high - low.shift(1)).abs().rolling(period, min_periods=period).sum()
    vm_minus = (low - high.shift(1)).abs().rolling(period, min_periods=period).sum()
    vi_plus = safe_divide(vm_plus, tr)
    vi_minus = safe_divide(vm_minus, tr)
    return vi_plus - vi_minus


def supertrend_state(high: pd.Series, low: pd.Series, close: pd.Series, period: int = 10, multiplier: float = 3.0) -> pd.Series:
    atr_series = atr(high, low, close, period)
    hl2 = (high + low) / 2
    basic_upper = hl2 + (multiplier * atr_series)
    basic_lower = hl2 - (multiplier * atr_series)

    upper = np.full(len(close), np.nan)
    lower = np.full(len(close), np.nan)
    state = np.full(len(close), np.nan)

    first_valid = None
    for idx in range(len(close)):
        if np.isfinite(basic_upper.iloc[idx]) and np.isfinite(basic_lower.iloc[idx]):
            first_valid = idx
            upper[idx] = basic_upper.iloc[idx]
            lower[idx] = basic_lower.iloc[idx]
            state[idx] = 1.0 if close.iloc[idx] >= hl2.iloc[idx] else -1.0
            break

    if first_valid is None:
        return pd.Series(state, index=close.index, dtype=float)

    for idx in range(first_valid + 1, len(close)):
        if not np.isfinite(basic_upper.iloc[idx]) or not np.isfinite(basic_lower.iloc[idx]):
            continue

        prev_upper = upper[idx - 1]
        prev_lower = lower[idx - 1]
        prev_close = close.iloc[idx - 1]

        curr_upper = basic_upper.iloc[idx]
        curr_lower = basic_lower.iloc[idx]

        upper[idx] = curr_upper if (np.isnan(prev_upper) or curr_upper < prev_upper or prev_close > prev_upper) else prev_upper
        lower[idx] = curr_lower if (np.isnan(prev_lower) or curr_lower > prev_lower or prev_close < prev_lower) else prev_lower

        prev_state = state[idx - 1]
        curr_close = close.iloc[idx]

        if prev_state == 1.0:
            state[idx] = -1.0 if curr_close < lower[idx] else 1.0
        else:
            state[idx] = 1.0 if curr_close > upper[idx] else -1.0

    return pd.Series(state, index=close.index, dtype=float)
