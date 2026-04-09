# Current Working State

- updated_on: `2026-04-09`
- active_branch: `codex/governance-stage22-ablation`
- main_base_note: `main is behind the active Stage 22 + governance line; use this note before assuming main reflects the latest decision chain`

## Read This First

1. `AGENTS.md`
2. `docs/context/stage_reporting_standard.md`
3. `docs/context/regular_experiment_roadmap_20260409.md`
4. `stages/26_gov_adaptive_overlay/00_spec/stage_brief.md`
5. `stages/26_gov_adaptive_overlay/03_reviews/review_index.md`
6. `stages/26_gov_adaptive_overlay/04_selected/selection_status.md`
7. `stages/25_soft_contextual_control/04_selected/selection_status.md`
8. `stages/24_gated_specialist_overlay/04_selected/selection_status.md`
9. `stages/23_state_conditioned_exit/04_selected/selection_status.md`
10. `foundation/reports/governance_selected_runs_standard_20260409.md`

## Current Decisions

- Stage 26 regular incumbent: `26A_25d_govref_0001`
- Stage 26 regular shadow challenger: `26C_25d_gext085_0001`
- Stage 25 regular incumbent seed behind Stage 26: `25D_24a_monpost_t050_m030_psh2_0001`
- Stage 25 best internal non-promoted arm: `25C_24a_postshort_t050_m030_0001`
- Stage 24 regular incumbent: `24A_23a_base_gate_ref_0001`
- Stage 24 best internal gate arm: `24B_23a_17csg040_gate_0001`
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
- Stage 24 opened the `17C short specialist as gate` retry and kept the inherited baseline (`24A`); the gate arms improved some non-OOS reads but materially hurt the regular OOS window.
- Stage 25 converted the next roadmap item into a soft contextual short cleanup wave and promoted `25D` over the inherited `24A` baseline.
- Stage 26 turned governance telemetry into non-blocking risk tapers and kept the observe-only baseline (`26A`) while promoting `26C` only to shadow challenger status.
- Selected-run governance reporting now has a richer standard report instead of the sparse legacy summary.

## Current Follow-Up Bias

- keep `26A` as the carry-forward regular baseline; the governance-led wave did not show a large enough overlay gain to justify immediate promotion
- treat `26C` as the best Stage 26 internal arm; the external skip taper produced a small positive read across windows but the edge was too small to count as a true incumbent replacement
- treat `26B` as an over-strong signal taper; it improved containment but starved too much headline return
- keep `25D` as the pre-Stage-26 operating seed; it improved the regular OOS headline and cleaned up both weak short pockets
- treat `25C` as the best non-promoted Stage 25 internal arm; it helped the postcash short pocket but did less overall than `25D`
- keep `24A` as the inherited pre-Stage-25 reference; the gated specialist line remains closed diagnostic context only
- move the roadmap forward to Stage 27 rather than widening the Stage 26 governance sweep immediately
- Keep `23A` as the carry-forward regular baseline.
- Keep `23C` as the first serious state-conditioned exit challenger.
- Treat `23D` as a redundancy result and `23B` as a closed diagnostic arm.
- Keep `22Q` as the source operating reference behind `23A`.
- Keep `22R` as the containment challenger worth shadowing for the Stage 22 line.
- Treat `22A` and `22O` as structural-scout context, not as the final operating scoreboard.
