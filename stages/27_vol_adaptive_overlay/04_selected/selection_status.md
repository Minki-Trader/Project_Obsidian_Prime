# Stage 27 Selection Status

- reviewed_on: `2026-04-09`
- stage: `27_vol_adaptive_overlay`
- roadmap_anchor: `Grok volatility-adaptive overlay wave`
- inherited_regular_reference: `26A_25d_govref_0001`

## Current Read

- regular incumbent: `27A_26a_volref_0001`
- regular shadow challenger: `27D_26a_vl110h085_0001`
- keep_or_replace: `keep_incumbent`

## Promotion Gates

- gate_1: `improve test headline without obvious validation/2024 damage`
- gate_2: `or materially improve test containment with only limited headline sacrifice`
- gate_3: `prefer volatility overlays that improve the risk read without turning into a hidden leverage boost story`

## Scoreboards

- regular_risk_execution: `active for this wave`
- structural_scout: `not separated in wave 1; this is already a live-like risk overlay test`

## Headline

- baseline `27A`: `{'hist': 25.958, 'val': 256.928, 'test': 85.98599999999999, 'test_dd': 27.317947209370747, 'test_pf': 1.39208944742866}`
- best challenger `27D`: `{'hist': 23.433999999999997, 'val': 225.49, 'test': 68.084, 'test_dd': 25.04855213194586, 'test_pf': 1.3515210342619937}`

## Risk

- baseline risk: `{'worst_week': -130.89000000000001, 'ulcer': 12.46086877071514, 'consecutive_losses': 11}`
- challenger risk: `{'worst_week': -121.18999999999997, 'ulcer': 11.243547588861215, 'consecutive_losses': 11}`

## Diagnostics

- baseline diagnostics: `{'no_trade_rate': 0.8760917838638046, 'long_count': 140, 'short_count': 139}`
- challenger diagnostics: `{'no_trade_rate': 0.8760917838638046, 'long_count': 140, 'short_count': 139}`

## Execution

- baseline execution: `{'skip_rate': 0.7660606060606061, 'external_mismatch_count': 8976, 'mean_overlay_rate': 0.2669856422808379, 'latest_state': 'OK'}`
- challenger execution: `{'skip_rate': 0.7660606060606061, 'external_mismatch_count': 8976, 'mean_overlay_rate': 0.9590481086889061, 'latest_state': 'OK'}`

## Decision

- decision: `keep_incumbent`
- regular incumbent: `27A_26a_volref_0001`
- regular shadow challenger: `27D_26a_vl110h085_0001`

## Follow-Up Bias

- follow_up_1: `keep the volatility overlay line only if it improves the risk read without obvious non-OOS drag`
- follow_up_2: `if a high-vol taper helps but two-sided buckets overfit, keep the high-vol containment interpretation and avoid low-vol leverage chasing`

## Report Refs

- `03_reviews/stage27_vol_adaptive_wave1_20260409.md`
