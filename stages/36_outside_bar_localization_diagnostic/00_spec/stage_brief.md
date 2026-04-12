# Stage 36 Outside Bar Localization Diagnostic

- stage: `36_outside_bar_localization_diagnostic`
- updated_on: `2026-04-12`
- current_wave: `wave1_completed`
- roadmap_anchor: `diagnostic localization of why the promoted Stage 34 outside-bar sidecar still beats the governance-only simplification`
- inherited_regular_reference: `34D_29s_outbarlong_0001`
- inherited_regular_shadow: `34B_29s_refcarry_0001`
- stage35_comparison_runs: `35A_34d_refcarry_0001` vs `35B_34b_simpleref_0001`

## Purpose

- inspect the current regular operating reference:
  - `34D_29s_outbarlong_0001`
- compare it directly against the closed simplification shadow:
  - `34B_29s_refcarry_0001`
- localize whether the remaining `34D` edge is:
  - a broad distributional improvement
  - or a small number of concrete protected exits that still matter enough to keep the sidecar
- keep this stage diagnostic-only:
  - no runtime change or simplification promotion from this read alone

## Scope

- use the existing Stage 35 carry reruns only:
  - `35A_34d_refcarry_0001`
  - `35B_34b_simpleref_0001`
- work from the recorded shadow logs and trade ledgers for:
  - `validation`
  - `test`
  - `hist_2024`
- decompose the `34D minus 34B` result into:
  - direct outside-bar suppression deltas
  - shifted-entry side effects
  - propagated `risk_pct` sizing drift after balance divergence

## Evaluation Rules

- report direct suppression counts by:
  - split
  - direction
  - weekday
  - session bucket
  - decision reason at the suppressed bar
- treat the split headline delta between `35A` and `35B` as the reference scoreboard
- judge localization value by whether the sidecar edge is concentrated enough to guide any later narrowing work without reopening the closed `remove the sidecar entirely` path

## Promotion Gates

- this is a diagnostic sidecar, not a promotion stage
- only reopen runtime changes if the localization shows a clearly narrower condition than full removal and that narrower condition can preserve the direct long-side benefit
- do not simplify from this stage alone just because the value is sparse; the Stage 35 decision still stands unless a later targeted rerun proves otherwise
