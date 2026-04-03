# 05GC_05dp_fixed_stop10_riskpct300_brokersl_0001 Stage 05 05DP Risk Percent Probe Review

Generated at: `2026-03-31T15:40:31.094145+00:00`

## Scope

- purpose: `verify that the EA/runtime path can execute balance-based risk-percent sizing with an ATR hard stop on top of the existing 05DP logic`
- run: `05GC_05dp_fixed_stop10_riskpct300_brokersl_0001`
- sizing_mode: `risk_pct`
- risk_pct: `3.0000`
- capital_base: `balance`
- stop_model: `atr`
- stop_execution_mode: `broker_native`
- stop_policy: `fixed`
- stop_atr_period: `14`
- stop_atr_mult: `1.0000`

## Validation Read

- return_pct: `401.004`
- profit_factor: `1.1529`
- trade_count: `455`
- max_dd_pct: `53.3932`
- ulcer_index: `31.9590`
- ready_row_gap: `0`

## Ledger Verification

- trade_rows: `455`
- unique_volume_count: `206`
- volume_range: `0.1600 -> 7.5200`
- close_reason_breakdown: `{'BROKER_SL': 215, 'TIME_EXIT': 240}`
- stop_price_count: `455`
- realized_r_mean: `0.1518`
- unique_volumes_preview: `[0.16, 0.17, 0.18, 0.19, 0.2, 0.21, 0.22, 0.23, 0.24, 0.25, 0.26, 0.27]`

## Verdict

- status: `implementation_verified`
- reason: `risk_pct sizing path compiled, executed on MT5 validation, and produced trade ledger evidence for ATR-based stop-aware sizing`
