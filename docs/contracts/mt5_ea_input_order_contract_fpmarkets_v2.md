# MT5 EA Input-Order Contract FPMarkets v2

## 1. 문서 목적

이 문서는 MetaTrader 5 Expert Advisor가 ONNX 모델 추론 시 사용하는 입력 벡터의 **순서, 타입, shape, 계산 타이밍, 실패 처리 규칙**을 고정한다.

이 문서의 목적은 아래와 같다.

1. Python 학습 입력과 MT5 실전 입력의 의미를 일치시킨다.
2. ONNX inference 호출 시 shape mismatch / order mismatch를 방지한다.
3. EA 런타임에서 feature drift, stale input, partial-bar contamination을 막는다.

상위 문서:

- `feature_calculation_spec_fpmarkets_v2.md`
- `python_feature_parser_spec_fpmarkets_v2.md`

---

## 2. 핵심 원칙

### 2.1 one closed bar, one inference
EA는 **새로운 M5 bar가 확정될 때마다 최대 1회**만 추론한다.

### 2.2 no current-bar contamination
진행 중인 현재 bar 값은 입력에 포함하지 않는다.  
항상 **가장 최근 closed bar** 기준으로 feature vector를 만든다.

### 2.3 exact order match
MT5 input vector의 index 순서는 Python parser output order와 완전히 동일해야 한다.  
단 1칸이라도 어긋나면 같은 모델이 아니다.

### 2.4 all-or-skip
필수 feature 하나라도 계산 실패, 데이터 누락, 외부 심볼 미정렬이면 그 bar에서는 추론을 스킵한다.

### 2.5 stable runtime
indicator handle, ONNX session, external symbol subscription은 초기화 단계에서 준비하고, bar마다 재생성하지 않는다.

---

## 3. 런타임 전제

### 3.1 symbol / timeframe
- Main symbol: `US100`
- Timeframe: `PERIOD_M5`

### 3.2 ONNX artifact location
기본 가정:

- ONNX 파일은 `MQL5\Files\` 또는 common files 경로에 배치
- artifact 버전과 feature order 버전이 일치해야 함

### 3.3 model family assumption for FPMarkets v2
입력 계약은 확정한다.  
출력 계약은 기본적으로 아래 **권장 기본형**을 따른다.

- classification 3-class
- output order = `[p_short, p_flat, p_long]`
- output shape = `[1, 3]`

단, 실제 모델이 binary / regression이면 **새 output contract 버전**을 분리하는 것이 원칙이다.

---

## 4. 초기화 책임

### 4.1 OnInit 단계에서 해야 할 일
- symbol / timeframe 확인
- ONNX session 생성
- input/output count 점검
- input/output shape 설정
- built-in indicator handle 생성
- external symbol availability 점검
- custom feature calculator 초기화
- weight table / session calendar / configuration 로딩

### 4.2 handle 재사용
다음은 bar마다 새로 만들지 않는다.

- MA / RSI / ATR / ADX / Bands / Stochastic indicator handles
- ONNX session handle
- 외부 심볼 준비 상태
- top3 weight table

---

## 5. 데이터 획득 원칙

### 5.1 OHLC source
메인 심볼 OHLC는 M5 bar 기준으로 읽는다.  
권장 접근:

- `CopyRates()` 또는 동등한 rates 접근
- 필요한 warmup 길이만큼 history 확보
- 가장 최근 closed bar는 shift 1 의미로 다룬다

### 5.2 built-in indicator source
MT5 built-in indicator derived feature는 해당 handle에서 `CopyBuffer()`로 읽는다.

주의:

- 값이 계산되기 전에 읽으려 하지 않는다.
- `BarsCalculated(handle)` 또는 유사 검증으로 준비 상태 확인
- 필요한 buffer index를 명확히 문서화
- 현재 진행 중 bar를 읽지 않는다.

### 5.3 custom indicator source
`supertrend_10_3`, `vortex_indicator`, `stochrsi_kd_diff`, `ppo_hist_12_26_9`, `trix_15` 등 built-in이 아닌 항목은 아래 둘 중 하나를 채택한다.

1. EA 내부 수식 구현
2. 사전 검증된 custom indicator handle 사용

권장 기본값은 **EA 내부 구현 + parity test 완료 버전**이다.

### 5.4 external symbol source
외부 심볼은 동일 broker/동일 terminal 데이터로부터 확보하는 것을 우선한다.  
각 심볼의 최신 closed bar timestamp가 메인 심볼의 대상 timestamp와 일치하지 않으면 추론을 스킵한다.

---

## 6. 새로운 bar 감지 계약

권장 이벤트 규칙:

1. 틱 도착
2. 현재 chart symbol/timeframe의 latest bar open time 확인
3. 이전에 처리한 bar와 다르면 새로운 closed bar가 1개 생긴 것으로 간주
4. 그 시점에 직전 closed bar 기준으로 feature 계산
5. 추론 1회 실행
6. 결과 저장
7. 같은 bar에 대해서는 재실행 금지

즉, 실전 추론 단위는 **tick**이 아니라 **new closed M5 bar event**다.

---

## 7. Warmup 및 inference readiness

### 7.1 minimum readiness
다음이 모두 충족되어야 한다.

- 메인 심볼 history >= 300 bars
- 필수 built-in indicator buffers 준비 완료
- 외부 심볼 필수 history 준비 완료
- session feature 계산 가능
- top3 weight table 유효
- ONNX session 정상

### 7.2 readiness failure
준비 부족 시:

- 주문 금지
- 추론 금지
- reason code 로깅

---

## 8. Input tensor contract

### 8.1 tensor count
FPMarkets v2 기본 가정: input tensor는 **1개**

### 8.2 tensor shape
FPMarkets v2 기본 shape:

- `[1, 58]`

즉 batch size 1, feature dimension 58.

시퀀스 모델로 확장하면 별도 contract 버전 필요.

### 8.3 tensor dtype
권장 dtype:

- `float32`

내부 계산은 `double`이어도 되지만, ONNX 입력 직전 명시적으로 `float` vector / matrix로 변환하는 것을 권장한다.

### 8.4 auto-conversion
자동 형변환에 의존할 수는 있으나, FPMarkets v2 실무 계약은 **명시적 float32 정렬 후 전달**을 권장한다.  
입력 타입 혼선을 디버깅 포인트로 남기지 않기 위함이다.

---

## 9. Frozen input index map

아래 순서가 **절대 순서**다.

```text
00. log_return_1
01. log_return_3
02. hl_range
03. close_open_ratio
04. gap_percent
05. close_prev_close_ratio
06. return_zscore_20
07. hl_zscore_50
08. overnight_return
09. return_1_over_atr_14
10. close_ema20_ratio
11. close_ema50_ratio
12. ema9_ema20_diff
13. ema20_ema50_diff
14. ema50_ema200_diff
15. ema20_ema50_spread_zscore_50
16. sma50_sma200_ratio
17. rsi_14
18. rsi_50
19. rsi_14_slope_3
20. rsi_14_minus_50
21. stoch_kd_diff
22. stochrsi_kd_diff
23. ppo_hist_12_26_9
24. roc_12
25. trix_15
26. atr_14
27. atr_50
28. atr_14_over_atr_50
29. bollinger_width_20
30. bb_position_20
31. bb_squeeze
32. historical_vol_20
33. historical_vol_5_over_20
34. adx_14
35. di_spread_14
36. supertrend_10_3
37. vortex_indicator
38. is_us_cash_open
39. minutes_from_cash_open
40. is_first_30m_after_open
41. is_last_30m_before_cash_close
42. vix_change_1
43. vix_zscore_20
44. us10yr_change_1
45. us10yr_zscore_20
46. usdx_change_1
47. usdx_zscore_20
48. nvda_xnas_log_return_1
49. aapl_xnas_log_return_1
50. msft_xnas_log_return_1
51. amzn_xnas_log_return_1
52. mega8_equal_return_1
53. top3_weighted_return_1
54. mega8_pos_breadth_1
55. mega8_dispersion_5
56. us100_minus_mega8_equal_return_1
57. us100_minus_top3_weighted_return_1
```

총 입력 수: **58**

---

## 10. Feature class별 MT5 구현 책임

### 10.1 OHLC 직접 계산 가능
다음은 rates 데이터만으로 가능:

- `log_return_1`
- `log_return_3`
- `hl_range`
- `close_open_ratio`
- `gap_percent`
- `close_prev_close_ratio`
- `roc_12`
- 일부 session-independent ratio/spread 항목

### 10.2 built-in indicator handle 우선
다음은 MT5 built-in handle 우선:

- EMA / SMA 계열
- RSI 계열
- ATR 계열
- Bollinger 계열
- ADX / DI 계열
- Stochastic 계열

### 10.3 custom implementation required
다음은 custom implementation 또는 custom indicator 필요:

- `stochrsi_kd_diff`
- `ppo_hist_12_26_9`
- `trix_15`
- `supertrend_10_3`
- `vortex_indicator`
- breadth aggregate 계열
- session-aware `overnight_return`

---

## 11. 외부 심볼 동기화 계약

### 11.1 required symbols
FPMarkets v2 기준 후보:

- proxies: `VIX`, `US10YR`, `USDX`
- leaders: `NVDA`, `AAPL`, `MSFT`, `AMZN`
- breadth extras: `AMD`, `GOOGL`, `META`, `TSLA`

### 11.2 strict timestamp alignment
대상 inference timestamp `T`에 대해, 각 외부 심볼의 사용 row도 동일하게 `T`여야 한다.

### 11.3 skip conditions
아래 중 하나라도 발생하면 skip:

- symbol not selected / unavailable
- rates insufficient
- latest closed timestamp mismatch
- same-session exact close row 없음
- breadth constituent 일부 누락
- weight table 누락

### 11.4 no silent degradation
필수 외부 feature가 빠졌다고 해서 일부 feature만 0으로 채우고 진행하지 않는다.  
그 bar는 **skip**이 기본값이다.

---

## 12. session feature runtime contract

### 12.1 timezone basis
세션 계산의 기준 시간대는 `America/New_York`다.  
서버 시간이나 로컬 PC 시간을 직접 기준으로 삼지 않는다.

### 12.2 required session outputs
- `is_us_cash_open`
- `minutes_from_cash_open`
- `is_first_30m_after_open`
- `is_last_30m_before_cash_close`
- `overnight_return`

### 12.3 DST handling
서머타임 전환 주간에도 세션 flag가 깨지지 않아야 한다.  
이 부분은 별도 parity test 항목이다.

---

## 13. ONNX runtime 호출 계약

### 13.1 expected runtime sequence
권장 순서:

1. `OnnxCreate(...)`
2. input/output info 확인
3. `OnnxSetInputShape(...)`
4. `OnnxSetOutputShape(...)`
5. feature vector 준비
6. `OnnxRun(...)`
7. output 해석
8. 필요 시 session release

### 13.2 shape mismatch
shape mismatch, tensor count mismatch, run failure가 나면 즉시 추론 실패 처리하고 reason code를 남긴다.

### 13.3 one model version, one contract
ONNX 파일, feature order, parser version, output interpretation은 같은 artifact family여야 한다.

---

## 14. Output interpretation contract

### 14.1 default recommended output head
FPMarkets v2 권장 기본형:

- output vector length = 3
- order = `[p_short, p_flat, p_long]`

### 14.2 default decision fields
Base 메모를 반영한 최소 decision field:

- `short_threshold`
- `long_threshold`
- `min_margin`

### 14.3 default decision logic
권장 기본 해석:

- long 진입 후보: `p_long >= long_threshold`
- short 진입 후보: `p_short >= short_threshold`
- 추가 조건: 선택된 방향 확률이 다른 방향 최대값보다 `min_margin` 이상 커야 함
- 미충족 시 no-trade

### 14.4 versioning rule
output order 또는 의미가 바뀌면 input-order contract와 별도로 **output contract 버전**을 올린다.

---

## 15. Inference skip / fail-safe policy

### 15.1 skip is valid
아래 상황에서 추론을 하지 않는 것은 정상 동작이다.

- warmup 부족
- indicator buffer not ready
- external data mismatch
- session conversion failure
- ONNX run failure
- feature NaN / inf 검출

### 15.2 mandatory numeric audit
입력 직전 아래를 검사한다.

- `isfinite` for all 58 features
- NaN 없음
- inf 없음
- feature count 일치
- order hash 일치

### 15.3 fail-safe action
검사 실패 시:

- trade action = none
- inference result = invalid
- reason code 기록

---

## 16. 권장 로그 포인트

매 inference cycle마다 최소 아래를 남긴다.

- `timestamp_utc`
- `timestamp_ny`
- `symbol`
- `timeframe`
- `model_version`
- `parser_version`
- `feature_order_version`
- `row_ready`
- `skip_reason`
- `input_hash`
- `output_raw`
- `decision`
- `position_state_before`
- `position_state_after`

디버그 모드에서는 feature vector 전체도 저장 가능하게 한다.

---

## 17. Python ↔ MT5 parity audit

EA 출시 전 반드시 아래를 확인한다.

1. 동일 bar 500개 이상에 대해 feature vector 비교
2. 각 feature 절대 오차 / 상대 오차 허용치 정의
3. session feature exact match 확인
4. external merge timestamp exact match 확인
5. breadth aggregate exact match 확인
6. input order hash 동일성 확인
7. ONNX single-sample inference 결과 Python vs MT5 비교

권장 허용치 예시:

- float-derived continuous feature: `abs_diff <= 1e-5` 수준부터 시작
- binary flag feature: exact match
- session minute feature: exact match

---

## 18. 권장 구조체 / 내부 표현

권장 내부 표현:

- `double raw_features[58]` 또는 동등 컨테이너
- `float model_input[1][58]` 또는 동등 컨테이너
- `float model_output[1][3]` for default 3-class head

단, 실제 MQL5 구현 세부 문법은 코드 레벨에서 확정한다.

---

## 19. 변경 금지 항목

아래는 임의 수정 금지다.

- feature index 의미
- closed-bar only 규칙
- external exact-timestamp alignment 원칙
- all-or-skip 정책
- input tensor feature count
- session timezone 기준

바꾸려면 새 contract 버전을 발행해야 한다.

---

## 20. 런타임 승인 체크리스트

실전/포워드 테스트 투입 전 체크:

- [ ] ONNX model loads successfully
- [ ] input shape = `[1, 58]`
- [ ] output shape matches selected head
- [ ] all built-in handles valid
- [ ] custom feature modules parity-tested
- [ ] external symbol availability confirmed
- [ ] top3 weight table loaded
- [ ] DST week session test passed
- [ ] feature order hash matches training artifact
- [ ] skip reasons are logged and visible

---

## 21. FPMarkets v2 change notes

- `VXN` 관련 feature 3개는 런타임 계약에서 제거되었다.
- external proxy block은 `VIX`, `US10YR`, `USDX`로 재정렬되었다.
- breadth basket의 `AVGO`는 `AMD`로 교체되었고, 이 버전의 frozen basket은 `{AAPL, AMZN, AMD, GOOGL, META, MSFT, NVDA, TSLA}`다.
- input tensor shape는 `[1, 58]`이다.

---

## 22. 최종 요약

이 문서의 핵심은 아래 한 줄이다.

> MT5 EA input-order contract는 “모델을 실행하는 코드 규칙”이 아니라, Python에서 학습된 입력 의미를 MT5 런타임에 **같은 순서와 같은 시점**으로 재현하기 위한 실행 계약서다.
