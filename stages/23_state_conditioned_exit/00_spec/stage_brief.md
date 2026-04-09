# Stage 23 Brief

- stage: `23_state_conditioned_exit`
- reviewed_on: `2026-04-09`
- operating_seed: `22Q_05dp_base_risk2_dirsplit_postcash_0001`
- reference_shadow_challenger: `22R_05dp_psl45_qtr_h3_risk2_0001`
- roadmap_rank: `1`
- proposal_lineage: `Grok confidence-based dynamic exit + GPT state-conditioned exit`

## Purpose

Return the regular experiment line to `risk_pct` execution and test whether model-state exits can outperform the fixed `hold5` baseline more cleanly than Stage 22 point exits.

The stage is deliberately limited to state-aware exits that use the existing model output contract `[p_short, p_flat, p_long]`. It does not reopen mismatch relaxation, broad retraining, or specialist gating yet.

## Why This Stage Exists

- Stage 22 point exits failed to replace the incumbent even after follow-up refinement.
- Trigger-zone review showed that point exits mostly failed because they acted mechanically:
  - `partial_stop_loss` helped losers but fired too early and too heavily
  - `trailing_stop` clipped winners too often inside a `hold5` system
- Baseline `22Q` regular risk execution is now the correct operating scoreboard, so the next exit wave should stay on that lane.

## Wave 1 Hypotheses

1. `flat probability alone` may be too blunt, but it is the simplest diagnostic state exit and should be measured directly.
2. `directional margin decay` is more promising than point triggers because it directly reflects weakening edge after entry.
3. `combined flat + margin` may improve selectivity if the model only exits when both conviction and directional separation deteriorate.

## Wave 1 Parameter Anchors

The first wave uses the `22Q` test shadow/trade path as the calibration reference.

- `flat_exit_guard >= 0.35` is treated as a sparse diagnostic threshold rather than an aggressive production setting.
- `directional_margin <= 0.04` after `min_hold_bars=2` is the first meaningful decay threshold because it showed mild loser bias in the baseline postmortem while still firing often enough to matter.

## Planned Runs

- `23A`: regular baseline carry-forward from `22Q`
- `23B`: `flat_exit_guard(min_flat_probability=0.35, min_hold_bars=3)`
- `23C`: `state_exit_guard(max_direction_margin=0.04, min_hold_bars=2)`
- `23D`: `state_exit_guard(min_flat_probability=0.35, max_direction_margin=0.04, min_hold_bars=2)`

## Promotion Rule

- do not promote a challenger on OOS return alone
- a challenger must improve the regular OOS slice without obvious historical/validation drag
- close-reason mix and state-exit usage must stay interpretable; this stage is meant to explain behavior, not just search blindly
