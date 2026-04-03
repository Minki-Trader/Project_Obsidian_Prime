# Selection Status

- stage: `06_segmented_risk_validation`
- current phase active: `06H`
- current mode: `sequential multi-window pre-risk overlay batch`
- overlay config: `risk_pct=2.00, broker_native SL, direction_split(long=1.40, short=2.00), ATR14`
- batch progress: `completed=756/786`, `failed=30`, `pending=0`
- status file: `06H_multi_window_pre_risk_batch_status.json`
- current best completed holdout row: `2404` `05I` -> `06H_2404_05I_01`, `return_pct=1073858.524`, `PF=9.3459`
- next action: `let 06H finish, then compare window-by-window leaders and robustness across the six anchors`
