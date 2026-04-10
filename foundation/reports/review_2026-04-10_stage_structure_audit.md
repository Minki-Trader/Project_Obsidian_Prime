# Workspace Quick Review (2026-04-10)

## Scope
- Reviewed high-level repository structure and stage layout against `AGENTS.md` rules.
- Confirmed presence of contract/source-of-truth documents and monthly weights placeholder file.

## Checks
- Root directories are clean and high-signal only: `docs/`, `foundation/`, `stages/` (+ `.git/`).
- Required contract docs are present under `docs/contracts/`.
- `foundation/config/top3_monthly_weights_fpmarkets_v2.csv` exists as expected placeholder.

## Findings
- Stage folders inspected: **21**.
- Stages missing at least one default directory: **21**.
- Most stages are missing `02_runs/active` and `02_runs/archived` (empty scaffolding not created yet).
- Special case: `stages/05_optimization` is also missing `01_inputs`.

### Missing default stage directories
| Stage | Missing directories |
|---|---|
| `01_base_feature_ml` | `02_runs/active, 02_runs/archived` |
| `02_individual_thresholds` | `02_runs/active, 02_runs/archived` |
| `03_max_probability_margin` | `02_runs/active, 02_runs/archived` |
| `04_probability_difference_filter` | `02_runs/active, 02_runs/archived` |
| `05_optimization` | `01_inputs, 02_runs/active, 02_runs/archived` |
| `06_segmented_risk_validation` | `02_runs/active, 02_runs/archived` |
| `07_motif_transplant` | `02_runs/active, 02_runs/archived` |
| `08_strict_wfo_shortlist` | `02_runs/active, 02_runs/archived` |
| `09_05et_local_probe` | `02_runs/active, 02_runs/archived` |
| `10_09c_overlay_gate` | `02_runs/active, 02_runs/archived` |
| `11_09c_overlay_local_probe` | `02_runs/active, 02_runs/archived` |
| `12_09c_overlay_fine_probe` | `02_runs/active, 02_runs/archived` |
| `13_09c_overlay_micro_probe` | `02_runs/active, 02_runs/archived` |
| `14_13d_short_regime_detector` | `02_runs/active, 02_runs/archived` |
| `15_13d_server_hour_short_detector` | `02_runs/active, 02_runs/archived` |
| `16_09c_feature_core_fork` | `02_runs/active, 02_runs/archived` |
| `17_09c_directional_core_fork` | `02_runs/active, 02_runs/archived` |
| `18_directional_core_overlay_matrix` | `02_runs/active, 02_runs/archived` |
| `19_18e_recent_regime_emphasis` | `02_runs/active, 02_runs/archived` |
| `20_18e_specialist_mixture` | `02_runs/active, 02_runs/archived` |
| `21_retrain_cadence_wfo` | `02_runs/active, 02_runs/archived` |

## Recommendation (minimal-change)
1. Add only empty scaffold folders that are currently missing (no data movement).
2. Start with active stages first; archive scaffolds can remain empty.
3. Keep stage-specific run artifacts under `stages/<nn_name>/02_runs/<run_id>/` as per policy.

## Notes
- This is a structure/process audit only; no model, feature, or contract behavior was changed.
