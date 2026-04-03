# 05DY Stage 05 Model Family Trial Review

Generated at: `2026-03-30T14:28:29.818756+00:00`

## Scope

- purpose: `train a fresh trend_proxy_sector_logreg model on the frozen h/band dataset and run the current reference logic on MT5`
- logic reference: `05DP_05ca_margin0675_hold5_0001` with `min_margin=0.0663`
- dropped sectors: `trend_strength`
- replacement sector: `trend_proxy_regime`
- trend_proxy_persistence: `ema20_ema50_diff, ema50_ema200_diff, trix_15`
- trend_proxy_risk_off_confirmation: `vix_change_1, vix_zscore_20, us10yr_change_1, us10yr_zscore_20, usdx_change_1, usdx_zscore_20`

## Offline Test Confirmation

- incumbent Stage 01 test: macro_f1=`0.4581`, balanced_accuracy=`0.4694`, accuracy=`0.5769`, log_loss=`0.9728`
- trial model test: macro_f1=`0.4573`, balanced_accuracy=`0.4685`, accuracy=`0.5760`, log_loss=`0.9739`

## MT5 Validation Ranking

- [1] `05DP_05ca_margin0675_hold5_0001`: return_pct=122.570, profit_factor=1.5553, max_dd_pct=12.6031, ulcer_index=7.2871, trades=405, ready_gap=0, unexpected_skips=0
- [2] `05DY_05ca_margin06625_hold5_0001`: return_pct=114.880, profit_factor=1.5002, max_dd_pct=12.7910, ulcer_index=7.9823, trades=417, ready_gap=0, unexpected_skips=0

## MT5 Holdout Ranking

- [1] `05DP_05ca_margin0675_hold5_0001`: return_pct=68.574, profit_factor=1.4925, max_dd_pct=19.3936, ulcer_index=5.8587, trades=275, ready_gap=35, unexpected_skips=0
- [2] `05DY_05ca_margin06625_hold5_0001`: return_pct=54.286, profit_factor=1.3589, max_dd_pct=19.3936, ulcer_index=6.3259, trades=285, ready_gap=35, unexpected_skips=0

## Verdict

- status: `reject_keep_incumbent`
- selected_run_name: `05DP_05ca_margin0675_hold5_0001`
- reason: `trial model did not clear the incumbent on the holdout gate`

## Read

- validation leader: `05DP_05ca_margin0675_hold5_0001`
- holdout winner: `05DP_05ca_margin0675_hold5_0001`
- read: `treat model-family swaps with the same holdout gate as logic sweeps; validation spikes alone are not enough`
