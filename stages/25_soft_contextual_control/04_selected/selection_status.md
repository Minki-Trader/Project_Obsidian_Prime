# Stage 25 Selection Status

- reviewed_on: `2026-04-09`
- stage: `25_soft_contextual_control`
- roadmap_anchor: `Claude + GPT soft contextual threshold and hold-control wave`
- inherited_regular_reference: `24A_23a_base_gate_ref_0001`

## Current Read

- regular incumbent: `25D_24a_monpost_t050_m030_psh2_0001`
- regular shadow challenger: `25C_24a_postshort_t050_m030_0001`
- keep_or_replace: `replace_incumbent`

## Scoreboard

| run | hist_return | val_return | test_return | test_dd | test_pf | test_monshort_net | test_postshort_net | read |
|---|---|---|---|---|---|---|---|---|
| `25A` | `26.002` | `193.808` | `71.068` | `27.423` | `1.3199` | `-33.160` | `-39.480` | `regular inherited baseline` |
| `25B` | `33.536` | `224.066` | `75.288` | `28.125` | `1.3479` | `-21.000` | `-39.480` | `Monday short soft suppressor` |
| `25C` | `23.046` | `211.360` | `77.610` | `26.529` | `1.3496` | `-34.680` | `-17.970` | `NY postcash short soft suppressor` |
| `25D` | `25.958` | `256.928` | `85.986` | `27.318` | `1.3921` | `-22.660` | `-11.270` | `combined short suppressor plus postcash short hold cut` |

## Diagnostics

- shadow contextual short read `25C`: `{'short_total_count': 151, 'short_total_net': 346.17999999999995, 'short_total_avg': 2.2925827814569533, 'monday_short_count': 13, 'monday_short_net': -34.68, 'monday_short_avg': -2.667692307692308, 'postcash_short_count': 5, 'postcash_short_net': -17.970000000000002, 'postcash_short_avg': -3.5940000000000003, 'postcash_short_time_exit_count': 13, 'postcash_short_time_exit_net': 9.240000000000002, 'postcash_short_time_exit_avg': 0.7107692307692309}`

## Decision

- decision: `replace_incumbent`
- regular incumbent: `25D_24a_monpost_t050_m030_psh2_0001`
- regular shadow challenger: `25C_24a_postshort_t050_m030_0001`

## Follow-Up Bias

- keep the contextual overlay line only if it improves the OOS short pockets without obvious book starvation
- read the postcash short hold-cut arm as containment logic first, not as a headline-return trick

## Report Refs

- `03_reviews/stage25_soft_contextual_wave1_20260409.md`
