# 05GH_05dp_regime085_120_110_150_220_riskpct300_0001 Stage 05 05DP Risk Percent Probe Review

Generated at: `2026-03-31T15:49:10.082956+00:00`

## Scope

- purpose: `verify that the EA/runtime path can execute balance-based risk-percent sizing with an ATR hard stop on top of the existing 05DP logic`
- run: `05GH_05dp_regime085_120_110_150_220_riskpct300_0001`
- sizing_mode: `risk_pct`
- risk_pct: `3.0000`
- capital_base: `balance`
- stop_model: `atr`
- stop_execution_mode: `broker_native`
- stop_policy: `regime_bucket`
- stop_atr_period: `14`
- stop_atr_mult: `1.5000`

## Validation Read

- return_pct: `286.892`
- profit_factor: `1.2346`
- trade_count: `426`
- max_dd_pct: `40.6883`
- ulcer_index: `23.2829`
- ready_row_gap: `0`

## Ledger Verification

- trade_rows: `426`
- unique_volume_count: `136`
- volume_range: `0.0500 -> 2.6900`
- close_reason_breakdown: `{'BROKER_SL': 109, 'TIME_EXIT': 317}`
- stop_price_count: `426`
- realized_r_mean: `0.1222`
- unique_volumes_preview: `[0.05, 0.06, 0.08, 0.09, 0.1, 0.11, 0.12, 0.13, 0.14, 0.15, 0.16, 0.17]`

## Verdict

- status: `implementation_verified`
- reason: `risk_pct sizing path compiled, executed on MT5 validation, and produced trade ledger evidence for ATR-based stop-aware sizing`
