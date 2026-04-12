# Stage 31 Impulse Candle Exit Diagnostic

- stage: `31_impulse_candle_exit_diagnostic`
- updated_on: `2026-04-12`
- current_wave: `wave1_completed`
- roadmap_anchor: `extra diagnostic on whether large adverse candles are triggering costly early exits in the live Stage 29 lane`

## Purpose

- inspect the current regular operating reference:
  - `29N_25o_sxh2_0001`
- test the user's extra hypothesis:
  - `if the large opposite-direction candle had not appeared, would the trade have stayed open and avoided a bad early exit`
- keep this stage diagnostic-only:
  - do not promote any runtime change directly from this read
  - first measure whether the effect is real, large enough, and concentrated in `state_exit` rather than elsewhere

## Scope

- use the existing `29N` trade ledgers plus raw `US100` M5 bars
- define an impulse candle as a bar whose real body is large relative to trailing `ATR14`
- focus the main read on:
  - `STATE_EXIT_MARGIN` trades closed on an adverse impulse bar
- keep two counterfactual reads:
  - `policy_consistent_hold`: remove the state exit only, then let the normal Stage 29 time-exit / pocket hold-cap finish the trade
  - `probe_plus_3_bars`: purely diagnostic relaxed hold for three extra bars after the actual exit

## Evaluation Rules

- report counts for impulse thresholds:
  - `1.25 x ATR14`
  - `1.50 x ATR14`
  - `2.00 x ATR14`
- treat `1.50 x ATR14` as the main threshold for the headline read
- keep the split read on:
  - `hist_2024`
  - `validation`
  - `test`
- report both:
  - how often adverse impulse exits happen
  - whether those exits were actually saving loss or cutting recoverable trades too early

## Promotion Gates

- this is a diagnostic sidecar, not a promotion stage
- only reopen the EA/runtime path if the diagnostic shows:
  - enough adverse impulse `state_exit` cases to matter
  - a clear positive counterfactual read under the policy-consistent hold
  - limited added adverse excursion from holding through the impulse
