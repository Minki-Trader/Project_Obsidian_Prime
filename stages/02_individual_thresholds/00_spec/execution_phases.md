# Stage 02 Execution Phases

## 02A Threshold Sweep

Purpose:

- search `short_threshold`
- search `long_threshold`

Freeze:

- Stage 01 search-side model source
- `min_margin = 0`
- fixed `3`-bar time exit
- no overlap
- no flip
- zero cost assumption

Search split:

- `valid`

Exit condition:

- one threshold seed is selected for later confirmation or carry-forward

## Review Rule

This stage should remain strictly about threshold asymmetry and threshold tightness.
If a candidate depends on margin logic, move that question to Stage 03 instead of mixing it here.
