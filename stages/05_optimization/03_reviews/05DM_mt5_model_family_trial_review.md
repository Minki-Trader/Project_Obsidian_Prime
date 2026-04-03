# 05DM Stage 05 Model Family Trial Review

Generated at: `2026-03-30T13:40:11.259714+00:00`

## Scope

- purpose: `train a fresh trend_proxy_sector_logreg model on the frozen h/band dataset and run the current reference logic on MT5`
- logic reference: `05DJ_05bf_margin_hold5_0001` with `min_margin=0.0700`
- dropped sectors: `trend_strength`
- replacement sector: `trend_proxy_regime`
- trend_proxy_persistence: `ema20_ema50_diff, ema50_ema200_diff, trix_15`
- trend_proxy_downside_pressure: `close_ema20_ratio, close_ema50_ratio, overnight_return, return_1_over_atr_14, us100_minus_mega8_equal_return_1, us100_minus_top3_weighted_return_1`
- trend_proxy_risk_off_confirmation: `vix_change_1, vix_zscore_20, us10yr_change_1, us10yr_zscore_20, usdx_change_1, usdx_zscore_20`

## Offline Test Confirmation

- incumbent Stage 01 test: macro_f1=`0.4581`, balanced_accuracy=`0.4694`, accuracy=`0.5769`, log_loss=`0.9728`
- trial model test: macro_f1=`0.4565`, balanced_accuracy=`0.4676`, accuracy=`0.5754`, log_loss=`0.9736`

## MT5 Validation Ranking

- [1] `05DJ_05bf_margin_hold5_0001`: return_pct=119.436, profit_factor=1.5645, max_dd_pct=12.4696, ulcer_index=7.1858, trades=386, ready_gap=0, unexpected_skips=0
- [2] `05DM_05cc_margin_hold4_0001`: return_pct=92.446, profit_factor=1.4194, max_dd_pct=14.5029, ulcer_index=6.8711, trades=435, ready_gap=0, unexpected_skips=0

## Verdict

- status: `validation_only_pending_holdout`
- selected_run_name: `05DJ_05bf_margin_hold5_0001`
- reason: `holdout not run yet, so the incumbent remains the selected bundle`

## Read

- validation leader: `05DJ_05bf_margin_hold5_0001`
- read: `treat model-family swaps with the same holdout gate as logic sweeps; validation spikes alone are not enough`
