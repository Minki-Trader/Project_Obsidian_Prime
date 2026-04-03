# 06F Early WFO LP Compare Review

- window: `train=2022-09-01T00:00:00Z .. 2024-07-01T00:00:00Z`, `validation=2024-07-01T00:00:00Z .. 2025-04-01T00:00:00Z`, `test=2025-04-01T00:00:00Z .. 2025-09-01T00:00:00Z`
- leader_by_holdout_return: `06F_WFO_LP02` `local_probe_b`

## Runs

### 06F_WFO_LP01 `local_probe_a`

- description: `Softer Monday, tighter post-cash decay.`
- overlay: `{"monday_risk_pct_mult": 0.8, "ny_postcash_risk_pct_mult": 0.65, "risk_pct": 2.5, "stop_atr_period": 14, "stop_execution_mode": "broker_native", "stop_long_atr_mult": 1.4, "stop_policy": "direction_split", "stop_short_atr_mult": 2.0}`
- offline validation: `macro_f1=0.4032`, `balanced_accuracy=0.4261`, `log_loss=1.1314`
- offline test: `macro_f1=0.4486`, `balanced_accuracy=0.4666`, `log_loss=1.0617`
- MT5 validation: `return_pct=21.792`, `PF=1.0247`, `trades=1169`, `max_dd_pct=39.5464`
- MT5 test: `return_pct=-11.282`, `PF=0.9633`, `trades=537`, `max_dd_pct=32.9737`

### 06F_WFO_LP02 `local_probe_b`

- description: `Stronger Monday and post-cash decay.`
- overlay: `{"monday_risk_pct_mult": 0.7, "ny_postcash_risk_pct_mult": 0.65, "risk_pct": 2.5, "stop_atr_period": 14, "stop_execution_mode": "broker_native", "stop_long_atr_mult": 1.4, "stop_policy": "direction_split", "stop_short_atr_mult": 2.0}`
- offline validation: `macro_f1=0.4032`, `balanced_accuracy=0.4261`, `log_loss=1.1314`
- offline test: `macro_f1=0.4486`, `balanced_accuracy=0.4666`, `log_loss=1.0617`
- MT5 validation: `return_pct=22.850`, `PF=1.0263`, `trades=1169`, `max_dd_pct=39.2509`
- MT5 test: `return_pct=-10.504`, `PF=0.9650`, `trades=537`, `max_dd_pct=30.8782`
