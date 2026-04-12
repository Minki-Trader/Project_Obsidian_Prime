# Stage 39 Selection Status

- reviewed_on: `2026-04-13`
- stage: `39_window_extension_mt5_validation`
- stage_type: `diagnostic_runtime_validation_stage`
- inherited_regular_reference: `34D_29s_outbarlong_0001`
- inherited_regular_shadow: `34B_29s_refcarry_0001`

## Current Read

- extended_window_status: `wave1_completed`
- shared_window_override: `2022-08-01 .. 2026-04-12 inclusive`
- continuity_read: `34D_still_leads_34B_on_extended_mt5_bridge`
- parity_audit_status: `fresh_mt5_logs_opened_exact_checksum_parity_still_unresolved`

## Promotion Gates

- this stage is diagnostic-only
- keep the frozen split scoreboard untouched
- use this stage to answer:
  - whether the latest closed-bar extension changes the bridge continuity read
  - whether we now have fresh current-date MT5 logs for the next parity audit step

## Scoreboards

- regular_risk_execution: `completed`
- structural_scout: `not used`

## Headline

- `39A 34D` extended bridge: `net=2950.79` `return_pct=590.158` `pf=1.3025` `trade_count=1134`
- `39B 34B` extended bridge: `net=2842.86` `return_pct=568.572` `pf=1.3010` `trade_count=1134`
- `34D minus 34B`: `net=+107.93` `return_pct=+21.586` `pf=+0.0015`

## Risk

- `34D` kept the lead with only a small risk tax: `max_dd_pct_delta=+0.0319` `ulcer_delta=+0.0601`
- worst week was slightly worse on `34D`: `-427.10` versus `-412.52`
- external mismatch pressure stayed identical across both bridge runs: `53733`

## Diagnostics

- calendar attribution stayed positive in every carried bucket:
  - `2024 net delta=+34.50`
  - `2025 net delta=+43.65`
  - `2026_ytd net delta=+29.78`
- bridge trade count stayed identical at `1134`, so the edge remains mostly a trade-quality delta rather than a participation delta
- expectancy stayed slightly better on `34D`: `long_delta=+0.1040` `short_delta=+0.0867`

## Execution

- latest shadow audit window: `2026.03.01 -> 2026.04.13`
- fresh MT5 current-date runtime logs now exist: `ready_rows=2216` `external_mismatch_count=2299` `no_trade_rate=0.8985`
- proxy parity sample over the latest `100` ready rows improved versus the older Stage 38 proxy read: `mean_max_abs=0.0258` `p90=0.0448` `max=0.0965`
- exact feature checksum parity is still unresolved: `exact_checksum_matches=0` `best_neighbor_checksum_matches=0`
- first `39A att_0001` failed only because an already-open plain GUI terminal prevented the scripted tester launch from producing logs; rerunning with an exclusive launch succeeded

## Decision

- keep `34D` as the live regular lane
- treat the window extension as continuity evidence, not as permission to reopen blanket simplification or broad retraining
- treat the fresh `39A att_0003` logs as the new starting surface for the real Python-to-MT5 parity audit

## Follow-Up Bias

- keep the Stage 38 packaging priorities in front: critical-protection-event panel and `34B vs 34D` delta explanation panel
- use the new `2026-03-01 .. 2026-04-12` MT5 logs to chase exact feature checksum alignment next
- do not reopen broad retraining, blanket simplification, or broader window growth beyond `2026-04-12` without a separate decision

## Report Refs

- `03_reviews/stage39_extended_validation_20260413.md`
- `03_reviews/stage39_extended_validation_20260413.json`
