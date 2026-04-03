# 01F Sector Ablation Review

Generated at: `2026-03-26T17:18:35.087315+00:00`

## Scope

- purpose: `remove one feature sector at a time and see what actually matters`
- model family: `logistic_regression`
- fit split: `train`
- eval split: `valid`
- held-out test: `not touched in 01F`

## Full Baseline

- valid macro_f1: `0.4498`
- valid balanced_accuracy: `0.4546`
- valid accuracy: `0.5416`
- valid log_loss: `1.0120`

## Most Harmful Removals

| removed sector | delta macro_f1 vs full | delta balanced_accuracy | features removed |
| --- | ---: | ---: | ---: |
| `price_return` | -0.0045 | -0.0035 | 10 |
| `moving_average_trend` | -0.0028 | -0.0035 | 7 |
| `breadth_dispersion` | -0.0025 | -0.0027 | 2 |

## Most Helpful Removals

| removed sector | delta macro_f1 vs full | delta balanced_accuracy | features removed |
| --- | ---: | ---: | ---: |
| `volatility_band` | 0.0100 | 0.0070 | 8 |
| `risk_proxy` | 0.0033 | 0.0032 | 6 |
| `leader_relative` | 0.0024 | 0.0027 | 8 |

## Notes

- Negative delta means that sector was helping the baseline and removing it hurt validation performance.
- Positive delta means that sector may be noisy or redundant in the current Stage 01 setup.
- This is a post-selection diagnostic only. It does not replace the frozen Stage 01 final baseline.

## Artifacts

- full table: `02_runs/archived/01F_run_0001_sector_ablation/sector_ablation_results.csv`
- sorted table: `02_runs/archived/01F_run_0001_sector_ablation/sector_ablation_sorted.csv`
