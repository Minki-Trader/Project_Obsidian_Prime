# 05X Stage 05 Model Family Trial Review

Generated at: `2026-03-29T16:52:40.511050+00:00`

## Scope

- purpose: `train a fresh logistic_regression model on the frozen h/band dataset and run the current 03E logic on MT5`
- logic reference: `03E_mt5_validation_baseline_0001` with `min_margin=0.0700`

## Offline Test Confirmation

- incumbent Stage 01 test: macro_f1=`0.4581`, balanced_accuracy=`0.4694`, accuracy=`0.5769`, log_loss=`0.9728`
- trial model test: macro_f1=`0.4585`, balanced_accuracy=`0.4688`, accuracy=`0.5827`, log_loss=`0.9669`

## MT5 Validation Ranking

- [1] `05X_no_session_ctx_0001`: return_pct=75.382, profit_factor=1.3201, max_dd_pct=11.6004, ulcer_index=2.3678, trades=499, ready_gap=0, unexpected_skips=0
- [2] `03E_mt5_validation_baseline_0001`: return_pct=67.664, profit_factor=1.2655, max_dd_pct=12.2017, ulcer_index=3.5570, trades=530, ready_gap=0, unexpected_skips=0

## Verdict

- status: `validation_only_pending_holdout`
- selected_run_name: `03E_mt5_validation_baseline_0001`
- reason: `holdout not run yet, so the incumbent remains the selected bundle`

## Read

- validation leader: `05X_no_session_ctx_0001`
- read: `treat model-family swaps with the same holdout gate as logic sweeps; validation spikes alone are not enough`
