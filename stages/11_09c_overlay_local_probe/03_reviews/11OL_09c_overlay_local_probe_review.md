# Stage 11 09C Overlay Local Probe Review

- source core: `09C_05ET_margin0700_t30_l50_m0700_h4`
- source target 2407 holdout_b: `-9.064`
- source avg test return: `18.151`
- ranking basis: `2407 holdout_b return_pct -> min holdout_b return_pct -> avg test return_pct -> avg test PF`

## Variant Ranking

- [1] `11B` `monday_065_post065`: target_holdout_b=`-6.498`, target_holdout_b_PF=`0.8689`, min_holdout_b=`-6.498`, avg_test=`22.681`, positive_test_windows=`3/3`, positive_holdout_b_windows=`2/3`
  - `2401`: test=`2.100`, PF=`1.0067`, holdout_b=`12.066`, holdout_b_PF=`1.1555`, delta_test=`6.682`, delta_PF=`0.0200`
  - `2407`: test=`14.554`, PF=`1.0665`, holdout_b=`-6.498`, holdout_b_PF=`0.8689`, delta_test=`4.610`, delta_PF=`0.0299`
  - `2501`: test=`51.390`, PF=`1.3006`, holdout_b=`0.700`, holdout_b_PF=`1.0135`, delta_test=`2.300`, delta_PF=`0.0324`

- [2] `11D` `monday_065_post060`: target_holdout_b=`-6.586`, target_holdout_b_PF=`0.8651`, min_holdout_b=`-6.586`, avg_test=`24.381`, positive_test_windows=`3/3`, positive_holdout_b_windows=`2/3`
  - `2401`: test=`4.142`, PF=`1.0132`, holdout_b=`11.998`, holdout_b_PF=`1.1543`, delta_test=`8.724`, delta_PF=`0.0266`
  - `2407`: test=`16.788`, PF=`1.0780`, holdout_b=`-6.586`, holdout_b_PF=`0.8651`, delta_test=`6.844`, delta_PF=`0.0415`
  - `2501`: test=`52.212`, PF=`1.3089`, holdout_b=`0.514`, holdout_b_PF=`1.0099`, delta_test=`3.122`, delta_PF=`0.0407`

- [3] `11A` `lp02_reference`: target_holdout_b=`-6.696`, target_holdout_b_PF=`0.8622`, min_holdout_b=`-6.696`, avg_test=`21.734`, positive_test_windows=`3/3`, positive_holdout_b_windows=`2/3`
  - `2401`: test=`2.154`, PF=`1.0068`, holdout_b=`11.568`, holdout_b_PF=`1.1466`, delta_test=`6.736`, delta_PF=`0.0201`
  - `2407`: test=`11.506`, PF=`1.0529`, holdout_b=`-6.696`, holdout_b_PF=`0.8622`, delta_test=`1.562`, delta_PF=`0.0164`
  - `2501`: test=`51.542`, PF=`1.3005`, holdout_b=`0.498`, holdout_b_PF=`1.0095`, delta_test=`2.452`, delta_PF=`0.0323`

- [4] `11C` `monday_070_post060`: target_holdout_b=`-6.758`, target_holdout_b_PF=`0.8572`, min_holdout_b=`-6.758`, avg_test=`22.267`, positive_test_windows=`3/3`, positive_holdout_b_windows=`2/3`
  - `2401`: test=`2.942`, PF=`1.0093`, holdout_b=`11.616`, holdout_b_PF=`1.1470`, delta_test=`7.524`, delta_PF=`0.0227`
  - `2407`: test=`10.936`, PF=`1.0517`, holdout_b=`-6.758`, holdout_b_PF=`0.8572`, delta_test=`0.992`, delta_PF=`0.0152`
  - `2501`: test=`52.922`, PF=`1.3113`, holdout_b=`0.730`, holdout_b_PF=`1.0139`, delta_test=`3.832`, delta_PF=`0.0431`

- [5] `11F` `monday_070_post070`: target_holdout_b=`-6.822`, target_holdout_b_PF=`0.8625`, min_holdout_b=`-6.822`, avg_test=`20.703`, positive_test_windows=`3/3`, positive_holdout_b_windows=`2/3`
  - `2401`: test=`0.370`, PF=`1.0012`, holdout_b=`10.522`, holdout_b_PF=`1.1339`, delta_test=`4.952`, delta_PF=`0.0145`
  - `2407`: test=`10.436`, PF=`1.0470`, holdout_b=`-6.822`, holdout_b_PF=`0.8625`, delta_test=`0.492`, delta_PF=`0.0105`
  - `2501`: test=`51.302`, PF=`1.2981`, holdout_b=`0.364`, holdout_b_PF=`1.0070`, delta_test=`2.212`, delta_PF=`0.0298`

- [6] `11E` `monday_075_post065`: target_holdout_b=`-7.044`, target_holdout_b_PF=`0.8612`, min_holdout_b=`-7.044`, avg_test=`22.443`, positive_test_windows=`3/3`, positive_holdout_b_windows=`2/3`
  - `2401`: test=`1.674`, PF=`1.0052`, holdout_b=`11.118`, holdout_b_PF=`1.1389`, delta_test=`6.256`, delta_PF=`0.0186`
  - `2407`: test=`13.222`, PF=`1.0596`, holdout_b=`-7.044`, holdout_b_PF=`0.8612`, delta_test=`3.278`, delta_PF=`0.0231`
  - `2501`: test=`52.434`, PF=`1.3045`, holdout_b=`1.070`, holdout_b_PF=`1.0203`, delta_test=`3.344`, delta_PF=`0.0363`

## Readout

- overlay leader: `11B` `monday_065_post065`
- target 2407 holdout_b: `-6.498`
- vs 09C target delta: `2.566`
