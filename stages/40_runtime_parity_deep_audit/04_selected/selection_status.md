# Stage 40 Selection Status

- reviewed_on: `2026-04-13`
- stage: `40_runtime_parity_deep_audit`
- stage_type: `diagnostic_runtime_stage`
- inherited_regular_reference: `34D_29s_outbarlong_0001`
- inherited_runtime_surface: `exp_39a_34d_bridge_ext_v1 att_0003`

## Current Read

- parity_status: `still_open_after_latest_mt5_shadow_audit`
- working_read: `the fresh Stage 39 MT5 logs prove the runtime surface exists through 2026-04-12, but exact Python-to-MT5 parity is still not recovered and the drift does not look like a single fixed shift`

## Promotion Gates

- this stage is diagnostic-only
- do not claim parity closure from best-neighbor improvement alone
- do not reopen alpha search, simplification, or retraining from this stage alone
- require direct feature-vector dumps on the same timestamps before treating the runtime mismatch as understood

## Scoreboards

- regular_risk_execution: `reuse the Stage 39 live-like runtime evidence only; Stage 40 adds no new alpha scoreboard`
- structural_scout: `not used`

## Headline

- exact drift across all latest ready rows stayed material:
  - `count=2216`
  - `mean=0.0386`
  - `p90=0.0827`
  - `max=0.2012`
- best-neighbor drift improved, but did not close the gap:
  - `mean=0.0173`
  - `p90=0.0384`
  - `max=0.1399`
- zero-shift share was only `0.2924` (`648 / 2216`)

## Risk

- runtime-integrity risk is concentrated, not uniform:
  - `2026-03-23 17:20 UTC`
  - `2026-03-23 17:45 -> 18:15 UTC`
  - `2026-04-02 20:20 -> 20:45 UTC`
- latest MT5 runtime still carried a very high skip-heavy surface:
  - `no_trade_rate=0.8985`
  - `external_mismatch_count=2299`

## Diagnostics

- best-shift structure stayed broad across `-6 .. +6` bars rather than collapsing onto one offset
- checksum parity remained zero under every simple serialization check:
  - `exact_float64=0`
  - `exact_float32=0`
  - `neighbor_float64=0`
  - `neighbor_float32=0`
- session concentration points to a runtime-feature construction issue, not a broad random drift:
  - `ny_cash mean=0.0314`
  - `ny_late mean=0.0683`
  - `ny_postcash mean=0.0413`

## Execution

- latest skip-reason context from the same MT5 runtime:
  - `SESSION_CASH_OPEN_NOT_FOUND=3672`
  - `EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas=1466`
  - `EXTERNAL_TIMESTAMP_MISMATCH_USDX=396`
  - `EXTERNAL_TIMESTAMP_MISMATCH_US10YR=221`
  - `EXTERNAL_TIMESTAMP_MISMATCH_VIX=216`
  - `HANDLE_NOT_READY_EMA9_-1=1`

## Decision

- keep `34D_29s_outbarlong_0001` as the live regular lane
- keep Stage 39 as the latest continuity and MT5-attached runtime evidence
- open the next runtime-debug cycle as a targeted feature-snapshot audit, not as a new model or rule experiment

## Follow-Up Bias

- add MT5-side full ordered feature-vector dumping for exact audit bars instead of checksum-only logging
- start with the localized cluster windows first:
  - `2026-03-23 17:20 UTC`
  - `2026-03-23 17:45 -> 18:15 UTC`
  - `2026-04-02 20:20 -> 20:45 UTC`
- capture external-series timestamps and stale/readiness state together with the dumped feature vector
- compare per-feature Python vs MT5 deltas before touching alpha logic again

## Report Refs

- `03_reviews/stage40_runtime_parity_deep_audit_20260413.md`
- `03_reviews/stage40_runtime_parity_deep_audit_20260413.json`
- `../01_inputs/input_refs.md`
- `../../39_window_extension_mt5_validation/03_reviews/stage39_extended_validation_20260413.md`
