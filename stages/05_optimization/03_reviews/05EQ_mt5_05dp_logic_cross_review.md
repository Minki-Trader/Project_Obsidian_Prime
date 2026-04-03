# 05EQ Stage 05 05DP Logic Cross Review

Generated at: `2026-03-30T15:09:35.126542+00:00`

## Scope

- purpose: `re-open broader logic exploration from the stabilized 05DP line using non-additive gates and threshold asymmetry while keeping the feature/model bundle fixed`
- promoted incumbent: `05DP`

## MT5 Validation Ranking

- [1] `05DP_05ca_margin0675_hold5_0001`: mix=`promoted_05dp`, short_thr=-, long_thr=-, margin=-, diff=-, return_pct=122.570, profit_factor=1.5553, max_dd_pct=12.6031, ulcer_index=7.2871, trades=405, ready_gap=0, unexpected_skips=0
- [2] `05EA_05ca_margin0675_hold4_0001`: mix=`hold4_sibling_05ea`, short_thr=-, long_thr=-, margin=-, diff=-, return_pct=115.168, profit_factor=1.5352, max_dd_pct=11.5023, ulcer_index=6.5293, trades=453, ready_gap=0, unexpected_skips=0
- [3] `05DN_05ca_margin_hold5_0001`: mix=`same_family_05dn`, short_thr=-, long_thr=-, margin=-, diff=-, return_pct=109.314, profit_factor=1.5024, max_dd_pct=13.2239, ulcer_index=7.5148, trades=388, ready_gap=0, unexpected_skips=0
- [4] `05EM_05dp_short_bias_margin_hold5_0001`: mix=`short_bias_margin_hold5`, short_thr=0.3000, long_thr=0.4500, margin=0.0675, diff=-, return_pct=109.204, profit_factor=1.5289, max_dd_pct=13.0566, ulcer_index=7.9882, trades=356, ready_gap=0, unexpected_skips=0
- [5] `05EL_05dp_combo_loose_hold5_0001`: mix=`combo_loose_hold5`, short_thr=0.3333, long_thr=0.3333, margin=0.0500, diff=0.0700, return_pct=103.330, profit_factor=1.4582, max_dd_pct=13.7511, ulcer_index=7.9488, trades=395, ready_gap=0, unexpected_skips=0
- [6] `05DL_05cc_margin_hold5_0001`: mix=`risk_alt_05dl`, short_thr=-, long_thr=-, margin=-, diff=-, return_pct=99.682, profit_factor=1.4448, max_dd_pct=14.9161, ulcer_index=7.6350, trades=393, ready_gap=0, unexpected_skips=0
- [7] `05EP_05dp_balanced_tight_margin_hold5_0001`: mix=`balanced_tight_margin_hold5`, short_thr=0.4500, long_thr=0.4500, margin=0.0675, diff=-, return_pct=95.908, profit_factor=1.5214, max_dd_pct=10.7911, ulcer_index=6.4129, trades=289, ready_gap=0, unexpected_skips=0
- [8] `05EK_05dp_diff_only_hold5_0001`: mix=`diff_only_hold5`, short_thr=0.3333, long_thr=0.3333, margin=-, diff=0.0775, return_pct=92.640, profit_factor=1.4372, max_dd_pct=12.6843, ulcer_index=5.9084, trades=371, ready_gap=0, unexpected_skips=0
- [9] `05EO_05dp_short_bias_combo_hold5_0001`: mix=`short_bias_combo_hold5`, short_thr=0.3000, long_thr=0.4500, margin=0.0500, diff=0.0700, return_pct=91.690, profit_factor=1.4345, max_dd_pct=15.5133, ulcer_index=8.7054, trades=350, ready_gap=0, unexpected_skips=0
- [10] `05EN_05dp_short_bias_diff_hold5_0001`: mix=`short_bias_diff_hold5`, short_thr=0.3000, long_thr=0.4500, margin=-, diff=0.0775, return_pct=82.050, profit_factor=1.4089, max_dd_pct=13.9718, ulcer_index=6.9871, trades=332, ready_gap=0, unexpected_skips=0

## MT5 Holdout Ranking

- [1] `05DP_05ca_margin0675_hold5_0001`: mix=`promoted_05dp`, short_thr=-, long_thr=-, margin=-, diff=-, return_pct=68.574, profit_factor=1.4925, max_dd_pct=19.3936, ulcer_index=5.8587, trades=275, ready_gap=35, unexpected_skips=0
- [2] `05EM_05dp_short_bias_margin_hold5_0001`: mix=`short_bias_margin_hold5`, short_thr=0.3000, long_thr=0.4500, margin=0.0675, diff=-, return_pct=64.534, profit_factor=1.5249, max_dd_pct=20.1849, ulcer_index=6.0536, trades=229, ready_gap=35, unexpected_skips=0
- [3] `05DN_05ca_margin_hold5_0001`: mix=`same_family_05dn`, short_thr=-, long_thr=-, margin=-, diff=-, return_pct=60.940, profit_factor=1.4517, max_dd_pct=20.2732, ulcer_index=6.2392, trades=263, ready_gap=35, unexpected_skips=0
- [4] `05DL_05cc_margin_hold5_0001`: mix=`risk_alt_05dl`, short_thr=-, long_thr=-, margin=-, diff=-, return_pct=58.852, profit_factor=1.4311, max_dd_pct=18.3944, ulcer_index=5.5864, trades=267, ready_gap=35, unexpected_skips=0
- [5] `05EL_05dp_combo_loose_hold5_0001`: mix=`combo_loose_hold5`, short_thr=0.3333, long_thr=0.3333, margin=0.0500, diff=0.0700, return_pct=56.374, profit_factor=1.4000, max_dd_pct=19.6982, ulcer_index=6.3475, trades=270, ready_gap=35, unexpected_skips=0
- [6] `05EA_05ca_margin0675_hold4_0001`: mix=`hold4_sibling_05ea`, short_thr=-, long_thr=-, margin=-, diff=-, return_pct=53.742, profit_factor=1.3652, max_dd_pct=17.9030, ulcer_index=6.2325, trades=304, ready_gap=35, unexpected_skips=0

## Verdict

- status: `reject_keep_incumbent`
- selected_run_name: `05DP_05ca_margin0675_hold5_0001`
- reason: `no logic-cross candidate cleared 05DP on holdout`

## Read

- read: `this batch asks whether the 05DP frontier is limited by feature expressiveness or by how we gate the same probability output into trades`
