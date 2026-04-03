# 02D Local Surface Probe Review

Generated at: `2026-03-28T05:04:09.564297+00:00`

## Scope

- purpose: `probe a few local threshold neighborhoods more densely without freezing or promoting a final Stage 02 threshold`
- neighborhoods: `valid leader`, `balanced challenger`, `test-favored pocket`
- local offsets: `-0.050, -0.025, +0.000, +0.025, +0.050`
- this is exploration only; no threshold freeze is made here

## Blended Read

- best both-positive blended pair: `(Ts=0.575, Tl=0.400)` from `valid_leader`
- valid compounded return: `0.1345`
- test compounded return: `0.0698`
- average compounded return: `0.1021`

## Test-Favored Pocket

- strongest test pair inside the local probe: `(Ts=0.350, Tl=0.400)` from `test_favored`
- valid compounded return: `-0.0879`
- test compounded return: `0.2212`
- average compounded return: `0.0666`

## Balanced Region Read

- strongest balanced-region pair inside the local probe: `(Ts=0.450, Tl=0.500)`
- valid compounded return: `0.0914`
- test compounded return: `0.0838`
- average compounded return: `0.0876`

## Top Blended Reads

- `valid_leader` `(Ts=0.575, Tl=0.400)`: valid_comp=0.1345, test_comp=0.0698, avg_comp=0.1021, gap=0.0647
- `valid_leader` `(Ts=0.550, Tl=0.400)`: valid_comp=0.1254, test_comp=0.0720, avg_comp=0.0987, gap=0.0534
- `valid_leader` `(Ts=0.600, Tl=0.400)`: valid_comp=0.1342, test_comp=0.0554, avg_comp=0.0948, gap=0.0788
- `balanced_challenger` `(Ts=0.450, Tl=0.500)`: valid_comp=0.0914, test_comp=0.0838, avg_comp=0.0876, gap=0.0075
- `valid_leader` `(Ts=0.625, Tl=0.400)`: valid_comp=0.1231, test_comp=0.0496, avg_comp=0.0864, gap=0.0735
- `valid_leader` `(Ts=0.650, Tl=0.400)`: valid_comp=0.1231, test_comp=0.0496, avg_comp=0.0864, gap=0.0735
- `balanced_challenger` `(Ts=0.450, Tl=0.475)`: valid_comp=0.0882, test_comp=0.0730, avg_comp=0.0806, gap=0.0151
- `valid_leader` `(Ts=0.550, Tl=0.350)`: valid_comp=0.1245, test_comp=0.0349, avg_comp=0.0797, gap=0.0895
- `balanced_challenger` `(Ts=0.500, Tl=0.525)`: valid_comp=0.1275, test_comp=0.0196, avg_comp=0.0736, gap=0.1078
- `valid_leader` `(Ts=0.600, Tl=0.450)`: valid_comp=0.0404, test_comp=0.0571, avg_comp=0.0487, gap=0.0167
- `valid_leader` `(Ts=0.625, Tl=0.450)`: valid_comp=0.0523, test_comp=0.0430, avg_comp=0.0476, gap=0.0093
- `balanced_challenger` `(Ts=0.450, Tl=0.450)`: valid_comp=0.0199, test_comp=0.0708, avg_comp=0.0454, gap=0.0508

## Top Test Reads

- `test_favored` `(Ts=0.350, Tl=0.400)`: valid_comp=-0.0879, test_comp=0.2212, avg_comp=0.0666, gap=0.3091
- `test_favored` `(Ts=0.375, Tl=0.400)`: valid_comp=-0.0090, test_comp=0.1797, avg_comp=0.0853, gap=0.1887
- `test_favored` `(Ts=0.350, Tl=0.375)`: valid_comp=-0.1662, test_comp=0.1736, avg_comp=0.0037, gap=0.3398
- `test_favored` `(Ts=0.300, Tl=0.400)`: valid_comp=-0.1018, test_comp=0.1691, avg_comp=0.0337, gap=0.2709
- `test_favored` `(Ts=0.300, Tl=0.350)`: valid_comp=-0.1475, test_comp=0.1690, avg_comp=0.0107, gap=0.3165
- `test_favored` `(Ts=0.350, Tl=0.350)`: valid_comp=-0.0997, test_comp=0.1675, avg_comp=0.0339, gap=0.2672
- `test_favored` `(Ts=0.375, Tl=0.375)`: valid_comp=-0.1083, test_comp=0.1633, avg_comp=0.0275, gap=0.2716
- `test_favored` `(Ts=0.300, Tl=0.375)`: valid_comp=-0.1707, test_comp=0.1588, avg_comp=-0.0059, gap=0.3295
- `test_favored` `(Ts=0.400, Tl=0.400)`: valid_comp=-0.0303, test_comp=0.1541, avg_comp=0.0619, gap=0.1844
- `test_favored` `(Ts=0.350, Tl=0.425)`: valid_comp=-0.1947, test_comp=0.1498, avg_comp=-0.0224, gap=0.3445
- `test_favored` `(Ts=0.325, Tl=0.350)`: valid_comp=-0.1293, test_comp=0.1446, avg_comp=0.0076, gap=0.2739
- `test_favored` `(Ts=0.375, Tl=0.350)`: valid_comp=-0.0635, test_comp=0.1437, avg_comp=0.0401, gap=0.2072

## Verdict

- verdict: `keep exploring; do not freeze yet`
- read: the valid-leader neighborhood still gives the strongest blended both-positive reads, while the test-favored low-threshold pocket remains attractive on test but looks too split-dependent to treat as a stable answer yet.
- implication: if we keep exploring, the next useful small step is to probe a nearby ridge around the blended leader rather than widening the whole Stage 02 search again.
