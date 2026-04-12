# Stage 23-27 Wave 2 Cross-Split Synthesis

- reviewed_on: `2026-04-12`
- scope: `stage23_27_followup_search_plan_20260411`
- execution_mode: `regular_risk_execution`
- split_windows:
  - `validation`: `2025-01-01` through `2025-09-30`
  - `test`: `2025-10-01` through `2026-02-28`

## Why This Note Exists

- keep the full `23` through `27` wave-2 read in one place before the fusion stage opens
- separate the loud validation winners from the candidates that actually kept value on `test`
- record the common failure pattern so the next stage does not repeat it blindly

## Global Read

- all `53` wave-2 bundles completed on both `validation` and `test`
- no tester failures occurred after the MT5 runtime compile fix
- most wave-2 candidates improved weak short pockets and short-side expectancy
- most wave-2 candidates also suffered a large `validation -> test` headline drop
- the common failure pattern was:
  - `short expectancy` held up reasonably well on `test`
  - `long expectancy` collapsed toward a very small positive value on `test`
- read the whole wave as `short cleanup and containment logic that still needs long-side repair`

## Stage-Level Keepers

### Stage 23

- strongest `test` read: `23G_23c_margin004_h1_0001`
- core interpretation:
  - `state_exit_guard` with `min_hold_bars = 1`
  - `max_direction_margin = 0.04`
- why it matters:
  - it was the most stable `validation -> test` handoff in the full wave
  - `test_pf` improved over `validation_pf`

### Stage 24

- strongest `test` read: `24J_24a_17csg040_monpost_0001`
- core interpretation:
  - keep the specialist gate only inside `monday_or_postcash`
  - do not treat the confidence-band gate as a default carry-forward winner

### Stage 25

- strongest `validation` and `test` read: `25O_25d_ctx_exit_holdfusion_0001`
- core interpretation:
  - keep the `25O` soft contextual short cleanup as the fusion backbone
  - preserve:
    - Monday short suppressor
    - NY postcash short suppressor
    - late-session long penalty
    - Monday / postcash short hold cuts

### Stage 26

- strongest `test` headline: `26O_26a_gweakpocket_short_d3_0001`
- strongest `test` PF / DD balance: `26M_26a_gburst_mix_d3_0001`
- core interpretation:
  - `26O` is the better weak-pocket governance-context fusion
  - `26M` is the better burst-style governance overlay

### Stage 27

- strongest `test` headline: `27M_27a_vh092_postshort_0001`
- strongest `test` PF: `27L_27a_vh092_longonly_0001`
- strongest `test` DD containment: `27J_27a_holdonly_hv2_0001` and `27N_27a_vh092_short_h2_0001`
- core interpretation:
  - keep the `postcash high-vol short` overlay in the fusion candidate lane
  - keep the `high-vol hold-cap cut` arms as containment references rather than immediate headline arms

## Candidate Inputs For The Next Stage

- `25O_25d_ctx_exit_holdfusion_0001`: fusion backbone
- `23G_23c_margin004_h1_0001`: stable state-conditioned exit add-on
- `24J_24a_17csg040_monpost_0001`: contextual specialist gate add-on
- `26M_26a_gburst_mix_d3_0001`: governance burst overlay add-on
- `26O_26a_gweakpocket_short_d3_0001`: governance weak-pocket overlay add-on
- `27M_27a_vh092_postshort_0001`: postcash short volatility overlay add-on
- `27L_27a_vh092_longonly_0001`: long-only volatility overlay reference
- `27J_27a_holdonly_hv2_0001`: high-vol hold-cap containment reference
- `27N_27a_vh092_short_h2_0001`: high-vol short hold-cap containment reference

## Follow-Up Bias

- open the next stage as `fusion + long-side repair`, not as another broad local sweep
- keep `25O` as the carry-forward fusion reference inside that stage
- combine only a small number of validated add-ons at a time:
  - `23G`
  - `24J`
  - `26M`
  - `26O`
  - `27M`
- explicitly repair the weak `long` side in the next stage using:
  - stronger late-session long soft suppressor settings
  - Monday long hold caps
  - optional Monday long soft suppressor variants
