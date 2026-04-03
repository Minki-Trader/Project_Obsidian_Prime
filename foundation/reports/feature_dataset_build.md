# Feature Dataset Build

## 결론

`raw MT5 M5 bars -> feature dataset` 변환기를 구현했고, 실제 feature dataset까지 생성했다.

이번 빌드는 strict intersection parquet 위에서 직접 지표를 계산하지 않고,

- `US100` full M5 bar를 base frame으로 사용
- 외부 심볼 feature를 각 심볼의 자체 시계열에서 계산
- 마지막에 `timestamp` 기준으로 base frame에 merge

하는 방식으로 만들었다.

이 방식이 현재 계약에 더 가깝다.

---

## 생성 결과

- total rows: `252,882`
- valid rows: `54,702`
- invalid rows: `198,180`
- first valid timestamp: `2022-08-02 16:40:00 UTC`
- feature count: `58`

즉, 전체 `US100` M5 base row를 유지한 채 feature를 만들었고, 최종 valid mask로 학습 가능한 row를 구분할 수 있게 되었다.

---

## 생성 산출물

- feature matrix:
  - `data/processed/fpmarkets_v2/features/extended_window/feature_matrix.parquet`
- validity mask:
  - `data/processed/fpmarkets_v2/features/extended_window/feature_validity.parquet`
- build summary:
  - `data/processed/fpmarkets_v2/features/extended_window/feature_build_summary.json`

---

## 구현 파일

- `foundation/features/catalog.py`
- `foundation/features/indicators.py`
- `foundation/pipelines/build_feature_dataset.py`
- `foundation/config/top3_monthly_weights_fpmarkets_v2.csv`

---

## 중요한 메모

### 1. top3 weights는 현재 placeholder다

`top3_weighted_return_1`에 필요한 월별 weight table은 현재 로컬 frozen CSV로 공급하고 있다.

현재 파일은 다음 가정으로 채웠다.

- `MSFT`, `NVDA`, `AAPL` equal weight

즉, 현재 값은 **실무 placeholder artifact**이고, 실제 월별 frozen weight table이 준비되면 교체하는 것이 맞다.

### 2. valid row가 적게 남는 것은 주로 세션 차이 때문이다

전체 base row가 25만 개 이상인데 valid row는 5.47만 개 수준이다.

이건 대부분 아래 이유 때문이다.

- 주식 심볼 장중에만 모든 외부 심볼 feature가 동시에 존재
- 계약상 외부 심볼 missing row는 invalid 처리

즉, 현 구조는 “base rows 전체 유지 + valid mask 분리” 쪽으로 보는 것이 맞다.

### 3. 실전 학습 시작점은 2022-09가 더 깔끔하다

기술적으로 첫 valid row는 `2022-08-02`부터 이미 생기지만,

- 초기 warmup
- 월초 경계
- 운영상 단순성

을 고려하면 실제 학습 시작은 `2022-09-01`이 더 깔끔하다.
