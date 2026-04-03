# 05CY Stage 05 Model Family Trial Review

Generated at: `2026-03-30T12:55:35.142971+00:00`

## Scope

- purpose: `train a fresh elasticnet_logreg model on the frozen h/band dataset and run the current reference logic on MT5`
- logic reference: `05W_no_trend_strength_0001` with `min_margin=0.0700`
- dropped sectors: `trend_strength`

## Offline Test Confirmation

- incumbent Stage 01 test: macro_f1=`0.4581`, balanced_accuracy=`0.4694`, accuracy=`0.5769`, log_loss=`0.9728`
- trial model test: macro_f1=`0.4588`, balanced_accuracy=`0.4697`, accuracy=`0.5766`, log_loss=`0.9742`

## MT5 Validation Ranking

- [1] `05W_no_trend_strength_0001`: return_pct=91.168, profit_factor=1.4092, max_dd_pct=11.1472, ulcer_index=6.5205, trades=493, ready_gap=0, unexpected_skips=0
- [2] `05CY_mt5_validation_margin_elasticnet_logreg_0001`: return_pct=42.510, profit_factor=1.1782, max_dd_pct=14.8260, ulcer_index=8.7678, trades=477, ready_gap=0, unexpected_skips=0

## MT5 Holdout Ranking

- [1] `05W_no_trend_strength_0001`: return_pct=33.538, profit_factor=1.2253, max_dd_pct=17.0166, ulcer_index=7.8344, trades=336, ready_gap=35, unexpected_skips=0
- [2] `05CY_mt5_validation_margin_elasticnet_logreg_0001`: return_pct=29.234, profit_factor=1.2002, max_dd_pct=19.5236, ulcer_index=7.2056, trades=325, ready_gap=35, unexpected_skips=0

## Verdict

- status: `reject_keep_incumbent`
- selected_run_name: `05W_no_trend_strength_0001`
- reason: `trial model did not clear the incumbent on the holdout gate`

## Read

- validation leader: `05W_no_trend_strength_0001`
- holdout winner: `05W_no_trend_strength_0001`
- read: `treat model-family swaps with the same holdout gate as logic sweeps; validation spikes alone are not enough`
