# 05GG_05dp_regime090_110_090_140_180_riskpct300_0001 Stage 05 05DP Risk Percent Probe Review

Generated at: `2026-03-31T15:47:25.404427+00:00`

## Scope

- purpose: `verify that the EA/runtime path can execute balance-based risk-percent sizing with an ATR hard stop on top of the existing 05DP logic`
- run: `05GG_05dp_regime090_110_090_140_180_riskpct300_0001`
- sizing_mode: `risk_pct`
- risk_pct: `3.0000`
- capital_base: `balance`
- stop_model: `atr`
- stop_execution_mode: `broker_native`
- stop_policy: `regime_bucket`
- stop_atr_period: `14`
- stop_atr_mult: `1.5000`

## Validation Read

- return_pct: `339.024`
- profit_factor: `1.2094`
- trade_count: `435`
- max_dd_pct: `38.3453`
- ulcer_index: `21.1869`
- ready_row_gap: `0`

## Ledger Verification

- trade_rows: `435`
- unique_volume_count: `166`
- volume_range: `0.0700 -> 3.5000`
- close_reason_breakdown: `{'BROKER_SL': 132, 'TIME_EXIT': 303}`
- stop_price_count: `435`
- realized_r_mean: `0.1332`
- unique_volumes_preview: `[0.07, 0.08, 0.09, 0.1, 0.11, 0.12, 0.13, 0.14, 0.15, 0.16, 0.17, 0.18]`

## Verdict

- status: `implementation_verified`
- reason: `risk_pct sizing path compiled, executed on MT5 validation, and produced trade ledger evidence for ATR-based stop-aware sizing`
