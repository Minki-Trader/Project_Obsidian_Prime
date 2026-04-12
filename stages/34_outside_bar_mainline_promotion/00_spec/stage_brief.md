# Stage 34 Brief

- stage: `34_outside_bar_mainline_promotion`
- status: `wave1_completed`
- stage_type: `regular_alpha_stage`
- inherited_regular_reference: `29N_25o_sxh2_0001`
- inherited_regular_shadow: `29S_25o_sxh2_gweak_0001`

## Purpose

- return from the extra diagnostic lane to the regular alpha lane
- promote only the one extra finding that survived real MT5 runtime testing:
  - `33C` long-only outside adverse bar suppression
- check whether that sidecar deserves a place inside the main operating stage rather than as a diagnostic-only shadow note

## Working Hypothesis

- `29N` remains the balanced live lane
- `29S` remains the closest existing shadow because it slightly improved the current `test` window without recovering enough older-window edge to replace `29N`
- Stage 33 showed that `long-only outside adverse bar -> suppress STATE_EXIT_MARGIN` is the first candle-shape sidecar with real runtime value
- the next regular-stage question is therefore:
  - does the `33C` sidecar improve the mainline by itself?
  - does it combine cleanly with the `29S` shadow lane?

## Wave 1 Run Shape

- `34A`: direct `29N` carry rerun
- `34B`: direct `29S` carry rerun
- `34C`: `29N + 33C`
- `34D`: `29S + 33C`

## Promotion Gates

- carry clones must reproduce the inherited references cleanly
- any promoted arm must preserve the current `test` window while earning its change on the full three-window read
- do not promote a candle-sidecar lane that only recreates a diagnostic story without a cleaner operating read than `29N / 29S`
