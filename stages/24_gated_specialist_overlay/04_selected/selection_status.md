# Stage 24 Selection Status

- reviewed_on: `2026-04-09`
- stage: `24_gated_specialist_overlay`
- roadmap_anchor: `Claude gated specialist overlay wave`
- inherited_regular_reference: `23A_22q_base_stateexit_ref_0001`

## Current Read

- regular incumbent: `24A_23a_base_gate_ref_0001`
- regular shadow challenger: `24B_23a_17csg040_gate_0001`
- keep_or_replace: `keep_incumbent`

## Scoreboard

| run | hist_return | val_return | test_return | test_dd | test_pf | test_short_count | test_gate_rejects | read |
|---|---|---|---|---|---|---|---|---|
| `24A` | `26.002` | `193.808` | `71.068` | `27.423` | `1.3199` | `163` | `0` | `regular inherited baseline` |
| `24B` | `49.122` | `126.794` | `31.214` | `30.160` | `1.1908` | `108` | `1248` | `mild short specialist gate` |
| `24C` | `39.816` | `118.956` | `18.508` | `28.142` | `1.1279` | `67` | `1512` | `medium short specialist gate` |
| `24D` | `14.566` | `85.770` | `12.482` | `25.878` | `1.0974` | `40` | `1674` | `aggressive short specialist gate` |

## Diagnostics

- shadow gate stats `24B`: `{'active_count': 1836, 'passed_count': 588, 'rejected_count': 1248, 'pass_rate': 0.3202614379084967, 'aux_short_median': 0.35666699999999996, 'aux_short_p90': 0.493447, 'reject_reason_counts': {'SHORT_GATE_FAIL_AUX_SHORT': 1248}}`

## Decision

- decision: `keep_incumbent`
- regular incumbent: `24A_23a_base_gate_ref_0001`
- regular shadow challenger: `24B_23a_17csg040_gate_0001`

## Follow-Up Bias

- keep the current regular incumbent unless the gate line shows a cleaner OOS plus non-OOS balance
- use gate reject counts and short_count compression to decide whether the specialist is adding signal or just starving the book

## Report Refs

- `03_reviews/stage24_gated_specialist_wave1_20260409.md`
