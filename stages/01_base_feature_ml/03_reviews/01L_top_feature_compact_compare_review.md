# 01L Top-Feature Compact Compare Review

Generated at: `2026-03-26T17:59:28.625647+00:00`

## Scope

- purpose: `compare sector-pruned compact modeling against simple top-feature-only compact variants`
- model family: `logistic_regression`
- fit split: `train`
- eval split: `valid`
- held-out test: `not touched in 01L`
- ranking source: `01D permutation importance on held-out test`

## Ranking

| variant | features | overlap with compact_36 | valid macro_f1 | delta vs full | delta vs compact_36 |
| --- | ---: | ---: | ---: | ---: | ---: |
| `compact_36_without_volatility_band__risk_proxy__leader_relative` | 36 | 36 | 0.4628 | 0.0130 | 0.0000 |
| `top_08_perm` | 8 | 6 | 0.4621 | 0.0123 | -0.0007 |
| `top_16_perm` | 16 | 10 | 0.4567 | 0.0069 | -0.0061 |
| `top_36_perm` | 36 | 22 | 0.4560 | 0.0062 | -0.0068 |
| `top_24_perm` | 24 | 15 | 0.4534 | 0.0036 | -0.0094 |
| `top_12_perm` | 12 | 8 | 0.4522 | 0.0024 | -0.0105 |
| `full_58` | 58 | 36 | 0.4498 | 0.0000 | -0.0130 |

## Read

- best top-feature-only variant: `top_08_perm` (`0.4621`)
- compact_36 advantage over best top-feature variant: `0.0007`
- compact_36 overlap with `top_08_perm`: `6` features
- `top_08_perm` is slightly worse on macro_f1 but better on valid `log_loss`, so it looks like a surprisingly competitive ultra-small baseline rather than a throwaway toy.

## Notes

- This is review-only. The ranking source comes from test-based permutation importance, so it should not be used to replace the frozen 01D handoff.
- The point here is not reselection but to check whether a very simple top-feature subset can approach the compact sector-pruned variant.

## Artifacts

- full table: `02_runs/archived/01L_run_0001_top_feature_compact_compare/top_feature_compact_results.csv`
- sorted table: `02_runs/archived/01L_run_0001_top_feature_compact_compare/top_feature_compact_sorted.csv`
- feature sets: `02_runs/archived/01L_run_0001_top_feature_compact_compare/feature_sets.json`
