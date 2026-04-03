# 03D Margin Extreme Bracket Review

Generated at: `2026-03-28T07:00:35.066044+00:00`

## Scope

- purpose: `use low and high min_margin extremes to bracket the useful Stage 03 margin-only range without freezing a seed`
- fixed thresholds: `(short_threshold=0.333333, long_threshold=0.333333)`
- low edge values: `0.00, 0.01, 0.02, 0.03`
- high edge values: `0.07, 0.08, 0.09, 0.10`
- edges: `low_edge`, `high_edge`

## Edge Reads

- high-edge best avg: `(min_margin=0.07)`, valid_comp=`0.0385`, test_comp=`0.0985`, avg_comp=`0.0685`
- low-edge best test: `(min_margin=0.02)`, valid_comp=`-0.0809`, test_comp=`0.2494`, avg_comp=`0.0842`

## Edge Counts

- `low_edge`: total=`4`, both_positive=`0`
- `high_edge`: total=`4`, both_positive=`4`

## Top High-Edge Reads

- `min_margin=0.07`: valid_comp=0.0385, test_comp=0.0985, avg_comp=0.0685, gap=0.0600
- `min_margin=0.08`: valid_comp=0.0484, test_comp=0.0538, avg_comp=0.0511, gap=0.0055
- `min_margin=0.09`: valid_comp=0.0282, test_comp=0.0410, avg_comp=0.0346, gap=0.0128
- `min_margin=0.10`: valid_comp=0.0065, test_comp=0.0482, avg_comp=0.0273, gap=0.0417

## Top Low-Edge Reads

- `min_margin=0.02`: valid_comp=-0.0809, test_comp=0.2494, avg_comp=0.0842, gap=0.3304
- `min_margin=0.00`: valid_comp=-0.0874, test_comp=0.2064, avg_comp=0.0595, gap=0.2938
- `min_margin=0.03`: valid_comp=-0.0637, test_comp=0.1751, avg_comp=0.0557, gap=0.2388
- `min_margin=0.01`: valid_comp=-0.1525, test_comp=0.1862, avg_comp=0.0169, gap=0.3387

## Verdict

- verdict: `use the extremes only as a bracket, not as a selection shortcut`
- read: among the extreme edges, only the high-margin side keeps both valid and test positive. The low-margin edge can spike on test, but it stays negative on valid and does not look stable enough to treat as the main Stage 03 pocket.
- exploratory bracket suggestion: `min_margin` roughly `0.07-0.10`.
