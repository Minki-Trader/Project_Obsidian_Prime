# 05AD Stage 05 Model Family Trial Review

Generated at: `2026-03-29T17:22:46.895069+00:00`

## Scope

- purpose: `train a fresh logistic_regression model on the frozen h/band dataset and run the current 03E logic on MT5`
- logic reference: `05W_no_trend_strength_0001` with `min_margin=0.0700`
- dropped features: `di_spread_14`

## Offline Test Confirmation

- incumbent Stage 01 test: macro_f1=`0.4581`, balanced_accuracy=`0.4694`, accuracy=`0.5769`, log_loss=`0.9728`
- trial model test: macro_f1=`0.4566`, balanced_accuracy=`0.4674`, accuracy=`0.5763`, log_loss=`0.9733`

## MT5 Validation Ranking

- [1] `05AD_drop_di_spread14_0001`: return_pct=76.554, profit_factor=1.3094, max_dd_pct=11.1513, ulcer_index=4.3348, trades=524, ready_gap=0, unexpected_skips=0
- [2] `05W_no_trend_strength_0001`: return_pct=91.168, profit_factor=1.4092, max_dd_pct=11.1472, ulcer_index=6.5205, trades=493, ready_gap=0, unexpected_skips=0

## MT5 Holdout Ranking

- [1] `05W_no_trend_strength_0001`: return_pct=33.538, profit_factor=1.2253, max_dd_pct=17.0166, ulcer_index=7.8344, trades=336, ready_gap=35, unexpected_skips=0
- [2] `05AD_drop_di_spread14_0001`: return_pct=23.920, profit_factor=1.1485, max_dd_pct=24.3031, ulcer_index=7.7829, trades=346, ready_gap=35, unexpected_skips=0

## Verdict

- status: `reject_keep_incumbent`
- selected_run_name: `05W_no_trend_strength_0001`
- reason: `holdout still favors the incumbent logic/model bundle`

## Read

- validation leader: `05AD_drop_di_spread14_0001`
- holdout winner: `05W_no_trend_strength_0001`
- read: `treat model-family swaps with the same holdout gate as logic sweeps; validation spikes alone are not enough`
