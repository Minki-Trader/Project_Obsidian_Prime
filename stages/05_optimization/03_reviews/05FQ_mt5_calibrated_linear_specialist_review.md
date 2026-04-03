# 05FQ Stage 05 Calibrated Linear Specialist Review

Generated at: `2026-03-31T13:51:42.535877+00:00`

## Scope

- purpose: `retrain export-safe linear specialists on the 05CA feature line instead of applying post-hoc probability edits`
- feature line: `trend_proxy_persistence + trend_proxy_risk_off_confirmation over the no_trend_strength base`
- promoted incumbent: `05DP`

## MT5 Validation Ranking

- [1] `05DP_05ca_margin0675_hold5_0001`: variant=`promoted_05dp`, family=`-`, return_pct=122.570, profit_factor=1.5553, max_dd_pct=12.6031, ulcer_index=7.2871, trades=405, ready_gap=0, unexpected_skips=0
- [2] `05EM_05dp_short_bias_margin_hold5_0001`: variant=`closest_short_bias_05em`, family=`-`, return_pct=109.204, profit_factor=1.5289, max_dd_pct=13.0566, ulcer_index=7.9882, trades=356, ready_gap=0, unexpected_skips=0
- [3] `05DL_05cc_margin_hold5_0001`: variant=`lower_ulcer_alt_05dl`, family=`-`, return_pct=99.682, profit_factor=1.4448, max_dd_pct=14.9161, ulcer_index=7.6350, trades=393, ready_gap=0, unexpected_skips=0
- [4] `05FN_ovr_proxy_0001`: variant=`ovr_trend_proxy_logreg`, family=`ovr_trend_proxy_logreg`, return_pct=8.864, profit_factor=1.2003, max_dd_pct=9.7208, ulcer_index=3.4895, trades=70, ready_gap=0, unexpected_skips=0

## Export / Smoke Failures

- `05FO_cal_proxy_0001`: variant=`calibrated_trend_proxy_sigmoid`, family=`calibrated_trend_proxy_sigmoid`, status=`failed`, returncode=`1`

```text
                            ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\foundation\pipelines\build_experiment_bundle.py", line 336, in assemble_bundle
    smoke_summary = run_smoke_test(
        request,
    ...<2 lines>...
        feature_schema=feature_schema,
    )
  File "C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\foundation\pipelines\build_experiment_bundle.py", line 276, in run_smoke_test
    raise ValueError(
    ...<2 lines>...
    )
ValueError: smoke test output mismatch against expected output; max_abs_diff=0.00933573
```
- `05FP_cal_ovr_proxy_0001`: variant=`calibrated_ovr_trend_proxy_sigmoid`, family=`calibrated_ovr_trend_proxy_sigmoid`, status=`failed`, returncode=`1`

```text
                            ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\foundation\pipelines\build_experiment_bundle.py", line 336, in assemble_bundle
    smoke_summary = run_smoke_test(
        request,
    ...<2 lines>...
        feature_schema=feature_schema,
    )
  File "C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\foundation\pipelines\build_experiment_bundle.py", line 276, in run_smoke_test
    raise ValueError(
    ...<2 lines>...
    )
ValueError: smoke test output mismatch against expected output; max_abs_diff=0.04049981
```

## MT5 Holdout Ranking

- [1] `05DP_05ca_margin0675_hold5_0001`: variant=`promoted_05dp`, family=`-`, return_pct=68.574, profit_factor=1.4925, max_dd_pct=19.3936, ulcer_index=5.8587, trades=275, ready_gap=35, unexpected_skips=0
- [2] `05EM_05dp_short_bias_margin_hold5_0001`: variant=`closest_short_bias_05em`, family=`-`, return_pct=64.534, profit_factor=1.5249, max_dd_pct=20.1849, ulcer_index=6.0536, trades=229, ready_gap=35, unexpected_skips=0
- [3] `05DL_05cc_margin_hold5_0001`: variant=`lower_ulcer_alt_05dl`, family=`-`, return_pct=58.852, profit_factor=1.4311, max_dd_pct=18.3944, ulcer_index=5.5864, trades=267, ready_gap=35, unexpected_skips=0
- [4] `05FN_ovr_proxy_0001`: variant=`ovr_trend_proxy_logreg`, family=`ovr_trend_proxy_logreg`, return_pct=24.552, profit_factor=1.6891, max_dd_pct=13.9206, ulcer_index=5.2559, trades=61, ready_gap=35, unexpected_skips=0

## Verdict

- status: `reject_keep_incumbent`
- selected_run_name: `05DP_05ca_margin0675_hold5_0001`
- reason: `no calibration-aware linear specialist cleared 05DP on holdout`

## Read

- read: `this batch asks whether the 05CA edge needs retrained linear specialization and calibration, rather than post-hoc output surgery`
