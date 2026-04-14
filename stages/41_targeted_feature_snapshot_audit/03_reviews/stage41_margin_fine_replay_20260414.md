# Stage 41 Margin Fine Replay

- reviewed_on_utc: `2026-04-14T15:28:03.147386+00:00`
- replay surface: `34D latest-window contract-aligned fine min_margin replay around 0.06000`
- centerpoint source: `reuse 41F / 34D margin 0.06000`

## Executive Read

- the fine replay keeps `0.06000` as the local best point on the tested `34D` operating surface
- versus the `34D` contract baseline at `0.0675`, the best tested point delivered `net=10.39` `return_pct=2.078` `trade_count=15` `pf=0.0847` `max_dd_pct=-0.9851` `ulcer=0.0231` `long=21` `short=33` `no_trade=-54`
- versus the `34D` built-in reference at `0.0675`, the best tested point delivered `net=-5.89` `return_pct=-1.178` `trade_count=7` `pf=-0.0015` `max_dd_pct=3.0633` `ulcer=3.9021` `long=-7` `short=32` `no_trade=-25`

## References

- built-in reference `34D` `min_margin=0.0675` `net=-84.47` `return_pct=-16.894` `trade_count=99` `pf=0.6373` `max_dd_pct=17.6059`
- contract baseline `34D` `min_margin=0.0675` `net=-100.75` `return_pct=-20.150` `trade_count=91` `pf=0.5511` `max_dd_pct=21.6542`

## Fine Replay Results

- `34D margin 0.05875` `min_margin=0.05875` `net=-91.20` `return_pct=-18.240` `trade_count=110` `pf=0.6541` `max_dd_pct=21.8053` `ulcer=12.4410` `long=126` `short=137` `no_trade=1953`
- `34D margin 0.06000` `min_margin=0.06000` `net=-90.36` `return_pct=-18.072` `trade_count=106` `pf=0.6358` `max_dd_pct=20.6692` `ulcer=12.2651` `long=118` `short=132` `no_trade=1966`
- `34D margin 0.06125` `min_margin=0.06125` `net=-96.12` `return_pct=-19.224` `trade_count=105` `pf=0.6119` `max_dd_pct=21.2323` `ulcer=12.4668` `long=115` `short=126` `no_trade=1975`

## Centerpoint Read

- `34D margin 0.06000` `min_margin=0.06000` `net=-90.36` `return_pct=-18.072` `trade_count=106` `pf=0.6358` `max_dd_pct=20.6692` `ulcer=12.2651` `long=118` `short=132` `no_trade=1966`
- versus contract baseline `net=10.39` `return_pct=2.078` `trade_count=15` `pf=0.0847` `max_dd_pct=-0.9851` `ulcer=0.0231` `long=21` `short=33` `no_trade=-54`
- versus built-in reference `net=-5.89` `return_pct=-1.178` `trade_count=7` `pf=-0.0015` `max_dd_pct=3.0633` `ulcer=3.9021` `long=-7` `short=32` `no_trade=-25`

## Pairwise Versus Center

- `34D margin 0.05875`
  headline delta: `net=-0.84` `return_pct=-0.168` `trade_count=4` `pf=0.0183` `max_dd_pct=1.1362` `ulcer=0.1759` `long=8` `short=5` `no_trade=-13`
  ready-row diff: `shared_ready_rows=2216` `decision_diffs=13` `decision_reason_diffs=13` `trade_action_diffs=30`
  trade ledger diff: `left_trade_count=106` `right_trade_count=110` `mismatch_rows=4`
- `34D margin 0.06125`
  headline delta: `net=-5.76` `return_pct=-1.152` `trade_count=-1` `pf=-0.0239` `max_dd_pct=0.5632` `ulcer=0.2017` `long=-3` `short=-6` `no_trade=9`
  ready-row diff: `shared_ready_rows=2216` `decision_diffs=9` `decision_reason_diffs=9` `trade_action_diffs=12`
  trade ledger diff: `left_trade_count=106` `right_trade_count=105` `mismatch_rows=1`

## Best Reason Shift

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

- the fine replay is meant to answer a narrow operating question: whether the coarse `0.0600` candidate was a stable local peak or just a coarse-grid artifact
- within the tested neighborhood, the centerpoint survived the local check, so the evidence now supports treating `0.06000` as the best tested operating candidate rather than only a coarse-sweep hypothesis
- this still does not by itself resolve the remaining contract-versus-built-in residual tax; it only sharpens the best-tested operating gate on the contract-aligned lane
