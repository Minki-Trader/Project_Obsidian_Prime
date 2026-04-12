# Stage 31 Impulse Candle Exit Diagnostic

- reviewed_on: `2026-04-12`
- run_anchor: `29N_25o_sxh2_0001`
- main_threshold: `1.50 x ATR14` adverse real-body impulse
- probe_hold: `+3 bars` relaxed diagnostic

## Headline

- adverse impulse exits at the main threshold: `71` total
- adverse impulse `STATE_EXIT` subset: `8 / 351` state exits, `2.3%`
- adverse impulse `BROKER_SL` subset: `53`
- policy-consistent `state_exit` counterfactual: `approx +33.90`
- relaxed `+3 bar` probe: `approx +0.09`
- read: the effect exists, but it is sparse and not yet strong enough to justify a broad runtime rewrite

## Split Read

### hist_2024

- state exits: `128`
- adverse impulse exits at `1.50 x ATR14`: `26` total, reason mix `{'BROKER_SL': 20, 'TIME_EXIT': 1, 'TIME_EXIT_NY_POSTCASH_SHORT': 2, 'STATE_EXIT_MARGIN': 3}`
- adverse impulse `STATE_EXIT` subset: `3` (`2.3%` of state exits)
- policy-consistent hold: `sum_delta_net=14.69`, `pos=2`, `neg=1`
- relaxed +3 bars: `sum_delta_net=10.29`, `pos=1`, `neg=2`
- worst extra adverse excursion under policy hold: `-10.06`

### validation

- state exits: `143`
- adverse impulse exits at `1.50 x ATR14`: `23` total, reason mix `{'STATE_EXIT_MARGIN': 4, 'BROKER_SL': 16, 'TIME_EXIT_NY_POSTCASH_SHORT': 1, 'TIME_EXIT': 2}`
- adverse impulse `STATE_EXIT` subset: `4` (`2.8%` of state exits)
- policy-consistent hold: `sum_delta_net=15.42`, `pos=3`, `neg=1`
- relaxed +3 bars: `sum_delta_net=-14.00`, `pos=2`, `neg=2`
- worst extra adverse excursion under policy hold: `-22.42`

### test

- state exits: `80`
- adverse impulse exits at `1.50 x ATR14`: `22` total, reason mix `{'BROKER_SL': 17, 'TIME_EXIT_NY_POSTCASH_SHORT': 1, 'TIME_EXIT': 3, 'STATE_EXIT_MARGIN': 1}`
- adverse impulse `STATE_EXIT` subset: `1` (`1.2%` of state exits)
- policy-consistent hold: `sum_delta_net=3.80`, `pos=1`, `neg=0`
- relaxed +3 bars: `sum_delta_net=3.80`, `pos=1`, `neg=0`
- worst extra adverse excursion under policy hold: `-6.72`

## Threshold Ladder

| threshold | adverse state exits | state-exit share | policy delta | probe +3 bars |
| --- | ---: | ---: | ---: | ---: |
| 1.25 x ATR14 | 16 | 4.6% | 49.71 | -9.25 |
| 1.50 x ATR14 | 8 | 2.3% | 33.90 | 0.09 |
| 2.00 x ATR14 | 4 | 1.1% | 29.49 | 4.74 |

## Top Cases

### Missed Profit Candidates

- `validation` `SHORT` `exit=2025-09-25 16:50` `body_atr=2.16` `policy_delta=20.36` `probe3_delta=-19.67` `extra_mae=-22.42`
- `hist_2024` `SHORT` `exit=2024-11-15 16:50` `body_atr=2.00` `policy_delta=14.76` `probe3_delta=20.48` `extra_mae=-0.98`
- `validation` `LONG` `exit=2025-01-03 16:50` `body_atr=2.24` `policy_delta=6.56` `probe3_delta=19.24` `extra_mae=-17.76`
- `hist_2024` `SHORT` `exit=2024-12-13 18:20` `body_atr=1.74` `policy_delta=6.48` `probe3_delta=-3.65` `extra_mae=-0.32`
- `test` `SHORT` `exit=2025-12-18 16:55` `body_atr=1.92` `policy_delta=3.80` `probe3_delta=3.80` `extra_mae=-6.72`

### Saved Loss Candidates

- `validation` `SHORT` `exit=2025-01-02 16:50` `body_atr=2.34` `policy_delta=-12.18` `probe3_delta=-15.31` `extra_mae=-14.79`
- `hist_2024` `SHORT` `exit=2024-06-11 17:00` `body_atr=1.94` `policy_delta=-6.55` `probe3_delta=-6.55` `extra_mae=-10.06`

## Decision

- keep this as a diagnostic sidecar only
- if the impulse topic reopens, compare a targeted `state-exit-only` suppression with a stop-side sensitivity read before attempting full candle neutralization
