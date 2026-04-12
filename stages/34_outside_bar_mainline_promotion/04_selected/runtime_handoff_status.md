# Stage 34 Runtime Handoff Status

- reviewed_on: `2026-04-12`
- stage: `34_outside_bar_mainline_promotion`
- selected_regular_incumbent: `34D_29s_outbarlong_0001`
- source_bundle: `02_runs/active/34D_29s_outbarlong_0001/experiment_bundle.json`
- handoff_runtime_id: `exp_34d_29s_outbarlong_v1_handoff`
- handoff_status: `bundle_runtime_verified`

## Scope

- verify that the selected `34D` bundle can be compiled into a fresh Common Files runtime package
- rerun the bundle through the shared bundle-driven tester path instead of relying only on the original stage-local attempts
- check whether the handoff path reproduces the existing `validation / test / hist_2024` read exactly

## Runtime Package

- compile helper: `foundation/pipelines/compile_mt5_bundle_runtime.py`
- tester helper: `foundation/pipelines/run_mt5_bundle_tester.py`
- compile summary:
  - `C:/Users/awdse/AppData/Roaming/MetaQuotes/Terminal/Common/Files/Project_Obsidian_Prime/runtime/exp_34d_29s_outbarlong_v1_handoff/mt5_runtime_compile_summary.json`
- runtime config:
  - `C:/Users/awdse/AppData/Roaming/MetaQuotes/Terminal/Common/Files/Project_Obsidian_Prime/runtime/exp_34d_29s_outbarlong_v1_handoff/mt5_runtime_config.txt`

## Reproduction Read

- `validation`: original `att_0001` matched handoff `att_0004` exactly
- `validation` headline: `return_pct=197.52` `pf=1.5831571737` `max_dd_pct=12.9091358916` `trade_count=404`
- `validation` coverage: `ready_row_count=11756` `ready_row_gap=0`
- `test`: original `att_0002` matched handoff `att_0005` exactly
- `test` headline: `return_pct=100.594` `pf=1.4883014252` `max_dd_pct=20.1777371099` `trade_count=285`
- `test` coverage: `ready_row_count=6755` `ready_row_gap=35`
- `hist_2024`: original `att_0003` matched handoff `att_0006` exactly
- `hist_2024` headline: `return_pct=46.374` `pf=1.2359927941` `max_dd_pct=14.8520964694` `trade_count=343`
- `hist_2024` coverage: `ready_row_count=13873`

## Decision

- treat the `34D` experiment bundle as a verified runtime handoff artifact
- no metric drift appeared between the original stage-local bundle attempts and the fresh handoff runtime package
- the known `test` split ready-row gap of `35` remains part of the reproduced baseline; this is not a new handoff regression

## Next Bias

- use `34D` as the operating bundle reference for the next regular-stage follow-up
- if the next regular stage reopens simplification, compare `34D` against `34B` first
- do not reopen the older `29N` carry lane as the default starting point
