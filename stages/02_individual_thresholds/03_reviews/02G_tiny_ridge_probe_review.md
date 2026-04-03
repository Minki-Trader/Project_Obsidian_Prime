# 02G Tiny Ridge Probe Review

Generated at: `2026-03-28T05:57:28.953112+00:00`

## Scope

- purpose: `probe only the tiny pocket suggested by 02F without widening the search`
- short thresholds: `0.5350, 0.5375, 0.5400, 0.5425, 0.5450, 0.5475, 0.5500`
- long thresholds: `0.395, 0.396, 0.397, 0.398, 0.399, 0.400`
- this is still exploration only; no threshold freeze is made here

## Headline Read

- best both-positive blended pair: `(Ts=0.5350, Tl=0.400)`
- valid compounded return: `0.1688`
- test compounded return: `0.0714`
- average compounded return: `0.1201`
- abs valid/test gap: `0.0974`

## Top Stable Reads

- `(Ts=0.5350, Tl=0.400)`: valid_comp=0.1688, test_comp=0.0714, avg_comp=0.1201, gap=0.0974
- `(Ts=0.5400, Tl=0.400)`: valid_comp=0.1532, test_comp=0.0742, avg_comp=0.1137, gap=0.0790
- `(Ts=0.5375, Tl=0.400)`: valid_comp=0.1509, test_comp=0.0710, avg_comp=0.1109, gap=0.0800
- `(Ts=0.5425, Tl=0.400)`: valid_comp=0.1449, test_comp=0.0717, avg_comp=0.1083, gap=0.0732
- `(Ts=0.5350, Tl=0.399)`: valid_comp=0.1365, test_comp=0.0741, avg_comp=0.1053, gap=0.0624
- `(Ts=0.5400, Tl=0.399)`: valid_comp=0.1214, test_comp=0.0773, avg_comp=0.0993, gap=0.0441
- `(Ts=0.5500, Tl=0.400)`: valid_comp=0.1254, test_comp=0.0720, avg_comp=0.0987, gap=0.0534
- `(Ts=0.5450, Tl=0.400)`: valid_comp=0.1282, test_comp=0.0673, avg_comp=0.0977, gap=0.0608
- `(Ts=0.5375, Tl=0.399)`: valid_comp=0.1191, test_comp=0.0740, avg_comp=0.0966, gap=0.0451
- `(Ts=0.5425, Tl=0.399)`: valid_comp=0.1132, test_comp=0.0747, avg_comp=0.0940, gap=0.0385
- `(Ts=0.5475, Tl=0.400)`: valid_comp=0.1137, test_comp=0.0691, avg_comp=0.0914, gap=0.0446
- `(Ts=0.5350, Tl=0.398)`: valid_comp=0.1129, test_comp=0.0666, avg_comp=0.0898, gap=0.0463

## Top Test Read

- `(Ts=0.5500, Tl=0.395)`: valid_comp=0.0582, test_comp=0.0798, avg_comp=0.0690

## Verdict

- verdict: `tiny exploration still supports the lower-short / 0.400-long edge; do not freeze yet`
- read: the local optimum has not moved away from the lower edge of the short-threshold pocket, which means we are probably pressing against the boundary rather than sitting at a broad interior peak.
