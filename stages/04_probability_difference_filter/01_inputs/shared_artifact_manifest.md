# Shared Artifact Manifest

Stage 04 currently uses these shared artifacts:

- Stage 01 search-side model run:
  - `stages/01_base_feature_ml/02_runs/archived/01C_run_0001_h03_band000125_logreg`
- Stage 01 final-model run:
  - `stages/01_base_feature_ml/02_runs/active/01D_run_0001_final_h03_band000125_logreg`
- Stage 01 final selection reference:
  - `stages/01_base_feature_ml/04_selected/01D_final_stage01_selection.json`

Stage 04 fixed defaults:

- `short_threshold = 1/3`
- `long_threshold = 1/3`
- `min_margin = 0`

Important note:

- Stage 04 does not carry forward Stage 02 or Stage 03 choices.
- This stage is intentionally `probability-difference filter only`.
