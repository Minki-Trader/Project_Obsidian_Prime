# 03C Margin Stability Probe Review

Generated at: `2026-03-28T06:55:31.056669+00:00`

## Scope

- purpose: `probe the stability pocket more finely without changing the Stage 03 margin-only concept`
- fixed thresholds: `(short_threshold=0.333333, long_threshold=0.333333)`
- local min_margins: `0.0790, 0.0800, 0.0810, 0.0820, 0.0825, 0.0830, 0.0840, 0.0850, 0.0860`
- this is still margin-only exploration; no threshold asymmetry is introduced here

## Headline Read

- stability-pocket leader: `(min_margin=0.0825)`, valid_comp=`0.0770`, test_comp=`0.0540`, avg_comp=`0.0655`, gap=`0.0230`
- tight-gap leader: `(min_margin=0.0840)`, valid_comp=`0.0567`, test_comp=`0.0536`, avg_comp=`0.0552`, gap=`0.0031`

## Stability Order

- `min_margin=0.0825`: valid_comp=0.0770, test_comp=0.0540, avg_comp=0.0655, gap=0.0230
- `min_margin=0.0830`: valid_comp=0.0667, test_comp=0.0602, avg_comp=0.0634, gap=0.0065
- `min_margin=0.0820`: valid_comp=0.0731, test_comp=0.0516, avg_comp=0.0623, gap=0.0214
- `min_margin=0.0810`: valid_comp=0.0698, test_comp=0.0549, avg_comp=0.0623, gap=0.0149
- `min_margin=0.0840`: valid_comp=0.0567, test_comp=0.0536, avg_comp=0.0552, gap=0.0031
- `min_margin=0.0860`: valid_comp=0.0510, test_comp=0.0569, avg_comp=0.0540, gap=0.0059
- `min_margin=0.0800`: valid_comp=0.0484, test_comp=0.0538, avg_comp=0.0511, gap=0.0055
- `min_margin=0.0850`: valid_comp=0.0483, test_comp=0.0518, avg_comp=0.0501, gap=0.0035
- `min_margin=0.0790`: valid_comp=0.0295, test_comp=0.0580, avg_comp=0.0438, gap=0.0285

## Gap Order

- `min_margin=0.0840`: valid_comp=0.0567, test_comp=0.0536, avg_comp=0.0552, gap=0.0031
- `min_margin=0.0850`: valid_comp=0.0483, test_comp=0.0518, avg_comp=0.0501, gap=0.0035
- `min_margin=0.0800`: valid_comp=0.0484, test_comp=0.0538, avg_comp=0.0511, gap=0.0055
- `min_margin=0.0860`: valid_comp=0.0510, test_comp=0.0569, avg_comp=0.0540, gap=0.0059
- `min_margin=0.0830`: valid_comp=0.0667, test_comp=0.0602, avg_comp=0.0634, gap=0.0065
- `min_margin=0.0810`: valid_comp=0.0698, test_comp=0.0549, avg_comp=0.0623, gap=0.0149
- `min_margin=0.0820`: valid_comp=0.0731, test_comp=0.0516, avg_comp=0.0623, gap=0.0214
- `min_margin=0.0825`: valid_comp=0.0770, test_comp=0.0540, avg_comp=0.0655, gap=0.0230
- `min_margin=0.0790`: valid_comp=0.0295, test_comp=0.0580, avg_comp=0.0438, gap=0.0285

## Verdict

- verdict: `keep Stage 03 margin-only and treat this probe as a stability read, not a bundle decision`
- read: the local pocket now lets us separate the stronger blended read from the tighter-gap read, which is exactly the information we need before deciding whether to freeze or just synthesize.
