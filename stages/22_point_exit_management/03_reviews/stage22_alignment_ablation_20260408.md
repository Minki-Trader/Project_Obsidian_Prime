# Stage 22 Alignment Ablation Review

- reviewed on: `2026-04-08`
- purpose: `curiosity ablation` for external timestamp mismatch handling
- baseline contract remains `exact alignment + all-or-skip`; these runs are diagnostic only

## Setup

- `22I`: breadth-only `stale_closed_bar`, max stale `1`
- `22J`: macro-only `stale_closed_bar`, max stale `1`
- `22K`: all externals `stale_closed_bar`, max stale `1`
- guardrails: `future disallowed`, `date-cross carry disallowed`

## Validation

| run | return_pct | PF | trades | max_dd_pct | ready_rows | ext_mismatch_skips | fallback_rows | recovered_ready | recovered_signals |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `22A_exact` | `122.570` | `1.5553` | `405` | `12.603` | `11756` | `17350` | `0` | `0` | `0` |
| `22I_breadth_stale1` | `123.590` | `1.5558` | `412` | `12.259` | `11933` | `17173` | `177` | `177` | `13` |
| `22J_macro_stale1` | `122.396` | `1.5531` | `408` | `12.603` | `13221` | `15885` | `1465` | `1465` | `12` |
| `22K_all_stale1` | `123.416` | `1.5536` | `415` | `12.259` | `13405` | `15701` | `1649` | `1649` | `25` |

## Test

| run | return_pct | PF | trades | max_dd_pct | ready_rows | ext_mismatch_skips | fallback_rows | recovered_ready | recovered_signals |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `22A_exact` | `68.574` | `1.4925` | `275` | `19.394` | `6755` | `8976` | `0` | `0` | `0` |
| `22I_breadth_stale1` | `68.574` | `1.4925` | `275` | `19.394` | `6852` | `8879` | `97` | `97` | `2` |
| `22J_macro_stale1` | `71.138` | `1.5034` | `278` | `19.521` | `7600` | `8131` | `845` | `845` | `34` |
| `22K_all_stale1` | `71.138` | `1.5034` | `278` | `19.521` | `7701` | `8030` | `946` | `946` | `36` |

## KPI Notes

### Validation
- `22A_exact`: no-trade `0.8938`, max argmax share `0.5020`, avg entropy `0.9333`, extreme confidence `0.0000`, fallback symbols `{}`
- `22I_breadth_stale1`: no-trade `0.8942`, max argmax share `0.5041`, avg entropy `0.9331`, extreme confidence `0.0000`, fallback symbols `{'AAPL.xnas': 177, 'AMZN.xnas': 177, 'AMD.xnas': 177, 'GOOGL.xnas': 177, 'META.xnas': 177, 'MSFT.xnas': 177, 'NVDA.xnas': 177, 'TSLA.xnas': 177}`
- `22J_macro_stale1`: no-trade `0.9046`, max argmax share `0.5509`, avg entropy `0.9309`, extreme confidence `0.0000`, fallback symbols `{'US10YR': 470, 'VIX': 1074}`
- `22K_all_stale1`: no-trade `0.9050`, max argmax share `0.5524`, avg entropy `0.9307`, extreme confidence `0.0000`, fallback symbols `{'US10YR': 473, 'AAPL.xnas': 184, 'AMZN.xnas': 184, 'AMD.xnas': 184, 'GOOGL.xnas': 184, 'META.xnas': 184, 'MSFT.xnas': 184, 'NVDA.xnas': 184, 'TSLA.xnas': 184, 'VIX': 1078}`

### Test
- `22A_exact`: no-trade `0.8675`, max argmax share `0.5184`, avg entropy `0.9344`, extreme confidence `0.0000`, fallback symbols `{}`
- `22I_breadth_stale1`: no-trade `0.8691`, max argmax share `0.5213`, avg entropy `0.9342`, extreme confidence `0.0000`, fallback symbols `{'AAPL.xnas': 97, 'AMZN.xnas': 97, 'AMD.xnas': 97, 'GOOGL.xnas': 97, 'META.xnas': 97, 'MSFT.xnas': 97, 'NVDA.xnas': 97, 'TSLA.xnas': 97}`
- `22J_macro_stale1`: no-trade `0.8778`, max argmax share `0.5458`, avg entropy `0.9325`, extreme confidence `0.0000`, fallback symbols `{'VIX': 162, 'US10YR': 702, 'USDX': 1}`
- `22K_all_stale1`: no-trade `0.8791`, max argmax share `0.5482`, avg entropy `0.9323`, extreme confidence `0.0000`, fallback symbols `{'VIX': 164, 'US10YR': 704, 'AAPL.xnas': 101, 'AMZN.xnas': 101, 'AMD.xnas': 101, 'GOOGL.xnas': 101, 'META.xnas': 101, 'MSFT.xnas': 101, 'NVDA.xnas': 101, 'TSLA.xnas': 101, 'USDX': 1}`

## Interpretation

- `22I breadth-only stale1` recovered `177` validation rows and `97` test rows, but only produced `13` recovered signal rows on validation and `2` on test. Test PnL was unchanged versus baseline, so breadth mismatches do not look like a large hidden pool of missed trades.
- `22J macro-only stale1` was the only arm that moved OOS headline meaningfully: test return `68.574 -> 71.138`, trades `275 -> 278`, with DD `19.394 -> 19.521`. The gain is real but modest, and it came with slightly worse no-trade/argmax concentration KPIs.
- `22K all stale1` recovered the most rows, but its test headline matched `22J` exactly. That means the extra breadth relaxation on top of macro did not add incremental OOS alpha in this slice.
- Curiosity verdict: exact alignment is probably not hiding a huge missed-opportunity reservoir. If there is any upside to relaxing mismatch handling, it appears concentrated in macro externals and it is small enough that contract drift risk still matters.
