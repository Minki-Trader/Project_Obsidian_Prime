# 05GB_05dp_riskpct300_atr14x15_brokersl_0001 Stage 05 05DP Risk Percent Probe Review

Generated at: `2026-03-31T15:20:31.969400+00:00`

## Scope

- purpose: `verify that the EA/runtime path can execute balance-based risk-percent sizing with an ATR hard stop on top of the existing 05DP logic`
- run: `05GB_05dp_riskpct300_atr14x15_brokersl_0001`
- sizing_mode: `risk_pct`
- risk_pct: `3.0000`
- capital_base: `balance`
- stop_model: `atr`
- stop_execution_mode: `broker_native`
- stop_atr_period: `14`
- stop_atr_mult: `1.5000`

## Validation Read

- return_pct: `264.392`
- profit_factor: `1.1903`
- trade_count: `432`
- max_dd_pct: `39.0337`
- ulcer_index: `21.9114`
- ready_row_gap: `0`

## Ledger Verification

- trade_rows: `432`
- unique_volume_count: `150`
- volume_range: `0.0900 -> 3.3600`
- close_reason_breakdown: `{'BROKER_SL': 127, 'TIME_EXIT': 305}`
- stop_price_count: `432`
- realized_r_mean: `0.1187`
- unique_volumes_preview: `[0.09, 0.1, 0.12, 0.13, 0.14, 0.15, 0.16, 0.17, 0.18, 0.19, 0.2, 0.21]`

## Verdict

- status: `implementation_verified`
- reason: `risk_pct sizing path compiled, executed on MT5 validation, and produced trade ledger evidence for ATR-based stop-aware sizing`
