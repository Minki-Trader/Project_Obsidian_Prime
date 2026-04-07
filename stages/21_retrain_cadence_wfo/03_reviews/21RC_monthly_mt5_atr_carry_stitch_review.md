# Stage 21 Monthly MT5 ATR Carry Stitch

Generated at: `2026-04-07T10:29:28.748918+00:00`

- run: `21m1a`
- stitched return_pct: `-38.466`
- stitched net_profit: `-192.33`
- stitched PF: `0.8650`
- stitched trades: `676`
- stitched max_dd_pct: `45.494`
- positive months: `1/5`

## Monthly Results

- `2025_04`: deposit_in `500.00`, final_balance `396.61`, return_pct `-20.678`, net_profit `-103.39`, PF `0.8037`, trades `237`, max_dd_pct `29.040`
- `2025_05`: deposit_in `396.61`, final_balance `393.68`, return_pct `-0.585`, net_profit `-2.32`, PF `0.9850`, trades `69`, max_dd_pct `10.980`
- `2025_06`: deposit_in `393.68`, final_balance `311.95`, return_pct `-20.588`, net_profit `-81.05`, PF `0.6993`, trades `123`, max_dd_pct `24.022`
- `2025_07`: deposit_in `311.95`, final_balance `294.99`, return_pct `-5.132`, net_profit `-16.01`, PF `0.9113`, trades `93`, max_dd_pct `15.279`
- `2025_08`: deposit_in `294.99`, final_balance `307.67`, return_pct `4.634`, net_profit `13.67`, PF `1.0507`, trades `154`, max_dd_pct `17.016`

## Caveat

- This ATR+risk_pct stitch is more faithful to the current 18E risk engine than fixed lot, but it is still stitched from separate monthly MT5 runs rather than a single tester pass with model scheduling.
- Carry-account interpretation uses the chained month-end balance, ending at `307.67` from `500.00`. Month headline net profits from MT5 do not sum exactly to that chained ending balance, so the stitched top-line is anchored to the carry balance.
