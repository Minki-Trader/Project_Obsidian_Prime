# 01A Smoke Review

Generated at: `2026-03-26T14:32:25.277575+00:00`

## Summary

- horizon: `6` bars
- bands tested: `0.00075, 0.00100, 0.00125`
- baseline model: `lightgbm_multiclass`
- selection metric: `valid_macro_f1`

## Ranked Results

- `01A_run_0003_h06_band000125_lgbm`: macro_f1=0.4357, balanced_acc=0.4360, accuracy=0.4809, log_loss=1.0186
- `01A_run_0002_h06_band000100_lgbm`: macro_f1=0.4205, balanced_acc=0.4242, accuracy=0.4435, log_loss=1.0410
- `01A_run_0001_h06_band000075_lgbm`: macro_f1=0.4092, balanced_acc=0.4221, accuracy=0.4155, log_loss=1.0575

## Winner For 01B

- selected run: `01A_run_0003_h06_band000125_lgbm`
- selected band: `0.00125`
- next phase: freeze this label setup and compare learning tools in `01B`
