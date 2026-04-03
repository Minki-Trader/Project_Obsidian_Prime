# 05CC Stage 05 Model Family Trial Review

Generated at: `2026-03-30T13:09:47.784151+00:00`

## Scope

- purpose: `train a fresh trend_proxy_sector_logreg model on the frozen h/band dataset and run the current reference logic on MT5`
- logic reference: `05W_no_trend_strength_0001` with `min_margin=0.0700`
- dropped sectors: `trend_strength`
- replacement sector: `trend_proxy_regime`
- trend_proxy_persistence: `ema20_ema50_diff, ema50_ema200_diff, trix_15`
- trend_proxy_downside_pressure: `close_ema20_ratio, close_ema50_ratio, overnight_return, return_1_over_atr_14, us100_minus_mega8_equal_return_1, us100_minus_top3_weighted_return_1`
- trend_proxy_risk_off_confirmation: `vix_change_1, vix_zscore_20, us10yr_change_1, us10yr_zscore_20, usdx_change_1, usdx_zscore_20`

## Offline Test Confirmation

- incumbent Stage 01 test: macro_f1=`0.4581`, balanced_accuracy=`0.4694`, accuracy=`0.5769`, log_loss=`0.9728`
- trial model test: macro_f1=`0.4565`, balanced_accuracy=`0.4676`, accuracy=`0.5754`, log_loss=`0.9736`

## MT5 Validation Ranking

- [1] `05W_no_trend_strength_0001`: return_pct=91.168, profit_factor=1.4092, max_dd_pct=11.1472, ulcer_index=6.5205, trades=493, ready_gap=0, unexpected_skips=0
- [2] `05CC_trend_proxy_persistence_downside_riskoff_0001`: return_pct=78.506, profit_factor=1.3414, max_dd_pct=12.0064, ulcer_index=7.2488, trades=495, ready_gap=0, unexpected_skips=0

## MT5 Holdout Ranking

- [1] `05CC_trend_proxy_persistence_downside_riskoff_0001`: return_pct=47.402, profit_factor=1.3367, max_dd_pct=15.5405, ulcer_index=6.0251, trades=333, ready_gap=35, unexpected_skips=0
- [2] `05W_no_trend_strength_0001`: return_pct=33.538, profit_factor=1.2253, max_dd_pct=17.0166, ulcer_index=7.8344, trades=336, ready_gap=35, unexpected_skips=0

## Verdict

- status: `mixed_holdout_win_keep_incumbent`
- selected_run_name: `05W_no_trend_strength_0001`
- reason: `trial model improved holdout return/PF but trailed the incumbent on validation, so the incumbent stays promoted for now`

## Read

- validation leader: `05W_no_trend_strength_0001`
- holdout winner: `05CC_trend_proxy_persistence_downside_riskoff_0001`
- read: `treat model-family swaps with the same holdout gate as logic sweeps; validation spikes alone are not enough`
