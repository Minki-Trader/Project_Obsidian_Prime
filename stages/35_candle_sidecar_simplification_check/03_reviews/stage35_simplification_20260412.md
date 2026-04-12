# Stage 35 Simplification Review

- reviewed_on: `2026-04-12`
- stage: `35_candle_sidecar_simplification_check`
- inherited_regular_reference: `35A_34d_refcarry_0001`
- simplification_candidate: `35B_34b_simpleref_0001`
- simplification_acceptable: `false`

## Executive Read

- Stage 35 asks the simplest next regular-lane question after the Stage 34 promotion and handoff verification
- the only simplification candidate tested here is the full removal of the candle sidecar while keeping the `29S` governance backbone

## Candidate Scoreboard

### 35B_34b_simpleref_0001

- label: `35B governance-only simplification carry`
- test_non_regression: `true`
- simplification_acceptable: `false`
- weighted_score: `-8.043`
- validation: `return_pct=197.530` `pf=1.5810` `dd_pct=12.7357` `delta_return=0.010` `delta_pf=-0.0022` `delta_dd=-0.0004`
- test: `return_pct=100.594` `pf=1.4883` `dd_pct=18.4512` `delta_return=0.000` `delta_pf=0.0000` `delta_dd=0.0000`
- hist_2024: `return_pct=39.100` `pf=1.2009` `dd_pct=14.0827` `delta_return=-7.274` `delta_pf=-0.0351` `delta_dd=-0.1089`

