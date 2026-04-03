# 05GA Stage 05 05DP Risk Percent Probe Review

Generated at: `2026-03-31T15:06:09.861225+00:00`

## Scope

- purpose: `verify that the EA/runtime path can execute balance-based risk-percent sizing with an ATR hard stop on top of the existing 05DP logic`
- run: `05GA_05dp_riskpct050_atr14x15_0001`
- sizing_mode: `risk_pct`
- risk_pct: `0.5000`
- capital_base: `balance`
- stop_model: `atr`
- stop_atr_period: `14`
- stop_atr_mult: `1.5000`

## Validation Read

- return_pct: `25.078`
- profit_factor: `1.3112`
- trade_count: `426`
- max_dd_pct: `6.5594`
- ulcer_index: `3.5423`
- ready_row_gap: `0`

## Ledger Verification

- trade_rows: `426`
- unique_volume_count: `15`
- volume_range: `0.0100 -> 0.1500`
- close_reason_breakdown: `{'HARD_STOP': 126, 'TIME_EXIT': 300}`
- stop_price_count: `426`
- realized_r_mean: `0.1256`
- unique_volumes_preview: `[0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.11, 0.12]`

## Verdict

- status: `implementation_verified`
- reason: `risk_pct sizing path compiled, executed on MT5 validation, and produced trade ledger evidence for ATR-based stop-aware sizing`
