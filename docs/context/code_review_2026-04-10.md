# Code Review Sweep — 2026-04-10

## Scope
- Repository: `Project_Obsidian_Prime`
- Requested scope: `main` + all descendant branches
- Actual branch topology found locally: only `work` branch exists (no `main`, no additional local/remote branches)

## What was checked
1. Branch inventory (`git branch -a -vv`) to confirm review coverage.
2. Python syntax pass for shared code (`python -m compileall foundation`).
3. Contract-alignment spot review in bundle/runtime pipeline files.

## Findings

### 1) Branch coverage blocker (Process / Visibility)
**Severity:** Medium

- The repository currently exposes only one branch (`work`), so there are no “sub-branches” to sweep in this local checkout.
- If branch-wide review is required, remote tracking branches need to be available in this clone.

**Evidence:** `git branch -a -vv` output during this review.

**Recommendation:**
- Ensure remote branches are fetched and tracked in this environment before requesting a cross-branch audit.

---

### 2) MT5 tester model fallback may silently use non-real-tick mode
**Severity:** Medium

- `run_mt5_bundle_tester.py` currently maps `runtime_snapshot.tester_model` to MT5 `Model=4` only when value is exactly `"real_ticks"`; all other values silently become `Model=1`.
- This can unintentionally downgrade runtime fidelity if a typo/variant is provided (for example, `"real_tick"`, `"every_tick_real_ticks"`, etc.).

**Evidence:**
- `tester_model_value = 4 if bundle.runtime_snapshot.tester_model == "real_ticks" else 1`

**Recommendation:**
- Add strict enum validation for `runtime_snapshot.tester_model` in the bundle model (e.g., allow only known values), and fail-fast on unknown values instead of defaulting to `Model=1`.

---

## Checks summary
- Branch enumeration: completed.
- Python syntax compile: passed.
- No immediate syntax errors in `foundation/` Python sources.

## Suggested next pass (optional)
- Add CI checks for:
  - bundle schema validation on sample manifests,
  - MT5 tester `.ini` generation assertions for `Model`, `Deposit`, `Leverage`, and split-date derivation.
