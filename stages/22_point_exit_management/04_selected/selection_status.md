# Stage 22 Selection Status

- reviewed_on: `2026-04-09`
- structural_scout_mode: `fixed_lot=0.1, point-exit behavior read only`
- regular_experiment_mode: `risk_pct=2.0 with direction-split ATR broker-native stops and monday/postcash overlay`
- closed_diagnostic_branch: `external_mismatch curiosity ablation reviewed; not promoted into regular experiment line`

## Current Read

- structural scout incumbent: `22A_05dp_base_hold5_0001`
- structural scout containment challenger: `22O_05dp_psl45_p10_h3_0001`
- regular incumbent: `22Q_05dp_base_risk2_dirsplit_postcash_0001`
- regular shadow challenger: `22R_05dp_psl45_qtr_h3_risk2_0001`
- keep_or_replace: `keep_incumbent`

## Promotion Gates

- Do not promote from the structural scout board alone.
- A regular challenger must improve the OOS slice without paying disproportionate historical and validation drag.
- Shared-position delta, winner clipping, and loser mitigation must all stay directionally healthy; raw OOS return alone is not enough.
- Closed diagnostic branches such as mismatch relaxation stay outside the regular promotion path unless a new contract hypothesis appears.

## Scoreboards

### Structural Scout

| run | val_return | val_dd | test_return | test_dd | shared_delta_vs_22A | winner_clip | loser_mitigation | read |
|---|---|---|---|---|---|---|---|---|
| `22A` | `122.570` | `12.603` | `68.574` | `19.394` | `0.000` | `0.0000` | `0.0000` | `scout incumbent` |
| `22O` | `119.106` | `11.878` | `66.680` | `18.806` | `-9.470` | `0.0846` | `0.0156` | `best scout containment challenger` |
| `22P` | `112.074` | `11.535` | `62.788` | `17.629` | `-28.930` | `0.2540` | `0.0464` | `more containment, more clipping` |

### Regular Risk Execution

| run | hist_return | hist_dd | val_return | val_dd | test_return | test_dd | shared_delta_vs_22Q | winner_clip | loser_mitigation | read |
|---|---|---|---|---|---|---|---|---|---|---|
| `22Q` | `26.002` | `25.433` | `193.808` | `20.824` | `71.068` | `27.423` | `0.000` | `0.0000` | `0.0000` | `regular incumbent` |
| `22R` | `25.488` | `25.342` | `183.788` | `20.440` | `71.514` | `27.125` | `2.230` | `0.0596` | `0.0252` | `shadow challenger` |
| `22S` | `21.516` | `25.392` | `191.362` | `20.693` | `65.412` | `27.734` | `-21.520` | `0.0273` | `0.0366` | `too gentle` |
| `22T` | `25.458` | `25.325` | `182.030` | `20.443` | `71.468` | `27.037` | `2.000` | `0.0746` | `0.0290` | `more drag than 22R` |

## Headline

- incumbent `22Q`: `hist_return=26.002`, `val_return=193.808`, `test_return=71.068`, `test_pf=1.3199`, `test_dd=27.423`
- challenger `22R`: `hist_return=25.488`, `val_return=183.788`, `test_return=71.514`, `test_pf=1.3252`, `test_dd=27.125`

## Risk

- incumbent `22Q`: `ulcer=13.066`, `worst_week=-117.39`, `consecutive_losses=9`, `min_free_margin=415.74`
- challenger `22R`: `ulcer=12.793`, `worst_week=-117.38`, `consecutive_losses=15`, `min_free_margin=416.07`

## Diagnostics

- incumbent `22Q`: `no_trade_rate=0.8675`, `long_short=139/163`, `avg_hold=4.0`, `risk_contexts={'BASE': 215, 'NY_POSTCASH': 60, 'MONDAY': 24, 'MONDAY|NY_POSTCASH': 3}`
- challenger `22R`: `no_trade_rate=0.8675`, `long_short=169/213`, `avg_hold=3.86`, `shared_delta=2.23`, `winner_clip=0.0596`, `loser_mitigation=0.0252`

## Execution

- incumbent `22Q`: `skip_rate=0.7661`, `external_mismatch_count=8976`, `fill_rate=n/a`, `contract_skip_count=22119`
- challenger `22R`: `skip_rate=0.7661`, `external_mismatch_count=8976`, `fill_rate=n/a`, `contract_skip_count=22119`
- regular line uses the intended risk stack; mismatch-relaxation runs remain outside the regular decision lane.

## Decision

- decision: `keep_incumbent`
- regular incumbent: `22Q_05dp_base_risk2_dirsplit_postcash_0001`
- regular shadow challenger: `22R_05dp_psl45_qtr_h3_risk2_0001`

## Follow-Up Bias

- keep `22Q` as the regular Stage 22 reference
- keep `22R` as the shadow containment challenger
- treat `22A` and `22O` as structural-scout context, not as the operating scoreboard
- do not advance mismatch-relaxation experiments into the regular line unless a new contract hypothesis appears

## Report Refs

- `03_reviews/stage22_ledger_postmortem_20260408.md`
- `03_reviews/stage22_trigger_zone_review_20260408.md`
- `03_reviews/stage22_followup_execution_review_20260408.md`
- `03_reviews/stage22_partial_sl_refine_wave2_20260408.md`
- `03_reviews/stage22_alignment_ablation_20260408.md`
- `03_reviews/stage22_risk_overlay_wave1_20260409.md`
