# Stage 41 Targeted Feature Snapshot Audit

- stage: `41_targeted_feature_snapshot_audit`
- updated_on: `2026-04-14`
- current_wave: `wave0_scaffolded`
- stage_type: `diagnostic_runtime_stage`
- inherited_regular_reference: `34D_29s_outbarlong_0001`
- inherited_runtime_surface: `exp_39a_34d_bridge_ext_v1`

## Purpose

- turn the Stage 40 parity brief into a direct per-feature audit on the same MT5 timestamps
- capture MT5-side ordered feature vectors, external-series timestamps, fallback state, and skip context on the localized drift windows
- compare MT5 feature values against the shared Python feature surface before touching alpha logic, simplification, or retraining

## Scope

- keep alpha selection frozen on `34D`
- instrument the shared MT5 shadow EA so the targeted windows emit `feature snapshot` JSONL rows
- route the snapshot log through the shared bundle tester path so each attempt keeps the artifact next to the shadow log
- analyze exact timestamp feature deltas, worst rows, and external-input status concentration

## Evaluation Rules

- diagnostic-only stage; do not use this stage alone to promote or demote model/rule variants
- prefer exact-timestamp feature comparisons over fresh probability-only proxy checks
- keep skip rows visible when they occur inside the audit windows, but prioritize ready-row feature mismatch localization first
- treat external timestamp status and stale-fallback state as first-class audit context, not as side notes

## Initial Target Windows

- `2026.03.23 17:20:00`
- `2026.03.23 17:45:00..2026.03.23 18:15:00`
- `2026.04.02 20:20:00..2026.04.02 20:45:00`

## Expected Outputs

- `03_reviews/analyze_stage41_targeted_feature_snapshot_audit.py`
- `03_reviews/stage41_targeted_feature_snapshot_audit_<date>.json`
- `03_reviews/stage41_targeted_feature_snapshot_audit_<date>.md`
- `04_selected/selection_status.md`
