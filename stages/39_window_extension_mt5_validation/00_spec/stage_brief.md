# Stage 39 Window Extension MT5 Validation

- stage: `39_window_extension_mt5_validation`
- updated_on: `2026-04-13`
- current_wave: `wave1_completed`
- stage_type: `diagnostic_runtime_validation_stage`
- inherited_regular_reference: `34D_29s_outbarlong_0001`
- inherited_regular_shadow: `34B_29s_refcarry_0001`
- source_comparison_runs:
  - `35A_34d_refcarry_0001`
  - `35B_34b_simpleref_0001`
- extended_common_window:
  - `start`: `2022-08-01`
  - `end_inclusive`: `2026-04-12`
  - `end_exclusive_utc`: `2026-04-13T00:00:00Z`

## Purpose

- extend the shared raw-bar and feature window from the older `2026-02-28` cutoff to the latest safe closed-bar day under the current date
- rerun the key `34D` versus `34B` continuity comparison through the extended window using MT5 tester execution
- add one fresh latest-window MT5 shadow run so pre-live parity work can point at current-date runtime logs instead of only older handoff artifacts

## Scope

- export the required `M5` raw bars through `2026-04-13T00:00:00Z` exclusive
- rebuild the shared intersection and feature dataset on that extended window
- create fresh Stage 39 carry bundles from the Stage 35 comparison pair
- run:
  - one extended continuous bridge for `34D`
  - one extended continuous bridge for `34B`
  - one latest-window `34D` shadow/parity audit slice

## Evaluation Rules

- treat the historical Stage 35 through Stage 37 chain as the baseline and ask only whether the latest-window extension changes the continuity story materially
- keep the frozen regular split scoreboard intact; this stage adds an extended continuity and runtime-audit read on top
- for the latest-window parity slice, record current-date MT5 runtime behavior even if exact Python proxy parity still fails

## Promotion Gates

- this stage is diagnostic-only
- do not use this stage alone to reopen blanket simplification or broad retraining
- use it to answer two practical pre-live questions:
  - does `34D` still stay ahead once the bridge is extended to the latest closed-bar day
  - do we have fresh MT5 runtime logs on the extended window for the next parity audit pass

## Wave 1 Outcome

- the shared raw-bar, intersection, and feature window is now extended through `2026-04-12` inclusive
- the MT5-driven extended bridge still prefers `34D` over `34B`
- a fresh latest-window `34D` shadow audit now exists on `2026-03-01` through `2026-04-12`, but exact Python-to-MT5 checksum parity remains open
