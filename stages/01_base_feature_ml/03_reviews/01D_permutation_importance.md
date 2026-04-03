# 01D Permutation Importance Review

Generated at: `2026-03-26T15:36:33.674670+00:00`

## Scope

- run: `01D_run_0001_final_h03_band000125_logreg`
- model: `logistic_regression`
- split: `test`
- scoring: `macro_f1`
- repeats: `20`

## Base Test Metrics

- macro_f1: `0.4581`
- balanced_accuracy: `0.4694`
- accuracy: `0.5769`
- log_loss: `0.9728`

## Top Features

| rank | feature | mean drop in macro_f1 | std |
| --- | --- | ---: | ---: |
| 1 | `atr_50` | 0.063509 | 0.003504 |
| 2 | `ema9_ema20_diff` | 0.060755 | 0.004723 |
| 3 | `close_ema20_ratio` | 0.039010 | 0.005108 |
| 4 | `close_ema50_ratio` | 0.035387 | 0.003711 |
| 5 | `ema20_ema50_diff` | 0.034871 | 0.004548 |
| 6 | `ema50_ema200_diff` | 0.027913 | 0.003497 |
| 7 | `historical_vol_20` | 0.023930 | 0.003489 |
| 8 | `hl_range` | 0.019493 | 0.003894 |
| 9 | `return_1_over_atr_14` | 0.017282 | 0.002355 |
| 10 | `top3_weighted_return_1` | 0.015411 | 0.003261 |
| 11 | `log_return_1` | 0.014367 | 0.003911 |
| 12 | `atr_14_over_atr_50` | 0.013892 | 0.002888 |
| 13 | `nvda_xnas_log_return_1` | 0.013871 | 0.004736 |
| 14 | `trix_15` | 0.013403 | 0.004096 |
| 15 | `atr_14` | 0.012402 | 0.003813 |

## Interpretation

- Higher mean drop means the model loses more test macro_f1 when that feature is shuffled.
- This is a better practical proxy for feature contribution than raw coefficients alone.
- Near-zero or negative values usually mean the feature adds little stable test-time value on its own.

## Artifacts

- full csv: `stages\01_base_feature_ml\03_reviews\01D_permutation_importance.csv`
- summary json: `stages\01_base_feature_ml\03_reviews\01D_permutation_importance.json`
