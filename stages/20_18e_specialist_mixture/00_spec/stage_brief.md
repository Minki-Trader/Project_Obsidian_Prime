# Stage Brief

- stage: `20_18e_specialist_mixture`
- goal: `test whether 18E can be improved by mixing in the 17C short specialist (and optionally 17D flat guard) instead of more recency weighting`
- source operating reference: `18E = 17E + PH20`
- windows: `2401, 2407, 2501`
- target segment: `2407 / holdout_b`
- ranking basis: `positive_test_windows -> positive_holdout_b_windows -> avg_test_return -> min_holdout_b -> target_holdout_b -> avg_test_pf`
- candidate matrix: `18E ref, 17C practical refs, 17E+17C soft vote, 17E+17C+17D tri-vote`
- operating overlays: `PH20, BD20`
