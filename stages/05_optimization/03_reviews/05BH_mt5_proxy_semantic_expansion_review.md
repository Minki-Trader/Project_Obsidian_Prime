# 05BH Stage 05 Proxy Semantic Expansion Review

Generated at: `2026-03-30T11:27:46.735768+00:00`

## Scope

- purpose: `widen feature-side exploration by trying broader semantic proxy variants after the 05AI/05AH mixed-challenger reads`
- model family: `trend_proxy_sector_logreg`
- reference runs: `05W`, `05AI`, `05AH`, `05AJ`

## MT5 Validation Ranking

- [1] `05W_no_trend_strength_0001`: variant=`incumbent_05w`, groups=`-`, return_pct=91.168, profit_factor=1.4092, max_dd_pct=11.1472, ulcer_index=6.5205, trades=493, ready_gap=0, unexpected_skips=0
- [2] `05BF_trend_proxy_persistence_volatility_0001`: variant=`persistence_volatility_pair`, groups=`trend_proxy_persistence, trend_proxy_volatility_regime`, return_pct=89.422, profit_factor=1.4012, max_dd_pct=11.9463, ulcer_index=7.1506, trades=487, ready_gap=0, unexpected_skips=0
- [3] `05AI_trend_proxy_light_pb_0001`: variant=`existing_light_pb`, groups=`-`, return_pct=86.868, profit_factor=1.3884, max_dd_pct=11.7173, ulcer_index=6.8444, trades=485, ready_gap=0, unexpected_skips=0
- [4] `05BB_trend_proxy_persistence_only_0001`: variant=`persistence_only`, groups=`trend_proxy_persistence`, return_pct=75.676, profit_factor=1.3308, max_dd_pct=12.3455, ulcer_index=7.2609, trades=490, ready_gap=0, unexpected_skips=0
- [5] `05AJ_trend_proxy_light_vb_0001`: variant=`existing_light_vb`, groups=`-`, return_pct=75.362, profit_factor=1.3242, max_dd_pct=12.0620, ulcer_index=7.1696, trades=492, ready_gap=0, unexpected_skips=0
- [6] `05BC_trend_proxy_breakout_only_0001`: variant=`breakout_only`, groups=`trend_proxy_breakout_pressure`, return_pct=74.408, profit_factor=1.3219, max_dd_pct=11.8789, ulcer_index=7.0989, trades=493, ready_gap=0, unexpected_skips=0
- [7] `05BD_trend_proxy_volatility_only_0001`: variant=`volatility_only`, groups=`trend_proxy_volatility_regime`, return_pct=74.302, profit_factor=1.3161, max_dd_pct=12.8128, ulcer_index=7.2981, trades=491, ready_gap=0, unexpected_skips=0
- [8] `05BE_trend_proxy_breadth_only_0001`: variant=`breadth_only`, groups=`trend_proxy_breadth_confirmation`, return_pct=65.234, profit_factor=1.2759, max_dd_pct=13.5304, ulcer_index=8.1469, trades=490, ready_gap=0, unexpected_skips=0
- [9] `05BG_trend_proxy_breakout_breadth_0001`: variant=`breakout_breadth_pair`, groups=`trend_proxy_breakout_pressure, trend_proxy_breadth_confirmation`, return_pct=63.412, profit_factor=1.2709, max_dd_pct=13.1445, ulcer_index=7.6195, trades=490, ready_gap=0, unexpected_skips=0
- [10] `05AH_trend_proxy_sector_replacement_0001`: variant=`existing_full_proxy`, groups=`-`, return_pct=62.200, profit_factor=1.2632, max_dd_pct=13.4545, ulcer_index=7.9225, trades=489, ready_gap=0, unexpected_skips=0

## MT5 Holdout Ranking

- [1] `05BB_trend_proxy_persistence_only_0001`: variant=`persistence_only`, groups=`trend_proxy_persistence`, return_pct=44.792, profit_factor=1.3193, max_dd_pct=15.5405, ulcer_index=6.3183, trades=328, ready_gap=35, unexpected_skips=0
- [2] `05AH_trend_proxy_sector_replacement_0001`: variant=`existing_full_proxy`, groups=`-`, return_pct=44.558, profit_factor=1.3109, max_dd_pct=17.7040, ulcer_index=7.1521, trades=331, ready_gap=35, unexpected_skips=0
- [3] `05BF_trend_proxy_persistence_volatility_0001`: variant=`persistence_volatility_pair`, groups=`trend_proxy_persistence, trend_proxy_volatility_regime`, return_pct=40.462, profit_factor=1.2801, max_dd_pct=17.0166, ulcer_index=6.9935, trades=331, ready_gap=35, unexpected_skips=0
- [4] `05AI_trend_proxy_light_pb_0001`: variant=`existing_light_pb`, groups=`-`, return_pct=37.274, profit_factor=1.2542, max_dd_pct=17.0373, ulcer_index=7.7860, trades=330, ready_gap=35, unexpected_skips=0
- [5] `05AJ_trend_proxy_light_vb_0001`: variant=`existing_light_vb`, groups=`-`, return_pct=34.760, profit_factor=1.2342, max_dd_pct=17.0373, ulcer_index=7.6654, trades=334, ready_gap=35, unexpected_skips=0
- [6] `05W_no_trend_strength_0001`: variant=`incumbent_05w`, groups=`-`, return_pct=33.538, profit_factor=1.2253, max_dd_pct=17.0166, ulcer_index=7.8344, trades=336, ready_gap=35, unexpected_skips=0

## Verdict

- status: `mixed_holdout_win_keep_incumbent`
- selected_run_name: `05W_no_trend_strength_0001`
- reason: `new semantic proxy variant improved holdout but did not lead validation, so the incumbent stays promoted for now`

## Read

- read: `semantic proxy expansion is a breadth-first feature pass; keep any holdout-positive read as a challenger unless it also proves validation durability`
