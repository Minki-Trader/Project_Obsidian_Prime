# Stage 16 09C Feature Core Fork Review

- windows: `2401, 2407, 2501`
- source core: `09C_05ET_margin0700_t30_l50_m0700_h4`
- target: `2407 / holdout_b`
- ranking basis: `positive_test_windows -> avg_test_return -> positive_holdout_b_windows -> min_holdout_b -> min_test -> avg_test_pf`

## Candidate Ranking

- [1] `16A` `09C_reference_full`: avg_test=`18.151`, min_test=`-4.582`, target_holdout_b=`-9.064`, target_holdout_b_PF=`0.8558`, min_holdout_b=`-9.064`, positive_test_windows=`2/3`, positive_holdout_b_windows=`2/3`
  - rationale: `Reference 09C core with persistence+riskoff proxy, session features, and external breadth intact.`
  - `2401`: validation=`-1.918`, test=`-4.582`, PF=`0.9866`, holdout_b=`8.112`, holdout_b_PF=`1.0953`
  - `2407`: validation=`23.612`, test=`9.944`, PF=`1.0365`, holdout_b=`-9.064`, holdout_b_PF=`0.8558`
  - `2501`: validation=`2.118`, test=`49.090`, PF=`1.2682`, holdout_b=`1.722`, holdout_b_PF=`1.0313`

- [2] `16B` `09C_persistence_only`: avg_test=`12.754`, min_test=`-19.272`, target_holdout_b=`-10.322`, target_holdout_b_PF=`0.8128`, min_holdout_b=`-10.322`, positive_test_windows=`1/3`, positive_holdout_b_windows=`2/3`
  - rationale: `Strip macro risk-off confirmation and keep only persistence proxy to test whether macro confirmation is overfitting shifted windows.`
  - `2401`: validation=`-32.572`, test=`-19.272`, PF=`0.9412`, holdout_b=`10.062`, holdout_b_PF=`1.1202`
  - `2407`: validation=`44.662`, test=`-1.214`, PF=`0.9954`, holdout_b=`-10.322`, holdout_b_PF=`0.8128`
  - `2501`: validation=`-0.200`, test=`58.748`, PF=`1.3186`, holdout_b=`9.636`, holdout_b_PF=`1.1854`

- [3] `16C` `09C_sessionless`: avg_test=`5.090`, min_test=`-18.750`, target_holdout_b=`-9.702`, target_holdout_b_PF=`0.8337`, min_holdout_b=`-9.702`, positive_test_windows=`1/3`, positive_holdout_b_windows=`2/3`
  - rationale: `Remove explicit session-timing inputs and let price/volatility drive entry quality instead of time-of-day memorization.`
  - `2401`: validation=`-14.342`, test=`-11.612`, PF=`0.9658`, holdout_b=`5.264`, holdout_b_PF=`1.0592`
  - `2407`: validation=`45.688`, test=`-18.750`, PF=`0.9315`, holdout_b=`-9.702`, holdout_b_PF=`0.8337`
  - `2501`: validation=`4.070`, test=`45.632`, PF=`1.2623`, holdout_b=`10.862`, holdout_b_PF=`1.2639`

- [4] `16D` `09C_external_breadthless`: avg_test=`-5.071`, min_test=`-24.932`, target_holdout_b=`-11.106`, target_holdout_b_PF=`0.7772`, min_holdout_b=`-11.106`, positive_test_windows=`1/3`, positive_holdout_b_windows=`2/3`
  - rationale: `Remove mega-cap constituent/breadth inputs to test whether component crowding is causing recent-only edge.`
  - `2401`: validation=`-44.208`, test=`-15.256`, PF=`0.9477`, holdout_b=`5.344`, holdout_b_PF=`1.0752`
  - `2407`: validation=`10.790`, test=`-24.932`, PF=`0.8987`, holdout_b=`-11.106`, holdout_b_PF=`0.7772`
  - `2501`: validation=`-15.466`, test=`24.976`, PF=`1.1415`, holdout_b=`1.484`, holdout_b_PF=`1.0280`

## Readout

- feature-fork leader: `16A` `09C_reference_full`
- leader avg test return: `18.151`
- leader min holdout_b: `-9.064`
- leader target 2407 holdout_b: `-9.064`
- total runs captured: `12`
