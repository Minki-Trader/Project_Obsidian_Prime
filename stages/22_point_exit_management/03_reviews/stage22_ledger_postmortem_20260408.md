# Stage 22 Ledger Postmortem Review

Generated at: `2026-04-08T12:19:19.047232+00:00`

## Method

- baseline: `22A baseline_time_exit`
- comparison set: `22B break_even`, `22C trailing_stop`, `22D partial_stop_loss`, `22E partial_take_profit`
- unit of analysis: `position_identifier` grouped back into one logical position before comparison
- match key across runs: `entry_bar_time_server + direction`
- note: partial variants inflate ledger rows because one position can emit both a partial close row and a final close row

## Aggregate Read

| variant | mean net delta vs 22A | mean winner clip rate | mean loser mitigation rate | mean big-winner clip rate | mean overlap vs 22A |
|---|---:|---:|---:|---:|---:|
| 22B | -85.567 | 0.209 | 0.142 | 0.234 | 0.916 |
| 22C | -75.590 | 0.313 | 0.083 | 0.713 | 0.894 |
| 22D | -106.933 | 0.208 | 0.465 | 0.227 | 1.000 |
| 22E | -93.893 | 0.404 | 0.088 | 1.000 | 1.000 |

## 2024 historical

- baseline `22A`: return_pct `23.282`, PF `1.1334`, summary trade_count `384`, position_count `384`, max_dd_pct `14.863`

| variant | return_pct | summary trade_count | position_count | ledger rows | net delta vs 22A | winner clip rate | loser mitigation rate | variant-only positions | event share |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 22B | 37.596 | 397 | 397 | 397 | 71.570 | 0.137 | 0.076 | 29 | 0.109 |
| 22C | 15.838 | 410 | 410 | 410 | -37.220 | 0.215 | 0.034 | 56 | 0.195 |
| 22D | 14.086 | 543 | 384 | 543 | -45.980 | 0.135 | 0.396 | 0 | 0.414 |
| 22E | 13.494 | 494 | 384 | 494 | -48.940 | 0.318 | 0.031 | 0 | 0.286 |

- `22B` `break_even`: matched `368`, baseline_only `16`, variant_only `29`, shared delta `-52.840`, baseline_only_profit `24.890`, variant_only_profit `149.300`, close_reasons `{'TIME_EXIT': 349, 'BREAK_EVEN_STOP': 48}`
- `22C` `trailing_stop`: matched `354`, baseline_only `30`, variant_only `56`, shared delta `-69.880`, baseline_only_profit `35.500`, variant_only_profit `68.160`, close_reasons `{'TIME_EXIT': 316, 'TRAIL_STOP': 94}`
- `22D` `partial_stop_loss`: matched `384`, baseline_only `0`, variant_only `0`, shared delta `-45.980`, baseline_only_profit `0.000`, variant_only_profit `0.000`, close_reasons `{'TIME_EXIT': 384, 'PARTIAL_STOP_LOSS': 159}`
- `22E` `partial_take_profit`: matched `384`, baseline_only `0`, variant_only `0`, shared delta `-48.940`, baseline_only_profit `0.000`, variant_only_profit `0.000`, close_reasons `{'TIME_EXIT': 384, 'PARTIAL_TAKE_PROFIT': 110}`

## 2025 validation Jan-Sep

- baseline `22A`: return_pct `122.570`, PF `1.5553`, summary trade_count `405`, position_count `405`, max_dd_pct `12.603`

| variant | return_pct | summary trade_count | position_count | ledger rows | net delta vs 22A | winner clip rate | loser mitigation rate | variant-only positions | event share |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 22B | 74.422 | 442 | 442 | 442 | -240.740 | 0.215 | 0.198 | 75 | 0.237 |
| 22C | 94.626 | 467 | 467 | 467 | -139.720 | 0.361 | 0.127 | 108 | 0.351 |
| 22D | 82.834 | 611 | 405 | 611 | -198.680 | 0.254 | 0.489 | 0 | 0.509 |
| 22E | 94.264 | 596 | 405 | 596 | -141.530 | 0.456 | 0.144 | 0 | 0.472 |

- `22B` `break_even`: matched `367`, baseline_only `38`, variant_only `75`, shared delta `-134.130`, baseline_only_profit `197.610`, variant_only_profit `91.000`, close_reasons `{'BREAK_EVEN_STOP': 120, 'TIME_EXIT': 322}`
- `22C` `trailing_stop`: matched `359`, baseline_only `46`, variant_only `108`, shared delta `-177.290`, baseline_only_profit `115.000`, variant_only_profit `152.570`, close_reasons `{'TRAIL_STOP': 193, 'TIME_EXIT': 274}`
- `22D` `partial_stop_loss`: matched `405`, baseline_only `0`, variant_only `0`, shared delta `-198.680`, baseline_only_profit `0.000`, variant_only_profit `0.000`, close_reasons `{'PARTIAL_STOP_LOSS': 206, 'TIME_EXIT': 405}`
- `22E` `partial_take_profit`: matched `405`, baseline_only `0`, variant_only `0`, shared delta `-141.530`, baseline_only_profit `0.000`, variant_only_profit `0.000`, close_reasons `{'PARTIAL_TAKE_PROFIT': 191, 'TIME_EXIT': 405}`

## 2501 OOS

- baseline `22A`: return_pct `68.574`, PF `1.4925`, summary trade_count `275`, position_count `275`, max_dd_pct `19.394`

| variant | return_pct | summary trade_count | position_count | ledger rows | net delta vs 22A | winner clip rate | loser mitigation rate | variant-only positions | event share |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 22B | 51.068 | 290 | 290 | 290 | -87.530 | 0.275 | 0.152 | 47 | 0.226 |
| 22C | 58.608 | 301 | 301 | 301 | -49.830 | 0.362 | 0.088 | 61 | 0.321 |
| 22D | 53.346 | 411 | 275 | 411 | -76.140 | 0.235 | 0.508 | 0 | 0.494 |
| 22E | 50.332 | 390 | 275 | 390 | -91.210 | 0.438 | 0.090 | 0 | 0.418 |

- `22B` `break_even`: matched `243`, baseline_only `32`, variant_only `47`, shared delta `-115.650`, baseline_only_profit `-7.070`, variant_only_profit `21.050`, close_reasons `{'TIME_EXIT': 221, 'BREAK_EVEN_STOP': 69}`
- `22C` `trailing_stop`: matched `240`, baseline_only `35`, variant_only `61`, shared delta `-96.480`, baseline_only_profit `-48.760`, variant_only_profit `-2.110`, close_reasons `{'TIME_EXIT': 198, 'TRAIL_STOP': 103}`
- `22D` `partial_stop_loss`: matched `275`, baseline_only `0`, variant_only `0`, shared delta `-76.140`, baseline_only_profit `0.000`, variant_only_profit `0.000`, close_reasons `{'PARTIAL_STOP_LOSS': 136, 'TIME_EXIT': 275}`
- `22E` `partial_take_profit`: matched `275`, baseline_only `0`, variant_only `0`, shared delta `-91.210`, baseline_only_profit `0.000`, variant_only_profit `0.000`, close_reasons `{'TIME_EXIT': 275, 'PARTIAL_TAKE_PROFIT': 115}`

## Working Conclusion

- `22B break_even` is the clearest winner-clipping candidate when judged against matched baseline winners.
- `22C trailing_stop` changes relatively few positions but still gives away too much shared-position profit when it fires.
- `22D partial_stop_loss` is the strongest risk-control read: it helps more baseline losers than the other variants, but its row inflation and added churn mean it should be framed as containment rather than alpha.
- `22E partial_take_profit` adds bookkeeping churn and clips winners without enough loser relief to justify a rerun as a simple fixed-point rule.
