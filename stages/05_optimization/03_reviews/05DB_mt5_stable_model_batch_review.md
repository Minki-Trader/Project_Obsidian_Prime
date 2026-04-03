# 05DB Stage 05 Stable Model Batch Review

Generated at: `2026-03-30T12:55:35.657767+00:00`

## Scope

- purpose: `test stability-oriented linear training methods instead of validation-spiky tree swaps`
- feature base: `05W no_trend_strength 54-feature contract`
- reference runs: `05W`, `05BB`, `05BF`, `05AH`

## MT5 Validation Ranking

- [1] `05W_no_trend_strength_0001`: variant=`incumbent_05w`, family=`-`, return_pct=91.168, profit_factor=1.4092, max_dd_pct=11.1472, ulcer_index=6.5205, trades=493, ready_gap=0, unexpected_skips=0
- [2] `05BF_trend_proxy_persistence_volatility_0001`: variant=`persistence_volatility_reference`, family=`-`, return_pct=89.422, profit_factor=1.4012, max_dd_pct=11.9463, ulcer_index=7.1506, trades=487, ready_gap=0, unexpected_skips=0
- [3] `05BB_trend_proxy_persistence_only_0001`: variant=`persistence_only_reference`, family=`-`, return_pct=75.676, profit_factor=1.3308, max_dd_pct=12.3455, ulcer_index=7.2609, trades=490, ready_gap=0, unexpected_skips=0
- [4] `05AH_trend_proxy_sector_replacement_0001`: variant=`full_proxy_reference`, family=`-`, return_pct=62.200, profit_factor=1.2632, max_dd_pct=13.4545, ulcer_index=7.9225, trades=489, ready_gap=0, unexpected_skips=0
- [5] `05DA_mt5_validation_margin_regularized_vote_0001`: variant=`regularized_logreg_voter`, family=`regularized_logreg_voter`, return_pct=53.238, profit_factor=1.2220, max_dd_pct=14.1490, ulcer_index=8.2869, trades=489, ready_gap=0, unexpected_skips=0
- [6] `05CY_mt5_validation_margin_elasticnet_logreg_0001`: variant=`elasticnet_logreg`, family=`elasticnet_logreg`, return_pct=42.510, profit_factor=1.1782, max_dd_pct=14.8260, ulcer_index=8.7678, trades=477, ready_gap=0, unexpected_skips=0
- [7] `05CZ_mt5_validation_margin_pca_logreg_0001`: variant=`pca_logreg`, family=`pca_logreg`, return_pct=37.500, profit_factor=1.4010, max_dd_pct=21.3049, ulcer_index=2.8959, trades=168, ready_gap=0, unexpected_skips=0

## MT5 Holdout Ranking

- [1] `05DA_mt5_validation_margin_regularized_vote_0001`: variant=`regularized_logreg_voter`, family=`regularized_logreg_voter`, return_pct=46.218, profit_factor=1.3289, max_dd_pct=17.7040, ulcer_index=6.7318, trades=329, ready_gap=35, unexpected_skips=0
- [2] `05BB_trend_proxy_persistence_only_0001`: variant=`persistence_only_reference`, family=`-`, return_pct=44.792, profit_factor=1.3193, max_dd_pct=15.5405, ulcer_index=6.3183, trades=328, ready_gap=35, unexpected_skips=0
- [3] `05AH_trend_proxy_sector_replacement_0001`: variant=`full_proxy_reference`, family=`-`, return_pct=44.558, profit_factor=1.3109, max_dd_pct=17.7040, ulcer_index=7.1521, trades=331, ready_gap=35, unexpected_skips=0
- [4] `05BF_trend_proxy_persistence_volatility_0001`: variant=`persistence_volatility_reference`, family=`-`, return_pct=40.462, profit_factor=1.2801, max_dd_pct=17.0166, ulcer_index=6.9935, trades=331, ready_gap=35, unexpected_skips=0
- [5] `05W_no_trend_strength_0001`: variant=`incumbent_05w`, family=`-`, return_pct=33.538, profit_factor=1.2253, max_dd_pct=17.0166, ulcer_index=7.8344, trades=336, ready_gap=35, unexpected_skips=0
- [6] `05CY_mt5_validation_margin_elasticnet_logreg_0001`: variant=`elasticnet_logreg`, family=`elasticnet_logreg`, return_pct=29.234, profit_factor=1.2002, max_dd_pct=19.5236, ulcer_index=7.2056, trades=325, ready_gap=35, unexpected_skips=0

## Verdict

- status: `mixed_holdout_win_keep_incumbent`
- selected_run_name: `05W_no_trend_strength_0001`
- reason: `stable linear model improved holdout but did not lead validation, so the incumbent stays promoted for now`

## Read

- read: `this batch asks whether training-method stability, not raw model complexity, can recover holdout without relying on validation spikes`
