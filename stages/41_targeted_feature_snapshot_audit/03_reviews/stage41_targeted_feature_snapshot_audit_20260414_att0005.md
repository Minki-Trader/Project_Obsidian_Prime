# Stage 41 Targeted Feature Snapshot Audit

- reviewed_on_utc: `2026-04-14T10:17:46.763402+00:00`
- snapshot_jsonl: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\Common\Files\Project_Obsidian_Prime\runtime\exp_39a_34d_bridge_ext_v1\logs\att_0005_feature_snapshot.jsonl`
- snapshot rows: `14`
- ready rows: `14`
- skip rows: `0`
- matched feature rows: `14`
- missing feature-matrix timestamps: `0`

## Executive Read

- row max abs diff: `mean=0.000003` `median=0.000002` `p90=0.000004` `max=0.000006`
- tolerance counts: `le_1e-9=0` `le_1e-6=0` `le_1e-4=14`

## Top Feature Drifts

- `ema50_ema200_diff` `count=14` `mean=0.000002` `p90=0.000004` `max=0.000006` `worst_ts=2026-03-23T17:20:00+00:00`
- `ema20_ema50_diff` `count=14` `mean=0.000002` `p90=0.000003` `max=0.000003` `worst_ts=2026-03-23T17:45:00+00:00`
- `atr_14` `count=14` `mean=0.000001` `p90=0.000002` `max=0.000002` `worst_ts=2026-03-23T17:50:00+00:00`
- `rsi_50` `count=14` `mean=0.000001` `p90=0.000002` `max=0.000002` `worst_ts=2026-04-02T20:20:00+00:00`
- `rsi_14` `count=14` `mean=0.000001` `p90=0.000001` `max=0.000002` `worst_ts=2026-04-02T20:25:00+00:00`
- `atr_50` `count=14` `mean=0.000001` `p90=0.000002` `max=0.000002` `worst_ts=2026-04-02T20:45:00+00:00`
- `ema9_ema20_diff` `count=14` `mean=0.000000` `p90=0.000001` `max=0.000001` `worst_ts=2026-03-23T17:55:00+00:00`
- `stochrsi_kd_diff` `count=14` `mean=0.000000` `p90=0.000001` `max=0.000001` `worst_ts=2026-04-02T20:45:00+00:00`
- `rsi_14_minus_50` `count=14` `mean=0.000000` `p90=0.000000` `max=0.000000` `worst_ts=2026-03-23T17:50:00+00:00`
- `stoch_kd_diff` `count=14` `mean=0.000000` `p90=0.000000` `max=0.000000` `worst_ts=2026-03-23T18:15:00+00:00`
- `usdx_zscore_20` `count=14` `mean=0.000000` `p90=0.000000` `max=0.000000` `worst_ts=2026-04-02T20:25:00+00:00`
- `vix_zscore_20` `count=14` `mean=0.000000` `p90=0.000000` `max=0.000000` `worst_ts=2026-04-02T20:25:00+00:00`
- `rsi_14_slope_3` `count=14` `mean=0.000000` `p90=0.000000` `max=0.000000` `worst_ts=2026-03-23T17:20:00+00:00`
- `us10yr_zscore_20` `count=14` `mean=0.000000` `p90=0.000000` `max=0.000000` `worst_ts=2026-03-23T18:10:00+00:00`
- `atr_14_over_atr_50` `count=14` `mean=0.000000` `p90=0.000000` `max=0.000000` `worst_ts=2026-04-02T20:25:00+00:00`
- `close_ema50_ratio` `count=14` `mean=0.000000` `p90=0.000000` `max=0.000000` `worst_ts=2026-03-23T18:15:00+00:00`
- `sma50_sma200_ratio` `count=14` `mean=0.000000` `p90=0.000000` `max=0.000000` `worst_ts=2026-03-23T18:00:00+00:00`
- `close_ema20_ratio` `count=14` `mean=0.000000` `p90=0.000000` `max=0.000000` `worst_ts=2026-04-02T20:40:00+00:00`
- `return_1_over_atr_14` `count=14` `mean=0.000000` `p90=0.000000` `max=0.000000` `worst_ts=2026-03-23T18:05:00+00:00`
- `close_open_ratio` `count=14` `mean=0.000000` `p90=0.000000` `max=0.000000` `worst_ts=2026-03-23T17:50:00+00:00`

## Worst Rows

- `2026.03.23 17:20:00` `ready=True` `skip=n/a` `matched=54` `max=0.000006` `mean=0.000000` `top=ema50_ema200_diff=0.000006; atr_14=0.000001; ema9_ema20_diff=0.000001; ema20_ema50_diff=0.000001; rsi_50=0.000001`
- `2026.03.23 18:15:00` `ready=True` `skip=n/a` `matched=54` `max=0.000005` `mean=0.000000` `top=ema50_ema200_diff=0.000005; ema20_ema50_diff=0.000003; atr_50=0.000002; rsi_50=0.000001; atr_14=0.000001`
- `2026.03.23 17:55:00` `ready=True` `skip=n/a` `matched=54` `max=0.000004` `mean=0.000000` `top=ema50_ema200_diff=0.000004; ema20_ema50_diff=0.000002; rsi_50=0.000002; atr_50=0.000001; atr_14=0.000001`
- `2026.03.23 17:45:00` `ready=True` `skip=n/a` `matched=54` `max=0.000003` `mean=0.000000` `top=ema20_ema50_diff=0.000003; ema50_ema200_diff=0.000003; rsi_50=0.000002; atr_50=0.000002; rsi_14=0.000001`
- `2026.03.23 18:00:00` `ready=True` `skip=n/a` `matched=54` `max=0.000002` `mean=0.000000` `top=ema20_ema50_diff=0.000002; atr_14=0.000002; rsi_14=0.000001; atr_50=0.000001; ema50_ema200_diff=0.000000`
- `2026.03.23 17:50:00` `ready=True` `skip=n/a` `matched=54` `max=0.000002` `mean=0.000000` `top=ema20_ema50_diff=0.000002; atr_14=0.000002; rsi_14=0.000001; ema50_ema200_diff=0.000001; rsi_14_minus_50=0.000000`
- `2026.04.02 20:30:00` `ready=True` `skip=n/a` `matched=54` `max=0.000002` `mean=0.000000` `top=ema50_ema200_diff=0.000002; ema20_ema50_diff=0.000002; atr_50=0.000001; rsi_14=0.000001; atr_14=0.000001`
- `2026.04.02 20:25:00` `ready=True` `skip=n/a` `matched=54` `max=0.000002` `mean=0.000000` `top=ema20_ema50_diff=0.000002; rsi_14=0.000002; ema50_ema200_diff=0.000002; atr_14=0.000002; atr_50=0.000001`
- `2026.04.02 20:20:00` `ready=True` `skip=n/a` `matched=54` `max=0.000002` `mean=0.000000` `top=rsi_50=0.000002; ema50_ema200_diff=0.000002; atr_14=0.000002; atr_50=0.000002; ema9_ema20_diff=0.000000`
- `2026.03.23 18:10:00` `ready=True` `skip=n/a` `matched=54` `max=0.000002` `mean=0.000000` `top=ema20_ema50_diff=0.000002; ema50_ema200_diff=0.000001; atr_50=0.000001; stochrsi_kd_diff=0.000001; atr_14=0.000001`
- `2026.04.02 20:45:00` `ready=True` `skip=n/a` `matched=54` `max=0.000002` `mean=0.000000` `top=atr_50=0.000002; rsi_50=0.000001; ema20_ema50_diff=0.000001; rsi_14=0.000001; stochrsi_kd_diff=0.000001`
- `2026.04.02 20:35:00` `ready=True` `skip=n/a` `matched=54` `max=0.000002` `mean=0.000000` `top=ema50_ema200_diff=0.000002; atr_50=0.000001; rsi_50=0.000001; atr_14=0.000001; rsi_14=0.000001`
- `2026.04.02 20:40:00` `ready=True` `skip=n/a` `matched=54` `max=0.000002` `mean=0.000000` `top=rsi_50=0.000002; atr_50=0.000002; atr_14=0.000001; stochrsi_kd_diff=0.000001; rsi_14=0.000001`
- `2026.03.23 18:05:00` `ready=True` `skip=n/a` `matched=54` `max=0.000001` `mean=0.000000` `top=rsi_50=0.000001; atr_14=0.000001; ema50_ema200_diff=0.000001; ema9_ema20_diff=0.000001; rsi_14_minus_50=0.000000`

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
