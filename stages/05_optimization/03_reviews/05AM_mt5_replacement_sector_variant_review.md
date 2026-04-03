# 05AM Stage 05 Replacement Sector Variant Review

Generated at: `2026-03-29T17:54:12.854815+00:00`

## Scope

- purpose: `scan lighter replacement-sector variants before deciding whether the full 05AH proxy block is too heavy`
- model family: `trend_proxy_sector_logreg`
- incumbent reference: `05W_no_trend_strength_0001`

## MT5 Validation Ranking

- [1] `05AI_trend_proxy_light_pb_0001`: variant=`light_persistence_breakout`, groups=`trend_proxy_persistence, trend_proxy_breakout_pressure`, return_pct=86.868, profit_factor=1.3884, max_dd_pct=11.7173, ulcer_index=6.8444, trades=485, ready_gap=0, unexpected_skips=0
- [2] `05AJ_trend_proxy_light_vb_0001`: variant=`light_volatility_breadth`, groups=`trend_proxy_volatility_regime, trend_proxy_breadth_confirmation`, return_pct=75.362, profit_factor=1.3242, max_dd_pct=12.0620, ulcer_index=7.1696, trades=492, ready_gap=0, unexpected_skips=0
- [3] `05AL_trend_proxy_light_pc_0001`: variant=`light_persistence_confirmation`, groups=`trend_proxy_persistence, trend_proxy_breadth_confirmation`, return_pct=62.736, profit_factor=1.2682, max_dd_pct=14.0671, ulcer_index=8.4630, trades=490, ready_gap=0, unexpected_skips=0
- [4] `05AK_trend_proxy_light_core3_0001`: variant=`light_core_three`, groups=`trend_proxy_persistence, trend_proxy_volatility_regime, trend_proxy_breakout_pressure`, return_pct=61.826, profit_factor=1.2557, max_dd_pct=13.9113, ulcer_index=8.3938, trades=493, ready_gap=0, unexpected_skips=0

## MT5 Holdout Ranking

- [1] `05AI_trend_proxy_light_pb_0001`: variant=`light_persistence_breakout`, groups=`trend_proxy_persistence, trend_proxy_breakout_pressure`, return_pct=37.274, profit_factor=1.2542, max_dd_pct=17.0373, ulcer_index=7.7860, trades=330, ready_gap=35, unexpected_skips=0
- [2] `05AJ_trend_proxy_light_vb_0001`: variant=`light_volatility_breadth`, groups=`trend_proxy_volatility_regime, trend_proxy_breadth_confirmation`, return_pct=34.760, profit_factor=1.2342, max_dd_pct=17.0373, ulcer_index=7.6654, trades=334, ready_gap=35, unexpected_skips=0
- [3] `05W_no_trend_strength_0001`: variant=`incumbent`, groups=``, return_pct=33.538, profit_factor=1.2253, max_dd_pct=17.0166, ulcer_index=7.8344, trades=336, ready_gap=35, unexpected_skips=0

## Verdict

- status: `mixed_holdout_win_keep_incumbent`
- selected_run_name: `05W_no_trend_strength_0001`
- reason: `05AI won the lightweight-variant sweep and improved holdout versus 05W, but it still trailed the incumbent on validation, so 05W stays promoted for now`

## Read

- read: `lighter replacement sectors are useful if they keep 05W's validation edge while borrowing some of 05AH's holdout strength`
