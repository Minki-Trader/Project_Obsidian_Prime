# Stage 30 Macro Mismatch Root-Cause Review

- reviewed_on: `2026-04-12`
- stage: `30_macro_mismatch_root_cause`
- purpose: `diagnostic sidecar for clustered macro mismatch pressure; not a promotion lane`
- analyzed_reference_run: `29N_25o_sxh2_0001`
- operating contract reminder: `keep exact alignment + all-or-skip as the live rule unless a new contract hypothesis clears a separate diagnostic gate`

## Setup

- runtime evidence source: `29N` validation / test / hist_2024 shadow logs
- raw evidence source: `data/raw/mt5_bars/m5/<symbol>` exact timestamp coverage against the Stage 29 base-bar timeline
- focus symbols: `VIX`, `US10YR`, plus `AAPL.xnas` / `USDX` as structural context controls

## hist_2024

- window: `2024-01-01 -> 2024-12-31`
- runtime headline: `base_bars=70658`, `recorded_external_mismatches=25010`

| symbol | runtime mismatches | raw exact misses | runtime/raw | stale1 recoverable | stale1/raw | raw p90 streak | raw max streak | median bars/day | median first-last UTC |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| `VIX` | `15832` | `36494` | `0.433825` | `8444` | `0.231381` | `10` | `94` | `122` | `01:00` -> `23:35` |
| `US10YR` | `1651` | `13158` | `0.125475` | `7108` | `0.540204` | `3` | `26` | `226` | `01:00` -> `23:55` |
| `AAPL.xnas` | `6131` | `51215` | `0.119711` | `256` | `0.004999` | `185` | `229` | `78` | `16:30` -> `22:55` |
| `USDX` | `1192` | `6323` | `0.188518` | `94` | `0.014866` | `23` | `56` | `252` | `03:00` -> `23:55` |

- `VIX` runtime clusters: top dates `[('2024-07-10', 135), ('2024-07-02', 129), ('2024-05-10', 127)]`, top hours `[(2, 1786), (23, 1641), (3, 1627), (14, 1385)]`, top streaks `[('2024-11-14 01:05', '2024-11-14 04:55', 47), ('2024-01-23 01:40', '2024-01-23 04:55', 40), ('2024-01-24 01:40', '2024-01-24 04:55', 40)]`
- `US10YR` runtime clusters: top dates `[('2024-07-26', 24), ('2024-06-03', 21), ('2024-06-21', 21)]`, top hours `[(22, 289), (1, 270), (21, 205), (2, 161)]`, top streaks `[('2024-07-25 02:15', '2024-07-25 02:40', 6), ('2024-02-14 01:15', '2024-02-14 01:35', 5), ('2024-03-28 22:15', '2024-03-28 22:35', 5)]`
- `AAPL.xnas` runtime clusters: top dates `[('2024-11-28', 71), ('2024-08-07', 57), ('2024-11-13', 57)]`, top hours `[(15, 1779), (16, 1064), (14, 1017), (23, 973)]`, top streaks `[('2024-11-28 14:35', '2024-11-28 18:35', 49), ('2024-04-15 13:35', '2024-04-15 16:30', 36), ('2024-04-16 13:35', '2024-04-16 16:30', 36)]`
- `USDX` runtime clusters: top dates `[('2024-08-07', 24), ('2024-11-13', 24), ('2024-11-15', 24)]`, top hours `[(1, 647), (2, 501), (3, 41), (23, 2)]`, top streaks `[('2024-08-07 01:05', '2024-08-07 03:00', 24), ('2024-11-13 01:05', '2024-11-13 03:00', 24), ('2024-11-15 01:05', '2024-11-15 03:00', 24)]`

## validation

- window: `2025.01.01 -> 2025.10.01`
- runtime headline: `base_bars=52808`, `recorded_external_mismatches=17350`

| symbol | runtime mismatches | raw exact misses | runtime/raw | stale1 recoverable | stale1/raw | raw p90 streak | raw max streak | median bars/day | median first-last UTC |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| `VIX` | `8673` | `21417` | `0.404959` | `6276` | `0.293038` | `7` | `78` | `152` | `01:00` -> `23:50` |
| `US10YR` | `1204` | `6747` | `0.17845` | `4388` | `0.650363` | `2` | `276` | `247` | `01:00` -> `23:55` |
| `AAPL.xnas` | `5926` | `38396` | `0.154339` | `186` | `0.004844` | `185` | `229` | `78` | `16:30` -> `22:55` |
| `USDX` | `1547` | `4672` | `0.331122` | `45` | `0.009632` | `23` | `23` | `252` | `03:00` -> `23:55` |

- `VIX` runtime clusters: top dates `[('2025-09-12', 112), ('2025-01-23', 108), ('2025-02-14', 107)]`, top hours `[(23, 1046), (2, 1027), (3, 947), (14, 808)]`, top streaks `[('2025-02-17 14:35', '2025-02-17 18:15', 45), ('2025-01-15 01:40', '2025-01-15 04:55', 40), ('2025-01-22 01:40', '2025-01-22 04:55', 40)]`
- `US10YR` runtime clusters: top dates `[('2025-05-22', 132), ('2025-05-23', 130), ('2025-05-26', 33)]`, top hours `[(22, 147), (1, 133), (3, 117), (21, 115)]`, top streaks `[('2025-05-23 14:20', '2025-05-23 20:35', 76), ('2025-05-22 14:00', '2025-05-22 19:10', 63), ('2025-05-23 20:45', '2025-05-23 23:20', 32)]`
- `AAPL.xnas` runtime clusters: top dates `[('2025-03-12', 69), ('2025-03-11', 68), ('2025-03-13', 66)]`, top hours `[(15, 1571), (14, 1104), (16, 984), (23, 917)]`, top streaks `[('2025-03-10 13:35', '2025-03-10 17:30', 48), ('2025-03-13 14:00', '2025-03-13 17:30', 43), ('2025-03-11 14:30', '2025-03-11 17:30', 37)]`
- `USDX` runtime clusters: top dates `[('2025-04-03', 24), ('2025-04-04', 24), ('2025-04-08', 24)]`, top hours `[(1, 740), (2, 711), (3, 85), (0, 11)]`, top streaks `[('2025-04-03 01:05', '2025-04-03 03:00', 24), ('2025-04-04 01:05', '2025-04-04 03:00', 24), ('2025-04-08 01:05', '2025-04-08 03:00', 24)]`

## test

- window: `2025.10.01 -> 2026.03.01`
- runtime headline: `base_bars=28874`, `recorded_external_mismatches=8976`

| symbol | runtime mismatches | raw exact misses | runtime/raw | stale1 recoverable | stale1/raw | raw p90 streak | raw max streak | median bars/day | median first-last UTC |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| `VIX` | `1540` | `3779` | `0.407515` | `1648` | `0.436094` | `4` | `107` | `254` | `01:00` -> `23:55` |
| `US10YR` | `2467` | `7111` | `0.346927` | `3842` | `0.54029` | `3` | `118` | `206` | `01:00` -> `23:55` |
| `AAPL.xnas` | `3809` | `20912` | `0.182144` | `103` | `0.004925` | `185` | `229` | `78` | `16:30` -> `22:55` |
| `USDX` | `1147` | `2650` | `0.43283` | `24` | `0.009057` | `23` | `118` | `252` | `03:00` -> `23:55` |

- `VIX` runtime clusters: top dates `[('2025-10-28', 84), ('2025-11-11', 73), ('2025-11-12', 72)]`, top hours `[(23, 435), (2, 156), (3, 147), (1, 125)]`, top streaks `[('2026-02-12 01:05', '2026-02-12 03:45', 33), ('2025-11-12 02:25', '2025-11-12 04:00', 20), ('2025-11-27 18:35', '2025-11-27 20:05', 19)]`
- `US10YR` runtime clusters: top dates `[('2025-11-27', 55), ('2025-12-19', 54), ('2025-12-23', 52)]`, top hours `[(4, 322), (1, 300), (22, 296), (3, 253)]`, top streaks `[('2025-11-06 22:05', '2025-11-06 23:10', 14), ('2025-11-27 03:50', '2025-11-27 04:55', 14), ('2025-12-12 04:10', '2025-12-12 04:55', 10)]`
- `AAPL.xnas` runtime clusters: top dates `[('2025-10-14', 55), ('2026-01-30', 54), ('2025-10-17', 53)]`, top hours `[(15, 1107), (16, 668), (3, 560), (14, 529)]`, top streaks `[('2025-10-14 13:35', '2025-10-14 16:30', 36), ('2025-10-17 13:35', '2025-10-17 16:30', 36), ('2025-10-09 13:55', '2025-10-09 16:30', 32)]`
- `USDX` runtime clusters: top dates `[('2026-01-29', 22), ('2026-02-06', 22), ('2025-10-08', 21)]`, top hours `[(2, 615), (1, 488), (3, 36), (0, 6)]`, top streaks `[('2025-11-25 01:30', '2025-11-25 02:55', 18), ('2025-11-21 01:05', '2025-11-21 02:25', 17), ('2025-10-07 01:15', '2025-10-07 02:25', 15)]`

## Interpretation

- `VIX` is a real sparse-feed problem, not a one-off calendar glitch: its largest runtime pressure lands on `hist_2024` with `15832` recorded mismatches, while the raw missing streak p90 stays around `7` bars across the analyzed windows.
- `US10YR` becomes the main macro runtime pressure on `test` with `2467` recorded mismatches. The source shape is mostly short holes plus date-local clusters, which fits holiday / feed-quality pockets better than a strategy-specific bug.
- `AAPL.xnas` is structurally session-bound rather than mysteriously sparse: median bars per day stay around `78`, far below the US100 base cadence, so its mismatches are expected outside its narrower CFD session.
- `USDX` looks like a scheduled closure artifact more than a macro anomaly: the raw missing streak p90 sits near `23` bars and repeats in the same overnight pocket.
- A one-bar same-day stale fallback is symbol-specific rather than broadly safe: `VIX` only recovers about `0.3202` of raw exact misses on average, while `US10YR` sits nearer `0.577`. That split is exactly why a whole-workspace relaxation story is too blunt for the regular lane.
- Current read: keep `exact alignment + all-or-skip` as the operating contract, keep the old stale-bar branch closed as a promotion path, and treat any future relaxation as a tightly scoped diagnostic for `VIX` / `US10YR` only after separate feed-health evidence is gathered.

## Decision

- keep `exact alignment + all-or-skip` as the operating contract
- keep broad stale-bar relaxation closed as a promotion path
- if this branch reopens, scope it to a feed-health diagnostic on `VIX` / `US10YR`, not to a workspace-wide alignment relaxation
- do not treat `AAPL.xnas` or `USDX` mismatches as evidence for macro stale fallback; they are structural session-shape controls

## Report Refs

- `validation` summary: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages\29_fusion_long_repair\02_runs\active\29N_25o_sxh2_0001\mt5_attempts\att_0001\tester_attempt_summary.json`
- `validation` shadow csv: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\Common\Files\Project_Obsidian_Prime\runtime\exp_29n_25o_sxh2_v1\logs\att_0001_shadow.csv`
- `test` summary: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages\29_fusion_long_repair\02_runs\active\29N_25o_sxh2_0001\mt5_attempts\att_0002\tester_attempt_summary.json`
- `test` shadow csv: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\Common\Files\Project_Obsidian_Prime\runtime\exp_29n_25o_sxh2_v1\logs\att_0002_shadow.csv`
- `hist_2024` summary: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime\stages\29_fusion_long_repair\02_runs\active\29N_25o_sxh2_0001\mt5_attempts\att_0003\tester_attempt_summary.json`
- `hist_2024` shadow csv: `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\Common\Files\Project_Obsidian_Prime\runtime\exp_29n_25o_sxh2_v1\logs\att_0003_shadow.csv`
