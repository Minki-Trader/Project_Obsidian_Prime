# Stage 38 Visual Panels

- reviewed_on: `2026-04-13`
- stage: `38_prelive_evidence_pack`
- purpose: `copy_ready_panels_for_live_packet_or_external_model_briefing`

## Panel 1. Critical Protection Events

1. Headline concentration.
- `events=7` `direct_net=34.060` `headline_net=36.320` `share=0.9378`
2. Split concentration.
- `hist_2024` `count=5` `net_delta=34.860`
- `validation` `count=2` `net_delta=-0.800`
- `test` `count=0` `net_delta=0.000`
3. Session concentration.
- `ny_cash` `count=5` `net_delta=27.240`
- `ny_postcash` `count=2` `net_delta=6.820`
4. Trigger reasons.
- `DUAL_SIGNAL_TIE_OR_MARGIN_FAIL` `count=4`
- `LONG_MARGIN_FAIL` `count=3`
5. Ranked critical bars.
- `1` `hist_2024` `2024.11.05 16:45:00` `delta=15.680` `reason=DUAL_SIGNAL_TIE_OR_MARGIN_FAIL` `session=ny_cash` `atr_ratio=1.4339` `range=46.88` `body=14.50` `float=3.150`
- trigger `outside_prev=True` `direction=bear` `VIX=True` `US10YR=True` `USDX=True`
- `2` `hist_2024` `2024.12.02 16:45:00` `delta=13.990` `reason=LONG_MARGIN_FAIL` `session=ny_cash` `atr_ratio=1.5934` `range=42.37` `body=6.12` `float=-0.530`
- trigger `outside_prev=True` `direction=bear` `VIX=True` `US10YR=True` `USDX=True`
- `3` `hist_2024` `2024.08.15 16:45:00` `delta=7.540` `reason=DUAL_SIGNAL_TIE_OR_MARGIN_FAIL` `session=ny_cash` `atr_ratio=1.4418` `range=47.75` `body=11.88` `float=2.200`
- trigger `outside_prev=True` `direction=bear` `VIX=True` `US10YR=True` `USDX=True`
- `4` `hist_2024` `2024.03.18 16:50:00` `delta=-5.170` `reason=LONG_MARGIN_FAIL` `session=ny_cash` `atr_ratio=1.3704` `range=36.95` `body=1.30` `float=0.810`
- trigger `outside_prev=True` `direction=bear` `VIX=True` `US10YR=True` `USDX=True`
- `5` `validation` `2025.01.03 16:50:00` `delta=-4.800` `reason=DUAL_SIGNAL_TIE_OR_MARGIN_FAIL` `session=ny_cash` `atr_ratio=1.5402` `range=88.50` `body=60.63` `float=10.050`
- trigger `outside_prev=True` `direction=bear` `VIX=True` `US10YR=True` `USDX=True`
- `6` `validation` `2025.04.09 21:20:00` `delta=4.000` `reason=DUAL_SIGNAL_TIE_OR_MARGIN_FAIL` `session=ny_postcash` `atr_ratio=1.4766` `range=164.25` `body=2.25` `float=0.160`
- trigger `outside_prev=True` `direction=bear` `VIX=True` `US10YR=True` `USDX=True`
- `7` `hist_2024` `2024.09.05 21:15:00` `delta=2.820` `reason=LONG_MARGIN_FAIL` `session=ny_postcash` `atr_ratio=0.9716` `range=24.25` `body=12.50` `float=-1.960`
- trigger `outside_prev=True` `direction=bear` `VIX=True` `US10YR=True` `USDX=True`

## Panel 2. 34B vs 34D Delta Explanation

1. Stage 34 decomposition.
- `validation` `34B-29N=0.722` `34C-29N=-0.030` `34D-29N=0.712` `34D-34B=-0.010`
- `test` `34B-29N=1.038` `34C-29N=0.000` `34D-29N=1.038` `34D-34B=0.000`
- `hist_2024` `34B-29N=-0.268` `34C-29N=6.448` `34D-29N=7.006` `34D-34B=7.274`
2. Stage 35 and Stage 36 split-reset attribution.
- `validation` `return_delta=-0.010` `pf_delta=0.0022` `dd_delta=0.0004` `direct_events=2` `direct_net=-0.800`
- `test` `return_delta=0.000` `pf_delta=0.0000` `dd_delta=0.0000` `direct_events=0` `direct_net=0.000`
- `hist_2024` `return_delta=7.274` `pf_delta=0.0351` `dd_delta=0.1089` `direct_events=5` `direct_net=34.860`
3. Stage 37 continuous bridge.
- window `2024-01-01 .. 2026-02-28 inclusive` `net=129.640` `return_pct=25.928` `pf=0.0015` `dd_pct=0.0319` `ulcer=0.0622`
- `2024` `net_delta=34.500` `trade_delta=0`
- `2025` `net_delta=43.650` `trade_delta=0`
- `2026_ytd` `net_delta=51.490` `trade_delta=0`
4. Stage 39 extended bridge.
- window `2022-08-01 .. 2026-04-12 inclusive` `net=107.930` `return_pct=21.586` `pf=0.0015` `dd_pct=0.0319` `ulcer=0.0601`
- `2024` `net_delta=34.500` `trade_delta=0`
- `2025` `net_delta=43.650` `trade_delta=0`
- `2026_ytd` `net_delta=29.780` `trade_delta=0`
5. Operating message.
- 34B explains the governance-only carry in the current windows.
- 34C explains the older-window rescue driven by the long outside-bar pocket.
- 34D stays ahead because it keeps both pieces without widening trade count.
