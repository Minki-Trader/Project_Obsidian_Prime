# Stage 30 Brief

- stage: `30_macro_mismatch_root_cause`
- roadmap_anchor: `diagnostic sidecar for clustered macro mismatch pressure`
- status: `active diagnostic`
- promotion_lane: `closed`

## Purpose

- explain why `VIX` and `US10YR` timestamp mismatches cluster on the live regular line
- separate structural session-shape mismatches from true macro feed-health anomalies
- keep the old alignment-relaxation branch closed unless a new contract hypothesis earns follow-up

## Inputs

- latest regular operating reference: `29N_25o_sxh2_0001`
- runtime evidence: `shadow.csv` and `tester_attempt_summary.json` for `validation`, `test`, and `hist_2024`
- source evidence: `data/raw/mt5_bars/m5/<symbol>` exact timestamp coverage against the same base-bar timeline

## Non-Goals

- do not promote stale-bar handling as part of this stage
- do not reopen the broad Stage 22 alignment-relaxation lane
- do not create a new alpha incumbent / challenger pair here

## Expected Output

- one diagnostic review that classifies the mismatch families
- a short selected summary that records the current diagnostic read
- follow-up bias that says whether any later feed-health work is justified
