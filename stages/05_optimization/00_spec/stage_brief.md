# Stage 05 Optimization

## Objective

Use MT5-connected optimization to find the strongest next-step rule family without forcing a combined Stage 02/03/04 stack.

This stage should answer one question first:

Which single rule family is strongest and most stable on the current Stage 01 baseline after runtime parity is confirmed?

## Current Exploration Override

- user-directed breadth-first exploration is open for this stage
- model-family swaps, logic mixes, and 2-mix/3-mix custom rule stacks are now in scope as explicit experiments
- keep the EA-facing output fixed as `[p_short, p_flat, p_long]`
- keep holdout promotion standards unchanged even during broad exploration

## In Scope

- keep the current Stage 01 model and 58-feature contract fixed for first-pass logic work
- keep MT5 runtime execution as the truth layer
- compare single-family logic bundles first:
  - Stage 03 `max_probability_margin`
  - Stage 04 `probability_difference_filter`
  - Stage 02 thresholds only as a control reference
- probe local robustness neighborhoods around the current leader
- decide whether a later synthesis step is justified
- run explicit breadth-first challengers such as model-family swaps and custom threshold/margin/diff mixes when the user wants wider exploration

## Out Of Scope

- forcing a Stage 02 + Stage 03 + Stage 04 combined rule stack because it was the original end-state
- reopening the feature contract before a logic winner exists
- optionalizing the current required external/session inputs
- broad EA behavior changes unrelated to the current single-family logic search
- promoting a broad-exploration candidate without the same holdout gate used for the narrower passes

## Fixed Constraints

- base model output stays `[p_short, p_flat, p_long]`
- current Stage 01 final model lineage stays fixed for the first Stage 05 logic pass
- current FPMarkets v2 58-feature contract stays fixed
- `US100` `M5`, real-tick tester, fixed `0.1` lot, one concurrent position max
- exact closed-bar alignment for external inputs stays fixed
- validation remains `2025-01-01` through `2025-09-30`
- test remains `2025-10-01` through `2026-02-28`

## Current Read

- Stage 03 MT5 validation leader: `03E_mt5_validation_baseline_0001`, `min_margin=0.07`, return_pct=`67.664`, profit_factor=`1.2655`, max_dd_pct=`12.2017`
- Stage 04 MT5 validation runner-up: `04C_mt5_validation_baseline_0001`, `min_probability_diff=0.0825`, return_pct=`60.648`, profit_factor=`1.2830`, max_dd_pct=`12.6687`
- Stage 02 remains useful as a threshold-only control, not as the default synthesis base
- the runtime coverage mismatch bug is fixed; the remaining low ready rate is a current contract property, not the active blocker

## Working Order

1. keep feature/runtime sanity checks green on the current bundle lineage
2. run local robustness probes around the current Stage 03 leader
3. run local robustness probes around the current Stage 04 leader
4. compare the surviving single-family winners on held-out test
5. only then decide whether to promote one single-family stack directly or open a justified synthesis pass

## Promotion Gate

Do not open a combined-rule experiment unless at least one of these is true:

- the best single-family candidate plateaus and diagnostics show a clear complementary gap
- Stage 03 and Stage 04 both remain stable enough that a hybrid is worth an explicit test
- the user explicitly wants a synthesis pass despite the added ambiguity
