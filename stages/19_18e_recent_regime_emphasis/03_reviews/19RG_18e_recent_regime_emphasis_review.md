# Stage 19 18E Recent Regime Emphasis Review

- windows: `2401, 2407, 2501`
- source operating reference: `18E = 17E + PH20`
- target: `2407 / holdout_b`
- ranking basis: `positive_test_windows -> positive_holdout_b_windows -> avg_test_return -> min_holdout_b -> avg_test_delta_vs_18E -> avg_test_pf`

## Candidate Ranking

- [1] `19A` `18E_reference`: avg_test=`32.863`, avg_test_delta_vs_18E=`0.000`, target_holdout_b=`-3.282`, target_holdout_b_delta_vs_18E=`0.000`, min_holdout_b=`-3.282`, positive_test_windows=`3/3`, positive_holdout_b_windows=`2/3`
  - rationale: `Exact 18E learning recipe plus the PH20 operating overlay for sanity-check parity.`
  - `2401`: validation=`20.938`, test=`32.412`, PF=`1.2205`, holdout_b=`24.702`, holdout_b_PF=`1.6512`, test_delta_vs_18E=`0.000`, holdout_b_delta_vs_18E=`0.000`
  - `2407`: validation=`61.388`, test=`27.700`, PF=`1.4127`, holdout_b=`-3.282`, holdout_b_PF=`0.7972`, test_delta_vs_18E=`0.000`, holdout_b_delta_vs_18E=`0.000`
  - `2501`: validation=`-5.520`, test=`38.478`, PF=`1.5343`, holdout_b=`0.662`, holdout_b_PF=`1.0342`, test_delta_vs_18E=`0.000`, holdout_b_delta_vs_18E=`0.000`

- [2] `19G` `linear_ramp_x2p0`: avg_test=`32.136`, avg_test_delta_vs_18E=`-0.727`, target_holdout_b=`-4.608`, target_holdout_b_delta_vs_18E=`-1.326`, min_holdout_b=`-4.608`, positive_test_windows=`3/3`, positive_holdout_b_windows=`2/3`
  - rationale: `Linearly increase weight toward the end of each train window to create a smoother recency prior than hard recent buckets.`
  - `2401`: validation=`10.740`, test=`22.420`, PF=`1.1397`, holdout_b=`24.690`, holdout_b_PF=`1.5579`, test_delta_vs_18E=`-9.992`, holdout_b_delta_vs_18E=`-0.012`
  - `2407`: validation=`57.986`, test=`17.244`, PF=`1.3030`, holdout_b=`-4.608`, holdout_b_PF=`0.7218`, test_delta_vs_18E=`-10.456`, holdout_b_delta_vs_18E=`-1.326`
  - `2501`: validation=`-13.452`, test=`56.744`, PF=`1.7980`, holdout_b=`7.600`, holdout_b_PF=`1.4994`, test_delta_vs_18E=`18.266`, holdout_b_delta_vs_18E=`6.938`

- [3] `19C` `recent_6m_x2p0`: avg_test=`28.797`, avg_test_delta_vs_18E=`-4.067`, target_holdout_b=`-10.144`, target_holdout_b_delta_vs_18E=`-6.862`, min_holdout_b=`-10.144`, positive_test_windows=`3/3`, positive_holdout_b_windows=`2/3`
  - rationale: `Stronger six-month recency emphasis to test whether later-train structure improves strict-WFO robustness.`
  - `2401`: validation=`10.926`, test=`27.996`, PF=`1.1625`, holdout_b=`32.444`, holdout_b_PF=`1.7804`, test_delta_vs_18E=`-4.416`, holdout_b_delta_vs_18E=`7.742`
  - `2407`: validation=`21.516`, test=`6.334`, PF=`1.1112`, holdout_b=`-10.144`, holdout_b_PF=`0.3893`, test_delta_vs_18E=`-21.366`, holdout_b_delta_vs_18E=`-6.862`
  - `2501`: validation=`-16.302`, test=`52.060`, PF=`2.0738`, holdout_b=`11.236`, holdout_b_PF=`2.0695`, test_delta_vs_18E=`13.582`, holdout_b_delta_vs_18E=`10.574`

- [4] `19F` `recent_6m_flat_guard`: avg_test=`25.181`, avg_test_delta_vs_18E=`-7.683`, target_holdout_b=`-10.444`, target_holdout_b_delta_vs_18E=`-7.162`, min_holdout_b=`-10.444`, positive_test_windows=`3/3`, positive_holdout_b_windows=`2/3`
  - rationale: `Recency emphasis with an extra flat boost to test whether later-regime abstention is the missing model-side edge.`
  - `2401`: validation=`6.128`, test=`30.664`, PF=`1.2024`, holdout_b=`32.860`, holdout_b_PF=`1.9256`, test_delta_vs_18E=`-1.748`, holdout_b_delta_vs_18E=`8.158`
  - `2407`: validation=`30.886`, test=`13.414`, PF=`1.2843`, holdout_b=`-10.444`, holdout_b_PF=`0.2130`, test_delta_vs_18E=`-14.286`, holdout_b_delta_vs_18E=`-7.162`
  - `2501`: validation=`-13.194`, test=`31.464`, PF=`1.7735`, holdout_b=`2.640`, holdout_b_PF=`1.2567`, test_delta_vs_18E=`-7.014`, holdout_b_delta_vs_18E=`1.978`

- [5] `19B` `recent_6m_x1p5`: avg_test=`23.797`, avg_test_delta_vs_18E=`-9.066`, target_holdout_b=`-8.872`, target_holdout_b_delta_vs_18E=`-5.590`, min_holdout_b=`-8.872`, positive_test_windows=`3/3`, positive_holdout_b_windows=`2/3`
  - rationale: `Boost the most recent six months of train data modestly to prefer later-regime structure without hard targeting a date.`
  - `2401`: validation=`26.686`, test=`20.590`, PF=`1.1274`, holdout_b=`28.178`, holdout_b_PF=`1.6802`, test_delta_vs_18E=`-11.822`, holdout_b_delta_vs_18E=`3.476`
  - `2407`: validation=`28.212`, test=`14.104`, PF=`1.2392`, holdout_b=`-8.872`, holdout_b_PF=`0.4470`, test_delta_vs_18E=`-13.596`, holdout_b_delta_vs_18E=`-5.590`
  - `2501`: validation=`-27.168`, test=`36.698`, PF=`1.5542`, holdout_b=`4.884`, holdout_b_PF=`1.3397`, test_delta_vs_18E=`-1.780`, holdout_b_delta_vs_18E=`4.222`

- [6] `19D` `recent_9m_x2p0`: avg_test=`20.622`, avg_test_delta_vs_18E=`-12.241`, target_holdout_b=`-12.544`, target_holdout_b_delta_vs_18E=`-9.262`, min_holdout_b=`-12.544`, positive_test_windows=`3/3`, positive_holdout_b_windows=`2/3`
  - rationale: `Broader nine-month emphasis to capture a wider late-train regime instead of a narrow recent pocket.`
  - `2401`: validation=`-11.658`, test=`10.238`, PF=`1.0607`, holdout_b=`25.298`, holdout_b_PF=`1.5820`, test_delta_vs_18E=`-22.174`, holdout_b_delta_vs_18E=`0.596`
  - `2407`: validation=`45.228`, test=`1.898`, PF=`1.0311`, holdout_b=`-12.544`, holdout_b_PF=`0.3461`, test_delta_vs_18E=`-25.802`, holdout_b_delta_vs_18E=`-9.262`
  - `2501`: validation=`-16.384`, test=`49.730`, PF=`1.8559`, holdout_b=`8.438`, holdout_b_PF=`1.6962`, test_delta_vs_18E=`11.252`, holdout_b_delta_vs_18E=`7.776`

- [7] `19E` `recent_6m_short_guard`: avg_test=`-11.205`, avg_test_delta_vs_18E=`-44.068`, target_holdout_b=`-19.064`, target_holdout_b_delta_vs_18E=`-15.782`, min_holdout_b=`-19.064`, positive_test_windows=`1/3`, positive_holdout_b_windows=`1/3`
  - rationale: `Recency emphasis with an extra short boost to see whether the 2407-like bad regime is best handled by later short separation.`
  - `2401`: validation=`-23.850`, test=`-10.400`, PF=`0.9623`, holdout_b=`7.466`, holdout_b_PF=`1.0968`, test_delta_vs_18E=`-42.812`, holdout_b_delta_vs_18E=`-17.236`
  - `2407`: validation=`37.322`, test=`-37.392`, PF=`0.7843`, holdout_b=`-19.064`, holdout_b_PF=`0.5597`, test_delta_vs_18E=`-65.092`, holdout_b_delta_vs_18E=`-15.782`
  - `2501`: validation=`-10.370`, test=`14.178`, PF=`1.0462`, holdout_b=`-10.916`, holdout_b_PF=`0.8820`, test_delta_vs_18E=`-24.300`, holdout_b_delta_vs_18E=`-11.578`

## Readout

- recent-regime leader: `19A` `18E_reference`
- leader avg test return: `32.863`
- leader avg delta vs 18E: `0.000`
- leader target 2407 holdout_b: `-3.282`
- leader target holdout_b delta vs 18E: `0.000`
- total runs captured: `21`
