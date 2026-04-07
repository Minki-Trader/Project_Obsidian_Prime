# Stage 21 18E Same-Period Baseline Review

Generated at: `2026-04-07T10:40:24.177154+00:00`

- baseline: `18E` `17E + PH20`
- run: `21e18`
- attempt: `att_0003`
- window: `2025-04-01` to `2025-09-01`
- return_pct: `27.700`
- net_profit: `138.50`
- PF: `1.4127`
- trades: `109`
- max_dd_pct: `14.595`
- final_balance: `638.50`

## Direct Compare

- `18E same-period baseline`: return `27.700`, PF `1.4127`, trades `109`, max_dd `14.595`
- `21m1a monthly 1M retrain ATR carry`: return `-38.466`, PF `0.8650`, trades `676`, max_dd `45.494`

## Notes

- This rerun confirms the original 18E fixed model for the 2407 window remains much stronger than the Stage 21 monthly 1M retrain variant over the exact same five-month market period.
- close reasons: `TIME_EXIT=63`, `TIME_EXIT_NY_POSTCASH=26`, `BROKER_SL=20`
- execution avg_spread: `135.482`, external_mismatch_count: `9902`
