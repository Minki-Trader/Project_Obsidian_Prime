# Stage 28 Retrain Feature Checks

- stage: `28_retrain_feature_checks`
- updated_on: `2026-04-10`
- current_wave: `wave2_event_triggered_retrain`
- roadmap_anchor: `Stage 28 event-triggered retrain and feature simplification checks`

## Purpose

- reopen the `17E/18E` lineage only as a bounded check, not as an automatic replacement path for the current `27A` operating reference
- test whether the old Stage 16-style feature simplification ideas behave differently once they are applied to the stronger `17E + 18E(PH20)` lineage
- keep the overlay and risk-execution contract fixed while only changing the model feature subset

## Wave 1 Scope

- source core model family: `17E_2501_ovr_balanced_0001`
- source practical overlay: `18E_2501_17e_ph20_0001`
- execution style: `risk_pct`, `direction_split ATR stop`, `PH20 postcash hold-cut`
- comparison lane:
  - `28A` full `54`-feature `17E` reference rebuilt under the Stage 18 practical overlay
  - `28B` persistence-only compact fork
  - `28C` sessionless compact fork
  - `28D` external-breadthless compact fork

## Wave 2 Scope

- use `28B_18e_persist48_ph20_0001` as the reopened compact lineage anchor
- compare three stitched long-window reads on `2025-01-01 <= t < 2026-03-01`:
  - `28E` fixed carry of the compact lineage
  - `28F` blind monthly `2M` retrain of the compact lineage
  - `28G` bounded month-level event-trigger retrain using `prev_month_return < 0 or PF < 1`
- keep this wave inside the lineage lane only; do not treat it as a direct operating replacement path for `27A`

## Evaluation Rules

- use the standard fixed chronology:
  - `hist_2024`: `2024-01-01` through `2024-12-31`
  - `validation`: `2025-01-01` through `2025-09-30`
  - `test`: `2025-10-01` through `2026-02-28`
- keep governance telemetry enabled in observe-only mode during MT5 execution
- treat this wave as a `lineage check`, not as a direct promotion stage over `27A`
- only reopen the `18E` branch for further work if a compact arm beats the rebuilt `28A` full-reference arm without creating a worse cross-split drag profile

## Current Read

- `28B` was good enough to reopen the lineage, but the retrain add-on was not
- `28E` fixed carry is now the internal stitched reference for the reopened compact branch
- `28F` blind monthly retrain repeated the broad Stage 21 failure pattern
- `28G` event-trigger retrain was less bad than blind monthly retrain, but still clearly worse than `28E`
