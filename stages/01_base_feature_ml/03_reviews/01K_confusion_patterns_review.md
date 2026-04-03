# 01K Confusion Patterns Review

Generated at: `2026-03-26T17:43:51.401547+00:00`

## Scope

- purpose: `compare class confusion structure between the frozen full baseline and the recommended compact candidate`
- model family: `logistic_regression`
- fit split: `train`
- eval split: `valid`
- held-out test: `not touched in 01K`

## Class Metric Delta

| class | recall delta compact-full | precision delta compact-full | f1 delta compact-full |
| --- | ---: | ---: | ---: |
| `flat` | 0.0499 | -0.0162 | 0.0201 |
| `short` | 0.0335 | 0.0293 | 0.0312 |
| `long` | -0.0526 | 0.0220 | -0.0124 |

## Biggest Reduced Error Routes

| true -> pred | full row rate | compact row rate | delta compact-full | count delta |
| --- | ---: | ---: | ---: | ---: |
| `short->long` | 0.3939 | 0.3147 | -0.0792 | -180 |
| `flat->long` | 0.1620 | 0.1233 | -0.0387 | -272 |
| `flat->short` | 0.1657 | 0.1544 | -0.0112 | -79 |

## Biggest Expanded Error Routes

| true -> pred | full row rate | compact row rate | delta compact-full | count delta |
| --- | ---: | ---: | ---: | ---: |
| `long->flat` | 0.2867 | 0.3426 | 0.0559 | 137 |
| `short->flat` | 0.2909 | 0.3367 | 0.0458 | 104 |

## Notes

- Negative route delta means the compact candidate reduced that specific error route.
- Positive route delta means the compact candidate made that route more often.
- This stays inside post-selection diagnostics and does not replace the frozen 01D handoff.

## Artifacts

- confusion counts: `02_runs/archived/01K_run_0001_confusion_patterns/confusion_counts.csv`
- class metrics: `02_runs/archived/01K_run_0001_confusion_patterns/class_metrics.csv`
- route comparison: `02_runs/archived/01K_run_0001_confusion_patterns/misclassification_route_comparison.csv`
- class comparison: `02_runs/archived/01K_run_0001_confusion_patterns/class_metric_comparison.csv`
