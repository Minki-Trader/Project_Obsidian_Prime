# Stage 40 Runtime Parity Deep Audit

- reviewed_on: `2026-04-13`
- stage: `40_runtime_parity_deep_audit`
- ready_rows: `2216`

## Executive Read

- exact timestamp drift: `mean=0.0386` `p90=0.0827` `max=0.2012`
- best neighbor drift: `mean=0.0173` `p90=0.0384` `max=0.1399`
- improvement from best neighbor: `mean=0.0213` `p90=0.0575`
- zero-shift share: `0.2924`
- checksum parity: `exact64=0` `exact32=0` `neighbor64=0` `neighbor32=0`

## Exact Threshold Counts

- `le_0.001` `19`
- `le_0.005` `201`
- `le_0.010` `431`
- `le_0.020` `790`
- `le_0.050` `1538`
- `le_0.100` `2123`

## Shift Structure

- `shift=0` `count=648`
- `shift=-1` `count=231`
- `shift=1` `count=179`
- `shift=-2` `count=166`
- `shift=-6` `count=137`
- `shift=2` `count=122`
- `shift=-4` `count=119`
- `shift=-3` `count=117`
- `shift=-5` `count=116`
- `shift=3` `count=108`
- `shift=4` `count=105`
- `shift=6` `count=85`
- `shift=5` `count=83`

## Session Breakdown

- `ny_cash` `count=1068` `mean=0.0314` `p90=0.0698` `max=0.2012`
- `ny_late` `count=169` `mean=0.0683` `p90=0.1033` `max=0.1457`
- `ny_postcash` `count=979` `mean=0.0413` `p90=0.0837` `max=0.1774`

## High Diff Clusters

- `2026-03-23T18:10:00+00:00 -> 2026-03-23T18:15:00+00:00` `count=2` `mean=0.1977` `max=0.2012` `sessions={'ny_cash': 2}`
- `2026-03-23T17:55:00+00:00 -> 2026-03-23T18:00:00+00:00` `count=2` `mean=0.1803` `max=0.1903` `sessions={'ny_cash': 2}`
- `2026-04-02T20:20:00+00:00 -> 2026-04-02T20:45:00+00:00` `count=6` `mean=0.1638` `max=0.1774` `sessions={'ny_postcash': 6}`
- `2026-03-23T17:45:00+00:00 -> 2026-03-23T17:45:00+00:00` `count=1` `mean=0.1762` `max=0.1762` `sessions={'ny_cash': 1}`
- `2026-03-23T17:20:00+00:00 -> 2026-03-23T17:20:00+00:00` `count=1` `mean=0.1692` `max=0.1692` `sessions={'ny_cash': 1}`

## Worst Exact Rows

- `2026.03.23 18:10:00` `session=ny_cash` `exact=0.2012` `best=0.0865` `best_shift=-1` `decision=DUAL_SIGNAL_LONG_WINS`
- `2026.03.23 18:15:00` `session=ny_cash` `exact=0.1942` `best=0.0955` `best_shift=-2` `decision=DUAL_SIGNAL_LONG_WINS`
- `2026.03.23 18:00:00` `session=ny_cash` `exact=0.1903` `best=0.0905` `best_shift=1` `decision=DUAL_SIGNAL_TIE_OR_MARGIN_FAIL`
- `2026.04.02 20:30:00` `session=ny_postcash` `exact=0.1774` `best=0.0461` `best_shift=5` `decision=LONG_MARGIN_FAIL`
- `2026.03.23 17:45:00` `session=ny_cash` `exact=0.1762` `best=0.0654` `best_shift=4` `decision=DUAL_SIGNAL_TIE_OR_MARGIN_FAIL`
- `2026.03.23 17:55:00` `session=ny_cash` `exact=0.1703` `best=0.0935` `best_shift=2` `decision=DUAL_SIGNAL_TIE_OR_MARGIN_FAIL`
- `2026.04.02 20:25:00` `session=ny_postcash` `exact=0.1699` `best=0.0487` `best_shift=6` `decision=LONG_MARGIN_FAIL`
- `2026.03.23 17:20:00` `session=ny_cash` `exact=0.1692` `best=0.0532` `best_shift=-6` `decision=DUAL_SIGNAL_TIE_OR_MARGIN_FAIL`
- `2026.04.02 20:20:00` `session=ny_postcash` `exact=0.1610` `best=0.0264` `best_shift=6` `decision=DUAL_SIGNAL_TIE_OR_MARGIN_FAIL`
- `2026.04.02 20:40:00` `session=ny_postcash` `exact=0.1607` `best=0.0377` `best_shift=2` `decision=LONG_MARGIN_FAIL`

## MT5 Runtime Context

- latest no-trade rate: `0.8985`
- latest external mismatch count: `2299`
- latest skip reasons: `{'HANDLE_NOT_READY_EMA9_-1': 1, 'EXTERNAL_TIMESTAMP_MISMATCH_USDX': 396, 'SESSION_CASH_OPEN_NOT_FOUND': 3672, 'EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas': 1466, 'EXTERNAL_TIMESTAMP_MISMATCH_US10YR': 221, 'EXTERNAL_TIMESTAMP_MISMATCH_VIX': 216}`

## Interpretation

- Exact-timestamp drift remains too large to call runtime parity closed.
- Best-neighbor drift improves materially, but the winning shift is not concentrated on zero, so this is not a single-bar offset story.
- Checksum parity stays at zero under both float64-style and float32-style serialization checks, so the issue is not explained by a simple token-format mismatch.
- Drift worsens in ny_late and forms concrete March and April clusters, which points to a session-sensitive feature-surface divergence worth instrumenting directly.
