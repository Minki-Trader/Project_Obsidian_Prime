# Stage 21 Direct MT5 Short-Lookback Review

Generated at: `2026-04-07T11:41:39.240220+00:00`

- mode: `direct_mt5_short_lookback_monthly_carry`
- comparison window: `2025-04-01 <= t < 2025-09-01`
- assumption: `1D/5D/1W use trailing trading-day lookbacks at each monthly refit point`

## Same-Period 18E Baseline

- run: `21e18`
- return_pct: `27.700`
- net_profit: `138.50`
- PF: `1.4127`
- trades: `109`
- max_dd_pct: `14.877`

## Existing 1M ATR Carry Reference

- run: `21m1a`
- return_pct: `-38.466`
- net_profit: `-192.33`
- PF: `0.8650`
- trades: `676`
- max_dd_pct: `45.494`

## Direct MT5 Short-Lookback Results

- `21I` `5D` (5 trading days): return_pct `1.228`, net_profit `6.14`, PF `1.0026`, trades `1189`, max_dd_pct `42.015`, positive_months `3/5`
- `21J` `1W` (7 trading days): return_pct `-45.304`, net_profit `-226.52`, PF `0.9032`, trades `1045`, max_dd_pct `54.530`, positive_months `1/5`
- `21H` `1D` (1 trading days): return_pct `-51.286`, net_profit `-256.43`, PF `0.8652`, trades `1327`, max_dd_pct `62.400`, positive_months `1/5`

## Readout

- direct-MT5 short-lookback leader: `21I / 5D`
- note: `same-period 18E baseline still remains stronger than every direct MT5 short-lookback retrain tested so far`
- note: `short-lookback leader improves on the prior 1M ATR carry retrain reference`
