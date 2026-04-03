# 06G Early WFO Core Compare Review

- window: `train=2022-09-01T00:00:00Z .. 2024-07-01T00:00:00Z`, `validation=2024-07-01T00:00:00Z .. 2025-04-01T00:00:00Z`, `test=2025-04-01T00:00:00Z .. 2025-09-01T00:00:00Z`
- leader_by_holdout_return: `06G_WFO_D` `soft_decay_reference`

## Runs

### 06G_WFO_C `plain_direction_split`

- description: `06C baseline without session decay.`
- overlay: `{"risk_pct": 2.5, "stop_atr_period": 14, "stop_execution_mode": "broker_native", "stop_long_atr_mult": 1.4, "stop_policy": "direction_split", "stop_short_atr_mult": 2.0}`
- offline validation: `macro_f1=0.4032`, `balanced_accuracy=0.4261`, `log_loss=1.1314`
- offline test: `macro_f1=0.4486`, `balanced_accuracy=0.4666`, `log_loss=1.0617`
- MT5 validation: `return_pct=12.840`, `PF=1.0128`, `trades=1169`, `max_dd_pct=48.4159`
- MT5 test: `return_pct=-13.448`, `PF=0.9644`, `trades=537`, `max_dd_pct=38.5927`

### 06G_WFO_D `soft_decay_reference`

- description: `06D soft session decay reference.`
- overlay: `{"monday_risk_pct_mult": 0.75, "ny_postcash_risk_pct_mult": 0.7, "risk_pct": 2.5, "stop_atr_period": 14, "stop_execution_mode": "broker_native", "stop_long_atr_mult": 1.4, "stop_policy": "direction_split", "stop_short_atr_mult": 2.0}`
- offline validation: `macro_f1=0.4032`, `balanced_accuracy=0.4261`, `log_loss=1.1314`
- offline test: `macro_f1=0.4486`, `balanced_accuracy=0.4666`, `log_loss=1.0617`
- MT5 validation: `return_pct=21.318`, `PF=1.0238`, `trades=1169`, `max_dd_pct=40.0773`
- MT5 test: `return_pct=-11.522`, `PF=0.9630`, `trades=537`, `max_dd_pct=32.6318`
