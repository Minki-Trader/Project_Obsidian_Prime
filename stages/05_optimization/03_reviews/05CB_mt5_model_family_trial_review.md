# 05CB Stage 05 Model Family Trial Review

Generated at: `2026-03-30T13:00:54.257494+00:00`

## Scope

- purpose: `train a fresh trend_proxy_sector_logreg model on the frozen h/band dataset and run the current reference logic on MT5`
- logic reference: `05W_no_trend_strength_0001` with `min_margin=0.0700`
- dropped sectors: `trend_strength`
- replacement sector: `trend_proxy_regime`
- trend_proxy_persistence: `ema20_ema50_diff, ema50_ema200_diff, trix_15`
- trend_proxy_leader_drag: `nvda_xnas_log_return_1, aapl_xnas_log_return_1, msft_xnas_log_return_1, amzn_xnas_log_return_1, mega8_equal_return_1, mega8_pos_breadth_1, mega8_dispersion_5`

## Offline Test Confirmation

- incumbent Stage 01 test: macro_f1=`0.4581`, balanced_accuracy=`0.4694`, accuracy=`0.5769`, log_loss=`0.9728`
- trial model test: macro_f1=`0.4574`, balanced_accuracy=`0.4686`, accuracy=`0.5762`, log_loss=`0.9737`

## MT5 Validation Ranking

- [1] `05W_no_trend_strength_0001`: return_pct=91.168, profit_factor=1.4092, max_dd_pct=11.1472, ulcer_index=6.5205, trades=493, ready_gap=0, unexpected_skips=0
- [2] `05CB_trend_proxy_persistence_leader_drag_0001`: return_pct=69.212, profit_factor=1.2934, max_dd_pct=12.1108, ulcer_index=7.2745, trades=489, ready_gap=0, unexpected_skips=0

## Verdict

- status: `validation_only_pending_holdout`
- selected_run_name: `05W_no_trend_strength_0001`
- reason: `holdout not run yet, so the incumbent remains the selected bundle`

## Read

- validation leader: `05W_no_trend_strength_0001`
- read: `treat model-family swaps with the same holdout gate as logic sweeps; validation spikes alone are not enough`
