# Stage 38 Pre-Live Evidence Pack

- stage: `38_prelive_evidence_pack`
- updated_on: `2026-04-13`
- current_wave: `wave1_completed`
- stage_type: `diagnostic_evidence_stage`
- inherited_regular_reference: `34D_29s_outbarlong_0001`
- inherited_regular_shadow: `34B_29s_refcarry_0001`
- diagnostic_inputs:
  - `Stage 34 mainline promotion review`
  - `Stage 35 simplification review`
  - `Stage 36 outside-bar localization`
  - `Stage 37 long-horizon bridge`

## Purpose

- keep the next-work package broad enough to absorb both the GPT and Grok follow-up ideas without reopening a full retrain wave too early
- convert the Stage 36 `sparse pocket` read into a reusable evidence pack:
  - direct-event timestamps
  - raw-bar context
  - feature context
  - incremental P&L attribution
- make the `34B -> 34D` value story easier to explain as:
  - split-reset attribution
  - Stage 34 decomposition
  - continuous bridge continuity
- add a practical pre-live parity read:
  - what is already runtime-verified
  - what still needs a fresh Python-to-MT5 audit surface

## Scope

- reuse the existing Stage 34 through Stage 37 artifacts as the primary evidence surface
- enrich the Stage 36 direct events with:
  - raw `US100` M5 bar context
  - current feature-row context from the shared feature matrix
  - exact-match checks for key externals such as `VIX`, `US10YR`, and `USDX`
- summarize the `34D` edge through three lenses:
  - Stage 34 decomposition
  - Stage 35 and Stage 36 split-reset attribution
  - Stage 37 continuous bridge attribution
- include a parity proxy read from the verified Stage 34 handoff runtime logs, but do not mistake that proxy for a final runtime snapshot audit

## Evaluation Rules

- keep `34B` as the base line for incremental sidecar attribution unless a narrower decomposition question explicitly needs `34C`
- treat Stage 37 as continuity evidence only; do not let the bridge replace the frozen `hist_2024 / validation / test` scoreboard
- if the proxy parity surface does not match MT5 exactly, record that as an audit-surface gap rather than as a live-runtime regression claim

## Promotion Gates

- this is a diagnostic stage, not a promotion stage
- do not reopen blanket simplification from this stage alone
- do not reopen broad retraining from this stage alone
- use this stage to define the next pre-live work package more concretely:
  - evidence-pack hardening
  - base-versus-incumbent attribution
  - dedicated fresh runtime snapshot parity audit
