# 05DA Stage 05 Model Family Trial Review

Generated at: `2026-03-30T12:52:42.567171+00:00`

## Scope

- purpose: `train a fresh regularized_logreg_voter model on the frozen h/band dataset and run the current reference logic on MT5`
- logic reference: `05W_no_trend_strength_0001` with `min_margin=0.0700`
- dropped sectors: `trend_strength`

## Offline Test Confirmation

- incumbent Stage 01 test: macro_f1=`0.4581`, balanced_accuracy=`0.4694`, accuracy=`0.5769`, log_loss=`0.9728`
- trial model test: macro_f1=`0.4569`, balanced_accuracy=`0.4676`, accuracy=`0.5754`, log_loss=`0.9737`

## MT5 Validation Ranking

- [1] `05W_no_trend_strength_0001`: return_pct=91.168, profit_factor=1.4092, max_dd_pct=11.1472, ulcer_index=6.5205, trades=493, ready_gap=0, unexpected_skips=0
- [2] `05DA_mt5_validation_margin_regularized_vote_0001`: return_pct=53.238, profit_factor=1.2220, max_dd_pct=14.1490, ulcer_index=8.2869, trades=489, ready_gap=0, unexpected_skips=0

## MT5 Holdout Ranking

- [1] `05DA_mt5_validation_margin_regularized_vote_0001`: return_pct=46.218, profit_factor=1.3289, max_dd_pct=17.7040, ulcer_index=6.7318, trades=329, ready_gap=35, unexpected_skips=0
- [2] `05W_no_trend_strength_0001`: return_pct=33.538, profit_factor=1.2253, max_dd_pct=17.0166, ulcer_index=7.8344, trades=336, ready_gap=35, unexpected_skips=0

## Verdict

- status: `mixed_holdout_win_keep_incumbent`
- selected_run_name: `05W_no_trend_strength_0001`
- reason: `trial model improved holdout return/PF but trailed the incumbent on validation, so the incumbent stays promoted for now`

## Read

- validation leader: `05W_no_trend_strength_0001`
- holdout winner: `05DA_mt5_validation_margin_regularized_vote_0001`
- read: `treat model-family swaps with the same holdout gate as logic sweeps; validation spikes alone are not enough`
