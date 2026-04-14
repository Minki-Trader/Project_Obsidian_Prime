# Stage 41 Selection Status

- reviewed_on: `2026-04-14T23:03:56.612119+00:00`
- stage: `41_targeted_feature_snapshot_audit`
- stage_type: `diagnostic_runtime_stage`
- inherited_regular_reference: `34D_29s_outbarlong_0001`
- latest_mt5_attempt: `att_0005`
- latest_snapshot_review: `stages/41_targeted_feature_snapshot_audit/03_reviews/stage41_targeted_feature_snapshot_audit_20260414_att0005.md`
- latest_shared_attribution_attempt: `att_0010`
- latest_shared_attribution_review: `stages/41_targeted_feature_snapshot_audit/03_reviews/stage41_feature_path_shared_attribution_20260414.md`
- latest_threshold_sensitivity_review: `stages/41_targeted_feature_snapshot_audit/03_reviews/stage41_threshold_sensitivity_20260414.md`
- latest_margin_sensitivity_review: `stages/41_targeted_feature_snapshot_audit/03_reviews/stage41_margin_sensitivity_replay_20260414.md`
- latest_margin_fine_replay_review: `stages/41_targeted_feature_snapshot_audit/03_reviews/stage41_margin_fine_replay_20260414.md`
- latest_margin_bridge_confirmation_review: `stages/41_targeted_feature_snapshot_audit/03_reviews/stage41_margin_bridge_confirmation_20260414.md`

## Current Read

- status: `targeted_runtime_parity_recovered_on_localized_windows`
- working_read: `the Stage 40 cluster windows now close to near-exact Python-to-MT5 feature parity after replacing MT5 built-in ATR and Stochastic feature calculations with custom contract-matching implementations inside the runtime feature builder`
- shared_feature_path_read: `a broader latest-window A/B snapshot sample on the simpler 34B bundle now shows that the post-patch built-in-versus-contract KPI gap is shared across 34B and 34D rather than 34D-specific; across 121 sampled snapshot rows, ATR14, ATR50, ATR14_over_ATR50, and secondarily stoch_kd_diff dominate the drift surface, while the contract-aligned path usually shifts probability mass toward p_flat and turns many built-in directional entries into NO_TRADE`
- threshold_sensitivity_read: `the same 121-row sample now shows that the sampled decision drift is almost entirely a fixed-base margin sensitivity story: 25 of 26 directional-to-NO_TRADE flips are max_probability_margin failures, only one row is a pure threshold-cross, and none of the 32 sampled decision-diff rows activated a relevant contextual soft suppressor`
- margin_replay_read: `a fresh latest-window contract-aligned min_margin replay on 34B now shows that 0.0600 is the only tested value that materially improves the KPI surface; versus the 0.0675 contract baseline it recovered net by 10.39, return_pct by 2.078, trade_count by 15, profit_factor by 0.0847, and max_dd_pct by 0.9851, while the same 0.0600 replay matched exactly on the operating 34D bundle`
- margin_fine_replay_read: `a focused 34D-only fine replay around 0.06000 now keeps 0.06000 as the local best tested operating point: 0.05875 added trade count and slightly higher profit factor but gave back net by 0.84 and added max_dd_pct by 1.1362, while 0.06125 weakened net by 5.76 and profit_factor by 0.0239 versus the 0.06000 centerpoint`
- margin_bridge_confirmation_read: `a broader 34D contract-aligned extended-bridge confirmation on 2024.01.01 -> 2026.04.13 now keeps 0.06000 as the best tested carried operating candidate; versus the 0.0675 contract baseline it improved net by 834.45, return_pct by 166.890, trade_count by 200, profit_factor by 0.0113, max_dd_pct by 0.4561, and ulcer_index by 1.6069 while holding external mismatch pressure flat`

## Promotion Gates

- this stage is diagnostic-only
- do not reopen alpha search, simplification, or retraining from localized parity closure alone
- treat the Stage 40 cluster windows as closed for targeted feature parity only after the `att_0005` post-patch audit, not from the pre-patch `att_0004` read
- require a broader follow-up feature snapshot sweep before claiming full runtime parity closure outside the localized windows

## Scoreboards

- pre-patch localized audit (`att_0004`): `row max abs diff mean=23.036015` `max=29.672052`
- post-patch localized audit (`att_0005`): `row max abs diff mean=0.000003` `max=0.000006`
- tolerance closure (`att_0005`): `14 / 14` rows within `1e-4`

## Headline

- targeted feature snapshot audit rows: `14`
- ready rows: `14`
- matched feature-matrix timestamps: `14`
- external exact-match telemetry: `14 / 14` for every tracked external symbol
- largest remaining drift after patch: `ema50_ema200_diff max=0.000006`

## Risk

- full-window runtime parity is not yet proven from this localized audit alone
- stop sizing and runtime overlay helpers still use MT5 built-in ATR paths outside the model-input feature builder
- skip-rate and external availability issues from Stage 39/40 still remain separate operational concerns from the now-closed localized feature parity gap

## Diagnostics

- pre-patch drift was concentrated in `atr_14`, `atr_50`, `atr_14_over_atr_50`, `return_1_over_atr_14`, `bb_squeeze`, and `stoch_kd_diff`
- the localized root cause was MT5 feature generation using built-in ATR/Stochastic values that did not match the Python contract surface for the audited rows
- replacing those feature-path calculations with custom contract-matching Wilder ATR and rolling Stochastic logic collapsed the targeted drift to float-noise scale
- the broader shared A/B snapshot sample (`att_0007` through `att_0010`) now shows the live latest-window weakness is mostly a thresholding effect: contract-aligned inputs weaken directional conviction and raise `p_flat`, with `32 / 121` sampled decision rows flipping and `26` of those flips moving from built-in directional decisions to contract `NO_TRADE`
- the new threshold-sensitivity pass narrows that read further: the sampled weakness is overwhelmingly a fixed `max_probability_margin min_margin=0.0675` effect rather than a contextual soft-suppressor effect, with `25 / 26` directional-to-`NO_TRADE` flips crossing the margin gate and zero sampled relevant contextual-rule activations
- long-side failures are mostly a `flat-wall` pattern, while short-side failures are more often a `short-vs-long tie compression` pattern
- the fresh replay confirms that `min_margin` is not just descriptive; it is an active live lever on the latest window, and the tested response surface strongly prefers a narrow relaxation toward `0.0600` over either the original `0.0675` or stricter values
- the `34D` confirmation run at `0.0600` matched the best `34B` replay exactly on headline metrics, ready-row decisions, and trade ledger shape, so the candidate improvement is not a simplification-only artifact
- the new `34D` fine replay now shows that the coarse `0.0600` candidate was not just a grid accident: both adjacent tests were worse on net, and the lower-side `0.05875` variant also paid a meaningful drawdown tax despite slightly higher trade count and profit factor
- the new extended-bridge confirmation shows that the same `0.0600` candidate also generalizes across the longer carried contract-aligned path rather than only the short latest window, materially lifting both return and risk quality versus the contract baseline while still remaining weaker than the built-in bridge reference in absolute terms

## Execution

- localized windows audited:
  - `2026-03-23 17:20 UTC`
  - `2026-03-23 17:45 UTC` through `2026-03-23 18:15 UTC`
  - `2026-04-02 20:20 UTC` through `2026-04-02 20:45 UTC`
- MT5 post-patch snapshot artifact: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\Common\Files\Project_Obsidian_Prime\runtime\exp_39a_34d_bridge_ext_v1\logs\att_0005_feature_snapshot.jsonl`
- MT5 attempt summary: `stages/39_window_extension_mt5_validation/02_runs/active/39A_34d_bridge_ext_0001/mt5_attempts/att_0005/tester_attempt_summary.json`
- latest shared attribution sample windows:
  - `2026-03-02 16:35 UTC` through `2026-03-02 17:30 UTC`
  - `2026-03-03 17:15 UTC` through `2026-03-03 19:30 UTC`
  - `2026-03-09 17:55 UTC` through `2026-03-09 20:30 UTC`
  - `2026-03-12 18:40 UTC` through `2026-03-12 20:20 UTC`
  - `2026-03-26 19:30 UTC` through `2026-03-26 19:55 UTC`
  - `2026-04-07 19:05 UTC` through `2026-04-07 20:50 UTC`
- latest fixed-margin replay runs:
  - `41A` `34B` `min_margin=0.0600`
  - `41B` `34B` `min_margin=0.0625`
  - `41C` `34B` `min_margin=0.0650`
  - `41D` `34B` `min_margin=0.0675`
  - `41E` `34B` `min_margin=0.0700`
  - `41F` `34D` `min_margin=0.0600`
- latest fixed-margin fine replay runs:
  - `41G` `34D` `min_margin=0.05875`
  - `41F` `34D` `min_margin=0.06000`
  - `41H` `34D` `min_margin=0.06125`
- latest bridge confirmation runs:
  - `41I` `34D` `contract-aligned` `min_margin=0.06750`
  - `41J` `34D` `contract-aligned` `min_margin=0.06000`

## Decision

- keep `34D` as the operating regular reference
- mark the localized Stage 40 feature parity gap as closed for the audited windows
- move the next parity task from root-cause search to broader confirmation sampling
- move the next latest-window attribution task from generic feature drift description to fixed-margin sensitivity replay around the base `min_margin=0.0675` surface
- keep `0.0600` as the best tested latest-window contract-aligned operating candidate after both coarse and fine replay
- keep `0.0600` as the best tested carried contract-aligned operating candidate after the extended-bridge confirmation as well
- do not treat the local fine replay alone as a global promotion argument; require broader confirmation before changing the operating contract-aligned gate outside this stage

## Follow-Up Bias

- keep broad retraining off the critical path; the open question is now shared feature-surface attribution rather than unresolved localized parity drift
- decide explicitly whether the contract-aligned ATR surface should now standardize on the best-tested `34D min_margin=0.0600` gate when a parity-faithful lane is required, or whether the built-in bridge should remain the absolute operating reference while parity confirmation broadens further
- if attribution deepens further, prefer broader parity confirmation or an explicit operating-decision memo on `built-in versus contract-aligned 0.0600`, and keep contextual soft-suppressor hunting off the critical path unless a new sampled window actually activates those rules

## Report Refs

- pre-patch localized read: `stages/41_targeted_feature_snapshot_audit/03_reviews/stage41_targeted_feature_snapshot_audit_20260414.md`
- post-patch localized read: `stages/41_targeted_feature_snapshot_audit/03_reviews/stage41_targeted_feature_snapshot_audit_20260414_att0005.md`
- shared feature-path attribution read: `stages/41_targeted_feature_snapshot_audit/03_reviews/stage41_feature_path_shared_attribution_20260414.md`
- threshold sensitivity read: `stages/41_targeted_feature_snapshot_audit/03_reviews/stage41_threshold_sensitivity_20260414.md`
- margin sensitivity replay read: `stages/41_targeted_feature_snapshot_audit/03_reviews/stage41_margin_sensitivity_replay_20260414.md`
- margin fine replay read: `stages/41_targeted_feature_snapshot_audit/03_reviews/stage41_margin_fine_replay_20260414.md`
- margin bridge confirmation read: `stages/41_targeted_feature_snapshot_audit/03_reviews/stage41_margin_bridge_confirmation_20260414.md`
