# 05DV Stage 05 Downside Local Probe Review

Generated at: `2026-03-30T14:08:53.606376+00:00`

## Scope

- purpose: `run a narrow local probe around the 05CA/05CC hold5 line using only mild margin and hold-window tweaks`
- promoted incumbent: `05DJ`

## MT5 Validation Ranking

- [1] `05DP_05ca_margin0675_hold5_0001`: variant=`05ca_m0675_h5`, groups=`trend_proxy_persistence, trend_proxy_risk_off_confirmation`, margin=0.0675, hold=5, return_pct=122.570, profit_factor=1.5553, max_dd_pct=12.6031, ulcer_index=7.2871, trades=405, ready_gap=0, unexpected_skips=0
- [2] `05DJ_05bf_margin_hold5_0001`: variant=`promoted_05dj`, groups=`-`, margin=-, hold=-, return_pct=119.436, profit_factor=1.5645, max_dd_pct=12.4696, ulcer_index=7.1858, trades=386, ready_gap=0, unexpected_skips=0
- [3] `05DN_05ca_margin_hold5_0001`: variant=`cross_05ca_hold5`, groups=`-`, margin=-, hold=-, return_pct=109.314, profit_factor=1.5024, max_dd_pct=13.2239, ulcer_index=7.5148, trades=388, ready_gap=0, unexpected_skips=0
- [4] `05DQ_05ca_margin0725_hold5_0001`: variant=`05ca_m0725_h5`, groups=`trend_proxy_persistence, trend_proxy_risk_off_confirmation`, margin=0.0725, hold=5, return_pct=106.636, profit_factor=1.5021, max_dd_pct=15.8403, ulcer_index=7.5284, trades=375, ready_gap=0, unexpected_skips=0
- [5] `05DR_05cc_margin0675_hold5_0001`: variant=`05cc_m0675_h5`, groups=`trend_proxy_persistence, trend_proxy_downside_pressure, trend_proxy_risk_off_confirmation`, margin=0.0675, hold=5, return_pct=102.060, profit_factor=1.4440, max_dd_pct=14.2717, ulcer_index=7.8671, trades=408, ready_gap=0, unexpected_skips=0
- [6] `05DL_05cc_margin_hold5_0001`: variant=`cross_05cc_hold5`, groups=`-`, margin=-, hold=-, return_pct=99.682, profit_factor=1.4448, max_dd_pct=14.9161, ulcer_index=7.6350, trades=393, ready_gap=0, unexpected_skips=0
- [7] `05DT_05ca_margin0700_hold6_0001`: variant=`05ca_m0700_h6`, groups=`trend_proxy_persistence, trend_proxy_risk_off_confirmation`, margin=0.0700, hold=6, return_pct=92.632, profit_factor=1.4004, max_dd_pct=14.8844, ulcer_index=9.3741, trades=358, ready_gap=0, unexpected_skips=0
- [8] `05DU_05cc_margin0700_hold6_0001`: variant=`05cc_m0700_h6`, groups=`trend_proxy_persistence, trend_proxy_downside_pressure, trend_proxy_risk_off_confirmation`, margin=0.0700, hold=6, return_pct=91.588, profit_factor=1.4009, max_dd_pct=15.4154, ulcer_index=9.2171, trades=360, ready_gap=0, unexpected_skips=0
- [9] `05DS_05cc_margin0725_hold5_0001`: variant=`05cc_m0725_h5`, groups=`trend_proxy_persistence, trend_proxy_downside_pressure, trend_proxy_risk_off_confirmation`, margin=0.0725, hold=5, return_pct=86.434, profit_factor=1.3771, max_dd_pct=16.0091, ulcer_index=7.7280, trades=382, ready_gap=0, unexpected_skips=0

## MT5 Holdout Ranking

- [1] `05DP_05ca_margin0675_hold5_0001`: variant=`05ca_m0675_h5`, groups=`trend_proxy_persistence, trend_proxy_risk_off_confirmation`, margin=0.0675, hold=5, return_pct=68.574, profit_factor=1.4925, max_dd_pct=19.3936, ulcer_index=5.8587, trades=275, ready_gap=35, unexpected_skips=0
- [2] `05DN_05ca_margin_hold5_0001`: variant=`cross_05ca_hold5`, groups=`-`, margin=-, hold=-, return_pct=60.940, profit_factor=1.4517, max_dd_pct=20.2732, ulcer_index=6.2392, trades=263, ready_gap=35, unexpected_skips=0
- [3] `05DJ_05bf_margin_hold5_0001`: variant=`promoted_05dj`, groups=`-`, margin=-, hold=-, return_pct=59.190, profit_factor=1.4283, max_dd_pct=20.2732, ulcer_index=6.1801, trades=265, ready_gap=35, unexpected_skips=0
- [4] `05DL_05cc_margin_hold5_0001`: variant=`cross_05cc_hold5`, groups=`-`, margin=-, hold=-, return_pct=58.852, profit_factor=1.4311, max_dd_pct=18.3944, ulcer_index=5.5864, trades=267, ready_gap=35, unexpected_skips=0
- [5] `05DQ_05ca_margin0725_hold5_0001`: variant=`05ca_m0725_h5`, groups=`trend_proxy_persistence, trend_proxy_risk_off_confirmation`, margin=0.0725, hold=5, return_pct=54.478, profit_factor=1.4179, max_dd_pct=21.3567, ulcer_index=6.6866, trades=250, ready_gap=35, unexpected_skips=0

## Verdict

- status: `promote_candidate`
- selected_run_name: `05DP_05ca_margin0675_hold5_0001`
- reason: `local-probe candidate led both validation and holdout versus the promoted incumbent`

## Read

- read: `this is a local neighborhood test, not a new family; the goal is to see whether the near-tie versus 05DJ can be resolved with small changes only`
