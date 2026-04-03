# 05AR Stage 05 Broad Logic Scan Review

Generated at: `2026-03-29T18:00:40.679661+00:00`

## Scope

- purpose: `scan diverse rule stacks on top of the 05W feature-side incumbent instead of narrowing too early`
- source model lineage: `05W_no_trend_strength_0001`

## MT5 Validation Ranking

- [1] `05W_no_trend_strength_0001`: mix=`incumbent`, Ts=-, Tl=-, margin=-, diff=-, return_pct=91.168, profit_factor=1.4092, max_dd_pct=11.1472, ulcer_index=6.5205, trades=493, ready_gap=0, unexpected_skips=0
- [2] `05AP_05w_thr_margin_0001`: mix=`threshold_margin_on_05w`, Ts=0.5350, Tl=0.4000, margin=0.0700, diff=-, return_pct=86.150, profit_factor=1.7021, max_dd_pct=10.8914, ulcer_index=1.4256, trades=250, ready_gap=0, unexpected_skips=0
- [3] `05AQ_05w_thr_combo_0001`: mix=`threshold_margin_diff_on_05w`, Ts=0.5350, Tl=0.4000, margin=0.0500, diff=0.0700, return_pct=86.150, profit_factor=1.7021, max_dd_pct=10.8914, ulcer_index=1.4256, trades=250, ready_gap=0, unexpected_skips=0
- [4] `05AO_05w_combo_loose_0001`: mix=`margin_diff_loose_on_05w`, Ts=0.3333, Tl=0.3333, margin=0.0500, diff=0.0700, return_pct=82.792, profit_factor=1.3594, max_dd_pct=12.8845, ulcer_index=7.3520, trades=500, ready_gap=0, unexpected_skips=0
- [5] `05AN_05w_diff_only_0001`: mix=`diff_only_on_05w`, Ts=0.3333, Tl=0.3333, margin=-, diff=0.0775, return_pct=63.130, profit_factor=1.2958, max_dd_pct=12.4030, ulcer_index=7.0333, trades=463, ready_gap=0, unexpected_skips=0

## MT5 Holdout Ranking

- [1] `05W_no_trend_strength_0001`: mix=`incumbent`, Ts=-, Tl=-, margin=-, diff=-, return_pct=33.538, profit_factor=1.2253, max_dd_pct=17.0166, ulcer_index=7.8344, trades=336, ready_gap=35, unexpected_skips=0
- [2] `05AP_05w_thr_margin_0001`: mix=`threshold_margin_on_05w`, Ts=0.5350, Tl=0.4000, margin=0.0700, diff=-, return_pct=5.752, profit_factor=1.0858, max_dd_pct=16.1339, ulcer_index=9.7962, trades=163, ready_gap=35, unexpected_skips=0

## Verdict

- status: `reject_keep_incumbent`
- selected_run_name: `05W_no_trend_strength_0001`
- reason: `no logic candidate cleared the incumbent on holdout`

## Read

- read: `this batch is breadth-first logic exploration on the 05W base; treat any holdout-positive mixed result as a challenger, not an automatic promotion`
