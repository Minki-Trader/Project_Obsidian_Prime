# 05AG Stage 05 Trend-Strength Feature Ablation Review

Generated at: `2026-03-29T17:22:47.203715+00:00`

## Scope

- purpose: `drop one trend_strength feature at a time to see whether a single toxic feature explains the 05W sector-ablation win`
- model family: `logistic_regression`
- logic: `margin-only (min_margin=0.0700)`
- incumbent reference: `05W_no_trend_strength_0001`

## MT5 Validation Ranking

- [1] `05AD_drop_di_spread14_0001`: drop_feature=`di_spread_14`, offline_test_macro_f1=0.4566, return_pct=76.554, profit_factor=1.3094, max_dd_pct=11.1513, ulcer_index=4.3348, trades=524, remaining_features=57, ready_gap=0, unexpected_skips=0
- [2] `05AF_drop_vortex_indicator_0001`: drop_feature=`vortex_indicator`, offline_test_macro_f1=0.4560, return_pct=73.574, profit_factor=1.2927, max_dd_pct=11.8586, ulcer_index=3.0411, trades=533, remaining_features=57, ready_gap=0, unexpected_skips=0
- [3] `05AC_drop_adx14_0001`: drop_feature=`adx_14`, offline_test_macro_f1=0.4570, return_pct=68.006, profit_factor=1.2725, max_dd_pct=11.9457, ulcer_index=3.6810, trades=532, remaining_features=57, ready_gap=0, unexpected_skips=0
- [4] `05AE_drop_supertrend103_0001`: drop_feature=`supertrend_10_3`, offline_test_macro_f1=0.4553, return_pct=65.958, profit_factor=1.2826, max_dd_pct=12.5845, ulcer_index=4.2484, trades=523, remaining_features=57, ready_gap=0, unexpected_skips=0

## MT5 Holdout Ranking

- [1] `05W_no_trend_strength_0001`: drop_feature=`incumbent`, return_pct=33.538, profit_factor=1.2253, max_dd_pct=17.0166, ulcer_index=7.8344, trades=336, ready_gap=35, unexpected_skips=0
- [2] `05AD_drop_di_spread14_0001`: drop_feature=`di_spread_14`, return_pct=23.920, profit_factor=1.1485, max_dd_pct=24.3031, ulcer_index=7.7829, trades=346, ready_gap=35, unexpected_skips=0

## Verdict

- status: `reject_keep_incumbent`
- selected_run_name: `05W_no_trend_strength_0001`
- reason: `holdout still favors the current feature-side incumbent`

## Read

- read: `if no single-feature drop beats the sector-level incumbent, the edge likely comes from removing a correlated cluster rather than one obviously toxic feature`
