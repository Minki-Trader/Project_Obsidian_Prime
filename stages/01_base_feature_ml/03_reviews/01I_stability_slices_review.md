# 01I Stability Slices Review

Generated at: `2026-03-26T17:30:21.721983+00:00`

## Scope

- purpose: `check whether the recommended compact candidate stays stable across month/session/hour slices`
- model family: `logistic_regression`
- fit split: `train`
- eval split: `valid`
- held-out test: `not touched in 01I`

## Overall Valid

- `full_58`: macro_f1 `0.4498`, balanced_accuracy `0.4546`, accuracy `0.5416`, log_loss `1.0120`
- `compact_36_without_volatility_band__risk_proxy__leader_relative`: macro_f1 `0.4628`, balanced_accuracy `0.4649`, accuracy `0.5669`, log_loss `1.0043`

## Stability Read

- monthly compact wins: `6/9`
- session compact wins: `3/3`
- hour compact wins: `8/9`

## Most Positive Slice

- month: `2025-04` delta macro_f1 `0.0559`
- session: `cash_close_30m` delta macro_f1 `0.0249`

## Weakest Slice

- month: `2025-09` delta macro_f1 `-0.0114`
- session: `overnight` delta macro_f1 `0.0104`

## Notes

- Positive delta means the compact candidate outperformed the full baseline in that slice.
- Negative delta means the full baseline held up better in that slice.
- The valid window only produced `3` populated session buckets and `9` populated NY-hour buckets, so read these as observed-slice diagnostics rather than full-day coverage claims.
- The weakest session slice is still positive here, which means the compact candidate stayed ahead in every populated session bucket.
- This remains a post-selection stability diagnostic and does not replace the frozen 01D handoff.

## Artifacts

- monthly comparison: `02_runs/archived/01I_run_0001_stability_slices/month_ny_metrics_comparison.csv`
- session comparison: `02_runs/archived/01I_run_0001_stability_slices/session_bucket_metrics_comparison.csv`
- hour comparison: `02_runs/archived/01I_run_0001_stability_slices/hour_ny_metrics_comparison.csv`
