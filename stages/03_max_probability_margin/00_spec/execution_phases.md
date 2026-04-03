# Stage 03 Execution Phases

## 03A Margin-Only Sweep

Purpose:

- keep `short_threshold = 1/3`
- keep `long_threshold = 1/3`
- sweep `min_margin`

Search split:

- `valid`

Diagnostic read:

- also record how the same margin candidates behave on the reserved final-model `test` split
- do not freeze from the test read inside 03A

## Review Rule

This stage should remain about `min_margin` only.

If a candidate depends on Stage 02 threshold asymmetry or a pure `p_long - p_short` filter, move that question to another stage instead of mixing it into Stage 03.
