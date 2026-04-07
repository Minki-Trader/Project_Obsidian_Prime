# Stage Brief

- stage: `12_09c_overlay_fine_probe`
- goal: `run a tiny 3x3 fine probe around the Stage 11 Monday/post-cash overlay pocket on top of the 09C core`
- source core: `09C_05ET_margin0700_t30_l50_m0700_h4`
- windows: `2401, 2407, 2501`
- target: `2407 / holdout_b`
- local axes: `monday_risk_pct_mult in {0.60, 0.625, 0.65}`, `ny_postcash_risk_pct_mult in {0.60, 0.625, 0.65}`
