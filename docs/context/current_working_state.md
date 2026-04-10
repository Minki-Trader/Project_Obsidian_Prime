# Current Working State

- updated_on: `2026-04-10`
- active_branch: `work`
- main_base_note: `main is behind the active Stage 22 + governance line; use this note before assuming main reflects the latest decision chain`

## Read This First

1. `AGENTS.md`
2. `docs/context/stage_reporting_standard.md`
3. `docs/context/regular_experiment_roadmap_20260409.md`
4. `stages/28_retrain_feature_checks/00_spec/stage_brief.md`
5. `stages/28_retrain_feature_checks/03_reviews/review_index.md`
6. `stages/28_retrain_feature_checks/04_selected/selection_status.md`
7. `stages/27_vol_adaptive_overlay/04_selected/selection_status.md`
8. `stages/26_gov_adaptive_overlay/04_selected/selection_status.md`
9. `stages/25_soft_contextual_control/04_selected/selection_status.md`
10. `foundation/reports/governance_selected_runs_standard_20260409.md`

## Current Decisions

- Stage 28 current wave: `event_triggered_retrain_wave1`
- Stage 28 lineage full-reference rebuild: `28A_18e_full54_ph20_0001`
- Stage 28 best lineage compact arm: `28B_18e_persist48_ph20_0001`
- Stage 28 stitched fixed-carry reference: `28E_28b_fixedcarry_long14m_0001`
- Stage 28 stitched shadow candidate: `28G_28b_negpf_trigger_long14m_0001`
- Stage 28 lineage decision: `keep_fixed_carry_reference`
- current regular operating reference remains: `27A_26a_volref_0001`
- Stage 27 regular incumbent: `27A_26a_volref_0001`
- Stage 27 regular shadow challenger: `27D_26a_vl110h085_0001`
- Stage 26 regular incumbent seed behind Stage 27: `26A_25d_govref_0001`
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
- Stage 27 reused the EA's ATR14/ATR50 regime ratio as a volatility-aware risk overlay and kept the inherited baseline (`27A`) while promoting `27D` only to shadow challenger status.
- Stage 28 reopened the `17E/18E` lineage only as a bounded feature-simplification check and found that the `28B` persistence-only compact fork beat the rebuilt `28A` full-reference arm on both validation and OOS.
- Stage 28 wave 2 then tested month-level retrain logic on that reopened compact lineage and found that both blind monthly retrain (`28F`) and bounded event-trigger retrain (`28G`) underperformed the fixed-carry compact read (`28E`).
- Selected-run governance reporting now has a richer standard report instead of the sparse legacy summary.

## Current Follow-Up Bias

- keep `27A` as the live regular lane even after Stage 28; the lineage work still did not open a direct operating replacement
- treat `28E` as the internal long-window reference for the reopened compact lineage; if the `18E` branch is revisited, start from fixed carry rather than from monthly retrain
- close the broad `28F/28G` retrain lane for now; neither blind monthly retrain nor the first event-trigger variant added value on top of compact `28B`
- keep `28B` as the compact feature proof, not as a live regular promotion claim
- treat `28D` as a misleading hist-heavy read; it looked strong on `hist_2024` but collapsed on validation and did not earn follow-up priority
- keep `27A` as the carry-forward regular baseline; the volatility-adaptive wave improved containment but gave up too much headline return to justify promotion
- treat `27D` as the best Stage 27 internal arm; it was the least bad two-sided bucket but still cost too much non-OOS and OOS headline return
- treat `27B` as the clearest high-vol containment read; it reduced DD the most, but the headline sacrifice was too large for the regular lane
- keep `26A` as the pre-Stage-27 operating seed; the governance-led wave did not show a large enough overlay gain to justify immediate promotion
- treat `26C` as the best Stage 26 internal arm; the external skip taper produced a small positive read across windows but the edge was too small to count as a true incumbent replacement
- treat `26B` as an over-strong signal taper; it improved containment but starved too much headline return
- keep `25D` as the pre-Stage-26 operating seed; it improved the regular OOS headline and cleaned up both weak short pockets
- treat `25C` as the best non-promoted Stage 25 internal arm; it helped the postcash short pocket but did less overall than `25D`
- keep `24A` as the inherited pre-Stage-25 reference; the gated specialist line remains closed diagnostic context only
- treat Stage 28 event-trigger retrain as completed for wave 1; only reopen it if a stronger trigger hypothesis appears
- keep `23A` as the carry-forward regular baseline
- keep `23C` as the first serious state-conditioned exit challenger
- treat `23D` as a redundancy result and `23B` as a closed diagnostic arm
- keep `22Q` as the source operating reference behind `23A`
- keep `22R` as the containment challenger worth shadowing for the Stage 22 line
- treat `22A` and `22O` as structural-scout context, not as the final operating scoreboard
