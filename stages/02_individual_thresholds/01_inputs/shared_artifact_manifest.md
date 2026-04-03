# Shared Artifact Manifest

## Search Source

- Stage 01 search-side candidate: `stages/01_base_feature_ml/02_runs/archived/01C_run_0001_h03_band000125_logreg`
- Stage 01 frozen final handoff: `stages/01_base_feature_ml/04_selected/01D_final_stage01_selection.json`

## Dataset

- shared dataset: `stages/01_base_feature_ml/01_inputs/stage01c_h03_band000125_dataset.parquet`

## Contract References

- `docs/context/Base_fpmarkets_v2.txt`
- `docs/contracts/mt5_ea_input_order_contract_fpmarkets_v2.md`

## Note

Stage 02 is threshold-only.
`min_margin` or any probability-gap logic should not be introduced here.
