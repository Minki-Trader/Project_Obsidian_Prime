# Obsidian Prime 코드 스윕 리뷰 (2026-04-10)

## 범위
- 현재 로컬 저장소의 브랜치 전수 점검 (`refs/heads`, `refs/remotes`).
- `foundation/` 파이프라인 중심 정적 점검 (`compileall`, `ruff`).

## 브랜치 스캔 결과
- 현재 저장소에는 로컬 브랜치 `work`만 존재하며, `main` 또는 기타 하위 브랜치(로컬/리모트)는 확인되지 않음.
- 따라서 실제 코드 스윕은 `work` 기준으로 진행됨.

## 점검 명령
1. `git branch -vv`
2. `git for-each-ref --format='%(refname:short)' refs/heads refs/remotes`
3. `python -m compileall foundation`
4. `ruff check foundation`

## 핵심 발견 사항

### 1) (High) 타입 힌트 이름 미정의로 런타임 실패 가능
- 파일: `foundation/pipelines/build_experiment_bundle.py`
- 이슈: `build_identity` 함수가 `IdentityRequest`를 타입 힌트로 사용하지만 import 누락.
- 영향: 모듈 import 시점에 `NameError`가 발생해 번들 빌드 파이프라인이 시작조차 되지 않을 수 있음.
- 근거: `ruff check foundation`의 `F821 Undefined name 'IdentityRequest'`.

### 2) (Medium) 린트 누적 부채가 큼 (총 205건)
- 범주:
  - `E402` (모듈 import 위치 규칙 위반) 다수
  - `F401` (unused import) 다수
  - `F541` (placeholder 없는 f-string) 다수
  - `F841` (할당 후 미사용 변수)
- 영향: 유지보수성 저하, 실수 은닉 가능성 증가, CI 도입 시 대량 실패 위험.

### 3) (Info) 파이썬 구문 컴파일은 통과
- `python -m compileall foundation`는 전체 통과.
- 의미: 최소한의 구문 오류는 없으나, 의미적/구조적 문제(예: 미정의 이름)는 별도 관리 필요.

## 권장 조치
1. **즉시 수정 (우선순위 1)**
   - `build_experiment_bundle.py`에 `IdentityRequest` import 추가 또는 타입 힌트 교정.
2. **린트 정리 (우선순위 2)**
   - 1차: `ruff --fix`로 안전 자동수정 가능한 항목 정리.
   - 2차: `E402`는 현재 `sys.path` 주입 패턴을 고려해 폴더 패키징/실행 진입점 구조를 통일한 뒤 점진 정리.
3. **브랜치 운영 개선 (우선순위 3)**
   - 요청한 "main + 하위 브랜치 스윕"을 가능하게 하려면 원격 연결 및 브랜치 전략(예: `main`, `dev/*`, `stage/*`) 명시 필요.

## 메모
- 이번 리뷰는 저장소 메타 상태상 `work` 단일 브랜치만 대상으로 수행됨.
