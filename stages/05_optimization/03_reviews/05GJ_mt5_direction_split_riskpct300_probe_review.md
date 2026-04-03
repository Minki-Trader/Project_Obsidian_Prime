# 05GJ_05dp_dirsplit_l12_s18_riskpct300_0001 Stage 05 05DP Risk Percent Probe Review

Generated at: `2026-03-31T15:52:37.684331+00:00`

## Scope

- purpose: `verify that the EA/runtime path can execute balance-based risk-percent sizing with an ATR hard stop on top of the existing 05DP logic`
- run: `05GJ_05dp_dirsplit_l12_s18_riskpct300_0001`
- sizing_mode: `risk_pct`
- risk_pct: `3.0000`
- capital_base: `balance`
- stop_model: `atr`
- stop_execution_mode: `broker_native`
- stop_policy: `direction_split`
- stop_atr_period: `14`
- stop_atr_mult: `1.5000`

## Validation Read

- return_pct: `413.408`
- profit_factor: `1.2376`
- trade_count: `431`
- max_dd_pct: `42.8275`
- ulcer_index: `25.7335`
- ready_row_gap: `0`

## Ledger Verification

- trade_rows: `431`
- unique_volume_count: `169`
- volume_range: `0.0800 -> 3.9600`
- close_reason_breakdown: `{'BROKER_SL': 123, 'TIME_EXIT': 308}`
- stop_price_count: `431`
- realized_r_mean: `0.1466`
- unique_volumes_preview: `[0.08, 0.1, 0.11, 0.12, 0.13, 0.14, 0.15, 0.16, 0.17, 0.18, 0.19, 0.2]`

## Verdict

- status: `implementation_verified`
- reason: `risk_pct sizing path compiled, executed on MT5 validation, and produced trade ledger evidence for ATR-based stop-aware sizing`
