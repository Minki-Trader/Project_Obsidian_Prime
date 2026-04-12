# Stage 35 Brief

- stage: `35_candle_sidecar_simplification_check`
- status: `wave1_completed`
- stage_type: `regular_alpha_stage`
- inherited_regular_reference: `34D_29s_outbarlong_0001`
- inherited_regular_shadow: `34B_29s_refcarry_0001`
- verified_runtime_reference: `exp_34d_29s_outbarlong_v1_handoff`

## Purpose

- test whether the new `34D` operating line should stay as-is after the runtime handoff check
- compare the full `34D` line directly against the simplest already-proven fallback:
  - `34B` governance-only carry without the candle sidecar
- answer the simplification question before opening any broader local follow-up wave

## Working Hypothesis

- `34D` is the strongest balanced regular operating answer after Stage 34
- the most honest simplification check is not a new local tweak but the clean removal of the extra moving part:
  - remove the long-only outside-bar suppressor
  - keep the underlying `29S` governance line
- if that simplification preserves the current-window read but gives back too much `hist_2024` edge, keep `34D`

## Wave 1 Run Shape

- `35A`: direct `34D` carry rerun inside the new stage path
- `35B`: direct `34B` governance-only simplification carry rerun inside the new stage path

## Promotion Gates

- carry clones must reproduce the inherited Stage 34 reads cleanly
- any simplification claim must preserve the current `test` window
- simplification must not give back a material amount of the older-window edge that made `34D` worth promoting
- do not simplify just because a governance-only lane is cleaner on paper if the measured three-window balance is worse
