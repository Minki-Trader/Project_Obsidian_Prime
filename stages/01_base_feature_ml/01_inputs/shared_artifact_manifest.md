# Shared Artifact Manifest

## Contract Documents

- `docs/contracts/feature_calculation_spec_fpmarkets_v2.md`
- `docs/contracts/python_feature_parser_spec_fpmarkets_v2.md`
- `docs/contracts/mt5_ea_input_order_contract_fpmarkets_v2.md`

## Context Documents

- `docs/context/Base_fpmarkets_v2.txt`
- `docs/context/migration_note_fpmarkets_v2.md`

## Shared Data Inputs

- `data/processed/fpmarkets_v2/features/extended_window/feature_matrix.parquet`
  - current 58-feature matrix on the full `US100` M5 base frame
- `data/processed/fpmarkets_v2/features/extended_window/feature_validity.parquet`
  - row-level validity mask for the feature matrix
- `data/processed/fpmarkets_v2/features/extended_window/feature_build_summary.json`
  - current feature build summary and counts

## Supporting Audit Artifacts

- `data/processed/fpmarkets_v2/m5_intersection/extended_window/fpmarkets_v2_m5_intersection_2022-08-01_2026-02-28_summary.json`
- `foundation/reports/us100_real_tick_window_review.md`
- `foundation/reports/external_m5_symbol_coverage.md`
- `foundation/reports/m5_intersection_alignment.md`
- `foundation/reports/feature_dataset_build.md`

## Shared Config

- `foundation/config/top3_monthly_weights_fpmarkets_v2.csv`
  - current placeholder monthly weights for the top3 aggregate feature

## Stage 01 Usage Rule

- reference shared inputs from here
- do not copy raw or processed datasets into this stage
- create stage-local derived artifacts only when they are specific to a label, split, or experiment run
