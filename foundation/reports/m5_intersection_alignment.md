# M5 Intersection Alignment

## 결론

`US100`과 외부 심볼들을 `M5 close timestamp` 기준으로 strict inner join 했다.

정렬 결과:

- aligned window: `2022-08-01` to `2026-02-28`
- aligned rows: `54,926`
- base `US100` rows in same window: `252,882`
- strict intersection coverage vs `US100`: `21.720012%`

즉, 교집합 정렬은 성공했고 실제 학습용 timestamp 집합도 만들었다.

---

## 사용 심볼

- `US100`
- `VIX`
- `US10YR`
- `USDX`
- `AAPL.xnas`
- `AMZN.xnas`
- `AMD.xnas`
- `GOOGL.xnas`
- `META.xnas`
- `MSFT.xnas`
- `NVDA.xnas`
- `TSLA.xnas`

`GOOG.xnas`는 보관은 했지만, 현재 교집합 정렬에는 포함하지 않았다.

---

## 생성 산출물

- aligned parquet:
  - `data/processed/fpmarkets_v2/m5_intersection/extended_window/fpmarkets_v2_m5_intersection_2022-08-01_2026-02-28.parquet`
- alignment summary:
  - `data/processed/fpmarkets_v2/m5_intersection/extended_window/fpmarkets_v2_m5_intersection_2022-08-01_2026-02-28_summary.json`

컬럼 구조는 아래 형태다.

- `time_utc`
- `us100_open`, `us100_high`, `us100_low`, `us100_close`, ...
- `vix_open`, `vix_high`, `vix_low`, `vix_close`, ...
- `aapl_xnas_open`, `aapl_xnas_high`, `aapl_xnas_low`, `aapl_xnas_close`, ...

---

## 교집합 구간

- first aligned bar: `2022-08-01 16:35:00 UTC`
- last aligned bar: `2026-02-27 22:55:00 UTC`

첫 bar가 `2022-08-01 16:35 UTC`부터 시작하는 건 이상이 아니라, 주식 심볼 교집합이 실제로 살아 있는 장중 분 단위부터 정렬되기 때문이다.

---

## 행 감소가 큰 이유

strict inner join 과정에서 가장 크게 줄어든 구간은 아래다.

1. `US100 -> VIX`
   - `252,882 -> 150,030`
2. `... -> AAPL.xnas`
   - `127,501 -> 55,840`
3. `... -> NVDA.xnas`
   - `55,823 -> 54,927`

이건 대부분 데이터 고장이라기보다 **세션 차이** 때문이다.

- `US100`, `US10YR`, `USDX`, `VIX`는 더 넓은 시간대에 바가 존재한다.
- 개별 주식 심볼은 거래 시간이 훨씬 짧다.
- 그래서 모든 심볼이 동시에 존재하는 분만 남기면, 결과가 자연스럽게 주식 장중 중심으로 압축된다.

---

## 해석

현재 결과는 “교집합 정렬이 실패했다”가 아니라 아래 의미다.

> 계약을 엄격하게 지키면, 실제 학습 가능한 공통 timestamp는 `US100` 전체 M5 바보다 훨씬 적다.

이건 오히려 중요한 확인이다.

- 앞으로 학습셋을 strict intersection으로 갈지
- 아니면 일부 외부 심볼 feature는 별도 규칙으로 계산할지

를 결정할 수 있게 해준다.

---

## 현재 판단

문서 계약을 보수적으로 따르면, 지금 만든 strict intersection parquet는 **바로 학습 입력 베이스로 쓸 수 있는 가장 안전한 공통 바 집합**이다.

다만 `US100` 기준 row 수를 최대한 살리고 싶다면, 다음 단계에서 아래를 따로 검토해야 한다.

1. 주식 심볼 feature를 “주식 장중에만 유효”로 둘지
2. 리스크 프록시(`VIX`, `US10YR`, `USDX`)와 주식 바스켓을 같은 invalid-row 규칙으로 묶을지
3. `US100` 전체 세션을 유지하고 싶은 경우 어떤 feature block을 세션 조건부로 나눌지
