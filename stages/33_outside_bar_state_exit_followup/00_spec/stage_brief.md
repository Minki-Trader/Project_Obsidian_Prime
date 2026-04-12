# Stage 33 Brief

- stage: `33_outside_bar_state_exit_followup`
- status: `wave1_completed`
- roadmap_anchor: `targeted runtime follow-up on Stage 32 outside adverse bar diagnosis`
- inherited_regular_reference: `29N_25o_sxh2_0001`

## Purpose

- convert the Stage 32 `outside_adverse_bar` diagnosis into a small runtime sidecar
- test whether suppressing `STATE_EXIT_MARGIN` on that candle shape adds value in full MT5 runs
- keep the hypothesis narrow enough that we can tell whether candle morphology has real runtime value, not just diagnostic hindsight value

## Working Hypothesis

- the broad large-candle idea from Stage 31 stayed too diffuse
- the narrower Stage 32 read suggested that `outside_adverse_bar` is the first candle shape with enough specificity to justify a runtime pass
- the positive counterfactual was concentrated in `STATE_EXIT_MARGIN`, not in all exit types
- direction split matters:
  - long-side policy deltas were meaningfully positive
  - short-side policy deltas were near flat to mildly negative

## Wave 1 Run Shape

- rerun a direct `29N` carry clone under the updated EA to confirm no accidental regression
- test `outside adverse bar -> suppress margin state exit` with:
  - `direction = both / long / short`
  - `min_range_atr14 = 0.0 / 1.25`
- keep the trigger scope at `margin_only` for the first runtime pass

## Promotion Gates

- any promoted follow-up must keep the current `29N` test window intact or clearly better
- improvement must be visible in actual MT5 `validation / test / hist_2024` runs, not only in diagnostic counterfactuals
- if the sidecar only helps `hist_2024` or only inflates variance without a clean operating read, keep it closed
