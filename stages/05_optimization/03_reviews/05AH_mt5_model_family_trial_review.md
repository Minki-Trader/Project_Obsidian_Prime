# 05AH Stage 05 Model Family Trial Review

Generated at: `2026-03-29T17:32:24.347206+00:00`

## Scope

- purpose: `train a fresh trend_proxy_sector_logreg model on the frozen h/band dataset and run the current reference logic on MT5`
- logic reference: `05W_no_trend_strength_0001` with `min_margin=0.0700`
- dropped sectors: `trend_strength`
- replacement sector: `trend_proxy_regime`
- trend_proxy_persistence: `ema20_ema50_diff, ema50_ema200_diff, trix_15`
- trend_proxy_volatility_regime: `atr_14_over_atr_50, historical_vol_5_over_20, bb_squeeze`
- trend_proxy_breakout_pressure: `log_return_1, return_1_over_atr_14, hl_range`
- trend_proxy_breadth_confirmation: `top3_weighted_return_1, mega8_pos_breadth_1, mega8_dispersion_5`

## Offline Test Confirmation

- incumbent Stage 01 test: macro_f1=`0.4581`, balanced_accuracy=`0.4694`, accuracy=`0.5769`, log_loss=`0.9728`
- trial model test: macro_f1=`0.4577`, balanced_accuracy=`0.4686`, accuracy=`0.5766`, log_loss=`0.9735`

## MT5 Validation Ranking

- [1] `05W_no_trend_strength_0001`: return_pct=91.168, profit_factor=1.4092, max_dd_pct=11.1472, ulcer_index=6.5205, trades=493, ready_gap=0, unexpected_skips=0
- [2] `05AH_trend_proxy_sector_replacement_0001`: return_pct=62.200, profit_factor=1.2632, max_dd_pct=13.4545, ulcer_index=7.9225, trades=489, ready_gap=0, unexpected_skips=0

## MT5 Holdout Ranking

- [1] `05AH_trend_proxy_sector_replacement_0001`: return_pct=44.558, profit_factor=1.3109, max_dd_pct=17.7040, ulcer_index=7.1521, trades=331, ready_gap=35, unexpected_skips=0
- [2] `05W_no_trend_strength_0001`: return_pct=33.538, profit_factor=1.2253, max_dd_pct=17.0166, ulcer_index=7.8344, trades=336, ready_gap=35, unexpected_skips=0

## Verdict

- status: `mixed_holdout_win_keep_incumbent`
- selected_run_name: `05W_no_trend_strength_0001`
- reason: `trial model improved holdout return/PF but trailed the incumbent on validation, so the incumbent stays promoted for now`

## Read

- validation leader: `05W_no_trend_strength_0001`
- holdout winner: `05AH_trend_proxy_sector_replacement_0001`
- read: `treat model-family swaps with the same holdout gate as logic sweeps; validation spikes alone are not enough`
