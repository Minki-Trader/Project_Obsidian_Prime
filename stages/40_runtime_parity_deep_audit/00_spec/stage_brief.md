# Stage 40 Runtime Parity Deep Audit

- stage: `40_runtime_parity_deep_audit`
- stage_type: `diagnostic_runtime_stage`
- current_wave: `wave1_completed`
- owner_path: `stages/40_runtime_parity_deep_audit/`

## Purpose

- reopen the Python-to-MT5 parity question using the fresh Stage 39 latest-window MT5 shadow logs instead of the older Stage 34 handoff sample alone
- measure whether the remaining drift is an exact-timestamp mismatch, a simple bar offset, or a broader runtime feature-surface divergence
- leave alpha selection untouched while making the next runtime-debug target concrete

## Inputs

- Stage 39 latest shadow log and tester attempt metadata from `39A_34d_bridge_ext_0001`
- shared extended-window feature matrix on the `US100` base frame
- current `34D` ONNX model and feature schema from the verified Stage 34 bundle lineage

## Evaluation Read

- treat this as a diagnostic-only stage; do not use it to promote or demote alpha variants
- focus on exact probability drift, best-neighbor drift, checksum parity, shift concentration, session concentration, and cluster localization
- if checksum parity stays at zero, turn the result into a concrete runtime-debug brief instead of repeating broad proxy checks

## Expected Outputs

- `03_reviews/stage40_runtime_parity_deep_audit_20260413.json`
- `03_reviews/stage40_runtime_parity_deep_audit_20260413.md`
- `04_selected/selection_status.md`
