# External Symbol M5 Coverage

## 결론

현재 프로젝트에서 잡은 확장 학습 구간

- `2022-08-01` to `2026-02-28`

은 외부 심볼 M5 데이터 기준으로도 유지 가능하다.

검증 결과, 아래 대상 심볼은 모두 위 구간에서 **43개 월 구간이 전부 비지 않고 이어진다.**

---

## 수집 대상

- `VIX`
- `US10YR`
- `USDX`
- `AAPL.xnas`
- `AMZN.xnas`
- `AMD.xnas`
- `GOOGL.xnas`
- `GOOG.xnas`
- `META.xnas`
- `MSFT.xnas`
- `NVDA.xnas`
- `TSLA.xnas`

Google 계열은 브로커에 `GOOG.xnas`, `GOOGL.xnas` 두 개가 모두 있으므로 둘 다 저장했다.

다만 현재 feature contract 관점의 기본 사용 대상은 `GOOGL.xnas`로 보는 편이 맞다.

---

## 최대 가용 시작 시점

| Symbol | Earliest M5 bar (UTC) |
|---|---|
| `VIX` | `2020-02-17 00:00:00` |
| `US10YR` | `2021-12-09 01:00:00` |
| `USDX` | `2012-11-13 00:00:00` |
| `AAPL.xnas` | `2011-08-22 00:00:00` |
| `AMZN.xnas` | `2011-08-22 00:00:00` |
| `AMD.xnas` | `2021-04-14 16:30:00` |
| `GOOGL.xnas` | `2011-08-22 00:00:00` |
| `GOOG.xnas` | `2011-08-22 00:00:00` |
| `META.xnas` | `2012-05-18 00:00:00` |
| `MSFT.xnas` | `2011-08-22 00:00:00` |
| `NVDA.xnas` | `2011-09-01 00:00:00` |
| `TSLA.xnas` | `2021-01-29 16:30:00` |

가장 늦게 시작하는 필수 축은 `US10YR`이지만, 그래도 `2022-08-01`보다 앞서므로 확장 학습 구간을 막지 않는다.

---

## 확장 학습 구간 검증

검증 기준:

- window: `2022-08-01` to `2026-02-28`
- monthly coverage count expected: `43`
- zero-row month가 하나라도 있으면 교집합 후보에서 재검토

검증 결과:

- 모든 심볼이 `43 / 43` 개월을 채움
- 모든 심볼의 zero-row month = `0`

즉, 외부 심볼 M5 기준으로는 이 구간을 교집합 후보로 유지할 수 있다.

---

## 참고 메모

- `VIX`, `US10YR`, `USDX`는 월별 row 수가 주식 심볼보다 많다.
- 주식 심볼은 정규/확장 세션 구조 때문에 월별 row 수가 대체로 `1400~1800` 수준에 모인다.
- `VIX`는 월별 row 수 변동폭이 상대적으로 크지만, 확장 학습 구간 내 zero month는 없다.
- `GOOG.xnas`는 참고용으로 저장했고, 실제 contract 사용 심볼은 문서 기준으로 `GOOGL.xnas`를 우선한다.

---

## 저장 위치

- root: `data/raw/mt5_bars/m5`
- session manifest: `data/raw/mt5_bars/m5/session_manifest_m5.json`

심볼별 예시:

- `data/raw/mt5_bars/m5/VIX`
- `data/raw/mt5_bars/m5/US10YR`
- `data/raw/mt5_bars/m5/GOOGL.xnas`

---

## 다음 단계

이제 남은 일은 “있느냐”가 아니라 “정렬되느냐”다.

다음 단계에서 확인할 것:

1. `US100` M5 기준으로 외부 심볼 close timestamp를 어떻게 맞출지
2. 세션 차이 때문에 invalid row가 얼마나 생기는지
3. `GOOG.xnas`는 보조 보관만 하고, 실제 feature pipeline에서는 `GOOGL.xnas`만 쓸지 최종 확정
