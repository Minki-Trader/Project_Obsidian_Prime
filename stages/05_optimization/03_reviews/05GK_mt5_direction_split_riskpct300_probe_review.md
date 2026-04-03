# 05GK_05dp_dirsplit_l14_s20_riskpct300_0001 Stage 05 05DP Risk Percent Probe Review

Generated at: `2026-03-31T15:54:21.211481+00:00`

## Scope

- purpose: `verify that the EA/runtime path can execute balance-based risk-percent sizing with an ATR hard stop on top of the existing 05DP logic`
- run: `05GK_05dp_dirsplit_l14_s20_riskpct300_0001`
- sizing_mode: `risk_pct`
- risk_pct: `3.0000`
- capital_base: `balance`
- stop_model: `atr`
- stop_execution_mode: `broker_native`
- stop_policy: `direction_split`
- stop_atr_period: `14`
- stop_atr_mult: `1.5000`

## Validation Read

- return_pct: `521.996`
- profit_factor: `1.3291`
- trade_count: `425`
- max_dd_pct: `34.5037`
- ulcer_index: `15.2271`
- ready_row_gap: `0`

## Ledger Verification

- trade_rows: `425`
- unique_volume_count: `169`
- volume_range: `0.0800 -> 3.9800`
- close_reason_breakdown: `{'BROKER_SL': 92, 'TIME_EXIT': 333}`
- stop_price_count: `425`
- realized_r_mean: `0.1612`
- unique_volumes_preview: `[0.08, 0.09, 0.1, 0.11, 0.12, 0.13, 0.14, 0.15, 0.16, 0.17, 0.18, 0.19]`

## Verdict

- status: `implementation_verified`
- reason: `risk_pct sizing path compiled, executed on MT5 validation, and produced trade ledger evidence for ATR-based stop-aware sizing`
