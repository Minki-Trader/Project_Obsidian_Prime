# Current Working State

- updated_on: `2026-04-13`
- active_branch: `main`
- main_base_note: `main now includes the Stage 22 through Stage 39 chain; Stage 38 broadened the pre-live evidence pack and Stage 39 extended the shared window plus reopened a fresh MT5 parity surface`

## Read This First

1. `AGENTS.md`
2. `docs/context/stage_reporting_standard.md`
3. `docs/context/regular_experiment_roadmap_20260409.md`
4. `stages/39_window_extension_mt5_validation/00_spec/stage_brief.md`
5. `stages/39_window_extension_mt5_validation/03_reviews/review_index.md`
6. `stages/39_window_extension_mt5_validation/04_selected/selection_status.md`
7. `stages/38_prelive_evidence_pack/00_spec/stage_brief.md`
8. `stages/38_prelive_evidence_pack/03_reviews/review_index.md`
9. `stages/38_prelive_evidence_pack/04_selected/selection_status.md`
10. `stages/37_long_horizon_bridge_read/00_spec/stage_brief.md`
11. `stages/37_long_horizon_bridge_read/03_reviews/review_index.md`
12. `stages/37_long_horizon_bridge_read/04_selected/selection_status.md`
13. `stages/36_outside_bar_localization_diagnostic/00_spec/stage_brief.md`
14. `stages/36_outside_bar_localization_diagnostic/03_reviews/review_index.md`
15. `stages/36_outside_bar_localization_diagnostic/04_selected/selection_status.md`
16. `stages/35_candle_sidecar_simplification_check/00_spec/stage_brief.md`
17. `stages/35_candle_sidecar_simplification_check/03_reviews/review_index.md`
18. `stages/35_candle_sidecar_simplification_check/04_selected/selection_status.md`
19. `stages/34_outside_bar_mainline_promotion/00_spec/stage_brief.md`
20. `stages/34_outside_bar_mainline_promotion/03_reviews/review_index.md`
21. `stages/34_outside_bar_mainline_promotion/04_selected/selection_status.md`
22. `stages/34_outside_bar_mainline_promotion/04_selected/runtime_handoff_status.md`
23. `stages/33_outside_bar_state_exit_followup/00_spec/stage_brief.md`
24. `stages/33_outside_bar_state_exit_followup/03_reviews/review_index.md`
25. `stages/33_outside_bar_state_exit_followup/04_selected/selection_status.md`
26. `stages/32_candle_pattern_exit_diagnostic/00_spec/stage_brief.md`
27. `stages/32_candle_pattern_exit_diagnostic/03_reviews/review_index.md`
28. `stages/32_candle_pattern_exit_diagnostic/04_selected/selection_status.md`
29. `stages/31_impulse_candle_exit_diagnostic/00_spec/stage_brief.md`
30. `stages/31_impulse_candle_exit_diagnostic/03_reviews/review_index.md`
31. `stages/31_impulse_candle_exit_diagnostic/04_selected/selection_status.md`
32. `stages/30_macro_mismatch_root_cause/00_spec/stage_brief.md`
33. `stages/30_macro_mismatch_root_cause/03_reviews/review_index.md`
34. `stages/30_macro_mismatch_root_cause/04_selected/selection_status.md`
35. `docs/context/stage23_27_wave2_crosssplit_synthesis_20260412.md`
36. `stages/29_fusion_long_repair/00_spec/stage_brief.md`
37. `stages/29_fusion_long_repair/03_reviews/review_index.md`
38. `stages/29_fusion_long_repair/04_selected/selection_status.md`
39. `stages/28_retrain_feature_checks/00_spec/stage_brief.md`
40. `stages/28_retrain_feature_checks/03_reviews/review_index.md`
41. `stages/28_retrain_feature_checks/04_selected/selection_status.md`
42. `stages/27_vol_adaptive_overlay/04_selected/selection_status.md`
43. `stages/26_gov_adaptive_overlay/04_selected/selection_status.md`
44. `stages/25_soft_contextual_control/04_selected/selection_status.md`
45. `foundation/reports/governance_selected_runs_standard_20260409.md`

## Current Decisions

- shared working window override: `2022-08-01 .. 2026-04-12 inclusive`
- shared working window build summary: `intersection_rows=57142` `feature_valid_rows=56918`
- Stage 39 status: `wave1_completed`
- Stage 39 decision: `extended_bridge_still_prefers_34D_and_fresh_mt5_runtime_logs_now_exist`
- Stage 39 read: `the 2024-01-01 through 2026-04-12 MT5 bridge still preferred 34D over 34B by net +107.93 and return_pct +21.586, while a fresh 2026-03-01 through 2026-04-12 shadow run produced current-date logs but still failed exact checksum parity`
- Stage 39 parity read: `latest proxy parity improved to mean_max_abs about 0.0258 on the latest 100 ready rows, but exact and best-neighbor feature checksum matches both remained zero`
- Stage 38 evidence-pack status: `wave1_completed`
- Stage 38 evidence-pack decision: `keep_34D_and_expand_the_pre_live_work_package_beyond_a_single_narrow_followup`
- Stage 38 evidence-pack read: `the best broad next package is now explicit: direct-event evidence hardening, 34B-versus-34D value attribution, and a fresh runtime snapshot parity audit before any broad retrain or window extension`
- Stage 37 bridge status: `wave1_completed`
- Stage 37 bridge decision: `continuous_bridge_still_prefers_34D_over_34B`
- Stage 37 bridge read: `a continuous 2024-01-01 through 2026-02-28 risk_pct account path still preferred 34D by net +129.64, with positive contribution in 2024, 2025, and 2026_ytd`
- Stage 37 continuity bias: `do not assume a near-tie after split resets will remain a near-tie once 2024 through early 2026 compounds continuously`
- Stage 36 localization status: `wave1_completed`
- Stage 36 localization decision: `34D_edge_is_sparse_long_state_exit_protection_not_broad_systemic_drift`
- Stage 36 localization read: `only 7 direct long suppressions fired across Stage 35, with 5 hist_2024 events explaining almost all of the older-window edge and zero test-window events`
- Stage 36 simplification bias: `if simplification reopens, target a narrower long no-entry subset rather than removing the candle sidecar entirely`
- Stage 35 simplification status: `wave1_completed`
- Stage 35 verified carry: `35A_34d_refcarry_0001`
- Stage 35 simplification candidate: `35B_34b_simpleref_0001`
- Stage 35 simplification decision: `keep_34D_do_not_simplify_to_34B`
- Stage 35 simplification read: `governance-only simplification preserved validation and test, but gave back too much hist_2024 edge to justify removing the candle sidecar`
- Stage 34 mainline status: `wave1_completed`
- Stage 34 new regular incumbent: `34D_29s_outbarlong_0001`
- Stage 34 new regular shadow: `34B_29s_refcarry_0001`
- Stage 34 decomposition reference: `34C_29n_outbarlong_0001`
- Stage 34 mainline decision: `promote_34D_over_29N_and_29S`
- Stage 34 promotion read: `29S governance carry plus long-only outside-bar suppression is the first clean regular-stage upgrade beyond 29N`
- Stage 34 handoff status: `bundle_runtime_verified`
- Stage 34 handoff runtime id: `exp_34d_29s_outbarlong_v1_handoff`
- Stage 34 handoff verification read: `fresh bundle-driven validation / test / hist_2024 reruns matched att_0001 / att_0002 / att_0003 exactly; the known test ready-row gap remains 35`
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

- Stage 39 then extended the shared data and MT5 execution window beyond the older `2026-02-28` cutoff and asked whether the continuity story survives the latest closed-bar day:
  - rerun `34D` and `34B` through one uninterrupted `risk_pct` account path from `2024-01-01` through `2026-04-12`
  - rerun `34D` again on a latest-window shadow slice from `2026-03-01` through `2026-04-12`
- That Stage 39 read still preferred `34D`:
  - `34D` beat `34B` by about `+107.93` net and `+21.586` return points on the extended bridge
  - the carried edge remained positive in `2024`, `2025`, and `2026_ytd`
  - bridge trade count stayed identical, which keeps the story focused on trade quality rather than broader participation
- The same Stage 39 read also reopened the runtime-audit surface with current-date MT5 logs:
  - the latest `34D` shadow slice produced `2216` ready rows through `2026-04-10 23:55:00`
  - proxy probability drift improved versus the earlier Stage 38 proxy check
  - exact feature checksum parity still did not match, so the fresh runtime surface exists but the true Python-to-MT5 parity audit is not yet closed
- Stage 37 then added the widest practical continuity read on top of the Stage 35 and Stage 36 conclusions:
  - run `34D` and `34B` through one uninterrupted `risk_pct` account path from `2024-01-01` through `2026-02-28`
- That Stage 37 bridge still preferred `34D`:
  - `34D` beat `34B` by about `+129.64` net and `+25.928` return points
  - the bridge advantage was not only a `2024` story; calendar slices stayed positive in `2024`, `2025`, and `2026_ytd`
  - bridge risk was nearly tied, with only a tiny DD and ulcer tax on the stronger `34D` line
- That means the anti-simplification case is now supported by three different reads:
  - Stage 35 split-reset scoreboard
  - Stage 36 direct-event localization
  - Stage 37 continuous-account bridge
- Stage 36 then answered the next question left open by Stage 35:
  - if full removal of the candle sidecar is too blunt, where exactly is the surviving `34D` value coming from
- That Stage 36 read localized the answer tightly:
  - only `7` direct outside-bar suppressions fired across `validation / test / hist_2024`
  - all `7` were long-side `STATE_EXIT_MARGIN` suppressions
  - all `7` held for exactly one more bar
  - `hist_2024` supplied `5` of those `7` events and about `34.86` of the `36.37` net-profit edge over `34B`
- The same Stage 36 read also showed what the sidecar is not:
  - it is not a broad current-window test rescue
  - it is not a short-side story
  - it is not a general distributional lift spread evenly across trades
- That means the sidecar remains worth keeping, but future simplification should focus on preserving a small long no-entry protection pocket rather than on blanket removal.
- Stage 35 then asked the cleanest next-step question after the Stage 34 promotion and handoff check:
  - can the live line be simplified back to the governance-only `34B` backbone without losing what made `34D` worth keeping
- That Stage 35 read answered `no`:
  - validation stayed effectively identical
  - test stayed exactly identical
  - `hist_2024` fell materially from `46.374` to `39.100`
- The practical read is therefore:
  - the candle sidecar is not cosmetic
  - it is still earning its moving-part cost in the older window
- That closes the most obvious `remove the sidecar entirely` simplification path and keeps `34D` as the live regular answer.
- Stage 34 then brought the Stage 33 extra finding back into the regular alpha lane and tested it directly against the active `29N / 29S` mainline.
- That Stage 34 read showed that the `33C` candle-sidecar survives regular-stage scrutiny:
  - `34C` improved `hist_2024` strongly while preserving the current `test` window
  - `34B` preserved the older `29S` governance-shadow current-window edge
  - `34D` combined both stories cleanly
- The same Stage 34 read promoted `34D` over both prior mainline references:
  - versus `29N`, it improved `validation`, `test`, and `hist_2024`
  - versus `29S`, it held the same current-window shape while materially improving `hist_2024`
- That makes `34D` the first regular-stage promotion built from a formerly extra-only candle-shape idea.
- This branch then verified that the selected `34D` bundle survives the shared handoff path:
  - compile into a fresh Common Files runtime package
  - rerun through the shared bundle-driven tester path
  - reproduce the existing `validation / test / hist_2024` metrics exactly
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

- keep `34D` as the live regular lane; Stage 39 showed it still wins after extending the MT5 bridge through `2026-04-12`
- treat the window extension as a continuity and runtime-audit upgrade, not as permission to reopen blanket simplification, broad retraining, or a wider contract rewrite
- use the fresh Stage 39 `2026-03-01 .. 2026-04-12` MT5 logs as the starting surface for the next exact Python-to-MT5 parity pass
- keep the Stage 38 communication package in front: critical-protection-event visualization and `34B vs 34D` delta explanation remain the next high-value presentation tasks
- keep `34D` as the live regular lane; Stage 37 showed it still wins in one uninterrupted 2024 to early-2026 equity path
- keep the Stage 37 bridge as continuity evidence only; do not replace the frozen split scoreboard with it
- if we want a wider view again, prefer segmented bridge or rolling-window diagnostics before any new simplification claim
- if simplification reopens later, it now has to beat three reads together:
  - Stage 35 split-reset scoreboard
  - Stage 36 localization
  - Stage 37 continuous bridge
- keep `34D` as the live regular lane; Stage 36 showed the sidecar value is sparse but still real
- treat the Stage 36 read as a localization map, not as permission to reopen the closed `remove the sidecar entirely` simplification path
- if simplification reopens later, target the narrow long `no entry / weak margin` subset first rather than broad weekday or session heuristics
- keep the outside-bar topic `long-only` unless a later fresh rerun produces a different directional read
- do not spend follow-up time trying to explain the current test window through the sidecar; Stage 36 showed it simply never fired there
- keep `34D` as the live regular lane; it is now the strongest balanced operating answer
- treat the `34D` experiment bundle as the verified runtime handoff reference, not just as a stage-local winner
- close the plain `34B` governance-only simplification path for now; Stage 35 showed that it gives back too much `hist_2024` edge
- if simplification reopens later, require a narrower reduction than `remove the candle sidecar entirely`
- keep `34B` as the main regular shadow because it isolates the governance-only line behind the new incumbent
- keep `34C` as the candle-sidecar decomposition reference; it proved value but is not the preferred operating mix by itself
- if the next regular stage opens, start from the verified `34D` bundle handoff and test simplification against `34B` first
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
