# 01J Calibration Diagnostics Review

Generated at: `2026-03-26T17:37:27.633966+00:00`

## Scope

- purpose: `compare probability calibration between the frozen full baseline and the recommended compact candidate`
- model family: `logistic_regression`
- fit split: `train`
- eval split: `valid`
- held-out test: `not touched in 01J`
- bins: `10`

## Overall Calibration

| model | features | log_loss | multiclass_brier | top_label_ece | mean_classwise_ece | top_label_signed_gap |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `full_58` | 58 | 1.0120 | 0.5936 | 0.0872 | 0.1661 | -0.0870 |
| `compact_36_without_volatility_band__risk_proxy__leader_relative` | 36 | 1.0043 | 0.5904 | 0.1192 | 0.1612 | -0.1192 |

## Read

- better top-label calibration: `full_58`
- better classwise calibration: `compact_36_without_volatility_band__risk_proxy__leader_relative`
- compact minus full top-label ECE: `0.0320`
- compact minus full mean classwise ECE: `-0.0049`

## Worst Top-Label Bin

- `full_58`: bin `0.8-0.9`, abs gap `0.8014`
- `compact_36_without_volatility_band__risk_proxy__leader_relative`: bin `0.5-0.6`, abs gap `0.2292`

## Notes

- Lower ECE and lower Brier are better.
- Positive signed gap means the model is overconfident on average; negative means underconfident.
- Both variants are underconfident on average here, and the compact variant is more underconfident on the top-label view.
- The `full_58` worst top-label bin comes from a one-row outlier, so this review should lean more on ECE and classwise summaries than on raw MCE-like extremes.
- This stays inside post-selection diagnostics and does not replace the frozen 01D handoff.

## Artifacts

- overall summary: `02_runs/archived/01J_run_0001_calibration_diagnostics/overall_calibration_summary.csv`
- top-label reliability: `02_runs/archived/01J_run_0001_calibration_diagnostics/top_label_reliability.csv`
- classwise reliability: `02_runs/archived/01J_run_0001_calibration_diagnostics/classwise_reliability.csv`
- classwise summary: `02_runs/archived/01J_run_0001_calibration_diagnostics/classwise_summary.csv`
