# Stage 22 Risk Overlay Wave 1

- reviewed on: `2026-04-09`
- purpose: `return the Stage 22 family to regular risk-based execution instead of fixed 0.1 lot comparison`
- risk overlay: `risk_pct=2.0, balance base, ATR14 broker-native SL, direction_split(long=1.4, short=2.0), monday=0.75, ny_postcash=0.70, hold_cap=3`

## Cross-Split Headline

| run | hist_return | hist_dd | val_return | val_dd | test_return | test_dd | test_pf |
|---|---:|---:|---:|---:|---:|---:|---:|
| `22Q` | `26.002` | `25.433` | `193.808` | `20.824` | `71.068` | `27.423` | `1.3199` |
| `22R` | `25.488` | `25.342` | `183.788` | `20.440` | `71.514` | `27.125` | `1.3252` |
| `22S` | `21.516` | `25.392` | `191.362` | `20.693` | `65.412` | `27.734` | `1.2960` |
| `22T` | `25.458` | `25.325` | `182.030` | `20.443` | `71.468` | `27.037` | `1.3253` |

## Test Position Read

| run | shared_delta_vs_22Q | winner_clip | loser_mitigation | position_count | risk_contexts | partial_volumes |
|---|---:|---:|---:|---:|---|---|
| `22Q` | `0.000` | `0.0000` | `0.0000` | `302` | `{'BASE': 215, 'NY_POSTCASH': 60, 'MONDAY': 24, 'MONDAY|NY_POSTCASH': 3}` | `-` |
| `22R` | `2.230` | `0.0596` | `0.0252` | `302` | `{'BASE': 215, 'NY_POSTCASH': 60, 'MONDAY': 24, 'MONDAY|NY_POSTCASH': 3}` | `{'0.02': 33, '0.01': 10, '0.03': 23, '0.04': 7, '0.05': 4, '0.07': 1, '0.08': 1, '0.09': 1}` |
| `22S` | `-21.520` | `0.0273` | `0.0366` | `301` | `{'BASE': 215, 'NY_POSTCASH': 59, 'MONDAY': 24, 'MONDAY|NY_POSTCASH': 3}` | `{'0.01': 45, '0.02': 4, '0.03': 2}` |
| `22T` | `2.000` | `0.0746` | `0.0290` | `302` | `{'BASE': 215, 'NY_POSTCASH': 60, 'MONDAY': 24, 'MONDAY|NY_POSTCASH': 3}` | `{'0.02': 22, '0.01': 7, '0.03': 28, '0.04': 10, '0.05': 6, '0.06': 4, '0.08': 1, '0.09': 1, '0.10': 1}` |

## Interpretation

- `22Q` established the proper regular baseline: once Stage 22 is put back on risk-based execution, the headline profile changes materially from the earlier fixed-lot probe. That fixed-lot read should be treated as structural scouting, not as the final operating verdict.
- `22R` and `22T` were the only challengers that improved the risk-sized OOS slice at all. Both preserved the same `302` test positions as baseline and produced a small positive shared-position delta versus `22Q`.
- `22S` was too gentle. Its smaller partials reduced winner clipping the most, but the loser relief was not strong enough and the OOS result fell behind baseline.
- `22T` gave the best OOS drawdown and almost the same OOS return uplift as `22R`, but it paid a bit more validation and historical drag. `22R` was the cleaner compromise across the three windows.
- Promotion is still too early. `22Q` keeps the best multi-window stability overall, while `22R` is now the best risk-sized containment challenger worth carrying forward.
