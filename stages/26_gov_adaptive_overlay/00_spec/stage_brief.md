# Stage 26 Brief

- stage: `26_gov_adaptive_overlay`
- date_opened: `2026-04-09`
- inherited_regular_reference: `25D_24a_monpost_t050_m030_psh2_0001`
- roadmap_anchor: `Grok + GPT governance-led adaptive overlays`

## Purpose

- move governance telemetry from `monitoring-only` into `non-blocking risk overlay` logic
- keep the exact-alignment, closed-bar, risk-based execution contract unchanged
- test whether governance drift signals can improve the regular OOS read without starving the book

## Wave 1 Hypothesis

- `25D` already cleaned up weak short contexts, so the next small step is not more threshold slicing
- the first governance overlay wave should only taper `risk_pct`, not block entries
- the first trigger family should stay small and interpretable:
  - signal drift via `argmax concentration / entropy decay`
  - external skip burst via rolling `external_skip_rate`
  - a milder combined arm

## Execution Rules

- use `25D` as the bundle seed for every run
- run only the `regular_risk_execution` scoreboard in wave 1
- enable governance telemetry for every arm
- keep governance blocking disabled
- use the standard three windows:
  - `hist_2024`
  - `validation`
  - `test`

## Promotion Bias

- promote only if a governance taper arm improves the regular OOS read or clearly improves containment with limited non-OOS drag
- do not treat governance alerting by itself as a win
- keep Stage 22 alignment relaxation closed as a diagnostic sidecar, not a promotion path
