# 05FW Stage 05 05DP Regime Exit Review

Generated at: `2026-03-31T14:07:24.946743+00:00`

## Scope

- purpose: `retest 05DP with exit-side regime handling by adding a flat-probability guard on top of the incumbent time exit`
- promoted incumbent: `05DP`

## MT5 Validation Ranking

- [1] `05DP_05ca_margin0675_hold5_0001`: variant=`promoted_05dp`, max_hold=-, flat_exit_prob=-, flat_exit_min_hold=-, return_pct=122.570, profit_factor=1.5553, max_dd_pct=12.6031, ulcer_index=7.2871, trades=405, ready_gap=0, unexpected_skips=0
- [2] `05FR_05dp_flatexit052_hold1_0001`: variant=`flat_exit052_hold1`, max_hold=5, flat_exit_prob=0.5200, flat_exit_min_hold=1, return_pct=122.570, profit_factor=1.5553, max_dd_pct=12.6031, ulcer_index=7.2871, trades=405, ready_gap=0, unexpected_skips=0
- [3] `05FS_05dp_flatexit055_hold1_0001`: variant=`flat_exit055_hold1`, max_hold=5, flat_exit_prob=0.5500, flat_exit_min_hold=1, return_pct=122.570, profit_factor=1.5553, max_dd_pct=12.6031, ulcer_index=7.2871, trades=405, ready_gap=0, unexpected_skips=0
- [4] `05FT_05dp_flatexit055_hold2_0001`: variant=`flat_exit055_hold2`, max_hold=5, flat_exit_prob=0.5500, flat_exit_min_hold=2, return_pct=122.570, profit_factor=1.5553, max_dd_pct=12.6031, ulcer_index=7.2871, trades=405, ready_gap=0, unexpected_skips=0
- [5] `05FU_05dp_flatexit058_hold1_0001`: variant=`flat_exit058_hold1`, max_hold=5, flat_exit_prob=0.5800, flat_exit_min_hold=1, return_pct=122.570, profit_factor=1.5553, max_dd_pct=12.6031, ulcer_index=7.2871, trades=405, ready_gap=0, unexpected_skips=0
- [6] `05FV_05dp_flatexit060_hold2_0001`: variant=`flat_exit060_hold2`, max_hold=5, flat_exit_prob=0.6000, flat_exit_min_hold=2, return_pct=122.570, profit_factor=1.5553, max_dd_pct=12.6031, ulcer_index=7.2871, trades=405, ready_gap=0, unexpected_skips=0
- [7] `05FY_05dp_flatexit048_hold1_0001`: variant=`flat_exit048_hold1`, max_hold=5, flat_exit_prob=0.4800, flat_exit_min_hold=1, return_pct=122.570, profit_factor=1.5553, max_dd_pct=12.6031, ulcer_index=7.2871, trades=405, ready_gap=0, unexpected_skips=0
- [8] `05FZ_05dp_flatexit050_hold1_0001`: variant=`flat_exit050_hold1`, max_hold=5, flat_exit_prob=0.5000, flat_exit_min_hold=1, return_pct=122.570, profit_factor=1.5553, max_dd_pct=12.6031, ulcer_index=7.2871, trades=405, ready_gap=0, unexpected_skips=0
- [9] `05FX_05dp_flatexit045_hold1_0001`: variant=`flat_exit045_hold1`, max_hold=5, flat_exit_prob=0.4500, flat_exit_min_hold=1, return_pct=122.402, profit_factor=1.5541, max_dd_pct=12.6031, ulcer_index=7.3116, trades=405, ready_gap=0, unexpected_skips=0
- [10] `05EM_05dp_short_bias_margin_hold5_0001`: variant=`closest_short_bias_05em`, max_hold=-, flat_exit_prob=-, flat_exit_min_hold=-, return_pct=109.204, profit_factor=1.5289, max_dd_pct=13.0566, ulcer_index=7.9882, trades=356, ready_gap=0, unexpected_skips=0
- [11] `05DL_05cc_margin_hold5_0001`: variant=`lower_ulcer_alt_05dl`, max_hold=-, flat_exit_prob=-, flat_exit_min_hold=-, return_pct=99.682, profit_factor=1.4448, max_dd_pct=14.9161, ulcer_index=7.6350, trades=393, ready_gap=0, unexpected_skips=0

## MT5 Holdout Ranking

- [1] `05DP_05ca_margin0675_hold5_0001`: variant=`promoted_05dp`, max_hold=-, flat_exit_prob=-, flat_exit_min_hold=-, return_pct=68.574, profit_factor=1.4925, max_dd_pct=19.3936, ulcer_index=5.8587, trades=275, ready_gap=35, unexpected_skips=0
- [2] `05FR_05dp_flatexit052_hold1_0001`: variant=`flat_exit052_hold1`, max_hold=5, flat_exit_prob=0.5200, flat_exit_min_hold=1, return_pct=68.574, profit_factor=1.4925, max_dd_pct=19.3936, ulcer_index=5.8587, trades=275, ready_gap=35, unexpected_skips=0
- [3] `05FS_05dp_flatexit055_hold1_0001`: variant=`flat_exit055_hold1`, max_hold=5, flat_exit_prob=0.5500, flat_exit_min_hold=1, return_pct=68.574, profit_factor=1.4925, max_dd_pct=19.3936, ulcer_index=5.8587, trades=275, ready_gap=35, unexpected_skips=0
- [4] `05EM_05dp_short_bias_margin_hold5_0001`: variant=`closest_short_bias_05em`, max_hold=-, flat_exit_prob=-, flat_exit_min_hold=-, return_pct=64.534, profit_factor=1.5249, max_dd_pct=20.1849, ulcer_index=6.0536, trades=229, ready_gap=35, unexpected_skips=0
- [5] `05DL_05cc_margin_hold5_0001`: variant=`lower_ulcer_alt_05dl`, max_hold=-, flat_exit_prob=-, flat_exit_min_hold=-, return_pct=58.852, profit_factor=1.4311, max_dd_pct=18.3944, ulcer_index=5.5864, trades=267, ready_gap=35, unexpected_skips=0

## Verdict

- status: `reject_keep_incumbent`
- selected_run_name: `05DP_05ca_margin0675_hold5_0001`
- reason: `no exit-side regime candidate cleared 05DP on holdout`

## Read

- read: `this batch asks whether plateau behavior improves when existing positions are cut early once the model flips into a high-flat regime, instead of waiting only for max_hold`
