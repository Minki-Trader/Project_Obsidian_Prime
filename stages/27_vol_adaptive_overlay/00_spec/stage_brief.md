# Stage 27 Brief

- stage: `27_vol_adaptive_overlay`
- date_opened: `2026-04-09`
- inherited_regular_reference: `26A_25d_govref_0001`
- roadmap_anchor: `Grok volatility-adaptive overlay`

## Purpose

- extend the proven risk-overlay family with a market-state overlay instead of another telemetry taper
- keep the exact-alignment, closed-bar, `risk_pct` execution contract unchanged
- reuse the EA's existing `ATR14 / ATR50` closed-bar regime ratio rather than introducing a new volatility proxy

## Why This Wave Exists

- `26B` governance signal taper was too blunt and starved too much headline return
- `26C` external skip taper improved the read only by a very small amount
- the next small step should be a direct market-state overlay, not a more permissive governance threshold sweep

## Wave 1 Hypothesis

- a high-volatility risk taper may improve drawdown containment without hurting the book as much as governance signal taper
- a two-sided volatility bucket may help more if low-volatility conditions deserve a small participation boost
- the first wave should stay simple and interpretability-first:
  - `high volatility taper only`
  - `two-sided mild bucket`
  - `two-sided stronger bucket`

## Execution Rules

- use `26A` as the bundle seed for every run
- keep governance telemetry enabled in observe-only mode so execution diagnostics stay comparable
- keep governance blocking disabled
- run only the `regular_risk_execution` scoreboard in wave 1
- use the standard three windows:
  - `hist_2024`
  - `validation`
  - `test`

## Promotion Bias

- promote only if a volatility overlay improves the regular OOS read or clearly improves containment with limited non-OOS drag
- do not promote a bucket overlay that simply increases leverage in low-volatility pockets without improving the stability read
