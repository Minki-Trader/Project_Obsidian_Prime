# 03A Margin-Only Sweep Review

Generated at: `2026-03-28T06:44:38.376413+00:00`

## Scope

- purpose: `evaluate max_probability_margin on its own with neutral default thresholds`
- fixed thresholds: `(short_threshold=0.333333, long_threshold=0.333333)`
- source run: `01C_run_0001_h03_band000125_logreg`
- reserved final confirmation model: `01D_run_0001_final_h03_band000125_logreg`
- search split: `valid`
- diagnostic split: `test`
- execution assumptions: `3-bar time exit, no overlap, no flip, zero cost`
- margin definition: `selected direction probability must exceed max(p_flat, opposing side probability) by at least min_margin`

## Threshold-Only Default Reference

- threshold-only default `(1/3, 1/3)`: valid_comp=`-0.1270`, test_comp=`0.2312`, valid_trades=`2292`, test_trades=`1180`

## Margin Baseline

- baseline `min_margin=0.00`: valid_comp=`-0.0874`, test_comp=`0.2064`, valid_trades=`2056`, test_trades=`1083`

## Selected Valid-Side Margin Seed

- selected `min_margin=0.08`: valid_comp=`0.0484`, test_comp=`0.0538`, valid_trades=`788`, test_trades=`232`
- delta vs threshold-only default: valid_comp=`+0.1753`, test_comp=`-0.1773`

## Top Valid Reads

- `min_margin=0.08`: valid_comp=0.0484, test_comp=0.0538, valid_trades=788, test_trades=232, valid_margin_rejects=3945, test_margin_rejects=2514
- `min_margin=0.07`: valid_comp=0.0385, test_comp=0.0985, valid_trades=940, test_trades=304, valid_margin_rejects=3499, test_margin_rejects=2303
- `min_margin=0.09`: valid_comp=0.0282, test_comp=0.0410, valid_trades=676, test_trades=183, valid_margin_rejects=4278, test_margin_rejects=2658
- `min_margin=0.10`: valid_comp=0.0065, test_comp=0.0482, valid_trades=596, test_trades=151, valid_margin_rejects=4517, test_margin_rejects=2753
- `min_margin=0.06`: valid_comp=-0.0122, test_comp=0.1414, valid_trades=1089, test_trades=370, valid_margin_rejects=3073, test_margin_rejects=2114
- `min_margin=0.03`: valid_comp=-0.0637, test_comp=0.1751, valid_trades=1593, test_trades=716, valid_margin_rejects=1633, test_margin_rejects=1147
- `min_margin=0.05`: valid_comp=-0.0672, test_comp=0.1867, valid_trades=1229, test_trades=470, valid_margin_rejects=2664, test_margin_rejects=1821
- `min_margin=0.02`: valid_comp=-0.0809, test_comp=0.2494, valid_trades=1743, test_trades=868, valid_margin_rejects=1220, test_margin_rejects=714
- `min_margin=0.04`: valid_comp=-0.0845, test_comp=0.1618, valid_trades=1409, test_trades=584, valid_margin_rejects=2164, test_margin_rejects=1508
- `min_margin=0.00`: valid_comp=-0.0874, test_comp=0.2064, valid_trades=2056, test_trades=1083, valid_margin_rejects=432, test_margin_rejects=167

## Strongest Test Read

- `min_margin=0.02`: valid_comp=`-0.0809`, test_comp=`0.2494`, valid_trades=`1743`, test_trades=`868`

## Verdict

- verdict: `Stage 03 is now pure margin-only; do not mix this with threshold asymmetry yet`
- read: this phase shows what max_probability_margin alone does relative to the neutral default threshold logic, so later synthesis can compare rule families one by one.
