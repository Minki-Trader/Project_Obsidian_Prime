# 05A max_probability_margin Family Probe Review

Generated at: `2026-03-29T10:34:09.713386+00:00`

## Scope

- purpose: `probe max_probability_margin on its own inside Stage 05 before any combined-rule synthesis`
- fixed thresholds: `(short_threshold=0.333333, long_threshold=0.333333)`
- local min_margin values: `0.0650, 0.0700, 0.0725, 0.0750, 0.0775, 0.0800, 0.0825, 0.0850, 0.0900`
- this remains a single-family logic read on the fixed Stage 01 model and feature base

## Headline Read

- blended leader: `(min_margin=0.0700)`, valid_comp=`0.0385`, test_comp=`0.0985`, avg_comp=`0.0685`
- tight-gap leader: `(min_margin=0.0850)`, valid_comp=`0.0483`, test_comp=`0.0518`, avg_comp=`0.0501`, gap=`0.0035`

## Stability Order

- `min_margin=0.0700`: valid_comp=0.0385, test_comp=0.0985, avg_comp=0.0685, gap=0.0600
- `min_margin=0.0825`: valid_comp=0.0770, test_comp=0.0540, avg_comp=0.0655, gap=0.0230
- `min_margin=0.0725`: valid_comp=0.0151, test_comp=0.1000, avg_comp=0.0575, gap=0.0849
- `min_margin=0.0800`: valid_comp=0.0484, test_comp=0.0538, avg_comp=0.0511, gap=0.0055
- `min_margin=0.0850`: valid_comp=0.0483, test_comp=0.0518, avg_comp=0.0501, gap=0.0035
- `min_margin=0.0750`: valid_comp=0.0164, test_comp=0.0836, avg_comp=0.0500, gap=0.0672
- `min_margin=0.0775`: valid_comp=0.0159, test_comp=0.0593, avg_comp=0.0376, gap=0.0434
- `min_margin=0.0900`: valid_comp=0.0282, test_comp=0.0410, avg_comp=0.0346, gap=0.0128
- `min_margin=0.0650`: valid_comp=-0.0222, test_comp=0.1094, avg_comp=0.0436, gap=0.1316

## Verdict

- verdict: `keep max_probability_margin isolated for Stage 05 and compare it family-first before any synthesis`
- read: this probe is meant to keep the search family-isolated so the next Stage 05 step can compare rule families cleanly instead of forcing a merged stack too early.
