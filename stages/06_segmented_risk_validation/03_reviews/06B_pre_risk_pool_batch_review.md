# 06B Pre-Risk Pool Batch Review

- generated_at_utc: `2026-03-31T22:17:50.184694+00:00`
- source_total: `131`
- completed_count: `126`
- failed_count: `5`

- best_holdout: `05ER` `05ER_05dp_short_bias_margin_hold4_0001` -> `06B_05ER_01`, return_pct `81.054`, PF `1.4202`
- best_validation: `05I` `05I_mt5_validation_margin_lightgbm_modelswap_0001` -> `06B_05I_01`, return_pct `1587758.124`, PF `10.2378`

## Top Holdout

- `05ER` `05ER_05dp_short_bias_margin_hold4_0001` -> `06B_05ER_01`: return_pct `81.054`, PF `1.4202`, trades `257`, max_dd_pct `22.7904`
- `05EM` `05EM_05dp_short_bias_margin_hold5_0001` -> `06B_05EM_01`: return_pct `78.956`, PF `1.4278`, trades `237`, max_dd_pct `24.6099`
- `05FX` `05FX_05dp_flatexit045_hold1_0001` -> `06B_05FX_01`: return_pct `71.956`, PF `1.3051`, trades `289`, max_dd_pct `30.2021`
- `05FY` `05FY_05dp_flatexit048_hold1_0001` -> `06B_05FY_01`: return_pct `71.956`, PF `1.3051`, trades `289`, max_dd_pct `30.2021`
- `05DP` `05DP_05ca_margin0675_hold5_0001` -> `06B_05DP_01`: return_pct `69.832`, PF `1.2971`, trades `289`, max_dd_pct `30.1748`
- `05FR` `05FR_05dp_flatexit052_hold1_0001` -> `06B_05FR_01`: return_pct `69.832`, PF `1.2971`, trades `289`, max_dd_pct `30.1748`
- `05FS` `05FS_05dp_flatexit055_hold1_0001` -> `06B_05FS_01`: return_pct `69.832`, PF `1.2971`, trades `289`, max_dd_pct `30.1748`
- `05FT` `05FT_05dp_flatexit055_hold2_0001` -> `06B_05FT_01`: return_pct `69.832`, PF `1.2971`, trades `289`, max_dd_pct `30.1748`
- `05FU` `05FU_05dp_flatexit058_hold1_0001` -> `06B_05FU_01`: return_pct `69.832`, PF `1.2971`, trades `289`, max_dd_pct `30.1748`
- `05FV` `05FV_05dp_flatexit060_hold2_0001` -> `06B_05FV_01`: return_pct `69.832`, PF `1.2971`, trades `289`, max_dd_pct `30.1748`

## Top Validation

- `05I` `05I_mt5_validation_margin_lightgbm_modelswap_0001` -> `06B_05I_01`: return_pct `1587758.124`, PF `10.2378`, trades `1573`, max_dd_pct `6.7114`
- `05K` `05K_mt5_validation_margin_xgboost_modelswap_0001` -> `06B_05K_01`: return_pct `425541.978`, PF `3.4612`, trades `1423`, max_dd_pct `6.8200`
- `05L` `05L_rf_margin_swap_0001` -> `06B_05L_01`: return_pct `105701.704`, PF `3.9106`, trades `854`, max_dd_pct `9.1459`
- `05M` `05M_et_margin_swap_0001` -> `06B_05M_01`: return_pct `6257.538`, PF `4.0364`, trades `453`, max_dd_pct `6.5865`
- `05DP` `05DP_05ca_margin0675_hold5_0001` -> `06B_05DP_01`: return_pct `249.090`, PF `1.3903`, trades `425`, max_dd_pct `24.2840`
- `05FR` `05FR_05dp_flatexit052_hold1_0001` -> `06B_05FR_01`: return_pct `249.090`, PF `1.3903`, trades `425`, max_dd_pct `24.2840`
- `05FS` `05FS_05dp_flatexit055_hold1_0001` -> `06B_05FS_01`: return_pct `249.090`, PF `1.3903`, trades `425`, max_dd_pct `24.2840`
- `05FT` `05FT_05dp_flatexit055_hold2_0001` -> `06B_05FT_01`: return_pct `249.090`, PF `1.3903`, trades `425`, max_dd_pct `24.2840`
- `05FU` `05FU_05dp_flatexit058_hold1_0001` -> `06B_05FU_01`: return_pct `249.090`, PF `1.3903`, trades `425`, max_dd_pct `24.2840`
- `05FV` `05FV_05dp_flatexit060_hold2_0001` -> `06B_05FV_01`: return_pct `249.090`, PF `1.3903`, trades `425`, max_dd_pct `24.2840`

## Failed Runs

- `05A` `05A_run_0001_margin_family_probe`: `FileNotFoundError: unsupported source layout: bundle=False config=False model=False rule_stack=False`
- `05B` `05B_run_0001_diff_family_probe`: `FileNotFoundError: unsupported source layout: bundle=False config=False model=False rule_stack=False`
- `05J` `05J_mt5_validation_margin_catboost_modelswap_0001`: `TypeError: float() argument must be a string or a real number, not 'dict'`
- `05FO` `05FO_cal_proxy_0001`: `ValueError: smoke test output mismatch against expected output; max_abs_diff=0.00933573`
- `05FP` `05FP_cal_ovr_proxy_0001`: `ValueError: smoke test output mismatch against expected output; max_abs_diff=0.04049981`
