# Stage Brief

- stage: `17_09c_directional_core_fork`
- goal: `search for a new core edge by changing the directional learning objective around 09C instead of more overlay micro-tuning`
- base core: `09C_05ET_margin0700_t30_l50_m0700_h4`
- windows: `2401, 2407, 2501`
- target segment: `2407 / holdout_b`
- ranking basis: `positive_test_windows -> positive_holdout_b_windows -> avg_test_return -> min_holdout_b -> avg_test_pf -> min_test`
- candidates: `reference_balanced, short_guard, short_specialist, flat_guard, ovr_balanced`
