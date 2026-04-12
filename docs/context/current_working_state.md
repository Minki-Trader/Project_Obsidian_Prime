# Current Working State

- updated_on: `2026-04-12`
- active_branch: `codex/governance-stage22-ablation`
- main_base_note: `main is behind the active Stage 22 + governance line; use this note before assuming main reflects the latest decision chain`

## Read This First

1. `AGENTS.md`
2. `docs/context/stage_reporting_standard.md`
3. `docs/context/regular_experiment_roadmap_20260409.md`
4. `stages/34_outside_bar_mainline_promotion/00_spec/stage_brief.md`
5. `stages/34_outside_bar_mainline_promotion/03_reviews/review_index.md`
6. `stages/34_outside_bar_mainline_promotion/04_selected/selection_status.md`
7. `stages/33_outside_bar_state_exit_followup/00_spec/stage_brief.md`
8. `stages/33_outside_bar_state_exit_followup/03_reviews/review_index.md`
9. `stages/33_outside_bar_state_exit_followup/04_selected/selection_status.md`
10. `stages/32_candle_pattern_exit_diagnostic/00_spec/stage_brief.md`
11. `stages/32_candle_pattern_exit_diagnostic/03_reviews/review_index.md`
12. `stages/32_candle_pattern_exit_diagnostic/04_selected/selection_status.md`
13. `stages/31_impulse_candle_exit_diagnostic/00_spec/stage_brief.md`
14. `stages/31_impulse_candle_exit_diagnostic/03_reviews/review_index.md`
15. `stages/31_impulse_candle_exit_diagnostic/04_selected/selection_status.md`
16. `stages/30_macro_mismatch_root_cause/00_spec/stage_brief.md`
17. `stages/30_macro_mismatch_root_cause/03_reviews/review_index.md`
18. `stages/30_macro_mismatch_root_cause/04_selected/selection_status.md`
19. `docs/context/stage23_27_wave2_crosssplit_synthesis_20260412.md`
20. `stages/29_fusion_long_repair/00_spec/stage_brief.md`
21. `stages/29_fusion_long_repair/03_reviews/review_index.md`
22. `stages/29_fusion_long_repair/04_selected/selection_status.md`
23. `stages/28_retrain_feature_checks/00_spec/stage_brief.md`
24. `stages/28_retrain_feature_checks/03_reviews/review_index.md`
25. `stages/28_retrain_feature_checks/04_selected/selection_status.md`
26. `stages/27_vol_adaptive_overlay/04_selected/selection_status.md`
27. `stages/26_gov_adaptive_overlay/04_selected/selection_status.md`
28. `stages/25_soft_contextual_control/04_selected/selection_status.md`
29. `foundation/reports/governance_selected_runs_standard_20260409.md`

## Current Decisions

- Stage 34 mainline status: `wave1_completed`
- Stage 34 new regular incumbent: `34D_29s_outbarlong_0001`
- Stage 34 new regular shadow: `34B_29s_refcarry_0001`
- Stage 34 decomposition reference: `34C_29n_outbarlong_0001`
- Stage 34 mainline decision: `promote_34D_over_29N_and_29S`
- Stage 34 promotion read: `29S governance carry plus long-only outside-bar suppression is the first clean regular-stage upgrade beyond 29N`
- Stage 33 follow-up status: `wave1_completed`
- Stage 33 carry check: `33A_29n_refcarry_0001`
- Stage 33 best new candidate: `33C_29n_outbar_long_0001`
- Stage 33 broader near-tie: `33B_29n_outbar_both_0001`
- Stage 33 decision: `keep_29N_live_record_33C_as_targeted_shadow_only`
- Stage 33 runtime read: `outside adverse bar suppression has real older-window value, but the clean answer is long-only and not yet a live replacement`
- Stage 29 current wave: `wave3_h2_refinement_completed`
- Stage 29 balanced incumbent: `29N_25o_sxh2_0001`
- Stage 29 regular shadow challenger: `29S_25o_sxh2_gweak_0001`
- Stage 29 best recent-window arm: `29W_25o_sxdirls_gweak_0001`
- Stage 29 best Wave 3 close call: `29AC_25o_sxh2_lock1_gweak_0001`
- Stage 32 diagnostic status: `wave1_completed`
- Stage 32 diagnostic decision: `outside_adverse_bar_is_the_only_candle_shape_with_clear_followup_value`
- Stage 32 candle-shape read: `outside adverse bar is cleaner than broad impulse-body suppression, rejection tail is unstable, wide-range doji is unattractive`
- Stage 31 diagnostic status: `wave1_completed`
- Stage 31 diagnostic decision: `impulse_state_exit_effect_is_real_but_sparse`
- Stage 31 impulse read: `adverse impulse candles are far more concentrated in broker SL than in state exit`
- Stage 31 counterfactual read: `main-threshold state-exit subset is mildly positive under policy-consistent hold, but too sparse for a broad runtime fork`
- Stage 30 diagnostic status: `wave1_completed`
- Stage 30 diagnostic decision: `keep exact alignment + all-or-skip`
- Stage 30 macro pressure read: `VIX sparse-feed holes dominate hist_2024 / validation, US10YR date-local clusters dominate test`
- Stage 30 stale1 recovery read: `symbol-specific only; VIX about 0.32, US10YR about 0.58, AAPL.xnas / USDX structural`
- current regular operating reference is now: `34D_29s_outbarlong_0001`
- prior regular operating reference before Stage 34: `29N_25o_sxh2_0001`
- prior Stage 29 wave1 incumbent: `29A_25o_refcarry_0001`
- prior live regular reference before Stage 29: `27A_26a_volref_0001`
- Stage 28 current wave: `event_triggered_retrain_wave1`
- Stage 28 lineage full-reference rebuild: `28A_18e_full54_ph20_0001`
- Stage 28 best lineage compact arm: `28B_18e_persist48_ph20_0001`
- Stage 28 stitched fixed-carry reference: `28E_28b_fixedcarry_long14m_0001`
- Stage 28 stitched shadow candidate: `28G_28b_negpf_trigger_long14m_0001`
- Stage 28 lineage decision: `keep_fixed_carry_reference`
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

- Stage 34 then brought the Stage 33 extra finding back into the regular alpha lane and tested it directly against the active `29N / 29S` mainline.
- That Stage 34 read showed that the `33C` candle-sidecar survives regular-stage scrutiny:
  - `34C` improved `hist_2024` strongly while preserving the current `test` window
  - `34B` preserved the older `29S` governance-shadow current-window edge
  - `34D` combined both stories cleanly
- The same Stage 34 read promoted `34D` over both prior mainline references:
  - versus `29N`, it improved `validation`, `test`, and `hist_2024`
  - versus `29S`, it held the same current-window shape while materially improving `hist_2024`
- That makes `34D` the first regular-stage promotion built from a formerly extra-only candle-shape idea.
- Stage 33 then converted the Stage 32 candle-shape diagnosis into a real MT5 runtime follow-up on top of `29N`.
- That Stage 33 read first reran a direct carry clone (`33A`) and matched `29N` exactly, which confirmed the EA-side outside-bar suppressor path did not create a hidden regression.
- The same Stage 33 read then showed that targeted `outside adverse bar -> suppress STATE_EXIT_MARGIN` logic does have runtime value:
  - the long-only arm `33C` preserved the current `test` window exactly
  - validation stayed almost flat
  - `hist_2024` improved from `39.368` to `45.816`
- The broader `33B` both-direction arm was a near-tie on headline, but it depended on more short-side suppressions than the diagnostic story really justified.
- Stage 33 also showed what not to do:
  - short-only `33D` weakened the older-window headline
  - the first ATR-floor arms `33E / 33F` overfiltered validation without producing a cleaner overall answer
- Stage 23 through Stage 27 received a broad local-plus-expansion follow-up sweep, and that synthesis identified `25O` as the best carry reference for a focused fusion stage.
- Stage 29 then converted that broad sweep into a bounded fusion wave and gave the `25O` family a full `hist_2024 / validation / test` read.
- That full Stage 29 read promoted plain `29A` over the older live `27A` lane.
- Stage 29 wave 2 then isolated the `23G`-style state-exit family and found that slower `h2` state exit (`29N`) is the balanced answer: it improved `hist_2024` and `test` together, unlike the earlier aggressive `h1` variants.
- the governance-assisted `29S` variant stayed close enough to shadow, while the aggressive `29W` read became the best pure recent-window arm without clearing the older-window check.
- Stage 29 wave 3 then tested the most natural local refinements around that `h2` backbone and found no stronger balanced replacement; `29AC` was the closest new arm, but still weaker than `29N/29S` on the full read.
- Stage 32 then extended the extra diagnostic lane from broad impulse bodies to candle morphology not explicitly modeled in the current feature set.
- That Stage 32 read showed `outside_adverse_bar` as the first candle-shape sidecar worth keeping in mind: it had `45` total exits, `15` state exits, and about `+72.11` on the policy-consistent state-exit counterfactual.
- The same Stage 32 read showed `rejection_tail` as split-unstable and `wide_range_doji` as a poor runtime candidate despite firing often.
- Stage 31 then opened a separate extra diagnostic on top of `29N` to test the user's large-candle intuition without touching the live runtime.
- That Stage 31 read showed that adverse impulse exits do exist, but only a small slice of them are `STATE_EXIT_MARGIN`; the larger concentration is currently in `BROKER_SL`.
- The same Stage 31 read showed a mildly positive `state_exit` counterfactual when the strategy is allowed to finish under its normal hold-cap, but the sample is too sparse and the added excursion too real to justify immediate broad candle-neutralization work.
- Stage 30 then converted the roadmap's macro-mismatch sidecar into a concrete source audit on top of `29N`, using both the runtime shadow logs and the raw M5 source bars.
- That Stage 30 audit showed `VIX` as the dominant sparse-feed problem on `hist_2024` and `validation`, while `US10YR` becomes the main macro pressure on the current `test` window through date-local clusters.
- The same Stage 30 audit showed that `AAPL.xnas` and `USDX` are structural session-shape controls, not evidence for a broad macro stale-fallback story.
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

- keep `34D` as the live regular lane; it is now the strongest balanced operating answer
- keep `34B` as the main regular shadow because it isolates the governance-only line behind the new incumbent
- keep `34C` as the candle-sidecar decomposition reference; it proved value but is not the preferred operating mix by itself
- if the outside-bar topic reopens inside the regular lane, keep it long-only first
- if a simplification pass is needed later, compare `34D` against `34B` before removing the candle-sidecar
- if the outside-bar topic reopens, start from `33C` long-only without the ATR floor
- treat `33B` as the broader near-tie, not as the default reopen point
- close short-only outside-bar suppression for now; `33D` failed the older-window headline check
- close the first ATR-floor local variants for now; they bought less than the validation tax they introduced
- keep `exact alignment + all-or-skip` as the live contract; Stage 30 did not justify reopening broad stale fallback
- if the candle-shape topic reopens, start with `outside_adverse_bar` only; Stage 32 made it the first non-modeled candle shape with real follow-up value
- do not spend follow-up time on `wide_range_doji`; Stage 32 showed frequent triggers but a negative state-exit counterfactual
- keep `rejection_tail` as optional later context only; it stayed too unstable across splits
- keep the large-candle idea in diagnostic mode for now; Stage 31 did not justify a broad `giant-candle neutralization` runtime fork
- if the impulse topic reopens, split it into `state-exit-only` suppression versus stop-side sensitivity, because the current larger concentration is in `BROKER_SL`
- if the mismatch topic reopens, keep it as a symbol-specific macro feed-health diagnostic rather than a whole-workspace execution change
- keep `AAPL.xnas` and `USDX` out of any future macro stale-fallback story; they are structural controls, not the root-cause target
- keep `29N` as the live regular lane; it is the first Stage 29 state-exit fusion that cleared both the recent-window and older-window checks
- treat `29S` as the closest balanced shadow, not as an urgent replacement
- treat `29W` and `29T` as diagnostic high-upside templates only if a later wave can recover their `hist_2024` tax
- treat `29AC` as the best local `h2` refinement close call, but not as a real promotion threat
- close the current short-only state-exit lane as a live-candidate path; it preserves older carry but leaves too much newer-window upside on the table
- close the current explicit Stage 29 long-repair recipe; it did not solve the long-side problem robustly
- close the local `h2` refinement lane for now; a future Stage 29 reopen should require a clearly different hypothesis
- treat `28E` as the internal long-window reference for the reopened compact lineage; if the `18E` branch is revisited, start from fixed carry rather than from monthly retrain
- close the broad `28F/28G` retrain lane for now; neither blind monthly retrain nor the first event-trigger variant added value on top of compact `28B`
- keep `28B` as the compact feature proof, not as a live regular promotion claim
- treat `28D` as a misleading hist-heavy read; it looked strong on `hist_2024` but collapsed on validation and did not earn follow-up priority
- treat `27A` as the previous regular baseline that carried forward through Stages 27 and 28 before Stage 29 replaced it
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
