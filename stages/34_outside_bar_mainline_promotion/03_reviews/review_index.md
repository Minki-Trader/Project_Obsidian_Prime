# Stage 34 Review Index

- reviewed_on: `2026-04-12`
- latest_review: `03_reviews/stage34_mainline_20260412.md`
- inherited_regular_reference: `34A_29n_refcarry_0001`
- promoted_candidate: `34D_29s_outbarlong_0001`
- decomposition_reference: `34C_29n_outbarlong_0001`
- governance_carry_reference: `34B_29s_refcarry_0001`
- decision: `promote_34D_over_29N_and_29S`

## Quick Read

- `34A` reproduced `29N` exactly, so the mainline promotion stage started from a clean carry base
- `34B` reproduced the old `29S` shadow shape and confirmed that the governance shadow still improves the current `test` window
- `34C` confirmed that the long-only outside-bar sidecar is real even without governance:
  - `hist_2024` improved strongly
  - `test` stayed unchanged
- `34D` is the key result:
  - it kept the `29S` current-window improvement
  - it also recovered the stronger older-window gain from the candle sidecar
  - the DD tax versus `29N` stayed tiny enough to accept
