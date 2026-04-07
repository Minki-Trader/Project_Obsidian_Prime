# Selection Status

- stage: `21_retrain_cadence_wfo`
- long-window comparison window: `2025-01-01 <= t < 2026-03-01`
- long-window direct mt5 slow-lookback leader: `21P / 2M`
- long-window slow leader return_pct: `-5.512`
- long-window slow leader net_profit: `-27.56`
- long-window slow leader PF: `0.9906`
- long-window slow leader trades: `1514`
- long-window slow leader max_dd_pct: `54.867`
- long-window slow leader positive months: `6/14`
- long-window 18E baseline run: `21e18_2501_long14m`
- long-window 18E return_pct: `30.974`
- long-window 18E net_profit: `154.87`
- long-window 18E PF: `1.2131`
- long-window 18E trades: `283`
- long-window 18E max_dd_pct: `14.801`
- comparison note: `2M is much better than 2W, 1M, and the earlier short-lookback retrains, but it still loses to the fixed 18E baseline by a wide margin`
- conclusion: `do not promote monthly retraining over the fixed 18E baseline on the long 2501 window`
- next action: `if we keep exploring retraining, move slower still or change the cadence itself rather than shrinking or lightly extending the lookback alone`
