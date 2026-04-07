# Stage 13 09C Overlay Micro Probe Review

- source core: `09C_05ET_margin0700_t30_l50_m0700_h4`
- source target 2407 holdout_b: `-9.064`
- source avg test return: `18.151`
- ranking basis: `2407 holdout_b return_pct -> min holdout_b return_pct -> avg test return_pct -> avg test PF`

## Variant Ranking

- [1] `13C` `monday_0.550_post_0.6375`: target_holdout_b=`-5.462`, target_holdout_b_PF=`0.8865`, min_holdout_b=`-5.462`, avg_test=`23.016`, positive_test_windows=`3/3`, positive_holdout_b_windows=`1/3`
  - `2401`: test=`1.316`, PF=`1.0043`, holdout_b=`12.580`, holdout_b_PF=`1.1683`, delta_test=`5.898`, delta_PF=`0.0177`
  - `2407`: test=`17.970`, PF=`1.0832`, holdout_b=`-5.462`, holdout_b_PF=`0.8865`, delta_test=`8.026`, delta_PF=`0.0467`
  - `2501`: test=`49.762`, PF=`1.2968`, holdout_b=`-0.282`, holdout_b_PF=`0.9944`, delta_test=`0.672`, delta_PF=`0.0286`

- [2] `13F` `monday_0.575_post_0.6375`: target_holdout_b=`-5.586`, target_holdout_b_PF=`0.8852`, min_holdout_b=`-5.586`, avg_test=`23.135`, positive_test_windows=`3/3`, positive_holdout_b_windows=`1/3`
  - `2401`: test=`1.654`, PF=`1.0054`, holdout_b=`12.422`, holdout_b_PF=`1.1650`, delta_test=`6.236`, delta_PF=`0.0187`
  - `2407`: test=`17.780`, PF=`1.0820`, holdout_b=`-5.586`, holdout_b_PF=`0.8852`, delta_test=`7.836`, delta_PF=`0.0455`
  - `2501`: test=`49.972`, PF=`1.2971`, holdout_b=`-0.156`, holdout_b_PF=`0.9969`, delta_test=`0.882`, delta_PF=`0.0289`

- [3] `13A` `monday_0.550_post_0.6125`: target_holdout_b=`-5.650`, target_holdout_b_PF=`0.8815`, min_holdout_b=`-5.650`, avg_test=`24.356`, positive_test_windows=`3/3`, positive_holdout_b_windows=`1/3`
  - `2401`: test=`2.968`, PF=`1.0097`, holdout_b=`12.436`, holdout_b_PF=`1.1653`, delta_test=`7.550`, delta_PF=`0.0231`
  - `2407`: test=`18.976`, PF=`1.0893`, holdout_b=`-5.650`, holdout_b_PF=`0.8815`, delta_test=`9.032`, delta_PF=`0.0528`
  - `2501`: test=`51.124`, PF=`1.3048`, holdout_b=`-0.098`, holdout_b_PF=`0.9981`, delta_test=`2.034`, delta_PF=`0.0366`

- [4] `13B` `monday_0.550_post_0.625`: target_holdout_b=`-5.710`, target_holdout_b_PF=`0.8815`, min_holdout_b=`-5.710`, avg_test=`23.143`, positive_test_windows=`3/3`, positive_holdout_b_windows=`1/3`
  - `2401`: test=`1.482`, PF=`1.0049`, holdout_b=`12.332`, holdout_b_PF=`1.1645`, delta_test=`6.064`, delta_PF=`0.0182`
  - `2407`: test=`18.468`, PF=`1.0859`, holdout_b=`-5.710`, holdout_b_PF=`0.8815`, delta_test=`8.524`, delta_PF=`0.0494`
  - `2501`: test=`49.478`, PF=`1.2957`, holdout_b=`-0.754`, holdout_b_PF=`0.9850`, delta_test=`0.388`, delta_PF=`0.0275`

- [5] `13D` `monday_0.575_post_0.6125`: target_holdout_b=`-5.768`, target_holdout_b_PF=`0.8802`, min_holdout_b=`-5.768`, avg_test=`24.554`, positive_test_windows=`3/3`, positive_holdout_b_windows=`2/3`
  - `2401`: test=`2.886`, PF=`1.0094`, holdout_b=`12.494`, holdout_b_PF=`1.1645`, delta_test=`7.468`, delta_PF=`0.0227`
  - `2407`: test=`18.792`, PF=`1.0879`, holdout_b=`-5.768`, holdout_b_PF=`0.8802`, delta_test=`8.848`, delta_PF=`0.0514`
  - `2501`: test=`51.984`, PF=`1.3089`, holdout_b=`0.576`, holdout_b_PF=`1.0113`, delta_test=`2.894`, delta_PF=`0.0407`

- [6] `13G` `monday_0.600_post_0.6125`: target_holdout_b=`-5.856`, target_holdout_b_PF=`0.8789`, min_holdout_b=`-5.856`, avg_test=`24.223`, positive_test_windows=`3/3`, positive_holdout_b_windows=`2/3`
  - `2401`: test=`2.852`, PF=`1.0092`, holdout_b=`12.296`, holdout_b_PF=`1.1603`, delta_test=`7.434`, delta_PF=`0.0225`
  - `2407`: test=`17.882`, PF=`1.0834`, holdout_b=`-5.856`, holdout_b_PF=`0.8789`, delta_test=`7.938`, delta_PF=`0.0469`
  - `2501`: test=`51.934`, PF=`1.3084`, holdout_b=`0.504`, holdout_b_PF=`1.0099`, delta_test=`2.844`, delta_PF=`0.0402`

- [7] `13H` `monday_0.600_post_0.625`: target_holdout_b=`-5.892`, target_holdout_b_PF=`0.8795`, min_holdout_b=`-5.892`, avg_test=`23.538`, positive_test_windows=`3/3`, positive_holdout_b_windows=`2/3`
  - `2401`: test=`2.142`, PF=`1.0069`, holdout_b=`12.182`, holdout_b_PF=`1.1586`, delta_test=`6.724`, delta_PF=`0.0203`
  - `2407`: test=`17.766`, PF=`1.0819`, holdout_b=`-5.892`, holdout_b_PF=`0.8795`, delta_test=`7.822`, delta_PF=`0.0453`
  - `2501`: test=`50.706`, PF=`1.3006`, holdout_b=`0.232`, holdout_b_PF=`1.0046`, delta_test=`1.616`, delta_PF=`0.0324`

- [8] `13I` `monday_0.600_post_0.6375`: target_holdout_b=`-6.138`, target_holdout_b_PF=`0.8746`, min_holdout_b=`-6.138`, avg_test=`22.841`, positive_test_windows=`3/3`, positive_holdout_b_windows=`1/3`
  - `2401`: test=`1.684`, PF=`1.0054`, holdout_b=`12.040`, holdout_b_PF=`1.1580`, delta_test=`6.266`, delta_PF=`0.0188`
  - `2407`: test=`16.684`, PF=`1.0767`, holdout_b=`-6.138`, holdout_b_PF=`0.8746`, delta_test=`6.740`, delta_PF=`0.0402`
  - `2501`: test=`50.156`, PF=`1.2978`, holdout_b=`-0.032`, holdout_b_PF=`0.9994`, delta_test=`1.066`, delta_PF=`0.0296`

- [9] `13E` `monday_0.575_post_0.625`: target_holdout_b=`-6.262`, target_holdout_b_PF=`0.8711`, min_holdout_b=`-6.262`, avg_test=`23.847`, positive_test_windows=`3/3`, positive_holdout_b_windows=`2/3`
  - `2401`: test=`3.602`, PF=`1.0116`, holdout_b=`12.388`, holdout_b_PF=`1.1629`, delta_test=`8.184`, delta_PF=`0.0250`
  - `2407`: test=`17.248`, PF=`1.0800`, holdout_b=`-6.262`, holdout_b_PF=`0.8711`, delta_test=`7.304`, delta_PF=`0.0435`
  - `2501`: test=`50.690`, PF=`1.3008`, holdout_b=`0.206`, holdout_b_PF=`1.0040`, delta_test=`1.600`, delta_PF=`0.0326`

## Readout

- overlay leader: `13C` `monday_0.550_post_0.6375`
- target 2407 holdout_b: `-5.462`
- vs 09C target delta: `3.602`
