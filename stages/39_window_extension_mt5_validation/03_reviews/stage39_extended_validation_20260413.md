# Stage 39 Extended Window MT5 Validation

- reviewed_on: `2026-04-13`
- stage: `39_window_extension_mt5_validation`
- extended_window: `2022-08-01 .. 2026-04-12 inclusive`

## Executive Read

- this stage extends the common window to the latest safe closed-bar date and then checks both the continuity story and the current-date MT5 runtime surface
- extended bridge result `39A minus 39B`: `net=107.930` `return_pct=21.586` `pf=0.0015` `dd_pct=0.0319`
- latest shadow audit sample: `ready_rows=100` `mean_max_abs=0.0258` `checksum_exact=0`

## Extended Bridge

### 39A_34d_bridge_ext_0001

- label: `39A 34D extended bridge`
- bridge headline: `net=2950.790` `return_pct=590.158` `pf=1.3025` `dd_pct=18.7609` `trades=1134`
- bridge risk: `ulcer=7.1375` `worst_week=-427.100` `no_trade_rate=0.9151` `external_mismatch_count=53733`
- 2024: `net=190.320` `trades=346` `long=148` `short=198`
- 2025: `net=1738.420` `trades=572` `long=284` `short=288`
- 2026_ytd: `net=1022.050` `trades=216` `long=123` `short=93`

### 39B_34b_bridge_ext_0001

- label: `39B 34B extended bridge`
- bridge headline: `net=2842.860` `return_pct=568.572` `pf=1.3010` `dd_pct=18.7290` `trades=1134`
- bridge risk: `ulcer=7.0774` `worst_week=-412.520` `no_trade_rate=0.9151` `external_mismatch_count=53733`
- 2024: `net=155.820` `trades=346` `long=148` `short=198`
- 2025: `net=1694.770` `trades=572` `long=284` `short=288`
- 2026_ytd: `net=992.270` `trades=216` `long=123` `short=93`

## Latest Shadow Audit

- audit window: `2026.03.01 -> 2026.04.13` `ready_rows=2216`
- MT5 latest runtime: `no_trade_rate=0.8985` `external_mismatch_count=2299`
- exact timestamp proxy: `mean_max_abs=0.0258` `p90=0.0448` `max=0.0965`
- checksum matches: `exact=0` `best_neighbor=0`

## Follow-Up Bias

- keep the historical frozen split scoreboard intact and treat this stage as a latest-window continuity and runtime-audit extension
- if `34D` still leads on the extended bridge, keep simplification closed and carry the base-versus-incumbent story forward
- use the fresh latest shadow logs as the next true parity-audit starting surface rather than leaning only on older handoff logs
