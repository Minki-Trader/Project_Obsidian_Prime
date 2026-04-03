# 05CE Stage 05 Downside Proxy Batch Review

Generated at: `2026-03-30T13:09:48.506559+00:00`

## Scope

- purpose: `extend the persistence-family frontier with downside, risk-off, leader-drag, and session-aware semantic proxies`
- model family: `trend_proxy_sector_logreg`
- reference runs: `05W`, `05BB`, `05BF`, `05AH`, `05AI`

## MT5 Validation Ranking

- [1] `05W_no_trend_strength_0001`: variant=`incumbent_05w`, groups=`-`, return_pct=91.168, profit_factor=1.4092, max_dd_pct=11.1472, ulcer_index=6.5205, trades=493, ready_gap=0, unexpected_skips=0
- [2] `05BF_trend_proxy_persistence_volatility_0001`: variant=`persistence_volatility_reference`, groups=`-`, return_pct=89.422, profit_factor=1.4012, max_dd_pct=11.9463, ulcer_index=7.1506, trades=487, ready_gap=0, unexpected_skips=0
- [3] `05AI_trend_proxy_light_pb_0001`: variant=`light_pb_reference`, groups=`-`, return_pct=86.868, profit_factor=1.3884, max_dd_pct=11.7173, ulcer_index=6.8444, trades=485, ready_gap=0, unexpected_skips=0
- [4] `05CA_trend_proxy_persistence_riskoff_0001`: variant=`persistence_riskoff`, groups=`trend_proxy_persistence, trend_proxy_risk_off_confirmation`, return_pct=84.152, profit_factor=1.3760, max_dd_pct=12.0537, ulcer_index=7.2741, trades=488, ready_gap=0, unexpected_skips=0
- [5] `05CC_trend_proxy_persistence_downside_riskoff_0001`: variant=`persistence_downside_riskoff`, groups=`trend_proxy_persistence, trend_proxy_downside_pressure, trend_proxy_risk_off_confirmation`, return_pct=78.506, profit_factor=1.3414, max_dd_pct=12.0064, ulcer_index=7.2488, trades=495, ready_gap=0, unexpected_skips=0
- [6] `05BZ_trend_proxy_persistence_downside_0001`: variant=`persistence_downside`, groups=`trend_proxy_persistence, trend_proxy_downside_pressure`, return_pct=78.354, profit_factor=1.3388, max_dd_pct=12.2728, ulcer_index=7.3679, trades=494, ready_gap=0, unexpected_skips=0
- [7] `05BB_trend_proxy_persistence_only_0001`: variant=`persistence_only_reference`, groups=`-`, return_pct=75.676, profit_factor=1.3308, max_dd_pct=12.3455, ulcer_index=7.2609, trades=490, ready_gap=0, unexpected_skips=0
- [8] `05CD_trend_proxy_persistence_session_riskoff_0001`: variant=`persistence_session_riskoff`, groups=`trend_proxy_persistence, trend_proxy_session_pressure, trend_proxy_risk_off_confirmation`, return_pct=73.066, profit_factor=1.3154, max_dd_pct=12.0517, ulcer_index=7.1456, trades=489, ready_gap=0, unexpected_skips=0
- [9] `05CB_trend_proxy_persistence_leader_drag_0001`: variant=`persistence_leader_drag`, groups=`trend_proxy_persistence, trend_proxy_leader_drag`, return_pct=69.212, profit_factor=1.2934, max_dd_pct=12.1108, ulcer_index=7.2745, trades=489, ready_gap=0, unexpected_skips=0
- [10] `05AH_trend_proxy_sector_replacement_0001`: variant=`full_proxy_reference`, groups=`-`, return_pct=62.200, profit_factor=1.2632, max_dd_pct=13.4545, ulcer_index=7.9225, trades=489, ready_gap=0, unexpected_skips=0

## MT5 Holdout Ranking

- [1] `05CC_trend_proxy_persistence_downside_riskoff_0001`: variant=`persistence_downside_riskoff`, groups=`trend_proxy_persistence, trend_proxy_downside_pressure, trend_proxy_risk_off_confirmation`, return_pct=47.402, profit_factor=1.3367, max_dd_pct=15.5405, ulcer_index=6.0251, trades=333, ready_gap=35, unexpected_skips=0
- [2] `05BB_trend_proxy_persistence_only_0001`: variant=`persistence_only_reference`, groups=`-`, return_pct=44.792, profit_factor=1.3193, max_dd_pct=15.5405, ulcer_index=6.3183, trades=328, ready_gap=35, unexpected_skips=0
- [3] `05AH_trend_proxy_sector_replacement_0001`: variant=`full_proxy_reference`, groups=`-`, return_pct=44.558, profit_factor=1.3109, max_dd_pct=17.7040, ulcer_index=7.1521, trades=331, ready_gap=35, unexpected_skips=0
- [4] `05BF_trend_proxy_persistence_volatility_0001`: variant=`persistence_volatility_reference`, groups=`-`, return_pct=40.462, profit_factor=1.2801, max_dd_pct=17.0166, ulcer_index=6.9935, trades=331, ready_gap=35, unexpected_skips=0
- [5] `05CA_trend_proxy_persistence_riskoff_0001`: variant=`persistence_riskoff`, groups=`trend_proxy_persistence, trend_proxy_risk_off_confirmation`, return_pct=38.456, profit_factor=1.2639, max_dd_pct=17.0166, ulcer_index=7.0800, trades=330, ready_gap=35, unexpected_skips=0
- [6] `05AI_trend_proxy_light_pb_0001`: variant=`light_pb_reference`, groups=`-`, return_pct=37.274, profit_factor=1.2542, max_dd_pct=17.0373, ulcer_index=7.7860, trades=330, ready_gap=35, unexpected_skips=0
- [7] `05W_no_trend_strength_0001`: variant=`incumbent_05w`, groups=`-`, return_pct=33.538, profit_factor=1.2253, max_dd_pct=17.0166, ulcer_index=7.8344, trades=336, ready_gap=35, unexpected_skips=0

## Verdict

- status: `mixed_holdout_win_keep_incumbent`
- selected_run_name: `05W_no_trend_strength_0001`
- reason: `downside-aware persistence proxy improved holdout but did not lead validation, so the incumbent stays promoted for now`

## Read

- read: `this batch asks whether the persistence edge improves when downside/risk-off structure is added instead of reintroducing the old trend-strength cluster`
