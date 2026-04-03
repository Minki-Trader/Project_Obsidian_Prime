# 05D Stage 05 MT5 Holdout Duel Review

Generated at: `2026-03-29T11:05:00+00:00`

## Scope

- purpose: `compare the incumbent MT5 leader against the Stage 05 challengers on the MT5 holdout window`
- split: `test`
- tester date window: `2025.10.01` through `2026.03.01`
- compared runs:
  - `03E_mt5_validation_baseline_0001`
  - `05D_mt5_validation_diff_tightgap_0001`
  - `05C_mt5_validation_margin_tightgap_0001`

## Coverage Note

- all three holdout runs show `actual_ready_row_count=6755` versus `expected_ready_row_count=6720`
- that is `ready_row_gap=+35` for every compared run
- read: the MT5 tester uses date-only boundaries, so the first holdout day includes `35` extra ready rows beyond the offline test registry
- conclusion: offline parity is not exact on holdout, but the relative comparison is still fair because the same boundary effect hits all compared runs

## Holdout Ranking

- [1] `03E_mt5_validation_baseline_0001`: `min_margin=0.0700`, return_pct=`7.0720`, profit_factor=`1.0441`, max_dd_pct=`20.0228`, ulcer_index=`8.1911`, trades=`357`
- [2] `05D_mt5_validation_diff_tightgap_0001`: `min_probability_diff=0.0775`, return_pct=`1.8080`, profit_factor=`1.0114`, max_dd_pct=`20.7317`, ulcer_index=`8.0764`, trades=`351`
- [3] `05C_mt5_validation_margin_tightgap_0001`: `min_margin=0.0850`, return_pct=`0.7420`, profit_factor=`1.0060`, max_dd_pct=`24.4524`, ulcer_index=`10.5101`, trades=`255`

## Verdict

- verdict: `keep 03E as the promoted MT5 holdout winner`
- read: `05D` won the validation batch, but it did not carry that edge into holdout
- read: `05C` also failed to beat the incumbent on holdout and did so with the weakest drawdown profile of the three
- action: `keep synthesis closed and treat 03E as the current bundle to beat`
