# Stage 22 Partial Stop-Loss Refinement Wave 2

- reviewed on: `2026-04-08`
- focus: `partial stop-loss refinement after 22F/22M follow-up and volume-step alias check`
- note: `US100 fixed 0.1 lot means partial close fractions collapse onto broker volume steps`

## Validation

| run | return_pct | PF | trade_count | max_dd_pct |
|---|---:|---:|---:|---:|
| `22A` | `122.570` | `1.5553` | `405` | `12.603` |
| `22D` | `82.834` | `1.3944` | `611` | `10.417` |
| `22F` | `108.676` | `1.4947` | `596` | `11.252` |
| `22M` | `115.468` | `1.5191` | `579` | `11.598` |
| `22O` | `119.106` | `1.5377` | `579` | `11.878` |
| `22P` | `112.074` | `1.5022` | `579` | `11.535` |

## Test

| run | return_pct | PF | trade_count | max_dd_pct | shared_delta_vs_22A | winner_clip | loser_mitigation | partial_events | partial_volume |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| `22A` | `68.574` | `1.4925` | `275` | `19.394` | `0.000` | `0.0000` | `0.0000` | `0` | `-` |
| `22D` | `53.346` | `1.3934` | `411` | `15.218` | `-76.140` | `0.5128` | `0.1052` | `136` | `{'0.05': 136}` |
| `22F` | `64.488` | `1.4650` | `403` | `18.009` | `-20.430` | `0.2001` | `0.0367` | `128` | `{'0.02': 128}` |
| `22M` | `64.644` | `1.4618` | `393` | `18.235` | `-19.650` | `0.1699` | `0.0308` | `118` | `{'0.02': 118}` |
| `22O` | `66.680` | `1.4779` | `393` | `18.806` | `-9.470` | `0.0846` | `0.0156` | `118` | `{'0.01': 118}` |
| `22P` | `62.788` | `1.4476` | `393` | `17.629` | `-28.930` | `0.2540` | `0.0464` | `118` | `{'0.03': 118}` |

## Test Event Timing

- alias pairs: `22F == 22L, 22M == 22N`
- `22F`: holds `{2: 87, 3: 17, 4: 17, 5: 7}`, class mix `{'loser': 99, 'winner': 29}`
- `22M`: holds `{3: 89, 4: 21, 5: 8}`, class mix `{'loser': 96, 'winner': 22}`
- `22O`: holds `{3: 89, 4: 21, 5: 8}`, class mix `{'loser': 96, 'winner': 22}`
- `22P`: holds `{3: 89, 4: 21, 5: 8}`, class mix `{'loser': 96, 'winner': 22}`

## Interpretation

- `22L` and `22N` were not real new information. Because `0.1 lot` is quantized by broker volume step, both `20%` and `25%` partial closes resolved to the same `0.02 lot` close volume as their paired runs.
- `22M` confirmed that delaying partial stop loss to `min_hold_bars=3` helps compared with `22F`: fewer events (`128 -> 118`) and lower winner contamination (`29 -> 22` winner-tagged events), with slightly better OOS return.
- `22O` was the cleanest alpha-preserving containment candidate. It kept the cleaner `h3` timing from `22M`, but reduced the actual close size to `0.01 lot`. That cut shared-position drag to `-9.470`, the best among partial-stop variants tested here, and lifted OOS return to `66.680`.
- `22P` showed the other side of the frontier. Raising the actual close size to `0.03 lot` improved containment more strongly than `22O`, but it also increased winner clipping and gave back more headline return.
- None of the refinement variants beat `22A`. The current read is still `keep incumbent`, but if a containment challenger is worth carrying forward, `22O` is the most interesting trade-off after accounting for real broker volume quantization.
