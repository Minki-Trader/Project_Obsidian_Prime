# Stage Brief

- stage: `16_09c_feature_core_fork`
- goal: `test feature-level core forks around 09C instead of continuing reverse-WFO micro overlays`
- base core: `09C_05ET_margin0700_t30_l50_m0700_h4`
- windows: `2401, 2407, 2501`
- target segment: `2407 / holdout_b`
- ranking basis: `positive_test_windows -> avg_test_return -> positive_holdout_b_windows -> min_holdout_b -> min_test -> avg_test_pf`
- forks: `reference_full, persistence_only, sessionless, external_breadthless`
