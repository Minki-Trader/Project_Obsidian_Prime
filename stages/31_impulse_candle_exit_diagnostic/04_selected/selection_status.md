# Stage 31 Selection Status

- reviewed_on: `2026-04-12`
- stage: `31_impulse_candle_exit_diagnostic`
- roadmap_anchor: `extra diagnostic on large adverse candles and early exit quality in the live Stage 29 lane`
- inherited_regular_reference: `29N_25o_sxh2_0001`

## Current Read

- main_threshold: `1.50 x ATR14`
- diagnostic_decision: `impulse_state_exit_effect_is_real_but_sparse`
- keep_or_replace: `keep_29N_runtime_unchanged_treat_impulse_topic_as_sidecar_only`

## Promotion Gates

- this stage is diagnostic-only
- only reopen runtime work if a follow-up shows:
  - materially more affected `state_exit` cases than the first pass
  - a stronger and smoother counterfactual gain
  - limited added adverse excursion while holding through the impulse

## Scoreboards

- regular_risk_execution: `29N only; no new tester rerun in this stage`
- structural_scout: `not used`

## Headline

- adverse impulse exits at `1.50 x ATR14`: `71` total across `hist_2024 / validation / test`
- adverse impulse `STATE_EXIT` subset: `8 / 351` state exits, about `2.3%`
- adverse impulse `BROKER_SL` subset: `53` cases
- policy-consistent `state_exit` counterfactual: `approx +33.90`
- relaxed `+3 bar` probe: `approx +0.09`

## Risk

- the policy-consistent hold is not free:
  - validation worst added adverse excursion was about `-22.42`
  - test worst added adverse excursion was about `-6.72`
  - hist worst added adverse excursion was about `-10.06`
- read: some missed-profit cases exist, but the added pain can still be meaningful when the trade is forced to stay through the impulse

## Diagnostics

- the impulse-candle story is dominated by `BROKER_SL`, not by `STATE_EXIT_MARGIN`
- immediate rebound is not stable:
  - the short `+3 bar` relaxed probe is roughly flat overall
- the smoother positive read appears only in the narrower `remove state exit, then let normal hold-cap finish` counterfactual

## Execution

- this stage reuses existing `29N` trade ledgers and raw `US100` M5 bars
- no MT5 rerun was needed
- execution path remains the same as the current live-like Stage 29 lane

## Decision

- decision: `keep_diagnostic_only_no_live_change`
- operating_reference: `29N_25o_sxh2_0001`
- follow_up_priority: `targeted_impulse_sidecar_only_if_user_wants_deeper_drill`

## Follow-Up Bias

- do not jump straight to a broad `giant-candle neutralization` runtime fork
- if the impulse topic reopens, split the next check into:
  - `state-exit-only` impulse suppression
  - `broker-SL / stop-side` impulse sensitivity
- treat the stop-side lane as the larger quantitative story for now

## Report Refs

- `03_reviews/stage31_impulse_candle_exit_20260412.md`
- `03_reviews/stage31_impulse_candle_exit_20260412.json`
