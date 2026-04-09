# Stage 24 Brief

- stage: `24_gated_specialist_overlay`
- reviewed_on: `2026-04-09`
- operating_seed: `23A_22q_base_stateexit_ref_0001`
- roadmap_rank: `2`
- proposal_lineage: `Claude gated specialist overlay`

## Purpose

Test whether the old `17C` short specialist becomes useful when it is used as a `short entry gate` on top of the current regular baseline, instead of being blended into the main output stream.

The stage is deliberately narrow:

- keep the current regular baseline logic from `23A`
- leave long entries untouched
- only suppress short entries when the `17C_2501_short_specialist_0001` model is not supportive enough

## Why This Stage Exists

- Stage 20 showed that `specialist mixture` did not beat the `18E_reference` line.
- That result closes the `blend outputs together` path, not the `use a specialist as a direction-specific guard` path.
- `17C` was designed as a short specialist, so the most faithful retry is to use it only where it claims to be strong: short entry confirmation.

## Wave 1 Hypotheses

1. Mild specialist confirmation may remove weak shorts without choking the whole strategy.
2. A medium gate may improve OOS drawdown if the current baseline still over-fires marginal shorts.
3. An aggressive gate may over-prune the short book, but it is worth measuring because the old specialist is structurally short-biased.

## Wave 1 Parameter Anchors

The gate thresholds are anchored to the offline distribution of `17C` short probabilities on bars where the `23A` baseline would already choose a short.

- `aux_short >= 0.40` keeps about two thirds of baseline short decisions on both validation and test, so it is the mild arm.
- `aux_short >= 0.45` keeps about forty percent of short decisions, so it is the medium arm.
- `aux_short >= 0.50` keeps about one quarter of short decisions, so it is the aggressive arm.

## Planned Runs

- `24A`: regular baseline carry-forward from `23A`
- `24B`: `specialist_short_gate(min_aux_short_probability=0.40)`
- `24C`: `specialist_short_gate(min_aux_short_probability=0.45)`
- `24D`: `specialist_short_gate(min_aux_short_probability=0.50)`

## Promotion Rule

- do not promote on OOS return alone
- keep the incumbent unless the gate improves the regular OOS read without obvious historical or validation collapse
- judge the gate using both headline metrics and explanation metrics:
  `gate reject count`, `short signal reduction`, and `aux short probability distribution`
