# Stage 23-27 Follow-Up Search Plan

## Purpose

This note maps the full Stage 23-27 follow-up suggestion set into runnable wave-2 experiment builders rooted in the current workspace contracts and EA runtime.

## Anchor Reuse

- Stage 23 keeps `23C_22q_margin004_h2_risk2_0001` as the state-exit anchor for the `margin=0.04 / min_hold_bars=2` center point.
- Stage 24 keeps `24A_23a_base_gate_ref_0001` as the ungated reference and reuses the `17C` auxiliary short specialist ONNX.
- Stage 25 keeps `25D_24a_monpost_t050_m030_psh2_0001` as the incumbent reference while stripping stage-local contextual rules when running ablations.
- Stage 26 keeps `26A_25d_govref_0001` as the governance observe-only reference.
- Stage 27 keeps `27A_26a_volref_0001` as the volatility observe-only reference.

## Runtime Extensions Added

- State-exit rules now accept `direction`, optional `close_fraction`, and `state_exit_reentry_lock_bars`.
- Entry blocking now behaves as a block-until time so multi-bar state-exit locks actually hold.
- Specialist short gate now supports:
  - contextual application
  - low-primary-margin apply-only mode
  - soft-penalty mode
  - confidence-band reject/penalty/pass behavior
  - joint gating with a minimum primary short margin
- Context matching now supports `late_session` in addition to the existing Monday and NY postcash pockets.
- Governance overlays now support:
  - signal modes `argmax_only`, `entropy_only`, `both`, `either`
  - multi-bar durations
  - context and direction scoping
- Volatility overlays now support:
  - context and direction scoping
  - high-vol hold-cap reductions

## Search Mapping

- Stage 23 local search is covered by margin retunes, hold retunes, partial-reduce variants, and 1-2 bar reentry locks.
- Stage 23 expansion search is covered by ladder exits and direction-specific state exits.
- Stage 24 local search is covered by denser thresholds, low-margin-only apply mode, soft-penalty mode, and Monday-only gate scope.
- Stage 24 expansion search is covered by contextual weak-pocket gating, confidence-band gating, and joint primary-margin gating.
- Stage 25 local search is covered by threshold-only vs margin-only ablations, postcash hold-cap sweeps, Monday strength sweeps, and hold-only vs suppressor-only decomposition.
- Stage 25 expansion search is covered by late-session long asymmetry, session-direction pocket maps, and pocket-specific hold-cap exit fusion.
- Stage 26 local search is covered by tighter external skip triggers, split signal trigger modes, taper-strength retunes, and duration sweeps.
- Stage 26 expansion search is covered by burst-style mixed triggers, postcash short governance scope, and weak-pocket governance fusion.
- Stage 27 local search is covered by lighter high-vol taper strengths, denser high-vol boundaries, high-vol-only reruns, and hold-cap-only high-vol control.
- Stage 27 expansion search is covered by volatility-direction splits, volatility-session scoping, and volatility-aware hold fusion.

## Builder Scripts

- `stages/23_state_conditioned_exit/01_inputs/build_stage23_state_exit_wave2_runs.py`
- `stages/24_gated_specialist_overlay/01_inputs/build_stage24_gated_specialist_wave2_runs.py`
- `stages/25_soft_contextual_control/01_inputs/build_stage25_soft_contextual_wave2_runs.py`
- `stages/26_gov_adaptive_overlay/01_inputs/build_stage26_gov_adaptive_wave2_runs.py`
- `stages/27_vol_adaptive_overlay/01_inputs/build_stage27_vol_adaptive_wave2_runs.py`

## Execution Notes

- The wave-2 builders create ready bundles and preserve the existing stage artifacts for MT5 runtime compilation later.
- Existing anchor runs are intentionally reused instead of duplicated when a suggestion already matches a completed run point.
