# Stage 01 Base Feature ML

## Objective

Build the first reusable baseline ML stage on top of the current FPMarkets v2 feature dataset.

This stage should answer one question first:

Can the shared 58-feature dataset produce a stable baseline model before any logic-specific specialization begins?

## In Scope

- define the first base-model label family
- freeze the first train/valid/test split
- build stage-local run folders for repeated experiments
- train and review the first baseline model
- promote only the best baseline artifacts into `04_selected/`
- run Stage 01 as a phased progression instead of one large mixed sweep

## Out Of Scope

- logic-specific rule engineering for `02_individual_thresholds`, `03_max_probability_margin`, or `04_probability_difference_filter`
- final threshold optimization
- broad folder restructuring
- replacing the current feature contract

## Fixed Constraints

- base modeling frame: `US100` M5
- shared common window: `2022-08-01` through `2026-02-28`
- practical modeling start: `2022-09-01`
- contract Google symbol: `GOOGL.xnas`
- output interpretation family: `[p_short, p_flat, p_long]`
- stage outputs stay inside this stage unless they become shared reusable artifacts

## Frozen For Stage 01

- output interpretation family stays fixed as `[p_short, p_flat, p_long]`
- base frame stays fixed as `US100` `M5`
- train, valid, test keep strict chronological order
- shared feature contract stays fixed at the current FPMarkets v2 feature set and column order

## Experimental For Stage 01

- forecast horizon
- neutral-band definition for `flat`
- fixed-band versus volatility-scaled band
- label cost adjustment policy
- first baseline classifier choice
- exact split boundaries, as long as chronological ordering is preserved

## Shared Inputs Already Available

- `data/processed/fpmarkets_v2/features/extended_window/feature_matrix.parquet`
- `data/processed/fpmarkets_v2/features/extended_window/feature_validity.parquet`
- `data/processed/fpmarkets_v2/features/extended_window/feature_build_summary.json`
- `data/processed/fpmarkets_v2/m5_intersection/extended_window/fpmarkets_v2_m5_intersection_2022-08-01_2026-02-28_summary.json`
- `foundation/reports/feature_dataset_build.md`
- `foundation/reports/m5_intersection_alignment.md`

## Open Decisions Before Run 0001

- which forecast horizon to use first
- how to define the neutral band for `flat`
- exact first split boundaries
- which baseline classifier to use first

## Search Discipline

- keep the fixed constraints above untouched during Stage 01
- treat label setup as a small bounded search, not an open-ended sweep
- compare candidate label setups on train and valid only
- do not use test results to redesign the label family
- promote one selected Stage 01 baseline before starting logic-specific stages

## Stage 01 Phases

### 01A Smoke

- freeze one initial horizon
- compare only `2-3` band candidates
- use one baseline model only
- objective: verify that the label family is viable at all

### 01B Model Compare

- freeze the winning label setup from `01A`
- compare multiple learning tools on the same dataset
- objective: separate label quality from model quality

### 01C Expanded Search

- keep only the top `1-2` model families from `01B`
- reopen bounded search on horizon and band candidates
- objective: search more seriously only after a viable baseline exists

### 01D Final Confirmation

- freeze the final selected setup from `01C`
- run the held-out test check once
- promote the chosen artifacts into `04_selected/`

## Initial Working Order

1. `01A`: freeze one horizon and `2-3` band candidates
2. freeze the first split manifest
3. generate the first stage-local modeling dataset
4. `01A`: run the smoke baseline and pick one label setup
5. `01B`: compare learning tools on the fixed label setup
6. `01C`: reopen bounded horizon and band search only if warranted
7. `01D`: confirm once on the held-out test and promote or archive
