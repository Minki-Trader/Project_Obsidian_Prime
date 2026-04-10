# Obsidian Prime 코드 리뷰 (2026-04-10)

## 범위
- Git 브랜치: 로컬/원격 포함 `git branch -a`, `git show-ref --heads` 기준 확인.
- 코드 점검: `foundation/collectors/`, `foundation/features/` 핵심 유틸과 수집 스크립트 중심 정적 리뷰.
- 기본 검증: `python -m compileall foundation`.

## 브랜치 스캔 결과
- 현재 저장소에는 `work` 단일 로컬 브랜치만 존재.
- 원격(remote) 설정 없음.
- 따라서 "main 외 하위 브랜치"에 대한 비교 리뷰는 현재 체크아웃 가능한 대상이 없어 수행 불가.

## 주요 리뷰 이슈

### 1) 월별 export 재실행 시 manifest가 누락된 월을 포함하지 않음 (중요)
- 위치: `foundation/collectors/export_mt5_bars.py`
- 현상: parquet 파일이 이미 존재하고 `--overwrite`가 꺼져 있으면 `continue`로 건너뛰며 `manifest["chunks"]`에 해당 월 정보가 기록되지 않음.
- 영향:
  - manifest 기준으로는 실제 보유 월 데이터 대비 누락이 발생.
  - 후속 파이프라인이 manifest를 source-of-truth로 읽는 경우 데이터 공백으로 오판 가능.
- 제안:
  - skip된 월도 `chunks`에 `status: "skipped_existing"` 형태로 기록하거나,
  - skip 시 기존 parquet 메타(행 수/시작/종료 바)를 역조회해 동일 스키마로 적재.

### 2) tick exporter의 0-row chunk에서 파일 경로를 항상 기록 (중간)
- 위치: `foundation/collectors/export_mt5_real_ticks.py`
- 현상: `export_window`가 0-row를 반환해도 chunk의 `file` 필드가 항상 문자열 경로로 채워짐.
- 영향:
  - 소비자 코드가 `file != null`을 존재 보장으로 해석하면 FileNotFound 오류 가능.
- 제안:
  - bars exporter와 일관되게 `rows == 0`이면 `file: null` 처리.

## 이번 점검에서 확인한 긍정 포인트
- `foundation` 전체 Python 소스는 `compileall` 기준 문법 오류 없음.
- `sector_map.validate_sector_map()`로 feature-order 정합성 자체는 방어되고 있어 유지보수 안정성에 도움.

## 권장 후속 액션
1. 두 collector manifest 스키마를 통일 (`rows == 0` 처리, skipped chunk 처리).
2. manifest를 읽는 소비자 파이프라인에서 `rows`/`file` 동시 검증을 강제.
3. 브랜치 기반 리뷰를 원하면 remote 연결 후 `main`, `develop`, 실험 브랜치 fetch 정책을 먼저 확정.
