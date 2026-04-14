# Stage 39 Latest-Window Feature-Path A/B Correction

- reviewed_on: `2026-04-14`
- stage: `39_window_extension_mt5_validation`
- focus: `latest_live_2026q2` feature-path replay correction
- affected bundles:
  - `39A_34d_bridge_ext_0001`
  - `39B_34b_bridge_ext_0001`

## Executive Read

- the earlier `34B` companion A/B read was not valid as written because `39B att_0002` saved `use_contract_aligned_feature_indicators=false` in `tester_attempt_summary.json` but the actual `tester_run.ini` set `InpUseContractAlignedFeatureIndicators=true`
- rerunning the genuine `34B` built-in lane as `39B att_0004` repaired that gap and changed the interpretation materially
- the corrected latest-window read is now exact across families:
  - `34B built-in` (`39B att_0004`) matches `34D built-in` (`39A att_0007`) exactly
  - `34B contract-aligned` (`39B att_0003`) matches `34D contract-aligned` (`39A att_0008`) exactly
- that means the latest-window KPI degradation after forcing contract-aligned feature indicators is a shared feature-surface effect, not a `34D`-only outside-bar sidecar effect

## Evidence Correction

- invalid artifact:
  - `39B att_0002`
  - summary field: `use_contract_aligned_feature_indicators=false`
  - actual tester input: `InpUseContractAlignedFeatureIndicators=true`
- direct confirmation:
  - `39B att_0002` shadow surface matched `39B att_0003` exactly on all `2216` ready rows
  - `39B att_0002` therefore behaves as a duplicate contract-aligned run, not as a genuine built-in replay
- corrective rerun:
  - `39B att_0004`
  - `InpUseContractAlignedFeatureIndicators=false`

## Corrected Scoreboard

- built-in lane:
  - `39A att_0007` `34D`: `net=-84.47` `return_pct=-16.894` `trade_count=99` `pf=0.6373` `max_dd_pct=17.6059`
  - `39B att_0004` `34B`: `net=-84.47` `return_pct=-16.894` `trade_count=99` `pf=0.6373` `max_dd_pct=17.6059`
- contract-aligned lane:
  - `39A att_0008` `34D`: `net=-100.75` `return_pct=-20.150` `trade_count=91` `pf=0.5511` `max_dd_pct=21.6542`
  - `39B att_0003` `34B`: `net=-100.75` `return_pct=-20.150` `trade_count=91` `pf=0.5511` `max_dd_pct=21.6542`
- shared contract-minus-built-in delta:
  - `net=-16.28`
  - `return_pct=-3.256`
  - `trade_count=-8`
  - `profit_factor=-0.0862`
  - `max_dd_pct=+4.0484`
  - `ulcer_index=+3.8790`
  - `long_signal_count=-28`
  - `short_signal_count=-1`
  - `no_trade_count=+29`

## Exact Match Checks

- built-in family parity:
  - shadow ready-row checksum diffs between `39B att_0004` and `39A att_0007`: `0 / 2216`
  - shadow decision diffs: `0`
  - shadow trade-action diffs: `0`
  - trade-ledger match by `entry_bar_time_server + direction`: `99 both`, `0 left_only`, `0 right_only`, `0 outcome diffs`
- contract-aligned family parity:
  - shadow ready-row checksum diffs between `39B att_0003` and `39A att_0008`: `0 / 2216`
  - shadow decision diffs: `0`
  - shadow trade-action diffs: `0`
  - trade-ledger match by `entry_bar_time_server + direction`: `91 both`, `0 left_only`, `0 right_only`, `0 outcome diffs`

## Interpretation

- the latest-window feature-path switch does not separate `34D` from `34B`
- on this `2026-03-01 .. 2026-04-13` slice, the `34D` outside-bar sidecar is effectively inactive at the realized path level
- the meaningful open question is no longer `why does 34D collapse to 34B only after the patch`
- the meaningful open question is now `why does the contract-aligned feature surface weaken both 34B and 34D equally on the latest window while still closing the targeted Stage 40 parity gap`

## Decision Bias

- retire the earlier `34D-specific latest-window degradation` read
- treat `39B att_0002` as a mislabeled artifact, not as valid A/B evidence
- use `39B att_0004` and `39A att_0007` as the genuine built-in lane
- use `39B att_0003` and `39A att_0008` as the genuine contract-aligned lane
- keep the next runtime-debug step focused on shared feature-surface attribution, not on a `34D`-only sidecar explanation
