# Stage 41 Targeted Feature Snapshot Audit

- reviewed_on_utc: `2026-04-14T10:07:32.493779+00:00`
- snapshot_jsonl: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\Common\Files\Project_Obsidian_Prime\runtime\exp_39a_34d_bridge_ext_v1\logs\att_0004_feature_snapshot.jsonl`
- snapshot rows: `14`
- ready rows: `14`
- skip rows: `0`
- matched feature rows: `14`
- missing feature-matrix timestamps: `0`

## Executive Read

- row max abs diff: `mean=23.036015` `median=25.780024` `p90=29.049107` `max=29.672052`
- tolerance counts: `le_1e-9=0` `le_1e-6=0` `le_1e-4=0`

## Top Feature Drifts

- `atr_50` `count=14` `mean=23.036015` `p90=29.049107` `max=29.672052` `worst_ts=2026-03-23T18:15:00+00:00`
- `atr_14` `count=14` `mean=4.974894` `p90=7.292264` `max=7.598383` `worst_ts=2026-03-23T18:15:00+00:00`
- `bb_squeeze` `count=14` `mean=0.285714` `p90=1.000000` `max=1.000000` `worst_ts=2026-03-23T17:20:00+00:00`
- `stoch_kd_diff` `count=14` `mean=0.192875` `p90=0.499974` `max=0.841760` `worst_ts=2026-03-23T18:05:00+00:00`
- `atr_14_over_atr_50` `count=14` `mean=0.356427` `p90=0.380342` `max=0.387118` `worst_ts=2026-03-23T18:15:00+00:00`
- `return_1_over_atr_14` `count=14` `mean=0.030974` `p90=0.056293` `max=0.133124` `worst_ts=2026-03-23T18:05:00+00:00`
- `ema50_ema200_diff` `count=14` `mean=0.000002` `p90=0.000004` `max=0.000006` `worst_ts=2026-03-23T17:20:00+00:00`
- `ema20_ema50_diff` `count=14` `mean=0.000002` `p90=0.000003` `max=0.000003` `worst_ts=2026-03-23T17:45:00+00:00`
- `rsi_50` `count=14` `mean=0.000001` `p90=0.000002` `max=0.000002` `worst_ts=2026-04-02T20:20:00+00:00`
- `rsi_14` `count=14` `mean=0.000001` `p90=0.000001` `max=0.000002` `worst_ts=2026-04-02T20:25:00+00:00`
- `ema9_ema20_diff` `count=14` `mean=0.000000` `p90=0.000001` `max=0.000001` `worst_ts=2026-03-23T17:55:00+00:00`
- `stochrsi_kd_diff` `count=14` `mean=0.000000` `p90=0.000001` `max=0.000001` `worst_ts=2026-04-02T20:45:00+00:00`
- `rsi_14_minus_50` `count=14` `mean=0.000000` `p90=0.000000` `max=0.000000` `worst_ts=2026-03-23T17:50:00+00:00`
- `usdx_zscore_20` `count=14` `mean=0.000000` `p90=0.000000` `max=0.000000` `worst_ts=2026-04-02T20:25:00+00:00`
- `vix_zscore_20` `count=14` `mean=0.000000` `p90=0.000000` `max=0.000000` `worst_ts=2026-04-02T20:25:00+00:00`
- `rsi_14_slope_3` `count=14` `mean=0.000000` `p90=0.000000` `max=0.000000` `worst_ts=2026-03-23T17:20:00+00:00`
- `us10yr_zscore_20` `count=14` `mean=0.000000` `p90=0.000000` `max=0.000000` `worst_ts=2026-03-23T18:10:00+00:00`
- `close_ema50_ratio` `count=14` `mean=0.000000` `p90=0.000000` `max=0.000000` `worst_ts=2026-03-23T18:15:00+00:00`
- `sma50_sma200_ratio` `count=14` `mean=0.000000` `p90=0.000000` `max=0.000000` `worst_ts=2026-03-23T18:00:00+00:00`
- `close_ema20_ratio` `count=14` `mean=0.000000` `p90=0.000000` `max=0.000000` `worst_ts=2026-04-02T20:40:00+00:00`

## Worst Rows

- `2026.03.23 18:15:00` `ready=True` `skip=n/a` `matched=54` `max=29.672052` `mean=0.702121` `top=atr_50=29.672052; atr_14=7.598383; atr_14_over_atr_50=0.387118; stoch_kd_diff=0.225085; return_1_over_atr_14=0.031865`
- `2026.03.23 18:00:00` `ready=True` `skip=n/a` `matched=54` `max=29.067683` `mean=0.684118` `top=atr_50=29.067683; atr_14=6.862405; stoch_kd_diff=0.617783; atr_14_over_atr_50=0.379435; return_1_over_atr_14=0.015072`
- `2026.03.23 18:10:00` `ready=True` `skip=n/a` `matched=54` `max=29.005764` `mean=0.674908` `top=atr_50=29.005764; atr_14=6.957050; atr_14_over_atr_50=0.379575; stoch_kd_diff=0.098165; return_1_over_atr_14=0.004448`
- `2026.03.23 17:55:00` `ready=True` `skip=n/a` `matched=54` `max=28.616104` `mean=0.629001` `top=atr_50=28.616104; atr_14=4.854016; atr_14_over_atr_50=0.359097; stoch_kd_diff=0.099738; return_1_over_atr_14=0.037096`
- `2026.03.23 18:05:00` `ready=True` `skip=n/a` `matched=54` `max=28.333230` `mean=0.680183` `top=atr_50=28.333230; atr_14=7.041108; stoch_kd_diff=0.841760; atr_14_over_atr_50=0.380671; return_1_over_atr_14=0.133124`
- `2026.03.23 17:50:00` `ready=True` `skip=n/a` `matched=54` `max=27.786638` `mean=0.571911` `top=atr_50=27.786638; atr_14=2.659548; atr_14_over_atr_50=0.332680; stoch_kd_diff=0.085395; return_1_over_atr_14=0.018915`
- `2026.03.23 17:45:00` `ready=True` `skip=n/a` `matched=54` `max=27.473918` `mean=0.520393` `top=atr_50=27.473918; atr_14_over_atr_50=0.302903; atr_14=0.244072; stoch_kd_diff=0.079361; return_1_over_atr_14=0.000958`
- `2026.03.23 17:20:00` `ready=True` `skip=n/a` `matched=54` `max=24.086129` `mean=0.611891` `top=atr_50=24.086129; atr_14=7.399902; bb_squeeze=1.000000; atr_14_over_atr_50=0.374247; stoch_kd_diff=0.117288`
- `2026.04.02 20:35:00` `ready=True` `skip=n/a` `matched=54` `max=16.890506` `mean=0.414108` `top=atr_50=16.890506; atr_14=3.971072; bb_squeeze=1.000000; atr_14_over_atr_50=0.345549; stoch_kd_diff=0.122400`
- `2026.04.02 20:40:00` `ready=True` `skip=n/a` `matched=54` `max=16.770596` `mean=0.410191` `top=atr_50=16.770596; atr_14=3.897884; bb_squeeze=1.000000; atr_14_over_atr_50=0.337617; stoch_kd_diff=0.136210`
- `2026.04.02 20:30:00` `ready=True` `skip=n/a` `matched=54` `max=16.548476` `mean=0.390517` `top=atr_50=16.548476; atr_14=4.102089; atr_14_over_atr_50=0.348037; stoch_kd_diff=0.069672; return_1_over_atr_14=0.019648`
- `2026.04.02 20:45:00` `ready=True` `skip=n/a` `matched=54` `max=16.495887` `mean=0.435305` `top=atr_50=16.495887; atr_14=5.485534; bb_squeeze=1.000000; atr_14_over_atr_50=0.358964; stoch_kd_diff=0.131986`
- `2026.04.02 20:25:00` `ready=True` `skip=n/a` `matched=54` `max=16.076508` `mean=0.373451` `top=atr_50=16.076508; atr_14=3.729449; atr_14_over_atr_50=0.342383; return_1_over_atr_14=0.014818; stoch_kd_diff=0.003191`
- `2026.04.02 20:20:00` `ready=True` `skip=n/a` `matched=54` `max=15.680720` `mean=0.388508` `top=atr_50=15.680720; atr_14=4.846000; atr_14_over_atr_50=0.361699; stoch_kd_diff=0.072216; return_1_over_atr_14=0.018782`

## External Telemetry

- `AAPL.xnas` `exact_match=14`
- `AMD.xnas` `exact_match=14`
- `AMZN.xnas` `exact_match=14`
- `GOOGL.xnas` `exact_match=14`
- `META.xnas` `exact_match=14`
- `MSFT.xnas` `exact_match=14`
- `NVDA.xnas` `exact_match=14`
- `TSLA.xnas` `exact_match=14`
- `US10YR` `exact_match=14`
- `USDX` `exact_match=14`
- `VIX` `exact_match=14`

## Interpretation

- Use the top feature drift table to identify the first exact-timestamp mismatch before touching model logic.
- Use the external telemetry breakdown to decide whether the first divergence is driven by exact-match failures, stale fallback, or a downstream derived-feature calculation gap.
