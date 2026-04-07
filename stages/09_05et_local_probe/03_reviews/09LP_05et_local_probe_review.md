# Stage 09 05ET Local Probe Review

- windows: `2401, 2407, 2501`
- target: `2407 / holdout_b`
- ranking basis: `2407 holdout_b return_pct -> min holdout_b return_pct -> avg test return_pct -> avg test PF`

## Candidate Ranking

- [1] `09C` `05ET_margin0700_t30_l50_m0700_h4`: Ts=`0.300`, Tl=`0.500`, margin=`0.0700`, hold=`4`, target_holdout_b=`-9.064`, target_holdout_b_PF=`0.8558`, min_holdout_b=`-9.064`, avg_test=`18.151`, positive_test_windows=`2/3`, positive_holdout_b_windows=`2/3`
  - `2401`: validation=`-1.918`, test=`-4.582`, PF=`0.9866`, holdout_b=`8.112`, holdout_b_PF=`1.0953`
  - `2407`: validation=`23.612`, test=`9.944`, PF=`1.0365`, holdout_b=`-9.064`, holdout_b_PF=`0.8558`
  - `2501`: validation=`2.118`, test=`49.090`, PF=`1.2682`, holdout_b=`1.722`, holdout_b_PF=`1.0313`

- [2] `09E` `05ET_short325_t325_l50_m0700_h4`: Ts=`0.325`, Tl=`0.500`, margin=`0.0700`, hold=`4`, target_holdout_b=`-9.064`, target_holdout_b_PF=`0.8558`, min_holdout_b=`-9.064`, avg_test=`18.151`, positive_test_windows=`2/3`, positive_holdout_b_windows=`2/3`
  - `2401`: validation=`-1.918`, test=`-4.582`, PF=`0.9866`, holdout_b=`8.112`, holdout_b_PF=`1.0953`
  - `2407`: validation=`23.612`, test=`9.944`, PF=`1.0365`, holdout_b=`-9.064`, holdout_b_PF=`0.8558`
  - `2501`: validation=`2.118`, test=`49.090`, PF=`1.2682`, holdout_b=`1.722`, holdout_b_PF=`1.0313`

- [3] `09G` `05ET_long525_t30_l525_m0700_h4`: Ts=`0.300`, Tl=`0.525`, margin=`0.0700`, hold=`4`, target_holdout_b=`-9.894`, target_holdout_b_PF=`0.8413`, min_holdout_b=`-9.894`, avg_test=`17.619`, positive_test_windows=`2/3`, positive_holdout_b_windows=`2/3`
  - `2401`: validation=`-0.286`, test=`-1.142`, PF=`0.9966`, holdout_b=`8.898`, holdout_b_PF=`1.1060`
  - `2407`: validation=`12.788`, test=`18.466`, PF=`1.0690`, holdout_b=`-9.894`, holdout_b_PF=`0.8413`
  - `2501`: validation=`3.066`, test=`35.532`, PF=`1.2264`, holdout_b=`4.870`, holdout_b_PF=`1.1048`

- [4] `09A` `05ET_base_t30_l50_m0675_h4`: Ts=`0.300`, Tl=`0.500`, margin=`0.0675`, hold=`4`, target_holdout_b=`-10.192`, target_holdout_b_PF=`0.8350`, min_holdout_b=`-10.192`, avg_test=`11.005`, positive_test_windows=`1/3`, positive_holdout_b_windows=`1/3`
  - `2401`: validation=`-0.264`, test=`-10.468`, PF=`0.9699`, holdout_b=`7.646`, holdout_b_PF=`1.0889`
  - `2407`: validation=`37.642`, test=`-0.036`, PF=`0.9999`, holdout_b=`-10.192`, holdout_b_PF=`0.8350`
  - `2501`: validation=`-2.824`, test=`43.518`, PF=`1.2396`, holdout_b=`-1.664`, holdout_b_PF=`0.9697`

- [5] `09B` `05ET_short325_t325_l50_m0675_h4`: Ts=`0.325`, Tl=`0.500`, margin=`0.0675`, hold=`4`, target_holdout_b=`-10.192`, target_holdout_b_PF=`0.8350`, min_holdout_b=`-10.192`, avg_test=`11.005`, positive_test_windows=`1/3`, positive_holdout_b_windows=`1/3`
  - `2401`: validation=`-0.264`, test=`-10.468`, PF=`0.9699`, holdout_b=`7.646`, holdout_b_PF=`1.0889`
  - `2407`: validation=`37.642`, test=`-0.036`, PF=`0.9999`, holdout_b=`-10.192`, holdout_b_PF=`0.8350`
  - `2501`: validation=`-2.824`, test=`43.518`, PF=`1.2396`, holdout_b=`-1.664`, holdout_b_PF=`0.9697`

- [6] `09H` `05ET_short325_long525_m0700_h3`: Ts=`0.325`, Tl=`0.525`, margin=`0.0700`, hold=`3`, target_holdout_b=`-13.854`, target_holdout_b_PF=`0.7335`, min_holdout_b=`-13.854`, avg_test=`5.431`, positive_test_windows=`1/3`, positive_holdout_b_windows=`2/3`
  - `2401`: validation=`-6.752`, test=`-0.610`, PF=`0.9981`, holdout_b=`13.274`, holdout_b_PF=`1.1648`
  - `2407`: validation=`57.042`, test=`-13.290`, PF=`0.9454`, holdout_b=`-13.854`, holdout_b_PF=`0.7335`
  - `2501`: validation=`-2.662`, test=`30.192`, PF=`1.1848`, holdout_b=`3.652`, holdout_b_PF=`1.0703`

- [7] `09D` `05ET_hold3_t30_l50_m0675_h3`: Ts=`0.300`, Tl=`0.500`, margin=`0.0675`, hold=`3`, target_holdout_b=`-18.912`, target_holdout_b_PF=`0.7054`, min_holdout_b=`-18.912`, avg_test=`11.227`, positive_test_windows=`2/3`, positive_holdout_b_windows=`1/3`
  - `2401`: validation=`-21.792`, test=`5.186`, PF=`1.0152`, holdout_b=`15.646`, holdout_b_PF=`1.1915`
  - `2407`: validation=`15.554`, test=`-8.974`, PF=`0.9665`, holdout_b=`-18.912`, holdout_b_PF=`0.7054`
  - `2501`: validation=`-1.618`, test=`37.468`, PF=`1.1928`, holdout_b=`-3.238`, holdout_b_PF=`0.9514`

- [8] `09F` `05ET_short325_t325_l50_m0675_h3`: Ts=`0.325`, Tl=`0.500`, margin=`0.0675`, hold=`3`, target_holdout_b=`-18.912`, target_holdout_b_PF=`0.7054`, min_holdout_b=`-18.912`, avg_test=`11.227`, positive_test_windows=`2/3`, positive_holdout_b_windows=`1/3`
  - `2401`: validation=`-21.792`, test=`5.186`, PF=`1.0152`, holdout_b=`15.646`, holdout_b_PF=`1.1915`
  - `2407`: validation=`15.554`, test=`-8.974`, PF=`0.9665`, holdout_b=`-18.912`, holdout_b_PF=`0.7054`
  - `2501`: validation=`-1.618`, test=`37.468`, PF=`1.1928`, holdout_b=`-3.238`, holdout_b_PF=`0.9514`

## Readout

- probe leader: `09C` `05ET_margin0700_t30_l50_m0700_h4`
- target 2407 holdout_b: `-9.064`
- min holdout_b: `-9.064`
- avg test return: `18.151`
- total runs captured: `24`
