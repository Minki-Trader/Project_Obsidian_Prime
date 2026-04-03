# 05N Stage 05 MT5 Logic Mix Validation Review

Generated at: `2026-03-29T16:05:30.409136+00:00`

## Scope

- purpose: `scan broad Stage 05 logic mixes before narrowing the search again`
- baseline model lineage remains the Stage 01 final logistic bundle
- mixes combine tuned thresholds, tuned margin, and tuned probability-diff gates without forcing promotion yet

## Ranking

- [1] `05P_margin_diff_mix_0001`: mix=margin_diff_mix, Ts=0.3333, Tl=0.3333, margin=0.0700, diff=0.0775, return_pct=67.402, profit_factor=1.3082, max_dd_pct=12.5507, ulcer_index=2.3919, trades=451, ready_gap=0, unexpected_skips=0
- [2] `05O_thr_diff_mix_0001`: mix=threshold_diff_mix, Ts=0.5350, Tl=0.4000, margin=-, diff=0.0775, return_pct=41.006, profit_factor=1.2793, max_dd_pct=16.2807, ulcer_index=2.4835, trades=247, ready_gap=0, unexpected_skips=0
- [3] `05Q_thr_margin_diff_0001`: mix=threshold_margin_diff_mix, Ts=0.5350, Tl=0.4000, margin=0.0700, diff=0.0775, return_pct=41.006, profit_factor=1.2793, max_dd_pct=16.2807, ulcer_index=2.4835, trades=247, ready_gap=0, unexpected_skips=0
- [4] `05N_thr_margin_mix_0001`: mix=threshold_margin_mix, Ts=0.5350, Tl=0.4000, margin=0.0700, diff=-, return_pct=35.614, profit_factor=1.2197, max_dd_pct=17.1620, ulcer_index=6.0258, trades=278, ready_gap=0, unexpected_skips=0

## Follow-up Holdout

- candidate: `05P_margin_diff_mix_0001`, return_pct=`1.686`, profit_factor=`1.0113`, max_dd_pct=`22.0335`, ulcer_index=`9.3256`, trades=`309`, ready_gap=`35`
- incumbent: `03E_mt5_validation_baseline_0001`, return_pct=`7.072`, profit_factor=`1.0441`, max_dd_pct=`20.0228`, ulcer_index=`8.1911`, trades=`357`, ready_gap=`35`
- verdict: `reject_keep_incumbent`
- read: `the margin+diff mix was the best broad logic candidate on validation, but it still did not clear the incumbent on holdout`

## Read

- read: `use this as breadth-first validation scanning; only open holdout for a mix candidate if it looks materially stronger than the current same-model frontier`
