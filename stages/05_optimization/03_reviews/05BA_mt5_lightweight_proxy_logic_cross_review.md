# 05BA Stage 05 Lightweight Proxy Logic Cross Review

Generated at: `2026-03-30T10:49:30.774775+00:00`

## Scope

- purpose: `cross lightweight proxy variants with alternate logic families to widen the search instead of narrowing too early`
- reference runs: `05W`, `05AI`, `05AJ`

## MT5 Validation Ranking

- [1] `05W_no_trend_strength_0001`: source=`incumbent`, mix=`margin_only`, Ts=-, Tl=-, margin=-, diff=-, return_pct=91.168, profit_factor=1.4092, max_dd_pct=11.1472, ulcer_index=6.5205, trades=493, ready_gap=0, unexpected_skips=0
- [2] `05AI_trend_proxy_light_pb_0001`: source=`light_pb`, mix=`margin_only`, Ts=-, Tl=-, margin=-, diff=-, return_pct=86.868, profit_factor=1.3884, max_dd_pct=11.7173, ulcer_index=6.8444, trades=485, ready_gap=0, unexpected_skips=0
- [3] `05AW_05aj_thr_margin_0001`: source=`light_vb`, mix=`threshold_margin`, Ts=0.5350, Tl=0.4000, margin=0.0700, diff=-, return_pct=86.626, profit_factor=1.7084, max_dd_pct=10.8796, ulcer_index=1.5009, trades=245, ready_gap=0, unexpected_skips=0
- [4] `05AX_05aj_thr_combo_0001`: source=`light_vb`, mix=`threshold_margin_diff`, Ts=0.5350, Tl=0.4000, margin=0.0500, diff=0.0700, return_pct=86.626, profit_factor=1.7084, max_dd_pct=10.8796, ulcer_index=1.5009, trades=245, ready_gap=0, unexpected_skips=0
- [5] `05AS_05ai_thr_margin_0001`: source=`light_pb`, mix=`threshold_margin`, Ts=0.5350, Tl=0.4000, margin=0.0700, diff=-, return_pct=85.754, profit_factor=1.7013, max_dd_pct=10.9516, ulcer_index=1.5052, trades=244, ready_gap=0, unexpected_skips=0
- [6] `05AT_05ai_thr_combo_0001`: source=`light_pb`, mix=`threshold_margin_diff`, Ts=0.5350, Tl=0.4000, margin=0.0500, diff=0.0700, return_pct=85.754, profit_factor=1.7013, max_dd_pct=10.9516, ulcer_index=1.5052, trades=244, ready_gap=0, unexpected_skips=0
- [7] `05AV_05ai_combo_loose_0001`: source=`light_pb`, mix=`margin_diff_loose`, Ts=0.3333, Tl=0.3333, margin=0.0500, diff=0.0700, return_pct=80.510, profit_factor=1.3499, max_dd_pct=12.8986, ulcer_index=7.3025, trades=492, ready_gap=0, unexpected_skips=0
- [8] `05AJ_trend_proxy_light_vb_0001`: source=`light_vb`, mix=`margin_only`, Ts=-, Tl=-, margin=-, diff=-, return_pct=75.362, profit_factor=1.3242, max_dd_pct=12.0620, ulcer_index=7.1696, trades=492, ready_gap=0, unexpected_skips=0
- [9] `05AZ_05aj_combo_loose_0001`: source=`light_vb`, mix=`margin_diff_loose`, Ts=0.3333, Tl=0.3333, margin=0.0500, diff=0.0700, return_pct=69.174, profit_factor=1.2905, max_dd_pct=13.3143, ulcer_index=7.6298, trades=498, ready_gap=0, unexpected_skips=0
- [10] `05AY_05aj_diff_only_0001`: source=`light_vb`, mix=`diff_only`, Ts=0.3333, Tl=0.3333, margin=-, diff=0.0775, return_pct=67.054, profit_factor=1.3161, max_dd_pct=12.4689, ulcer_index=6.5087, trades=462, ready_gap=0, unexpected_skips=0
- [11] `05AU_05ai_diff_only_0001`: source=`light_pb`, mix=`diff_only`, Ts=0.3333, Tl=0.3333, margin=-, diff=0.0775, return_pct=63.462, profit_factor=1.3004, max_dd_pct=12.1672, ulcer_index=6.4045, trades=457, ready_gap=0, unexpected_skips=0

## MT5 Holdout Ranking

- [1] `05AI_trend_proxy_light_pb_0001`: source=`light_pb`, mix=`margin_only`, Ts=-, Tl=-, margin=-, diff=-, return_pct=37.274, profit_factor=1.2542, max_dd_pct=17.0373, ulcer_index=7.7860, trades=330, ready_gap=35, unexpected_skips=0
- [2] `05AJ_trend_proxy_light_vb_0001`: source=`light_vb`, mix=`margin_only`, Ts=-, Tl=-, margin=-, diff=-, return_pct=34.760, profit_factor=1.2342, max_dd_pct=17.0373, ulcer_index=7.6654, trades=334, ready_gap=35, unexpected_skips=0
- [3] `05W_no_trend_strength_0001`: source=`incumbent`, mix=`margin_only`, Ts=-, Tl=-, margin=-, diff=-, return_pct=33.538, profit_factor=1.2253, max_dd_pct=17.0166, ulcer_index=7.8344, trades=336, ready_gap=35, unexpected_skips=0
- [4] `05AW_05aj_thr_margin_0001`: source=`light_vb`, mix=`threshold_margin`, Ts=0.5350, Tl=0.4000, margin=0.0700, diff=-, return_pct=2.384, profit_factor=1.0345, max_dd_pct=16.9030, ulcer_index=10.5363, trades=161, ready_gap=35, unexpected_skips=0
- [5] `05AX_05aj_thr_combo_0001`: source=`light_vb`, mix=`threshold_margin_diff`, Ts=0.5350, Tl=0.4000, margin=0.0500, diff=0.0700, return_pct=2.384, profit_factor=1.0345, max_dd_pct=16.9030, ulcer_index=10.5363, trades=161, ready_gap=35, unexpected_skips=0

## Verdict

- status: `reject_keep_incumbent`
- selected_run_name: `05W_no_trend_strength_0001`
- reason: `no cross candidate cleared the current incumbents on holdout`

## Read

- read: `this cross batch is breadth-first by design; mixed holdout-positive results should stay as challengers until they also prove validation durability`
