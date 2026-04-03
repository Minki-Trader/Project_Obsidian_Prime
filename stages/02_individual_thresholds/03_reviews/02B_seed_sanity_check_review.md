# 02B Seed Sanity Check Review

Generated at: `2026-03-28T04:43:19.354558+00:00`

## Scope

- purpose: `sanity-check whether the selected 02A threshold seed is too directionally collapsed to carry forward blindly`
- method: `compare the raw-return leader against a balanced challenger drawn from the existing 02A result table`
- this stays inside threshold-only logic; no margin rule or probability-gap rule is introduced here

## Guardrail

- balanced challenger minimum direction trades: `100`
- balanced challenger minimum minority share: `0.20`
- promotion threshold: keep at least `85%` of the raw-return leader compounded return

## Overall Best

- `(Ts=0.60, Tl=0.40)`: compounded_return=`0.1342`, trades=`925`, longs=`915`, shorts=`10`, minority_share=`0.011`

## Balanced Challenger

- `(Ts=0.45, Tl=0.50)`: compounded_return=`0.0914`, trades=`573`, longs=`183`, shorts=`390`, minority_share=`0.319`
- balanced challenger return ratio vs raw-return leader: `0.681`

## Verdict

- verdict: `keep current 02A seed; balanced challenger stays as reference`
- read: the selected seed is highly long-skewed, but the best genuinely two-sided challenger gives up too much compounded return to replace it at this stage.
- carry-forward implication: keep the current 02A seed as the preferred raw threshold seed, but preserve the balanced challenger as the main alternate if later confirmation penalizes one-sided behavior.

## Shortlist

- overall `(Ts=0.60, Tl=0.40)`: compounded_return=0.1342, trades=925, longs=915, shorts=10, minority_share=0.011, max_drawdown=-0.0759
- overall `(Ts=0.55, Tl=0.40)`: compounded_return=0.1254, trades=946, longs=903, shorts=43, minority_share=0.045, max_drawdown=-0.0759
- overall `(Ts=0.55, Tl=0.35)`: compounded_return=0.1245, trades=1622, longs=1581, shorts=41, minority_share=0.025, max_drawdown=-0.0984
- overall `(Ts=0.65, Tl=0.40)`: compounded_return=0.1231, trades=920, longs=917, shorts=3, minority_share=0.003, max_drawdown=-0.0759
- overall `(Ts=0.65, Tl=0.35)`: compounded_return=0.0974, trades=1606, longs=1603, shorts=3, minority_share=0.002, max_drawdown=-0.1004
- overall `(Ts=0.45, Tl=0.50)`: compounded_return=0.0914, trades=573, longs=183, shorts=390, minority_share=0.319, max_drawdown=-0.0667
- overall `(Ts=0.60, Tl=0.35)`: compounded_return=0.0820, trades=1609, longs=1600, shorts=9, minority_share=0.006, max_drawdown=-0.1115
- overall `(Ts=0.50, Tl=0.40)`: compounded_return=0.0460, trades=994, longs=856, shorts=138, minority_share=0.139, max_drawdown=-0.0867
- overall `(Ts=0.65, Tl=0.45)`: compounded_return=0.0459, trades=444, longs=441, shorts=3, minority_share=0.007, max_drawdown=-0.0815
- overall `(Ts=0.50, Tl=0.55)`: compounded_return=0.0455, trades=234, longs=88, shorts=146, minority_share=0.376, max_drawdown=-0.0928
- overall `(Ts=0.60, Tl=0.45)`: compounded_return=0.0404, trades=451, longs=441, shorts=10, minority_share=0.022, max_drawdown=-0.0821
- overall `(Ts=0.55, Tl=0.50)`: compounded_return=0.0350, trades=241, longs=190, shorts=51, minority_share=0.212, max_drawdown=-0.0747
