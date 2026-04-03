# 05BQ Stage 05 Model Family Trial Review

Generated at: `2026-03-30T11:55:08.474570+00:00`

## Scope

- purpose: `train a fresh persistence_frontier_voter model on the frozen h/band dataset and run the current reference logic on MT5`
- logic reference: `05W_no_trend_strength_0001` with `min_margin=0.0700`
- dropped sectors: `trend_strength`
- voter components: `base_05w, persistence_volatility`
- voter weights: `1.000, 1.000`

## Offline Test Confirmation

- incumbent Stage 01 test: macro_f1=`0.4581`, balanced_accuracy=`0.4694`, accuracy=`0.5769`, log_loss=`0.9728`
- trial model test: macro_f1=`0.4582`, balanced_accuracy=`0.4694`, accuracy=`0.5769`, log_loss=`0.9734`

## MT5 Validation Ranking

- [1] `05BQ_frontier_vote_w_bf_0001`: return_pct=92.292, profit_factor=1.4157, max_dd_pct=10.9660, ulcer_index=6.4919, trades=491, ready_gap=0, unexpected_skips=0
- [2] `05W_no_trend_strength_0001`: return_pct=91.168, profit_factor=1.4092, max_dd_pct=11.1472, ulcer_index=6.5205, trades=493, ready_gap=0, unexpected_skips=0

## MT5 Holdout Ranking

- [1] `05BQ_frontier_vote_w_bf_0001`: return_pct=34.760, profit_factor=1.2326, max_dd_pct=17.0166, ulcer_index=7.7800, trades=335, ready_gap=35, unexpected_skips=0
- [2] `05W_no_trend_strength_0001`: return_pct=33.538, profit_factor=1.2253, max_dd_pct=17.0166, ulcer_index=7.8344, trades=336, ready_gap=35, unexpected_skips=0

## Verdict

- status: `promote_candidate`
- selected_run_name: `05BQ_frontier_vote_w_bf_0001`
- reason: `trial model improved both validation and holdout versus the incumbent`

## Read

- validation leader: `05BQ_frontier_vote_w_bf_0001`
- holdout winner: `05BQ_frontier_vote_w_bf_0001`
- read: `treat model-family swaps with the same holdout gate as logic sweeps; validation spikes alone are not enough`
