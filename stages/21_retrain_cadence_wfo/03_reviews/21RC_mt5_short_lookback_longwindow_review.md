# Stage 21 Direct MT5 Short-Lookback Long-Window Review

Generated at: `2026-04-07T12:18:18+00:00`

- mode: `direct_mt5_short_lookback_monthly_carry`
- comparison window: `2025-01-01 <= t < 2026-03-01`
- assumption: `1D/5D/1W use trailing trading-day lookbacks at each monthly refit point`

## Same-Period 18E Baseline

- run: `21e18_2501_long14m`
- source shell: `18E_2501_17e_ph20_0001`
- return_pct: `30.974`
- net_profit: `154.87`
- PF: `1.2131`
- trades: `283`
- max_dd_pct: `14.801`

## Direct MT5 Short-Lookback Results

- `21L` `5D` (5 trading days): return_pct `-57.700`, net_profit `-288.50`, PF `0.9397`, trades `2868`, max_dd_pct `67.311`, positive_months `3/14`
- `21M` `1W` (7 trading days): return_pct `-77.316`, net_profit `-386.58`, PF `0.9066`, trades `2676`, max_dd_pct `81.567`, positive_months `6/14`
- `21K` `1D` (1 trading day): return_pct `-85.986`, net_profit `-429.93`, PF `0.8882`, trades `3220`, max_dd_pct `89.308`, positive_months `2/14`

## Readout

- direct-MT5 short-lookback leader: `21L / 5D`
- short-window note: `5D had been the least-bad direct MT5 retrain on the 2025-04..2025-08 check, but it does not survive the full 2501 long window`
- decision: `the fixed 18E baseline remains clearly stronger than every short-lookback monthly retrain once the out-of-sample window is extended`
