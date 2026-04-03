# 01B Model Compare Review

Generated at: `2026-03-26T14:55:26.380293+00:00`

## Frozen Label Setup

- horizon: `6` bars
- band: `0.00125`
- train rows: `34695`
- valid rows: `11756`
- test rows kept untouched for later confirmation: `6720`

## Ranked Results

- `01B_run_0004_h06_band000125_logreg` (logistic_regression): macro_f1=0.4378, balanced_acc=0.4388, accuracy=0.4886, log_loss=1.0353
- `01B_run_0001_h06_band000125_lightgbm` (lightgbm): macro_f1=0.4357, balanced_acc=0.4360, accuracy=0.4809, log_loss=1.0186
- `01B_run_0003_h06_band000125_catboost` (catboost): macro_f1=0.4355, balanced_acc=0.4352, accuracy=0.4809, log_loss=1.0198
- `01B_run_0002_h06_band000125_xgboost` (xgboost): macro_f1=0.4327, balanced_acc=0.4330, accuracy=0.4839, log_loss=1.0285

## Selected For 01C

- primary candidate: `01B_run_0004_h06_band000125_logreg`
- secondary candidate: `01B_run_0001_h06_band000125_lightgbm`
- archived this phase: `01B_run_0002_h06_band000125_xgboost, 01B_run_0003_h06_band000125_catboost`
