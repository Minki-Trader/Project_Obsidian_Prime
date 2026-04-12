# Stage 35 Selection Status

- reviewed_on: `2026-04-12`
- stage: `35_candle_sidecar_simplification_check`
- stage_type: `regular_alpha_stage`
- inherited_regular_reference: `34D_29s_outbarlong_0001`
- inherited_regular_shadow: `34B_29s_refcarry_0001`

## Current Read

- verified_regular_incumbent: `35A_34d_refcarry_0001`
- simplification_shadow: `35B_34b_simpleref_0001`
- keep_or_replace: `keep_34D_do_not_simplify_to_34B`

## Promotion Gates

- gate_1: `carry clones must reproduce the Stage 34 operating read cleanly under the new stage path`
- gate_2: `any simplification claim must preserve the current test window`
- gate_3: `a simplification must not give back a material amount of the older-window edge that made 34D worth promoting`

## Scoreboards

- regular_risk_execution: `active`
- structural_scout: `not used`

## Headline

- verified `35A / 34D` carry: `{'hist': 46.374, 'validation': 197.520, 'test': 100.594}`
- simplification `35B / 34B` carry: `{'hist': 39.100, 'validation': 197.530, 'test': 100.594}`
- simplification delta versus `35A`:
  - validation return: `+0.010`
  - test return: `+0.000`
  - hist return: `-7.274`

## Risk

- validation and test DD were effectively identical between `35A` and `35B`
- `35B` improved `hist_2024` DD slightly:
  - hist DD delta versus `35A`: `-0.1089`
- that DD improvement was too small to offset the large `hist_2024` return and PF giveback

## Diagnostics

- the simplification candidate did exactly what the stage was designed to test:
  - preserve the `29S` governance backbone
  - remove the long-only outside-bar sidecar entirely
- the cost of that simplification showed up in the older window, not in the current one
- the clearest diagnostic loss was on the long side:
  - `hist_2024` long expectancy fell from `0.4357` to `0.1661`
- that means the candle sidecar is still earning its moving-part cost in the one place where `34D` originally distinguished itself from `34B`

## Execution

- both carry clones reproduced their inherited execution path cleanly
- no new alignment relaxation, governance blocking mode, or volatility overlay change was introduced
- Stage 35 is therefore a clean simplification comparison, not an execution rewrite

## Decision

- keep `34D` as the live regular operating line
- keep `35B / 34B` only as the simplification shadow reference
- do not simplify back to the governance-only line at this time

## Follow-Up Bias

- if a later stage reopens simplification, do not start with `remove the candle sidecar entirely`; Stage 35 already closed that path
- any future simplification pass should target a narrower complexity reduction than full removal of the `outside_bar` sidecar
- keep `34D` as the default reference for the next regular-stage work

## Report Refs

- `03_reviews/stage35_simplification_20260412.md`
- `03_reviews/stage35_simplification_20260412.json`
