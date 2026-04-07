# Stage Brief

- stage: `14_13d_short_regime_detector`
- goal: `test whether a Tue/Wed NY cash short-only detector can improve the 13D failure regime without breaking the better windows`
- source core: `09C_05ET_margin0700_t30_l50_m0700_h4`
- reference overlay: `13D monday=0.575, post-cash=0.6125`
- windows: `2401, 2407, 2501`
- target: `2407 / holdout_b`
- detector focus: `Tue/Wed NY cash shorts, especially NY 12:00 and 14:00`
