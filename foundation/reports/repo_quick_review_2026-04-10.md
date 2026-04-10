# Repo Quick Review (2026-04-10)

## Scope
- Reviewed repository structure and key MT5 runtime tester defaults against project operating guidance.
- Performed a lightweight, non-invasive audit (no pipeline behavior changes).

## What Looks Good
- Root-level organization follows the expected high-signal layout (`docs/`, `data/`, `foundation/`, `stages/`).
- Tester defaults in checked runtime `.ini` files are aligned with project defaults:
  - `Symbol=US100`
  - `Period=M5`
  - `Model=4` (Every tick based on real ticks)
  - `Deposit=500`
  - `Leverage=100`

## Risks / Follow-up Suggestions
1. **Absolute report paths in tester INI files**
   - Current `Report=` values point to a machine-specific Windows terminal data path.
   - Suggestion: generate/report paths via a portable runner or template resolver to reduce environment coupling.

2. **Runtime window appears smoke-oriented**
   - Current `FromDate`/`ToDate` values are short (late February 2026), which is fine for smoke checks.
   - Suggestion: keep this as explicit smoke config and maintain separate, clearly named configs for full split evaluation windows.

3. **Placeholder monthly weights remains expected but should be tracked**
   - `foundation/config/top3_monthly_weights_fpmarkets_v2.csv` is still placeholder by project contract.
   - Suggestion: maintain a TODO/issue pointer to replace with real monthly weights when available.

## Suggested Next Step
- If desired, I can follow up with a small normalization patch to centralize tester report-path templating in shared pipeline utilities, while preserving existing behavior.
