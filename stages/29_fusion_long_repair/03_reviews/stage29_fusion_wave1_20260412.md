# Stage 29 Fusion Wave 1 Review

- reviewed_on: `2026-04-12`
- stage: `29_fusion_long_repair`
- live_regular_reference_before_wave: `27A_26a_volref_0001`
- plain_carry_reference_inside_wave: `29A_25o_refcarry_0001`
- regular_incumbent_after_wave: `29A_25o_refcarry_0001`
- regular_shadow_after_wave: `29B_25o_sx23g_0001`
- best_recent_window_arm: `29J_25o_sx23g_gweak_0001`
- decision: `replace_27A_with_29A_keep_state_exit_fusions_as_follow-up_lane`

## Executive Read

- the plain `25O` carry family finally received a full `hist_2024 / validation / test` read inside Stage 29 and beat the old live `27A` lane across all three windows
- the strongest follow-up idea from the broad predecessor sweep was still `23G`-style state exit; that family clearly improved `2025`-era `validation / test`, but it paid a meaningful `hist_2024` tax
- `29J` was the best pure `test` headline read, but the extra `26O` weak-pocket governance layer did not overcome the older-window giveback strongly enough to justify immediate live promotion
- the explicit long-repair recipe failed; it mostly reduced trade quality by starving longs rather than repairing them

## Selected Scoreboard

- prior live `27A`: `{'hist': {'return_pct': 25.958, 'pf': 1.1179, 'dd_pct': 21.0053}, 'validation': {'return_pct': 256.928, 'pf': 1.5912, 'dd_pct': 15.6765}, 'test': {'return_pct': 85.986, 'pf': 1.3921, 'dd_pct': 27.3179}}`
- new regular incumbent `29A`: `{'hist': {'return_pct': 36.994, 'pf': 1.1710, 'dd_pct': 20.7718}, 'validation': {'return_pct': 271.178, 'pf': 1.6057, 'dd_pct': 15.6747}, 'test': {'return_pct': 91.166, 'pf': 1.4083, 'dd_pct': 24.9847}}`
- simpler state-exit shadow `29B`: `{'hist': {'return_pct': 17.512, 'pf': 1.1088, 'dd_pct': 21.9507}, 'validation': {'return_pct': 159.024, 'pf': 1.5153, 'dd_pct': 11.9913}, 'test': {'return_pct': 99.71, 'pf': 1.5096, 'dd_pct': 18.3129}}`
- best recent-window arm `29J`: `{'hist': {'return_pct': 17.08, 'pf': 1.1063, 'dd_pct': 21.8603}, 'validation': {'return_pct': 158.286, 'pf': 1.5214, 'dd_pct': 11.6853}, 'test': {'return_pct': 101.248, 'pf': 1.5165, 'dd_pct': 18.4206}}`

## What Worked

- `29A` is the cleanest Stage 29 result because it converts the earlier `25O` wave-2 signal into a full three-window win over `27A` without adding new rule complexity
- `29B` proved that the `23G` state-exit backbone is the real Stage 29 alpha source: it cut the `validation -> test` headline gap from `180.012` in `29A` to `59.314`, and the PF gap from `0.197377` to `0.005648`
- `29J` was the best OOS read of the wave and improved the plain carry reference on every main `test` field that mattered:
  - `return_pct`: `101.248` vs `91.166`
  - `pf`: `1.5165` vs `1.4083`
  - `dd_pct`: `18.4206` vs `24.9847`
  - `long_expectancy`: `0.5836` vs `0.2701`
- execution stayed effectively unchanged across the compared arms, so the gains came from logic behavior rather than a looser runtime path:
  - `test skip_rate`: `0.7660606060606061`
  - `test external_mismatch_count`: `8976`

## What Failed

- the overlay-only add-ons `29D / 29E / 29F` behaved like near-noise around the plain `29A` carry reference; they did not materially change the `test` long-side collapse
- the specialist-gate fusion `29C` finished correctly after the missing aux-ONNX artifact was restored, but the final read was still too close to `29A` to justify the extra moving part
- the explicit long-repair lane `29G / 29H / 29K / 29L / 29M` did not deliver the hoped-for repair:
  - `29H` pushed `test long_expectancy` negative to `-0.2831`
  - `29K / 29L / 29M` lowered `test` drawdown, but only with a large `hist_2024` and `validation` haircut and no convincing long-quality gain
- the full `state_exit` family still carries a visible older-window tax:
  - `29B hist_2024 return_pct = 17.512`
  - `29J hist_2024 return_pct = 17.08`
  - both sit well below `29A hist_2024 return_pct = 36.994`

## Decision

- replace the old live regular reference `27A` with the plain `29A` carry line
- keep `29B` as the official regular shadow challenger because it preserves almost all of the `29J` recent-window gain with slightly less complexity and slightly better older-window balance
- keep `29J` as the best recent-window arm, but do not promote it over `29A` until the `hist_2024` penalty is reduced
- close the current explicit long-repair recipe; it did not repair longs in a robust way

## Follow-Up Bias

- if Stage 29 opens `wave2`, start from `29B` and `29J`, not from the failed explicit long-repair arms
- bias the next search toward lighter or context-conditional state-exit behavior so the `2025` improvement can be kept without throwing away so much `2024` carry
- treat long-side repair as a secondary micro-tuning problem attached to the `state_exit` backbone, not as its own blunt suppressor lane
