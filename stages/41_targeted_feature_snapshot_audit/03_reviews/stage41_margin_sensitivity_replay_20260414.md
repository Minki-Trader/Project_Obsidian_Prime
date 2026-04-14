# Stage 41 Margin Sensitivity Replay

- reviewed_on_utc: `2026-04-14T15:19:31.969584+00:00`
- replay surface: `34B latest-window contract-aligned min_margin sweep around 0.0675`
- confirmation surface: `34D latest-window contract-aligned replay at the best 34B min_margin candidate`

## Executive Read

- relaxing the fixed `max_probability_margin` gate from `0.0675` to `0.0600` was the only tested move that materially improved the contract-aligned latest-window KPI surface
- the `0.0600` replay improved the contract-aligned baseline by `net +10.39`, `return_pct +2.078`, `trade_count +15`, `profit_factor +0.0847`, and `max_dd_pct -0.9851`, while stricter settings from `0.0625` through `0.0700` were flat-to-worse
- the same `0.0600` replay matched exactly on the operating `34D` bundle versus the simpler `34B` bundle in this latest window sample, so the candidate is not a 34B-only artifact

## References

- built-in reference `34B/34D` `min_margin=0.0675` `net=-84.47` `return_pct=-16.894` `trade_count=99` `pf=0.6373` `max_dd_pct=17.6059`
- contract baseline `34B/34D` `min_margin=0.0675` `net=-100.75` `return_pct=-20.150` `trade_count=91` `pf=0.5511` `max_dd_pct=21.6542`

## Sweep Results

- `34B margin 0.0600` `min_margin=0.0600` `net=-90.36` `return_pct=-18.072` `trade_count=106` `pf=0.6358` `max_dd_pct=20.6692` `ulcer=12.2651` `long=118` `short=132` `no_trade=1966`
- `34B margin 0.0625` `min_margin=0.0625` `net=-102.98` `return_pct=-20.596` `trade_count=104` `pf=0.5784` `max_dd_pct=22.5491` `ulcer=13.2656` `long=113` `short=120` `no_trade=1983`
- `34B margin 0.0650` `min_margin=0.0650` `net=-102.40` `return_pct=-20.480` `trade_count=99` `pf=0.5589` `max_dd_pct=21.9780` `ulcer=12.6963` `long=107` `short=106` `no_trade=2003`
- `34B margin 0.0675` `min_margin=0.0675` `net=-100.75` `return_pct=-20.150` `trade_count=91` `pf=0.5511` `max_dd_pct=21.6542` `ulcer=12.2420` `long=97` `short=99` `no_trade=2020`
- `34B margin 0.0700` `min_margin=0.0700` `net=-116.96` `return_pct=-23.392` `trade_count=87` `pf=0.4743` `max_dd_pct=24.8352` `ulcer=13.4347` `long=86` `short=87` `no_trade=2043`

## Best Candidate

- `34B margin 0.0600` `min_margin=0.0600` `net=-90.36` `return_pct=-18.072` `trade_count=106` `pf=0.6358` `max_dd_pct=20.6692` `ulcer=12.2651` `long=118` `short=132` `no_trade=1966`
- `delta_vs_contract_baseline` `net=10.39` `return_pct=2.078` `trade_count=15` `pf=0.0847` `max_dd_pct=-0.9851` `ulcer=0.0231` `long=21` `short=33` `no_trade=-54`
- `delta_vs_builtin_reference` `net=-5.89` `return_pct=-1.178` `trade_count=7` `pf=-0.0015` `max_dd_pct=3.0633` `ulcer=3.9021` `long=-7` `short=32` `no_trade=-25`

## Baseline Deltas

- `34B margin 0.0600`
  contract baseline: `vs_contract` `net=10.39` `return_pct=2.078` `trade_count=15` `pf=0.0847` `max_dd_pct=-0.9851` `ulcer=0.0231` `long=21` `short=33` `no_trade=-54`
  built-in reference: `vs_builtin` `net=-5.89` `return_pct=-1.178` `trade_count=7` `pf=-0.0015` `max_dd_pct=3.0633` `ulcer=3.9021` `long=-7` `short=32` `no_trade=-25`
- `34B margin 0.0625`
  contract baseline: `vs_contract` `net=-2.23` `return_pct=-0.446` `trade_count=13` `pf=0.0273` `max_dd_pct=0.8948` `ulcer=1.0237` `long=16` `short=21` `no_trade=-37`
  built-in reference: `vs_builtin` `net=-18.51` `return_pct=-3.702` `trade_count=5` `pf=-0.0589` `max_dd_pct=4.9432` `ulcer=4.9027` `long=-12` `short=20` `no_trade=-8`
- `34B margin 0.0650`
  contract baseline: `vs_contract` `net=-1.65` `return_pct=-0.330` `trade_count=8` `pf=0.0078` `max_dd_pct=0.3238` `ulcer=0.4544` `long=10` `short=7` `no_trade=-17`
  built-in reference: `vs_builtin` `net=-17.93` `return_pct=-3.586` `trade_count=0` `pf=-0.0784` `max_dd_pct=4.3721` `ulcer=4.3334` `long=-18` `short=6` `no_trade=12`
- `34B margin 0.0675`
  contract baseline: `vs_contract` `net=0.00` `return_pct=0.000` `trade_count=0` `pf=0.0000` `max_dd_pct=0.0000` `ulcer=0.0000` `long=0` `short=0` `no_trade=0`
  built-in reference: `vs_builtin` `net=-16.28` `return_pct=-3.256` `trade_count=-8` `pf=-0.0862` `max_dd_pct=4.0484` `ulcer=3.8790` `long=-28` `short=-1` `no_trade=29`
- `34B margin 0.0700`
  contract baseline: `vs_contract` `net=-16.21` `return_pct=-3.242` `trade_count=-4` `pf=-0.0768` `max_dd_pct=3.1809` `ulcer=1.1928` `long=-11` `short=-12` `no_trade=23`
  built-in reference: `vs_builtin` `net=-32.49` `return_pct=-6.498` `trade_count=-12` `pf=-0.1631` `max_dd_pct=7.2293` `ulcer=5.0718` `long=-39` `short=-13` `no_trade=52`

## Operating Confirmation

- `34D margin 0.0600` `min_margin=0.0600` `net=-90.36` `return_pct=-18.072` `trade_count=106` `pf=0.6358` `max_dd_pct=20.6692` `ulcer=12.2651` `long=118` `short=132` `no_trade=1966`
- headline diff versus best `34B 0.0600`: `net=0.00` `return_pct=0.000` `trade_count=0` `pf=0.0000` `max_dd_pct=0.0000`
- shadow parity `shared_rows=8188` `shared_ready_rows=2216` `decision_diffs=0` `decision_reason_diffs=0` `trade_action_diffs=0`
- trade ledger parity `left_trade_count=106` `right_trade_count=106` `mismatch_rows=0`

## Decision Reason Shift

- `DUAL_SIGNAL_TIE_OR_MARGIN_FAIL` `delta=-29` `best=611` `baseline=640`
- `DUAL_SIGNAL_SHORT_WINS` `delta=20` `best=91` `baseline=71`
- `SHORT_FILTERS_OK` `delta=13` `best=41` `baseline=28`
- `LONG_FILTERS_OK` `delta=12` `best=66` `baseline=54`
- `LONG_MARGIN_FAIL` `delta=-12` `best=327` `baseline=339`
- `DUAL_SIGNAL_LONG_WINS` `delta=9` `best=52` `baseline=43`
- `SHORT_MARGIN_FAIL` `delta=-7` `best=96` `baseline=103`
- `SHORT_MARGIN_FAIL_SOFT_CONTEXT` `delta=-6` `best=32` `baseline=38`
- `LONG_MARGIN_FAIL_SOFT_CONTEXT` `delta=0` `best=3` `baseline=3`
- `SKIPPED` `delta=0` `best=5972` `baseline=5972`

## Interpretation

- the fixed margin gate is now confirmed as a live lever rather than just a descriptive hypothesis: a narrow relaxation to `0.0600` recovers directional participation and improves both headline return and drawdown versus the contract baseline
- the recovery is only partial relative to the built-in lane, so the contract-aligned feature surface still carries some residual tax even after the margin adjustment
- the next high-signal follow-up is a finer `34D`-only replay around `0.0600`, for example `0.05875 / 0.0600 / 0.06125`, before deciding whether to treat `0.0600` as a new operating candidate
