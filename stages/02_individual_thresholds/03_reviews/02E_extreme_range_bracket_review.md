# 02E Extreme Range Bracket Review

Generated at: `2026-03-28T05:20:33.967172+00:00`

## Scope

- purpose: `use low and high threshold extremes to bracket the useful Stage 02 exploration range without freezing a threshold`
- low edge values: `0.25, 0.30, 0.35, 0.40`
- high edge values: `0.55, 0.60, 0.65, 0.70`
- regions: `low_low`, `high_high`, `high_low`, `low_high`

## Region Reads

- high_low best avg: `(Ts=0.55, Tl=0.40)`, valid_comp=`0.1254`, test_comp=`0.0720`, avg_comp=`0.0987`
- low_low best test: `(Ts=0.25, Tl=0.30)`, valid_comp=`-0.0981`, test_comp=`0.2262`, avg_comp=`0.0641`
- high_high best avg: `(Ts=0.70, Tl=0.55)`, valid_comp=`0.0414`, test_comp=`0.0024`, avg_comp=`0.0219`
- low_high best avg: `(Ts=0.40, Tl=0.55)`, valid_comp=`-0.1052`, test_comp=`0.0851`, avg_comp=`-0.0100`

## Region Counts

- `low_low`: total=`16`, both_positive=`0`
- `high_high`: total=`16`, both_positive=`5`
- `high_low`: total=`16`, both_positive=`5`
- `low_high`: total=`16`, both_positive=`0`

## Top High-Low Edge Reads

- `(Ts=0.55, Tl=0.40)`: valid_comp=0.1254, test_comp=0.0720, avg_comp=0.0987, gap=0.0534
- `(Ts=0.60, Tl=0.40)`: valid_comp=0.1342, test_comp=0.0554, avg_comp=0.0948, gap=0.0788
- `(Ts=0.70, Tl=0.40)`: valid_comp=0.1337, test_comp=0.0501, avg_comp=0.0919, gap=0.0836
- `(Ts=0.65, Tl=0.40)`: valid_comp=0.1231, test_comp=0.0496, avg_comp=0.0864, gap=0.0735
- `(Ts=0.55, Tl=0.35)`: valid_comp=0.1245, test_comp=0.0349, avg_comp=0.0797, gap=0.0895
- `(Ts=0.55, Tl=0.25)`: valid_comp=0.1491, test_comp=-0.0027, avg_comp=0.0732, gap=0.1518
- `(Ts=0.70, Tl=0.25)`: valid_comp=0.1408, test_comp=-0.0117, avg_comp=0.0646, gap=0.1525
- `(Ts=0.65, Tl=0.25)`: valid_comp=0.1329, test_comp=-0.0125, avg_comp=0.0602, gap=0.1455
- `(Ts=0.55, Tl=0.30)`: valid_comp=0.1178, test_comp=-0.0008, avg_comp=0.0585, gap=0.1187
- `(Ts=0.70, Tl=0.30)`: valid_comp=0.1415, test_comp=-0.0294, avg_comp=0.0561, gap=0.1709

## Top Low-Low Edge Reads

- `(Ts=0.35, Tl=0.40)`: valid_comp=-0.0879, test_comp=0.2212, avg_comp=0.0666, gap=0.3091
- `(Ts=0.25, Tl=0.30)`: valid_comp=-0.0981, test_comp=0.2262, avg_comp=0.0641, gap=0.3243
- `(Ts=0.40, Tl=0.40)`: valid_comp=-0.0303, test_comp=0.1541, avg_comp=0.0619, gap=0.1844
- `(Ts=0.35, Tl=0.30)`: valid_comp=-0.0682, test_comp=0.1822, avg_comp=0.0570, gap=0.2504
- `(Ts=0.30, Tl=0.25)`: valid_comp=-0.0706, test_comp=0.1677, avg_comp=0.0486, gap=0.2383
- `(Ts=0.35, Tl=0.35)`: valid_comp=-0.0997, test_comp=0.1675, avg_comp=0.0339, gap=0.2672
- `(Ts=0.30, Tl=0.40)`: valid_comp=-0.1018, test_comp=0.1691, avg_comp=0.0337, gap=0.2709
- `(Ts=0.25, Tl=0.25)`: valid_comp=-0.1397, test_comp=0.1894, avg_comp=0.0249, gap=0.3291

## Verdict

- verdict: `use the extremes only as a bracket, not as a selection shortcut`
- read: among the extreme edges, only the `high_short / low_long` band keeps producing clearly both-positive blended reads. The `low_low` edge can spike on test, but it is too negative on valid to treat as a stable bracket candidate.
- exploratory bracket suggestion: `short_threshold` roughly `0.55-0.70`, `long_threshold` roughly `0.35-0.40`.
