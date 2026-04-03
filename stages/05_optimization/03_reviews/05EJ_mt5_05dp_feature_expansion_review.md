# 05EJ Stage 05 05DP Feature Expansion Review

Generated at: `2026-03-30T14:51:24.471485+00:00`

## Scope

- purpose: `re-open broader feature exploration from the stabilized 05DP line while holding logic fixed at min_margin=0.0675 and max_hold_bars=5`
- promoted incumbent: `05DP`

## MT5 Validation Ranking

- [1] `05DP_05ca_margin0675_hold5_0001`: variant=`promoted_05dp`, groups=`-`, return_pct=122.570, profit_factor=1.5553, max_dd_pct=12.6031, ulcer_index=7.2871, trades=405, ready_gap=0, unexpected_skips=0
- [2] `05EA_05ca_margin0675_hold4_0001`: variant=`hold4_sibling_05ea`, groups=`-`, return_pct=115.168, profit_factor=1.5352, max_dd_pct=11.5023, ulcer_index=6.5293, trades=453, ready_gap=0, unexpected_skips=0
- [3] `05EH_05ca_plus_leader_session_margin0675_hold5_0001`: variant=`05ca_plus_leader_session`, groups=`trend_proxy_persistence, trend_proxy_risk_off_confirmation, trend_proxy_leader_drag, trend_proxy_session_pressure`, return_pct=106.016, profit_factor=1.4650, max_dd_pct=14.4414, ulcer_index=7.6915, trades=406, ready_gap=0, unexpected_skips=0
- [4] `05EE_05ca_plus_downside_margin0675_hold5_0001`: variant=`05ca_plus_downside`, groups=`trend_proxy_persistence, trend_proxy_risk_off_confirmation, trend_proxy_downside_pressure`, return_pct=105.412, profit_factor=1.4590, max_dd_pct=14.7165, ulcer_index=7.6017, trades=408, ready_gap=0, unexpected_skips=0
- [5] `05EF_05ca_plus_leader_margin0675_hold5_0001`: variant=`05ca_plus_leader`, groups=`trend_proxy_persistence, trend_proxy_risk_off_confirmation, trend_proxy_leader_drag`, return_pct=102.846, profit_factor=1.4497, max_dd_pct=14.2892, ulcer_index=7.7889, trades=405, ready_gap=0, unexpected_skips=0
- [6] `05DL_05cc_margin_hold5_0001`: variant=`risk_alt_05dl`, groups=`-`, return_pct=99.682, profit_factor=1.4448, max_dd_pct=14.9161, ulcer_index=7.6350, trades=393, ready_gap=0, unexpected_skips=0
- [7] `05ED_05ca_plus_breakout_margin0675_hold5_0001`: variant=`05ca_plus_breakout`, groups=`trend_proxy_persistence, trend_proxy_risk_off_confirmation, trend_proxy_breakout_pressure`, return_pct=99.014, profit_factor=1.4313, max_dd_pct=14.8674, ulcer_index=8.0607, trades=401, ready_gap=0, unexpected_skips=0
- [8] `05EC_05ca_plus_volatility_margin0675_hold5_0001`: variant=`05ca_plus_volatility`, groups=`trend_proxy_persistence, trend_proxy_risk_off_confirmation, trend_proxy_volatility_regime`, return_pct=95.752, profit_factor=1.4127, max_dd_pct=14.7851, ulcer_index=7.5317, trades=404, ready_gap=0, unexpected_skips=0
- [9] `05EG_05ca_plus_session_margin0675_hold5_0001`: variant=`05ca_plus_session`, groups=`trend_proxy_persistence, trend_proxy_risk_off_confirmation, trend_proxy_session_pressure`, return_pct=94.992, profit_factor=1.4078, max_dd_pct=15.4130, ulcer_index=8.0147, trades=404, ready_gap=0, unexpected_skips=0

## MT5 Holdout Ranking

- [1] `05DP_05ca_margin0675_hold5_0001`: variant=`promoted_05dp`, groups=`-`, return_pct=68.574, profit_factor=1.4925, max_dd_pct=19.3936, ulcer_index=5.8587, trades=275, ready_gap=35, unexpected_skips=0
- [2] `05DL_05cc_margin_hold5_0001`: variant=`risk_alt_05dl`, groups=`-`, return_pct=58.852, profit_factor=1.4311, max_dd_pct=18.3944, ulcer_index=5.5864, trades=267, ready_gap=35, unexpected_skips=0
- [3] `05EE_05ca_plus_downside_margin0675_hold5_0001`: variant=`05ca_plus_downside`, groups=`trend_proxy_persistence, trend_proxy_risk_off_confirmation, trend_proxy_downside_pressure`, return_pct=57.082, profit_factor=1.3892, max_dd_pct=19.4049, ulcer_index=5.9535, trades=278, ready_gap=35, unexpected_skips=0
- [4] `05EH_05ca_plus_leader_session_margin0675_hold5_0001`: variant=`05ca_plus_leader_session`, groups=`trend_proxy_persistence, trend_proxy_risk_off_confirmation, trend_proxy_leader_drag, trend_proxy_session_pressure`, return_pct=54.940, profit_factor=1.3728, max_dd_pct=19.3936, ulcer_index=6.2151, trades=280, ready_gap=35, unexpected_skips=0
- [5] `05EA_05ca_margin0675_hold4_0001`: variant=`hold4_sibling_05ea`, groups=`-`, return_pct=53.742, profit_factor=1.3652, max_dd_pct=17.9030, ulcer_index=6.2325, trades=304, ready_gap=35, unexpected_skips=0

## Verdict

- status: `reject_keep_incumbent`
- selected_run_name: `05DP_05ca_margin0675_hold5_0001`
- reason: `no feature-expansion candidate cleared 05DP on holdout`

## Read

- read: `this batch asks which extra semantic block is actually additive once the 05DP logic surface is fixed, rather than whether the logic itself should move again`
