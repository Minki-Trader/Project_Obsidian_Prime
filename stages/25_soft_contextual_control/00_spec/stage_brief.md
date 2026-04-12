# Stage 25 Brief

- stage: `25_soft_contextual_control`
- updated_on: `2026-04-09`
- regular_seed: `24A_23a_base_gate_ref_0001`
- roadmap_anchor: `soft contextual thresholds and asymmetric hold control`

## Purpose

- retry the failed detector idea as a `soft` contextual overlay instead of a hard block
- split entry pressure by `session` and `direction` before widening into a larger overlay sweep
- test whether weak `short` pockets can be improved with small threshold/margin penalties plus a narrow postcash short hold cut

## Why This Stage Exists

- the Stage 24 inherited baseline kept the regular OOS headline, but context slicing showed two repeat weak pockets on the short book:
  - `Monday short (non-postcash)` was negative in `validation` and `test`
  - `NY postcash short (non-Monday)` was negative in `validation` and `test`
- the older overlay family (`10C` through `13C`) improved performance with soft risk shaping, while hard detector retries (`14A`, `15A`) failed to replace the reference
- this wave should therefore stay `soft`, `interpretable`, and `small`

## Wave 1 Hypothesis

- `short` entries in weak contexts may be too permissive even after Stage 22/23/24 carry-forward controls
- a contextual `threshold_add` plus `min_margin_add` may trim the weakest short rows without starving the whole book
- if postcash shorts are still weak after soft suppression, a narrower `NY postcash short hold cap` may contain the remaining tail

## Wave 1 Arms

- `25A`: inherited `24A` regular reference
- `25B`: `Monday short` soft suppressor
- `25C`: `NY postcash short` soft suppressor
- `25D`: combined `Monday + NY postcash short` soft suppressor plus `NY postcash short hold cap = 2`

## Evaluation Rule

- keep the inherited regular incumbent unless a challenger improves the regular `test` read without obvious `hist_2024` or `validation` damage
- read this wave through both headline metrics and contextual short diagnostics
- context diagnostics should focus on:
  - `Monday short net`
  - `NY postcash short net`
  - `test short_count`
  - whether the hold-cap asymmetry changes `TIME_EXIT_NY_POSTCASH_SHORT` behavior without obvious winner clipping elsewhere
