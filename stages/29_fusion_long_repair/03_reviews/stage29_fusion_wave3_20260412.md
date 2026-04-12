# Stage 29 Fusion Wave 3 Review

- reviewed_on: `2026-04-12`
- stage: `29_fusion_long_repair`
- inherited_regular_incumbent: `29N_25o_sxh2_0001`
- inherited_regular_shadow: `29S_25o_sxh2_gweak_0001`
- best_wave3_close_call: `29AC_25o_sxh2_lock1_gweak_0001`
- decision: `keep_29N_and_29S_no_wave3_promotion`

## Executive Read

- Wave 3 was a narrow refinement pass around the successful `h2` backbone.
- none of the six follow-up arms beat the `29N / 29S` pair on a full three-window read
- the strongest new close call was `29AC`, which kept the `h2` balance fairly well, but it still lost on both `hist_2024` and `test` headline versus `29S`
- the practical result is a no-change decision:
  - incumbent stays `29N`
  - shadow stays `29S`
  - best pure recent-window arm stays `29W`

## What Was Tested

- `29X / 29Y`: `h2` directional split long-loose short-tight, with and without weak-pocket governance
- `29Z / 29AA`: `h2` looser `max_direction_margin=0.05`, with and without weak-pocket governance
- `29AB / 29AC`: `h2` base rule plus one-bar reentry lock, with and without weak-pocket governance

## Main Read

- incumbent `29N`: `{'hist': {'return_pct': 39.368, 'pf': 1.2021, 'dd_pct': 14.8134}, 'validation': {'return_pct': 196.808, 'pf': 1.5717, 'dd_pct': 12.9472}, 'test': {'return_pct': 99.556, 'pf': 1.4828, 'dd_pct': 20.2164}}`
- shadow `29S`: `{'hist': {'return_pct': 39.10, 'pf': 1.2009, 'dd_pct': 14.7646}, 'validation': {'return_pct': 197.53, 'pf': 1.5810, 'dd_pct': 12.9087}, 'test': {'return_pct': 100.594, 'pf': 1.4883, 'dd_pct': 20.1777}}`
- best Wave 3 close call `29AC`: `{'hist': {'return_pct': 36.924, 'pf': 1.1920, 'dd_pct': 14.7695}, 'validation': {'return_pct': 188.284, 'pf': 1.5457, 'dd_pct': 12.7781}, 'test': {'return_pct': 99.086, 'pf': 1.4833, 'dd_pct': 19.9942}}`

## What Failed

- `h2` direction split did not keep the magic from the aggressive `29W` family:
  - `29X / 29Y` both lost too much `hist_2024` headline while still failing to reach the recent-window upside of `29W`
- `h2` loose margin also was not the bridge we wanted:
  - `29Z / 29AA` improved drawdown versus `29N`
  - but they gave back too much `hist_2024` and `test` headline
- the one-bar lock arms were the closest:
  - `29AB / 29AC` kept the shape of `29N`
  - but neither one clearly improved enough to justify another incumbent replacement

## Best New Close Call

- `29AC` was the best Wave 3 arm because it stayed reasonably close to the `29N / 29S` balanced line:
  - `hist_2024 return_pct = 36.924`
  - `test return_pct = 99.086`
  - `test pf = 1.4833`
  - `test dd_pct = 19.9942`
- but it still lost to `29S` on all three headline windows:
  - `hist_2024`: `36.924` vs `39.10`
  - `validation`: `188.284` vs `197.53`
  - `test`: `99.086` vs `100.594`

## Decision

- keep `29N_25o_sxh2_0001` as the live regular lane
- keep `29S_25o_sxh2_gweak_0001` as the regular shadow challenger
- record `29AC_25o_sxh2_lock1_gweak_0001` as the best Wave 3 close call, not as a promoted arm
- close the narrow `h2 refinement` lane for now; it did not find a stronger balanced replacement

## Follow-Up Bias

- do not reopen more tiny `h2` parameter nudges immediately; Wave 3 already tested the most natural nearby variants
- if Stage 29 reopens, it should do so only for a genuinely different hypothesis, not another local tweak around `29N`
- keep `29W` and `29T` as the aggressive upside references if a future stage wants to deliberately trade some older-window balance for more recent-window power
