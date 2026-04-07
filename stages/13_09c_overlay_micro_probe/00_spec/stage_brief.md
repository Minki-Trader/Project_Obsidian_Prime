# Stage Brief

- stage: `13_09c_overlay_micro_probe`
- goal: `run a micro-probe around the Stage 12 Monday/post-cash pocket on top of the 09C core`
- source core: `09C_05ET_margin0700_t30_l50_m0700_h4`
- windows: `2401, 2407, 2501`
- target: `2407 / holdout_b`
- local axes: `monday_risk_pct_mult in {0.55, 0.575, 0.60}`, `ny_postcash_risk_pct_mult in {0.6125, 0.625, 0.6375}`
