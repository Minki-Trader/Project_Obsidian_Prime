# 05I Stage 05 Alternate Model MT5 Review

Generated at: `2026-03-29T15:23:19.332041+00:00`

## Scope

- purpose: `swap the Stage 01 baseline learner while keeping the current 03E logic fixed on MT5 validation`
- source candidate: `01C_run_0002_h03_band000125_lightgbm` (lightgbm)
- logic reference: `03E_mt5_validation_baseline_0001` with `min_margin=0.0700`
- holdout policy: `reopened because the alternate model materially exceeded the current validation frontier`

## Offline Test Confirmation

- incumbent Stage 01 test: macro_f1=`0.4581`, balanced_accuracy=`0.4694`, accuracy=`0.5769`, log_loss=`0.9728`
- alternate model test: macro_f1=`0.4532`, balanced_accuracy=`0.4638`, accuracy=`0.5713`, log_loss=`0.8978`

## MT5 Validation Ranking

- [1] `05I_mt5_validation_margin_lightgbm_modelswap_0001`: return_pct=1308.556, profit_factor=15.2902, max_dd_pct=1.9298, ulcer_index=0.0841, trades=1554, ready_gap=0, unexpected_skips=0
- [2] `03E_mt5_validation_baseline_0001`: return_pct=67.664, profit_factor=1.2655, max_dd_pct=12.2017, ulcer_index=3.5570, trades=530, ready_gap=0, unexpected_skips=0

## MT5 Holdout Ranking

- [1] `03E_mt5_validation_baseline_0001`: return_pct=7.0720, profit_factor=1.0441, max_dd_pct=20.0228, ulcer_index=8.1911, trades=357, ready_gap=35, unexpected_skips=0
- [2] `05I_mt5_validation_margin_lightgbm_modelswap_0001`: return_pct=-5.0700, profit_factor=0.9854, max_dd_pct=29.9836, ulcer_index=16.7447, trades=794, ready_gap=35, unexpected_skips=0

## Read

- validation leader from this comparison: `05I_mt5_validation_margin_lightgbm_modelswap_0001`
- holdout winner from this comparison: `03E_mt5_validation_baseline_0001`
- verdict: `do not promote the alternate LightGBM model family`
- read: `05I` produced an extreme validation spike, but it failed the shared MT5 holdout gate immediately and with materially worse drawdown than `03E`
