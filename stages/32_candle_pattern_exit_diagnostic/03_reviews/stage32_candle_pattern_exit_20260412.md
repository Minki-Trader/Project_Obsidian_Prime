# Stage 32 Candle Pattern Exit Diagnostic

- reviewed_on: `2026-04-12`
- run_anchor: `29N_25o_sxh2_0001`
- probe_hold: `+3 bars` relaxed diagnostic

## Headline

- `outside_adverse_bar` `total=45` `state_exit=15` `broker_sl=7` `policy_delta=72.11`
- `rejection_tail` `total=32` `state_exit=9` `broker_sl=12` `policy_delta=48.37`
- `wide_range_doji` `total=54` `state_exit=19` `broker_sl=14` `policy_delta=-11.11`

## Split Read

### hist_2024

- `outside_adverse_bar` `total=23` `state_exit=9` `broker_sl=4` `policy_delta=59.16`
- `rejection_tail` `total=17` `state_exit=6` `broker_sl=5` `policy_delta=65.22`
- `wide_range_doji` `total=21` `state_exit=11` `broker_sl=3` `policy_delta=-13.29`

### validation

- `outside_adverse_bar` `total=17` `state_exit=6` `broker_sl=1` `policy_delta=12.95`
- `rejection_tail` `total=8` `state_exit=3` `broker_sl=3` `policy_delta=-16.85`
- `wide_range_doji` `total=16` `state_exit=5` `broker_sl=6` `policy_delta=-24.24`

### test

- `outside_adverse_bar` `total=5` `state_exit=0` `broker_sl=2` `policy_delta=n/a`
- `rejection_tail` `total=7` `state_exit=0` `broker_sl=4` `policy_delta=n/a`
- `wide_range_doji` `total=17` `state_exit=3` `broker_sl=5` `policy_delta=26.43`

## Pattern Ladder

| pattern | total exits | state exits | broker SL | policy hold delta | probe +3 bars |
| --- | ---: | ---: | ---: | ---: | ---: |
| outside_adverse_bar | 45 | 15 | 7 | 72.11 | 102.26 |
| rejection_tail | 32 | 9 | 12 | 48.37 | 94.41 |
| wide_range_doji | 54 | 19 | 14 | -11.11 | 19.43 |

## Best Candidate

- `outside_adverse_bar` is the only pattern with a clean first-pass read: `total=45`, `state_exit=15`, `policy_hold_delta=72.11`
- `rejection_tail` is mixed because its validation read is weak even though its overall total stays positive
- `wide_range_doji` is not attractive because it fires often but its state-exit counterfactual is negative overall

## Top Outside-Bar Cases

### Missed Profit Candidates

- `hist_2024` `LONG` `exit=2024-11-05 16:45` `policy_delta=36.75` `probe3_delta=36.75` `range_atr=2.62`
- `hist_2024` `LONG` `exit=2024-08-15 16:45` `policy_delta=18.92` `probe3_delta=18.92` `range_atr=1.86`
- `hist_2024` `LONG` `exit=2024-12-02 16:45` `policy_delta=14.53` `probe3_delta=14.53` `range_atr=2.26`
- `validation` `SHORT` `exit=2025-03-13 19:45` `policy_delta=7.65` `probe3_delta=7.65` `range_atr=2.04`
- `validation` `LONG` `exit=2025-01-03 16:50` `policy_delta=6.56` `probe3_delta=19.24` `range_atr=3.27`

### Saved Loss Candidates

- `hist_2024` `LONG` `exit=2024-03-18 16:50` `policy_delta=-9.15` `probe3_delta=-9.15` `range_atr=2.44`
- `validation` `SHORT` `exit=2025-08-05 18:05` `policy_delta=-7.17` `probe3_delta=2.28` `range_atr=1.62`
- `hist_2024` `SHORT` `exit=2024-05-03 17:30` `policy_delta=-4.75` `probe3_delta=-4.75` `range_atr=1.88`
- `hist_2024` `SHORT` `exit=2024-05-28 17:05` `policy_delta=-2.98` `probe3_delta=-3.12` `range_atr=2.67`
- `validation` `SHORT` `exit=2025-04-23 17:05` `policy_delta=-2.00` `probe3_delta=10.98` `range_atr=3.00`

## Decision

- keep this as a diagnostic sidecar only
- if the candle-shape topic reopens, start with `outside_adverse_bar` only
- do not spend follow-up time on `wide_range_doji`
