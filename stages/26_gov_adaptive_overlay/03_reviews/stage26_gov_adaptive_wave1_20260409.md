# Stage 26 Governance-Led Adaptive Overlays Wave 1

- reviewed_on: `2026-04-09`
- purpose: `move governance telemetry from monitoring into non-blocking risk taper overlays on the 25D regular baseline`
- operating_seed: `25D_24a_monpost_t050_m030_psh2_0001`
- roadmap_anchor: `Grok + GPT governance-led adaptive overlays wave`

## Scoreboard

| run | hist_return | val_return | test_return | test_dd | test_pf | gov_state | mean_ext_skip | mean_argmax | mean_entropy | mean_overlay | read |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `26A` | `25.958` | `256.928` | `85.986` | `27.318` | `1.3921` | `OK` | `0.3119` | `0.5879` | `0.9323` | `0.2670` | `governance observe-only inherited baseline` |
| `26B` | `15.268` | `194.724` | `74.020` | `23.861` | `1.4043` | `OK` | `0.3119` | `0.5879` | `0.9323` | `0.6219` | `signal drift taper` |
| `26C` | `26.696` | `257.694` | `86.314` | `27.225` | `1.3937` | `OK` | `0.3119` | `0.5879` | `0.9323` | `0.2670` | `external skip burst taper` |
| `26D` | `21.228` | `225.064` | `80.084` | `25.735` | `1.3982` | `OK` | `0.3119` | `0.5879` | `0.9323` | `0.6219` | `combined mild governance taper` |

## Headline

- baseline `26A`: `{'hist': 25.958, 'val': 256.928, 'test': 85.98599999999999, 'test_dd': 27.317947209370747, 'test_pf': 1.39208944742866}`
- best challenger `26C`: `{'hist': 26.695999999999998, 'val': 257.694, 'test': 86.31400000000001, 'test_dd': 27.225333850205196, 'test_pf': 1.3936676761411317}`

## Risk

- baseline OOS risk read: `{'worst_week': -130.89000000000001, 'ulcer': 12.46086877071514, 'consecutive_losses': 11}`
- challenger OOS risk read: `{'worst_week': -130.89000000000001, 'ulcer': 12.39945069825904, 'consecutive_losses': 11}`

## Diagnostics

- baseline diagnostics: `{'no_trade_rate': 0.8760917838638046, 'long_count': 140, 'short_count': 139}`
- challenger diagnostics: `{'no_trade_rate': 0.8760917838638046, 'long_count': 140, 'short_count': 139}`
- this wave should be read as a `risk taper` experiment, so `mean overlay rate` and trade-mix drift matter alongside headline return.

## Execution

- baseline governance read: `{'latest_state': 'OK', 'latest_reason': 'WITHIN_LIMITS', 'top_reasons': {'WITHIN_LIMITS': 11037, 'ARGMAX_DOMINANCE': 3165, 'OP_SKIP_RATE|EXTERNAL_SKIP_RATE|ARGMAX_DOMINANCE': 2444}}`
- challenger governance read: `{'latest_state': 'OK', 'latest_reason': 'WITHIN_LIMITS', 'top_reasons': {'WITHIN_LIMITS': 11037, 'ARGMAX_DOMINANCE': 3165, 'OP_SKIP_RATE|EXTERNAL_SKIP_RATE|ARGMAX_DOMINANCE': 2444}}`
- execution path stayed exact-alignment and non-blocking: `governance was observe-only for all arms; challengers only changed risk_pct taper behavior, not entry blocking`

## Decision

- regular incumbent: `26A_25d_govref_0001`
- regular shadow challenger: `26C_25d_gext085_0001`
- decision: `keep_incumbent`
- why: `promote only if governance-driven taper improves the regular OOS read or clearly improves containment without obvious non-OOS damage`
