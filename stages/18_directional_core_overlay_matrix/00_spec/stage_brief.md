# Stage Brief

- stage: `18_directional_core_overlay_matrix`
- goal: `scale out practical session/risk overlays across the new Stage 17 directional cores instead of continuing narrow micro-probes`
- source cores: `17E ovr_balanced`, `17C short_specialist`, `17D flat_guard`
- windows: `2401, 2407, 2501`
- ranking basis: `positive_test_windows -> positive_holdout_b_windows -> avg_test_return -> target_2407_holdout_b -> min_holdout_b -> avg_test_pf`
- broad matrix: `plain, soft_decay, LP02, 13D-balanced, postcash_hold_cut, clock_taper`
