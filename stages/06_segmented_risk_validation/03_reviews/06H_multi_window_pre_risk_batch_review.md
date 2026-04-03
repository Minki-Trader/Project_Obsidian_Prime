# 06H Multi-Window Pre-Risk Batch Review

- generated_at_utc: `2026-04-03T03:24:22.142302+00:00`
- run_total: `786`
- completed_count: `756`
- failed_count: `30`

## Window Leaders

- `2310`: `05I` -> `06H_2310_05I_01`, return_pct `415423.902`, PF `6.6733`, max_dd_pct `5.2223`
- `2401`: `05I` -> `06H_2401_05I_01`, return_pct `448684.786`, PF `8.0692`, max_dd_pct `10.1585`
- `2404`: `05I` -> `06H_2404_05I_01`, return_pct `1073858.524`, PF `9.3459`, max_dd_pct `6.7114`
- `2407`: `05I` -> `06H_2407_05I_01`, return_pct `429728.016`, PF `14.5028`, max_dd_pct `6.4569`
- `2410`: `05I` -> `06H_2410_05I_01`, return_pct `5896.646`, PF `1.3989`, max_dd_pct `28.6670`
- `2501`: `05ER` -> `06H_2501_05ER_01`, return_pct `81.054`, PF `1.4202`, max_dd_pct `22.7904`

## Top Holdout Overall

- `2404` `05I` `05I_mt5_validation_margin_lightgbm_modelswap_0001` -> `06H_2404_05I_01`: return_pct `1073858.524`, PF `9.3459`, trades `1235`, max_dd_pct `6.7114`
- `2401` `05I` `05I_mt5_validation_margin_lightgbm_modelswap_0001` -> `06H_2401_05I_01`: return_pct `448684.786`, PF `8.0692`, trades `793`, max_dd_pct `10.1585`
- `2407` `05I` `05I_mt5_validation_margin_lightgbm_modelswap_0001` -> `06H_2407_05I_01`: return_pct `429728.016`, PF `14.5028`, trades `812`, max_dd_pct `6.4569`
- `2310` `05I` `05I_mt5_validation_margin_lightgbm_modelswap_0001` -> `06H_2310_05I_01`: return_pct `415423.902`, PF `6.6733`, trades `927`, max_dd_pct `5.2223`
- `2404` `05K` `05K_mt5_validation_margin_xgboost_modelswap_0001` -> `06H_2404_05K_01`: return_pct `175282.406`, PF `3.3102`, trades `1146`, max_dd_pct `6.8200`
- `2407` `05K` `05K_mt5_validation_margin_xgboost_modelswap_0001` -> `06H_2407_05K_01`: return_pct `36772.258`, PF `4.0908`, trades `714`, max_dd_pct `5.2165`
- `2310` `05K` `05K_mt5_validation_margin_xgboost_modelswap_0001` -> `06H_2310_05K_01`: return_pct `21217.990`, PF `2.9045`, trades `823`, max_dd_pct `11.7204`
- `2401` `05K` `05K_mt5_validation_margin_xgboost_modelswap_0001` -> `06H_2401_05K_01`: return_pct `19142.550`, PF `3.8271`, trades `705`, max_dd_pct `6.5861`
- `2404` `05L` `05L_rf_margin_swap_0001` -> `06H_2404_05L_01`: return_pct `18233.800`, PF `7.1685`, trades `608`, max_dd_pct `6.1746`
- `2410` `05I` `05I_mt5_validation_margin_lightgbm_modelswap_0001` -> `06H_2410_05I_01`: return_pct `5896.646`, PF `1.3989`, trades `582`, max_dd_pct `28.6670`
- `2407` `05L` `05L_rf_margin_swap_0001` -> `06H_2407_05L_01`: return_pct `4523.818`, PF `3.8772`, trades `456`, max_dd_pct `9.1417`
- `2401` `05L` `05L_rf_margin_swap_0001` -> `06H_2401_05L_01`: return_pct `4272.812`, PF `6.2850`, trades `452`, max_dd_pct `5.7195`
- `2310` `05L` `05L_rf_margin_swap_0001` -> `06H_2310_05L_01`: return_pct `3542.308`, PF `3.9775`, trades `446`, max_dd_pct `6.8873`
- `2404` `05M` `05M_et_margin_swap_0001` -> `06H_2404_05M_01`: return_pct `2377.668`, PF `9.4411`, trades `355`, max_dd_pct `4.5833`
- `2410` `05K` `05K_mt5_validation_margin_xgboost_modelswap_0001` -> `06H_2410_05K_01`: return_pct `984.146`, PF `1.4422`, trades `543`, max_dd_pct `24.9752`
- `2407` `05M` `05M_et_margin_swap_0001` -> `06H_2407_05M_01`: return_pct `936.726`, PF `6.5162`, trades `237`, max_dd_pct `5.6097`
- `2401` `05M` `05M_et_margin_swap_0001` -> `06H_2401_05M_01`: return_pct `538.932`, PF `4.7905`, trades `208`, max_dd_pct `5.5196`
- `2310` `05M` `05M_et_margin_swap_0001` -> `06H_2310_05M_01`: return_pct `480.678`, PF `3.4981`, trades `253`, max_dd_pct `5.6368`
- `2410` `05L` `05L_rf_margin_swap_0001` -> `06H_2410_05L_01`: return_pct `347.472`, PF `1.7071`, trades `379`, max_dd_pct `9.4386`
- `2404` `05DP` `05DP_05ca_margin0675_hold5_0001` -> `06H_2404_05DP_01`: return_pct `222.332`, PF `1.5339`, trades `349`, max_dd_pct `20.4665`

## Failed Runs

- `2310` `05A` `05A_run_0001_margin_family_probe`: `FileNotFoundError: unsupported source layout: bundle=False config=False model=False rule_stack=False`
- `2310` `05B` `05B_run_0001_diff_family_probe`: `FileNotFoundError: unsupported source layout: bundle=False config=False model=False rule_stack=False`
- `2310` `05J` `05J_mt5_validation_margin_catboost_modelswap_0001`: `TypeError: float() argument must be a string or a real number, not 'dict'`
- `2310` `05FO` `05FO_cal_proxy_0001`: `ValueError: smoke test output mismatch against expected output; max_abs_diff=0.00933573`
- `2310` `05FP` `05FP_cal_ovr_proxy_0001`: `ValueError: smoke test output mismatch against expected output; max_abs_diff=0.04049981`
- `2401` `05A` `05A_run_0001_margin_family_probe`: `FileNotFoundError: unsupported source layout: bundle=False config=False model=False rule_stack=False`
- `2401` `05B` `05B_run_0001_diff_family_probe`: `FileNotFoundError: unsupported source layout: bundle=False config=False model=False rule_stack=False`
- `2401` `05J` `05J_mt5_validation_margin_catboost_modelswap_0001`: `TypeError: float() argument must be a string or a real number, not 'dict'`
- `2401` `05FO` `05FO_cal_proxy_0001`: `ValueError: smoke test output mismatch against expected output; max_abs_diff=0.00933573`
- `2401` `05FP` `05FP_cal_ovr_proxy_0001`: `ValueError: smoke test output mismatch against expected output; max_abs_diff=0.04049981`
- `2404` `05A` `05A_run_0001_margin_family_probe`: `FileNotFoundError: unsupported source layout: bundle=False config=False model=False rule_stack=False`
- `2404` `05B` `05B_run_0001_diff_family_probe`: `FileNotFoundError: unsupported source layout: bundle=False config=False model=False rule_stack=False`
- `2404` `05J` `05J_mt5_validation_margin_catboost_modelswap_0001`: `TypeError: float() argument must be a string or a real number, not 'dict'`
- `2404` `05FO` `05FO_cal_proxy_0001`: `ValueError: smoke test output mismatch against expected output; max_abs_diff=0.00933573`
- `2404` `05FP` `05FP_cal_ovr_proxy_0001`: `ValueError: smoke test output mismatch against expected output; max_abs_diff=0.04049981`
- `2407` `05A` `05A_run_0001_margin_family_probe`: `FileNotFoundError: unsupported source layout: bundle=False config=False model=False rule_stack=False`
- `2407` `05B` `05B_run_0001_diff_family_probe`: `FileNotFoundError: unsupported source layout: bundle=False config=False model=False rule_stack=False`
- `2407` `05J` `05J_mt5_validation_margin_catboost_modelswap_0001`: `TypeError: float() argument must be a string or a real number, not 'dict'`
- `2407` `05FO` `05FO_cal_proxy_0001`: `ValueError: smoke test output mismatch against expected output; max_abs_diff=0.00933573`
- `2407` `05FP` `05FP_cal_ovr_proxy_0001`: `ValueError: smoke test output mismatch against expected output; max_abs_diff=0.04049981`
- `2410` `05A` `05A_run_0001_margin_family_probe`: `FileNotFoundError: unsupported source layout: bundle=False config=False model=False rule_stack=False`
- `2410` `05B` `05B_run_0001_diff_family_probe`: `FileNotFoundError: unsupported source layout: bundle=False config=False model=False rule_stack=False`
- `2410` `05J` `05J_mt5_validation_margin_catboost_modelswap_0001`: `TypeError: float() argument must be a string or a real number, not 'dict'`
- `2410` `05FO` `05FO_cal_proxy_0001`: `ValueError: smoke test output mismatch against expected output; max_abs_diff=0.00933573`
- `2410` `05FP` `05FP_cal_ovr_proxy_0001`: `ValueError: smoke test output mismatch against expected output; max_abs_diff=0.04049981`
- `2501` `05A` `05A_run_0001_margin_family_probe`: `FileNotFoundError: unsupported source layout: bundle=False config=False model=False rule_stack=False`
- `2501` `05B` `05B_run_0001_diff_family_probe`: `FileNotFoundError: unsupported source layout: bundle=False config=False model=False rule_stack=False`
- `2501` `05J` `05J_mt5_validation_margin_catboost_modelswap_0001`: `TypeError: float() argument must be a string or a real number, not 'dict'`
- `2501` `05FO` `05FO_cal_proxy_0001`: `ValueError: smoke test output mismatch against expected output; max_abs_diff=0.00933573`
- `2501` `05FP` `05FP_cal_ovr_proxy_0001`: `ValueError: smoke test output mismatch against expected output; max_abs_diff=0.04049981`
