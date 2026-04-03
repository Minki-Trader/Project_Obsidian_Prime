# Project Obsidian Prime

## Scope

This workspace is the FPMarkets `US100` M5 data, feature, and modeling pipeline for Project Obsidian Prime.

## Organizational Goals

- Keep the project easy to re-enter from a new thread.
- Keep the main theme visible: shared market-data and feature pipeline first, stage experiments second.
- Prevent any single folder from becoming a dump of mixed artifacts.
- Favor stable placement rules over ad hoc convenience.

## Directory Rules

- Keep the root limited to high-signal project folders such as `docs`, `data`, `foundation`, and later `stages`.
- Keep source documents in `docs/`.
- Keep raw and processed artifacts in `data/`.
- Keep reusable shared code in `foundation/`.
- Do not add a top-level `scripts/` folder.
- Do not duplicate raw datasets into stage folders.

## Source Of Truth

- Treat `docs/contracts/feature_calculation_spec_fpmarkets_v2.md` and `docs/contracts/python_feature_parser_spec_fpmarkets_v2.md` as the feature contract source of truth.
- Treat `docs/contracts/mt5_ea_input_order_contract_fpmarkets_v2.md` as the runtime input contract source of truth.
- Use `docs/context/` for project background and migration history.
- Treat reports in `foundation/reports/` as implementation notes, not contract overrides.

## Data And Feature Rules

- Use `US100` M5 as the base modeling frame.
- Use the strict M5 symbol intersection as a coverage audit artifact, not as the rolling-feature base frame.
- Compute external-symbol features on each symbol's own raw M5 series, then merge them onto the `US100` base frame by bar-close timestamp.
- Use `GOOGL.xnas` as the contract Google symbol unless the task explicitly calls for `GOOG.xnas`.
- Treat `foundation/config/top3_monthly_weights_fpmarkets_v2.csv` as a placeholder until real monthly weights are supplied.
- Use `2022-08-01` through `2026-02-28` as the expanded common window unless the user explicitly changes it.
- Use `2022-09-01` as the practical modeling start unless the user explicitly wants a different warmup policy.

## Tester And Runtime Defaults

- For MT5 Strategy Tester runs, runtime checks, and EA optimization setup, default to `US100` on `M5`.
- Default tester model to `Every tick based on real ticks` (`Model=4`) unless the user explicitly approves another model.
- Do not use `1 minute OHLC`, open-prices-only, or inherited example tester defaults unless the user explicitly asks for them.
- Default initial deposit to `500 USD` and leverage to `1:100` unless the user explicitly changes them.
- Treat signal generation as `new closed M5 bar only`, even when the tester itself runs on every tick.
- Treat execution and risk management as tick-driven, but never let the model read partial current-bar values.
- Keep external-symbol sourcing on closed `M5` bars with exact timestamp alignment to the target `US100` inference bar.
- When creating `.ini` or `.set` files, explicitly write these tester defaults instead of relying on MetaTrader example files or platform defaults.

## Optimization Experiment Defaults

- Freeze the long-run chronological split for optimization work as:
  - train: `2022-09-01` through `2024-12-31`
  - validation/optimize: `2025-01-01` through `2025-09-30`
  - test/holdout: `2025-10-01` through `2026-02-28`
- Treat model family, feature subset, feature count, and rule composition as experiment variables. Do not globally freeze them for optimize-stage work.
- Freeze only the EA-facing output interface: `[p_short, p_flat, p_long]`.
- Prefer a single manifest-centered experiment handoff such as `experiment_bundle.json` plus referenced artifact files, rather than implicit folder-name conventions.
- Represent EA logic as an ordered rule stack, not as a growing list of hard-coded monolithic modes.
- Prefer Python-led orchestration for model training, export, bundle creation, tester invocation, and result collection. Treat MT5 as the execution and verification engine.
- For optimization experiments, default to next-tick entry after a closed-bar signal and allow at most one concurrent position unless the user explicitly changes that policy.
- Treat opposite-signal immediate exit and max-hold-bar behavior as logic-specific experiment settings declared in the rule stack, not as global defaults.
- For optimization experiments, default position sizing to fixed `0.1` lot unless the user explicitly changes it.
- Prefer broker-native tester cost behavior in real-tick runs. Do not invent extra commission assumptions when the account does not use commission.

## Experiment Bundle Defaults

- Prefer a manifest-centered experiment handoff rooted at `experiment_bundle.json`.
- Treat the following top-level bundle groups as the long-run default structure:
  - `identity`
  - `artifacts`
  - `feature_schema`
  - `output_schema`
  - `external_inputs`
  - `data_snapshot`
  - `runtime_snapshot`
  - `rule_stack`
  - `results`
  - `compatibility`
- Freeze only the EA-facing output schema to:
  - `type = probs3`
  - `order = [p_short, p_flat, p_long]`
- In `artifacts`, prefer a list of artifact objects rather than fixed top-level path keys.
- Each artifact object should be able to carry at least:
  - `role`
  - `path`
  - `format`
  - `sha256`
  - `required`
- In `feature_schema`, prefer a compact runtime summary plus a referenced schema artifact.
- Keep `feature_schema` ready to carry at least:
  - `feature_count`
  - `order_version`
  - `feature_schema_artifact_role`
  - `feature_fingerprint`
- In `external_inputs`, describe each external requirement explicitly rather than relying on implicit contract inheritance.
- Keep each external input entry ready to carry at least:
  - `symbol`
  - `timeframe`
  - `required`
  - `alignment_rule`
  - optional `group` or `role`
- In `data_snapshot`, prefer a rich snapshot that preserves experiment reproducibility.
- Keep `data_snapshot` ready to carry at least:
  - split boundaries
  - label configuration
  - dataset id
  - source artifact references
  - row counts or split counts when available
- In `runtime_snapshot`, preserve the actual execution assumptions used by the tester run.
- Keep `runtime_snapshot` ready to carry at least:
  - `symbol`
  - `timeframe`
  - `tester_model`
  - `deposit`
  - `leverage`
  - `sizing_mode`
  - `fixed_lot`
  - `entry_timing`
  - `max_concurrent_positions`
  - `cost_behavior`
  - optional `currency`
- In `rule_stack`, prefer category-separated rule objects over flat mode names.
- Treat the long-run rule-stack categories as:
  - `entry`
  - `filters`
  - `position`
  - `exit`
- Keep each rule entry ready to carry at least:
  - `type`
  - `enabled`
  - `params`
- In `results`, prefer a layered quantitative-analysis structure rather than a single flat score table.
- Treat the long-run top-level `results` groups as:
  - `by_split`
  - `cross_split`
  - `report_refs`
- In `results.by_split`, prefer a named split registry rather than a hard-coded small set of split keys.
- Default named splits should be able to cover at least:
  - `validation`
  - `test`
  - optional `train`
  - optional `walkforward_*`
  - optional `paper`
  - optional `live_shadow`
- Within each split result, prefer separate analysis layers for:
  - `headline`
  - `risk`
  - `diagnostics`
  - `execution`
- Keep `headline` as a fast selection layer, not as a dump of all metrics.
- Keep `headline` ready to carry at least:
  - `net_profit`
  - `return_pct`
  - `trade_count`
  - `win_rate`
  - `profit_factor`
  - `expectancy_per_trade`
  - `max_dd_pct`
  - `recovery_factor`
- Keep `risk` as a dedicated account-stress and drawdown layer.
- Keep `risk` ready to carry at least:
  - `max_dd_pct`
  - `max_dd_amount`
  - `equity_dd_pct`
  - `equity_dd_amount`
  - `time_under_water`
  - `longest_recovery_duration`
  - `worst_day`
  - `worst_week`
  - `min_free_margin`
  - `margin_call_proximity`
  - `ulcer_index`
  - `consecutive_losses`
- Keep `diagnostics` as the explanation layer for trade distribution, excursion behavior, and rule effects.
- Keep `diagnostics` ready to carry at least:
  - `avg_win`
  - `avg_loss`
  - `payoff_ratio`
  - `avg_hold`
  - `hold_distribution`
  - `long_count`
  - `short_count`
  - `long_expectancy`
  - `short_expectancy`
  - `mfe_mean`
  - `mfe_median`
  - `mfe_p90`
  - `mae_mean`
  - `mae_median`
  - `mae_p90`
  - `realized_over_mfe`
  - `win_trade_mae`
  - `loss_trade_mfe`
  - `rule_pass_rates`
  - `no_trade_rate`
- Keep `execution` as the real-tick implementation and broker-behavior layer.
- Keep `execution` ready to carry at least:
  - `skip_rate`
  - `reject_count`
  - `avg_spread`
  - `avg_slippage`
  - `skip_reason_breakdown`
  - `external_mismatch_count`
  - `fill_rate`
  - `entry_delay_stats`
  - `next_tick_fill_distance`
  - `spread_regime_breakdown`
  - `slippage_regime_breakdown`
  - `sessionwise_execution_quality`
  - `runtime_warning_counts`
  - `data_readiness_failures`
  - `broker_constraint_events`
- In `results.cross_split`, keep `stability` as a dedicated layer rather than mixing it into per-split metrics.
- Keep `stability` ready to carry at least:
  - validation/test gap metrics
  - `profit_factor_gap`
  - `expectancy_gap`
  - `win_rate_gap`
  - `long_short_mix_shift`
  - `parameter_neighborhood_robustness`
  - `subperiod_consistency`
  - `regime_slice_consistency`
  - `rank_consistency`
  - `parameter_surface_smoothness`
- In `results.report_refs`, prefer a list of report-reference objects rather than flat path fields or fixed role-key maps.
- Keep each report reference ready to carry at least:
  - `role`
  - `split`
  - `artifact_id`
  - `description`
- In `compatibility`, prefer a strong fail-fast contract rather than a warning-only compatibility note.
- Keep `compatibility` ready to carry at least:
  - `schema_version`
  - `required_ea_capabilities`
  - `required_output_schema`
  - `required_feature_fingerprint`
  - `required_artifact_hashes`
  - `bundle_integrity_hash`
  - `mismatch_policy`
  - `min_ea_bundle_support_version`
- Prefer `required_ea_capabilities` as a list of capability objects, not as plain strings.
- Keep each capability requirement ready to carry at least:
  - `name`
  - `min_version`
  - optional `params`
- In `artifacts`, assign an explicit `artifact_id` to each artifact object and use `artifact_id` for internal bundle references instead of relying only on file paths or role names.
- Build `bundle_integrity_hash` from a canonical representation of the manifest's core structure plus artifact identity/hash summaries, rather than from the raw manifest text alone.
- Treat `mismatch_policy` as fail-fast by default. Required schema, capability, feature-fingerprint, artifact-hash, and bundle-support mismatches should stop execution rather than degrade to warnings.
- Do not add extra strictness-flag subpolicies by default. Keep the compatibility contract simple: required mismatches are errors.

## Working Style

- Prefer minimal structural changes over broad reorganization.
- Put reusable collectors in `foundation/collectors/`.
- Put reusable indicators and feature helpers in `foundation/features/`.
- Put shared build pipelines in `foundation/pipelines/`.
- Put shared audit or build notes in `foundation/reports/`.
- For bundle handoff workflows, prefer shared pipeline helpers in `foundation/pipelines/`:
  `export_experiment_bundle_assets.py` for run-dir export,
  `prepare_experiment_bundle_request.py` for request-only assembly,
  and `build_experiment_bundle.py` for validated final bundle creation.
- Put reusable datasets or shared pipeline outputs in `data/processed/`.
- Put stage-specific configs, run outputs, reviews, and selected artifacts under `stages/<nn_name>/`.

## Data Placement Rules

- Keep `data/raw/` for source-like datasets only.
- Keep `data/processed/` for reusable shared outputs that multiple stages may depend on.
- Do not store one-off experiment clutter directly in `data/processed/`.
- If an output is specific to a single stage or a single experiment run, keep it under that stage instead of promoting it into `data/`.
- Promote only stable, reused artifacts into `data/processed/`.

## Stage Structure Rules

- Use stage folders only for work that belongs to a distinct modeling phase.
- Default stage layout:
  - `stages/<nn_name>/00_spec/`
  - `stages/<nn_name>/01_inputs/`
  - `stages/<nn_name>/02_runs/active/`
  - `stages/<nn_name>/02_runs/archived/`
  - `stages/<nn_name>/03_reviews/`
  - `stages/<nn_name>/04_selected/`
- Keep `00_spec/` small and focused on the current stage purpose, label policy, split policy, and evaluation rules.
- Keep `01_inputs/` limited to manifests, config snapshots, and references to shared datasets rather than copied datasets.
- Keep `02_runs/` as one-folder-per-run. Do not drop loose result files at the stage root.
- Move stale or superseded runs from `02_runs/active/` to `02_runs/archived/`.
- Keep `03_reviews/` for comparison notes, leaderboard-style summaries, and validation conclusions.
- Keep `04_selected/` for the chosen outputs that the next stage should inherit.

## Naming And Re-entry Rules

- Prefer names that reveal purpose at a glance.
- One run should have one folder with all of its local outputs together.
- Keep a short stage brief in `00_spec/` so a new thread can recover the stage goal quickly.
- Keep a short selected-summary note in `04_selected/` so the current best choice is always obvious.
- When resuming work in a new thread, read in this order:
  - `AGENTS.md`
  - relevant contract docs in `docs/contracts/`
  - relevant stage `00_spec/`
  - latest `03_reviews/`
  - latest `04_selected/`

## Encoding

- Keep Korean `.md` and `.txt` documents in UTF-8 with BOM so Windows tools do not garble text.

## MT5 Bundle And Tester Notes

- Prefer `foundation/pipelines/export_experiment_bundle_assets.py` when a run already has `model.joblib` and should emit ONNX, smoke assets, request, and bundle in one pass.
- Prefer `foundation/pipelines/compile_mt5_bundle_runtime.py` to materialize a Common Files runtime package from `experiment_bundle.json`.
- Prefer `foundation/pipelines/run_mt5_bundle_tester.py` to execute bundle-driven Strategy Tester attempts and enrich bundle attempt/execution metadata before falling back to ad hoc temp `.ini` runs.
