#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parents[3]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from foundation.pipelines.stage_reporting import code, render_markdown_table, write_json, write_markdown  # noqa: E402


STAGE_DIR = Path(__file__).resolve().parents[1]
ACTIVE_RUNS_DIR = STAGE_DIR / "02_runs" / "active"
REVIEW_PATH = STAGE_DIR / "03_reviews" / "stage28_event_retrain_wave2_20260410.md"
REVIEW_JSON_PATH = STAGE_DIR / "03_reviews" / "stage28_event_retrain_wave2_20260410.json"
REVIEW_INDEX_PATH = STAGE_DIR / "03_reviews" / "review_index.md"
SELECTION_PATH = STAGE_DIR / "04_selected" / "selection_status.md"

RUNS = [
    ("28E", "28E_28b_fixedcarry_long14m_0001"),
    ("28F", "28F_28b_2m_monthly_long14m_0001"),
    ("28G", "28G_28b_negpf_trigger_long14m_0001"),
]


def load_summary(run_name: str) -> dict:
    path = ACTIVE_RUNS_DIR / run_name / "stitched_summary.json"
    if not path.exists():
        raise FileNotFoundError(f"missing stitched summary: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def headline(payload: dict) -> dict:
    return payload["stitched_financial_metrics"]["headline"]


def governance(payload: dict) -> dict:
    return payload["stitched_governance_metrics"]


def choose_shadow(runs: dict[str, dict], incumbent_code: str) -> str | None:
    candidate_codes = [code for code in runs if code != incumbent_code]
    if not candidate_codes:
        return None

    def score(code_value: str) -> tuple[float, float]:
        h = headline(runs[code_value])
        return float(h.get("return_pct") or -10**9), -(float(h.get("max_dd_pct") or 10**9))

    return max(candidate_codes, key=score)


def main() -> int:
    payloads = {code: load_summary(run_name) for code, run_name in RUNS}
    fixed = payloads["28E"]
    fixed_headline = headline(fixed)
    event_headline = headline(payloads["28G"])
    monthly_headline = headline(payloads["28F"])

    keep_fixed = True
    lineage_followup = None
    if (event_headline.get("return_pct") or -10**9) > (fixed_headline.get("return_pct") or -10**9) and (
        event_headline.get("max_dd_pct") or 10**9
    ) <= (fixed_headline.get("max_dd_pct") or 10**9) * 1.08:
        keep_fixed = False
        lineage_followup = "28G"
    elif (monthly_headline.get("return_pct") or -10**9) > (fixed_headline.get("return_pct") or -10**9) and (
        monthly_headline.get("max_dd_pct") or 10**9
    ) <= (fixed_headline.get("max_dd_pct") or 10**9) * 1.08:
        keep_fixed = False
        lineage_followup = "28F"

    shadow_code = choose_shadow(payloads, "28E")
    decision = "keep_fixed_carry_reference" if keep_fixed else "reopen_event_retrain_followup"

    scoreboard_rows = []
    for code_value, run_name in RUNS:
        payload = payloads[code_value]
        head = headline(payload)
        gov = governance(payload)
        scoreboard_rows.append(
            [
                code(code_value),
                code(head.get("return_pct")),
                code(head.get("profit_factor"), digits=4),
                code(head.get("trade_count")),
                code(head.get("max_dd_pct"), digits=4),
                code(payload.get("positive_months")),
                code(payload.get("retrain_month_count")),
                code(gov.get("latest_state")),
                code(gov.get("max_external_skip_rate"), digits=4),
            ]
        )

    review_payload = {
        "reviewed_on": "2026-04-10",
        "wave": "event_triggered_retrain_wave1",
        "regular_operating_reference_unchanged": "27A_26a_volref_0001",
        "lineage_reference": "28B_18e_persist48_ph20_0001",
        "decision": decision,
        "fixed_carry_reference": "28E_28b_fixedcarry_long14m_0001",
        "best_shadow_candidate": payloads[shadow_code]["run_name"] if shadow_code else None,
        "lineage_followup_candidate": payloads[lineage_followup]["run_name"] if lineage_followup else None,
        "scoreboard": {
            code_value: {
                "run_name": payloads[code_value]["run_name"],
                "return_pct": headline(payloads[code_value]).get("return_pct"),
                "profit_factor": headline(payloads[code_value]).get("profit_factor"),
                "trade_count": headline(payloads[code_value]).get("trade_count"),
                "max_dd_pct": headline(payloads[code_value]).get("max_dd_pct"),
                "positive_months": payloads[code_value].get("positive_months"),
                "retrain_month_count": payloads[code_value].get("retrain_month_count"),
            }
            for code_value in payloads
        },
    }
    write_json(REVIEW_JSON_PATH, review_payload)

    lines = [
        "# Stage 28 Event-Triggered Retrain Wave 1",
        "",
        "- reviewed_on: `2026-04-10`",
        "- purpose: `test whether the reopened 28B compact lineage behaves better under bounded month-level retrain triggers than under blind monthly cadence`",
        "- lineage_reference: `28B_18e_persist48_ph20_0001`",
        "- operating_reference_unchanged: `27A_26a_volref_0001`",
        "",
        "## Scoreboard",
        "",
        *render_markdown_table(
            ["run", "return_pct", "pf", "trades", "max_dd_pct", "positive_months", "retrain_months", "gov_state", "max_ext_skip"],
            scoreboard_rows,
        ),
        "",
        "## Headline",
        "",
        f"- fixed carry `28E`: return_pct {code(fixed_headline.get('return_pct'))}, PF {code(fixed_headline.get('profit_factor'), digits=4)}, trades {code(fixed_headline.get('trade_count'))}, max_dd_pct {code(fixed_headline.get('max_dd_pct'), digits=4)}",
        f"- monthly retrain `28F`: return_pct {code(monthly_headline.get('return_pct'))}, PF {code(monthly_headline.get('profit_factor'), digits=4)}, trades {code(monthly_headline.get('trade_count'))}, max_dd_pct {code(monthly_headline.get('max_dd_pct'), digits=4)}",
        f"- event trigger `28G`: return_pct {code(event_headline.get('return_pct'))}, PF {code(event_headline.get('profit_factor'), digits=4)}, trades {code(event_headline.get('trade_count'))}, max_dd_pct {code(event_headline.get('max_dd_pct'), digits=4)}",
        "",
        "## Diagnostics",
        "",
        f"- fixed carry retrain_months: {code(fixed.get('retrain_month_count'))}",
        f"- monthly retrain retrain_months: {code(payloads['28F'].get('retrain_month_count'))}",
        f"- event trigger retrain_months: {code(payloads['28G'].get('retrain_month_count'))}",
        f"- event trigger months: {code(', '.join(payloads['28G'].get('retrain_months') or []))}",
        "",
        "## Execution",
        "",
        f"- fixed carry governance latest: {code(governance(fixed).get('latest_state'))}, max_external_skip_rate {code(governance(fixed).get('max_external_skip_rate'), digits=4)}",
        f"- monthly retrain governance latest: {code(governance(payloads['28F']).get('latest_state'))}, max_external_skip_rate {code(governance(payloads['28F']).get('max_external_skip_rate'), digits=4)}",
        f"- event trigger governance latest: {code(governance(payloads['28G']).get('latest_state'))}, max_external_skip_rate {code(governance(payloads['28G']).get('max_external_skip_rate'), digits=4)}",
        "",
        "## Decision",
        "",
        f"- decision: `{decision}`",
        f"- fixed_carry_reference: `28E_28b_fixedcarry_long14m_0001`",
        f"- shadow_candidate: `{payloads[shadow_code]['run_name'] if shadow_code else 'n/a'}`",
        f"- lineage_followup_candidate: `{payloads[lineage_followup]['run_name'] if lineage_followup else 'none'}`",
    ]
    write_markdown(REVIEW_PATH, lines, bom=True)

    review_index_lines = [
        "# Review Index",
        "",
        "- latest_review: `stage28_event_retrain_wave2_20260410.md`",
        f"- best_compact_code: `{lineage_followup or '28E'}`",
        f"- lineage_status: `{decision}`",
        "- current_regular_reference_unchanged: `27A_26a_volref_0001`",
        "",
        "## Wave Reviews",
        "",
        "- `wave1_feature_simplification`: `stage28_feature_wave1_20260409.md`",
        "- `wave2_event_triggered_retrain`: `stage28_event_retrain_wave2_20260410.md`",
    ]
    write_markdown(REVIEW_INDEX_PATH, review_index_lines, bom=True)

    selection_lines = [
        "# Selection Status",
        "",
        "- stage: `28_retrain_feature_checks`",
        "- wave: `event_triggered_retrain_wave1`",
        "- status: `completed`",
        "- lineage_reference: `28B_18e_persist48_ph20_0001`",
        "- fixed_carry_reference: `28E_28b_fixedcarry_long14m_0001`",
        f"- best_shadow_candidate: `{payloads[shadow_code]['run_name'] if shadow_code else 'n/a'}`",
        f"- lineage_followup_candidate: `{payloads[lineage_followup]['run_name'] if lineage_followup else 'none'}`",
        f"- decision: `{decision}`",
        "- operating_reference_unchanged: `27A_26a_volref_0001`",
        "- interpretation: `Stage 28 remains a lineage follow-up lane; use the wave to decide whether bounded retrain logic adds value on top of compact 28B, not to override the live regular lane directly.`",
    ]
    write_markdown(SELECTION_PATH, selection_lines, bom=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
