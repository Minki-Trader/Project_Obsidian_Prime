# Project Obsidian Prime

FPMarkets `US100` M5 data, feature, modeling, and MT5 execution pipeline for Project Obsidian Prime.

## Included

- contracts and project docs in `docs/`
- reusable collectors, features, EA, and pipeline code in `foundation/`
- stage specs, reviews, and selected summaries in `stages/`
- workspace guidance in `AGENTS.md`

## Excluded From GitHub

This repository intentionally excludes heavy local artifacts such as:

- raw and processed data in `data/`
- stage run artifacts under `stages/*/02_runs/`
- exported models, ONNX bundles, tester logs, and runtime outputs

Those files stay local because they are large, frequently regenerated, and not a good fit for standard Git hosting.
