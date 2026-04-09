# Stage 25 Soft Contextual Thresholds and Hold Control Wave 1

- reviewed_on: `2026-04-09`
- purpose: `softly penalize weak short contexts instead of reviving hard detector blocks`
- operating_seed: `24A_23a_base_gate_ref_0001`
- roadmap_anchor: `Claude + GPT soft contextual threshold and hold-control wave`

## Scoreboard

| run | hist_return | val_return | test_return | test_dd | test_pf | test_short_count | test_monshort_net | test_postshort_net | read |
|---|---|---|---|---|---|---|---|---|---|
| `25A` | `26.002` | `193.808` | `71.068` | `27.423` | `1.3199` | `163` | `-33.160` | `-39.480` | `regular inherited baseline` |
| `25B` | `33.536` | `224.066` | `75.288` | `28.125` | `1.3479` | `153` | `-21.000` | `-39.480` | `Monday short soft suppressor` |
| `25C` | `23.046` | `211.360` | `77.610` | `26.529` | `1.3496` | `151` | `-34.680` | `-17.970` | `NY postcash short soft suppressor` |
| `25D` | `25.958` | `256.928` | `85.986` | `27.318` | `1.3921` | `139` | `-22.660` | `-11.270` | `combined short suppressor plus postcash short hold cut` |

## Headline

- inherited `25A` reference: `{'hist': 26.002, 'val': 193.808, 'test': 71.06800000000001, 'test_dd': 27.422721683680763, 'test_pf': 1.3199272524286705}`
- promoted candidate `25D`: `{'hist': 25.958, 'val': 256.928, 'test': 85.98599999999999, 'test_dd': 27.317947209370747, 'test_pf': 1.39208944742866}`

## Risk

- inherited reference OOS risk read: `{'worst_week': -117.39000000000001, 'ulcer': 13.066089094415775, 'consecutive_losses': 9}`
- promoted candidate OOS risk read: `{'worst_week': -130.89000000000001, 'ulcer': 12.46086877071514, 'consecutive_losses': 11}`

## Diagnostics

- inherited reference short pockets: `{'monday_short_net': -33.160000000000004, 'postcash_short_net': -39.48000000000001, 'postcash_short_time_exit_net': 3.5199999999999974}`
- promoted candidate short pockets: `{'monday_short_net': -22.66, 'postcash_short_net': -11.27, 'postcash_short_time_exit_net': 0.0}`
- this wave should be read as a `contextual short cleanup` experiment, so `Monday short` and `NY postcash short` nets matter as much as raw test return.

## Execution

- execution path is unchanged: `same exact-alignment runtime, same feature contract, same risk_pct execution; only contextual filter penalties and one optional postcash short hold cut changed`
- inherited reference test execution: `{'skip_rate': 0.7660606060606061, 'external_mismatch_count': 8976}`
- promoted candidate test execution: `{'skip_rate': 0.7660606060606061, 'external_mismatch_count': 8976}`

## Decision

- inherited_regular_reference: `24A_23a_base_gate_ref_0001`
- regular incumbent: `25D_24a_monpost_t050_m030_psh2_0001`
- regular shadow challenger: `25C_24a_postshort_t050_m030_0001`
- decision: `replace_incumbent`
- why: `replace only if the contextual cleanup helps the regular OOS read without obvious non-OOS damage or obvious short-book starvation`
