# Stage 22 Selection Status

- reviewed_on: `2026-04-09`
- regular_experiment_mode: `risk_pct`
- closed_diagnostic_branch: `external_mismatch curiosity ablation reviewed; not promoted into regular experiment line`

## Current Read

- risk incumbent: `22Q_05dp_base_risk2_dirsplit_postcash_0001`
- containment challenger: `22R_05dp_psl45_qtr_h3_risk2_0001`
- keep_or_replace: `keep_incumbent`

## Why

- `22Q` keeps the best overall three-window stability after returning Stage 22 to regular risk-based execution.
- `22R` slightly improves the OOS test slice and trims OOS drawdown, but it gives back more return on `2024 historical` and `2025 validation`.
- `22S` under-fires and falls behind baseline.
- `22T` is a stronger containment variant than `22R`, but it pays slightly more non-OOS drag.

## Follow-Up Bias

- keep `22Q` as the regular Stage 22 reference
- keep `22R` as the shadow containment challenger
- do not advance mismatch-relaxation experiments into the regular line unless a new contract hypothesis appears
