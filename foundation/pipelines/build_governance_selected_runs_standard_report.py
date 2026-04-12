#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path
from typing import Any

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from foundation.pipelines.stage_reporting import code, render_markdown_table, write_json, write_markdown


SOURCE_JSON = ROOT_DIR / "tmp" / "analysis" / "governance_selected_runs_deep_20260408.json"
STAMP = date.today().strftime("%Y%m%d")
OUTPUT_JSON = ROOT_DIR / "foundation" / "reports" / f"governance_selected_runs_standard_{STAMP}.json"
OUTPUT_MD = ROOT_DIR / "foundation" / "reports" / f"governance_selected_runs_standard_{STAMP}.md"


def rounded(value: Any, digits: int = 3) -> Any:
    if value is None:
        return "n/a"
    if isinstance(value, float):
        return round(value, digits)
    return value


def top_reason_string(reason_map: dict[str, int], limit: int = 3) -> str:
    ranked = sorted(reason_map.items(), key=lambda item: (-item[1], item[0]))
    if not ranked:
        return "n/a"
    return ", ".join(f"{name}:{count}" for name, count in ranked[:limit])


def load_summary(summary_path: str) -> dict[str, Any]:
    return json.loads(Path(summary_path).read_text(encoding="utf-8"))


def normalize_record(record: dict[str, Any]) -> dict[str, Any]:
    summary = load_summary(record["summary_path"])
    financial = summary["financial_metrics"]
    metrics = summary.get("metrics", {})
    headline = financial["headline"]
    risk = financial["risk"]
    diagnostics = financial["diagnostics"]
    execution = financial["execution"]

    return {
        "code": record["code"],
        "window": {
            "from_date": record["from_date"],
            "to_date": record["to_date"],
        },
        "headline": {
            "return_pct": rounded(headline.get("return_pct")),
            "profit_factor": rounded(headline.get("profit_factor"), 4),
            "max_dd_pct": rounded(headline.get("max_dd_pct")),
            "trade_count": headline.get("trade_count", "n/a"),
        },
        "risk": {
            "ulcer_index": rounded(risk.get("ulcer_index")),
            "worst_week": rounded(risk.get("worst_week")),
            "consecutive_losses": risk.get("consecutive_losses", "n/a"),
            "min_free_margin": rounded(risk.get("min_free_margin"), 2),
        },
        "diagnostics": {
            "no_trade_rate": rounded(diagnostics.get("no_trade_rate"), 4),
            "long_count": diagnostics.get("long_count", "n/a"),
            "short_count": diagnostics.get("short_count", "n/a"),
            "long_expectancy": rounded(diagnostics.get("long_expectancy")),
            "short_expectancy": rounded(diagnostics.get("short_expectancy")),
        },
        "execution": {
            "skip_rate": rounded(
                (metrics.get("skip_row_count", 0) / metrics.get("row_count")) if metrics.get("row_count") else None,
                4,
            ),
            "external_mismatch_count": metrics.get("external_mismatch_count", "n/a"),
            "fill_rate": rounded(execution.get("fill_rate"), 4),
            "data_readiness_failures": metrics.get("data_readiness_failures", "n/a"),
            "broker_constraint_events": execution.get("broker_constraint_events", "n/a"),
            "ready_row_gap": record.get("ready_row_gap", "n/a"),
            "ready_rate": rounded(metrics.get("ready_rate", record.get("ready_rate")), 4),
            "mean_external_skip_rate": rounded(record.get("mean_external_skip_rate"), 4),
            "latest_external_skip_rate": rounded(record.get("latest_external_skip_rate"), 4),
            "mean_argmax_share": rounded(record.get("mean_argmax_share"), 4),
            "p90_argmax_share": rounded(record.get("p90_argmax_share"), 4),
            "mean_entropy": rounded(record.get("mean_entropy"), 4),
            "p10_entropy": rounded(record.get("p10_entropy"), 4),
            "mean_risk_overlay_rate": rounded(record.get("mean_risk_overlay_rate"), 4),
            "latest_risk_overlay_rate": rounded(record.get("latest_risk_overlay_rate"), 4),
            "latest_governance_reason": record.get("latest_gov_reason") or "n/a",
            "top_skip_reasons": top_reason_string(record.get("top_skip_reasons", {})),
            "top_governance_reasons": record.get("top_gov_reasons") or [],
        },
        "source": {
            "summary_path": record["summary_path"],
            "governance_csv": record["governance_csv"],
        },
    }


def build_markdown(records: list[dict[str, Any]]) -> list[str]:
    lines = [
        "# Governance Selected Runs Standard Report",
        "",
        f"- reviewed_on: `{date.today().isoformat()}`",
        "- purpose: `keep a null-free comparison board for selected incumbents and reference runs`",
        "- source: `tmp/analysis/governance_selected_runs_deep_20260408.json + each attempt summary financial_metrics`",
        "",
        "## Summary Board",
        "",
    ]

    rows: list[list[str]] = []
    for record in records:
        headline = record["headline"]
        diagnostics = record["diagnostics"]
        execution = record["execution"]
        rows.append(
            [
                code(record["code"]),
                code(f"{record['window']['from_date']}..{record['window']['to_date']}"),
                code(headline["return_pct"]),
                code(headline["profit_factor"], digits=4),
                code(headline["max_dd_pct"]),
                code(headline["trade_count"], digits=0),
                code(diagnostics["no_trade_rate"], digits=4),
                code(f"{diagnostics['long_count']}/{diagnostics['short_count']}"),
                code(execution["mean_external_skip_rate"], digits=4),
                code(execution["mean_argmax_share"], digits=4),
                code(execution["mean_entropy"], digits=4),
                code(execution["mean_risk_overlay_rate"], digits=4),
                code(execution["top_skip_reasons"]),
            ]
        )
    lines.extend(
        render_markdown_table(
            [
                "code",
                "window",
                "return_pct",
                "pf",
                "max_dd_pct",
                "trades",
                "no_trade_rate",
                "long/short",
                "ext_skip_mean",
                "argmax_mean",
                "entropy_mean",
                "overlay_mean",
                "top_skip_reasons",
            ],
            rows,
        )
    )

    lines.extend(
        [
            "",
            "## Read Rule",
            "",
            "- `headline` answers how the run performed.",
            "- `risk` answers how painful the path was.",
            "- `diagnostics` answers how selective or directional the run was.",
            "- `execution` answers whether the environment / telemetry picture stayed comparable.",
        ]
    )

    for record in records:
        headline = record["headline"]
        risk = record["risk"]
        diagnostics = record["diagnostics"]
        execution = record["execution"]
        lines.extend(
            [
                "",
                f"## {record['code']}",
                "",
                f"- window: `{record['window']['from_date']} .. {record['window']['to_date']}`",
                "",
                "### Headline",
                "",
                f"- return_pct: `{headline['return_pct']}`",
                f"- profit_factor: `{headline['profit_factor']}`",
                f"- trade_count: `{headline['trade_count']}`",
                f"- max_dd_pct: `{headline['max_dd_pct']}`",
                "",
                "### Risk",
                "",
                f"- ulcer_index: `{risk['ulcer_index']}`",
                f"- worst_week: `{risk['worst_week']}`",
                f"- consecutive_losses: `{risk['consecutive_losses']}`",
                f"- min_free_margin: `{risk['min_free_margin']}`",
                "",
                "### Diagnostics",
                "",
                f"- no_trade_rate: `{diagnostics['no_trade_rate']}`",
                f"- long_short_mix: `{diagnostics['long_count']}/{diagnostics['short_count']}`",
                f"- long_expectancy: `{diagnostics['long_expectancy']}`",
                f"- short_expectancy: `{diagnostics['short_expectancy']}`",
                "",
                "### Execution",
                "",
                f"- skip_rate: `{execution['skip_rate']}`",
                f"- external_mismatch_count: `{execution['external_mismatch_count']}`",
                f"- fill_rate: `{execution['fill_rate']}`",
                f"- ready_row_gap: `{execution['ready_row_gap']}`",
                f"- mean_external_skip_rate: `{execution['mean_external_skip_rate']}`",
                f"- latest_external_skip_rate: `{execution['latest_external_skip_rate']}`",
                f"- mean_argmax_share: `{execution['mean_argmax_share']}`",
                f"- p90_argmax_share: `{execution['p90_argmax_share']}`",
                f"- mean_entropy: `{execution['mean_entropy']}`",
                f"- p10_entropy: `{execution['p10_entropy']}`",
                f"- mean_risk_overlay_rate: `{execution['mean_risk_overlay_rate']}`",
                f"- latest_risk_overlay_rate: `{execution['latest_risk_overlay_rate']}`",
                f"- latest_governance_reason: `{execution['latest_governance_reason']}`",
                f"- top_skip_reasons: `{execution['top_skip_reasons']}`",
            ]
        )
    return lines


def main() -> int:
    source_records = json.loads(SOURCE_JSON.read_text(encoding="utf-8"))
    records = [normalize_record(record) for record in source_records]
    records.sort(key=lambda item: item["code"])

    payload = {
        "reviewed_on": date.today().isoformat(),
        "source_json": str(SOURCE_JSON),
        "records": records,
    }

    write_json(OUTPUT_JSON, payload)
    write_markdown(OUTPUT_MD, build_markdown(records))
    print(f"[done] json={OUTPUT_JSON}")
    print(f"[done] md={OUTPUT_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
