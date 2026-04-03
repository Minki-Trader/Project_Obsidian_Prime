# 05FM Stage 05 05DP Output Shape Review

Generated at: `2026-03-30T16:27:27.644960+00:00`

## Scope

- purpose: `keep the 05CA feature/model lineage fixed and explore calibration-aware probability reshaping on top of the 05DP logic surface`
- promoted incumbent: `05DP`
- idea: `test whether temperature, class-bias, or class-specific logit scaling can improve plateau behavior without changing the feature stack or rule family`

## MT5 Validation Ranking

- [1] `05FB_05ca_temp090_margin0675_hold5_0001`: variant=`temp_sharp_090`, temp=0.900, scales=[1.000, 1.000, 1.000], biases=[0.000, 0.000, 0.000], return_pct=124.448, profit_factor=1.4869, max_dd_pct=13.3627, ulcer_index=6.7073, trades=475, ready_gap=0, unexpected_skips=0, offline_macro_f1=0.4573, offline_bal_acc=0.4685, offline_log_loss=0.9686, pred_share=`short=0.253, flat=0.563, long=0.183`
- [2] `05DP_05ca_margin0675_hold5_0001`: variant=`promoted_05dp`, temp=n/a, scales=-, biases=-, return_pct=122.570, profit_factor=1.5553, max_dd_pct=12.6031, ulcer_index=7.2871, trades=405, ready_gap=0, unexpected_skips=0, offline_macro_f1=n/a, offline_bal_acc=n/a, offline_log_loss=n/a, pred_share=`-`
- [3] `05EM_05dp_short_bias_margin_hold5_0001`: variant=`closest_short_bias_05em`, temp=n/a, scales=-, biases=-, return_pct=109.204, profit_factor=1.5289, max_dd_pct=13.0566, ulcer_index=7.9882, trades=356, ready_gap=0, unexpected_skips=0, offline_macro_f1=n/a, offline_bal_acc=n/a, offline_log_loss=n/a, pred_share=`-`
- [4] `05DL_05cc_margin_hold5_0001`: variant=`lower_ulcer_alt_05dl`, temp=n/a, scales=-, biases=-, return_pct=99.682, profit_factor=1.4448, max_dd_pct=14.9161, ulcer_index=7.6350, trades=393, ready_gap=0, unexpected_skips=0, offline_macro_f1=n/a, offline_bal_acc=n/a, offline_log_loss=n/a, pred_share=`-`
- [5] `05FA_05ca_temp115_margin0675_hold5_0001`: variant=`temp_soft_115`, temp=1.150, scales=[1.000, 1.000, 1.000], biases=[0.000, 0.000, 0.000], return_pct=92.762, profit_factor=1.4722, max_dd_pct=12.4660, ulcer_index=5.7619, trades=338, ready_gap=0, unexpected_skips=0, offline_macro_f1=0.4573, offline_bal_acc=0.4685, offline_log_loss=0.9821, pred_share=`short=0.253, flat=0.563, long=0.183`
- [6] `05FE_05ca_cls_scale_0001`: variant=`short_scale_up_long_scale_down`, temp=1.000, scales=[1.080, 1.000, 0.920], biases=[0.000, 0.000, 0.000], return_pct=65.192, profit_factor=1.2422, max_dd_pct=16.6429, ulcer_index=7.3142, trades=440, ready_gap=0, unexpected_skips=0, offline_macro_f1=0.4526, offline_bal_acc=0.4690, offline_log_loss=0.9745, pred_share=`short=0.291, flat=0.564, long=0.145`
- [7] `05FD_05ca_flatup_longdown_margin0675_hold5_0001`: variant=`flat_up_long_down_bias`, temp=1.000, scales=[1.000, 1.000, 1.000], biases=[0.000, 0.100, -0.100], return_pct=64.770, profit_factor=1.2216, max_dd_pct=22.9428, ulcer_index=12.9802, trades=511, ready_gap=0, unexpected_skips=0, offline_macro_f1=0.4237, offline_bal_acc=0.4523, offline_log_loss=0.9371, pred_share=`short=0.320, flat=0.625, long=0.055`
- [8] `05FF_05ca_temp_shortbias_0001`: variant=`soft_temp_short_bias_combo`, temp=1.100, scales=[1.000, 1.000, 1.000], biases=[0.080, 0.000, -0.080], return_pct=62.432, profit_factor=1.1539, max_dd_pct=29.9352, ulcer_index=16.9408, trades=722, ready_gap=0, unexpected_skips=0, offline_macro_f1=0.3929, offline_bal_acc=0.4536, offline_log_loss=0.9816, pred_share=`short=0.431, flat=0.545, long=0.024`
- [9] `05FC_05ca_shortup_longdown_margin0675_hold5_0001`: variant=`short_up_long_down_bias`, temp=1.000, scales=[1.000, 1.000, 1.000], biases=[0.100, 0.000, -0.100], return_pct=49.110, profit_factor=1.1025, max_dd_pct=31.0364, ulcer_index=18.3173, trades=840, ready_gap=0, unexpected_skips=0, offline_macro_f1=0.3873, offline_bal_acc=0.4533, offline_log_loss=0.9773, pred_share=`short=0.443, flat=0.540, long=0.017`

## MT5 Holdout Ranking

- [1] `05DP_05ca_margin0675_hold5_0001`: variant=`promoted_05dp`, temp=n/a, scales=-, biases=-, return_pct=68.574, profit_factor=1.4925, max_dd_pct=19.3936, ulcer_index=5.8587, trades=275, ready_gap=35, unexpected_skips=0
- [2] `05EM_05dp_short_bias_margin_hold5_0001`: variant=`closest_short_bias_05em`, temp=n/a, scales=-, biases=-, return_pct=64.534, profit_factor=1.5249, max_dd_pct=20.1849, ulcer_index=6.0536, trades=229, ready_gap=35, unexpected_skips=0
- [3] `05DL_05cc_margin_hold5_0001`: variant=`lower_ulcer_alt_05dl`, temp=n/a, scales=-, biases=-, return_pct=58.852, profit_factor=1.4311, max_dd_pct=18.3944, ulcer_index=5.5864, trades=267, ready_gap=35, unexpected_skips=0
- [4] `05FB_05ca_temp090_margin0675_hold5_0001`: variant=`temp_sharp_090`, temp=0.900, scales=[1.000, 1.000, 1.000], biases=[0.000, 0.000, 0.000], return_pct=56.260, profit_factor=1.3313, max_dd_pct=17.9401, ulcer_index=6.0985, trades=317, ready_gap=35, unexpected_skips=0
- [5] `05FA_05ca_temp115_margin0675_hold5_0001`: variant=`temp_soft_115`, temp=1.150, scales=[1.000, 1.000, 1.000], biases=[0.000, 0.000, 0.000], return_pct=45.618, profit_factor=1.4165, max_dd_pct=17.0108, ulcer_index=5.6055, trades=209, ready_gap=35, unexpected_skips=0

## Verdict

- status: `reject_keep_incumbent`
- selected_run_name: `05DP_05ca_margin0675_hold5_0001`
- reason: `no output-shape candidate cleared 05DP on holdout`

## Read

- read: `this batch separates output-shape effects from feature or rule changes, so any win here means the 05CA edge was partly trapped in probability geometry rather than the raw feature stack`
