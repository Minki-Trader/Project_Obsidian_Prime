# 05AF Stage 05 Model Family Trial Review

Generated at: `2026-03-29T17:20:29.892975+00:00`

## Scope

- purpose: `train a fresh logistic_regression model on the frozen h/band dataset and run the current 03E logic on MT5`
- logic reference: `05W_no_trend_strength_0001` with `min_margin=0.0700`
- dropped features: `vortex_indicator`

## Offline Test Confirmation

- incumbent Stage 01 test: macro_f1=`0.4581`, balanced_accuracy=`0.4694`, accuracy=`0.5769`, log_loss=`0.9728`
- trial model test: macro_f1=`0.4560`, balanced_accuracy=`0.4671`, accuracy=`0.5750`, log_loss=`0.9731`

## MT5 Validation Ranking

- [1] `05AF_drop_vortex_indicator_0001`: return_pct=73.574, profit_factor=1.2927, max_dd_pct=11.8586, ulcer_index=3.0411, trades=533, ready_gap=0, unexpected_skips=0
- [2] `05W_no_trend_strength_0001`: return_pct=91.168, profit_factor=1.4092, max_dd_pct=11.1472, ulcer_index=6.5205, trades=493, ready_gap=0, unexpected_skips=0

## Verdict

- status: `validation_only_pending_holdout`
- selected_run_name: `05W_no_trend_strength_0001`
- reason: `holdout not run yet, so the incumbent remains the selected bundle`

## Read

- validation leader: `05AF_drop_vortex_indicator_0001`
- read: `treat model-family swaps with the same holdout gate as logic sweeps; validation spikes alone are not enough`
