# 22 Point Exit Management Review

Generated at: `2026-04-07T23:27:26.853919+00:00`

## Scope

- source: `05DP_05ca_margin0675_hold5_0001`
- experiment style: `keep time_exit hold5 and add one point-based management rule at a time`
- windows: `2024 historical`, `2025 validation Jan-Sep`, `2501 OOS`

## Derived Point Plan

- baseline trade count used for sizing: `1064`
- combined MFE p50/p60: `45.4` / `57.8`
- combined MAE p50/p60: `41.0` / `52.5`
- break-even: `trigger=50` `lock=10`
- trailing stop: `activate=60` `distance=35`
- partial stop loss: `trigger=45` `close_fraction=0.50`
- partial take profit: `trigger=60` `close_fraction=0.50`

## 2024 historical

- [1] `22B_05dp_be50_lock10_0001` `break_even`: return_pct `37.596`, PF `1.2325`, trades `397`, max_dd_pct `11.528`
- [2] `22A_05dp_base_hold5_0001` `baseline_time_exit`: return_pct `23.282`, PF `1.1334`, trades `384`, max_dd_pct `14.863`
- [3] `22C_05dp_trail60_dist35_0001` `trailing_stop`: return_pct `15.838`, PF `1.0876`, trades `410`, max_dd_pct `13.058`
- [4] `22D_05dp_psl45_half_0001` `partial_stop_loss`: return_pct `14.086`, PF `1.0830`, trades `543`, max_dd_pct `16.748`
- [5] `22E_05dp_ptp60_half_0001` `partial_take_profit`: return_pct `13.494`, PF `1.0784`, trades `494`, max_dd_pct `15.355`

## 2025 validation (Jan-Sep)

- [1] `22A_05dp_base_hold5_0001` `baseline_time_exit`: return_pct `122.570`, PF `1.5553`, trades `405`, max_dd_pct `12.603`
- [2] `22C_05dp_trail60_dist35_0001` `trailing_stop`: return_pct `94.626`, PF `1.4144`, trades `467`, max_dd_pct `10.457`
- [3] `22E_05dp_ptp60_half_0001` `partial_take_profit`: return_pct `94.264`, PF `1.4531`, trades `596`, max_dd_pct `11.929`
- [4] `22D_05dp_psl45_half_0001` `partial_stop_loss`: return_pct `82.834`, PF `1.3944`, trades `611`, max_dd_pct `10.417`
- [5] `22B_05dp_be50_lock10_0001` `break_even`: return_pct `74.422`, PF `1.3657`, trades `442`, max_dd_pct `11.558`

## 2501 OOS

- [1] `22A_05dp_base_hold5_0001` `baseline_time_exit`: return_pct `68.574`, PF `1.4925`, trades `275`, max_dd_pct `19.394`
- [2] `22C_05dp_trail60_dist35_0001` `trailing_stop`: return_pct `58.608`, PF `1.4183`, trades `301`, max_dd_pct `24.512`
- [3] `22D_05dp_psl45_half_0001` `partial_stop_loss`: return_pct `53.346`, PF `1.3934`, trades `411`, max_dd_pct `15.218`
- [4] `22B_05dp_be50_lock10_0001` `break_even`: return_pct `51.068`, PF `1.4228`, trades `290`, max_dd_pct `15.705`
- [5] `22E_05dp_ptp60_half_0001` `partial_take_profit`: return_pct `50.332`, PF `1.3774`, trades `390`, max_dd_pct `19.061`

## Aggregate

- `22B_05dp_be50_lock10_0001` `break_even`: window_wins `1`, avg_return_pct `54.362`, avg_PF `1.3403`, worst_max_dd_pct `15.705`
- `22A_05dp_base_hold5_0001` `baseline_time_exit`: window_wins `0`, avg_return_pct `71.475`, avg_PF `1.3937`, worst_max_dd_pct `19.394`
- `22C_05dp_trail60_dist35_0001` `trailing_stop`: window_wins `0`, avg_return_pct `56.357`, avg_PF `1.3068`, worst_max_dd_pct `24.512`
- `22E_05dp_ptp60_half_0001` `partial_take_profit`: window_wins `0`, avg_return_pct `52.697`, avg_PF `1.3029`, worst_max_dd_pct `19.061`
- `22D_05dp_psl45_half_0001` `partial_stop_loss`: window_wins `0`, avg_return_pct `50.089`, avg_PF `1.2903`, worst_max_dd_pct `16.748`

## Verdict

- status: `reject_keep_incumbent`
- selected_run_name: `22A_05dp_base_hold5_0001`
- reason: `no point-exit candidate cleared the baseline across the three-window check`

