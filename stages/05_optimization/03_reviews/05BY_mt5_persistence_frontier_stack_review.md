# 05BY Stage 05 Persistence Frontier Stack Review

Generated at: `2026-03-30T12:19:31.587305+00:00`

## Scope

- purpose: `probe stacking blends built from the persistence-heavy frontier so the meta learner can react to regime/context instead of plain averaging`
- model family: `persistence_frontier_stacker`
- reference runs: `05W`, `05BB`, `05BF`, `05AH`

## MT5 Validation Ranking

- [1] `05W_no_trend_strength_0001`: variant=`incumbent_05w`, components=`-`, return_pct=91.168, profit_factor=1.4092, max_dd_pct=11.1472, ulcer_index=6.5205, trades=493, ready_gap=0, unexpected_skips=0
- [2] `05BF_trend_proxy_persistence_volatility_0001`: variant=`persistence_volatility_reference`, components=`-`, return_pct=89.422, profit_factor=1.4012, max_dd_pct=11.9463, ulcer_index=7.1506, trades=487, ready_gap=0, unexpected_skips=0
- [3] `05BB_trend_proxy_persistence_only_0001`: variant=`persistence_only_reference`, components=`-`, return_pct=75.676, profit_factor=1.3308, max_dd_pct=12.3455, ulcer_index=7.2609, trades=490, ready_gap=0, unexpected_skips=0
- [4] `05AH_trend_proxy_sector_replacement_0001`: variant=`full_proxy_reference`, components=`-`, return_pct=62.200, profit_factor=1.2632, max_dd_pct=13.4545, ulcer_index=7.9225, trades=489, ready_gap=0, unexpected_skips=0
- [5] `05BV_frontier_stack_w_bb_bf_0001`: variant=`stack_05w_bb_bf`, components=`base_05w, persistence_only, persistence_volatility`, return_pct=-11.846, profit_factor=0.9292, max_dd_pct=27.6013, ulcer_index=13.9872, trades=270, ready_gap=0, unexpected_skips=0
- [6] `05BW_frontier_stack_w_bb_ah_0001`: variant=`stack_05w_bb_fullproxy`, components=`base_05w, persistence_only, full_proxy`, return_pct=-16.900, profit_factor=0.9302, max_dd_pct=30.3667, ulcer_index=17.5035, trades=416, ready_gap=0, unexpected_skips=0
- [7] `05BU_frontier_stack_w_bf_0001`: variant=`stack_05w_bf`, components=`base_05w, persistence_volatility`, return_pct=-20.890, profit_factor=0.8873, max_dd_pct=30.0738, ulcer_index=19.2198, trades=301, ready_gap=0, unexpected_skips=0

## MT5 Holdout Ranking

- [1] `05BB_trend_proxy_persistence_only_0001`: variant=`persistence_only_reference`, components=`-`, return_pct=44.792, profit_factor=1.3193, max_dd_pct=15.5405, ulcer_index=6.3183, trades=328, ready_gap=35, unexpected_skips=0
- [2] `05AH_trend_proxy_sector_replacement_0001`: variant=`full_proxy_reference`, components=`-`, return_pct=44.558, profit_factor=1.3109, max_dd_pct=17.7040, ulcer_index=7.1521, trades=331, ready_gap=35, unexpected_skips=0
- [3] `05BF_trend_proxy_persistence_volatility_0001`: variant=`persistence_volatility_reference`, components=`-`, return_pct=40.462, profit_factor=1.2801, max_dd_pct=17.0166, ulcer_index=6.9935, trades=331, ready_gap=35, unexpected_skips=0
- [4] `05BW_frontier_stack_w_bb_ah_0001`: variant=`stack_05w_bb_fullproxy`, components=`base_05w, persistence_only, full_proxy`, return_pct=33.584, profit_factor=1.2945, max_dd_pct=13.5938, ulcer_index=4.6007, trades=247, ready_gap=35, unexpected_skips=0
- [5] `05W_no_trend_strength_0001`: variant=`incumbent_05w`, components=`-`, return_pct=33.538, profit_factor=1.2253, max_dd_pct=17.0166, ulcer_index=7.8344, trades=336, ready_gap=35, unexpected_skips=0
- [6] `05BV_frontier_stack_w_bb_bf_0001`: variant=`stack_05w_bb_bf`, components=`base_05w, persistence_only, persistence_volatility`, return_pct=12.022, profit_factor=1.1434, max_dd_pct=17.3147, ulcer_index=8.6240, trades=153, ready_gap=35, unexpected_skips=0

## Verdict

- status: `reject_keep_incumbent`
- selected_run_name: `05W_no_trend_strength_0001`
- reason: `no persistence-heavy stacking blend cleared the current frontier on holdout`

## Read

- read: `these stacking blends are meant to be regime-conditioned frontier probes; keep any holdout-positive read as a challenger unless it also proves validation durability`
