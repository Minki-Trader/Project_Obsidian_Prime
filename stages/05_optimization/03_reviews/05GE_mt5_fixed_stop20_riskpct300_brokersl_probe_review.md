# 05GE_05dp_fixed_stop20_riskpct300_brokersl_0001 Stage 05 05DP Risk Percent Probe Review

Generated at: `2026-03-31T15:44:00.549036+00:00`

## Scope

- purpose: `verify that the EA/runtime path can execute balance-based risk-percent sizing with an ATR hard stop on top of the existing 05DP logic`
- run: `05GE_05dp_fixed_stop20_riskpct300_brokersl_0001`
- sizing_mode: `risk_pct`
- risk_pct: `3.0000`
- capital_base: `balance`
- stop_model: `atr`
- stop_execution_mode: `broker_native`
- stop_policy: `fixed`
- stop_atr_period: `14`
- stop_atr_mult: `2.0000`

## Validation Read

- return_pct: `388.414`
- profit_factor: `1.3120`
- trade_count: `417`
- max_dd_pct: `36.9980`
- ulcer_index: `19.3046`
- ready_row_gap: `0`

## Ledger Verification

- trade_rows: `417`
- unique_volume_count: `134`
- volume_range: `0.0600 -> 2.8500`
- close_reason_breakdown: `{'BROKER_SL': 71, 'TIME_EXIT': 346}`
- stop_price_count: `417`
- realized_r_mean: `0.1417`
- unique_volumes_preview: `[0.06, 0.07, 0.09, 0.1, 0.11, 0.12, 0.13, 0.14, 0.15, 0.16, 0.17, 0.18]`

## Verdict

- status: `implementation_verified`
- reason: `risk_pct sizing path compiled, executed on MT5 validation, and produced trade ledger evidence for ATR-based stop-aware sizing`
