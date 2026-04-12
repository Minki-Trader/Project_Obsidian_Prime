# Stage 22 Follow-Up Execution Review

- reviewed on: `2026-04-08`
- base incumbent: `22A_05dp_base_hold5_0001`
- follow-up candidates: `22F`, `22G`, `22H`

## Historical Primitive Reproduction

Current `foundation/mt5/ObsidianPrime_Stage1_ShadowEA.mq5` was updated to restore Stage 22 point-exit execution using runtime-config exit rules.

OOS reproduction check against archived `att_0003` matched exactly after restoring the correct `US100 price-delta` semantics:

| run | archived return | rerun return | archived PF | rerun PF | archived trades | rerun trades | archived DD | rerun DD | close reasons |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| `22B` | `51.068` | `51.068` | `1.4228` | `1.4228` | `290` | `290` | `15.705` | `15.705` | `TIME_EXIT=221`, `BREAK_EVEN_STOP=69` |
| `22C` | `58.608` | `58.608` | `1.4183` | `1.4183` | `301` | `301` | `24.512` | `24.512` | `TIME_EXIT=198`, `TRAIL_STOP=103` |
| `22D` | `53.346` | `53.346` | `1.3934` | `1.3934` | `411` | `411` | `15.218` | `15.218` | `PARTIAL_STOP_LOSS=136`, `TIME_EXIT=275` |
| `22E` | `50.332` | `50.332` | `1.3774` | `1.3774` | `390` | `390` | `19.061` | `19.061` | `TIME_EXIT=275`, `PARTIAL_TAKE_PROFIT=115` |

This confirms the restored runtime matches the historical Stage 22 artifacts before any new candidate interpretation.

## New Follow-Up Runs

### Candidate specs

- `22F`: `partial_stop_loss(trigger=45, close_fraction=0.25, min_hold_bars=2)`
- `22G`: `trailing_stop(trigger=80, distance=45, min_hold_bars=4)`
- `22H`: `22F + 22G`

### Validation `2025-01-01 .. 2025-10-01`

| run | return_pct | PF | trade_count | max_dd_pct | close reasons |
|---|---:|---:|---:|---:|---|
| `22A` | `122.570` | `1.5553` | `405` | `12.603` | `TIME_EXIT=405` |
| `22C` | `94.626` | `1.4144` | `467` | `10.457` | `TRAIL_STOP=193`, `TIME_EXIT=274` |
| `22D` | `82.834` | `1.3944` | `611` | `10.417` | `PARTIAL_STOP_LOSS=206`, `TIME_EXIT=405` |
| `22F` | `108.676` | `1.4947` | `596` | `11.252` | `PARTIAL_STOP_LOSS=191`, `TIME_EXIT=405` |
| `22G` | `123.094` | `1.5474` | `427` | `12.250` | `TRAIL_STOP=108`, `TIME_EXIT=319` |
| `22H` | `115.630` | `1.5275` | `616` | `11.356` | `TRAIL_STOP=104`, `TIME_EXIT=322`, `PARTIAL_STOP_LOSS=190` |

### Test `2025-10-01 .. 2026-03-01`

| run | return_pct | PF | trade_count | max_dd_pct | close reasons |
|---|---:|---:|---:|---:|---|
| `22A` | `68.574` | `1.4925` | `275` | `19.394` | `TIME_EXIT=275` |
| `22C` | `58.608` | `1.4183` | `301` | `24.512` | `TIME_EXIT=198`, `TRAIL_STOP=103` |
| `22D` | `53.346` | `1.3934` | `411` | `15.218` | `PARTIAL_STOP_LOSS=136`, `TIME_EXIT=275` |
| `22F` | `64.488` | `1.4650` | `403` | `18.009` | `PARTIAL_STOP_LOSS=128`, `TIME_EXIT=275` |
| `22G` | `60.854` | `1.4452` | `283` | `22.273` | `TIME_EXIT=221`, `TRAIL_STOP=62` |
| `22H` | `54.436` | `1.3911` | `417` | `21.001` | `PARTIAL_STOP_LOSS=134`, `TIME_EXIT=222`, `TRAIL_STOP=61` |

## Interpretation

- `22F` validated the main partial-SL hypothesis. It materially improved over `22D` in both validation and test while preserving the same `275` OOS base positions and reducing partial events from `136` to `128`. It still did not beat `22A`.
- `22G` validated the main trailing hypothesis. It was much less aggressive than `22C` and cut trail events from `103` to `62` on test and from `193` to `108` on validation. It almost matched `22A` on validation, but still lagged on test and still increased OOS drawdown versus baseline.
- `22H` did not validate the combination hypothesis. The two rules interacted, but the stacked behavior did not beat `22F` or `22G`, and it remained below `22A`.

## Bottom Line

- `22A` remains the incumbent within the Stage 22 family.
- `22F` is the strongest follow-up if the goal is `less damaging partial stop loss`, not outright promotion.
- `22G` is a cleaner trailing candidate than `22C`, but still not enough to replace baseline.
- `22H` should not be advanced without a new interaction hypothesis.
