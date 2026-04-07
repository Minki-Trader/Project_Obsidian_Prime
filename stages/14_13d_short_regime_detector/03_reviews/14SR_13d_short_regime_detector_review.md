# Stage 14 13D Short Regime Detector Review

- source core: `09C_05ET_margin0700_t30_l50_m0700_h4`
- reference overlay: `13D monday=0.575, post-cash=0.6125`
- reference target 2407 holdout_b: `-5.768`
- reference avg test return: `24.554`
- ranking basis: `2407 holdout_b return_pct -> min holdout_b return_pct -> avg test return_pct -> avg test PF`

## Variant Ranking

- [1] `14A` `stage13d_reference`: target_holdout_b=`-5.768`, target_holdout_b_PF=`0.8802`, min_holdout_b=`-5.768`, avg_test=`24.554`, positive_test_windows=`3/3`, positive_holdout_b_windows=`2/3`
  - `2401`: test=`2.886`, PF=`1.0094`, holdout_b=`12.494`, holdout_b_PF=`1.1645`, delta_test=`0.000`, delta_PF=`0.0000`
  - `2407`: test=`18.792`, PF=`1.0879`, holdout_b=`-5.768`, holdout_b_PF=`0.8802`, delta_test=`0.000`, delta_PF=`0.0000`
  - `2501`: test=`51.984`, PF=`1.3089`, holdout_b=`0.576`, holdout_b_PF=`1.0113`, delta_test=`0.000`, delta_PF=`0.0000`

- [2] `14B` `tuewed_cash_short_075`: target_holdout_b=`-5.768`, target_holdout_b_PF=`0.8802`, min_holdout_b=`-5.768`, avg_test=`24.554`, positive_test_windows=`3/3`, positive_holdout_b_windows=`2/3`
  - `2401`: test=`2.886`, PF=`1.0094`, holdout_b=`12.494`, holdout_b_PF=`1.1645`, delta_test=`0.000`, delta_PF=`0.0000`
  - `2407`: test=`18.792`, PF=`1.0879`, holdout_b=`-5.768`, holdout_b_PF=`0.8802`, delta_test=`0.000`, delta_PF=`0.0000`
  - `2501`: test=`51.984`, PF=`1.3089`, holdout_b=`0.576`, holdout_b_PF=`1.0113`, delta_test=`0.000`, delta_PF=`0.0000`

- [3] `14C` `tuewed_cash_short_050`: target_holdout_b=`-5.768`, target_holdout_b_PF=`0.8802`, min_holdout_b=`-5.768`, avg_test=`24.554`, positive_test_windows=`3/3`, positive_holdout_b_windows=`2/3`
  - `2401`: test=`2.886`, PF=`1.0094`, holdout_b=`12.494`, holdout_b_PF=`1.1645`, delta_test=`0.000`, delta_PF=`0.0000`
  - `2407`: test=`18.792`, PF=`1.0879`, holdout_b=`-5.768`, holdout_b_PF=`0.8802`, delta_test=`0.000`, delta_PF=`0.0000`
  - `2501`: test=`51.984`, PF=`1.3089`, holdout_b=`0.576`, holdout_b_PF=`1.0113`, delta_test=`0.000`, delta_PF=`0.0000`

- [4] `14D` `tuewed_cash_short_035`: target_holdout_b=`-5.768`, target_holdout_b_PF=`0.8802`, min_holdout_b=`-5.768`, avg_test=`24.554`, positive_test_windows=`3/3`, positive_holdout_b_windows=`2/3`
  - `2401`: test=`2.886`, PF=`1.0094`, holdout_b=`12.494`, holdout_b_PF=`1.1645`, delta_test=`0.000`, delta_PF=`0.0000`
  - `2407`: test=`18.792`, PF=`1.0879`, holdout_b=`-5.768`, holdout_b_PF=`0.8802`, delta_test=`0.000`, delta_PF=`0.0000`
  - `2501`: test=`51.984`, PF=`1.3089`, holdout_b=`0.576`, holdout_b_PF=`1.0113`, delta_test=`0.000`, delta_PF=`0.0000`

- [5] `14E` `tuewed_cash_short_h12h14_035`: target_holdout_b=`-5.768`, target_holdout_b_PF=`0.8802`, min_holdout_b=`-5.768`, avg_test=`24.554`, positive_test_windows=`3/3`, positive_holdout_b_windows=`2/3`
  - `2401`: test=`2.886`, PF=`1.0094`, holdout_b=`12.494`, holdout_b_PF=`1.1645`, delta_test=`0.000`, delta_PF=`0.0000`
  - `2407`: test=`18.792`, PF=`1.0879`, holdout_b=`-5.768`, holdout_b_PF=`0.8802`, delta_test=`0.000`, delta_PF=`0.0000`
  - `2501`: test=`51.984`, PF=`1.3089`, holdout_b=`0.576`, holdout_b_PF=`1.0113`, delta_test=`0.000`, delta_PF=`0.0000`

- [6] `14F` `tuewed_cash_short_075_h12h14_035`: target_holdout_b=`-5.768`, target_holdout_b_PF=`0.8802`, min_holdout_b=`-5.768`, avg_test=`24.554`, positive_test_windows=`3/3`, positive_holdout_b_windows=`2/3`
  - `2401`: test=`2.886`, PF=`1.0094`, holdout_b=`12.494`, holdout_b_PF=`1.1645`, delta_test=`0.000`, delta_PF=`0.0000`
  - `2407`: test=`18.792`, PF=`1.0879`, holdout_b=`-5.768`, holdout_b_PF=`0.8802`, delta_test=`0.000`, delta_PF=`0.0000`
  - `2501`: test=`51.984`, PF=`1.3089`, holdout_b=`0.576`, holdout_b_PF=`1.0113`, delta_test=`0.000`, delta_PF=`0.0000`

## Readout

- detector leader: `14A` `stage13d_reference`
- target 2407 holdout_b: `-5.768`
- vs 13D target delta: `0.000`
