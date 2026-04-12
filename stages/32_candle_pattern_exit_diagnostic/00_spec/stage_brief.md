# Stage 32 Candle Pattern Exit Diagnostic

- stage: `32_candle_pattern_exit_diagnostic`
- updated_on: `2026-04-12`
- current_wave: `wave1_completed`
- roadmap_anchor: `extra diagnostic on unmodeled candle morphology around exits in the live Stage 29 lane`

## Purpose

- inspect the current regular operating reference:
  - `29N_25o_sxh2_0001`
- test whether candle shapes not explicitly modeled in the current feature set show a stronger exit-quality story than the broad impulse-body read from Stage 31
- keep this stage diagnostic-only:
  - no runtime or model promotion from this read alone

## Scope

- use the existing `29N` trade ledgers plus raw `US100` M5 bars
- test three candle patterns that are not explicit current features:
  - `outside_adverse_bar`
  - `rejection_tail`
  - `wide_range_doji`
- for each pattern, measure:
  - total exit concentration
  - `STATE_EXIT` concentration
  - `BROKER_SL` concentration
  - `state_exit` counterfactual under policy-consistent hold

## Pattern Definitions

- `outside_adverse_bar`
  - exit bar closes against the position and its high/low both exceed the previous bar range
- `rejection_tail`
  - exit bar closes against the position, has a long wick in the position-favorable direction, and has at least moderate ATR-scaled range
- `wide_range_doji`
  - very small body, wide total range, and high ATR-scaled range

## Evaluation Rules

- keep the split read on:
  - `hist_2024`
  - `validation`
  - `test`
- use the same policy-consistent hold counterfactual as Stage 31:
  - remove the state exit only
  - let the normal hold-cap logic decide the later close
- judge follow-up value by:
  - pattern frequency
  - state-exit specificity
  - sign and stability of the policy-hold counterfactual

## Promotion Gates

- this is a diagnostic sidecar, not a promotion stage
- only reopen runtime work if one candle pattern shows:
  - enough `state_exit` cases to matter
  - a positive counterfactual that is not purely hist-heavy noise
  - a cleaner read than the Stage 31 broad impulse-body story
