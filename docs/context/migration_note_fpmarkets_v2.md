# FPMarkets v2 Migration Note

## 목적
이 문서는 기존 초안(v1 계열)에서 현재 FPMarkets MT5 실사용 가능 심볼 기준으로 계약을 어떻게 교체했는지 빠르게 보여준다.

## 핵심 변경
1. `VXN` 관련 feature 삭제
   - removed: `vxn_change_1`
   - removed: `vxn_zscore_20`
   - removed: `vxn_minus_vix`

2. risk proxy block 재설계
   - added: `vix_change_1`
   - added: `vix_zscore_20`
   - renamed/re-scoped: `tnx_*` -> `us10yr_*`
   - renamed/re-scoped: `dxy_*` -> `usdx_*`

3. breadth basket constituent 교체
   - old mega8: `AAPL, AMZN, AVGO, GOOGL, META, MSFT, NVDA, TSLA`
   - new mega8: `AAPL, AMZN, AMD, GOOGL, META, MSFT, NVDA, TSLA`

## 결과
- old feature count: 59
- new feature count: 58
- old input shape: `[1, 59]`
- new input shape: `[1, 58]`

## 해석 규칙
- 이번 교체 버전은 “몰래 대체”가 아니라 **새 버전 계약**이다.
- `US10YR`, `USDX`, `AMD`는 이 버전에서 공식 feature source로 취급한다.
- `VXN` 부재를 억지 spread로 보정하지 않는다.
