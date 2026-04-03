# 05BT Stage 05 Persistence Frontier Vote Review

Generated at: `2026-03-30T11:58:04.892363+00:00`

## Scope

- purpose: `probe soft-voting blends built from the persistence-heavy frontier instead of narrowing too early to one feature-side line`
- model family: `persistence_frontier_voter`
- reference runs: `05W`, `05BB`, `05BF`, `05AH`

## MT5 Validation Ranking

- [1] `05BQ_frontier_vote_w_bf_0001`: variant=`vote_05w_bf_equal`, components=`base_05w, persistence_volatility`, weights=`1.000, 1.000`, return_pct=92.292, profit_factor=1.4157, max_dd_pct=10.9660, ulcer_index=6.4919, trades=491, ready_gap=0, unexpected_skips=0
- [2] `05W_no_trend_strength_0001`: variant=`incumbent_05w`, components=`-`, weights=`-`, return_pct=91.168, profit_factor=1.4092, max_dd_pct=11.1472, ulcer_index=6.5205, trades=493, ready_gap=0, unexpected_skips=0
- [3] `05BF_trend_proxy_persistence_volatility_0001`: variant=`persistence_volatility_reference`, components=`-`, weights=`-`, return_pct=89.422, profit_factor=1.4012, max_dd_pct=11.9463, ulcer_index=7.1506, trades=487, ready_gap=0, unexpected_skips=0
- [4] `05BR_frontier_vote_w_bb_bf_0001`: variant=`vote_05w_bb_bf_equal`, components=`base_05w, persistence_only, persistence_volatility`, weights=`1.000, 1.000, 1.000`, return_pct=87.628, profit_factor=1.3944, max_dd_pct=12.1698, ulcer_index=7.2493, trades=487, ready_gap=0, unexpected_skips=0
- [5] `05BB_trend_proxy_persistence_only_0001`: variant=`persistence_only_reference`, components=`-`, weights=`-`, return_pct=75.676, profit_factor=1.3308, max_dd_pct=12.3455, ulcer_index=7.2609, trades=490, ready_gap=0, unexpected_skips=0
- [6] `05BP_frontier_vote_w_bb_0001`: variant=`vote_05w_bb_equal`, components=`base_05w, persistence_only`, weights=`1.000, 1.000`, return_pct=72.706, profit_factor=1.3149, max_dd_pct=13.0856, ulcer_index=7.8210, trades=488, ready_gap=0, unexpected_skips=0
- [7] `05BS_frontier_vote_w_bb_ah_0001`: variant=`vote_05w_bb_fullproxy_weighted`, components=`base_05w, persistence_only, full_proxy`, weights=`2.000, 2.000, 1.000`, return_pct=70.768, profit_factor=1.3065, max_dd_pct=13.0287, ulcer_index=7.8789, trades=488, ready_gap=0, unexpected_skips=0
- [8] `05AH_trend_proxy_sector_replacement_0001`: variant=`full_proxy_reference`, components=`-`, weights=`-`, return_pct=62.200, profit_factor=1.2632, max_dd_pct=13.4545, ulcer_index=7.9225, trades=489, ready_gap=0, unexpected_skips=0

## MT5 Holdout Ranking

- [1] `05BB_trend_proxy_persistence_only_0001`: variant=`persistence_only_reference`, components=`-`, weights=`-`, return_pct=44.792, profit_factor=1.3193, max_dd_pct=15.5405, ulcer_index=6.3183, trades=328, ready_gap=35, unexpected_skips=0
- [2] `05AH_trend_proxy_sector_replacement_0001`: variant=`full_proxy_reference`, components=`-`, weights=`-`, return_pct=44.558, profit_factor=1.3109, max_dd_pct=17.7040, ulcer_index=7.1521, trades=331, ready_gap=35, unexpected_skips=0
- [3] `05BF_trend_proxy_persistence_volatility_0001`: variant=`persistence_volatility_reference`, components=`-`, weights=`-`, return_pct=40.462, profit_factor=1.2801, max_dd_pct=17.0166, ulcer_index=6.9935, trades=331, ready_gap=35, unexpected_skips=0
- [4] `05BR_frontier_vote_w_bb_bf_0001`: variant=`vote_05w_bb_bf_equal`, components=`base_05w, persistence_only, persistence_volatility`, weights=`1.000, 1.000, 1.000`, return_pct=38.266, profit_factor=1.2635, max_dd_pct=17.0166, ulcer_index=7.6083, trades=332, ready_gap=35, unexpected_skips=0
- [5] `05BQ_frontier_vote_w_bf_0001`: variant=`vote_05w_bf_equal`, components=`base_05w, persistence_volatility`, weights=`1.000, 1.000`, return_pct=34.760, profit_factor=1.2326, max_dd_pct=17.0166, ulcer_index=7.7800, trades=335, ready_gap=35, unexpected_skips=0
- [6] `05W_no_trend_strength_0001`: variant=`incumbent_05w`, components=`-`, weights=`-`, return_pct=33.538, profit_factor=1.2253, max_dd_pct=17.0166, ulcer_index=7.8344, trades=336, ready_gap=35, unexpected_skips=0

## Verdict

- status: `reject_keep_incumbent`
- selected_run_name: `05W_no_trend_strength_0001`
- reason: `no persistence-heavy voting blend cleared the current frontier on holdout`

## Read

- read: `these voting blends are breadth-first ensemble probes; keep any holdout-positive mix as a challenger unless it also proves validation durability`
