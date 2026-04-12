# Stage 29 Fusion Wave 2 Review

- reviewed_on: `2026-04-12`
- stage: `29_fusion_long_repair`
- inherited_wave1_incumbent: `29A_25o_refcarry_0001`
- inherited_wave1_shadow: `29B_25o_sx23g_0001`
- new_regular_incumbent: `29N_25o_sxh2_0001`
- new_regular_shadow: `29S_25o_sxh2_gweak_0001`
- best_recent_window_arm: `29W_25o_sxdirls_gweak_0001`
- decision: `replace_29A_with_29N_keep_h2_state_exit_as_balanced_backbone`

## Executive Read

- Wave 2 answered the main Stage 29 follow-up question clearly: the right way to keep the `state_exit` gain without paying so much `hist_2024` tax was not `short-only` and not a more aggressive `h1` layout, but a slower `h2` state-exit backbone.
- `29N` became the new balanced winner. It beat `29A` on `hist_2024` and `test` at the same time while also cutting drawdown materially.
- `29S` proved that the weak-pocket governance overlay can still help a little on top of the slower `h2` backbone, but the gain was too small to justify promoting the more complex version over `29N`.
- the aggressive `h1` follow-ups were still useful diagnostically:
  - `29O / 29T` showed that looser `h1` state exit can create a much stronger `2025` read with lower `test` DD
  - `29R / 29W` pushed that further and became the best pure `test` arms
  - but none of those aggressive layouts solved the older-window tax

## Main Scoreboard

- prior incumbent `29A`: `{'hist': {'return_pct': 36.994, 'pf': 1.1710, 'dd_pct': 20.7718}, 'validation': {'return_pct': 271.178, 'pf': 1.6057, 'dd_pct': 15.6747}, 'test': {'return_pct': 91.166, 'pf': 1.4083, 'dd_pct': 24.9847}}`
- new incumbent `29N`: `{'hist': {'return_pct': 39.368, 'pf': 1.2021, 'dd_pct': 14.8134}, 'validation': {'return_pct': 196.808, 'pf': 1.5717, 'dd_pct': 12.9472}, 'test': {'return_pct': 99.556, 'pf': 1.4828, 'dd_pct': 20.2164}}`
- governance shadow `29S`: `{'hist': {'return_pct': 39.10, 'pf': 1.2009, 'dd_pct': 14.7646}, 'validation': {'return_pct': 197.53, 'pf': 1.5810, 'dd_pct': 12.9087}, 'test': {'return_pct': 100.594, 'pf': 1.4883, 'dd_pct': 20.1777}}`
- best recent-window arm `29W`: `{'hist': {'return_pct': 12.718, 'pf': 1.0805, 'dd_pct': 22.2771}, 'validation': {'return_pct': 145.278, 'pf': 1.4911, 'dd_pct': 11.3529}, 'test': {'return_pct': 120.754, 'pf': 1.6626, 'dd_pct': 19.1610}}`

## Why `29N` Won

- it is the first Stage 29 `state_exit` fusion that actually clears both required checks at once:
  - better `hist_2024` than `29A`
  - better `test` than `29A`
- relative to `29A`, `29N` improved the full live-like read in the most important places:
  - `hist_2024 return_pct`: `39.368` vs `36.994`
  - `hist_2024 pf`: `1.2021` vs `1.1710`
  - `hist_2024 dd_pct`: `14.8134` vs `20.7718`
  - `test return_pct`: `99.556` vs `91.166`
  - `test pf`: `1.4828` vs `1.4083`
  - `test dd_pct`: `20.2164` vs `24.9847`
- the key behavioral fix is that the `h2` backbone removed the very ugly older-window long decay from `29B / 29J`:
  - `29B hist long_expectancy`: `-0.3721`
  - `29J hist long_expectancy`: `-0.3708`
  - `29N hist long_expectancy`: `0.1697`
- at the same time it kept the newer-window long improvement alive:
  - `29N test long_expectancy`: `0.6008`
  - `29A test long_expectancy`: `0.2701`

## What Wave 2 Taught Us

- `min_hold_bars` was the decisive lever.
- moving from the aggressive `h1` state-exit family back to `h2` restored older-window quality without giving back all of the `test` benefit.
- `short-only` state exit was a useful diagnostic but not a final answer:
  - `29Q / 29V` had the best `hist_2024` return in the whole wave
  - but their `test` read dropped back near the plain `29A` carry baseline
  - this is strong evidence that the `test` alpha is not a short-only story
- more aggressive `h1` designs remained attractive only as recent-window probes:
  - `29O / 29T` were the smoothest recent-window reads with the lowest `test` DD
  - `29R / 29W` were the best pure `test` headline reads
  - but all four paid too much `hist_2024` cost to replace `29N`

## Close Calls

- `29S` was close enough to matter:
  - slightly better `validation` and `test` than `29N`
  - effectively tied `hist_2024`
  - but the gain was too small to justify carrying the extra weak-pocket governance layer as default live complexity
- `29T` was the best lower-DD aggressive arm:
  - `test return_pct = 108.754`
  - `test pf = 1.5905`
  - `test dd_pct = 17.0237`
  - but `hist_2024 return_pct = 19.524`, which is still far below `29N`

## Decision

- promote `29N_25o_sxh2_0001` to the new regular operating reference
- keep `29S_25o_sxh2_gweak_0001` as the official regular shadow challenger
- keep `29W_25o_sxdirls_gweak_0001` as the best pure recent-window arm, not as the live lane
- close `29Q / 29V` as proof that short-only state exit preserves older carry but loses too much of the newer-window payoff

## Follow-Up Bias

- if Stage 29 opens another wave, start from `29N` and `29S`
- keep `h2` as the balanced state-exit backbone until a later wave proves that an aggressive `h1` design can recover its `hist_2024` tax
- treat `29T` and `29W` as diagnostic high-upside templates, not as immediate promotion candidates
