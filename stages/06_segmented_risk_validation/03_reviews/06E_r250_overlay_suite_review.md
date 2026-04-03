# 06E R250 Session Overlay Suite Review

- source_run: `06C_R250`
- source_run_dir: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages\06_segmented_risk_validation\02_runs\active\06C_R250`
- reference_soft_decay: `06D_R250_SD01` holdout `return_pct=115.632`, `PF=1.4638`, `max_dd_pct=24.9935`

## Batch Summary

- best_holdout_run: `06E_R250_LP01` `local_probe_a`
- best_holdout_headline: `return_pct=117.018`, `PF=1.4658`, `max_dd_pct=24.5013`, `ulcer=12.7321`

## Runs

### 06E_R250_LP01 `local_probe_a`

- description: `Softer Monday, tighter post-cash decay.`
- holdout: `return_pct=117.018`, `PF=1.4658`, `trades=257`, `max_dd_pct=24.5013`, `ulcer=12.7321`
- vs 06C_R250: `return_pct_delta=9.980`, `PF_delta=0.0507`, `max_dd_pct_delta=-3.7502`, `ulcer_delta=-1.5877`
- overlay: `{"monday_risk_pct_mult": 0.8, "ny_postcash_risk_pct_mult": 0.65, "risk_pct": 2.5, "stop_atr_period": 14, "stop_execution_mode": "broker_native", "stop_long_atr_mult": 1.4, "stop_policy": "direction_split", "stop_short_atr_mult": 2.0}`

### 06E_R250_LP02 `local_probe_b`

- description: `Stronger Monday and post-cash decay.`
- holdout: `return_pct=116.910`, `PF=1.4729`, `trades=257`, `max_dd_pct=24.5097`, `ulcer=12.5464`
- vs 06C_R250: `return_pct_delta=9.872`, `PF_delta=0.0578`, `max_dd_pct_delta=-3.7418`, `ulcer_delta=-1.7734`
- overlay: `{"monday_risk_pct_mult": 0.7, "ny_postcash_risk_pct_mult": 0.65, "risk_pct": 2.5, "stop_atr_period": 14, "stop_execution_mode": "broker_native", "stop_long_atr_mult": 1.4, "stop_policy": "direction_split", "stop_short_atr_mult": 2.0}`

### 06E_R250_MD01 `monday_direction_split`

- description: `Decay Monday longs only while leaving Monday shorts intact.`
- holdout: `return_pct=104.538`, `PF=1.4205`, `trades=257`, `max_dd_pct=25.2147`, `ulcer=13.1278`
- vs 06C_R250: `return_pct_delta=-2.500`, `PF_delta=0.0054`, `max_dd_pct_delta=-3.0368`, `ulcer_delta=-1.1920`
- overlay: `{"monday_long_risk_pct_mult": 0.6, "monday_risk_pct_mult": 1.0, "monday_short_risk_pct_mult": 1.0, "ny_postcash_risk_pct_mult": 0.7, "risk_pct": 2.5, "stop_atr_period": 14, "stop_execution_mode": "broker_native", "stop_long_atr_mult": 1.4, "stop_policy": "direction_split", "stop_short_atr_mult": 2.0}`

### 06E_R250_PH01 `postcash_hold_cut`

- description: `Keep the 06D soft decay and shorten post-cash hold time.`
- holdout: `return_pct=98.146`, `PF=1.4017`, `trades=260`, `max_dd_pct=22.6136`, `ulcer=12.4791`
- vs 06C_R250: `return_pct_delta=-8.892`, `PF_delta=-0.0134`, `max_dd_pct_delta=-5.6379`, `ulcer_delta=-1.8407`
- overlay: `{"monday_risk_pct_mult": 0.75, "ny_postcash_hold_cap_bars": 3, "ny_postcash_risk_pct_mult": 0.7, "risk_pct": 2.5, "stop_atr_period": 14, "stop_execution_mode": "broker_native", "stop_long_atr_mult": 1.4, "stop_policy": "direction_split", "stop_short_atr_mult": 2.0}`

### 06E_R250_CT01 `clock_taper`

- description: `Use a gradual NY-local taper instead of one hard post-cash multiplier.`
- holdout: `return_pct=112.242`, `PF=1.4547`, `trades=257`, `max_dd_pct=25.0109`, `ulcer=12.6946`
- vs 06C_R250: `return_pct_delta=5.204`, `PF_delta=0.0396`, `max_dd_pct_delta=-3.2406`, `ulcer_delta=-1.6252`
- overlay: `{"monday_risk_pct_mult": 0.75, "ny_clock_taper_late_minute": 1080, "ny_clock_taper_late_mult": 0.6, "ny_clock_taper_mid_minute": 960, "ny_clock_taper_mid_mult": 0.75, "ny_clock_taper_start_minute": 930, "ny_clock_taper_start_mult": 0.9, "ny_postcash_risk_pct_mult": 1.0, "risk_pct": 2.5, "stop_atr_period": 14, "stop_execution_mode": "broker_native", "stop_long_atr_mult": 1.4, "stop_policy": "direction_split", "stop_short_atr_mult": 2.0}`

## Baseline

- 06C_R250 holdout: `return_pct=107.038`, `PF=1.4151`, `max_dd_pct=28.2515`

