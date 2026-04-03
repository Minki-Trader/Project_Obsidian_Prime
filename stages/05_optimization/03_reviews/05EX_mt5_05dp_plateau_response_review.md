# 05EX Stage 05 05DP Plateau Response Review

Generated at: `2026-03-30T15:54:51.430143+00:00`

## Scope

- purpose: `target the observed plateau behavior directly by suppressing longs, shortening hold, and adding light flat-regime avoidance while keeping the 05DP feature/model bundle fixed`
- promoted incumbent: `05DP`

## MT5 Validation Ranking

- [1] `05DP_05ca_margin0675_hold5_0001`: mix=`promoted_05dp`, short_thr=-, long_thr=-, hold=-, margin=-, diff=-, return_pct=122.570, profit_factor=1.5553, max_dd_pct=12.6031, ulcer_index=7.2871, trades=405, ready_gap=0, unexpected_skips=0
- [2] `05EA_05ca_margin0675_hold4_0001`: mix=`hold4_ref_05ea`, short_thr=-, long_thr=-, hold=-, margin=-, diff=-, return_pct=115.168, profit_factor=1.5352, max_dd_pct=11.5023, ulcer_index=6.5293, trades=453, ready_gap=0, unexpected_skips=0
- [3] `05EM_05dp_short_bias_margin_hold5_0001`: mix=`short_bias_ref_05em`, short_thr=-, long_thr=-, hold=-, margin=-, diff=-, return_pct=109.204, profit_factor=1.5289, max_dd_pct=13.0566, ulcer_index=7.9882, trades=356, ready_gap=0, unexpected_skips=0
- [4] `05ER_05dp_short_bias_margin_hold4_0001`: mix=`short_bias_margin_hold4`, short_thr=0.3000, long_thr=0.4500, hold=4, margin=0.0675, diff=-, return_pct=102.634, profit_factor=1.5067, max_dd_pct=12.6582, ulcer_index=7.8586, trades=397, ready_gap=0, unexpected_skips=0
- [5] `05DL_05cc_margin_hold5_0001`: mix=`risk_alt_05dl`, short_thr=-, long_thr=-, hold=-, margin=-, diff=-, return_pct=99.682, profit_factor=1.4448, max_dd_pct=14.9161, ulcer_index=7.6350, trades=393, ready_gap=0, unexpected_skips=0
- [6] `05ES_05dp_stronger_long_suppression_hold5_0001`: mix=`short_bias_margin_long050_hold5`, short_thr=0.3000, long_thr=0.5000, hold=5, margin=0.0675, diff=-, return_pct=96.932, profit_factor=1.5316, max_dd_pct=13.4620, ulcer_index=8.0777, trades=309, ready_gap=0, unexpected_skips=0
- [7] `05ET_05dp_stronger_long_suppression_hold4_0001`: mix=`short_bias_margin_long050_hold4`, short_thr=0.3000, long_thr=0.5000, hold=4, margin=0.0675, diff=-, return_pct=91.330, profit_factor=1.5092, max_dd_pct=13.1747, ulcer_index=8.0439, trades=346, ready_gap=0, unexpected_skips=0
- [8] `05EW_05dp_balanced_tight_combo_hold5_0001`: mix=`balanced_tight_combo_hold5`, short_thr=0.4500, long_thr=0.4500, hold=5, margin=0.0500, diff=0.0700, return_pct=90.542, profit_factor=1.4985, max_dd_pct=10.6569, ulcer_index=6.2199, trades=282, ready_gap=0, unexpected_skips=0
- [9] `05EV_05dp_short_bias_combo_hold4_0001`: mix=`short_bias_combo_hold4`, short_thr=0.3000, long_thr=0.4500, hold=4, margin=0.0500, diff=0.0700, return_pct=90.092, profit_factor=1.4420, max_dd_pct=13.9062, ulcer_index=8.3820, trades=384, ready_gap=0, unexpected_skips=0
- [10] `05EU_05dp_near_short_only_hold5_0001`: mix=`near_short_only_margin_hold5`, short_thr=0.3000, long_thr=0.6000, hold=5, margin=0.0675, diff=-, return_pct=68.948, profit_factor=1.4599, max_dd_pct=13.6789, ulcer_index=7.9481, trades=255, ready_gap=0, unexpected_skips=0

## MT5 Holdout Ranking

- [1] `05DP_05ca_margin0675_hold5_0001`: mix=`promoted_05dp`, short_thr=-, long_thr=-, hold=-, margin=-, diff=-, return_pct=68.574, profit_factor=1.4925, max_dd_pct=19.3936, ulcer_index=5.8587, trades=275, ready_gap=35, unexpected_skips=0
- [2] `05EM_05dp_short_bias_margin_hold5_0001`: mix=`short_bias_ref_05em`, short_thr=-, long_thr=-, hold=-, margin=-, diff=-, return_pct=64.534, profit_factor=1.5249, max_dd_pct=20.1849, ulcer_index=6.0536, trades=229, ready_gap=35, unexpected_skips=0
- [3] `05DL_05cc_margin_hold5_0001`: mix=`risk_alt_05dl`, short_thr=-, long_thr=-, hold=-, margin=-, diff=-, return_pct=58.852, profit_factor=1.4311, max_dd_pct=18.3944, ulcer_index=5.5864, trades=267, ready_gap=35, unexpected_skips=0
- [4] `05EA_05ca_margin0675_hold4_0001`: mix=`hold4_ref_05ea`, short_thr=-, long_thr=-, hold=-, margin=-, diff=-, return_pct=53.742, profit_factor=1.3652, max_dd_pct=17.9030, ulcer_index=6.2325, trades=304, ready_gap=35, unexpected_skips=0
- [5] `05ER_05dp_short_bias_margin_hold4_0001`: mix=`short_bias_margin_hold4`, short_thr=0.3000, long_thr=0.4500, hold=4, margin=0.0675, diff=-, return_pct=49.452, profit_factor=1.3845, max_dd_pct=18.3829, ulcer_index=6.7534, trades=249, ready_gap=35, unexpected_skips=0
- [6] `05ES_05dp_stronger_long_suppression_hold5_0001`: mix=`short_bias_margin_long050_hold5`, short_thr=0.3000, long_thr=0.5000, hold=5, margin=0.0675, diff=-, return_pct=47.788, profit_factor=1.4196, max_dd_pct=20.9706, ulcer_index=6.7349, trades=190, ready_gap=35, unexpected_skips=0

## Verdict

- status: `reject_keep_incumbent`
- selected_run_name: `05DP_05ca_margin0675_hold5_0001`
- reason: `no plateau-response candidate cleared 05DP on holdout`

## Read

- read: `this batch asks whether the plateau is mainly a long-side drag problem, a hold-length problem, or a flat-regime gating problem`
