# 05K Stage 05 Model Family Trial Review

Generated at: `2026-03-29T15:42:46.091953+00:00`

## Scope

- purpose: `train a fresh xgboost model on the frozen h/band dataset and run the current 03E logic on MT5`
- logic reference: `03E_mt5_validation_baseline_0001` with `min_margin=0.0700`

## Offline Test Confirmation

- incumbent Stage 01 test: macro_f1=`0.4581`, balanced_accuracy=`0.4694`, accuracy=`0.5769`, log_loss=`0.9728`
- trial model test: macro_f1=`0.4441`, balanced_accuracy=`0.4570`, accuracy=`0.5552`, log_loss=`0.9158`

## MT5 Validation Ranking

- [1] `05K_mt5_validation_margin_xgboost_modelswap_0001`: return_pct=816.882, profit_factor=4.5617, max_dd_pct=8.1457, ulcer_index=0.3186, trades=1394, ready_gap=0, unexpected_skips=0
- [2] `03E_mt5_validation_baseline_0001`: return_pct=67.664, profit_factor=1.2655, max_dd_pct=12.2017, ulcer_index=3.5570, trades=530, ready_gap=0, unexpected_skips=0

## MT5 Holdout Ranking

- [1] `03E_mt5_validation_baseline_0001`: return_pct=7.072, profit_factor=1.0441, max_dd_pct=20.0228, ulcer_index=8.1911, trades=357, ready_gap=35, unexpected_skips=0
- [2] `05K_mt5_validation_margin_xgboost_modelswap_0001`: return_pct=-0.210, profit_factor=0.9994, max_dd_pct=28.3434, ulcer_index=14.4717, trades=780, ready_gap=35, unexpected_skips=0

## Verdict

- status: `reject_keep_incumbent`
- selected_run_name: `03E_mt5_validation_baseline_0001`
- reason: `holdout still favors the incumbent logic/model bundle`

## Read

- validation leader: `05K_mt5_validation_margin_xgboost_modelswap_0001`
- holdout winner: `03E_mt5_validation_baseline_0001`
- read: `treat model-family swaps with the same holdout gate as logic sweeps; validation spikes alone are not enough`
