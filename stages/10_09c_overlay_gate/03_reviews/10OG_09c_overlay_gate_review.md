# Stage 10 09C Overlay Gate Review

- source core: `09C_05ET_margin0700_t30_l50_m0700_h4`
- source target 2407 holdout_b: `-9.064`
- source avg test return: `18.151`
- ranking basis: `2407 holdout_b return_pct -> min holdout_b return_pct -> avg test return_pct -> avg test PF`

## Variant Ranking

- [1] `10C` `local_probe_b`: target_holdout_b=`-6.696`, target_holdout_b_PF=`0.8622`, min_holdout_b=`-6.696`, avg_test=`21.734`, positive_test_windows=`3/3`, positive_holdout_b_windows=`2/3`
  - `2401`: test=`2.154`, PF=`1.0068`, holdout_b=`11.568`, holdout_b_PF=`1.1466`, delta_test=`6.736`, delta_PF=`0.0201`
  - `2407`: test=`11.506`, PF=`1.0529`, holdout_b=`-6.696`, holdout_b_PF=`0.8622`, delta_test=`1.562`, delta_PF=`0.0164`
  - `2501`: test=`51.542`, PF=`1.3005`, holdout_b=`0.498`, holdout_b_PF=`1.0095`, delta_test=`2.452`, delta_PF=`0.0323`

- [2] `10A` `soft_decay_reference`: target_holdout_b=`-7.256`, target_holdout_b_PF=`0.8605`, min_holdout_b=`-7.256`, avg_test=`21.999`, positive_test_windows=`3/3`, positive_holdout_b_windows=`2/3`
  - `2401`: test=`0.774`, PF=`1.0024`, holdout_b=`10.290`, holdout_b_PF=`1.1285`, delta_test=`5.356`, delta_PF=`0.0158`
  - `2407`: test=`13.642`, PF=`1.0599`, holdout_b=`-7.256`, holdout_b_PF=`0.8605`, delta_test=`3.698`, delta_PF=`0.0234`
  - `2501`: test=`51.582`, PF=`1.2978`, holdout_b=`0.604`, holdout_b_PF=`1.0115`, delta_test=`2.492`, delta_PF=`0.0296`

- [3] `10B` `local_probe_a`: target_holdout_b=`-7.476`, target_holdout_b_PF=`0.8556`, min_holdout_b=`-7.476`, avg_test=`22.621`, positive_test_windows=`3/3`, positive_holdout_b_windows=`2/3`
  - `2401`: test=`1.970`, PF=`1.0061`, holdout_b=`10.426`, holdout_b_PF=`1.1280`, delta_test=`6.552`, delta_PF=`0.0195`
  - `2407`: test=`13.236`, PF=`1.0591`, holdout_b=`-7.476`, holdout_b_PF=`0.8556`, delta_test=`3.292`, delta_PF=`0.0226`
  - `2501`: test=`52.658`, PF=`1.3045`, holdout_b=`1.088`, holdout_b_PF=`1.0204`, delta_test=`3.568`, delta_PF=`0.0363`

## Readout

- overlay leader: `10C` `local_probe_b`
- target 2407 holdout_b: `-6.696`
- vs 09C target delta: `2.368`
