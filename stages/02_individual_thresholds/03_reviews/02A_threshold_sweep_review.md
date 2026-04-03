# 02A Threshold Sweep Review

Generated at: `2026-03-28T04:32:36.217314+00:00`

## Scope

- purpose: `search short_threshold and long_threshold only on the Stage 01 search-side model`
- source run: `01C_run_0001_h03_band000125_logreg`
- reserved final confirmation model: `01D_run_0001_final_h03_band000125_logreg`
- source model family: `logistic_regression`
- horizon: `3` bars
- source band: `0.00125`
- search split: `valid`
- execution assumptions: `min_margin=0, no overlap, no flip, 3-bar time exit, zero cost`
- selection metric: `valid_compounded_return`
- qualified threshold pairs after min-trades filter: `42`

## Reference Reads

- default threshold reference (`1/3`, `1/3`): compounded_return=`-0.1270`, trades=`2292`
- best symmetric pair: `(0.45, 0.45)`, compounded_return=`0.0199`, trades=`766`

## Top Results

- `(Ts=0.60, Tl=0.40)`: compounded_return=0.1342, mean_trade_return=0.000146, trades=925, longs=915, shorts=10, max_drawdown=-0.0759
- `(Ts=0.55, Tl=0.40)`: compounded_return=0.1254, mean_trade_return=0.000134, trades=946, longs=903, shorts=43, max_drawdown=-0.0759
- `(Ts=0.55, Tl=0.35)`: compounded_return=0.1245, mean_trade_return=0.000078, trades=1622, longs=1581, shorts=41, max_drawdown=-0.0984
- `(Ts=0.65, Tl=0.40)`: compounded_return=0.1231, mean_trade_return=0.000136, trades=920, longs=917, shorts=3, max_drawdown=-0.0759
- `(Ts=0.65, Tl=0.35)`: compounded_return=0.0974, mean_trade_return=0.000064, trades=1606, longs=1603, shorts=3, max_drawdown=-0.1004
- `(Ts=0.45, Tl=0.50)`: compounded_return=0.0914, mean_trade_return=0.000166, trades=573, longs=183, shorts=390, max_drawdown=-0.0667
- `(Ts=0.60, Tl=0.35)`: compounded_return=0.0820, mean_trade_return=0.000055, trades=1609, longs=1600, shorts=9, max_drawdown=-0.1115
- `(Ts=0.50, Tl=0.40)`: compounded_return=0.0460, mean_trade_return=0.000053, trades=994, longs=856, shorts=138, max_drawdown=-0.0867
- `(Ts=0.65, Tl=0.45)`: compounded_return=0.0459, mean_trade_return=0.000115, trades=444, longs=441, shorts=3, max_drawdown=-0.0815
- `(Ts=0.50, Tl=0.55)`: compounded_return=0.0455, mean_trade_return=0.000211, trades=234, longs=88, shorts=146, max_drawdown=-0.0928

## Selection

- selected threshold seed: `(short_threshold=0.60, long_threshold=0.40)`
- selected run folder: `02A_run_0001_threshold_sweep`
- valid compounded return: `0.1342`
- valid mean trade return: `0.000146`
- trade count: `925`
- long trades: `915`
- short trades: `10`
- keep or archive: `keep as current Stage 02 seed`

## Notes

- This phase is intentionally threshold-only. No margin or probability-gap logic was introduced.
- The selected pair is a search-stage seed on `valid`; it is not the final confirmation artifact yet.
- A strongly asymmetric seed is acceptable here as long as later stages decide whether to preserve or regularize it.
