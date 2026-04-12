# Stage 31 Diagnostic Inputs

- operating reference run:
  - `stages/29_fusion_long_repair/02_runs/active/29N_25o_sxh2_0001/experiment_bundle.json`
- split attempt summaries:
  - `stages/29_fusion_long_repair/02_runs/active/29N_25o_sxh2_0001/mt5_attempts/att_0001/tester_attempt_summary.json`
  - `stages/29_fusion_long_repair/02_runs/active/29N_25o_sxh2_0001/mt5_attempts/att_0002/tester_attempt_summary.json`
  - `stages/29_fusion_long_repair/02_runs/active/29N_25o_sxh2_0001/mt5_attempts/att_0003/tester_attempt_summary.json`
- raw price source:
  - `data/raw/mt5_bars/m5/US100/<year>/US100_m5_<YYYY-MM>.parquet`

## Read Notes

- the analysis uses the existing MT5 trade ledgers from the `29N` bundle, not a new tester rerun
- the counterfactual is approximate:
  - execution remains tied to the recorded trade exit price plus raw-bar continuation
  - it is meant to judge whether impulse-driven `state_exit` is worth a future runtime experiment
