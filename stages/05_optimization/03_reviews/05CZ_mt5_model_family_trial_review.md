# 05CZ Stage 05 Model Family Trial Review

Generated at: `2026-03-30T12:46:40.895261+00:00`

## Scope

- purpose: `train a fresh pca_logreg model on the frozen h/band dataset and run the current reference logic on MT5`
- logic reference: `05W_no_trend_strength_0001` with `min_margin=0.0700`
- dropped sectors: `trend_strength`

## Offline Test Confirmation

- incumbent Stage 01 test: macro_f1=`0.4581`, balanced_accuracy=`0.4694`, accuracy=`0.5769`, log_loss=`0.9728`
- trial model test: macro_f1=`0.4555`, balanced_accuracy=`0.4737`, accuracy=`0.5506`, log_loss=`1.0153`

## MT5 Validation Ranking

- [1] `05W_no_trend_strength_0001`: return_pct=91.168, profit_factor=1.4092, max_dd_pct=11.1472, ulcer_index=6.5205, trades=493, ready_gap=0, unexpected_skips=0
- [2] `05CZ_mt5_validation_margin_pca_logreg_0001`: return_pct=37.500, profit_factor=1.4010, max_dd_pct=21.3049, ulcer_index=2.8959, trades=168, ready_gap=0, unexpected_skips=0

## Verdict

- status: `validation_only_pending_holdout`
- selected_run_name: `05W_no_trend_strength_0001`
- reason: `holdout not run yet, so the incumbent remains the selected bundle`

## Read

- validation leader: `05W_no_trend_strength_0001`
- read: `treat model-family swaps with the same holdout gate as logic sweeps; validation spikes alone are not enough`
