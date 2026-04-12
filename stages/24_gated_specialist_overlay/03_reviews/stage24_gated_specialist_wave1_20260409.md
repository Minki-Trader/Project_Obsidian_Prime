# Stage 24 Gated Specialist Overlay Wave 1

- reviewed_on: `2026-04-09`
- purpose: `test 17C short specialist as a short-entry gate on the 23A regular baseline`
- operating_seed: `23A_22q_base_stateexit_ref_0001`
- roadmap_anchor: `Claude gated specialist overlay wave`

## Scoreboard

| run | hist_return | val_return | test_return | test_dd | test_pf | test_short_count | test_gate_rejects | test_gate_pass_rate | read |
|---|---|---|---|---|---|---|---|---|---|
| `24A` | `26.002` | `193.808` | `71.068` | `27.423` | `1.3199` | `163` | `0` | `n/a` | `regular inherited baseline` |
| `24B` | `49.122` | `126.794` | `31.214` | `30.160` | `1.1908` | `108` | `1248` | `0.320` | `mild short specialist gate` |
| `24C` | `39.816` | `118.956` | `18.508` | `28.142` | `1.1279` | `67` | `1512` | `0.176` | `medium short specialist gate` |
| `24D` | `14.566` | `85.770` | `12.482` | `25.878` | `1.0974` | `40` | `1674` | `0.088` | `aggressive short specialist gate` |

## Headline

- incumbent `24A`: `hist=26.002 / val=193.808 / test=71.06800000000001 / test_dd=27.422721683680763 / pf=1.3199272524286705`
- best challenger `24B`: `hist=49.122 / val=126.79400000000001 / test=31.214 / test_dd=30.159538357094373 / pf=1.190766635701364`

## Risk

- baseline OOS risk read: `worst_week=-117.39000000000001 / ulcer=13.066089094415775 / consecutive_losses=9`
- challenger OOS risk read: `worst_week=-79.99 / ulcer=14.141644574624376 / consecutive_losses=7`

## Diagnostics

- baseline test short_count: `163`
- challenger test short_count: `108`
- challenger gate stats: `{'active_count': 1836, 'passed_count': 588, 'rejected_count': 1248, 'pass_rate': 0.3202614379084967, 'aux_short_median': 0.35666699999999996, 'aux_short_p90': 0.493447, 'reject_reason_counts': {'SHORT_GATE_FAIL_AUX_SHORT': 1248}}`
- this wave should be read as a `short suppression` experiment, so short_count compression and gate reject counts matter as much as headline return.

## Execution

- execution quality should remain unchanged if the gate is behaving as designed: `same data path, same feature contract, same exact-alignment runtime; only short entry permission changes`
- baseline test execution: `skip_rate=0.7660606060606061 / external_mismatch_count=8976`
- challenger test execution: `skip_rate=0.7660606060606061 / external_mismatch_count=8976`

## Decision

- regular incumbent: `24A_23a_base_gate_ref_0001`
- regular shadow challenger: `24B_23a_17csg040_gate_0001`
- decision: `keep_incumbent`
- why: `wave 1 is meant to measure whether short specialist gating is alive at all; keep the incumbent unless a challenger improves the regular OOS read without obvious non-OOS damage`
