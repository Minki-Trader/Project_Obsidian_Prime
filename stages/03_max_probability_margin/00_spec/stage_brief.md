# Stage 03 Max Probability Margin

## Goal

Search the `max_probability_margin` logic on its own.

This stage is limited to:

- `min_margin`

## Fixed Baseline

To keep this stage logic-isolated:

- `short_threshold = 1/3`
- `long_threshold = 1/3`

These threshold values are treated as neutral default decision values, not as a carried Stage 02 result.

## Margin Definition

Use the contract interpretation:

- long candidate: `p_long >= long_threshold`
- short candidate: `p_short >= short_threshold`
- selected side still resolves between short and long first
- then require the selected side probability to exceed the maximum of the remaining probabilities by at least `min_margin`
- if the condition fails, convert to `no-trade`

This means `p_flat` participates in Stage 03 because it can block a trade through the max-probability comparison.

## Out Of Scope

Do not mix these into Stage 03:

- Stage 02 carried thresholds
- probability-difference filter logic
- hold-bar variants
- flip / re-entry / cooldown rules
- multi-logic bundles

## Search Discipline

- Use the Stage 01 search-side model path for Stage 03 exploration
- Keep the Stage 01 final refit handoff reserved for later confirmation reads
- Keep fixed `3`-bar time exit
- Keep no overlap
- Keep no flip
- Keep zero trading cost assumption
