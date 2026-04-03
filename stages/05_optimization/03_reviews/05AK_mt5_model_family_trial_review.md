# 05AK Stage 05 Model Family Trial Review

Generated at: `2026-03-29T17:47:14.483057+00:00`

## Scope

- purpose: `train a fresh trend_proxy_sector_logreg model on the frozen h/band dataset and run the current reference logic on MT5`
- logic reference: `05W_no_trend_strength_0001` with `min_margin=0.0700`
- dropped sectors: `trend_strength`
- replacement sector: `trend_proxy_regime`
- trend_proxy_persistence: `ema20_ema50_diff, ema50_ema200_diff, trix_15`
- trend_proxy_volatility_regime: `atr_14_over_atr_50, historical_vol_5_over_20, bb_squeeze`
- trend_proxy_breakout_pressure: `log_return_1, return_1_over_atr_14, hl_range`

## Offline Test Confirmation

- incumbent Stage 01 test: macro_f1=`0.4581`, balanced_accuracy=`0.4694`, accuracy=`0.5769`, log_loss=`0.9728`
- trial model test: macro_f1=`0.4591`, balanced_accuracy=`0.4697`, accuracy=`0.5774`, log_loss=`0.9736`

## MT5 Validation Ranking

- [1] `05W_no_trend_strength_0001`: return_pct=91.168, profit_factor=1.4092, max_dd_pct=11.1472, ulcer_index=6.5205, trades=493, ready_gap=0, unexpected_skips=0
- [2] `05AK_trend_proxy_light_core3_0001`: return_pct=61.826, profit_factor=1.2557, max_dd_pct=13.9113, ulcer_index=8.3938, trades=493, ready_gap=0, unexpected_skips=0

## Verdict

- status: `validation_only_pending_holdout`
- selected_run_name: `05W_no_trend_strength_0001`
- reason: `holdout not run yet, so the incumbent remains the selected bundle`

## Read

- validation leader: `05W_no_trend_strength_0001`
- read: `treat model-family swaps with the same holdout gate as logic sweeps; validation spikes alone are not enough`
