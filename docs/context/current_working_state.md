# Current Working State

- updated_on: `2026-04-09`
- active_branch: `codex/governance-stage22-ablation`
- main_base_note: `main is behind the active Stage 22 + governance line; use this note before assuming main reflects the latest decision chain`

## Read This First

1. `AGENTS.md`
2. `docs/context/stage_reporting_standard.md`
3. `docs/context/regular_experiment_roadmap_20260409.md`
4. `stages/23_state_conditioned_exit/00_spec/stage_brief.md`
5. `stages/23_state_conditioned_exit/03_reviews/review_index.md`
6. `stages/23_state_conditioned_exit/04_selected/selection_status.md`
7. `stages/22_point_exit_management/04_selected/selection_status.md`
8. `foundation/reports/governance_selected_runs_standard_20260409.md`

## Current Decisions

- Stage 23 regular incumbent: `23A_22q_base_stateexit_ref_0001`
- Stage 23 regular shadow challenger: `23C_22q_margin004_h2_risk2_0001`
- Stage 22 regular incumbent: `22Q_05dp_base_risk2_dirsplit_postcash_0001`
- Stage 22 regular shadow challenger: `22R_05dp_psl45_qtr_h3_risk2_0001`
- Stage 22 structural scout incumbent: `22A_05dp_base_hold5_0001`
- Stage 22 structural containment challenger: `22O_05dp_psl45_p10_h3_0001`
- external mismatch relaxation: `closed diagnostic branch only; do not treat as regular promotion work`

## Why This Branch Matters

- Governance telemetry and observe-only monitoring were added to the MT5 runtime and tester pipeline.
- Stage 22 point-exit runtime was restored and historical artifacts were reproduced before follow-up work continued.
- Stage 22 was re-read under `risk_pct` execution, which changed the operating judgment from the earlier fixed-lot scouting read.
- Stage 23 opened the first regular `state-conditioned exit` wave on top of `22Q`.
- The first state-exit wave kept the inherited baseline (`23A`) and promoted `23C` to shadow challenger status only.
- Selected-run governance reporting now has a richer standard report instead of the sparse legacy summary.

## Current Follow-Up Bias

- Keep `23A` as the carry-forward regular baseline.
- Keep `23C` as the first serious state-conditioned exit challenger.
- Treat `23D` as a redundancy result and `23B` as a closed diagnostic arm.
- Keep `22Q` as the source operating reference behind `23A`.
- Keep `22R` as the containment challenger worth shadowing for the Stage 22 line.
- Treat `22A` and `22O` as structural-scout context, not as the final operating scoreboard.
