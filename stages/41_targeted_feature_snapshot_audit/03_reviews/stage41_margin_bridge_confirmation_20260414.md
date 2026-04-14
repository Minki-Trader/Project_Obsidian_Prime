# Stage 41 Margin Bridge Confirmation

- reviewed_on_utc: `2026-04-14T23:03:56.612119+00:00`
- replay surface: `34D extended bridge contract-aligned confirmation on 2024.01.01 -> 2026.04.13`
- comparison: `baseline min_margin=0.06750` versus `candidate min_margin=0.06000`

## Executive Read

- the broader extended-bridge confirmation keeps `34D min_margin=0.06000` as the best tested contract-aligned operating candidate
- candidate versus contract baseline: `net=834.45` `return_pct=166.890` `trade_count=200` `pf=0.0113` `max_dd_pct=-0.4561` `ulcer=-1.6069` `long=242` `short=334` `no_trade=-576` `external_mismatch=0`
- candidate versus built-in bridge reference: `net=-712.76` `return_pct=-142.552` `trade_count=17` `pf=-0.0220` `max_dd_pct=4.2402` `ulcer=1.5700` `long=-280` `short=171` `no_trade=109` `external_mismatch=0`

## References

- built-in bridge reference `34D` `min_margin=0.0675` `net=2950.79` `return_pct=590.158` `trade_count=1134` `pf=1.3025` `max_dd_pct=20.2308`

## Contract-Aligned Bridge Results

- `34D contract bridge 0.06750` `min_margin=0.06750` `net=1403.58` `return_pct=280.716` `trade_count=951` `pf=1.2692` `max_dd_pct=24.9270` `ulcer=10.3144` `long=767` `short=1492` `no_trade=32404` `external_mismatch=53733`
- `34D contract bridge 0.06000` `min_margin=0.06000` `net=2238.03` `return_pct=447.606` `trade_count=1151` `pf=1.2805` `max_dd_pct=24.4710` `ulcer=8.7075` `long=1009` `short=1826` `no_trade=31828` `external_mismatch=53733`

## Candidate Read

- `34D contract bridge 0.06000` `min_margin=0.06000` `net=2238.03` `return_pct=447.606` `trade_count=1151` `pf=1.2805` `max_dd_pct=24.4710` `ulcer=8.7075` `long=1009` `short=1826` `no_trade=31828` `external_mismatch=53733`
- versus contract baseline `net=834.45` `return_pct=166.890` `trade_count=200` `pf=0.0113` `max_dd_pct=-0.4561` `ulcer=-1.6069` `long=242` `short=334` `no_trade=-576` `external_mismatch=0`
- versus built-in bridge reference `net=-712.76` `return_pct=-142.552` `trade_count=17` `pf=-0.0220` `max_dd_pct=4.2402` `ulcer=1.5700` `long=-280` `short=171` `no_trade=109` `external_mismatch=0`

## Interpretation

- this check answers a broader operating question than the latest-window replay: whether the relaxed contract-aligned margin gate can survive a carried multi-year bridge rather than only a short recent slice
- the evidence now says the `0.06000` candidate is not only a latest-window patch; it also survives the wider carried contract-aligned bridge better than the contract baseline
- this still does not replace the built-in bridge as the current best absolute line by itself; it only tests whether the best contract-aligned candidate improves the carried contract-aligned lane
