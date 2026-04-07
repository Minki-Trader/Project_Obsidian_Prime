# Stage 18 Directional Core Overlay Matrix Review

- source stage: `17_09c_directional_core_fork`
- source cores: `17E ovr_balanced`, `17C short_specialist`, `17D flat_guard`
- windows: `2401, 2407, 2501`
- ranking basis: `positive_test_windows -> positive_holdout_b_windows -> avg_test_return -> target_2407_holdout_b -> min_holdout_b -> avg_test_pf`
- total variants: `18`

## Core Leaders

- `17E` `09C_ovr_balanced` -> best `18E` `postcash_hold_cut`: avg_test=`32.863`, target_holdout_b=`-3.282`, min_holdout_b=`-3.282`, positive_test_windows=`3/3`, positive_holdout_b_windows=`2/3`
- `17C` `09C_short_specialist` -> best `18J` `balanced_micro`: avg_test=`10.231`, target_holdout_b=`7.472`, min_holdout_b=`-9.408`, positive_test_windows=`3/3`, positive_holdout_b_windows=`2/3`
- `17D` `09C_flat_guard` -> best `18Q` `postcash_hold_cut`: avg_test=`8.207`, target_holdout_b=`0.550`, min_holdout_b=`-4.224`, positive_test_windows=`2/3`, positive_holdout_b_windows=`2/3`

## Overlay Readout

- `PLAIN20` `plain_core` -> best core `17E`: avg_test=`29.141`, target_holdout_b=`-5.998`, min_holdout_b=`-5.998`
- `SD20` `soft_decay` -> best core `17E`: avg_test=`31.692`, target_holdout_b=`-5.282`, min_holdout_b=`-5.282`
- `LP20` `local_probe_b` -> best core `17E`: avg_test=`31.665`, target_holdout_b=`-5.080`, min_holdout_b=`-5.080`
- `BD20` `balanced_micro` -> best core `17E`: avg_test=`31.439`, target_holdout_b=`-4.648`, min_holdout_b=`-4.648`
- `PH20` `postcash_hold_cut` -> best core `17E`: avg_test=`32.863`, target_holdout_b=`-3.282`, min_holdout_b=`-3.282`
- `CT20` `clock_taper` -> best core `17E`: avg_test=`32.044`, target_holdout_b=`-5.204`, min_holdout_b=`-5.204`

## Variant Ranking

- [1] `18E` `17E + PH20`: avg_test=`32.863`, min_test=`27.700`, target_holdout_b=`-3.282`, min_holdout_b=`-3.282`, avg_test_PF=`1.3892`, positive_test_windows=`3/3`, positive_holdout_b_windows=`2/3`
  - `2401`: test=`32.412`, PF=`1.2205`, holdout_b=`24.702`, holdout_b_PF=`1.6512`, delta_test=`9.130`, delta_PF=`0.0768`
  - `2407`: test=`27.700`, PF=`1.4127`, holdout_b=`-3.282`, holdout_b_PF=`0.7972`, delta_test=`1.902`, delta_PF=`0.0787`
  - `2501`: test=`38.478`, PF=`1.5343`, holdout_b=`0.662`, holdout_b_PF=`1.0342`, delta_test=`0.134`, delta_PF=`0.0346`

- [2] `18F` `17E + CT20`: avg_test=`32.044`, min_test=`27.698`, target_holdout_b=`-5.204`, min_holdout_b=`-5.204`, avg_test_PF=`1.3921`, positive_test_windows=`3/3`, positive_holdout_b_windows=`2/3`
  - `2401`: test=`27.990`, PF=`1.1923`, holdout_b=`20.986`, holdout_b_PF=`1.5309`, delta_test=`4.708`, delta_PF=`0.0485`
  - `2407`: test=`27.698`, PF=`1.4235`, holdout_b=`-5.204`, holdout_b_PF=`0.6681`, delta_test=`1.900`, delta_PF=`0.0896`
  - `2501`: test=`40.444`, PF=`1.5606`, holdout_b=`3.678`, holdout_b_PF=`1.1938`, delta_test=`2.100`, delta_PF=`0.0608`

- [3] `18B` `17E + SD20`: avg_test=`31.692`, min_test=`26.820`, target_holdout_b=`-5.282`, min_holdout_b=`-5.282`, avg_test_PF=`1.3825`, positive_test_windows=`3/3`, positive_holdout_b_windows=`2/3`
  - `2401`: test=`29.150`, PF=`1.2015`, holdout_b=`21.170`, holdout_b_PF=`1.5421`, delta_test=`5.868`, delta_PF=`0.0578`
  - `2407`: test=`26.820`, PF=`1.4046`, holdout_b=`-5.282`, holdout_b_PF=`0.6661`, delta_test=`1.022`, delta_PF=`0.0706`
  - `2501`: test=`39.106`, PF=`1.5414`, holdout_b=`3.052`, holdout_b_PF=`1.1587`, delta_test=`0.762`, delta_PF=`0.0417`

- [4] `18C` `17E + LP20`: avg_test=`31.665`, min_test=`26.404`, target_holdout_b=`-5.080`, min_holdout_b=`-5.080`, avg_test_PF=`1.3891`, positive_test_windows=`3/3`, positive_holdout_b_windows=`2/3`
  - `2401`: test=`29.242`, PF=`1.2073`, holdout_b=`21.352`, holdout_b_PF=`1.5650`, delta_test=`5.960`, delta_PF=`0.0636`
  - `2407`: test=`26.404`, PF=`1.4083`, holdout_b=`-5.080`, holdout_b_PF=`0.6678`, delta_test=`0.606`, delta_PF=`0.0743`
  - `2501`: test=`39.350`, PF=`1.5518`, holdout_b=`3.064`, holdout_b_PF=`1.1620`, delta_test=`1.006`, delta_PF=`0.0520`

- [5] `18D` `17E + BD20`: avg_test=`31.439`, min_test=`26.602`, target_holdout_b=`-4.648`, min_holdout_b=`-4.648`, avg_test_PF=`1.4009`, positive_test_windows=`3/3`, positive_holdout_b_windows=`2/3`
  - `2401`: test=`28.452`, PF=`1.2107`, holdout_b=`21.568`, holdout_b_PF=`1.6104`, delta_test=`5.170`, delta_PF=`0.0670`
  - `2407`: test=`26.602`, PF=`1.4281`, holdout_b=`-4.648`, holdout_b_PF=`0.6785`, delta_test=`0.804`, delta_PF=`0.0941`
  - `2501`: test=`39.262`, PF=`1.5640`, holdout_b=`2.284`, holdout_b_PF=`1.1248`, delta_test=`0.918`, delta_PF=`0.0643`

- [6] `18A` `17E + PLAIN20`: avg_test=`29.141`, min_test=`23.282`, target_holdout_b=`-5.998`, min_holdout_b=`-5.998`, avg_test_PF=`1.3258`, positive_test_windows=`3/3`, positive_holdout_b_windows=`2/3`
  - `2401`: test=`23.282`, PF=`1.1437`, holdout_b=`19.366`, holdout_b_PF=`1.4295`, delta_test=`0.000`, delta_PF=`0.0000`
  - `2407`: test=`25.798`, PF=`1.3340`, holdout_b=`-5.998`, holdout_b_PF=`0.6786`, delta_test=`0.000`, delta_PF=`0.0000`
  - `2501`: test=`38.344`, PF=`1.4997`, holdout_b=`4.704`, holdout_b_PF=`1.2327`, delta_test=`0.000`, delta_PF=`0.0000`

- [7] `18J` `17C + BD20`: avg_test=`10.231`, min_test=`3.732`, target_holdout_b=`7.472`, min_holdout_b=`-9.408`, avg_test_PF=`1.0594`, positive_test_windows=`3/3`, positive_holdout_b_windows=`2/3`
  - `2401`: test=`7.660`, PF=`1.0282`, holdout_b=`3.614`, holdout_b_PF=`1.0535`, delta_test=`13.738`, delta_PF=`0.0485`
  - `2407`: test=`19.302`, PF=`1.1152`, holdout_b=`7.472`, holdout_b_PF=`1.3718`, delta_test=`-7.898`, delta_PF=`0.0003`
  - `2501`: test=`3.732`, PF=`1.0347`, holdout_b=`-9.408`, holdout_b_PF=`0.7111`, delta_test=`5.872`, delta_PF=`0.0526`

- [8] `18K` `17C + PH20`: avg_test=`9.337`, min_test=`0.890`, target_holdout_b=`7.348`, min_holdout_b=`-6.194`, avg_test_PF=`1.0602`, positive_test_windows=`3/3`, positive_holdout_b_windows=`2/3`
  - `2401`: test=`0.890`, PF=`1.0031`, holdout_b=`6.862`, holdout_b_PF=`1.0978`, delta_test=`6.968`, delta_PF=`0.0234`
  - `2407`: test=`17.402`, PF=`1.0906`, holdout_b=`7.348`, holdout_b_PF=`1.2838`, delta_test=`-9.798`, delta_PF=`-0.0243`
  - `2501`: test=`9.720`, PF=`1.0868`, holdout_b=`-6.194`, holdout_b_PF=`0.8155`, delta_test=`11.860`, delta_PF=`0.1047`

- [9] `18I` `17C + LP20`: avg_test=`8.620`, min_test=`2.586`, target_holdout_b=`6.014`, min_holdout_b=`-9.494`, avg_test_PF=`1.0501`, positive_test_windows=`3/3`, positive_holdout_b_windows=`2/3`
  - `2401`: test=`2.586`, PF=`1.0093`, holdout_b=`2.408`, holdout_b_PF=`1.0343`, delta_test=`8.664`, delta_PF=`0.0296`
  - `2407`: test=`20.512`, PF=`1.1158`, holdout_b=`6.014`, holdout_b_PF=`1.2648`, delta_test=`-6.688`, delta_PF=`0.0009`
  - `2501`: test=`2.762`, PF=`1.0252`, holdout_b=`-9.494`, holdout_b_PF=`0.7178`, delta_test=`4.902`, delta_PF=`0.0431`

- [10] `18L` `17C + CT20`: avg_test=`8.482`, min_test=`0.508`, target_holdout_b=`5.774`, min_holdout_b=`-8.850`, avg_test_PF=`1.0479`, positive_test_windows=`3/3`, positive_holdout_b_windows=`2/3`
  - `2401`: test=`0.508`, PF=`1.0018`, holdout_b=`2.060`, holdout_b_PF=`1.0289`, delta_test=`6.586`, delta_PF=`0.0220`
  - `2407`: test=`23.032`, PF=`1.1246`, holdout_b=`5.774`, holdout_b_PF=`1.2368`, delta_test=`-4.168`, delta_PF=`0.0097`
  - `2501`: test=`1.906`, PF=`1.0172`, holdout_b=`-8.850`, holdout_b_PF=`0.7395`, delta_test=`4.046`, delta_PF=`0.0351`

- [11] `18H` `17C + SD20`: avg_test=`8.055`, min_test=`1.390`, target_holdout_b=`5.774`, min_holdout_b=`-8.830`, avg_test_PF=`1.0462`, positive_test_windows=`3/3`, positive_holdout_b_windows=`2/3`
  - `2401`: test=`1.390`, PF=`1.0050`, holdout_b=`1.750`, holdout_b_PF=`1.0245`, delta_test=`7.468`, delta_PF=`0.0252`
  - `2407`: test=`19.976`, PF=`1.1085`, holdout_b=`5.774`, holdout_b_PF=`1.2415`, delta_test=`-7.224`, delta_PF=`-0.0064`
  - `2501`: test=`2.798`, PF=`1.0251`, holdout_b=`-8.830`, holdout_b_PF=`0.7429`, delta_test=`4.938`, delta_PF=`0.0430`

- [12] `18Q` `17D + PH20`: avg_test=`8.207`, min_test=`-2.244`, target_holdout_b=`0.550`, min_holdout_b=`-4.224`, avg_test_PF=`1.0764`, positive_test_windows=`2/3`, positive_holdout_b_windows=`2/3`
  - `2401`: test=`25.950`, PF=`1.2311`, holdout_b=`3.636`, holdout_b_PF=`1.1291`, delta_test=`7.850`, delta_PF=`0.0813`
  - `2407`: test=`-2.244`, PF=`0.9686`, holdout_b=`0.550`, holdout_b_PF=`1.3289`, delta_test=`6.816`, delta_PF=`0.0678`
  - `2501`: test=`0.914`, PF=`1.0297`, holdout_b=`-4.224`, holdout_b_PF=`0.7238`, delta_test=`-1.224`, delta_PF=`-0.0394`

- [13] `18O` `17D + LP20`: avg_test=`4.547`, min_test=`-5.796`, target_holdout_b=`1.196`, min_holdout_b=`-4.268`, avg_test_PF=`1.0610`, positive_test_windows=`2/3`, positive_holdout_b_windows=`1/3`
  - `2401`: test=`16.146`, PF=`1.1543`, holdout_b=`-4.268`, holdout_b_PF=`0.8505`, delta_test=`-1.954`, delta_PF=`0.0045`
  - `2407`: test=`-5.796`, PF=`0.9145`, holdout_b=`1.196`, holdout_b_PF=`5.3333`, delta_test=`3.264`, delta_PF=`0.0137`
  - `2501`: test=`3.290`, PF=`1.1142`, holdout_b=`-3.146`, holdout_b_PF=`0.7688`, delta_test=`1.152`, delta_PF=`0.0451`

- [14] `18P` `17D + BD20`: avg_test=`4.439`, min_test=`-5.058`, target_holdout_b=`1.162`, min_holdout_b=`-4.188`, avg_test_PF=`1.0641`, positive_test_windows=`2/3`, positive_holdout_b_windows=`1/3`
  - `2401`: test=`14.808`, PF=`1.1461`, holdout_b=`-4.188`, holdout_b_PF=`0.8491`, delta_test=`-3.292`, delta_PF=`-0.0037`
  - `2407`: test=`-5.058`, PF=`0.9209`, holdout_b=`1.162`, holdout_b_PF=`5.2101`, delta_test=`4.002`, delta_PF=`0.0202`
  - `2501`: test=`3.568`, PF=`1.1252`, holdout_b=`-3.158`, holdout_b_PF=`0.7677`, delta_test=`1.430`, delta_PF=`0.0561`

- [15] `18N` `17D + SD20`: avg_test=`4.257`, min_test=`-7.234`, target_holdout_b=`1.230`, min_holdout_b=`-3.598`, avg_test_PF=`1.0543`, positive_test_windows=`2/3`, positive_holdout_b_windows=`1/3`
  - `2401`: test=`16.852`, PF=`1.1578`, holdout_b=`-3.598`, holdout_b_PF=`0.8765`, delta_test=`-1.248`, delta_PF=`0.0080`
  - `2407`: test=`-7.234`, PF=`0.8972`, holdout_b=`1.230`, holdout_b_PF=`5.4565`, delta_test=`1.826`, delta_PF=`-0.0035`
  - `2501`: test=`3.152`, PF=`1.1079`, holdout_b=`-3.342`, holdout_b_PF=`0.7591`, delta_test=`1.014`, delta_PF=`0.0389`

- [16] `18R` `17D + CT20`: avg_test=`3.913`, min_test=`-7.796`, target_holdout_b=`1.020`, min_holdout_b=`-4.074`, avg_test_PF=`1.0524`, positive_test_windows=`2/3`, positive_holdout_b_windows=`1/3`
  - `2401`: test=`16.050`, PF=`1.1491`, holdout_b=`-4.074`, holdout_b_PF=`0.8628`, delta_test=`-2.050`, delta_PF=`-0.0007`
  - `2407`: test=`-7.796`, PF=`0.8875`, holdout_b=`1.020`, holdout_b_PF=`5.3220`, delta_test=`1.264`, delta_PF=`-0.0132`
  - `2501`: test=`3.486`, PF=`1.1207`, holdout_b=`-3.166`, holdout_b_PF=`0.7676`, delta_test=`1.348`, delta_PF=`0.0517`

- [17] `18M` `17D + PLAIN20`: avg_test=`3.726`, min_test=`-9.060`, target_holdout_b=`1.212`, min_holdout_b=`-4.136`, avg_test_PF=`1.0399`, positive_test_windows=`2/3`, positive_holdout_b_windows=`1/3`
  - `2401`: test=`18.100`, PF=`1.1498`, holdout_b=`-3.410`, holdout_b_PF=`0.8988`, delta_test=`0.000`, delta_PF=`0.0000`
  - `2407`: test=`-9.060`, PF=`0.9008`, holdout_b=`1.212`, holdout_b_PF=`5.7344`, delta_test=`0.000`, delta_PF=`0.0000`
  - `2501`: test=`2.138`, PF=`1.0691`, holdout_b=`-4.136`, holdout_b_PF=`0.7153`, delta_test=`0.000`, delta_PF=`0.0000`

- [18] `18G` `17C + PLAIN20`: avg_test=`6.327`, min_test=`-6.078`, target_holdout_b=`5.138`, min_holdout_b=`-7.702`, avg_test_PF=`1.0256`, positive_test_windows=`1/3`, positive_holdout_b_windows=`2/3`
  - `2401`: test=`-6.078`, PF=`0.9798`, holdout_b=`1.144`, holdout_b_PF=`1.0148`, delta_test=`0.000`, delta_PF=`0.0000`
  - `2407`: test=`27.200`, PF=`1.1149`, holdout_b=`5.138`, holdout_b_PF=`1.1585`, delta_test=`0.000`, delta_PF=`0.0000`
  - `2501`: test=`-2.140`, PF=`0.9821`, holdout_b=`-7.702`, holdout_b_PF=`0.7931`, delta_test=`0.000`, delta_PF=`0.0000`

## Readout

- overall leader: `18E` `17E + PH20`
- leader avg_test: `32.863`
- leader target_2407_holdout_b: `-3.282`
- leader min_holdout_b: `-3.282`
