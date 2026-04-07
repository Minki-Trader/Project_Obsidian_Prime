# Stage Brief

- stage: `09_05et_local_probe`
- goal: `run a narrow strict-retrain WFO local probe around 05ET to improve the 2407 holdout_b segment`
- windows: `2401, 2407, 2501`
- target segment: `2407 / holdout_b`
- local probe axes: `short_threshold, long_threshold, min_margin, max_hold_bars`
- ranking focus: `2407 holdout_b first, then worst holdout_b, then average test return`
