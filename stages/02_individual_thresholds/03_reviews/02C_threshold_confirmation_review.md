# 02C Threshold Confirmation Review

Generated at: `2026-03-28T04:54:19.832210+00:00`

## Scope

- purpose: `confirm how the Stage 02 threshold candidates behave on the untouched Stage 01 final-model test split`
- status: `review-only confirmation; final threshold freeze intentionally deferred`
- execution assumptions: `min_margin=0, no overlap, no flip, 3-bar time exit, zero cost`

## Preferred Seed On Test

- preferred seed `(Ts=0.60, Tl=0.40)`: test_compounded_return=`0.0554`, test_trades=`386`, test_longs=`381`, test_shorts=`5`, test_rank_within_02A_grid=`22`

## Balanced Challenger On Test

- balanced challenger `(Ts=0.45, Tl=0.50)`: test_compounded_return=`0.0838`, test_trades=`238`, test_longs=`18`, test_shorts=`220`, test_rank_within_02A_grid=`13`

## Reference Reads

- default reference `(1/3, 1/3)`: test_compounded_return=`0.2312`, test_trades=`1180`
- strongest test pair inside current 02A grid: `(Ts=0.35, Tl=0.40)`, test_compounded_return=`0.2212`
- valid/test spearman over compounded-return ranking: `-0.455`

## Top Test Reads

- `(Ts=0.35, Tl=0.40)`: test_compounded_return=0.2212, valid_compounded_return=-0.0879, test_trades=908, test_longs=203, test_shorts=705, test_max_drawdown=-0.0296
- `(Ts=0.35, Tl=0.35)`: test_compounded_return=0.1675, valid_compounded_return=-0.0997, test_trades=1052, test_longs=458, test_shorts=594, test_max_drawdown=-0.0461
- `(Ts=0.40, Tl=0.40)`: test_compounded_return=0.1541, valid_compounded_return=-0.0303, test_trades=613, test_longs=222, test_shorts=391, test_max_drawdown=-0.0438
- `(Ts=0.35, Tl=0.45)`: test_compounded_return=0.1292, valid_compounded_return=-0.1491, test_trades=882, test_longs=65, test_shorts=817, test_max_drawdown=-0.0415
- `(Ts=0.40, Tl=0.45)`: test_compounded_return=0.1125, valid_compounded_return=-0.1059, test_trades=515, test_longs=70, test_shorts=445, test_max_drawdown=-0.0422
- `(Ts=0.40, Tl=0.50)`: test_compounded_return=0.1076, valid_compounded_return=-0.0542, test_trades=499, test_longs=13, test_shorts=486, test_max_drawdown=-0.0416
- `(Ts=0.45, Tl=0.55)`: test_compounded_return=0.0895, valid_compounded_return=-0.0161, test_trades=224, test_longs=1, test_shorts=223, test_max_drawdown=-0.0284
- `(Ts=0.40, Tl=0.35)`: test_compounded_return=0.0864, valid_compounded_return=-0.0512, test_trades=924, test_longs=562, test_shorts=362, test_max_drawdown=-0.0385
- `(Ts=0.40, Tl=0.55)`: test_compounded_return=0.0851, valid_compounded_return=-0.1052, test_trades=494, test_longs=1, test_shorts=493, test_max_drawdown=-0.0416
- `(Ts=0.45, Tl=0.40)`: test_compounded_return=0.0850, valid_compounded_return=-0.0077, test_trades=487, test_longs=300, test_shorts=187, test_max_drawdown=-0.0379
- `(Ts=0.45, Tl=0.65)`: test_compounded_return=0.0841, valid_compounded_return=-0.0373, test_trades=223, test_longs=0, test_shorts=223, test_max_drawdown=-0.0284
- `(Ts=0.45, Tl=0.60)`: test_compounded_return=0.0841, valid_compounded_return=-0.0457, test_trades=223, test_longs=0, test_shorts=223, test_max_drawdown=-0.0284

## Verdict

- verdict: `do not freeze Stage 02 threshold yet; confirmation shows a material valid-test rank mismatch`
- read: the currently preferred valid-side seed stays profitable on test, but it is not the top-ranked test pair, and the test ranking differs materially from the valid ranking.
- implication: keep the preferred seed provisional, preserve the balanced challenger, and defer the final threshold freeze until we decide how to handle this rank mismatch.
