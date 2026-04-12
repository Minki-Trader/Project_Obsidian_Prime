# Stage 36 Outside Bar Localization Review

- reviewed_on: `2026-04-12`
- stage: `36_outside_bar_localization_diagnostic`
- reference_line: `35A_34d_refcarry_0001`
- simplification_shadow: `35B_34b_simpleref_0001`

## Executive Read

- the remaining `34D` edge is sparse and direct rather than broad and diffuse
- direct outside-bar suppressions fired only `7` times across all three Stage 35 comparison splits
- all direct events were `LONG` and all held the trade exactly `1` extra bar
- the current `test` window had `0` qualifying events, so the sidecar did not shape the test read because it never fired there
- `hist_2024` carried the real value: direct suppressions explain `34.86` of the `36.37` net-profit edge

## Split Decomposition

### validation

- headline `35A minus 35B`: `net=-0.05` `return_pct=-0.010` `pf=0.0022` `dd_pct=0.0004`
- direct suppressions: `count=2` `net=-0.80` `positive=1` `negative=1`
- residual path effects: `shifted_entry=-0.30` `carry_drift=1.05` `carry_trade_count=28`
- shifted-entry note: `35B` re-entered `SHORT` at `2025-04-09 21:25`, while `35A` entered one bar later at `2025-04-09 21:30`

### test

- headline `35A minus 35B`: `net=0.00` `return_pct=0.000` `pf=0.0000` `dd_pct=0.0000`
- direct suppressions: `count=0` `net=0.00` `positive=0` `negative=0`
- residual path effects: `shifted_entry=0.00` `carry_drift=0.00` `carry_trade_count=0`

### hist_2024

- headline `35A minus 35B`: `net=36.37` `return_pct=7.274` `pf=0.0351` `dd_pct=0.1089`
- direct suppressions: `count=5` `net=34.86` `positive=4` `negative=1`
- residual path effects: `shifted_entry=0.00` `carry_drift=1.51` `carry_trade_count=96`

## Direct Event Context

- decision reason breakdown: `DUAL_SIGNAL_TIE_OR_MARGIN_FAIL=4` `LONG_MARGIN_FAIL=3`
- session breakdown: `ny_cash=5` `ny_postcash=2`
- weekday breakdown: `Mon=2` `Tue=1` `Wed=1` `Thu=2` `Fri=1`
- later-close shape: `STATE_EXIT_MARGIN -> STATE_EXIT_MARGIN=5` `STATE_EXIT_MARGIN -> TIME_EXIT_NY_POSTCASH=2`

## Highest-Impact Direct Events

- `hist_2024` `2024-11-05 16:45` `LONG`: `delta=15.68` `35B_exit=STATE_EXIT_MARGIN` `35A_exit=STATE_EXIT_MARGIN` `ny=Tue 11:45`
- `hist_2024` `2024-12-02 16:45` `LONG`: `delta=13.99` `35B_exit=STATE_EXIT_MARGIN` `35A_exit=STATE_EXIT_MARGIN` `ny=Mon 11:45`
- `hist_2024` `2024-08-15 16:45` `LONG`: `delta=7.54` `35B_exit=STATE_EXIT_MARGIN` `35A_exit=STATE_EXIT_MARGIN` `ny=Thu 12:45`
- `hist_2024` `2024-03-18 16:50` `LONG`: `delta=-5.17` `35B_exit=STATE_EXIT_MARGIN` `35A_exit=STATE_EXIT_MARGIN` `ny=Mon 12:50`
- `validation` `2025-01-03 16:50` `LONG`: `delta=-4.80` `35B_exit=STATE_EXIT_MARGIN` `35A_exit=STATE_EXIT_MARGIN` `ny=Fri 11:50`

## Decision Bias

- keep `34D` unchanged; the sidecar value is real even though it is sparse
- do not reopen the closed `remove the sidecar entirely` simplification path; this stage shows exactly why the broad removal lost the older-window edge
- if simplification reopens later, target a narrower filter around the long no-entry state-exit subset rather than day-of-week rules or a full sidecar rollback
