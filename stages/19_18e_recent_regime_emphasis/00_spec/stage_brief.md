# Stage Brief

- stage: `19_18e_recent_regime_emphasis`
- goal: `test whether model-side recent-regime emphasis can improve on 18E without turning 2407 into a hard-coded date detector`
- source operating reference: `18E = 17E + PH20`
- windows: `2401, 2407, 2501`
- target segment: `2407 / holdout_b`
- ranking basis: `positive_test_windows -> positive_holdout_b_windows -> avg_test_return -> min_holdout_b -> avg_test_delta_vs_18E -> avg_test_pf`
- overlay policy: `fixed PH20 on every candidate`
- candidates: `reference, recent6_x1.5, recent6_x2.0, recent9_x2.0, recent6_short_guard, recent6_flat_guard, linear_ramp_x2.0`
