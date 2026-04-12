# Stage 37 Inputs

- base carry runs:
  - `stages/35_candle_sidecar_simplification_check/02_runs/active/35A_34d_refcarry_0001/experiment_bundle.json`
  - `stages/35_candle_sidecar_simplification_check/02_runs/active/35B_34b_simpleref_0001/experiment_bundle.json`
- bridge tester window:
  - from: `2024.01.01`
  - to: `2026.03.01`
  - read as: `2024-01-01` through `2026-02-28` inclusive

## Read Notes

- this stage keeps the logic comparison narrow:
  - current operating line `34D`
  - governance-only simplification shadow `34B`
- the only new ingredient is continuity:
  - one uninterrupted `risk_pct` account path instead of reset-by-split reads
