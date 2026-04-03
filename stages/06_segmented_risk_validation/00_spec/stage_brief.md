# Stage 06 Brief

- stage: `06_segmented_risk_validation`
- purpose: `apply EA-side risk overlays to selected Stage 05 logic references and evaluate them with independent segmented validation/holdout result packages`
- current focus: `05GK direction-split stop policy transplanted onto the 05DP model base at 2.0% broker-native risk`
- source family: `Stage 05 05DP risk-aware direction-split leader configuration`
- runtime rule: `broker-native SL, risk_pct overlay, independent segmented result export`
- split policy:
  - `validation`: `2025-01-01` through `2025-09-30`
  - `holdout`: `2025-10-01` through `2026-02-28`
- segment policy:
  - `validation_q1`: `2025-01-01` through `2025-03-31`
  - `validation_q2`: `2025-04-01` through `2025-06-30`
  - `validation_q3`: `2025-07-01` through `2025-09-30`
  - `holdout_a`: `2025-10-01` through `2025-11-15`
  - `holdout_b`: `2025-11-16` through `2025-12-31`
  - `holdout_c`: `2026-01-01` through `2026-02-28`
- result policy: `keep experiment_bundle split summaries as run-local artifacts, and emit segmented overlay results as independent Stage 06 review artifacts`
