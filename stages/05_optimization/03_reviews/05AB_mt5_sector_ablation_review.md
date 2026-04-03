# 05AB Stage 05 MT5 Sector Ablation Review

Generated at: `2026-03-29T16:59:10.601328+00:00`

## Scope

- purpose: `remove one Stage 01 base-feature sector at a time and see which omissions improve or damage MT5 behavior under the current 03E logic`
- model family: `logistic_regression`
- logic: `03E margin-only (min_margin=0.0700)`

## MT5 Validation Ranking

- [1] `05W_no_trend_strength_0001`: sector=`trend_strength`, return_pct=91.168, profit_factor=1.4092, max_dd_pct=11.1472, ulcer_index=6.5205, trades=493, remaining_features=54, ready_gap=0, unexpected_skips=0
- [2] `05S_no_price_return_0001`: sector=`price_return`, return_pct=89.294, profit_factor=1.3757, max_dd_pct=9.7109, ulcer_index=2.3986, trades=514, remaining_features=48, ready_gap=0, unexpected_skips=0
- [3] `05T_no_ma_trend_0001`: sector=`moving_average_trend`, return_pct=81.246, profit_factor=1.5315, max_dd_pct=12.3893, ulcer_index=2.3666, trades=325, remaining_features=51, ready_gap=0, unexpected_skips=0
- [4] `05Z_no_leader_rel_0001`: sector=`leader_relative`, return_pct=77.970, profit_factor=1.3351, max_dd_pct=11.7978, ulcer_index=3.5706, trades=523, remaining_features=50, ready_gap=0, unexpected_skips=0
- [5] `05X_no_session_ctx_0001`: sector=`session_context`, return_pct=75.382, profit_factor=1.3201, max_dd_pct=11.6004, ulcer_index=2.3678, trades=499, remaining_features=54, ready_gap=0, unexpected_skips=0
- [6] `05U_no_momentum_osc_0001`: sector=`momentum_oscillator`, return_pct=62.954, profit_factor=1.2822, max_dd_pct=12.4712, ulcer_index=4.3820, trades=461, remaining_features=49, ready_gap=0, unexpected_skips=0
- [7] `05V_no_vol_band_0001`: sector=`volatility_band`, return_pct=55.980, profit_factor=1.2701, max_dd_pct=14.4656, ulcer_index=4.3969, trades=429, remaining_features=50, ready_gap=0, unexpected_skips=0
- [8] `05AA_no_breadth_disp_0001`: sector=`breadth_dispersion`, return_pct=49.110, profit_factor=1.1920, max_dd_pct=13.6310, ulcer_index=5.1605, trades=501, remaining_features=56, ready_gap=0, unexpected_skips=0
- [9] `05Y_no_risk_proxy_0001`: sector=`risk_proxy`, return_pct=42.082, profit_factor=1.1793, max_dd_pct=16.5588, ulcer_index=9.3646, trades=494, remaining_features=52, ready_gap=0, unexpected_skips=0

## MT5 Holdout Ranking

- [1] `05W_no_trend_strength_0001`: sector=`trend_strength`, return_pct=33.538, profit_factor=1.2253, max_dd_pct=17.0166, ulcer_index=7.8344, trades=336, ready_gap=35, unexpected_skips=0
- [2] `03E_mt5_validation_baseline_0001`: sector=`incumbent`, return_pct=7.072, profit_factor=1.0441, max_dd_pct=20.0228, ulcer_index=8.1911, trades=357, ready_gap=35, unexpected_skips=0

## Verdict

- status: `promote_candidate`
- selected_run_name: `05W_no_trend_strength_0001`
- reason: `sector-ablation candidate cleared the holdout gate versus the incumbent`

## Read

- read: `sector ablation is useful for finding redundancy, but promotion still requires the same holdout gate as every other Stage 05 exploration path`
