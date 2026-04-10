# Stage 28 Event-Triggered Retrain Wave 2

- reviewed_on: `2026-04-10`
- purpose: `test whether the reopened 28B compact lineage behaves better under bounded month-level retrain triggers than under blind monthly cadence`
- lineage_reference: `28B_18e_persist48_ph20_0001`
- operating_reference_unchanged: `27A_26a_volref_0001`

## Scoreboard

| run | return_pct | pf | trades | max_dd_pct | positive_months | retrain_months | gov_state | max_ext_skip |
|---|---|---|---|---|---|---|---|---|
| `28E` | `58.134` | `1.4075` | `253` | `14.4089` | `7` | `0` | `OK` | `1.0000` |
| `28F` | `-22.870` | `0.9547` | `1414` | `50.4040` | `5` | `14` | `OK` | `1.0000` |
| `28G` | `18.384` | `1.0214` | `1439` | `40.0913` | `6` | `7` | `ALERT` | `1.0000` |

## Headline

- fixed carry `28E`: return_pct `58.134`, PF `1.4075`, trades `253`, max_dd_pct `14.4089`
- monthly retrain `28F`: return_pct `-22.870`, PF `0.9547`, trades `1414`, max_dd_pct `50.4040`
- event trigger `28G`: return_pct `18.384`, PF `1.0214`, trades `1439`, max_dd_pct `40.0913`

## Diagnostics

- fixed carry retrain_months: `0`
- monthly retrain retrain_months: `14`
- event trigger retrain_months: `7`
- event trigger months: `2025_02, 2025_05, 2025_06, 2025_07, 2025_08, 2025_10, 2025_11`

## Execution

- fixed carry governance latest: `OK`, max_external_skip_rate `1.0000`
- monthly retrain governance latest: `OK`, max_external_skip_rate `1.0000`
- event trigger governance latest: `ALERT`, max_external_skip_rate `1.0000`

## Decision

- decision: `keep_fixed_carry_reference`
- fixed_carry_reference: `28E_28b_fixedcarry_long14m_0001`
- shadow_candidate: `28G_28b_negpf_trigger_long14m_0001`
- lineage_followup_candidate: `none`
