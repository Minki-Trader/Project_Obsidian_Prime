# 05DT Stage 05 Model Family Trial Review

Generated at: `2026-03-30T14:01:35.053975+00:00`

## Scope

- purpose: `train a fresh trend_proxy_sector_logreg model on the frozen h/band dataset and run the current reference logic on MT5`
- logic reference: `05DJ_05bf_margin_hold5_0001` with `min_margin=0.0700`
- dropped sectors: `trend_strength`
- replacement sector: `trend_proxy_regime`
- trend_proxy_persistence: `ema20_ema50_diff, ema50_ema200_diff, trix_15`
- trend_proxy_risk_off_confirmation: `vix_change_1, vix_zscore_20, us10yr_change_1, us10yr_zscore_20, usdx_change_1, usdx_zscore_20`

## Offline Test Confirmation

- incumbent Stage 01 test: macro_f1=`0.4581`, balanced_accuracy=`0.4694`, accuracy=`0.5769`, log_loss=`0.9728`
- trial model test: macro_f1=`0.4573`, balanced_accuracy=`0.4685`, accuracy=`0.5760`, log_loss=`0.9739`

## MT5 Validation Ranking

- [1] `05DJ_05bf_margin_hold5_0001`: return_pct=119.436, profit_factor=1.5645, max_dd_pct=12.4696, ulcer_index=7.1858, trades=386, ready_gap=0, unexpected_skips=0
- [2] `05DT_05ca_margin0700_hold6_0001`: return_pct=92.632, profit_factor=1.4004, max_dd_pct=14.8844, ulcer_index=9.3741, trades=358, ready_gap=0, unexpected_skips=0

## Verdict

- status: `validation_only_pending_holdout`
- selected_run_name: `05DJ_05bf_margin_hold5_0001`
- reason: `holdout not run yet, so the incumbent remains the selected bundle`

## Read

- validation leader: `05DJ_05bf_margin_hold5_0001`
- read: `treat model-family swaps with the same holdout gate as logic sweeps; validation spikes alone are not enough`
