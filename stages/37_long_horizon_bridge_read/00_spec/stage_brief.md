# Stage 37 Long-Horizon Bridge Read

- stage: `37_long_horizon_bridge_read`
- updated_on: `2026-04-12`
- current_wave: `wave1_completed`
- stage_type: `diagnostic_bridge_stage`
- inherited_regular_reference: `34D_29s_outbarlong_0001`
- inherited_regular_shadow: `34B_29s_refcarry_0001`
- bridge_window: `2024-01-01` through `2026-02-28` inclusive

## Purpose

- keep the frozen regular promotion scoreboard unchanged:
  - `hist_2024`
  - `validation`
  - `test`
- add one wider continuity read on top:
  - run the live `34D` line and the simplification shadow `34B` through one continuous account path from `2024-01-01` through `2026-02-28`
- answer a different question from Stage 35:
  - not `which split wins after resets`
  - but `does the Stage 34 candle sidecar still earn its keep when 2024 through early 2026 is one uninterrupted risk_pct equity path`

## Working Hypothesis

- Stage 35 already showed that `34B` gives back too much `hist_2024` edge after split resets
- Stage 36 then localized that edge to a small number of direct long-side suppressions
- the natural next bridge read is therefore:
  - if that older-window edge happens first in one continuous equity path, does it still matter after the later 2025 through early-2026 trade sequence compounds on top of it

## Wave 1 Run Shape

- `37A`: continuous-bridge carry of `34D`
- `37B`: continuous-bridge carry of `34B`

## Promotion Gates

- this stage is diagnostic-only; do not replace the frozen regular split scoreboard with this bridge read
- use the bridge read to judge continuity, compounding behavior, and drawdown persistence, not to erase the Stage 35 conclusion by itself
- if the bridge read reopens simplification later, it must do so by adding continuity evidence on top of Stage 35 and Stage 36, not by discarding them
