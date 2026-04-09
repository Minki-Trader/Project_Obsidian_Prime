# Stage Reporting Standard

This note turns the current experiment-review lessons into a reusable reporting rule set.

## Why This Exists

- Some stages need an early `structural_scout` read to learn rule behavior quickly.
- The same stage may still need a separate `regular_risk_execution` read before any operating decision is trustworthy.
- Selection notes are easier to re-enter when every stage uses the same sections and promotion gates.
- Governance telemetry becomes more useful when every comparison report exposes the same core fields.

## Dual Scoreboard Rule

For any stage that changes exit behavior, position sizing, or execution semantics, keep two scoreboards:

1. `structural_scout`
   - frozen scouting assumptions
   - usually fixed-lot or reduced execution complexity
   - goal: understand rule shape, clipping, containment, and interaction risk
2. `regular_risk_execution`
   - intended operating assumptions
   - live-like risk sizing and stop behavior
   - goal: decide the real incumbent / challenger relationship

Do not treat the `structural_scout` winner as the operating winner unless the `regular_risk_execution` scoreboard agrees.

## Selection Status Standard

Each active stage should keep `04_selected/selection_status.md` with these sections:

1. `Current Read`
2. `Promotion Gates`
3. `Scoreboards`
4. `Headline`
5. `Risk`
6. `Diagnostics`
7. `Execution`
8. `Decision`
9. `Follow-Up Bias`
10. `Report Refs`

The selection note should answer four questions quickly:

- What is the current incumbent?
- What is the current challenger?
- Under which scoreboard was that decision made?
- What evidence still has to improve before promotion is allowed?

## Review Index Standard

Each active later-stage review folder should keep `03_reviews/review_index.md` with:

- the review reading order
- the latest regular decision
- the latest structural-scout decision when it differs
- any closed diagnostic branches that should not be mistaken for the regular line

## Governance Summary Standard

Human-facing governance summaries should always expose a stable comparison core:

- `headline`: return, PF, DD, trades
- `risk`: ulcer / worst-week / other available stress metrics
- `diagnostics`: no-trade rate, long-short mix, key trade-shape diagnostics
- `execution`: external skip pressure, argmax concentration, entropy, overlay rate, top skip reasons, ready-row gap

If a value is unavailable, show `n/a` and say why. Do not silently emit `None`.

## Branch Re-entry Standard

When branch work is materially ahead of `main`, keep `docs/context/current_working_state.md` updated with:

- current branch name
- where the latest decisions live
- which diagnostics are closed and should not be reopened casually
- the current operating incumbent / challenger pair
