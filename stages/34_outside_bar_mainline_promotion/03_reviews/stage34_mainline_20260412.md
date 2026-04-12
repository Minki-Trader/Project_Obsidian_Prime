# Stage 34 Mainline Review

- reviewed_on: `2026-04-12`
- stage: `34_outside_bar_mainline_promotion`
- inherited_regular_reference: `34A_29n_refcarry_0001`
- best_non_regression_run: `34D_29s_outbarlong_0001`

## Executive Read

- Stage 34 is the regular alpha-stage promotion check for the Stage 33 long-only outside-bar sidecar
- the read here matters more than the extra-stage read because it places the sidecar back inside the operating promotion lane

## Candidate Scoreboard

### 34B_29s_refcarry_0001

- label: `34B shadow carry`
- test_non_regression: `true`
- weighted_score: `4.868`
- validation: `return_pct=197.530` `pf=1.5810` `dd_pct=12.7357` `delta_return=0.722` `delta_pf=0.0093` `delta_dd=-0.0391`
- test: `return_pct=100.594` `pf=1.4883` `dd_pct=18.4512` `delta_return=1.038` `delta_pf=0.0055` `delta_dd=0.0451`
- hist_2024: `return_pct=39.100` `pf=1.2009` `dd_pct=14.0827` `delta_return=-0.268` `delta_pf=-0.0012` `delta_dd=-0.0485`

### 34C_29n_outbarlong_0001

- label: `34C 29N + outbar long`
- test_non_regression: `true`
- weighted_score: `7.054`
- validation: `return_pct=196.778` `pf=1.5741` `dd_pct=12.7761` `delta_return=-0.030` `delta_pf=0.0024` `delta_dd=0.0013`
- test: `return_pct=99.556` `pf=1.4828` `dd_pct=18.4060` `delta_return=0.000` `delta_pf=0.0000` `delta_dd=0.0000`
- hist_2024: `return_pct=45.816` `pf=1.2328` `dd_pct=14.1855` `delta_return=6.448` `delta_pf=0.0307` `delta_dd=0.0543`

### 34D_29s_outbarlong_0001

- label: `34D 29S + outbar long`
- test_non_regression: `true`
- weighted_score: `12.866`
- validation: `return_pct=197.520` `pf=1.5832` `dd_pct=12.7361` `delta_return=0.712` `delta_pf=0.0115` `delta_dd=-0.0387`
- test: `return_pct=100.594` `pf=1.4883` `dd_pct=18.4512` `delta_return=1.038` `delta_pf=0.0055` `delta_dd=0.0451`
- hist_2024: `return_pct=46.374` `pf=1.2360` `dd_pct=14.1916` `delta_return=7.006` `delta_pf=0.0339` `delta_dd=0.0604`

