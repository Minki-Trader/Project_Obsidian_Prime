# Stage 17 09C Directional Core Fork Review

- windows: `2401, 2407, 2501`
- source core: `09C_05ET_margin0700_t30_l50_m0700_h4`
- target: `2407 / holdout_b`
- ranking basis: `positive_test_windows -> positive_holdout_b_windows -> avg_test_return -> min_holdout_b -> avg_test_pf -> min_test`

## Candidate Ranking

- [1] `17E` `09C_ovr_balanced`: avg_test=`29.141`, min_test=`23.282`, target_holdout_b=`-5.998`, target_holdout_b_PF=`0.6786`, min_holdout_b=`-5.998`, positive_test_windows=`3/3`, positive_holdout_b_windows=`2/3`
  - rationale: `Use balanced one-vs-rest direction specialists to test whether separate directional margins survive shifted windows better.`
  - classifier_kind: `ovr`, class_weight: `"balanced"`
  - `2401`: validation=`29.186`, test=`23.282`, PF=`1.1437`, holdout_b=`19.366`, holdout_b_PF=`1.4295`
  - `2407`: validation=`54.782`, test=`25.798`, PF=`1.3340`, holdout_b=`-5.998`, holdout_b_PF=`0.6786`
  - `2501`: validation=`-9.092`, test=`38.344`, PF=`1.4997`, holdout_b=`4.704`, holdout_b_PF=`1.2327`

- [2] `17A` `09C_reference_balanced`: avg_test=`18.151`, min_test=`-4.582`, target_holdout_b=`-9.064`, target_holdout_b_PF=`0.8558`, min_holdout_b=`-9.064`, positive_test_windows=`2/3`, positive_holdout_b_windows=`2/3`
  - rationale: `Reference 09C trend-proxy multinomial logistic with balanced class weights.`
  - classifier_kind: `multinomial`, class_weight: `"balanced"`
  - `2401`: validation=`-1.918`, test=`-4.582`, PF=`0.9866`, holdout_b=`8.112`, holdout_b_PF=`1.0953`
  - `2407`: validation=`23.612`, test=`9.944`, PF=`1.0365`, holdout_b=`-9.064`, holdout_b_PF=`0.8558`
  - `2501`: validation=`2.118`, test=`49.090`, PF=`1.2682`, holdout_b=`1.722`, holdout_b_PF=`1.0313`

- [3] `17D` `09C_flat_guard`: avg_test=`3.726`, min_test=`-9.060`, target_holdout_b=`1.212`, target_holdout_b_PF=`5.7344`, min_holdout_b=`-4.136`, positive_test_windows=`2/3`, positive_holdout_b_windows=`1/3`
  - rationale: `Push more uncertain bars into flat globally to test whether abstention is the missing core edge.`
  - classifier_kind: `multinomial`, class_weight: `{"0": 1.0, "1": 1.45, "2": 1.0}`
  - `2401`: validation=`26.720`, test=`18.100`, PF=`1.1498`, holdout_b=`-3.410`, holdout_b_PF=`0.8988`
  - `2407`: validation=`-20.872`, test=`-9.060`, PF=`0.9008`, holdout_b=`1.212`, holdout_b_PF=`5.7344`
  - `2501`: validation=`-9.086`, test=`2.138`, PF=`1.0691`, holdout_b=`-4.136`, holdout_b_PF=`0.7153`

- [4] `17C` `09C_short_specialist`: avg_test=`6.327`, min_test=`-6.078`, target_holdout_b=`5.138`, target_holdout_b_PF=`1.1585`, min_holdout_b=`-7.702`, positive_test_windows=`1/3`, positive_holdout_b_windows=`2/3`
  - rationale: `Sharpen genuine short separation by boosting the short class and relaxing long slightly.`
  - classifier_kind: `multinomial`, class_weight: `{"0": 1.35, "1": 1.0, "2": 0.95}`
  - `2401`: validation=`0.474`, test=`-6.078`, PF=`0.9798`, holdout_b=`1.144`, holdout_b_PF=`1.0148`
  - `2407`: validation=`0.160`, test=`27.200`, PF=`1.1149`, holdout_b=`5.138`, holdout_b_PF=`1.1585`
  - `2501`: validation=`-19.796`, test=`-2.140`, PF=`0.9821`, holdout_b=`-7.702`, holdout_b_PF=`0.7931`

- [5] `17B` `09C_short_guard`: avg_test=`-0.685`, min_test=`-12.634`, target_holdout_b=`-0.254`, target_holdout_b_PF=`0.0797`, min_holdout_b=`-8.096`, positive_test_windows=`1/3`, positive_holdout_b_windows=`0/3`
  - rationale: `Reduce marginal shorts by lifting flat weight and slightly lowering short urgency.`
  - classifier_kind: `multinomial`, class_weight: `{"0": 0.85, "1": 1.35, "2": 1.0}`
  - `2401`: validation=`9.628`, test=`-12.634`, PF=`0.8827`, holdout_b=`-8.096`, holdout_b_PF=`0.7742`
  - `2407`: validation=`-10.298`, test=`-4.860`, PF=`0.9424`, holdout_b=`-0.254`, holdout_b_PF=`0.0797`
  - `2501`: validation=`-11.328`, test=`15.438`, PF=`1.5761`, holdout_b=`-1.696`, holdout_b_PF=`0.8952`

## Readout

- directional-core leader: `17E` `09C_ovr_balanced`
- leader avg test return: `29.141`
- leader min holdout_b: `-5.998`
- leader target 2407 holdout_b: `-5.998`
- total runs captured: `15`
