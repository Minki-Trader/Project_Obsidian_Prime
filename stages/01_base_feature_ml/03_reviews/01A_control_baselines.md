# 01A Control Baselines

Generated at: `2026-03-26T14:46:53.317511+00:00`

## Definitions

- `flat_only`: always predicts `flat`.
- `uniform_random`: samples `short/flat/long` uniformly, averaged over `300` Monte Carlo repeats.
- `frequency_based`: samples classes using the train split class frequencies, averaged over `300` Monte Carlo repeats.

## Validation Class Counts

- valid: `short=2875`, `flat=5641`, `long=3240`
- train frequency vector: `short=0.2634`, `flat=0.4400`, `long=0.2966`

## Results

- `selected_model`: macro_f1=0.4357, balanced_acc=0.4360, accuracy=0.4809, log_loss=1.0186
- `flat_only`: macro_f1=0.2162, balanced_acc=0.3333, accuracy=0.4798, log_loss=7.1863
- `uniform_random`: macro_f1=0.3259 +/- 0.0044, balanced_acc=0.3335 +/- 0.0046, accuracy=0.3335 +/- 0.0046, log_loss=1.0986
- `frequency_based`: macro_f1=0.3326 +/- 0.0043, balanced_acc=0.3332 +/- 0.0043, accuracy=0.3571 +/- 0.0042, log_loss=1.0552

## Interpretation

- The selected Stage 01A model should clear all three simple controls to justify moving into learning-tool comparison.
- `flat_only` is the majority-class shortcut.
- `uniform_random` approximates a no-skill three-way guesser.
- `frequency_based` approximates a predictor that knows only the train label mix, not the features.
