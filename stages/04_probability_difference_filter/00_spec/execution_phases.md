# Stage 04 Execution Phases

## 04A Difference-Only Sweep

Purpose:

- keep `short_threshold = 1/3`
- keep `long_threshold = 1/3`
- keep `min_margin = 0`
- sweep `min_probability_diff`

Search split:

- `valid`

Diagnostic read:

- also record how the same difference candidates behave on the reserved final-model `test` split
- do not freeze from the test read inside 04A

## Review Rule

This stage should remain about the directional probability difference only.

If a candidate depends on Stage 02 threshold asymmetry or Stage 03 max-probability margin, move that question to a later synthesis stage instead of mixing it into Stage 04.
