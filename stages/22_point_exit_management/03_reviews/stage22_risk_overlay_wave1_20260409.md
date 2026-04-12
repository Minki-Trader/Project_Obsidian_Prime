# Stage 22 Risk Overlay Wave 1

- reviewed_on: `2026-04-09`
- purpose: `return the Stage 22 family to regular risk-based execution instead of fixed 0.1 lot comparison`
- regular_risk_overlay: `risk_pct=2.0, balance base, ATR14 broker-native SL, direction_split(long=1.4, short=2.0), monday=0.75, ny_postcash=0.70, hold_cap=3`
- structural_scout_reference: `fixed_lot=0.1 scout board is kept as context only; promotion comes from the regular scoreboard`

## Structural Scout Scoreboard

| run | val_return | val_dd | test_return | test_dd | shared_delta_vs_22A | winner_clip | loser_mitigation | read |
|---|---|---|---|---|---|---|---|---|
| `22A` | `122.570` | `12.603` | `68.574` | `19.394` | `0.000` | `0.0000` | `0.0000` | `scout incumbent` |
| `22O` | `119.106` | `11.878` | `66.680` | `18.806` | `-9.470` | `0.0846` | `0.0156` | `best scout containment challenger` |
| `22P` | `112.074` | `11.535` | `62.788` | `17.629` | `-28.930` | `0.2540` | `0.0464` | `stronger containment, more clipping` |

## Regular Risk Execution Scoreboard

| run | hist_return | hist_dd | val_return | val_dd | test_return | test_dd | test_pf | shared_delta_vs_22Q | winner_clip | loser_mitigation | read |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `22Q` | `26.002` | `25.433` | `193.808` | `20.824` | `71.068` | `27.423` | `1.3199` | `0.000` | `0.0000` | `0.0000` | `regular incumbent` |
| `22R` | `25.488` | `25.342` | `183.788` | `20.440` | `71.514` | `27.125` | `1.3252` | `2.230` | `0.0596` | `0.0252` | `best regular containment challenger` |
| `22S` | `21.516` | `25.392` | `191.362` | `20.693` | `65.412` | `27.734` | `1.2960` | `-21.520` | `0.0273` | `0.0366` | `too gentle` |
| `22T` | `25.458` | `25.325` | `182.030` | `20.443` | `71.468` | `27.037` | `1.3253` | `2.000` | `0.0746` | `0.0290` | `stronger containment, more non-OOS drag` |

## Current Regular Read

- incumbent: `22Q_05dp_base_risk2_dirsplit_postcash_0001`
- shadow challenger: `22R_05dp_psl45_qtr_h3_risk2_0001`
- why: `22Q` keeps the best multi-window stability, while `22R` is the cleanest containment challenger with a small positive shared-position delta and limited additional clipping.

## Current Incumbent Snapshot

- headline_test: `return_pct=71.068`, `pf=1.3199`, `max_dd_pct=27.423`, `trades=302`
- risk_test: `ulcer_index=13.066`, `worst_week=-117.39`, `consecutive_losses=9`
- diagnostics_test: `no_trade_rate=0.8675`, `long_short=139/163`, `avg_hold=4.0`
- execution_test: `skip_rate=0.7661`, `external_mismatch_count=8976`, `fill_rate=n/a`

## Shadow Challenger Snapshot

- headline_test: `return_pct=71.514`, `pf=1.3252`, `max_dd_pct=27.125`, `trades=382`
- risk_test: `ulcer_index=12.793`, `worst_week=-117.38`, `consecutive_losses=15`
- diagnostics_test: `no_trade_rate=0.8675`, `long_short=169/213`, `avg_hold=3.86`
- execution_test: `skip_rate=0.7661`, `external_mismatch_count=8976`, `fill_rate=n/a`
- position_read: `shared_delta_vs_22Q=2.23`, `winner_clip=0.0596`, `loser_mitigation=0.0252`

## Interpretation

- `22Q` established the proper regular baseline: once Stage 22 is put back on risk-based execution, the headline profile changes materially from the earlier fixed-lot probe. That fixed-lot read should be treated as structural scouting, not as the final operating verdict.
- `22R` and `22T` were the only challengers that improved the risk-sized OOS slice at all. Both preserved the same test position universe as baseline and produced a small positive shared-position delta versus `22Q`.
- `22S` was too gentle. Its smaller partials reduced winner clipping the most, but the loser relief was not strong enough and the OOS result fell behind baseline.
- `22T` gave the best OOS drawdown and almost the same OOS return uplift as `22R`, but it paid a bit more validation and historical drag. `22R` was the cleaner compromise across the three windows.
- Promotion is still too early. `22Q` keeps the best multi-window stability overall, while `22R` is now the best risk-sized containment challenger worth carrying forward.
