# 05BU Stage 05 Model Family Trial Review

Generated at: `2026-03-30T12:08:32.770082+00:00`

## Scope

- purpose: `train a fresh persistence_frontier_stacker model on the frozen h/band dataset and run the current reference logic on MT5`
- logic reference: `05W_no_trend_strength_0001` with `min_margin=0.0700`
- dropped sectors: `trend_strength`
- voter components: `base_05w, persistence_volatility`
- voter weights: ``

## Offline Test Confirmation

- incumbent Stage 01 test: macro_f1=`0.4581`, balanced_accuracy=`0.4694`, accuracy=`0.5769`, log_loss=`0.9728`
- trial model test: macro_f1=`0.4488`, balanced_accuracy=`0.4737`, accuracy=`0.5436`, log_loss=`1.0084`

## MT5 Validation Ranking

- [1] `05W_no_trend_strength_0001`: return_pct=91.168, profit_factor=1.4092, max_dd_pct=11.1472, ulcer_index=6.5205, trades=493, ready_gap=0, unexpected_skips=0
- [2] `05BU_frontier_stack_w_bf_0001`: return_pct=-20.890, profit_factor=0.8873, max_dd_pct=30.0738, ulcer_index=19.2198, trades=301, ready_gap=0, unexpected_skips=0

## Verdict

- status: `validation_only_pending_holdout`
- selected_run_name: `05W_no_trend_strength_0001`
- reason: `holdout not run yet, so the incumbent remains the selected bundle`

## Read

- validation leader: `05W_no_trend_strength_0001`
- read: `treat model-family swaps with the same holdout gate as logic sweeps; validation spikes alone are not enough`
