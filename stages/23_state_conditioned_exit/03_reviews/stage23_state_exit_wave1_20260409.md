# Stage 23 State Exit Wave 1

- reviewed_on: `2026-04-09`
- purpose: `test model-state exits on the regular 22Q risk-execution lane`
- operating_seed: `22Q_05dp_base_risk2_dirsplit_postcash_0001`
- roadmap_anchor: `Grok + GPT state-conditioned exit wave`

## Scoreboard

| run | hist_return | hist_dd | val_return | val_dd | test_return | test_dd | test_pf | state_exit_count_test | state_exit_net_test | read |
|---|---|---|---|---|---|---|---|---|---|---|
| `23A` | `26.002` | `25.433` | `193.808` | `20.824` | `71.068` | `27.423` | `1.3199` | `0` | `0.000` | `regular inherited baseline` |
| `23B` | `20.000` | `28.479` | `181.062` | `20.858` | `69.212` | `26.255` | `1.3160` | `15` | `-8.640` | `flat-probability diagnostic challenger` |
| `23C` | `22.908` | `19.083` | `148.426` | `16.860` | `84.760` | `21.107` | `1.4116` | `87` | `123.110` | `best margin-decay state challenger` |
| `23D` | `22.908` | `19.083` | `148.426` | `16.860` | `84.760` | `21.107` | `1.4116` | `87` | `123.110` | `flat-plus-margin redundancy check` |

## Headline

- baseline `23A`: `hist=26.002 / val=193.808 / test=71.068 / test_dd=27.423 / pf=1.3199`
- flat-only `23B`: `hist=20.000 / val=181.062 / test=69.212 / test_dd=26.255 / pf=1.3160`
- margin `23C`: `hist=22.908 / val=148.426 / test=84.760 / test_dd=21.107 / pf=1.4116`
- combo `23D`: `headline matched 23C exactly on all three windows`

## Risk

- `23C` materially improved the OOS risk read versus baseline: `test_dd 27.423 -> 21.107, worst_week -117.39 -> -91.79`
- the same arm paid substantial non-OOS drag: `hist_return 26.002 -> 22.908, val_return 193.808 -> 148.426`
- `23B` reduced DD slightly but did not improve return enough to justify the trade-off.

## Diagnostics

- `23B` fired only `15` flat exits on test, with winner_share `0.400` and net `-8.640`. This is too weak to carry forward.
- `23C` fired `87` state exits on test, with winner_share `0.552`, avg_hold `2.483`, and net `123.110`. The state-exit bucket itself is profitable.
- `23D` proved the flat condition added no incremental behavior on top of margin decay in this wave. It split the close reasons, but the final headline and risk numbers matched `23C` exactly.
- test close reasons show the new lane is specifically a margin-decay story, not a generic flat-probability win: `{'STATE_EXIT_MARGIN': 87}`.

## Execution

- execution quality stayed unchanged across the wave: `skip_rate=0.7661 and external_mismatch_count=8976 on the test slice for every run`
- that means the performance differences came from exit behavior, not from readiness or alignment drift.

## Decision

- regular incumbent: `23A_22q_base_stateexit_ref_0001`
- regular shadow challenger: `23C_22q_margin004_h2_risk2_0001`
- decision: `keep_incumbent`
- why: `23C is the first state-conditioned exit arm that improved the OOS slice materially, but its validation and 2024 drag are too large for immediate promotion. 23D is redundant and 23B is too weak.`
