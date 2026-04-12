# Stage 33 Review Index

- reviewed_on: `2026-04-12`
- latest_review: `03_reviews/stage33_outside_bar_followup_20260412.md`
- inherited_regular_reference: `29N_25o_sxh2_0001`
- carry_check: `33A_29n_refcarry_0001`
- best_new_candidate: `33C_29n_outbar_long_0001`
- near_tie_broader_variant: `33B_29n_outbar_both_0001`
- decision: `keep_29N_live_record_33C_as_targeted_shadow_only`

## Quick Read

- `33A` reproduced the inherited `29N` numbers exactly, so the EA-side runtime change did not create a hidden regression
- `33C` was the cleanest new runtime-positive arm:
  - `test` stayed unchanged
  - `hist_2024` improved from `39.368` to `45.816`
  - validation stayed essentially flat at `196.778` vs `196.808`
- `33B` was a near-tie broad twin with slightly better risk deltas, but it leaned on extra short-side suppressions that the Stage 32 diagnostic did not really support
- `33D` confirmed the diagnostic warning that short-only suppression is not the story
- `33E / 33F` showed that adding the first ATR floor made validation worse without buying a better overall answer
