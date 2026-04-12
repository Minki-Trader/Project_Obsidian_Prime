# Stage 30 Selection Status

- reviewed_on: `2026-04-12`
- stage: `30_macro_mismatch_root_cause`
- stage_type: `diagnostic_sidecar`
- operating_reference_under_review: `29N_25o_sxh2_0001`

## Current Read

- current_status: `diagnostic_complete_wave1`
- operating_decision: `keep exact alignment + all-or-skip`
- stale_fallback_promotion_status: `closed`
- main_macro_findings: `VIX sparse-feed holes and US10YR date-local clusters`

## Promotion Gates

- gate_1: `no promotion decision happens inside this sidecar`
- gate_2: `any future relaxation must prove a new contract hypothesis, not just show that some rows are recoverable`
- gate_3: `any reopened feed-health work must stay scoped to VIX / US10YR and must not widen into a whole-workspace stale-bar policy`

## Scoreboards

- runtime_shadow_audit: `29N validation / test / hist_2024`
- raw_source_coverage_audit: `data/raw/mt5_bars/m5 exact timestamp comparison against the same base timeline`

## Headline

- dominant hist_2024 / validation macro pressure: `VIX`
- dominant test macro pressure: `US10YR`
- structural control mismatch family: `AAPL.xnas regular-session shape, USDX recurring overnight closure`
- stale1 recovery read: `VIX about 0.32, US10YR about 0.58, AAPL.xnas / USDX near zero`

## Risk

- diagnostic_risk: `broad stale relaxation would blur a source-health problem into an execution-policy change`
- promotion_risk: `recovering some skipped rows without separating structural vs sparse-feed gaps would create a misleading improvement story`

## Diagnostics

- reviewed_run: `29N_25o_sxh2_0001`
- evidence_type: `runtime mismatch clustering + raw exact-miss coverage`
- macro_takeaway: `the macro issue is source-shape dependent, not alpha-rule dependent`
- scope_takeaway: `a symbol-specific macro diagnostic is plausible later; a whole-workspace relaxation story is not`

## Execution

- operating_contract: `unchanged`
- runtime_followup_needed: `none for Stage 29`
- future_feed_health_followup: `optional diagnostic only`

## Decision

- decision: `keep exact alignment as the live contract and leave stale fallback closed`

## Follow-Up Bias

- only reopen this topic if a feed-health hypothesis appears that is narrower than the old Stage 22 relaxation lane
- if reopened, test symbol-specific macro diagnostics first and keep AAPL.xnas / USDX out of any stale-fallback story
- keep Stage 29 alpha work separate from this branch

## Report Refs

- `03_reviews/stage30_macro_mismatch_root_cause_20260412.md`
