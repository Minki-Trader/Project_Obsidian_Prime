# Stage 08 Strict WFO Shortlist Review

- windows: `2401, 2407, 2501`
- ranking basis: `min holdout_b return_pct -> avg test return_pct -> min test return_pct -> avg test PF`

## Candidate Ranking

- [1] `08C` `05ET_core_long_suppression_hold4`: core=`05ET_05dp_stronger_long_suppression_hold4_0001`, motif=`none`, avg_test=`11.005`, min_test=`-10.468`, avg_holdout_b=`-1.403`, min_holdout_b=`-10.192`, positive_test_windows=`1/3`, positive_holdout_b_windows=`1/3`, worst_window=`2407`
  - `2401`: validation=`-0.264`, test=`-10.468`, PF=`0.9699`, holdout_b=`7.646`, holdout_b_PF=`1.0889`
  - `2407`: validation=`37.642`, test=`-0.036`, PF=`0.9999`, holdout_b=`-10.192`, holdout_b_PF=`0.8350`
  - `2501`: validation=`-2.824`, test=`43.518`, PF=`1.2396`, holdout_b=`-1.664`, holdout_b_PF=`0.9697`

- [2] `08D` `05ET_plus_05FD_motif`: core=`05ET_05dp_stronger_long_suppression_hold4_0001`, motif=`05FD_05ca_flatup_longdown_margin0675_hold5_0001`, avg_test=`-3.733`, min_test=`-26.196`, avg_holdout_b=`-6.015`, min_holdout_b=`-15.296`, positive_test_windows=`1/3`, positive_holdout_b_windows=`1/3`, worst_window=`2407`
  - `2401`: validation=`-19.382`, test=`-26.196`, PF=`0.9188`, holdout_b=`-4.310`, holdout_b_PF=`0.9473`
  - `2407`: validation=`-22.166`, test=`-22.002`, PF=`0.9290`, holdout_b=`-15.296`, holdout_b_PF=`0.7683`
  - `2501`: validation=`-23.512`, test=`36.998`, PF=`1.1697`, holdout_b=`1.562`, holdout_b_PF=`1.0265`

- [3] `08B` `05EM_core_short_bias_hold5`: core=`05EM_05dp_short_bias_margin_hold5_0001`, motif=`none`, avg_test=`35.055`, min_test=`-2.636`, avg_holdout_b=`-0.286`, min_holdout_b=`-20.528`, positive_test_windows=`2/3`, positive_holdout_b_windows=`1/3`, worst_window=`2407`
  - `2401`: validation=`27.080`, test=`54.276`, PF=`1.1200`, holdout_b=`38.400`, holdout_b_PF=`1.3961`
  - `2407`: validation=`56.956`, test=`-2.636`, PF=`0.9919`, holdout_b=`-20.528`, holdout_b_PF=`0.7315`
  - `2501`: validation=`-39.972`, test=`53.526`, PF=`1.1996`, holdout_b=`-18.730`, holdout_b_PF=`0.7811`

- [4] `08A` `05ER_core_short_bias_hold4`: core=`05ER_05dp_short_bias_margin_hold4_0001`, motif=`none`, avg_test=`13.210`, min_test=`-8.508`, avg_holdout_b=`-3.103`, min_holdout_b=`-22.258`, positive_test_windows=`2/3`, positive_holdout_b_windows=`1/3`, worst_window=`2407`
  - `2401`: validation=`-7.414`, test=`15.488`, PF=`1.0343`, holdout_b=`24.412`, holdout_b_PF=`1.2268`
  - `2407`: validation=`14.382`, test=`-8.508`, PF=`0.9725`, holdout_b=`-22.258`, holdout_b_PF=`0.6878`
  - `2501`: validation=`-34.636`, test=`32.650`, PF=`1.1389`, holdout_b=`-11.462`, holdout_b_PF=`0.8472`

## Readout

- shortlist leader: `08C` `05ET_core_long_suppression_hold4`
- leader min_holdout_b: `-10.192`
- leader avg_test_return: `11.005`
- total runs captured: `12`
