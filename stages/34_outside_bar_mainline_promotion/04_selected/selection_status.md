# Stage 34 Selection Status

- reviewed_on: `2026-04-12`
- stage: `34_outside_bar_mainline_promotion`
- stage_type: `regular_alpha_stage`
- inherited_regular_reference: `29N_25o_sxh2_0001`
- inherited_regular_shadow: `29S_25o_sxh2_gweak_0001`

## Current Read

- new_regular_incumbent: `34D_29s_outbarlong_0001`
- new_regular_shadow: `34B_29s_refcarry_0001`
- decomposition_reference: `34C_29n_outbarlong_0001`
- keep_or_replace: `replace_29N_with_34D_keep_34B_as_governance_only_shadow`

## Promotion Gates

- gate_1: `carry clones must reproduce 29N / 29S cleanly under the new stage path`
- gate_2: `promoted arm must preserve the current test window while improving the broader three-window balance`
- gate_3: `the promoted answer should beat both the old regular incumbent and the old shadow, not just one of them`

## Scoreboards

- regular_risk_execution: `active`
- structural_scout: `not used`

## Headline

- old regular incumbent `29N`: `{'hist': 39.368, 'validation': 196.808, 'test': 99.556}`
- old shadow carry `34B`: `{'hist': 39.100, 'validation': 197.530, 'test': 100.594}`
- candle-only decomposition `34C`: `{'hist': 45.816, 'validation': 196.778, 'test': 99.556}`
- new regular incumbent `34D`: `{'hist': 46.374, 'validation': 197.520, 'test': 100.594}`

## Risk

- `34D` versus `29N`:
  - validation DD delta: `-0.0387`
  - test DD delta: `+0.0451`
  - hist DD delta: `+0.0604`
- the DD trade-off stayed very small relative to the headline and PF gains
- `34D` versus `34B`:
  - validation stayed effectively flat
  - test stayed effectively identical
  - `hist_2024` improved materially

## Diagnostics

- `34A` and `34B` validated that the stage opened from clean carry-forward baselines
- `34C` proved the long-only outside-bar sidecar is not just a governance interaction artifact
- `34D` showed the stronger combined story:
  - keep the `29S` shadow's current-window edge
  - add the `34C` older-window recovery
- this is the first time the candle-sidecar idea has earned a regular-stage promotion claim

## Execution

- execution contract remains the same live-like Stage 29 path
- no alignment relaxation or extra execution concession was introduced
- the promoted change is a narrow runtime state-exit sidecar, not a broad execution rewrite

## Decision

- promote `34D_29s_outbarlong_0001` as the new regular incumbent
- keep `34B_29s_refcarry_0001` as the new regular shadow because it isolates the prior governance-only answer
- keep `34C_29n_outbarlong_0001` as a decomposition reference that isolates the candle-sidecar contribution
- retire `29N` and `29S` as prior-stage references rather than current operating winners

## Follow-Up Bias

- if this new line gets a local follow-up, start from `34D`, not from `29N`
- keep the outside-bar sidecar long-only until a new hypothesis justifies widening it
- do not reopen short-only outside-bar logic
- if a later stage wants to simplify, compare `34D` against `34B` first to test whether the candle-sidecar remains worth the extra moving part

## Report Refs

- `03_reviews/stage34_mainline_20260412.md`
- `03_reviews/stage34_mainline_20260412.json`
