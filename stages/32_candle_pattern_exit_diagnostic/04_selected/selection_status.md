# Stage 32 Selection Status

- reviewed_on: `2026-04-12`
- stage: `32_candle_pattern_exit_diagnostic`
- roadmap_anchor: `extra diagnostic on unmodeled candle morphology around exits in the live Stage 29 lane`
- inherited_regular_reference: `29N_25o_sxh2_0001`

## Current Read

- best_candidate_pattern: `outside_adverse_bar`
- diagnostic_decision: `outside_bar_is_the_only_candle_shape_with_clear_followup_value`
- keep_or_replace: `keep_29N_runtime_unchanged_treat_candle_shape_topic_as_targeted_sidecar_only`

## Promotion Gates

- this stage is diagnostic-only
- only reopen runtime work if the selected candle shape:
  - still looks positive under a more targeted follow-up
  - is not validation- or hist-only noise
  - beats the Stage 31 broad impulse-body read on specificity

## Scoreboards

- regular_risk_execution: `29N only; no new tester rerun in this stage`
- structural_scout: `not used`

## Headline

- `outside_adverse_bar`: `45` total exits, `15` state exits, `7` broker SL, policy-hold state-exit delta `approx +72.11`
- `rejection_tail`: `32` total exits, `9` state exits, `12` broker SL, policy-hold state-exit delta `approx +48.37` but split stability is weak
- `wide_range_doji`: `54` total exits, `19` state exits, `14` broker SL, policy-hold state-exit delta `approx -11.10`

## Risk

- `outside_adverse_bar` is the cleanest balance of:
  - enough state-exit cases to matter
  - a positive counterfactual
  - less obvious split instability than the other new patterns
- `rejection_tail` is too unstable:
  - strong on `hist_2024`
  - negative on `validation`
- `wide_range_doji` is not attractive as a runtime sidecar:
  - it fires often
  - but the state-exit counterfactual is net negative

## Diagnostics

- the new candle-shape pass is more useful than the broad Stage 31 body-only pass
- among unmodeled candle morphologies, `outside_adverse_bar` is the first one worth a targeted second pass
- the pattern story is still mixed with stop-side behavior, so this is not yet a promotion lane

## Execution

- this stage reuses existing `29N` trade ledgers and raw `US100` M5 bars
- no MT5 rerun was needed
- execution path remains the same as the current live-like Stage 29 lane

## Decision

- decision: `keep_diagnostic_only_reopen_only_outside_bar_if_needed`
- operating_reference: `29N_25o_sxh2_0001`
- follow_up_priority: `outside_bar_sidecar_only`

## Follow-Up Bias

- if the candle-shape topic reopens, start with:
  - `outside_adverse_bar` only
- do not spend follow-up time on:
  - `wide_range_doji`
- treat `rejection_tail` as an optional later check, not the first reopen

## Report Refs

- `03_reviews/stage32_candle_pattern_exit_20260412.md`
- `03_reviews/stage32_candle_pattern_exit_20260412.json`
