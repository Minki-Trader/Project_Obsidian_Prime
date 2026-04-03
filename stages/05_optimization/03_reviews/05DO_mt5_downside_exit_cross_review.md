# 05DO Stage 05 Downside Exit Cross Review

Generated at: `2026-03-30T13:47:35.675281+00:00`

## Scope

- purpose: `test whether the 05DJ hold-discipline edge transfers onto downside-aware persistence feature lines`
- promoted incumbent: `05DJ`
- feature references: `05CC`, `05CA`, `05BF`

## MT5 Validation Ranking

- [1] `05DJ_05bf_margin_hold5_0001`: variant=`promoted_05dj`, groups=`-`, hold=-, return_pct=119.436, profit_factor=1.5645, max_dd_pct=12.4696, ulcer_index=7.1858, trades=386, ready_gap=0, unexpected_skips=0
- [2] `05DN_05ca_margin_hold5_0001`: variant=`05ca_hold5`, groups=`trend_proxy_persistence, trend_proxy_risk_off_confirmation`, hold=5, return_pct=109.314, profit_factor=1.5024, max_dd_pct=13.2239, ulcer_index=7.5148, trades=388, ready_gap=0, unexpected_skips=0
- [3] `05DL_05cc_margin_hold5_0001`: variant=`05cc_hold5`, groups=`trend_proxy_persistence, trend_proxy_downside_pressure, trend_proxy_risk_off_confirmation`, hold=5, return_pct=99.682, profit_factor=1.4448, max_dd_pct=14.9161, ulcer_index=7.6350, trades=393, ready_gap=0, unexpected_skips=0
- [4] `05DM_05cc_margin_hold4_0001`: variant=`05cc_hold4`, groups=`trend_proxy_persistence, trend_proxy_downside_pressure, trend_proxy_risk_off_confirmation`, hold=4, return_pct=92.446, profit_factor=1.4194, max_dd_pct=14.5029, ulcer_index=6.8711, trades=435, ready_gap=0, unexpected_skips=0
- [5] `05BF_trend_proxy_persistence_volatility_0001`: variant=`persistence_vol_reference`, groups=`-`, hold=-, return_pct=89.422, profit_factor=1.4012, max_dd_pct=11.9463, ulcer_index=7.1506, trades=487, ready_gap=0, unexpected_skips=0
- [6] `05CA_trend_proxy_persistence_riskoff_0001`: variant=`riskoff_reference`, groups=`-`, hold=-, return_pct=84.152, profit_factor=1.3760, max_dd_pct=12.0537, ulcer_index=7.2741, trades=488, ready_gap=0, unexpected_skips=0
- [7] `05CC_trend_proxy_persistence_downside_riskoff_0001`: variant=`downside_riskoff_reference`, groups=`-`, hold=-, return_pct=78.506, profit_factor=1.3414, max_dd_pct=12.0064, ulcer_index=7.2488, trades=495, ready_gap=0, unexpected_skips=0

## MT5 Holdout Ranking

- [1] `05DN_05ca_margin_hold5_0001`: variant=`05ca_hold5`, groups=`trend_proxy_persistence, trend_proxy_risk_off_confirmation`, hold=5, return_pct=60.940, profit_factor=1.4517, max_dd_pct=20.2732, ulcer_index=6.2392, trades=263, ready_gap=35, unexpected_skips=0
- [2] `05DJ_05bf_margin_hold5_0001`: variant=`promoted_05dj`, groups=`-`, hold=-, return_pct=59.190, profit_factor=1.4283, max_dd_pct=20.2732, ulcer_index=6.1801, trades=265, ready_gap=35, unexpected_skips=0
- [3] `05DL_05cc_margin_hold5_0001`: variant=`05cc_hold5`, groups=`trend_proxy_persistence, trend_proxy_downside_pressure, trend_proxy_risk_off_confirmation`, hold=5, return_pct=58.852, profit_factor=1.4311, max_dd_pct=18.3944, ulcer_index=5.5864, trades=267, ready_gap=35, unexpected_skips=0
- [4] `05CC_trend_proxy_persistence_downside_riskoff_0001`: variant=`downside_riskoff_reference`, groups=`-`, hold=-, return_pct=47.402, profit_factor=1.3367, max_dd_pct=15.5405, ulcer_index=6.0251, trades=333, ready_gap=35, unexpected_skips=0
- [5] `05BF_trend_proxy_persistence_volatility_0001`: variant=`persistence_vol_reference`, groups=`-`, hold=-, return_pct=40.462, profit_factor=1.2801, max_dd_pct=17.0166, ulcer_index=6.9935, trades=331, ready_gap=35, unexpected_skips=0
- [6] `05CA_trend_proxy_persistence_riskoff_0001`: variant=`riskoff_reference`, groups=`-`, hold=-, return_pct=38.456, profit_factor=1.2639, max_dd_pct=17.0166, ulcer_index=7.0800, trades=330, ready_gap=35, unexpected_skips=0

## Verdict

- status: `mixed_holdout_win_keep_incumbent`
- selected_run_name: `05DJ_05bf_margin_hold5_0001`
- reason: `cross candidate improved holdout but did not lead validation, so the promoted incumbent stays in place`

## Read

- read: `this batch checks whether the new promoted edge is really exit-discipline generalization or just a 05BF-specific fit`
