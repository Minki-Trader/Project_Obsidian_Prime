# 05DW Stage 05 05DP Fine Probe Review

Generated at: `2026-03-30T14:28:30.297970+00:00`

## Scope

- purpose: `test whether promoted 05DP is a true local peak by nudging only margin and hold around the 05CA hold5 line`
- promoted incumbent: `05DP`

## MT5 Validation Ranking

- [1] `05DP_05ca_margin0675_hold5_0001`: variant=`promoted_05dp`, margin=-, hold=-, return_pct=122.570, profit_factor=1.5553, max_dd_pct=12.6031, ulcer_index=7.2871, trades=405, ready_gap=0, unexpected_skips=0
- [2] `05EA_05ca_margin0675_hold4_0001`: variant=`05ca_m0675_h4`, margin=0.06750, hold=4, return_pct=115.168, profit_factor=1.5352, max_dd_pct=11.5023, ulcer_index=6.5293, trades=453, ready_gap=0, unexpected_skips=0
- [3] `05DY_05ca_margin06625_hold5_0001`: variant=`05ca_m06625_h5`, margin=0.06625, hold=5, return_pct=114.880, profit_factor=1.5002, max_dd_pct=12.7910, ulcer_index=7.9823, trades=417, ready_gap=0, unexpected_skips=0
- [4] `05DZ_05ca_margin06875_hold5_0001`: variant=`05ca_m06875_h5`, margin=0.06875, hold=5, return_pct=114.538, profit_factor=1.5254, max_dd_pct=12.6031, ulcer_index=7.3992, trades=396, ready_gap=0, unexpected_skips=0
- [5] `05DN_05ca_margin_hold5_0001`: variant=`same_family_05dn`, margin=-, hold=-, return_pct=109.314, profit_factor=1.5024, max_dd_pct=13.2239, ulcer_index=7.5148, trades=388, ready_gap=0, unexpected_skips=0
- [6] `05DX_05ca_margin0650_hold5_0001`: variant=`05ca_m0650_h5`, margin=0.06500, hold=5, return_pct=106.702, profit_factor=1.4447, max_dd_pct=14.8103, ulcer_index=8.4661, trades=433, ready_gap=0, unexpected_skips=0
- [7] `05EB_05ca_margin0675_hold6_0001`: variant=`05ca_m0675_h6`, margin=0.06750, hold=6, return_pct=100.700, profit_factor=1.4368, max_dd_pct=14.1583, ulcer_index=9.0074, trades=373, ready_gap=0, unexpected_skips=0
- [8] `05DL_05cc_margin_hold5_0001`: variant=`risk_alt_05dl`, margin=-, hold=-, return_pct=99.682, profit_factor=1.4448, max_dd_pct=14.9161, ulcer_index=7.6350, trades=393, ready_gap=0, unexpected_skips=0

## MT5 Holdout Ranking

- [1] `05DP_05ca_margin0675_hold5_0001`: variant=`promoted_05dp`, margin=-, hold=-, return_pct=68.574, profit_factor=1.4925, max_dd_pct=19.3936, ulcer_index=5.8587, trades=275, ready_gap=35, unexpected_skips=0
- [2] `05DN_05ca_margin_hold5_0001`: variant=`same_family_05dn`, margin=-, hold=-, return_pct=60.940, profit_factor=1.4517, max_dd_pct=20.2732, ulcer_index=6.2392, trades=263, ready_gap=35, unexpected_skips=0
- [3] `05DL_05cc_margin_hold5_0001`: variant=`risk_alt_05dl`, margin=-, hold=-, return_pct=58.852, profit_factor=1.4311, max_dd_pct=18.3944, ulcer_index=5.5864, trades=267, ready_gap=35, unexpected_skips=0
- [4] `05DY_05ca_margin06625_hold5_0001`: variant=`05ca_m06625_h5`, margin=0.06625, hold=5, return_pct=54.286, profit_factor=1.3589, max_dd_pct=19.3936, ulcer_index=6.3259, trades=285, ready_gap=35, unexpected_skips=0
- [5] `05EA_05ca_margin0675_hold4_0001`: variant=`05ca_m0675_h4`, margin=0.06750, hold=4, return_pct=53.742, profit_factor=1.3652, max_dd_pct=17.9030, ulcer_index=6.2325, trades=304, ready_gap=35, unexpected_skips=0

## Verdict

- status: `reject_keep_incumbent`
- selected_run_name: `05DP_05ca_margin0675_hold5_0001`
- reason: `no fine-probe candidate cleared 05DP on holdout`

## Read

- read: `this is a same-family micro-surface check; if 05DP survives it, the 05CA hold5 line is probably stable enough to re-open broader feature/logic exploration`
