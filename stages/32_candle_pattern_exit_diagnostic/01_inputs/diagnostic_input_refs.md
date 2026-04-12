# Stage 32 Diagnostic Inputs

- operating reference run:
  - `stages/29_fusion_long_repair/02_runs/active/29N_25o_sxh2_0001/experiment_bundle.json`
- split attempt summaries:
  - `stages/29_fusion_long_repair/02_runs/active/29N_25o_sxh2_0001/mt5_attempts/att_0001/tester_attempt_summary.json`
  - `stages/29_fusion_long_repair/02_runs/active/29N_25o_sxh2_0001/mt5_attempts/att_0002/tester_attempt_summary.json`
  - `stages/29_fusion_long_repair/02_runs/active/29N_25o_sxh2_0001/mt5_attempts/att_0003/tester_attempt_summary.json`
- raw price source:
  - `data/raw/mt5_bars/m5/US100/<year>/US100_m5_<YYYY-MM>.parquet`

## Read Notes

- this stage extends Stage 31 rather than replacing it
- the goal is not to prove a new signal edge yet
- the goal is to find out whether a narrower candle morphology is a better runtime sidecar candidate than broad giant-body suppression
