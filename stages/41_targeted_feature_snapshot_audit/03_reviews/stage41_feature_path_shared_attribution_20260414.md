# Stage 41 Shared Feature-Path Attribution

- reviewed_on_utc: `2026-04-14T11:17:27.821980+00:00`
- sampled snapshot rows: `121`
- decision diffs: `32`
- trade action diffs: `56`
- checksum diffs: `121`

## Executive Read

- the sampled latest-window built-in-versus-contract drift is dominated by shared ATR-path changes rather than family-specific rule behavior
- contract-aligned snapshots systematically push probability mass toward `p_flat`, while both directional probabilities usually weaken
- in the sampled rows, most decision changes were `directional -> NO_TRADE`, which is consistent with the shared headline drop already observed on the corrected Stage 39 A/B read

## Sample Batches

- `batch_a` `2026.03.02 16:35:00` -> `2026.03.09 20:30:00` `rows=72` `decision_diffs=22` `trade_action_diffs=38`
- `batch_b` `2026.03.12 18:40:00` -> `2026.04.07 20:50:00` `rows=49` `decision_diffs=10` `trade_action_diffs=18`

## Probability Drift

- `p_short_delta_contract_minus_builtin` `mean=-0.014106` `p10=-0.033251` `p90=0.005291` `min=-0.040017` `max=0.019510`
- `p_flat_delta_contract_minus_builtin` `mean=0.037305` `p10=-0.035703` `p90=0.088140` `min=-0.071852` `max=0.104510`
- `p_long_delta_contract_minus_builtin` `mean=-0.023199` `p10=-0.059136` `p90=0.028932` `min=-0.065187` `max=0.052341`

## Decision Transitions

- `same` `count=89`
- `long_to_no_trade` `count=15`
- `short_to_no_trade` `count=11`
- `no_trade_to_long` `count=5`
- `no_trade_to_short` `count=1`

## Top Feature Diffs

- `atr_14` `count=121` `mean_abs=5.238909` `p90_abs=11.579925` `max_abs=21.265421` `mean_signed_contract_minus_builtin=-0.995690`
- `atr_50` `count=121` `mean_abs=5.626953` `p90_abs=8.778549` `max_abs=12.523219` `mean_signed_contract_minus_builtin=-5.566246`
- `stoch_kd_diff` `count=121` `mean_abs=0.389416` `p90_abs=0.882565` `max_abs=5.606089` `mean_signed_contract_minus_builtin=0.011039`
- `bb_squeeze` `count=121` `mean_abs=0.016529` `p90_abs=0.000000` `max_abs=1.000000` `mean_signed_contract_minus_builtin=0.016529`
- `atr_14_over_atr_50` `count=121` `mean_abs=0.200698` `p90_abs=0.280809` `max_abs=0.376204` `mean_signed_contract_minus_builtin=0.106231`
- `return_1_over_atr_14` `count=121` `mean_abs=0.041103` `p90_abs=0.109663` `max_abs=0.258118` `mean_signed_contract_minus_builtin=-0.000757`
- `aapl_xnas_log_return_1` `count=121` `mean_abs=0.000000` `p90_abs=0.000000` `max_abs=0.000000` `mean_signed_contract_minus_builtin=0.000000`
- `amzn_xnas_log_return_1` `count=121` `mean_abs=0.000000` `p90_abs=0.000000` `max_abs=0.000000` `mean_signed_contract_minus_builtin=0.000000`
- `bb_position_20` `count=121` `mean_abs=0.000000` `p90_abs=0.000000` `max_abs=0.000000` `mean_signed_contract_minus_builtin=0.000000`
- `bollinger_width_20` `count=121` `mean_abs=0.000000` `p90_abs=0.000000` `max_abs=0.000000` `mean_signed_contract_minus_builtin=0.000000`

## Largest Feature-Drift Rows

- `2026.03.03 17:40:00` `SHORT -> SHORT` `max_feature_abs_diff=21.265421` `top=atr_14=-21.265421; atr_50=-1.953970; atr_14_over_atr_50=-0.376204`
- `2026.03.03 17:35:00` `SHORT -> NO_TRADE` `max_feature_abs_diff=18.564409` `top=atr_14=-18.564409; atr_50=-1.758766; stoch_kd_diff=-0.358085`
- `2026.03.03 17:45:00` `SHORT -> NO_TRADE` `max_feature_abs_diff=18.027329` `top=atr_14=-18.027329; atr_50=-2.372071; atr_14_over_atr_50=-0.294388`
- `2026.03.02 17:30:00` `NO_TRADE -> LONG` `max_feature_abs_diff=17.896037` `top=atr_14=-17.896037; atr_50=-2.081257; atr_14_over_atr_50=-0.359143`
- `2026.03.03 17:30:00` `SHORT -> NO_TRADE` `max_feature_abs_diff=17.533375` `top=atr_14=-17.533375; atr_50=-2.748353; stoch_kd_diff=-0.440966`
- `2026.03.03 17:25:00` `SHORT -> NO_TRADE` `max_feature_abs_diff=15.424403` `top=atr_14=-15.424403; atr_50=-2.849360; stoch_kd_diff=0.347742`
- `2026.03.02 17:25:00` `NO_TRADE -> LONG` `max_feature_abs_diff=15.221556` `top=atr_14=-15.221556; atr_50=-1.783099; atr_14_over_atr_50=-0.312197`
- `2026.03.09 17:55:00` `NO_TRADE -> LONG` `max_feature_abs_diff=14.967541` `top=atr_14=-14.967541; atr_50=-0.466790; stoch_kd_diff=0.317157`
- `2026.03.09 18:00:00` `NO_TRADE -> LONG` `max_feature_abs_diff=14.350217` `top=atr_14=-14.350217; atr_50=-0.673634; atr_14_over_atr_50=-0.280809`
- `2026.03.09 18:05:00` `NO_TRADE -> NO_TRADE` `max_feature_abs_diff=14.280304` `top=atr_14=-14.280304; atr_50=-0.799942; atr_14_over_atr_50=-0.276426`
- `2026.03.03 17:20:00` `SHORT -> NO_TRADE` `max_feature_abs_diff=13.610072` `top=atr_14=-13.610072; atr_50=-2.499734; stoch_kd_diff=0.383325`
- `2026.03.02 17:20:00` `NO_TRADE -> NO_TRADE` `max_feature_abs_diff=12.578983` `top=atr_14=-12.578983; atr_50=-1.367530; atr_14_over_atr_50=-0.266589`

## Decision-Diff Rows

- `2026.03.09 20:00:00` `LONG -> NO_TRADE` `reason=LONG_FILTERS_OK -> THRESHOLD_FAIL` `d_p_short=-0.033936` `d_p_flat=0.098612` `d_p_long=-0.064676` `top=atr_50=-7.560393; atr_14=4.294144; stoch_kd_diff=-0.297053`
- `2026.03.09 20:20:00` `LONG -> NO_TRADE` `reason=LONG_FILTERS_OK -> LONG_MARGIN_FAIL` `d_p_short=-0.037696` `d_p_flat=0.096253` `d_p_long=-0.058558` `top=atr_50=-8.450065; atr_14=3.284457; atr_14_over_atr_50=0.215949`
- `2026.03.09 20:05:00` `LONG -> NO_TRADE` `reason=LONG_FILTERS_OK -> LONG_MARGIN_FAIL` `d_p_short=-0.033251` `d_p_flat=0.095557` `d_p_long=-0.062306` `top=atr_50=-7.750225; atr_14=4.402215; stoch_kd_diff=-0.587595`
- `2026.03.03 19:30:00` `LONG -> NO_TRADE` `reason=DUAL_SIGNAL_LONG_WINS -> DUAL_SIGNAL_TIE_OR_MARGIN_FAIL` `d_p_short=-0.028131` `d_p_flat=0.086292` `d_p_long=-0.058162` `top=atr_50=-9.225245; atr_14=4.346793; atr_14_over_atr_50=0.244520`
- `2026.03.09 19:15:00` `LONG -> NO_TRADE` `reason=LONG_FILTERS_OK -> LONG_MARGIN_FAIL` `d_p_short=-0.026609` `d_p_flat=0.085346` `d_p_long=-0.058737` `top=atr_14=8.155932; atr_50=-4.544396; atr_14_over_atr_50=0.259008`
- `2026.03.09 19:10:00` `LONG -> NO_TRADE` `reason=LONG_FILTERS_OK -> LONG_MARGIN_FAIL` `d_p_short=-0.024074` `d_p_flat=0.083471` `d_p_long=-0.059398` `top=atr_14=8.470125; atr_50=-4.531139; atr_14_over_atr_50=0.265287`
- `2026.03.09 19:00:00` `LONG -> NO_TRADE` `reason=LONG_FILTERS_OK -> LONG_MARGIN_FAIL` `d_p_short=-0.023049` `d_p_flat=0.080868` `d_p_long=-0.057820` `top=atr_14=9.136527; atr_50=-3.963480; stoch_kd_diff=-0.371385`
- `2026.04.07 20:40:00` `LONG -> NO_TRADE` `reason=LONG_FILTERS_OK -> LONG_MARGIN_FAIL` `d_p_short=-0.019364` `d_p_flat=0.079686` `d_p_long=-0.060322` `top=atr_50=-8.130204; atr_14=6.917266; stoch_kd_diff=-0.341752`
- `2026.04.07 20:15:00` `LONG -> NO_TRADE` `reason=LONG_FILTERS_OK -> LONG_MARGIN_FAIL` `d_p_short=-0.025577` `d_p_flat=0.079307` `d_p_long=-0.053730` `top=atr_50=-7.231562; atr_14=4.961477; stoch_kd_diff=-1.761565`
- `2026.03.03 19:20:00` `LONG -> NO_TRADE` `reason=DUAL_SIGNAL_LONG_WINS -> DUAL_SIGNAL_TIE_OR_MARGIN_FAIL` `d_p_short=-0.020990` `d_p_flat=0.073607` `d_p_long=-0.052617` `top=atr_50=-8.395629; atr_14=5.875993; stoch_kd_diff=0.769909`
- `2026.03.03 19:15:00` `LONG -> NO_TRADE` `reason=DUAL_SIGNAL_LONG_WINS -> DUAL_SIGNAL_TIE_OR_MARGIN_FAIL` `d_p_short=-0.020496` `d_p_flat=0.072156` `d_p_long=-0.051660` `top=atr_50=-7.942908; atr_14=5.222223; stoch_kd_diff=-0.882565`
- `2026.03.09 17:55:00` `NO_TRADE -> LONG` `reason=LONG_MARGIN_FAIL -> LONG_FILTERS_OK` `d_p_short=0.019510` `d_p_flat=-0.071852` `d_p_long=0.052341` `top=atr_14=-14.967541; atr_50=-0.466790; stoch_kd_diff=0.317157`
- `2026.03.26 19:40:00` `SHORT -> NO_TRADE` `reason=SHORT_FILTERS_OK -> SHORT_MARGIN_FAIL` `d_p_short=-0.029486` `d_p_flat=0.065792` `d_p_long=-0.036306` `top=atr_50=-6.896963; atr_14=3.468460; stoch_kd_diff=-0.622988`
- `2026.03.09 18:00:00` `NO_TRADE -> LONG` `reason=LONG_MARGIN_FAIL -> LONG_FILTERS_OK` `d_p_short=0.017193` `d_p_flat=-0.062720` `d_p_long=0.045528` `top=atr_14=-14.350217; atr_50=-0.673634; atr_14_over_atr_50=-0.280809`
- `2026.03.26 19:45:00` `SHORT -> NO_TRADE` `reason=SHORT_FILTERS_OK -> SHORT_MARGIN_FAIL` `d_p_short=-0.026211` `d_p_flat=0.061207` `d_p_long=-0.034996` `top=atr_50=-6.800724; atr_14=3.111019; atr_14_over_atr_50=0.252360`

## Interpretation

- `atr_14`, `atr_50`, and `atr_14_over_atr_50` dominate the shared drift surface across the sampled bars, with `stoch_kd_diff` acting as a secondary contributor
- the strongest sampled decision flips are concentrated in bars where the contract-aligned path lowers directional conviction and raises `p_flat` enough to turn a built-in entry into `NO_TRADE`
- this supports the corrected Stage 39 read: the current open question is shared feature-surface attribution, not a `34D`-only sidecar explanation
