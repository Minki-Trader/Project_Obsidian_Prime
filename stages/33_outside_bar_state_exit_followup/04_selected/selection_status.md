# Stage 33 Selection Status

- reviewed_on: `2026-04-12`
- stage: `33_outside_bar_state_exit_followup`
- roadmap_anchor: `runtime follow-up on Stage 32 outside adverse bar diagnosis`
- inherited_regular_reference: `29N_25o_sxh2_0001`

## Current Read

- best_new_candidate: `33C_29n_outbar_long_0001`
- near_tie_broader_variant: `33B_29n_outbar_both_0001`
- keep_or_replace: `keep_29N_live_record_33C_only_as_targeted_shadow_candidate`

## Promotion Gates

- gate_1: `carry check must reproduce 29N exactly under the updated EA path`
- gate_2: `candidate must preserve the current test window while adding value elsewhere`
- gate_3: `the runtime story must stay aligned with the Stage 32 directional diagnosis; short-side-only value is not enough`

## Scoreboards

- regular_risk_execution: `active for this wave`
- structural_scout: `not used`

## Headline

- inherited reference `29N`: `{'hist': 39.368, 'validation': 196.808, 'test': 99.556}`
- carry check `33A`: `matched 29N exactly across validation / test / hist_2024`
- best new candidate `33C`: `{'hist': 45.816, 'validation': 196.778, 'test': 99.556}`
- broader near-tie `33B`: `{'hist': 45.826, 'validation': 196.772, 'test': 99.556}`
- short-only `33D`: `{'hist': 38.316, 'validation': 196.852, 'test': 99.556}`
- ATR-floor variants `33E / 33F`: `hist stayed positive but validation fell to 194.686 / 194.910`

## Risk

- `33C` kept the test DD unchanged and only nudged older-window DD slightly:
  - validation DD delta: `+0.0013`
  - test DD delta: `0.0000`
  - hist DD delta: `+0.0543`
- `33B` had slightly cleaner DD deltas than `33C`:
  - validation DD delta: `-0.0050`
  - test DD delta: `0.0000`
  - hist DD delta: `-0.0122`
- `33D` lowered hist DD a little but gave back headline return, so it did not earn continuation

## Diagnostics

- `33A` proved the new EA runtime path is clean:
  - no accidental metric drift versus `29N`
- the Stage 32 directional read held up in live MT5 runs:
  - `33C` long-only gave the cleanest follow-up
  - `33D` short-only weakened the older-window headline
- the intervention stayed sparse and interpretable:
  - `33C` suppressions: validation `2`, test `0`, hist `5`
  - `33B` suppressions: validation `6`, test `0`, hist `9`
- the first ATR floor did not help:
  - it removed some suppressions
  - but the validation tax was too visible for the small remaining benefit

## Execution

- execution contract stayed unchanged from the live-like Stage 29 lane
- the current test window was untouched because no qualifying outside-bar state exits fired there
- this means Stage 33 is an `older-window plus validation-shape` improvement, not a current-test-window rescue

## Decision

- keep `29N_25o_sxh2_0001` as the live regular lane
- record `33C_29n_outbar_long_0001` as the first runtime-positive candle-shape shadow candidate
- record `33B_29n_outbar_both_0001` as the broader near-tie, not as the preferred follow-up
- close `33D` short-only and `33E / 33F` ATR-floor local variants for now

## Follow-Up Bias

- if this topic reopens, start from `33C` long-only without the ATR floor
- do not reopen short-only outside-bar suppression first
- if a next local search is needed, prefer tighter long-side context or trigger-shape checks over broader both-direction expansion
- do not promote from Stage 33 alone unless a future window also shows real qualifying events and preserves the same non-regression shape

## Report Refs

- `03_reviews/stage33_outside_bar_followup_20260412.md`
- `03_reviews/stage33_outside_bar_followup_20260412.json`
