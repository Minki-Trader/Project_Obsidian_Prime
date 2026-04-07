# Stage 20 18E Specialist Mixture Review

- windows: `2401, 2407, 2501`
- source operating reference: `18E = 17E + PH20`
- target: `2407 / holdout_b`
- ranking basis: `positive_test_windows -> positive_holdout_b_windows -> avg_test_return -> min_holdout_b -> target_holdout_b -> avg_test_pf`

## Candidate Ranking

- [1] `20A` `18E_reference`: avg_test=`32.863`, avg_test_delta_vs_18E=`0.000`, target_holdout_b=`-3.282`, target_holdout_b_delta_vs_18E=`0.000`, min_holdout_b=`-3.282`, positive_test_windows=`3/3`, positive_holdout_b_windows=`2/3`
  - rationale: `Exact 18E reference so the mixture family is ranked against the current practical operating leader.`
  - components: `17E` / weights=`1.00`
  - `2401`: validation=`20.938`, test=`32.412`, PF=`1.2205`, holdout_b=`24.702`, holdout_b_PF=`1.6512`, test_delta_vs_18E=`0.000`, holdout_b_delta_vs_18E=`0.000`
  - `2407`: validation=`61.388`, test=`27.700`, PF=`1.4127`, holdout_b=`-3.282`, holdout_b_PF=`0.7972`, test_delta_vs_18E=`0.000`, holdout_b_delta_vs_18E=`0.000`
  - `2501`: validation=`-5.520`, test=`38.478`, PF=`1.5343`, holdout_b=`0.662`, holdout_b_PF=`1.0342`, test_delta_vs_18E=`0.000`, holdout_b_delta_vs_18E=`0.000`

- [2] `20F` `17E_17C_vote_75_25_ph20`: avg_test=`25.545`, avg_test_delta_vs_18E=`-7.318`, target_holdout_b=`-12.210`, target_holdout_b_delta_vs_18E=`-8.928`, min_holdout_b=`-12.210`, positive_test_windows=`3/3`, positive_holdout_b_windows=`2/3`
  - rationale: `More aggressive specialist share to test whether 2407-like windows need a stronger short-specialist contribution.`
  - components: `17E, 17C` / weights=`0.75, 0.25`
  - `2401`: validation=`-20.854`, test=`38.866`, PF=`1.1734`, holdout_b=`29.140`, holdout_b_PF=`1.5453`, test_delta_vs_18E=`6.454`, holdout_b_delta_vs_18E=`4.438`
  - `2407`: validation=`18.570`, test=`2.746`, PF=`1.0215`, holdout_b=`-12.210`, holdout_b_PF=`0.6041`, test_delta_vs_18E=`-24.954`, holdout_b_delta_vs_18E=`-8.928`
  - `2501`: validation=`15.112`, test=`35.024`, PF=`1.3718`, holdout_b=`9.850`, holdout_b_PF=`1.3857`, test_delta_vs_18E=`-3.454`, holdout_b_delta_vs_18E=`9.188`

- [3] `20I` `17E_17C_17D_vote_75_20_05_ph20`: avg_test=`23.334`, avg_test_delta_vs_18E=`-9.529`, target_holdout_b=`-11.998`, target_holdout_b_delta_vs_18E=`-8.716`, min_holdout_b=`-11.998`, positive_test_windows=`3/3`, positive_holdout_b_windows=`2/3`
  - rationale: `Three-way mixture that keeps 17E as the core, adds 17C short specialization, and lets 17D contribute a small abstention bias.`
  - components: `17E, 17C, 17D` / weights=`0.75, 0.20, 0.05`
  - `2401`: validation=`-27.338`, test=`22.306`, PF=`1.1085`, holdout_b=`18.452`, holdout_b_PF=`1.3503`, test_delta_vs_18E=`-10.106`, holdout_b_delta_vs_18E=`-6.250`
  - `2407`: validation=`34.616`, test=`2.492`, PF=`1.0216`, holdout_b=`-11.998`, holdout_b_PF=`0.5649`, test_delta_vs_18E=`-25.208`, holdout_b_delta_vs_18E=`-8.716`
  - `2501`: validation=`0.696`, test=`45.204`, PF=`1.5431`, holdout_b=`7.244`, holdout_b_PF=`1.3236`, test_delta_vs_18E=`6.726`, holdout_b_delta_vs_18E=`6.582`

- [4] `20J` `17E_17C_17D_vote_70_20_10_bd20`: avg_test=`22.993`, avg_test_delta_vs_18E=`-9.870`, target_holdout_b=`-8.032`, target_holdout_b_delta_vs_18E=`-4.750`, min_holdout_b=`-8.032`, positive_test_windows=`3/3`, positive_holdout_b_windows=`2/3`
  - rationale: `Broader mixture with a slightly larger flat-guard share under the balanced-micro overlay for a more defensive practical fork.`
  - components: `17E, 17C, 17D` / weights=`0.70, 0.20, 0.10`
  - `2401`: validation=`-26.968`, test=`20.490`, PF=`1.1026`, holdout_b=`21.550`, holdout_b_PF=`1.4462`, test_delta_vs_18E=`-11.922`, holdout_b_delta_vs_18E=`-3.152`
  - `2407`: validation=`35.180`, test=`5.184`, PF=`1.0495`, holdout_b=`-8.032`, holdout_b_PF=`0.5948`, test_delta_vs_18E=`-22.516`, holdout_b_delta_vs_18E=`-4.750`
  - `2501`: validation=`-2.564`, test=`43.306`, PF=`1.5789`, holdout_b=`8.682`, holdout_b_PF=`1.4356`, test_delta_vs_18E=`4.828`, holdout_b_delta_vs_18E=`8.020`

- [5] `20B` `17C_balanced_micro_reference`: avg_test=`10.231`, avg_test_delta_vs_18E=`-22.632`, target_holdout_b=`7.472`, target_holdout_b_delta_vs_18E=`10.754`, min_holdout_b=`-9.408`, positive_test_windows=`3/3`, positive_holdout_b_windows=`2/3`
  - rationale: `18J-style practical short specialist reference with the balanced-micro operating overlay.`
  - components: `17C` / weights=`1.00`
  - `2401`: validation=`-2.170`, test=`7.660`, PF=`1.0282`, holdout_b=`3.614`, holdout_b_PF=`1.0535`, test_delta_vs_18E=`-24.752`, holdout_b_delta_vs_18E=`-21.088`
  - `2407`: validation=`11.918`, test=`19.302`, PF=`1.1152`, holdout_b=`7.472`, holdout_b_PF=`1.3718`, test_delta_vs_18E=`-8.398`, holdout_b_delta_vs_18E=`10.754`
  - `2501`: validation=`-6.920`, test=`3.732`, PF=`1.0347`, holdout_b=`-9.408`, holdout_b_PF=`0.7111`, test_delta_vs_18E=`-34.746`, holdout_b_delta_vs_18E=`-10.070`

- [6] `20C` `17C_postcash_hold_cut_reference`: avg_test=`9.337`, avg_test_delta_vs_18E=`-23.526`, target_holdout_b=`7.348`, target_holdout_b_delta_vs_18E=`10.630`, min_holdout_b=`-6.194`, positive_test_windows=`3/3`, positive_holdout_b_windows=`2/3`
  - rationale: `18K-style practical short specialist reference with the post-cash hold-cut operating overlay.`
  - components: `17C` / weights=`1.00`
  - `2401`: validation=`4.630`, test=`0.890`, PF=`1.0031`, holdout_b=`6.862`, holdout_b_PF=`1.0978`, test_delta_vs_18E=`-31.522`, holdout_b_delta_vs_18E=`-17.840`
  - `2407`: validation=`3.094`, test=`17.402`, PF=`1.0906`, holdout_b=`7.348`, holdout_b_PF=`1.2838`, test_delta_vs_18E=`-10.298`, holdout_b_delta_vs_18E=`10.630`
  - `2501`: validation=`-12.188`, test=`9.720`, PF=`1.0868`, holdout_b=`-6.194`, holdout_b_PF=`0.8155`, test_delta_vs_18E=`-28.758`, holdout_b_delta_vs_18E=`-6.856`

- [7] `20H` `17E_17C_vote_75_25_bd20`: avg_test=`28.818`, avg_test_delta_vs_18E=`-4.045`, target_holdout_b=`-12.978`, target_holdout_b_delta_vs_18E=`-9.696`, min_holdout_b=`-12.978`, positive_test_windows=`2/3`, positive_holdout_b_windows=`2/3`
  - rationale: `Stronger specialist blend under the balanced-micro operating overlay to see whether the practical defender and the model-side specialist reinforce each other.`
  - components: `17E, 17C` / weights=`0.75, 0.25`
  - `2401`: validation=`-25.138`, test=`50.560`, PF=`1.2287`, holdout_b=`29.756`, holdout_b_PF=`1.5450`, test_delta_vs_18E=`18.148`, holdout_b_delta_vs_18E=`5.054`
  - `2407`: validation=`13.812`, test=`-0.646`, PF=`0.9944`, holdout_b=`-12.978`, holdout_b_PF=`0.5219`, test_delta_vs_18E=`-28.346`, holdout_b_delta_vs_18E=`-9.696`
  - `2501`: validation=`13.182`, test=`36.540`, PF=`1.3926`, holdout_b=`10.610`, holdout_b_PF=`1.4412`, test_delta_vs_18E=`-1.938`, holdout_b_delta_vs_18E=`9.948`

- [8] `20G` `17E_17C_vote_80_20_bd20`: avg_test=`24.265`, avg_test_delta_vs_18E=`-8.598`, target_holdout_b=`-8.488`, target_holdout_b_delta_vs_18E=`-5.206`, min_holdout_b=`-8.488`, positive_test_windows=`2/3`, positive_holdout_b_windows=`2/3`
  - rationale: `Blend the robust core with the short specialist while switching to the balanced-micro operating overlay used by 18J.`
  - components: `17E, 17C` / weights=`0.80, 0.20`
  - `2401`: validation=`-33.344`, test=`34.650`, PF=`1.1766`, holdout_b=`20.414`, holdout_b_PF=`1.3945`, test_delta_vs_18E=`2.238`, holdout_b_delta_vs_18E=`-4.288`
  - `2407`: validation=`26.968`, test=`-2.006`, PF=`0.9792`, holdout_b=`-8.488`, holdout_b_PF=`0.6241`, test_delta_vs_18E=`-29.706`, holdout_b_delta_vs_18E=`-5.206`
  - `2501`: validation=`13.102`, test=`40.152`, PF=`1.4763`, holdout_b=`7.208`, holdout_b_PF=`1.2936`, test_delta_vs_18E=`1.674`, holdout_b_delta_vs_18E=`6.546`

- [9] `20E` `17E_17C_vote_80_20_ph20`: avg_test=`24.119`, avg_test_delta_vs_18E=`-8.744`, target_holdout_b=`-9.458`, target_holdout_b_delta_vs_18E=`-6.176`, min_holdout_b=`-9.458`, positive_test_windows=`2/3`, positive_holdout_b_windows=`2/3`
  - rationale: `Mid-strength specialist blend under the proven 18E operating overlay.`
  - components: `17E, 17C` / weights=`0.80, 0.20`
  - `2401`: validation=`-27.584`, test=`36.248`, PF=`1.1736`, holdout_b=`26.934`, holdout_b_PF=`1.5257`, test_delta_vs_18E=`3.836`, holdout_b_delta_vs_18E=`2.232`
  - `2407`: validation=`31.696`, test=`-4.280`, PF=`0.9595`, holdout_b=`-9.458`, holdout_b_PF=`0.6341`, test_delta_vs_18E=`-31.980`, holdout_b_delta_vs_18E=`-6.176`
  - `2501`: validation=`8.938`, test=`40.390`, PF=`1.4591`, holdout_b=`6.006`, holdout_b_PF=`1.2352`, test_delta_vs_18E=`1.912`, holdout_b_delta_vs_18E=`5.344`

- [10] `20D` `17E_17C_vote_85_15_ph20`: avg_test=`23.263`, avg_test_delta_vs_18E=`-9.600`, target_holdout_b=`-5.458`, target_holdout_b_delta_vs_18E=`-2.176`, min_holdout_b=`-5.458`, positive_test_windows=`2/3`, positive_holdout_b_windows=`2/3`
  - rationale: `Conservative soft mixture that keeps 17E dominant while letting 17C nudge short probabilities in bad regimes.`
  - components: `17E, 17C` / weights=`0.85, 0.15`
  - `2401`: validation=`-20.958`, test=`37.756`, PF=`1.1897`, holdout_b=`25.268`, holdout_b_PF=`1.5094`, test_delta_vs_18E=`5.344`, holdout_b_delta_vs_18E=`0.566`
  - `2407`: validation=`58.064`, test=`-6.540`, PF=`0.9358`, holdout_b=`-5.458`, holdout_b_PF=`0.7683`, test_delta_vs_18E=`-34.240`, holdout_b_delta_vs_18E=`-2.176`
  - `2501`: validation=`15.022`, test=`38.574`, PF=`1.4338`, holdout_b=`8.544`, holdout_b_PF=`1.4084`, test_delta_vs_18E=`0.096`, holdout_b_delta_vs_18E=`7.882`

## Readout

- specialist-mixture leader: `20A` `18E_reference`
- leader avg test return: `32.863`
- leader avg delta vs 18E: `0.000`
- leader target 2407 holdout_b: `-3.282`
- leader target holdout_b delta vs 18E: `0.000`
- total runs captured: `30`
