# Stage 29 Fusion Long Repair

- stage: `29_fusion_long_repair`
- updated_on: `2026-04-12`
- current_wave: `wave3_h2_refinement_completed`
- roadmap_anchor: `post-wave fusion of the strongest stage23_27 follow-up ideas with explicit long-side repair`

## Purpose

- convert the broad `Stage 23` through `Stage 27` follow-up sweep into a smaller fusion stage
- use the strongest wave-2 carry candidate as the technical base:
  - `25O_25d_ctx_exit_holdfusion_0001`
- test whether a small number of proven add-ons can keep the short-side gains while reducing the long-side `test` collapse
- the stage opened with `27A_26a_volref_0001` as the live regular operating reference
- Wave 1 already replaced that live lane with `29A_25o_refcarry_0001`

## Current Stage Read

- Wave 1 promoted plain `29A_25o_refcarry_0001` over `27A`.
- Wave 2 then focused only on the `29B / 29J` state-exit family and asked whether the `2025` gain could be kept without the `hist_2024` tax.
- The balanced answer from that follow-up is now:
  - incumbent: `29N_25o_sxh2_0001`
  - shadow: `29S_25o_sxh2_gweak_0001`
  - best recent-window arm: `29W_25o_sxdirls_gweak_0001`
- Wave 3 tested nearby `h2` refinements and produced no further promotion.

## Predecessor Read

- read `docs/context/stage23_27_wave2_crosssplit_synthesis_20260412.md` before interpreting this stage
- `25O` was the best full-wave `test` headline read
- `23G` was the most stable `validation -> test` state-exit add-on
- `24J` was the best specialist-gate follow-up read
- `26M` and `26O` were the best governance overlay follow-up reads
- `27M` was the best volatility overlay follow-up headline read

## Wave 1 Scope

- keep the model artifacts fixed to the `25O` carry reference
- open the following fusion lanes:
  - `25O` carry reference inside Stage 29
  - `25O + 23G` state-exit fusion
  - `25O + 24J` specialist gate fusion
  - `25O + 26M` governance burst fusion
  - `25O + 26O` weak-pocket governance fusion
  - `25O + 27M` postcash high-vol short fusion
  - `25O + explicit long-side repair`
  - selected multi-add-on fusions built on top of `25O + 23G`
- keep the long-side repair bounded to:
  - stronger `late_session long` soft suppressor settings
  - optional `monday long` soft suppressor settings
  - `monday_long_hold_cap_bars`

## Evaluation Rules

- use the standard fixed chronology:
  - `hist_2024`: `2024-01-01` through `2024-12-31`
  - `validation`: `2025-01-01` through `2025-09-30`
  - `test`: `2025-10-01` through `2026-02-28`
- keep MT5 execution on:
  - `US100`
  - `M5`
  - `real_ticks`
  - `deposit = 500`
  - `leverage = 100`
- keep governance telemetry enabled in observe-or-adaptive mode as defined by each run
- judge promotion using `regular_risk_execution`, not validation-only headline noise

## Promotion Gates

- improve `test` headline over the plain `25O` carry reference
- or improve `test` PF / DD materially while keeping headline damage small
- specifically reduce the long-side `test` collapse that was visible across the predecessor wave
- do not promote a fusion read that only strengthens the short side while leaving the long side effectively dead
- after Wave 2, do not promote a new Stage 29 follow-up unless it also preserves the `hist_2024` balance recovered by `29N`
- after Wave 3, treat the local `h2` refinement lane as exhausted unless a non-local hypothesis appears
