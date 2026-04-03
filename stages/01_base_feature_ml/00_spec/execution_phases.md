# Stage 01 Execution Phases

## Why This Exists

Stage 01 should not mix label search, model search, and final evaluation in one sweep.

This stage uses phased passes so that:

- early runs stay light and easy to interpret
- model comparisons do not get confused with label changes
- heavier search happens only after a viable baseline exists

## Phase Layout

### 01A Smoke

Purpose:
- confirm that the base label family is viable

Freeze:
- one horizon
- one split definition
- one baseline model

Vary:
- `2-3` band candidates

Expected run naming:
- `01A_run_0001_*`
- `01A_run_0002_*`

Exit condition:
- one label setup is chosen for model comparison

### 01B Model Compare

Purpose:
- compare learning tools on the same exact label setup

Freeze:
- horizon
- band rule
- split definition

Vary:
- learning tool

Expected run naming:
- `01B_run_0001_*`
- `01B_run_0002_*`

Exit condition:
- top `1-2` model families selected

### 01C Expanded Search

Purpose:
- revisit horizon and band with stronger models only

Freeze:
- split definition
- candidate model family list

Vary:
- horizon
- band rule
- optionally cost treatment if it remains unresolved

Expected run naming:
- `01C_run_0001_*`
- `01C_run_0002_*`

Exit condition:
- one final candidate setup selected for confirmation

### 01D Final Confirmation

Purpose:
- perform the held-out confirmation pass and choose the Stage 01 handoff artifact

Freeze:
- label setup
- model family
- split definition

Vary:
- nothing material beyond deterministic rerun or packaging details

Expected run naming:
- `01D_run_0001_final_*`

Exit condition:
- chosen artifacts summarized in `04_selected/`

## Review Rule

At the end of each phase:

- archive rejected runs
- write a short conclusion in `03_reviews/`
- record the currently preferred candidate before moving to the next phase
