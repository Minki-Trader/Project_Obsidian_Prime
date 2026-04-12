# Stage 29 Selection Status

- reviewed_on: `2026-04-12`
- stage: `29_fusion_long_repair`
- roadmap_anchor: `fusion of stage23_27 wave-2 keepers plus explicit long-side repair`
- inherited_regular_reference: `29A_25o_refcarry_0001`
- inherited_fusion_reference: `25O_25d_ctx_exit_holdfusion_0001`

## Current Read

- regular incumbent: `29N_25o_sxh2_0001`
- regular shadow challenger: `29S_25o_sxh2_gweak_0001`
- best_recent_window_arm: `29W_25o_sxdirls_gweak_0001`
- keep_or_replace: `replace_29A_with_29N_keep_h2_state_exit_as_balanced_backbone`

## Promotion Gates

- gate_1: `beat the prior wave incumbent 29A on test headline or on test PF / DD trade-off`
- gate_2: `preserve or improve the recovered older-window balance while keeping the newer-window gain`
- gate_3: `do not re-promote an aggressive h1 state-exit arm unless it clears the hist_2024 tax as well as the test read`

## Scoreboards

- regular_risk_execution: `active for this wave`
- structural_scout: `not separated in wave2; this is already a live-like fused rule-stack test`

## Headline

- prior wave incumbent `29A`: `{'hist': 36.994, 'val': 271.178, 'test': 91.166, 'test_dd': 24.984702157660898, 'test_pf': 1.40830713281201}`
- new incumbent `29N`: `{'hist': 39.367999999999995, 'val': 196.808, 'test': 99.556, 'test_dd': 20.21644600658507, 'test_pf': 1.4827659780816604}`
- shadow `29S`: `{'hist': 39.099999999999994, 'val': 197.53, 'test': 100.59399999999998, 'test_dd': 20.177737109900313, 'test_pf': 1.4883014251873714}`
- best recent-window arm `29W`: `{'hist': 12.718000000000002, 'val': 145.278, 'test': 120.754, 'test_dd': 19.161024974206033, 'test_pf': 1.6626097453906936}`

## Risk

- prior wave risk `29A`: `{'hist_worst_week': -39.75, 'hist_ulcer': 9.357801416136732, 'test_worst_week': -122.96999999999997, 'test_ulcer': 11.363896714783825, 'test_consecutive_losses': 7}`
- new incumbent risk `29N`: `{'hist_worst_week': -42.940000000000005, 'hist_ulcer': 6.261507952387837, 'test_worst_week': -101.01, 'test_ulcer': 9.73976361403237, 'test_consecutive_losses': 7}`
- shadow risk `29S`: `{'hist_worst_week': -42.940000000000005, 'hist_ulcer': 6.221682349456928, 'test_worst_week': -101.60000000000001, 'test_ulcer': 9.678680352663603, 'test_consecutive_losses': 7}`
- recent-window arm risk `29W`: `{'hist_worst_week': -38.05, 'hist_ulcer': 12.147594907059633, 'test_worst_week': -104.92999999999999, 'test_ulcer': 8.816137999644235, 'test_consecutive_losses': 5}`

## Diagnostics

- prior wave diagnostics `29A`: `{'hist_long_exp': 0.43972027972027966, 'test_long_exp': 0.2700714285714285, 'test_short_exp': 2.9858571428571428, 'test_long_count': 140, 'test_short_count': 140}`
- new incumbent diagnostics `29N`: `{'hist_long_exp': 0.16972413793103444, 'test_long_exp': 0.6007801418439715, 'test_short_exp': 2.8685416666666668, 'test_long_count': 141, 'test_short_count': 144}`
- shadow diagnostics `29S`: `{'hist_long_exp': 0.16613793103448268, 'test_long_exp': 0.5934042553191489, 'test_short_exp': 2.9118055555555555, 'test_long_count': 141, 'test_short_count': 144}`
- recent-window arm diagnostics `29W`: `{'hist_long_exp': -0.2918543046357616, 'test_long_exp': 1.247945205479452, 'test_short_exp': 2.9275694444444444, 'test_long_count': 146, 'test_short_count': 144}`

## Execution

- hist execution note: `29N / 29S / 29W all use the same execution path as the rest of Stage 29 with skip_rate around 0.80366 and no execution relaxation story`
- test execution note: `all compared Wave 2 arms kept the same live-like runtime path with skip_rate 0.7660606060606061 and external_mismatch_count 8976`

## Decision

- decision: `keep_29N_and_29S_no_wave3_promotion`
- regular incumbent: `29N_25o_sxh2_0001`
- regular shadow challenger: `29S_25o_sxh2_gweak_0001`
- best recent-window arm: `29W_25o_sxdirls_gweak_0001`
- best wave3 close call: `29AC_25o_sxh2_lock1_gweak_0001`

## Follow-Up Bias

- keep `29N` as the live regular lane unless a later follow-up also preserves the recovered `hist_2024` balance
- treat `29S` as the main shadow because it is the only close balanced alternative
- treat `29W` and `29T` as aggressive recent-window templates, not as immediate promotion candidates
- close `29Q / 29V` as proof that short-only state exit is not enough for the full Stage 29 objective
- close the local `h2` refinement lane for now; Wave 3 did not find a better balanced replacement

## Report Refs

- `03_reviews/stage29_fusion_wave1_20260412.md`
- `03_reviews/stage29_fusion_wave2_20260412.md`
- `03_reviews/stage29_fusion_wave3_20260412.md`
