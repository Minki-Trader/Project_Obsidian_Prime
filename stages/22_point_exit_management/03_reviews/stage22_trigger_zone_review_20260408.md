# Stage 22 Trigger Zone Review

Generated at: `2026-04-08T12:27:16.208940+00:00`

- note: `trade ledger floating profit/loss is in account currency at fixed 0.1 lot; for these runs, about 10 points ~= 1.0 currency unit`

## Baseline Trigger Zones

### 2024 historical

- baseline positions: `192` winners, `192` losers

| profit trigger approx points | winner hit rate | loser hit rate | gap |
|---|---:|---:|---:|
| 40 | 0.792 | 0.115 | 0.677 |
| 45 | 0.724 | 0.088 | 0.635 |
| 50 | 0.641 | 0.073 | 0.568 |
| 55 | 0.583 | 0.057 | 0.526 |
| 60 | 0.542 | 0.031 | 0.510 |
| 70 | 0.438 | 0.016 | 0.422 |
| 80 | 0.349 | 0.005 | 0.344 |

| adverse trigger approx points | winner hit rate | loser hit rate | loser-minus-winner gap |
|---|---:|---:|---:|
| 40 | 0.162 | 0.750 | 0.589 |
| 45 | 0.135 | 0.693 | 0.557 |
| 50 | 0.094 | 0.620 | 0.526 |
| 55 | 0.083 | 0.542 | 0.458 |
| 60 | 0.062 | 0.464 | 0.401 |
| 70 | 0.052 | 0.396 | 0.344 |
| 80 | 0.021 | 0.312 | 0.292 |

### 2025 validation Jan-Sep

- baseline positions: `217` winners, `188` losers

| profit trigger approx points | winner hit rate | loser hit rate | gap |
|---|---:|---:|---:|
| 40 | 0.899 | 0.282 | 0.617 |
| 45 | 0.876 | 0.261 | 0.615 |
| 50 | 0.830 | 0.218 | 0.611 |
| 55 | 0.797 | 0.170 | 0.627 |
| 60 | 0.756 | 0.144 | 0.612 |
| 70 | 0.659 | 0.133 | 0.526 |
| 80 | 0.562 | 0.101 | 0.461 |

| adverse trigger approx points | winner hit rate | loser hit rate | loser-minus-winner gap |
|---|---:|---:|---:|
| 40 | 0.290 | 0.835 | 0.545 |
| 45 | 0.254 | 0.803 | 0.550 |
| 50 | 0.207 | 0.750 | 0.543 |
| 55 | 0.180 | 0.702 | 0.522 |
| 60 | 0.129 | 0.638 | 0.509 |
| 70 | 0.088 | 0.553 | 0.466 |
| 80 | 0.060 | 0.404 | 0.344 |

### 2501 OOS

- baseline positions: `153` winners, `122` losers

| profit trigger approx points | winner hit rate | loser hit rate | gap |
|---|---:|---:|---:|
| 40 | 0.804 | 0.262 | 0.542 |
| 45 | 0.765 | 0.189 | 0.576 |
| 50 | 0.739 | 0.131 | 0.607 |
| 55 | 0.719 | 0.107 | 0.612 |
| 60 | 0.680 | 0.090 | 0.590 |
| 70 | 0.601 | 0.066 | 0.536 |
| 80 | 0.523 | 0.033 | 0.490 |

| adverse trigger approx points | winner hit rate | loser hit rate | loser-minus-winner gap |
|---|---:|---:|---:|
| 40 | 0.301 | 0.836 | 0.535 |
| 45 | 0.235 | 0.820 | 0.584 |
| 50 | 0.222 | 0.779 | 0.556 |
| 55 | 0.176 | 0.738 | 0.561 |
| 60 | 0.150 | 0.697 | 0.546 |
| 70 | 0.111 | 0.590 | 0.479 |
| 80 | 0.059 | 0.500 | 0.441 |

## Event Timing By Variant

### 22B `break_even`

- 2024 historical `BREAK_EVEN_STOP` hold bars: `{1: 3, 2: 10, 3: 13, 4: 9, 5: 5}`
  baseline class mix: `{'bar_1_loser': 1, 'bar_1_winner': 2, 'bar_2_loser': 3, 'bar_2_winner': 7, 'bar_3_loser': 5, 'bar_3_winner': 8, 'bar_4_loser': 3, 'bar_4_winner': 6, 'bar_5_loser': 2, 'bar_5_winner': 3}`
- 2025 validation Jan-Sep `BREAK_EVEN_STOP` hold bars: `{1: 20, 2: 18, 3: 22, 4: 12, 5: 15}`
  baseline class mix: `{'bar_1_loser': 7, 'bar_1_winner': 13, 'bar_2_loser': 7, 'bar_2_winner': 11, 'bar_3_loser': 10, 'bar_3_winner': 12, 'bar_4_loser': 5, 'bar_4_winner': 7, 'bar_5_loser': 5, 'bar_5_winner': 10}`
- 2501 OOS `BREAK_EVEN_STOP` hold bars: `{1: 5, 2: 15, 3: 19, 4: 9, 5: 7}`
  baseline class mix: `{'bar_1_winner': 5, 'bar_2_loser': 5, 'bar_2_winner': 10, 'bar_3_loser': 4, 'bar_3_winner': 15, 'bar_4_loser': 5, 'bar_4_winner': 4, 'bar_5_loser': 2, 'bar_5_winner': 5}`

### 22C `trailing_stop`

- 2024 historical `TRAIL_STOP` hold bars: `{1: 2, 2: 20, 3: 16, 4: 13, 5: 18}`
  baseline class mix: `{'bar_1_loser': 1, 'bar_1_winner': 1, 'bar_2_loser': 2, 'bar_2_winner': 18, 'bar_3_loser': 3, 'bar_3_winner': 13, 'bar_4_winner': 13, 'bar_5_winner': 18}`
- 2025 validation Jan-Sep `TRAIL_STOP` hold bars: `{1: 26, 2: 32, 3: 31, 4: 16, 5: 21}`
  baseline class mix: `{'bar_1_loser': 5, 'bar_1_winner': 21, 'bar_2_loser': 7, 'bar_2_winner': 25, 'bar_3_loser': 6, 'bar_3_winner': 25, 'bar_4_loser': 2, 'bar_4_winner': 14, 'bar_5_loser': 1, 'bar_5_winner': 20}`
- 2501 OOS `TRAIL_STOP` hold bars: `{1: 5, 2: 23, 3: 24, 4: 11, 5: 14}`
  baseline class mix: `{'bar_1_loser': 1, 'bar_1_winner': 4, 'bar_2_loser': 4, 'bar_2_winner': 19, 'bar_3_loser': 2, 'bar_3_winner': 22, 'bar_4_winner': 11, 'bar_5_loser': 2, 'bar_5_winner': 12}`

### 22D `partial_stop_loss`

- 2024 historical `PARTIAL_STOP_LOSS` hold bars: `{1: 37, 2: 55, 3: 35, 4: 22, 5: 10}`
  baseline class mix: `{'bar_1_loser': 25, 'bar_1_winner': 12, 'bar_2_loser': 48, 'bar_2_winner': 7, 'bar_3_loser': 29, 'bar_3_winner': 6, 'bar_4_loser': 21, 'bar_4_winner': 1, 'bar_5_loser': 10}`
- 2025 validation Jan-Sep `PARTIAL_STOP_LOSS` hold bars: `{1: 90, 2: 53, 3: 23, 4: 29, 5: 11}`
  baseline class mix: `{'bar_1_loser': 56, 'bar_1_winner': 34, 'bar_2_loser': 40, 'bar_2_winner': 13, 'bar_3_loser': 16, 'bar_3_winner': 7, 'bar_4_loser': 28, 'bar_4_winner': 1, 'bar_5_loser': 11}`
- 2501 OOS `PARTIAL_STOP_LOSS` hold bars: `{1: 57, 2: 43, 3: 15, 4: 14, 5: 7}`
  baseline class mix: `{'bar_1_loser': 36, 'bar_1_winner': 21, 'bar_2_loser': 32, 'bar_2_winner': 11, 'bar_3_loser': 15, 'bar_4_loser': 10, 'bar_4_winner': 4, 'bar_5_loser': 7}`

### 22E `partial_take_profit`

- 2024 historical `PARTIAL_TAKE_PROFIT` hold bars: `{1: 21, 2: 29, 3: 15, 4: 27, 5: 18}`
  baseline class mix: `{'bar_1_loser': 2, 'bar_1_winner': 19, 'bar_2_loser': 3, 'bar_2_winner': 26, 'bar_3_loser': 1, 'bar_3_winner': 14, 'bar_4_winner': 27, 'bar_5_winner': 18}`
- 2025 validation Jan-Sep `PARTIAL_TAKE_PROFIT` hold bars: `{1: 57, 2: 50, 3: 31, 4: 34, 5: 19}`
  baseline class mix: `{'bar_1_loser': 13, 'bar_1_winner': 44, 'bar_2_loser': 11, 'bar_2_winner': 39, 'bar_3_loser': 1, 'bar_3_winner': 30, 'bar_4_loser': 2, 'bar_4_winner': 32, 'bar_5_winner': 19}`
- 2501 OOS `PARTIAL_TAKE_PROFIT` hold bars: `{1: 31, 2: 35, 3: 17, 4: 17, 5: 15}`
  baseline class mix: `{'bar_1_loser': 4, 'bar_1_winner': 27, 'bar_2_loser': 3, 'bar_2_winner': 32, 'bar_3_loser': 3, 'bar_3_winner': 14, 'bar_4_winner': 17, 'bar_5_loser': 1, 'bar_5_winner': 14}`

## Recommended Next Experiments

### 22F `partial_stop_loss_late_small`

- partial_stop_loss is the only variant that consistently helps baseline losers more than winners
- most partial stop loss events happen on bars 1-2, and bar 1 carries the heaviest winner contamination
- the 45-50 point adverse zone already separates losers from winners well enough; the bigger problem is firing too early and cutting too much size
- candidate logic: `{'trigger_points_anchor': 45, 'min_hold_bars': 2, 'close_fraction': 0.25}`
- success test: retain most deep-loser mitigation from 22D
- success test: reduce winner_clip_rate versus 22D
- success test: keep position_count identical to 22A

### 22G `trailing_stop_extreme_runner_only`

- trailing_stop fires overwhelmingly on baseline winners, especially from bars 2-5
- the 60-point trigger is not selective enough inside a hold5 system
- profit separation improves materially only in the 80-point zone, where loser hit rates drop much lower
- candidate logic: `{'activate_points_anchor': 80, 'min_hold_bars': 4, 'distance_points_anchor': 45}`
- success test: event_position_share falls well below 22C
- success test: big_winner_clip_rate falls materially below 22C
- success test: net delta versus 22A improves even if trade count stays similar

### 22H `partial_stop_loss_late_small_plus_extreme_runner_trail`

- 22D gives the best containment signal
- 22C as a broad trail is too destructive, but a very late trail may still help only on rare extended runners
- the combination only makes sense if partial stop loss is narrowed first
- candidate logic: `{'partial_stop_loss': {'trigger_points_anchor': 45, 'min_hold_bars': 2, 'close_fraction': 0.25}, 'trailing_stop': {'activate_points_anchor': 80, 'min_hold_bars': 4, 'distance_points_anchor': 45}}`
- success test: improve worst drawdown versus 22A without repeating 22D-size net profit drag
- success test: keep big winner clipping much lower than 22C and 22E
- success test: treat this as a containment challenger, not an automatic alpha upgrade

## Deprioritized

- `break_even`: event timing and class mix show too much winner-side interaction to justify another standalone rerun first
- `partial_take_profit`: profit-taking events repeatedly align with winner clipping and offer weak loser relief
