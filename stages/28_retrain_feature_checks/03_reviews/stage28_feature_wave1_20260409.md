# Stage 28 Feature Simplification Wave 1

- reviewed_on: `2026-04-09`
- purpose: `revisit Stage 16-style feature simplification on the stronger 17E/18E lineage without reopening calendar retraining yet`
- lineage_reference: `18E_2501_17e_ph20_0001`
- current_regular_reference_unchanged: `27A_26a_volref_0001`

## Scoreboard

| run | features | offline_valid_f1 | hist_return | val_return | test_return | test_dd | test_pf | mean_ext_skip | mean_entropy | read |
|---|---|---|---|---|---|---|---|---|---|---|
| `28A` | `54` | `0.4460` | `43.204` | `-5.520` | `38.478` | `14.505` | `1.5343` | `0.3119` | `0.9575` | `full 17E feature reference under 18E PH20 overlay` |
| `28B` | `48` | `0.4528` | `34.220` | `10.002` | `45.020` | `10.940` | `1.6553` | `0.3119` | `0.9578` | `persistence-only compact fork under 18E PH20 overlay` |
| `28C` | `50` | `0.4456` | `36.548` | `-3.288` | `29.966` | `14.039` | `1.3551` | `0.3119` | `0.9569` | `sessionless compact fork under 18E PH20 overlay` |
| `28D` | `44` | `0.4464` | `65.528` | `-22.804` | `37.872` | `12.015` | `1.5289` | `0.3119` | `0.9581` | `external-breadthless compact fork under 18E PH20 overlay` |

## Headline

- rebuilt full reference `28A`: `{'hist': 43.204, 'val': -5.52, 'test': 38.477999999999994, 'test_dd': 14.505022311181309, 'test_pf': 1.5343424524371616}`
- best compact `28B`: `{'hist': 34.22, 'val': 10.001999999999999, 'test': 45.019999999999996, 'test_dd': 10.93993830520777, 'test_pf': 1.6553320329558356}`

## Risk

- rebuilt full OOS risk: `{'ulcer': 6.542225876264124, 'worst_week': -39.92, 'consecutive_losses': 8}`
- best compact OOS risk: `{'ulcer': 5.216274439754374, 'worst_week': -20.24, 'consecutive_losses': 10}`

## Diagnostics

- rebuilt full offline metrics: `{'train': {'rows': 34695, 'macro_f1': 0.4297503870758624, 'balanced_accuracy': 0.4314768463519964, 'accuracy': 0.5151750972762645, 'log_loss': 1.0451941255671455}, 'validation': {'rows': 11756, 'macro_f1': 0.4460059869023321, 'balanced_accuracy': 0.45096343500715613, 'accuracy': 0.5377679482817285, 'log_loss': 1.0266110986561112}, 'test': {'rows': 6720, 'macro_f1': 0.44766639136146075, 'balanced_accuracy': 0.46343971962849834, 'accuracy': 0.5467261904761904, 'log_loss': 1.0144222069737676}}`
- best compact offline metrics: `{'train': {'rows': 34695, 'macro_f1': 0.4288686720802161, 'balanced_accuracy': 0.4303619174371494, 'accuracy': 0.5156074362300043, 'log_loss': 1.0456825267126664}, 'validation': {'rows': 11756, 'macro_f1': 0.4528410573579564, 'balanced_accuracy': 0.45902517480350796, 'accuracy': 0.5429567880231371, 'log_loss': 1.0264700000635507}, 'test': {'rows': 6720, 'macro_f1': 0.45643507654186033, 'balanced_accuracy': 0.47414045086396156, 'accuracy': 0.553422619047619, 'log_loss': 1.0140392184800278}}`
- rebuilt full OOS diagnostics: `{'long_count': 1, 'short_count': 129, 'avg_hold': 3.6153846153846154, 'no_trade_rate': 0.9376757957068838}`
- best compact OOS diagnostics: `{'long_count': 0, 'short_count': 126, 'avg_hold': 3.6825396825396823, 'no_trade_rate': 0.9391561806069578}`

## Execution

- rebuilt full governance read: `{'row_count': 28875, 'mean_external_skip_rate': 0.311891254961039, 'mean_argmax_class_share': 0.5732114171774892, 'mean_entropy': 0.9574750557048183, 'mean_overlay_rate': 0.2579513618533954, 'latest_state': 'OK', 'latest_reason': 'WITHIN_LIMITS'}`
- best compact governance read: `{'row_count': 28875, 'mean_external_skip_rate': 0.311891254961039, 'mean_argmax_class_share': 0.5782684497662338, 'mean_entropy': 0.957781325183593, 'mean_overlay_rate': 0.24730789174543163, 'latest_state': 'OK', 'latest_reason': 'WITHIN_LIMITS'}`

## Decision

- lineage status: `reopen_lineage_followup`
- this wave checks whether compact subsets help the 18E lineage internally; it does not replace the current `27A` operating reference by itself
