# Stage 27 Volatility-Adaptive Overlay Wave 1

- reviewed_on: `2026-04-09`
- purpose: `reuse the EA's ATR14/ATR50 regime ratio as a non-blocking volatility-aware risk overlay on the 26A regular baseline`
- operating_seed: `26A_25d_govref_0001`
- roadmap_anchor: `Grok volatility-adaptive overlay wave`

## Scoreboard

| run | hist_return | val_return | test_return | test_dd | test_pf | overlay_rate | mean_ext_skip | mean_argmax | mean_entropy | read |
|---|---|---|---|---|---|---|---|---|---|---|
| `27A` | `25.958` | `256.928` | `85.986` | `27.318` | `1.3921` | `0.2670` | `0.3119` | `0.5879` | `0.9323` | `volatility observe-only inherited baseline` |
| `27B` | `20.488` | `200.678` | `65.922` | `23.237` | `1.3656` | `0.8348` | `0.3119` | `0.5879` | `0.9323` | `high-volatility taper only` |
| `27C` | `20.720` | `204.100` | `65.918` | `23.600` | `1.3601` | `0.9590` | `0.3119` | `0.5879` | `0.9323` | `two-sided mild volatility bucket overlay` |
| `27D` | `23.434` | `225.490` | `68.084` | `25.049` | `1.3515` | `0.9590` | `0.3119` | `0.5879` | `0.9323` | `two-sided stronger volatility bucket overlay` |

## Headline

- baseline `27A`: `{'hist': 25.958, 'val': 256.928, 'test': 85.98599999999999, 'test_dd': 27.317947209370747, 'test_pf': 1.39208944742866}`
- best challenger `27D`: `{'hist': 23.433999999999997, 'val': 225.49, 'test': 68.084, 'test_dd': 25.04855213194586, 'test_pf': 1.3515210342619937}`

## Risk

- baseline OOS risk read: `{'worst_week': -130.89000000000001, 'ulcer': 12.46086877071514, 'consecutive_losses': 11}`
- challenger OOS risk read: `{'worst_week': -121.18999999999997, 'ulcer': 11.243547588861215, 'consecutive_losses': 11}`

## Diagnostics

- baseline diagnostics: `{'no_trade_rate': 0.8760917838638046, 'long_count': 140, 'short_count': 139}`
- challenger diagnostics: `{'no_trade_rate': 0.8760917838638046, 'long_count': 140, 'short_count': 139}`
- this wave should be read as a `market-state overlay` experiment, so `overlay_rate` and containment matter alongside raw headline return.

## Execution

- baseline execution read: `{'skip_rate': 0.7660606060606061, 'external_mismatch_count': 8976, 'mean_overlay_rate': 0.2669856422808379, 'latest_state': 'OK'}`
- challenger execution read: `{'skip_rate': 0.7660606060606061, 'external_mismatch_count': 8976, 'mean_overlay_rate': 0.9590481086889061, 'latest_state': 'OK'}`

## Decision

- regular incumbent: `27A_26a_volref_0001`
- regular shadow challenger: `27D_26a_vl110h085_0001`
- decision: `keep_incumbent`
- why: `promote only if the volatility bucket improves the regular OOS read or clearly improves containment without obvious non-OOS damage`
