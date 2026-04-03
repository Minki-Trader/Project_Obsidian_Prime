# 04A Probability-Diff Sweep Review

Generated at: `2026-03-28T07:12:37.755323+00:00`

## Scope

- purpose: `evaluate the directional probability-difference filter on its own with neutral default thresholds`
- fixed thresholds: `(short_threshold=0.333333, long_threshold=0.333333)`
- fixed max-probability margin: `0.00`
- source run: `01C_run_0001_h03_band000125_logreg`
- reserved final confirmation model: `01D_run_0001_final_h03_band000125_logreg`
- search split: `valid`
- diagnostic split: `test`
- execution assumptions: `3-bar time exit, no overlap, no flip, zero cost`
- difference definition: `selected direction probability must exceed opposing directional probability by at least min_probability_diff`

## Threshold-Only Default Reference

- threshold-only default `(1/3, 1/3)`: valid_comp=`-0.1270`, test_comp=`0.2312`, valid_trades=`2292`, test_trades=`1180`

## Difference Baseline

- baseline `min_probability_diff=0.00`: valid_comp=`-0.1270`, test_comp=`0.2312`, valid_trades=`2292`, test_trades=`1180`

## Selected Valid-Side Diff Seed

- selected `min_probability_diff=0.08`: valid_comp=`0.0709`, test_comp=`0.0447`, valid_trades=`989`, test_trades=`259`
- delta vs threshold-only default: valid_comp=`+0.1979`, test_comp=`-0.1864`

## Top Valid Reads

- `min_probability_diff=0.08`: valid_comp=0.0709, test_comp=0.0447, valid_trades=989, test_trades=259, valid_diff_rejects=3494, test_diff_rejects=2444
- `min_probability_diff=0.10`: valid_comp=0.0274, test_comp=0.0392, valid_trades=713, test_trades=161, valid_diff_rejects=4230, test_diff_rejects=2726
- `min_probability_diff=0.06`: valid_comp=0.0097, test_comp=0.1215, valid_trades=1363, test_trades=458, valid_diff_rejects=2478, test_diff_rejects=1912
- `min_probability_diff=0.16`: valid_comp=-0.0025, test_comp=0.0206, valid_trades=198, test_trades=33, valid_diff_rejects=5708, test_diff_rejects=3103
- `min_probability_diff=0.14`: valid_comp=-0.0079, test_comp=0.0196, valid_trades=315, test_trades=56, valid_diff_rejects=5366, test_diff_rejects=3034
- `min_probability_diff=0.20`: valid_comp=-0.0209, test_comp=0.0154, valid_trades=110, test_trades=16, valid_diff_rejects=5971, test_diff_rejects=3154
- `min_probability_diff=0.18`: valid_comp=-0.0331, test_comp=0.0092, valid_trades=143, test_trades=25, valid_diff_rejects=5872, test_diff_rejects=3127
- `min_probability_diff=0.12`: valid_comp=-0.0411, test_comp=0.0447, valid_trades=485, test_trades=93, valid_diff_rejects=4876, test_diff_rejects=2923
- `min_probability_diff=0.04`: valid_comp=-0.0567, test_comp=0.1577, valid_trades=1741, test_trades=714, valid_diff_rejects=1476, test_diff_rejects=1241
- `min_probability_diff=0.02`: valid_comp=-0.0996, test_comp=0.2581, valid_trades=2082, test_trades=1006, valid_diff_rejects=562, test_diff_rejects=469

## Strongest Test Read

- `min_probability_diff=0.02`: valid_comp=`-0.0996`, test_comp=`0.2581`, valid_trades=`2082`, test_trades=`1006`

## Verdict

- verdict: `Stage 04 is now pure probability-difference mode; do not mix this with threshold asymmetry or max-probability margin yet`
- read: this phase shows what the directional probability-difference filter alone does relative to the neutral default threshold logic, so later synthesis can compare rule families one by one.
