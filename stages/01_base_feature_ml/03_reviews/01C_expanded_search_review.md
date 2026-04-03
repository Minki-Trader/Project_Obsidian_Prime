# 01C Expanded Search Review

Generated at: `2026-03-26T15:00:14.890302+00:00`

## Search Scope

- horizons: `3, 6, 12`
- bands: `0.00100, 0.00125, 0.00150`
- models: `logistic_regression, lightgbm`
- selection metric: `valid_macro_f1`

## Top Results

- `01C_run_0001_h03_band000125_logreg` (logistic_regression, h=3, band=0.00125): macro_f1=0.4498, balanced_acc=0.4546, accuracy=0.5416, log_loss=1.0120
- `01C_run_0002_h03_band000125_lightgbm` (lightgbm, h=3, band=0.00125): macro_f1=0.4471, balanced_acc=0.4497, accuracy=0.5519, log_loss=0.9407
- `01C_run_0001_h03_band000100_logreg` (logistic_regression, h=3, band=0.00100): macro_f1=0.4451, balanced_acc=0.4461, accuracy=0.5083, log_loss=1.0265
- `01C_run_0001_h06_band000150_logreg` (logistic_regression, h=6, band=0.00150): macro_f1=0.4444, balanced_acc=0.4453, accuracy=0.5164, log_loss=1.0249
- `01C_run_0001_h03_band000150_logreg` (logistic_regression, h=3, band=0.00150): macro_f1=0.4434, balanced_acc=0.4592, accuracy=0.5584, log_loss=1.0075
- `01C_run_0002_h03_band000100_lightgbm` (lightgbm, h=3, band=0.00100): macro_f1=0.4428, balanced_acc=0.4436, accuracy=0.4988, log_loss=0.9947
- `01C_run_0002_h03_band000150_lightgbm` (lightgbm, h=3, band=0.00150): macro_f1=0.4406, balanced_acc=0.4486, accuracy=0.5747, log_loss=0.8975
- `01C_run_0001_h06_band000125_logreg` (logistic_regression, h=6, band=0.00125): macro_f1=0.4378, balanced_acc=0.4388, accuracy=0.4886, log_loss=1.0353
- `01C_run_0002_h06_band000150_lightgbm` (lightgbm, h=6, band=0.00150): macro_f1=0.4366, balanced_acc=0.4378, accuracy=0.5043, log_loss=0.9974
- `01C_run_0002_h06_band000125_lightgbm` (lightgbm, h=6, band=0.00125): macro_f1=0.4357, balanced_acc=0.4360, accuracy=0.4809, log_loss=1.0186

## Selection

- selected final candidate for `01D`: `01C_run_0001_h03_band000125_logreg`
- runner-up reference: `01C_run_0002_h03_band000125_lightgbm`
- archived 01C runs: `17`
