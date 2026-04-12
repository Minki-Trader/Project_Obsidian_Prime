# Stage 36 Selection Status

- reviewed_on: `2026-04-12`
- stage: `36_outside_bar_localization_diagnostic`
- roadmap_anchor: `diagnostic localization of why the promoted Stage 34 outside-bar sidecar still beats the governance-only simplification`
- inherited_regular_reference: `34D_29s_outbarlong_0001`
- inherited_regular_shadow: `34B_29s_refcarry_0001`

## Current Read

- localization_decision: `34D_edge_is_sparse_long_state_exit_protection_not_broad_systemic_drift`
- keep_or_replace: `keep_34D_runtime_unchanged_treat_outside_bar_value_as_targeted_long_exit_protection`
- main_localization: `the remaining edge comes from a few direct long suppressions, mostly in hist_2024, with zero qualifying test-window events`

## Promotion Gates

- this stage is diagnostic-only
- only reopen runtime changes if a later narrowing pass can preserve the direct long-side benefit without recreating the closed `remove the sidecar entirely` simplification loss
- do not infer that sparse value means removable value; Stage 35 already proved full removal is too blunt

## Scoreboards

- regular_risk_execution: `Stage 35 carry reruns only; no new MT5 rerun in this stage`
- structural_scout: `not used`

## Headline

- `35A minus 35B` net delta:
  - validation: `-0.05`
  - test: `0.00`
  - hist_2024: `+36.37`
- direct outside-bar suppressions:
  - validation: `2` events, direct net `-0.80`
  - test: `0` events, direct net `0.00`
  - hist_2024: `5` events, direct net `+34.86`

## Risk

- the sidecar value is sparse, so blanket simplification remains risky even though the current test window is unaffected
- Stage 36 also shows that the sidecar is not universally positive on every single trigger:
  - `2` of the `7` direct events were net negative
- that means any future narrowing pass must be precise; naive removal or naive broadening both remain unattractive

## Diagnostics

- all `7` direct events were `LONG`
- all `7` held the position exactly `1` extra bar
- later close shape:
  - `5` still closed as `STATE_EXIT_MARGIN`
  - `2` aged into `TIME_EXIT_NY_POSTCASH`
- suppression context at the blocked exit bar:
  - `DUAL_SIGNAL_TIE_OR_MARGIN_FAIL`: `4`
  - `LONG_MARGIN_FAIL`: `3`
- the older-window edge is therefore mostly a small cluster of long no-entry exits that were better served by waiting one more bar

## Execution

- this stage reuses the recorded Stage 35 shadow logs and trade ledgers
- no new bundle build, runtime compile, or MT5 tester rerun was required
- the residual delta outside the direct events is mostly propagated `risk_pct` carry drift after balance divergence, not a second independent mechanism

## Decision

- keep `34D_29s_outbarlong_0001` as the live regular lane
- keep `34B_29s_refcarry_0001` as the simplification shadow only
- treat Stage 36 as a localization map for later narrowing work, not as a simplification approval

## Follow-Up Bias

- if simplification reopens, do not start from full sidecar removal; Stage 35 and Stage 36 together have already closed that path
- keep the topic `long-only` first; Stage 36 found no reason to broaden into a short-side story
- if a later narrowing pass is needed, start from the sparse long `no entry / weak margin` subset and verify it with a fresh targeted rerun
- do not narrow by weekday alone; the positive and negative direct events are mixed across Monday, midweek, and Thursday cases

## Report Refs

- `03_reviews/stage36_outside_bar_localization_20260412.md`
- `03_reviews/stage36_outside_bar_localization_20260412.json`
