# Stage 04 Probability Difference Filter

## Goal

Search the probability-difference filter on its own.

This stage is limited to:

- `min_probability_diff`

## Fixed Baseline

To keep this stage logic-isolated:

- `short_threshold = 1/3`
- `long_threshold = 1/3`
- `min_margin = 0`

These values are neutral defaults, not carried outputs from Stage 02 or Stage 03.

## Difference Definition

Use the narrow Stage 04 interpretation:

- long candidate: `p_long >= long_threshold`
- short candidate: `p_short >= short_threshold`
- resolve direction between short and long first
- then require the selected side probability to exceed the opposing directional probability by at least `min_probability_diff`
- if the condition fails, convert to `no-trade`

This means Stage 04 ignores `p_flat` inside the added filter.

## Out Of Scope

Do not mix these into Stage 04:

- Stage 02 threshold asymmetry
- Stage 03 max-probability margin logic
- hold-bar variants
- flip / re-entry / cooldown rules
- multi-logic bundles

## Search Discipline

- Use the Stage 01 search-side model path for Stage 04 exploration
- Keep the Stage 01 final refit handoff reserved for later confirmation reads
- Keep fixed `3`-bar time exit
- Keep no overlap
- Keep no flip
- Keep zero trading cost assumption
