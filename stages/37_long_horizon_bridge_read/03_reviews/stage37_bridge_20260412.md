# Stage 37 Long-Horizon Bridge Review

- reviewed_on: `2026-04-12`
- stage: `37_long_horizon_bridge_read`
- bridge_window: `2024-01-01 .. 2026-02-28 inclusive`
- operating_reference: `37A_34d_bridge_0001`
- simplification_shadow: `37B_34b_bridge_0001`

## Executive Read

- this stage keeps the frozen split scoreboard untouched and asks only whether the Stage 35 simplification story survives one uninterrupted risk_pct equity path
- bridge result `37A minus 37B`: `net=129.640` `return_pct=25.928` `pf=0.0015` `dd_pct=0.0319`
- the yearly contribution shape was: `2024=34.500` `2025=43.650` `2026_ytd=51.490`

## Scoreboard

### 37A_34d_bridge_0001

- label: `37A 34D continuous bridge`
- bridge headline: `net=3677.680` `return_pct=735.536` `pf=1.4748` `dd_pct=18.7609` `trades=1035`
- bridge risk: `ulcer=6.9923` `worst_week=-427.100` `no_trade_rate=0.9162` `external_mismatch_count=51434`
- bridge expectancy: `long=2.3829` `short=4.6221` `per_trade=3.5533`
- 2024: `net=190.320` `trades=346` `long=148` `short=198`
- 2025: `net=1738.420` `trades=572` `long=284` `short=288`
- 2026_ytd: `net=1748.940` `trades=117` `long=62` `short=55`

### 37B_34b_bridge_0001

- label: `37B 34B continuous bridge`
- bridge headline: `net=3548.040` `return_pct=709.608` `pf=1.4733` `dd_pct=18.7290` `trades=1035`
- bridge risk: `ulcer=6.9301` `worst_week=-412.520` `no_trade_rate=0.9162` `external_mismatch_count=51434`
- bridge expectancy: `long=2.2450` `short=4.5083` `per_trade=3.4281`
- 2024: `net=155.820` `trades=346` `long=148` `short=198`
- 2025: `net=1694.770` `trades=572` `long=284` `short=288`
- 2026_ytd: `net=1697.450` `trades=117` `long=62` `short=55`

## Bridge Read

- use this read as continuity evidence only; it does not replace `hist_2024 / validation / test`
- if the bridge still prefers `34D`, then the Stage 35 and Stage 36 conclusions become more robust because they survive both reset and continuous-account views
- if the bridge narrows the gap materially, that still points toward a narrower future simplification pass, not blanket sidecar removal
