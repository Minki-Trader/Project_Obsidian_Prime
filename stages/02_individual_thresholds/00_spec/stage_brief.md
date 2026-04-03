# Stage 02 Individual Thresholds

## Goal

Search only the `individual thresholds` part of the contract.

This stage is limited to:

- `short_threshold`
- `long_threshold`

## Out Of Scope

Do not mix these into this stage:

- max-probability margin
- probability-difference based filter
- hold-bar variants
- flip / re-entry / cooldown rules

Those belong to later stages.

## Search Discipline

- Use the Stage 01 search-side model path for Stage 02 exploration
- Keep the Stage 01 final refit handoff reserved for later confirmation only
- Keep `min_margin = 0` throughout Stage 02
- Treat `p_flat` as part of the probability vector, but do not add extra margin logic yet

## Current 02A Scope

- fixed `3`-bar time exit aligned to the Stage 01 label horizon
- no overlap
- no flip
- no same-bar re-entry tricks
- zero trading cost assumption for the first threshold sweep
