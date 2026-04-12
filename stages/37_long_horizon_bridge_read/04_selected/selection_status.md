# Stage 37 Selection Status

- reviewed_on: `2026-04-12`
- stage: `37_long_horizon_bridge_read`
- stage_type: `diagnostic_bridge_stage`
- inherited_regular_reference: `34D_29s_outbarlong_0001`
- inherited_regular_shadow: `34B_29s_refcarry_0001`

## Current Read

- verified_bridge_reference: `37A_34d_bridge_0001`
- bridge_simplification_shadow: `37B_34b_bridge_0001`
- continuity_decision: `continuous_bridge_still_prefers_34D_over_34B`

## Promotion Gates

- this stage is diagnostic-only and does not replace the frozen `hist_2024 / validation / test` scoreboard
- treat the bridge read as continuity evidence for compounding and drawdown persistence
- do not reopen blanket simplification unless a later targeted rerun beats both the frozen split scoreboard and this continuous bridge read

## Scoreboards

- regular_risk_execution: `active as a continuous bridge read only`
- structural_scout: `not used`

## Headline

- continuous bridge window: `2024-01-01` through `2026-02-28` inclusive
- `37A / 34D`: `net=3677.68` `return_pct=735.536` `pf=1.4748` `trades=1035`
- `37B / 34B`: `net=3548.04` `return_pct=709.608` `pf=1.4733` `trades=1035`
- `37A minus 37B`: `net=+129.64` `return_pct=+25.928` `pf=+0.0015`
- calendar contribution deltas:
  - `2024`: `+34.50`
  - `2025`: `+43.65`
  - `2026_ytd`: `+51.49`

## Risk

- `34D` kept the bridge lead with only a tiny stress tax:
  - bridge DD delta: `+0.0319`
  - ulcer delta: `+0.0622`
  - worst-week delta: about `-14.58`
- that means the simplification shadow did not buy a meaningful enough bridge-risk improvement to offset the continuity headline loss

## Diagnostics

- the continuity edge was not just a `2024` artifact:
  - all three calendar slices stayed positive for `34D`
- expectancy stayed better on both sides:
  - long expectancy delta: about `+0.1379`
  - short expectancy delta: about `+0.1138`
- same trade count with a higher total net means the bridge read is about trade quality and compounding path, not about a broader trade-frequency difference

## Execution

- external mismatch pressure and no-trade rate were effectively unchanged between the two runs
- this bridge read therefore isolates strategy-path continuity rather than any new data-alignment or governance-mode change
- the bridge used one uninterrupted `risk_pct` account path, so the positive `2024` difference was allowed to carry into later position sizing instead of being reset away

## Decision

- keep `34D_29s_outbarlong_0001` as the live regular lane
- keep `34B_29s_refcarry_0001` as the simplification shadow only
- treat Stage 37 as continuity confirmation that strengthens the earlier Stage 35 and Stage 36 anti-simplification read

## Follow-Up Bias

- if we want a broader continuity read again, add segmented bridge diagnostics rather than reopening full sidecar removal
- if simplification reopens later, target a narrower long-side subset and force it to beat:
  - the frozen split scoreboard
  - the Stage 36 localization read
  - this Stage 37 continuous bridge read
- do not assume that a simplification that nearly ties on reset windows will stay near-tied once 2024 through early 2026 compounds continuously

## Report Refs

- `03_reviews/stage37_bridge_20260412.md`
- `03_reviews/stage37_bridge_20260412.json`
