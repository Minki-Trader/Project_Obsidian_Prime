# 05DQ Stage 05 Model Family Trial Review

Generated at: `2026-03-30T14:08:53.173491+00:00`

## Scope

- purpose: `train a fresh trend_proxy_sector_logreg model on the frozen h/band dataset and run the current reference logic on MT5`
- logic reference: `05DJ_05bf_margin_hold5_0001` with `min_margin=0.0725`
- dropped sectors: `trend_strength`
- replacement sector: `trend_proxy_regime`
- trend_proxy_persistence: `ema20_ema50_diff, ema50_ema200_diff, trix_15`
- trend_proxy_risk_off_confirmation: `vix_change_1, vix_zscore_20, us10yr_change_1, us10yr_zscore_20, usdx_change_1, usdx_zscore_20`

## Offline Test Confirmation

- incumbent Stage 01 test: macro_f1=`0.4581`, balanced_accuracy=`0.4694`, accuracy=`0.5769`, log_loss=`0.9728`
- trial model test: macro_f1=`0.4573`, balanced_accuracy=`0.4685`, accuracy=`0.5760`, log_loss=`0.9739`

## MT5 Validation Ranking

- [1] `05DJ_05bf_margin_hold5_0001`: return_pct=119.436, profit_factor=1.5645, max_dd_pct=12.4696, ulcer_index=7.1858, trades=386, ready_gap=0, unexpected_skips=0
- [2] `05DQ_05ca_margin0725_hold5_0001`: return_pct=106.636, profit_factor=1.5021, max_dd_pct=15.8403, ulcer_index=7.5284, trades=375, ready_gap=0, unexpected_skips=0

## MT5 Holdout Ranking

- [1] `05DJ_05bf_margin_hold5_0001`: return_pct=59.190, profit_factor=1.4283, max_dd_pct=20.2732, ulcer_index=6.1801, trades=265, ready_gap=35, unexpected_skips=0
- [2] `05DQ_05ca_margin0725_hold5_0001`: return_pct=54.478, profit_factor=1.4179, max_dd_pct=21.3567, ulcer_index=6.6866, trades=250, ready_gap=35, unexpected_skips=0

## Verdict

- status: `reject_keep_incumbent`
- selected_run_name: `05DJ_05bf_margin_hold5_0001`
- reason: `trial model did not clear the incumbent on the holdout gate`

## Read

- validation leader: `05DJ_05bf_margin_hold5_0001`
- holdout winner: `05DJ_05bf_margin_hold5_0001`
- read: `treat model-family swaps with the same holdout gate as logic sweeps; validation spikes alone are not enough`
