# Stage 21 Direct MT5 Slow-Lookback Long-Window Review

Generated at: `2026-04-07T12:51:42+00:00`

- mode: `direct_mt5_slow_lookback_monthly_carry`
- comparison window: `2025-01-01 <= t < 2026-03-01`
- assumption: `2W/1M/2M are interpreted as trailing trading-day lookbacks using 10, 21, and 42 trading days`

## Same-Period 18E Baseline

- run: `21e18_2501_long14m`
- source shell: `18E_2501_17e_ph20_0001`
- return_pct: `30.974`
- net_profit: `154.87`
- PF: `1.2131`
- trades: `283`
- max_dd_pct: `14.801`

## Direct MT5 Slow-Lookback Results

- `21P` `2M` (42 trading days): return_pct `-5.512`, net_profit `-27.56`, PF `0.9906`, trades `1514`, max_dd_pct `54.867`, positive_months `6/14`
- `21N` `2W` (10 trading days): return_pct `-55.386`, net_profit `-276.93`, PF `0.9363`, trades `2526`, max_dd_pct `69.108`, positive_months `6/14`
- `21O` `1M` (21 trading days): return_pct `-59.496`, net_profit `-297.48`, PF `0.9211`, trades `1962`, max_dd_pct `70.811`, positive_months `5/14`

## Readout

- direct-MT5 slow-lookback leader: `21P / 2M`
- note: `slower retraining is meaningfully less bad than short 1D/5D/1W retraining, but it still fails to beat the fixed 18E baseline on the long 2501 window`
- decision: `keep the fixed 18E baseline as the operating choice`
