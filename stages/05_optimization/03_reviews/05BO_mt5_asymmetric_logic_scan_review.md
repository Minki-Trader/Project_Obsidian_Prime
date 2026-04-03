# 05BO Stage 05 Asymmetric Logic Scan Review

Generated at: `2026-03-30T11:38:10.814327+00:00`

## Scope

- purpose: `widen logic-side exploration with directional threshold asymmetry instead of repeating symmetric copies of the same gate`
- source model lineage: `05W_no_trend_strength_0001`

## MT5 Validation Ranking

- [1] `05W_no_trend_strength_0001`: mix=`incumbent`, Ts=-, Tl=-, margin=-, diff=-, return_pct=91.168, profit_factor=1.4092, max_dd_pct=11.1472, ulcer_index=6.5205, trades=493, ready_gap=0, unexpected_skips=0
- [2] `05BK_05w_long_bias_margin_0001`: mix=`long_bias_margin`, Ts=0.5750, Tl=0.3750, margin=0.0700, diff=-, return_pct=85.582, profit_factor=1.8606, max_dd_pct=12.0744, ulcer_index=0.9020, trades=220, ready_gap=0, unexpected_skips=0
- [3] `05BM_05w_balanced_tight_margin_0001`: mix=`balanced_tight_margin`, Ts=0.4500, Tl=0.4500, margin=0.0700, diff=-, return_pct=77.296, profit_factor=1.4200, max_dd_pct=11.0647, ulcer_index=6.6881, trades=355, ready_gap=0, unexpected_skips=0
- [4] `05BI_05w_short_bias_margin_0001`: mix=`short_bias_margin`, Ts=0.3000, Tl=0.4500, margin=0.0700, diff=-, return_pct=68.414, profit_factor=1.3139, max_dd_pct=14.3445, ulcer_index=8.7746, trades=446, ready_gap=0, unexpected_skips=0
- [5] `05BN_05w_balanced_tight_diff_0001`: mix=`balanced_tight_diff`, Ts=0.4500, Tl=0.4500, margin=-, diff=0.0775, return_pct=63.282, profit_factor=1.3594, max_dd_pct=11.1458, ulcer_index=6.6483, trades=334, ready_gap=0, unexpected_skips=0
- [6] `05BL_05w_long_bias_diff_0001`: mix=`long_bias_diff`, Ts=0.5750, Tl=0.3750, margin=-, diff=0.0775, return_pct=62.228, profit_factor=1.6282, max_dd_pct=13.9967, ulcer_index=1.3846, trades=204, ready_gap=0, unexpected_skips=0
- [7] `05BJ_05w_short_bias_diff_0001`: mix=`short_bias_diff`, Ts=0.3000, Tl=0.4500, margin=-, diff=0.0775, return_pct=53.004, profit_factor=1.2588, max_dd_pct=13.4258, ulcer_index=8.1820, trades=416, ready_gap=0, unexpected_skips=0

## MT5 Holdout Ranking

- [1] `05W_no_trend_strength_0001`: mix=`incumbent`, Ts=-, Tl=-, margin=-, diff=-, return_pct=33.538, profit_factor=1.2253, max_dd_pct=17.0166, ulcer_index=7.8344, trades=336, ready_gap=35, unexpected_skips=0
- [2] `05BM_05w_balanced_tight_margin_0001`: mix=`balanced_tight_margin`, Ts=0.4500, Tl=0.4500, margin=0.0700, diff=-, return_pct=28.584, profit_factor=1.2730, max_dd_pct=14.0365, ulcer_index=7.8101, trades=227, ready_gap=35, unexpected_skips=0
- [3] `05BK_05w_long_bias_margin_0001`: mix=`long_bias_margin`, Ts=0.5750, Tl=0.3750, margin=0.0700, diff=-, return_pct=6.722, profit_factor=1.1126, max_dd_pct=11.8186, ulcer_index=6.7104, trades=159, ready_gap=35, unexpected_skips=0

## Verdict

- status: `reject_keep_incumbent`
- selected_run_name: `05W_no_trend_strength_0001`
- reason: `no asymmetric logic candidate cleared the incumbent on holdout`

## Read

- read: `asymmetric threshold scans are meant to test whether the strong short-side holdout behavior can be harvested without sacrificing too much validation durability`
