# Stage 23 Selection Status

- reviewed_on: `2026-04-09`
- stage: `23_state_conditioned_exit`
- roadmap_anchor: `Grok + GPT state-conditioned exit wave`
- inherited_regular_reference: `22Q_05dp_base_risk2_dirsplit_postcash_0001`

## Current Read

- regular incumbent: `23A_22q_base_stateexit_ref_0001`
- regular shadow challenger: `23C_22q_margin004_h2_risk2_0001`
- keep_or_replace: `keep_incumbent`

## Scoreboard

| run | hist_return | val_return | test_return | test_dd | test_pf | state_exit_count_test | read |
|---|---|---|---|---|---|---|---|
| `23A` | `26.002` | `193.808` | `71.068` | `27.423` | `1.3199` | `0` | `regular inherited baseline` |
| `23B` | `20.000` | `181.062` | `69.212` | `26.255` | `1.3160` | `15` | `flat-probability diagnostic challenger` |
| `23C` | `22.908` | `148.426` | `84.760` | `21.107` | `1.4116` | `87` | `best margin-decay state challenger` |
| `23D` | `22.908` | `148.426` | `84.760` | `21.107` | `1.4116` | `87` | `flat-plus-margin redundancy check` |

## Headline

- incumbent `23A`: `hist=26.002 / val=193.808 / test=71.068 / test_dd=27.423 / pf=1.3199`
- challenger `23C`: `hist=22.908 / val=148.426 / test=84.760 / test_dd=21.107 / pf=1.4116`

## Risk

- incumbent `23A`: `worst_week=-117.39 / ulcer=13.066 / consecutive_losses=9`
- challenger `23C`: `worst_week=-91.79 / ulcer=10.510 / consecutive_losses=10`

## Diagnostics

- incumbent `23A`: `avg_hold=4.00 / no_trade_rate=0.8675 / state_exit_count=0`
- challenger `23C`: `avg_hold=3.41 / no_trade_rate=0.8675 / state_exit_count=87 / state_exit_net=123.11 / state_exit_winner_share=0.5517`
- redundancy note `23D`: `flat+margin matched 23C exactly; flat condition added no incremental headline edge in wave 1`

## Execution

- incumbent `23A`: `skip_rate=0.7661 / external_mismatch_count=8976`
- challenger `23C`: `skip_rate=0.7661 / external_mismatch_count=8976`

## Decision

- decision: `keep_incumbent`
- regular incumbent: `23A_22q_base_stateexit_ref_0001`
- regular shadow challenger: `23C_22q_margin004_h2_risk2_0001`

## Follow-Up Bias

- keep `23A` as the carry-forward regular baseline until the state-exit line shows less non-OOS drag
- keep `23C` as the first serious state-conditioned exit challenger
- drop `23B` from the next wave
- treat `23D` as a redundancy result, not as a separate challenger

## Report Refs

- `03_reviews/stage23_state_exit_wave1_20260409.md`
