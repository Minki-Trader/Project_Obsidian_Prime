# Stage 41 Threshold Sensitivity Attribution

- reviewed_on_utc: `2026-04-14T15:03:58.175547+00:00`
- sampled snapshot rows: `121`
- decision diffs: `32`
- directional -> NO_TRADE diffs: `26`
- NO_TRADE -> directional recoveries: `6`

## Executive Read

- the sampled latest-window built-in-versus-contract decision drift is almost entirely a base margin sensitivity story, not a contextual suppressor story
- `25 / 26` sampled directional-to-`NO_TRADE` flips are `margin_cross`, while only `1 / 26` is a pure `threshold_cross`
- none of the `32` sampled decision-diff rows had an active contextual soft suppressor on the relevant direction, so the fixed `max_probability_margin min_margin=0.0675` gate is the dominant live decision tax in this sample

## Rule Surface

- base threshold entry: `short=0.333333` `long=0.333333`
- base max-probability margin: `min_margin=0.067500`
- contextual rule `filters_02` `context=monday` `direction=short` `threshold_add=0.050000` `min_margin_add=0.050000`
- contextual rule `filters_03` `context=ny_postcash` `direction=short` `threshold_add=0.050000` `min_margin_add=0.030000`
- contextual rule `filters_04` `context=late_session` `direction=long` `threshold_add=0.020000` `min_margin_add=0.010000`

## Cause Breakdown

- `margin_cross` `count=25`
- `margin_recovery` `count=6`
- `threshold_cross` `count=1`

## Transition Headroom

- `long_to_no_trade` `count=15` `thr_delta_mean=-0.050219` `margin_delta_mean=-0.070657` `p_flat_delta_mean=0.073782`
  `atr_14` `mean=4.108361` `atr_50` `mean=-7.066662` `atr_14_over_atr_50` `mean=0.226159`
- `no_trade_to_long` `count=5` `thr_delta_mean=0.039959` `margin_delta_mean=0.037767` `p_flat_delta_mean=-0.050036`
  `atr_14` `mean=-14.290621` `atr_50` `mean=-1.088387` `atr_14_over_atr_50` `mean=-0.294130`
- `no_trade_to_short` `count=1` `thr_delta_mean=-0.025228` `margin_delta_mean=0.007661` `p_flat_delta_mean=0.058117`
  `atr_14` `mean=2.347987` `atr_50` `mean=-6.948609` `atr_14_over_atr_50` `mean=0.236266`
- `short_to_no_trade` `count=11` `thr_delta_mean=-0.002719` `margin_delta_mean=-0.026739` `p_flat_delta_mean=-0.004844`
  `atr_14` `mean=-8.486837` `atr_50` `mean=-4.042915` `atr_14_over_atr_50` `mean=-0.059041`

## Comparator Shifts

- `short_to_no_trade` `long -> long` `count=7`
- `long_to_no_trade` `short -> short` `count=7`
- `no_trade_to_long` `short -> short` `count=4`
- `long_to_no_trade` `short -> flat` `count=4`
- `short_to_no_trade` `long -> flat` `count=4`
- `long_to_no_trade` `flat -> flat` `count=3`
- `no_trade_to_long` `flat -> short` `count=1`
- `no_trade_to_short` `long -> long` `count=1`

## Threshold Cross

- `2026.03.09 20:00:00` `LONG -> NO_TRADE` `cause=threshold_cross` `reason=LONG_FILTERS_OK -> THRESHOLD_FAIL` `thr=0.061041 -> -0.003635` `margin=0.000371 -> -0.162917` `comp=flat -> flat` `top=atr_50=-7.560393; atr_14=4.294144; stoch_kd_diff=-0.297053`

## Margin Cross Rows

- `2026.03.09 19:15:00` `LONG -> NO_TRADE` `cause=margin_cross` `reason=LONG_FILTERS_OK -> LONG_MARGIN_FAIL` `thr=0.069408 -> 0.010671` `margin=0.027466 -> -0.116617` `comp=flat -> flat` `top=atr_14=8.155932; atr_50=-4.544396; atr_14_over_atr_50=0.259008`
- `2026.03.09 19:10:00` `LONG -> NO_TRADE` `cause=margin_cross` `reason=LONG_FILTERS_OK -> LONG_MARGIN_FAIL` `thr=0.074956 -> 0.015558` `margin=0.037769 -> -0.105100` `comp=flat -> flat` `top=atr_14=8.470125; atr_50=-4.531139; atr_14_over_atr_50=0.265287`
- `2026.03.09 20:05:00` `LONG -> NO_TRADE` `cause=margin_cross` `reason=LONG_FILTERS_OK -> LONG_MARGIN_FAIL` `thr=0.085960 -> 0.023654` `margin=0.043794 -> -0.078778` `comp=short -> flat` `top=atr_50=-7.750225; atr_14=4.402215; stoch_kd_diff=-0.587595`
- `2026.03.09 19:00:00` `LONG -> NO_TRADE` `cause=margin_cross` `reason=LONG_FILTERS_OK -> LONG_MARGIN_FAIL` `thr=0.107993 -> 0.050173` `margin=0.077219 -> -0.026930` `comp=short -> flat` `top=atr_14=9.136527; atr_50=-3.963480; stoch_kd_diff=-0.371385`
- `2026.04.07 20:00:00` `LONG -> NO_TRADE` `cause=margin_cross` `reason=LONG_FILTERS_OK -> LONG_MARGIN_FAIL` `thr=0.057593 -> 0.022573` `margin=0.009916 -> -0.079719` `comp=flat -> flat` `top=atr_50=-7.618350; atr_14=-1.616251; atr_14_over_atr_50=0.133846`
- `2026.03.09 20:20:00` `LONG -> NO_TRADE` `cause=margin_cross` `reason=LONG_FILTERS_OK -> LONG_MARGIN_FAIL` `thr=0.070707 -> 0.012149` `margin=0.003322 -> -0.081013` `comp=short -> flat` `top=atr_50=-8.450065; atr_14=3.284457; atr_14_over_atr_50=0.215949`
- `2026.03.26 19:40:00` `SHORT -> NO_TRADE` `cause=margin_cross` `reason=SHORT_FILTERS_OK -> SHORT_MARGIN_FAIL` `thr=0.069733 -> 0.040247` `margin=0.018477 -> -0.039557` `comp=long -> flat` `top=atr_50=-6.896963; atr_14=3.468460; stoch_kd_diff=-0.622988`
- `2026.03.03 17:35:00` `SHORT -> NO_TRADE` `cause=margin_cross` `reason=DUAL_SIGNAL_SHORT_WINS -> DUAL_SIGNAL_TIE_OR_MARGIN_FAIL` `thr=0.151431 -> 0.147303` `margin=0.036505 -> -0.007454` `comp=long -> long` `top=atr_14=-18.564409; atr_50=-1.758766; stoch_kd_diff=-0.358085`
- `2026.03.26 19:45:00` `SHORT -> NO_TRADE` `cause=margin_cross` `reason=SHORT_FILTERS_OK -> SHORT_MARGIN_FAIL` `thr=0.068170 -> 0.041959` `margin=0.012138 -> -0.030047` `comp=long -> flat` `top=atr_50=-6.800724; atr_14=3.111019; atr_14_over_atr_50=0.252360`
- `2026.04.07 20:40:00` `LONG -> NO_TRADE` `cause=margin_cross` `reason=LONG_FILTERS_OK -> LONG_MARGIN_FAIL` `thr=0.106564 -> 0.046242` `margin=0.016025 -> -0.024933` `comp=short -> short` `top=atr_50=-8.130204; atr_14=6.917266; stoch_kd_diff=-0.341752`
- `2026.04.07 20:15:00` `LONG -> NO_TRADE` `cause=margin_cross` `reason=LONG_FILTERS_OK -> LONG_MARGIN_FAIL` `thr=0.091049 -> 0.037319` `margin=0.020334 -> -0.015225` `comp=short -> flat` `top=atr_50=-7.231562; atr_14=4.961477; stoch_kd_diff=-1.761565`
- `2026.03.03 19:20:00` `LONG -> NO_TRADE` `cause=margin_cross` `reason=DUAL_SIGNAL_LONG_WINS -> DUAL_SIGNAL_TIE_OR_MARGIN_FAIL` `thr=0.129887 -> 0.077270` `margin=0.009438 -> -0.022189` `comp=short -> short` `top=atr_50=-8.395629; atr_14=5.875993; stoch_kd_diff=0.769909`

## Margin Recovery Rows

- `2026.03.09 17:55:00` `NO_TRADE -> LONG` `cause=margin_recovery` `reason=LONG_MARGIN_FAIL -> LONG_FILTERS_OK` `thr=0.011282 -> 0.063623` `margin=-0.070288 -> 0.001964` `comp=flat -> short` `top=atr_14=-14.967541; atr_50=-0.466790; stoch_kd_diff=0.317157`
- `2026.03.02 17:25:00` `NO_TRADE -> LONG` `cause=margin_recovery` `reason=LONG_MARGIN_FAIL -> LONG_FILTERS_OK` `thr=0.067084 -> 0.106721` `margin=-0.014938 -> 0.017237` `comp=short -> short` `top=atr_14=-15.221556; atr_50=-1.783099; atr_14_over_atr_50=-0.312197`
- `2026.03.02 17:30:00` `NO_TRADE -> LONG` `cause=margin_recovery` `reason=LONG_MARGIN_FAIL -> DUAL_SIGNAL_LONG_WINS` `thr=0.077482 -> 0.119778` `margin=-0.029801 -> 0.000554` `comp=short -> short` `top=atr_14=-17.896037; atr_50=-2.081257; atr_14_over_atr_50=-0.359143`
- `2026.03.09 18:00:00` `NO_TRADE -> LONG` `cause=margin_recovery` `reason=LONG_MARGIN_FAIL -> LONG_FILTERS_OK` `thr=0.056331 -> 0.101859` `margin=-0.013355 -> 0.014980` `comp=short -> short` `top=atr_14=-14.350217; atr_50=-0.673634; atr_14_over_atr_50=-0.280809`
- `2026.03.02 17:05:00` `NO_TRADE -> LONG` `cause=margin_recovery` `reason=DUAL_SIGNAL_TIE_OR_MARGIN_FAIL -> DUAL_SIGNAL_LONG_WINS` `thr=0.132531 -> 0.152526` `margin=-0.020534 -> 0.005185` `comp=short -> short` `top=atr_14=-9.017756; atr_50=-0.437155; atr_14_over_atr_50=-0.218345`
- `2026.03.26 19:50:00` `NO_TRADE -> SHORT` `cause=margin_recovery` `reason=SHORT_MARGIN_FAIL -> SHORT_FILTERS_OK` `thr=0.075978 -> 0.050750` `margin=-0.003961 -> 0.003700` `comp=long -> long` `top=atr_50=-6.948609; atr_14=2.347987; atr_14_over_atr_50=0.236266`

## Interpretation

- the current sampled weakness is not pointing at a fresh runtime mismatch on these bars; it points at the contract-aligned feature surface pushing the model closer to the fixed decision boundary
- long-side failures are mostly a `flat-wall` problem: contract rows often raise `p_flat` enough to erase the built-in long margin
- short-side failures are mostly a `tie-compression` problem: the contract lane usually narrows the short-versus-long gap even when `p_flat` is not the main comparator
- the next high-signal task is a fixed-margin sensitivity replay around `min_margin=0.0675`, not another 34D-sidecar hunt
