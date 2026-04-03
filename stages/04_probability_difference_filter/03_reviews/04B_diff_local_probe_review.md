# 04B Probability-Diff Local Probe Review

Generated at: `2026-03-28T07:16:56.281687+00:00`

## Scope

- purpose: `probe the higher probability-difference pocket more finely without changing the Stage 04 concept`
- fixed thresholds: `(short_threshold=0.333333, long_threshold=0.333333)`
- fixed min_margin: `0.00`
- local min_probability_diffs: `0.0700, 0.0725, 0.0750, 0.0775, 0.0800, 0.0825, 0.0850, 0.0875, 0.0900, 0.0950, 0.1000`
- this is still probability-difference-only exploration; no threshold asymmetry or max-probability margin is introduced here

## Headline Read

- best local blended read: `(min_probability_diff=0.0825)`, valid_comp=`0.0922`, test_comp=`0.0494`, avg_comp=`0.0708`
- strongest local test read: `(min_probability_diff=0.0725)`, valid_comp=`0.0384`, test_comp=`0.0933`, avg_comp=`0.0659`

## Top Stable Reads

- `min_probability_diff=0.0825`: valid_comp=0.0922, test_comp=0.0494, avg_comp=0.0708, gap=0.0428
- `min_probability_diff=0.0725`: valid_comp=0.0384, test_comp=0.0933, avg_comp=0.0659, gap=0.0549
- `min_probability_diff=0.0700`: valid_comp=0.0432, test_comp=0.0883, avg_comp=0.0657, gap=0.0451
- `min_probability_diff=0.0800`: valid_comp=0.0709, test_comp=0.0447, avg_comp=0.0578, gap=0.0262
- `min_probability_diff=0.0750`: valid_comp=0.0344, test_comp=0.0747, avg_comp=0.0546, gap=0.0403
- `min_probability_diff=0.0850`: valid_comp=0.0559, test_comp=0.0457, avg_comp=0.0508, gap=0.0102
- `min_probability_diff=0.0775`: valid_comp=0.0492, test_comp=0.0504, avg_comp=0.0498, gap=0.0012
- `min_probability_diff=0.0950`: valid_comp=0.0455, test_comp=0.0384, avg_comp=0.0419, gap=0.0071
- `min_probability_diff=0.0875`: valid_comp=0.0365, test_comp=0.0416, avg_comp=0.0391, gap=0.0050
- `min_probability_diff=0.0900`: valid_comp=0.0313, test_comp=0.0366, avg_comp=0.0339, gap=0.0053

## Top Test Reads

- `min_probability_diff=0.0725`: valid_comp=0.0384, test_comp=0.0933, avg_comp=0.0659, gap=0.0549
- `min_probability_diff=0.0700`: valid_comp=0.0432, test_comp=0.0883, avg_comp=0.0657, gap=0.0451
- `min_probability_diff=0.0750`: valid_comp=0.0344, test_comp=0.0747, avg_comp=0.0546, gap=0.0403
- `min_probability_diff=0.0775`: valid_comp=0.0492, test_comp=0.0504, avg_comp=0.0498, gap=0.0012
- `min_probability_diff=0.0825`: valid_comp=0.0922, test_comp=0.0494, avg_comp=0.0708, gap=0.0428
- `min_probability_diff=0.0850`: valid_comp=0.0559, test_comp=0.0457, avg_comp=0.0508, gap=0.0102
- `min_probability_diff=0.0800`: valid_comp=0.0709, test_comp=0.0447, avg_comp=0.0578, gap=0.0262
- `min_probability_diff=0.0875`: valid_comp=0.0365, test_comp=0.0416, avg_comp=0.0391, gap=0.0050
- `min_probability_diff=0.1000`: valid_comp=0.0274, test_comp=0.0392, avg_comp=0.0333, gap=0.0118
- `min_probability_diff=0.0950`: valid_comp=0.0455, test_comp=0.0384, avg_comp=0.0419, gap=0.0071

## Verdict

- verdict: `keep Stage 04 in probability-difference-only mode and keep the probe narrow`
- read: once valid turns clearly positive, the better local blended reads stay in the higher-diff pocket rather than sliding back toward the lower-diff test-favored area.
