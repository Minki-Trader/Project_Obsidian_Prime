# 05GL Stage 05 Stop Policy Progression Review

Generated at: `2026-03-31T15:54:21.536261+00:00`

## Scope

- risk_pct: `3.0000`
- stop_execution_mode: `broker_native`
- progression: `fixed -> regime_bucket -> direction_split`

## fixed

- `05GC` `05GC_05dp_fixed_stop10_riskpct300_brokersl_0001`: return_pct `401.004`, PF `1.1529`, trades `455`, max_dd_pct `53.3932`, ulcer `31.9590`, avg_hold `3.6835`, no_trade_rate `0.8938`
- `05GD` `05GD_05dp_fixed_stop15_riskpct300_brokersl_0001`: return_pct `264.392`, PF `1.1903`, trades `432`, max_dd_pct `39.0337`, ulcer `21.9114`, avg_hold `4.2755`, no_trade_rate `0.8938`
- `05GE` `05GE_05dp_fixed_stop20_riskpct300_brokersl_0001`: return_pct `388.414`, PF `1.3120`, trades `417`, max_dd_pct `36.9980`, ulcer `19.3046`, avg_hold `4.6619`, no_trade_rate `0.8938`

- leader: `05GC` `05GC_05dp_fixed_stop10_riskpct300_brokersl_0001` with return_pct `401.004` and PF `1.1529`

## regime_bucket

- `05GF` `05GF_05dp_regime085_115_100_150_200_riskpct300_0001`: return_pct `347.492`, PF `1.2418`, trades `428`, max_dd_pct `41.0183`, ulcer `23.0897`, avg_hold `4.3832`, no_trade_rate `0.8938`
- `05GG` `05GG_05dp_regime090_110_090_140_180_riskpct300_0001`: return_pct `339.024`, PF `1.2094`, trades `435`, max_dd_pct `38.3453`, ulcer `21.1869`, avg_hold `4.2483`, no_trade_rate `0.8938`
- `05GH` `05GH_05dp_regime085_120_110_150_220_riskpct300_0001`: return_pct `286.892`, PF `1.2346`, trades `426`, max_dd_pct `40.6883`, ulcer `23.2829`, avg_hold `4.4272`, no_trade_rate `0.8938`

- leader: `05GF` `05GF_05dp_regime085_115_100_150_200_riskpct300_0001` with return_pct `347.492` and PF `1.2418`

## direction_split

- `05GI` `05GI_05dp_dirsplit_l13_s17_riskpct300_0001`: return_pct `455.306`, PF `1.2583`, trades `430`, max_dd_pct `39.8898`, ulcer `21.6570`, avg_hold `4.3558`, no_trade_rate `0.8938`
- `05GJ` `05GJ_05dp_dirsplit_l12_s18_riskpct300_0001`: return_pct `413.408`, PF `1.2376`, trades `431`, max_dd_pct `42.8275`, ulcer `25.7335`, avg_hold `4.3341`, no_trade_rate `0.8938`
- `05GK` `05GK_05dp_dirsplit_l14_s20_riskpct300_0001`: return_pct `521.996`, PF `1.3291`, trades `425`, max_dd_pct `34.5037`, ulcer `15.2271`, avg_hold `4.5176`, no_trade_rate `0.8938`

- leader: `05GK` `05GK_05dp_dirsplit_l14_s20_riskpct300_0001` with return_pct `521.996` and PF `1.3291`

## Overall

- leader: `05GK` `05GK_05dp_dirsplit_l14_s20_riskpct300_0001`
- return_pct: `521.996`
- profit_factor: `1.3291`
- max_dd_pct: `34.5037`
