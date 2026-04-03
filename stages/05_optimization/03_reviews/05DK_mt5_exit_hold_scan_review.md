# 05DK Stage 05 Exit Hold Scan Review

Generated at: `2026-03-30T13:21:55.127488+00:00`

## Scope

- purpose: `shift logic exploration away from extra entry filtering and toward exit discipline on persistence-heavy challengers`
- reference runs: `05W`, `05BB`, `05BF`

## MT5 Validation Ranking

- [1] `05DJ_05bf_margin_hold5_0001`: variant=`05bf_hold5`, source=`05BF_trend_proxy_persistence_volatility_0001`, margin=0.0700, hold=5, return_pct=119.436, profit_factor=1.5645, max_dd_pct=12.4696, ulcer_index=7.1858, trades=386, ready_gap=0, unexpected_skips=0
- [2] `05DE_05bb_margin_hold2_0001`: variant=`05bb_hold2`, source=`05BB_trend_proxy_persistence_only_0001`, margin=0.0700, hold=2, return_pct=107.676, profit_factor=1.4763, max_dd_pct=11.3352, ulcer_index=4.8741, trades=580, ready_gap=0, unexpected_skips=0
- [3] `05DI_05bf_margin_hold4_0001`: variant=`05bf_hold4`, source=`05BF_trend_proxy_persistence_volatility_0001`, margin=0.0700, hold=4, return_pct=104.536, profit_factor=1.5059, max_dd_pct=11.5423, ulcer_index=6.6349, trades=427, ready_gap=0, unexpected_skips=0
- [4] `05DH_05bf_margin_hold2_0001`: variant=`05bf_hold2`, source=`05BF_trend_proxy_persistence_volatility_0001`, margin=0.0700, hold=2, return_pct=102.284, profit_factor=1.4497, max_dd_pct=12.4474, ulcer_index=5.1608, trades=576, ready_gap=0, unexpected_skips=0
- [5] `05DG_05bb_margin_hold5_0001`: variant=`05bb_hold5`, source=`05BB_trend_proxy_persistence_only_0001`, margin=0.0700, hold=5, return_pct=99.730, profit_factor=1.4495, max_dd_pct=14.8335, ulcer_index=7.3532, trades=390, ready_gap=0, unexpected_skips=0
- [6] `05W_no_trend_strength_0001`: variant=`incumbent_05w`, source=`-`, margin=-, hold=-, return_pct=91.168, profit_factor=1.4092, max_dd_pct=11.1472, ulcer_index=6.5205, trades=493, ready_gap=0, unexpected_skips=0
- [7] `05BF_trend_proxy_persistence_volatility_0001`: variant=`persistence_volatility_reference`, source=`-`, margin=-, hold=-, return_pct=89.422, profit_factor=1.4012, max_dd_pct=11.9463, ulcer_index=7.1506, trades=487, ready_gap=0, unexpected_skips=0
- [8] `05DF_05bb_margin_hold4_0001`: variant=`05bb_hold4`, source=`05BB_trend_proxy_persistence_only_0001`, margin=0.0700, hold=4, return_pct=86.250, profit_factor=1.4010, max_dd_pct=14.6557, ulcer_index=6.6323, trades=428, ready_gap=0, unexpected_skips=0
- [9] `05BB_trend_proxy_persistence_only_0001`: variant=`persistence_only_reference`, source=`-`, margin=-, hold=-, return_pct=75.676, profit_factor=1.3308, max_dd_pct=12.3455, ulcer_index=7.2609, trades=490, ready_gap=0, unexpected_skips=0

## MT5 Holdout Ranking

- [1] `05DJ_05bf_margin_hold5_0001`: variant=`05bf_hold5`, source=`05BF_trend_proxy_persistence_volatility_0001`, margin=0.0700, hold=5, return_pct=59.190, profit_factor=1.4283, max_dd_pct=20.2732, ulcer_index=6.1801, trades=265, ready_gap=35, unexpected_skips=0
- [2] `05BB_trend_proxy_persistence_only_0001`: variant=`persistence_only_reference`, source=`-`, margin=-, hold=-, return_pct=44.792, profit_factor=1.3193, max_dd_pct=15.5405, ulcer_index=6.3183, trades=328, ready_gap=35, unexpected_skips=0
- [3] `05BF_trend_proxy_persistence_volatility_0001`: variant=`persistence_volatility_reference`, source=`-`, margin=-, hold=-, return_pct=40.462, profit_factor=1.2801, max_dd_pct=17.0166, ulcer_index=6.9935, trades=331, ready_gap=35, unexpected_skips=0
- [4] `05W_no_trend_strength_0001`: variant=`incumbent_05w`, source=`-`, margin=-, hold=-, return_pct=33.538, profit_factor=1.2253, max_dd_pct=17.0166, ulcer_index=7.8344, trades=336, ready_gap=35, unexpected_skips=0
- [5] `05DE_05bb_margin_hold2_0001`: variant=`05bb_hold2`, source=`05BB_trend_proxy_persistence_only_0001`, margin=0.0700, hold=2, return_pct=33.050, profit_factor=1.2199, max_dd_pct=14.3670, ulcer_index=5.9356, trades=404, ready_gap=35, unexpected_skips=0

## Verdict

- status: `promote_candidate`
- selected_run_name: `05DJ_05bf_margin_hold5_0001`
- reason: `exit-discipline candidate led both validation and holdout across the current logic frontier`

## Read

- read: `this batch asks whether persistence-heavy challengers were underperforming mainly because of exit timing rather than entry quality`
