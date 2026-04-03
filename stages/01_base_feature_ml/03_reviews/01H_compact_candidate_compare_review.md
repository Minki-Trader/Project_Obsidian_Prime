# 01H Compact Candidate Compare Review

Generated at: `2026-03-26T17:25:16.752154+00:00`

## Scope

- purpose: `compare the strongest compact candidates from 01G against the frozen full baseline`
- model family: `logistic_regression`
- fit split: `train`
- eval split: `valid`
- held-out test: `not touched in 01H`

## Ranking

| variant | features | removed sectors | valid macro_f1 | delta vs full | train-valid macro_f1 gap |
| --- | ---: | --- | ---: | ---: | ---: |
| `compact_36_without_volatility_band__risk_proxy__leader_relative` | 36 | `volatility_band,risk_proxy,leader_relative` | 0.4628 | 0.0130 | -0.0334 |
| `compact_42_without_volatility_band__leader_relative` | 42 | `volatility_band,leader_relative` | 0.4623 | 0.0125 | -0.0337 |
| `compact_50_without_volatility_band` | 50 | `volatility_band` | 0.4598 | 0.0100 | -0.0306 |
| `full_58` | 58 | `-` | 0.4498 | 0.0000 | -0.0195 |

## Practical Read

- best raw valid score: `compact_36_without_volatility_band__risk_proxy__leader_relative` (`0.4628`)
- recommended compact candidate: `compact_36_without_volatility_band__risk_proxy__leader_relative` with `36` features
- recommendation rule: prefer the strongest compact variant, but break ties toward fewer features when the score difference is small.

## Notes

- This phase compares compact variants only on the existing train/valid split.
- It is still a diagnostic pass and does not replace the frozen 01D selection.
- A recommended compact candidate here is only a candidate for later dedicated compact-model or stability checks.
- The negative `train-valid` gap in this table means the current valid window is behaving a bit easier than the train window, so this should be read as a split/regime effect rather than as proof that compact variants are universally stronger.

## Artifacts

- full table: `02_runs/archived/01H_run_0001_compact_candidate_compare/compact_candidate_results.csv`
- sorted table: `02_runs/archived/01H_run_0001_compact_candidate_compare/compact_candidate_sorted.csv`
- feature sets: `02_runs/archived/01H_run_0001_compact_candidate_compare/feature_sets.json`
