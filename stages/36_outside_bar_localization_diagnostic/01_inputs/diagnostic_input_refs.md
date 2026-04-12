# Stage 36 Diagnostic Inputs

- comparison bundles:
  - `stages/35_candle_sidecar_simplification_check/02_runs/active/35A_34d_refcarry_0001/experiment_bundle.json`
  - `stages/35_candle_sidecar_simplification_check/02_runs/active/35B_34b_simpleref_0001/experiment_bundle.json`
- split attempt summaries:
  - `stages/35_candle_sidecar_simplification_check/02_runs/active/35A_34d_refcarry_0001/mt5_attempts/att_0001/tester_attempt_summary.json`
  - `stages/35_candle_sidecar_simplification_check/02_runs/active/35A_34d_refcarry_0001/mt5_attempts/att_0002/tester_attempt_summary.json`
  - `stages/35_candle_sidecar_simplification_check/02_runs/active/35A_34d_refcarry_0001/mt5_attempts/att_0003/tester_attempt_summary.json`
  - `stages/35_candle_sidecar_simplification_check/02_runs/active/35B_34b_simpleref_0001/mt5_attempts/att_0001/tester_attempt_summary.json`
  - `stages/35_candle_sidecar_simplification_check/02_runs/active/35B_34b_simpleref_0001/mt5_attempts/att_0002/tester_attempt_summary.json`
  - `stages/35_candle_sidecar_simplification_check/02_runs/active/35B_34b_simpleref_0001/mt5_attempts/att_0003/tester_attempt_summary.json`

## Read Notes

- this stage does not rerun MT5 and does not rebuild bundles
- the outside-bar trigger itself is inherited from the already-verified Stage 33 / Stage 34 runtime path
- the goal here is narrower:
  - identify which recorded trade differences actually create the remaining `34D` edge
  - separate those direct effects from balance-driven `risk_pct` carry drift
