# 02F Narrow Ridge Probe Review

Generated at: `2026-03-28T05:28:07.087270+00:00`

## Scope

- purpose: `scratch the current high-short / low-long bracket one more time without widening the search`
- short thresholds: `0.540, 0.545, 0.550, 0.555, 0.560, 0.565, 0.570, 0.575, 0.580, 0.585, 0.590, 0.595, 0.600`
- long thresholds: `0.380, 0.385, 0.390, 0.395, 0.400`
- this is still exploration only; no threshold freeze is made here

## Headline Read

- best both-positive blended pair: `(Ts=0.540, Tl=0.400)`
- valid compounded return: `0.1532`
- test compounded return: `0.0742`
- average compounded return: `0.1137`
- abs valid/test gap: `0.0790`

## Edge Reads

- top valid pair in the narrow ridge: `(Ts=0.540, Tl=0.400)`, valid_comp=`0.1532`, test_comp=`0.0742`
- top test pair in the narrow ridge: `(Ts=0.550, Tl=0.395)`, valid_comp=`0.0582`, test_comp=`0.0798`

## Top Stable Reads

- `(Ts=0.540, Tl=0.400)`: valid_comp=0.1532, test_comp=0.0742, avg_comp=0.1137, gap=0.0790
- `(Ts=0.585, Tl=0.400)`: valid_comp=0.1368, test_comp=0.0698, avg_comp=0.1033, gap=0.0670
- `(Ts=0.575, Tl=0.400)`: valid_comp=0.1345, test_comp=0.0698, avg_comp=0.1021, gap=0.0647
- `(Ts=0.595, Tl=0.400)`: valid_comp=0.1358, test_comp=0.0680, avg_comp=0.1019, gap=0.0677
- `(Ts=0.580, Tl=0.400)`: valid_comp=0.1311, test_comp=0.0698, avg_comp=0.1004, gap=0.0613
- `(Ts=0.550, Tl=0.400)`: valid_comp=0.1254, test_comp=0.0720, avg_comp=0.0987, gap=0.0534
- `(Ts=0.590, Tl=0.400)`: valid_comp=0.1358, test_comp=0.0611, avg_comp=0.0984, gap=0.0747
- `(Ts=0.545, Tl=0.400)`: valid_comp=0.1282, test_comp=0.0673, avg_comp=0.0977, gap=0.0608
- `(Ts=0.600, Tl=0.400)`: valid_comp=0.1342, test_comp=0.0554, avg_comp=0.0948, gap=0.0788
- `(Ts=0.540, Tl=0.390)`: valid_comp=0.0966, test_comp=0.0636, avg_comp=0.0801, gap=0.0330
- `(Ts=0.570, Tl=0.400)`: valid_comp=0.0884, test_comp=0.0698, avg_comp=0.0791, gap=0.0186
- `(Ts=0.555, Tl=0.400)`: valid_comp=0.0784, test_comp=0.0727, avg_comp=0.0756, gap=0.0057

## Verdict

- verdict: `keep exploring only in tiny increments; do not widen or freeze`
- read: inside the current bracket, the blended ridge still sits near the lower end of the short threshold range and at the upper edge of the long-threshold range. That means the useful pocket looks narrower than the full `0.55-0.70 / 0.35-0.40` bracket.
