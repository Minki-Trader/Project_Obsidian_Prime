# Regular Experiment Roadmap

- updated_on: `2026-04-10`
- current_operating_reference: `27A_26a_volref_0001`
- current_shadow_challenger: `27D_26a_vl110h085_0001`
- lineage_followup_candidate: `28E_28b_fixedcarry_long14m_0001`
- roadmap_source: `ranked synthesis of external proposal reviews plus repo-grounded gap analysis`

## Ordered Roadmap

1. `Stage 23` `state-conditioned exit` -- `Grok + GPT`
   - convert fixed point exits into model-state exits using `p_flat`, directional margin decay, and later entropy
   - first wave should be regular risk execution only, anchored to `22Q`

2. `Stage 24` `gated specialist overlay` -- `Claude`
   - test `17C` and related specialists as decision gates or direction-specific suppressors rather than output mixtures

3. `Stage 25` `soft contextual thresholds and asymmetric hold control` -- `Claude + GPT`
   - split `threshold/min_margin` by session and direction
   - test direction-specific `hold_cap` and soft suppressor logic rather than hard detector blocks

4. `Stage 26` `governance-led adaptive overlays` -- `Grok + GPT`
   - move governance telemetry from monitoring-only into challenger design
   - connect skip bursts, signal imbalance, and execution drift to overlay policy changes

5. `Stage 27` `volatility-adaptive overlay` -- `Grok`
   - extend the proven overlay family with volatility-aware multiplier logic instead of fixed scalar values

6. `Stage 28` `event-triggered retrain and feature simplification checks` -- `Grok + Claude`
   - test retraining only on drift events, not on calendar cadence
   - revisit feature-fork simplification on the `17E/18E` lineage instead of the older `09C` lineage
   - wave1 feature simplification result: `28B` beat the rebuilt `28A` full-reference arm and reopened the lineage for follow-up
   - wave2 event-trigger result: fixed carry `28E` beat both blind monthly retrain `28F` and bounded event-trigger retrain `28G`
   - current Stage 28 read: keep `28E` only as an internal lineage reference; do not widen the retrain branch without a stronger trigger hypothesis

7. `Diagnostic sidecar` `macro mismatch root-cause` -- `Claude`
   - keep alignment relaxation closed as a promotion path
   - investigate why `US10YR` and `VIX` mismatches cluster instead of promoting stale-bar handling directly

## Execution Rule

- only one regular alpha stage should be live at a time
- closed diagnostic branches stay outside the promotion lane unless a new contract hypothesis appears
- each stage should emit both a `structural scout` read and a `regular risk execution` read when relevant
