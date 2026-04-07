# Stage 21 Brief

- stage: `21_retrain_cadence_wfo`
- purpose: `measure rolling-refit performance changes from paired retrain cadence and trailing lookback length`
- execution mode: `Python rolling proxy on 17E thresholds and margin logic`
- windows: `2407`
- paired periods: `1D, 2D, 5D, 10D, 2W, 1M, 2M`
- period interpretation: `1D/2D/5D/10D use business-day offsets, 2W/1M/2M use calendar offsets`
