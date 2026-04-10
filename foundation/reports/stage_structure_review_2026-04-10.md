# Stage Structure Review (2026-04-10)

## Purpose
빠른 재진입성과 폴더 일관성을 위해 `stages/*` 디렉터리가 AGENTS.md의 기본 레이아웃 규칙을 따르는지 점검했다.

## Check Scope
- 대상: `stages/` 하위 모든 stage 디렉터리
- 기준: 다음 기본 구조 존재 여부
  - `00_spec/`
  - `01_inputs/`
  - `02_runs/active/`
  - `02_runs/archived/`
  - `03_reviews/`
  - `04_selected/`

## Findings (before fix)
다음 누락이 확인되었다.

- 대부분 stage에서 `02_runs/active`, `02_runs/archived` 누락
- `05_optimization`에서 `01_inputs` 누락

## Applied Fix
일관성 확보를 위해 누락된 디렉터리를 생성하고, 빈 디렉터리 추적을 위해 각 신규 디렉터리에 `.gitkeep`를 추가했다.

## Result
현재 모든 stage가 기본 레이아웃을 충족한다.
