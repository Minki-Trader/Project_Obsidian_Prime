# 05W Stage 05 Model Family Trial Review

Generated at: `2026-03-29T16:59:10.090734+00:00`

## Scope

- purpose: `train a fresh logistic_regression model on the frozen h/band dataset and run the current 03E logic on MT5`
- logic reference: `03E_mt5_validation_baseline_0001` with `min_margin=0.0700`

## Offline Test Confirmation

- incumbent Stage 01 test: macro_f1=`0.4581`, balanced_accuracy=`0.4694`, accuracy=`0.5769`, log_loss=`0.9728`
- trial model test: macro_f1=`0.4587`, balanced_accuracy=`0.4696`, accuracy=`0.5772`, log_loss=`0.9733`

## MT5 Validation Ranking

- [1] `05W_no_trend_strength_0001`: return_pct=91.168, profit_factor=1.4092, max_dd_pct=11.1472, ulcer_index=6.5205, trades=493, ready_gap=0, unexpected_skips=0
- [2] `03E_mt5_validation_baseline_0001`: return_pct=67.664, profit_factor=1.2655, max_dd_pct=12.2017, ulcer_index=3.5570, trades=530, ready_gap=0, unexpected_skips=0

## MT5 Holdout Ranking

- [1] `05W_no_trend_strength_0001`: return_pct=33.538, profit_factor=1.2253, max_dd_pct=17.0166, ulcer_index=7.8344, trades=336, ready_gap=35, unexpected_skips=0
- [2] `03E_mt5_validation_baseline_0001`: return_pct=7.072, profit_factor=1.0441, max_dd_pct=20.0228, ulcer_index=8.1911, trades=357, ready_gap=35, unexpected_skips=0

## Verdict

- status: `promote_candidate`
- selected_run_name: `05W_no_trend_strength_0001`
- reason: `trial model cleared the holdout gate versus the incumbent`

## Read

- validation leader: `05W_no_trend_strength_0001`
- holdout winner: `05W_no_trend_strength_0001`
- read: `treat model-family swaps with the same holdout gate as logic sweeps; validation spikes alone are not enough`
