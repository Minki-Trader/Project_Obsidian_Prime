# 06A Stage 06 Direction-Split Risk Overlay Review

Generated at: `2026-03-31T16:19:53.916727+00:00`

## Scope

- run: `06A_dirsplit2pct_0001`
- source_run_dir: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages\05_optimization\02_runs\active\05DP_05ca_margin0675_hold5_0001`
- overlay: `risk_pct=2.00, broker_native SL, direction_split(long=1.40, short=2.00), ATR14`

## Split Headline

- `validation`: return_pct `249.090`, PF `1.3903`, trades `425`, max_dd_pct `24.2840`, ulcer `10.1786`
- `test`: return_pct `69.832`, PF `1.2971`, trades `289`, max_dd_pct `30.1748`, ulcer `14.6302`

## Segments

### validation

- `validation_q1`: return_pct `99.450`, PF `1.7221`, trades `199`, max_dd_pct `10.5186`, ulcer `5.2450`
- `validation_q2`: return_pct `157.428`, PF `1.4891`, trades `166`, max_dd_pct `24.1479`, ulcer `13.6030`
- `validation_q3`: return_pct `-7.788`, PF `0.9564`, trades `60`, max_dd_pct `12.4972`, ulcer `6.7756`

### test

- `holdout_a`: return_pct `10.074`, PF `1.1819`, trades `83`, max_dd_pct `20.6430`, ulcer `12.9480`
- `holdout_b`: return_pct `-13.564`, PF `0.8367`, trades `93`, max_dd_pct `27.6329`, ulcer `16.3344`
- `holdout_c`: return_pct `73.322`, PF `1.7590`, trades `113`, max_dd_pct `8.7569`, ulcer `3.5883`

## Cross-Segment Summary

- best_segment: `validation::validation_q2`, return_pct `157.428`, PF `1.4891`
- worst_segment: `test::holdout_b`, return_pct `-13.564`, PF `0.8367`

