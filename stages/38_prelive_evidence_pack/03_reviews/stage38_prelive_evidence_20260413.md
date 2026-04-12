# Stage 38 Pre-Live Evidence Pack

- reviewed_on: `2026-04-13`
- stage: `38_prelive_evidence_pack`
- operating_reference: `34D_29s_outbarlong_0001`
- base_shadow: `34B_29s_refcarry_0001`

## Executive Read

- this stage keeps the follow-up package broader than a single narrow rerun, but it still centers the work on the one place where the current live edge is actually being earned
- Stage 36 direct events remain the core evidence: `count=7` `direct_net=34.060` `headline_net=36.320` `share=0.9378`
- the broad next package is now easier to define as three linked workstreams:
  - event evidence hardening
  - base-versus-incumbent value attribution
  - dedicated fresh runtime parity audit

## Event Evidence

- direct-event count: `7`
- atr bucket breakdown: `{'high': 6, 'mid': 1}`
- external exact-match breakdown at trigger bars: `{'VIX:True': 7, 'US10YR:True': 7, 'USDX:True': 7}`

### Critical Protection Events

- `hist_2024` `2024.11.05 16:45:00` `delta=15.680` `reason=DUAL_SIGNAL_TIE_OR_MARGIN_FAIL` `session=ny_cash` `atr_ratio=1.4339` `vix_change_1=-0.0027` `us10yr_change_1=0.0000`
- trigger bar `2024.11.05 16:40:00` `outside_prev=True` `direction=bear` `range=46.88` `body=14.50` `float_at_suppression=3.150`
- externals: `VIX=True` `US10YR=True` `USDX=True`

- `hist_2024` `2024.12.02 16:45:00` `delta=13.990` `reason=LONG_MARGIN_FAIL` `session=ny_cash` `atr_ratio=1.5934` `vix_change_1=0.0007` `us10yr_change_1=-0.0005`
- trigger bar `2024.12.02 16:40:00` `outside_prev=True` `direction=bear` `range=42.37` `body=6.12` `float_at_suppression=-0.530`
- externals: `VIX=True` `US10YR=True` `USDX=True`

- `hist_2024` `2024.08.15 16:45:00` `delta=7.540` `reason=DUAL_SIGNAL_TIE_OR_MARGIN_FAIL` `session=ny_cash` `atr_ratio=1.4418` `vix_change_1=0.0032` `us10yr_change_1=-0.0004`
- trigger bar `2024.08.15 16:40:00` `outside_prev=True` `direction=bear` `range=47.75` `body=11.88` `float_at_suppression=2.200`
- externals: `VIX=True` `US10YR=True` `USDX=True`

- `hist_2024` `2024.03.18 16:50:00` `delta=-5.170` `reason=LONG_MARGIN_FAIL` `session=ny_cash` `atr_ratio=1.3704` `vix_change_1=-0.0035` `us10yr_change_1=0.0000`
- trigger bar `2024.03.18 16:45:00` `outside_prev=True` `direction=bear` `range=36.95` `body=1.30` `float_at_suppression=0.810`
- externals: `VIX=True` `US10YR=True` `USDX=True`

- `validation` `2025.01.03 16:50:00` `delta=-4.800` `reason=DUAL_SIGNAL_TIE_OR_MARGIN_FAIL` `session=ny_cash` `atr_ratio=1.5402` `vix_change_1=0.0000` `us10yr_change_1=0.0001`
- trigger bar `2025.01.03 16:45:00` `outside_prev=True` `direction=bear` `range=88.50` `body=60.63` `float_at_suppression=10.050`
- externals: `VIX=True` `US10YR=True` `USDX=True`

- `validation` `2025.04.09 21:20:00` `delta=4.000` `reason=DUAL_SIGNAL_TIE_OR_MARGIN_FAIL` `session=ny_postcash` `atr_ratio=1.4766` `vix_change_1=-0.0215` `us10yr_change_1=-0.0009`
- trigger bar `2025.04.09 21:15:00` `outside_prev=True` `direction=bear` `range=164.25` `body=2.25` `float_at_suppression=0.160`
- externals: `VIX=True` `US10YR=True` `USDX=True`

- `hist_2024` `2024.09.05 21:15:00` `delta=2.820` `reason=LONG_MARGIN_FAIL` `session=ny_postcash` `atr_ratio=0.9716` `vix_change_1=0.0000` `us10yr_change_1=0.0000`
- trigger bar `2024.09.05 21:10:00` `outside_prev=True` `direction=bear` `range=24.25` `body=12.50` `float_at_suppression=-1.960`
- externals: `VIX=True` `US10YR=True` `USDX=True`

## Value Attribution

### Stage 34 Decomposition

- `validation` `34B-29N=0.722` `34C-29N=-0.030` `34D-29N=0.712` `34D-34B=-0.010`
- `test` `34B-29N=1.038` `34C-29N=0.000` `34D-29N=1.038` `34D-34B=0.000`
- `hist_2024` `34B-29N=-0.268` `34C-29N=6.448` `34D-29N=7.006` `34D-34B=7.274`

### Stage 35 / Stage 36 Split-Reset Attribution

- `validation` `return_delta=-0.010` `pf_delta=0.0022` `dd_delta=0.0004` `direct_events=2` `direct_net=-0.800`
- `test` `return_delta=0.000` `pf_delta=0.0000` `dd_delta=0.0000` `direct_events=0` `direct_net=0.000`
- `hist_2024` `return_delta=7.274` `pf_delta=0.0351` `dd_delta=0.1089` `direct_events=5` `direct_net=34.860`

### Stage 37 Continuous Bridge

- bridge delta `net=129.640` `return_pct=25.928` `pf=0.0015` `dd_pct=0.0319` `ulcer=0.0622`
- `2024` `net_delta=34.500` `trade_delta=0`
- `2025` `net_delta=43.650` `trade_delta=0`
- `2026_ytd` `net_delta=51.490` `trade_delta=0`

## Proxy Parity Read

- exact timestamp proxy: `count=100` `mean_max_abs=0.0454` `p90=0.0913` `max=0.1184`
- best-neighbor proxy: `count=100` `mean_max_abs=0.0341` `p90=0.0752` `max=0.1077`
- checksum matches: `exact=0` `best_neighbor=0`
- interpretation: processed feature_matrix is a useful proxy surface, but it is not yet a drop-in parity audit surface for the live MT5 runtime because neither exact checksum parity nor exact probability parity was recovered

## Follow-Up Bias

- keep the next work package broader than a single narrow rerun, but still centered on the direct-event evidence that actually explains the live edge
- build the human-facing base-versus-incumbent story around `34B -> 34D`, then use `34C` only as the decomposition side note
- do not jump from this stage straight into broad retraining or blanket simplification
- before live attachment, prioritize a fresh runtime snapshot parity audit over any new alpha-search branch
