# 01G Sector Combo Pruning Review

Generated at: `2026-03-26T17:22:04.986017+00:00`

## Scope

- purpose: `test whether the helpful single-sector removals from 01F still help when combined`
- model family: `logistic_regression`
- fit split: `train`
- eval split: `valid`
- held-out test: `not touched in 01G`
- candidate sectors from 01F: `volatility_band, risk_proxy, leader_relative`

## Full Baseline

- valid macro_f1: `0.4498`
- valid balanced_accuracy: `0.4546`
- valid accuracy: `0.5416`
- valid log_loss: `1.0120`

## Best Single

| removed sectors | delta macro_f1 vs full | delta balanced_accuracy | removed feature count |
| --- | ---: | ---: | ---: |
| `volatility_band` | 0.0100 | 0.0070 | 8 |

## Best Pair

| removed sectors | delta macro_f1 vs full | delta balanced_accuracy | removed feature count |
| --- | ---: | ---: | ---: |
| `volatility_band,leader_relative` | 0.0125 | 0.0096 | 16 |

## Triple Cut

| removed sectors | delta macro_f1 vs full | delta balanced_accuracy | removed feature count |
| --- | ---: | ---: | ---: |
| `volatility_band,risk_proxy,leader_relative` | 0.0130 | 0.0103 | 22 |

## Top Overall Variants

| removed sectors | combo size | delta macro_f1 vs full | delta balanced_accuracy | delta accuracy |
| --- | ---: | ---: | ---: | ---: |
| `volatility_band,risk_proxy,leader_relative` | 3 | 0.0130 | 0.0103 | 0.0253 |
| `volatility_band,leader_relative` | 2 | 0.0125 | 0.0096 | 0.0246 |
| `volatility_band,risk_proxy` | 2 | 0.0101 | 0.0073 | 0.0231 |
| `volatility_band` | 1 | 0.0100 | 0.0070 | 0.0234 |
| `risk_proxy,leader_relative` | 2 | 0.0038 | 0.0038 | 0.0031 |

## Notes

- This phase stays inside post-selection diagnostics and does not replace the frozen Stage 01 final baseline.
- Strong pair or triple gains suggest a compact variant worth revisiting later as a dedicated compact-model phase.
- Weak pair or triple gains suggest the single-sector improvement was local and should not be over-read.

## Artifacts

- full table: `02_runs/archived/01G_run_0001_sector_combo_pruning/sector_combo_results.csv`
- sorted table: `02_runs/archived/01G_run_0001_sector_combo_pruning/sector_combo_sorted.csv`
