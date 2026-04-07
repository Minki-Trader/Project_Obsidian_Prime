# Stage 12 09C Overlay Fine Probe Review

- source core: `09C_05ET_margin0700_t30_l50_m0700_h4`
- source target 2407 holdout_b: `-9.064`
- source avg test return: `18.151`
- ranking basis: `2407 holdout_b return_pct -> min holdout_b return_pct -> avg test return_pct -> avg test PF`

## Variant Ranking

- [1] `12B` `monday_0.600_post_00625`: target_holdout_b=`-5.892`, target_holdout_b_PF=`0.8795`, min_holdout_b=`-5.892`, avg_test=`23.538`, positive_test_windows=`3/3`, positive_holdout_b_windows=`2/3`
  - `2401`: test=`2.142`, PF=`1.0069`, holdout_b=`12.182`, holdout_b_PF=`1.1586`, delta_test=`6.724`, delta_PF=`0.0203`
  - `2407`: test=`17.766`, PF=`1.0819`, holdout_b=`-5.892`, holdout_b_PF=`0.8795`, delta_test=`7.822`, delta_PF=`0.0453`
  - `2501`: test=`50.706`, PF=`1.3006`, holdout_b=`0.232`, holdout_b_PF=`1.0046`, delta_test=`1.616`, delta_PF=`0.0324`

- [2] `12C` `monday_0.600_post_0.650`: target_holdout_b=`-6.104`, target_holdout_b_PF=`0.8746`, min_holdout_b=`-6.104`, avg_test=`22.367`, positive_test_windows=`3/3`, positive_holdout_b_windows=`2/3`
  - `2401`: test=`1.240`, PF=`1.0040`, holdout_b=`11.904`, holdout_b_PF=`1.1569`, delta_test=`5.822`, delta_PF=`0.0174`
  - `2407`: test=`15.156`, PF=`1.0699`, holdout_b=`-6.104`, holdout_b_PF=`0.8746`, delta_test=`5.212`, delta_PF=`0.0334`
  - `2501`: test=`50.706`, PF=`1.2999`, holdout_b=`0.086`, holdout_b_PF=`1.0017`, delta_test=`1.616`, delta_PF=`0.0317`

- [3] `12A` `monday_0.600_post_0.600`: target_holdout_b=`-6.186`, target_holdout_b_PF=`0.8718`, min_holdout_b=`-6.186`, avg_test=`24.219`, positive_test_windows=`3/3`, positive_holdout_b_windows=`1/3`
  - `2401`: test=`3.944`, PF=`1.0127`, holdout_b=`12.312`, holdout_b_PF=`1.1606`, delta_test=`8.526`, delta_PF=`0.0261`
  - `2407`: test=`17.388`, PF=`1.0813`, holdout_b=`-6.186`, holdout_b_PF=`0.8718`, delta_test=`7.444`, delta_PF=`0.0448`
  - `2501`: test=`51.324`, PF=`1.3057`, holdout_b=`-0.044`, holdout_b_PF=`0.9991`, delta_test=`2.234`, delta_PF=`0.0375`

- [4] `12D` `monday_00625_post_0.600`: target_holdout_b=`-6.192`, target_holdout_b_PF=`0.8722`, min_holdout_b=`-6.192`, avg_test=`24.452`, positive_test_windows=`3/3`, positive_holdout_b_windows=`2/3`
  - `2401`: test=`4.130`, PF=`1.0133`, holdout_b=`12.042`, holdout_b_PF=`1.1554`, delta_test=`8.712`, delta_PF=`0.0266`
  - `2407`: test=`17.208`, PF=`1.0802`, holdout_b=`-6.192`, holdout_b_PF=`0.8722`, delta_test=`7.264`, delta_PF=`0.0437`
  - `2501`: test=`52.018`, PF=`1.3087`, holdout_b=`0.150`, holdout_b_PF=`1.0029`, delta_test=`2.928`, delta_PF=`0.0405`

- [5] `12E` `monday_00625_post_00625`: target_holdout_b=`-6.216`, target_holdout_b_PF=`0.8734`, min_holdout_b=`-6.216`, avg_test=`23.317`, positive_test_windows=`3/3`, positive_holdout_b_windows=`2/3`
  - `2401`: test=`1.716`, PF=`1.0055`, holdout_b=`11.888`, holdout_b_PF=`1.1537`, delta_test=`6.298`, delta_PF=`0.0189`
  - `2407`: test=`17.232`, PF=`1.0792`, holdout_b=`-6.216`, holdout_b_PF=`0.8734`, delta_test=`7.288`, delta_PF=`0.0427`
  - `2501`: test=`51.002`, PF=`1.3006`, holdout_b=`0.432`, holdout_b_PF=`1.0084`, delta_test=`1.912`, delta_PF=`0.0324`

- [6] `12F` `monday_00625_post_0.650`: target_holdout_b=`-6.278`, target_holdout_b_PF=`0.8716`, min_holdout_b=`-6.278`, avg_test=`22.451`, positive_test_windows=`3/3`, positive_holdout_b_windows=`2/3`
  - `2401`: test=`1.454`, PF=`1.0047`, holdout_b=`12.170`, holdout_b_PF=`1.1585`, delta_test=`6.036`, delta_PF=`0.0180`
  - `2407`: test=`14.550`, PF=`1.0668`, holdout_b=`-6.278`, holdout_b_PF=`0.8716`, delta_test=`4.606`, delta_PF=`0.0303`
  - `2501`: test=`51.348`, PF=`1.3024`, holdout_b=`0.316`, holdout_b_PF=`1.0062`, delta_test=`2.258`, delta_PF=`0.0342`

- [7] `12H` `monday_0.650_post_00625`: target_holdout_b=`-6.402`, target_holdout_b_PF=`0.8698`, min_holdout_b=`-6.402`, avg_test=`23.676`, positive_test_windows=`3/3`, positive_holdout_b_windows=`2/3`
  - `2401`: test=`2.762`, PF=`1.0088`, holdout_b=`11.984`, holdout_b_PF=`1.1541`, delta_test=`7.344`, delta_PF=`0.0222`
  - `2407`: test=`16.882`, PF=`1.0774`, holdout_b=`-6.402`, holdout_b_PF=`0.8698`, delta_test=`6.938`, delta_PF=`0.0409`
  - `2501`: test=`51.384`, PF=`1.3018`, holdout_b=`0.750`, holdout_b_PF=`1.0145`, delta_test=`2.294`, delta_PF=`0.0336`

- [8] `12I` `monday_0.650_post_0.650`: target_holdout_b=`-6.498`, target_holdout_b_PF=`0.8689`, min_holdout_b=`-6.498`, avg_test=`22.681`, positive_test_windows=`3/3`, positive_holdout_b_windows=`2/3`
  - `2401`: test=`2.100`, PF=`1.0067`, holdout_b=`12.066`, holdout_b_PF=`1.1555`, delta_test=`6.682`, delta_PF=`0.0200`
  - `2407`: test=`14.554`, PF=`1.0665`, holdout_b=`-6.498`, holdout_b_PF=`0.8689`, delta_test=`4.610`, delta_PF=`0.0299`
  - `2501`: test=`51.390`, PF=`1.3006`, holdout_b=`0.700`, holdout_b_PF=`1.0135`, delta_test=`2.300`, delta_PF=`0.0324`

- [9] `12G` `monday_0.650_post_0.600`: target_holdout_b=`-6.586`, target_holdout_b_PF=`0.8651`, min_holdout_b=`-6.586`, avg_test=`24.381`, positive_test_windows=`3/3`, positive_holdout_b_windows=`2/3`
  - `2401`: test=`4.142`, PF=`1.0132`, holdout_b=`11.998`, holdout_b_PF=`1.1543`, delta_test=`8.724`, delta_PF=`0.0266`
  - `2407`: test=`16.788`, PF=`1.0780`, holdout_b=`-6.586`, holdout_b_PF=`0.8651`, delta_test=`6.844`, delta_PF=`0.0415`
  - `2501`: test=`52.212`, PF=`1.3089`, holdout_b=`0.514`, holdout_b_PF=`1.0099`, delta_test=`3.122`, delta_PF=`0.0407`

## Readout

- overlay leader: `12B` `monday_0.600_post_00625`
- target 2407 holdout_b: `-5.892`
- vs 09C target delta: `3.172`
