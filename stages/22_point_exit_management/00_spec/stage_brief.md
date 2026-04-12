# Stage 22 Brief

- stage_id: `22_point_exit_management`
- updated_on: `2026-04-09`
- source_shell: `05DP_05ca_margin0675_hold5_0001`
- regular_reference: `22Q_05dp_base_risk2_dirsplit_postcash_0001`
- regular_shadow_challenger: `22R_05dp_psl45_qtr_h3_risk2_0001`

## Purpose

Stage 22 asks whether point-based exit management can improve the incumbent `hold5` family without damaging the strategy's original edge.

## Two Scoreboards

1. `structural_scout`
   - fixed `0.1` lot
   - used to understand point-exit shape, winner clipping, loser relief, and interaction risk
   - current scout incumbent: `22A`
   - current scout containment challenger: `22O`
2. `regular_risk_execution`
   - `risk_pct=2.0`
   - ATR broker-native stops with direction split and monday/postcash overlay
   - this is the only scoreboard allowed to promote the operating incumbent
   - current regular incumbent: `22Q`
   - current regular shadow challenger: `22R`

## Current Read

- simple single-rule point exits did not beat baseline on the original fixed-lot screen
- trigger-zone and ledger postmortems showed `partial SL` was the only family worth refining further
- mismatch relaxation was useful as a curiosity ablation, but it is closed outside the regular line
- once Stage 22 returned to regular risk execution, `22Q` stayed incumbent and `22R` became the best containment challenger

## Promotion Rule

- Do not promote from the structural scout board alone.
- Any challenger must clear the regular risk scoreboard with acceptable non-OOS drag.
- Shared-position delta, winner clipping, and loser mitigation should all support the promotion story.

## Read Order

1. `../03_reviews/review_index.md`
2. `../03_reviews/stage22_ledger_postmortem_20260408.md`
3. `../03_reviews/stage22_trigger_zone_review_20260408.md`
4. `../03_reviews/stage22_partial_sl_refine_wave2_20260408.md`
5. `../03_reviews/stage22_risk_overlay_wave1_20260409.md`
6. `../04_selected/selection_status.md`
