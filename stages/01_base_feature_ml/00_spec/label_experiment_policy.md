# Stage 01 Label Experiment Policy

## Intent

Stage 01 is allowed to search for a workable base label setup, but only inside a controlled box.

The goal is to identify a stable baseline label family for the shared feature set without drifting away from the fixed project contract.

## Fixed And Not To Be Tuned Here

- output interpretation family: `[p_short, p_flat, p_long]`
- base modeling frame: `US100` on `M5`
- shared FPMarkets v2 feature contract
- chronological split order: train before valid before test

## Allowed To Be Tested Here

- forecast horizon
- neutral-band size
- neutral-band construction method
- label-side cost adjustment rule
- first baseline classifier family
- exact date boundaries for train, valid, and test, while preserving chronology

## Search Rules

- keep the candidate set intentionally small
- choose using train and valid only
- touch test only after a candidate has been selected on valid
- do not let test performance trigger a new label redesign loop
- prefer stable monthly behavior over one-off headline metrics

## Phase Rules

### 01A Smoke

- freeze one horizon first
- test only `2-3` band candidates
- keep the model fixed to one simple baseline
- do not compare many model families here

### 01B Model Compare

- freeze the selected label setup from `01A`
- compare learning tools on the exact same label and split
- do not reopen horizon or band here

### 01C Expanded Search

- use only the strongest `01B` model families
- reopen a bounded horizon and band search
- keep the search explicit and small enough to review cleanly

### 01D Final Confirmation

- lock the chosen label and model setup
- run the test check once
- do not use test outcomes to restart the search loop unless the user explicitly decides to do so

## Candidate Selection Criteria

Use a candidate only if it is acceptable on all of the following:

- class distribution is not pathological
- validation performance is not obviously unstable across months
- trade density is not unrealistically low
- the setup still matches the intended runtime interpretation path

## Practical Next Step

Before `run_0001`, write down a compact candidate grid for:

- horizon
- flat-band rule
- cost treatment
- first chronological split
