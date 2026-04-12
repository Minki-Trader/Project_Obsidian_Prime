# Stage 33 Outside Bar Follow-Up Review

- reviewed_on: `2026-04-12`
- stage: `33_outside_bar_state_exit_followup`
- inherited_regular_reference: `29N_25o_sxh2_0001`
- carry_check_run: `33A_29n_refcarry_0001`
- best_non_regression_run: `33C_29n_outbar_long_0001`

## Executive Read

- this wave converts the Stage 32 `outside_adverse_bar` diagnosis into a live MT5 runtime sidecar
- the runtime change is intentionally narrow: suppress `STATE_EXIT_MARGIN` only when the closed bar is an adverse outside bar
- the main question is whether that diagnosis survives real path-dependent tester runs, not just counterfactual trade-ledger rewrites

## Carry Check

- `33A` exists only to rerun the inherited `29N` logic through the updated EA path
- carry check summary: `test_return_delta=0.000`, `validation_return_delta=0.000`, `hist_return_delta=0.000`

## Candidate Scoreboard

### 33B_29n_outbar_both_0001

- label: `33B both`
- test_non_regression: `true`
- weighted_score: `7.039`
- validation: `return_pct=196.772` `pf=1.5733` `dd_pct=12.7698` `delta_return=-0.036` `delta_pf=0.0016` `delta_dd=-0.0050` `suppressed=6`
- test: `return_pct=99.556` `pf=1.4828` `dd_pct=18.4060` `delta_return=0.000` `delta_pf=0.0000` `delta_dd=0.0000` `suppressed=0`
- hist_2024: `return_pct=45.826` `pf=1.2316` `dd_pct=14.1190` `delta_return=6.458` `delta_pf=0.0295` `delta_dd=-0.0122` `suppressed=9`

### 33C_29n_outbar_long_0001

- label: `33C long-only`
- test_non_regression: `true`
- weighted_score: `7.054`
- validation: `return_pct=196.778` `pf=1.5741` `dd_pct=12.7761` `delta_return=-0.030` `delta_pf=0.0024` `delta_dd=0.0013` `suppressed=2`
- test: `return_pct=99.556` `pf=1.4828` `dd_pct=18.4060` `delta_return=0.000` `delta_pf=0.0000` `delta_dd=0.0000` `suppressed=0`
- hist_2024: `return_pct=45.816` `pf=1.2328` `dd_pct=14.1855` `delta_return=6.448` `delta_pf=0.0307` `delta_dd=0.0543` `suppressed=5`

### 33D_29n_outbar_short_0001

- label: `33D short-only`
- test_non_regression: `true`
- weighted_score: `-1.130`
- validation: `return_pct=196.852` `pf=1.5707` `dd_pct=12.7594` `delta_return=0.044` `delta_pf=-0.0010` `delta_dd=-0.0155` `suppressed=4`
- test: `return_pct=99.556` `pf=1.4828` `dd_pct=18.4060` `delta_return=0.000` `delta_pf=0.0000` `delta_dd=0.0000` `suppressed=0`
- hist_2024: `return_pct=38.316` `pf=1.1958` `dd_pct=14.0693` `delta_return=-1.052` `delta_pf=-0.0063` `delta_dd=-0.0619` `suppressed=4`

### 33E_29n_outbar_both_a125_0001

- label: `33E both + ATR1.25`
- test_non_regression: `true`
- weighted_score: `2.288`
- validation: `return_pct=194.686` `pf=1.5691` `dd_pct=12.8081` `delta_return=-2.122` `delta_pf=-0.0026` `delta_dd=0.0332` `suppressed=5`
- test: `return_pct=99.556` `pf=1.4828` `dd_pct=18.4060` `delta_return=0.000` `delta_pf=0.0000` `delta_dd=0.0000` `suppressed=0`
- hist_2024: `return_pct=45.488` `pf=1.2304` `dd_pct=14.1190` `delta_return=6.120` `delta_pf=0.0283` `delta_dd=-0.0122` `suppressed=7`

### 33F_29n_outbar_long_a125_0001

- label: `33F long-only + ATR1.25`
- test_non_regression: `true`
- weighted_score: `2.775`
- validation: `return_pct=194.910` `pf=1.5704` `dd_pct=12.8034` `delta_return=-1.898` `delta_pf=-0.0013` `delta_dd=0.0286` `suppressed=1`
- test: `return_pct=99.556` `pf=1.4828` `dd_pct=18.4060` `delta_return=0.000` `delta_pf=0.0000` `delta_dd=0.0000` `suppressed=0`
- hist_2024: `return_pct=45.490` `pf=1.2312` `dd_pct=14.1855` `delta_return=6.122` `delta_pf=0.0292` `delta_dd=0.0543` `suppressed=4`

## Decision Bias

- prefer only candidates that preserve the current test window while adding value elsewhere
- if no candidate clears that bar, keep `29N` unchanged and treat the candle sidecar as informative but non-promoted
