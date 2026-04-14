#!/usr/bin/env python3
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


UTC = timezone.utc
ROOT_DIR = Path(__file__).resolve().parents[3]
STAGE_DIR = ROOT_DIR / "stages" / "41_targeted_feature_snapshot_audit"
REVIEW_STEM = STAGE_DIR / "03_reviews" / f"stage41_margin_bridge_confirmation_{datetime.now(tz=UTC).strftime('%Y%m%d')}"

RUN_SPECS = [
    {
        "label": "34D contract bridge 0.06750",
        "family": "34D",
        "min_margin": 0.06750,
        "run_dir": STAGE_DIR / "02_runs" / "active" / "41I_34d_bridge_contract0675_0001",
    },
    {
        "label": "34D contract bridge 0.06000",
        "family": "34D",
        "min_margin": 0.06000,
        "run_dir": STAGE_DIR / "02_runs" / "active" / "41J_34d_bridge_contract0600_0001",
    },
]

REFERENCE_BUILTIN_SUMMARY = (
    ROOT_DIR
    / "stages"
    / "39_window_extension_mt5_validation"
    / "02_runs"
    / "active"
    / "39A_34d_bridge_ext_0001"
    / "mt5_attempts"
    / "att_0002"
    / "tester_attempt_summary.json"
)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def maybe_int(value: Any) -> int | None:
    if value is None:
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def load_summary(path: Path) -> dict[str, Any]:
    payload = load_json(path)
    headline = payload["financial_metrics"]["headline"]
    risk = payload["financial_metrics"]["risk"]
    diagnostics = payload["financial_metrics"]["diagnostics"]
    metrics = payload["metrics"]
    return {
        "summary_path": str(path),
        "attempt_id": payload["attempt_id"],
        "net_profit": float(headline["net_profit"]),
        "return_pct": float(headline["return_pct"]),
        "trade_count": int(headline["trade_count"]),
        "win_rate": float(headline["win_rate"]),
        "profit_factor": float(headline["profit_factor"]),
        "expectancy_per_trade": float(headline["expectancy_per_trade"]),
        "max_dd_pct": float(headline["max_dd_pct"]),
        "ulcer_index": float(risk["ulcer_index"]),
        "long_signal_count": int(metrics["long_signal_count"]),
        "short_signal_count": int(metrics["short_signal_count"]),
        "no_trade_count": int(metrics["no_trade_count"]),
        "external_mismatch_count": maybe_int(metrics.get("external_mismatch_count")),
        "year_breakdown": diagnostics.get("extra", {}).get("calendar_breakdown", {}),
    }


def build_run_record(spec: dict[str, Any]) -> dict[str, Any]:
    summary_path = Path(spec["run_dir"]) / "mt5_attempts" / "att_0001" / "tester_attempt_summary.json"
    record = load_summary(summary_path)
    record.update(
        {
            "label": spec["label"],
            "family": spec["family"],
            "min_margin": float(spec["min_margin"]),
            "run_dir": str(spec["run_dir"]),
        }
    )
    return record


def diff_metrics(candidate: dict[str, Any], reference: dict[str, Any]) -> dict[str, float | int | None]:
    mismatch_left = candidate.get("external_mismatch_count")
    mismatch_right = reference.get("external_mismatch_count")
    mismatch_delta = None
    if mismatch_left is not None and mismatch_right is not None:
        mismatch_delta = int(mismatch_left - mismatch_right)
    return {
        "net_profit_delta": float(candidate["net_profit"] - reference["net_profit"]),
        "return_pct_delta": float(candidate["return_pct"] - reference["return_pct"]),
        "trade_count_delta": int(candidate["trade_count"] - reference["trade_count"]),
        "profit_factor_delta": float(candidate["profit_factor"] - reference["profit_factor"]),
        "max_dd_pct_delta": float(candidate["max_dd_pct"] - reference["max_dd_pct"]),
        "ulcer_index_delta": float(candidate["ulcer_index"] - reference["ulcer_index"]),
        "long_signal_delta": int(candidate["long_signal_count"] - reference["long_signal_count"]),
        "short_signal_delta": int(candidate["short_signal_count"] - reference["short_signal_count"]),
        "no_trade_delta": int(candidate["no_trade_count"] - reference["no_trade_count"]),
        "external_mismatch_delta": mismatch_delta,
    }


def rank_records(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted(
        records,
        key=lambda item: (
            -item["net_profit"],
            -item["profit_factor"],
            item["max_dd_pct"],
            item["ulcer_index"],
        ),
    )


def fmt_num(value: float | int | None, digits: int = 4) -> str:
    if value is None:
        return "n/a"
    if isinstance(value, int):
        return str(value)
    return f"{value:.{digits}f}"


def render_record(record: dict[str, Any]) -> str:
    mismatch = record.get("external_mismatch_count")
    return (
        f"- `{record['label']}` `min_margin={record['min_margin']:.5f}` "
        f"`net={fmt_num(record['net_profit'], 2)}` `return_pct={fmt_num(record['return_pct'], 3)}` "
        f"`trade_count={record['trade_count']}` `pf={fmt_num(record['profit_factor'])}` "
        f"`max_dd_pct={fmt_num(record['max_dd_pct'])}` `ulcer={fmt_num(record['ulcer_index'])}` "
        f"`long={record['long_signal_count']}` `short={record['short_signal_count']}` "
        f"`no_trade={record['no_trade_count']}` `external_mismatch={fmt_num(mismatch, 0)}`"
    )


def render_delta(delta: dict[str, float | int | None]) -> str:
    return (
        f"`net={fmt_num(delta['net_profit_delta'], 2)}` "
        f"`return_pct={fmt_num(delta['return_pct_delta'], 3)}` "
        f"`trade_count={fmt_num(delta['trade_count_delta'], 0)}` "
        f"`pf={fmt_num(delta['profit_factor_delta'])}` "
        f"`max_dd_pct={fmt_num(delta['max_dd_pct_delta'])}` "
        f"`ulcer={fmt_num(delta['ulcer_index_delta'])}` "
        f"`long={fmt_num(delta['long_signal_delta'], 0)}` "
        f"`short={fmt_num(delta['short_signal_delta'], 0)}` "
        f"`no_trade={fmt_num(delta['no_trade_delta'], 0)}` "
        f"`external_mismatch={fmt_num(delta['external_mismatch_delta'], 0)}`"
    )


def build_payload() -> dict[str, Any]:
    reference_builtin = load_summary(REFERENCE_BUILTIN_SUMMARY)
    records = [build_run_record(spec) for spec in RUN_SPECS]
    contract_baseline = next(record for record in records if abs(record["min_margin"] - 0.06750) < 1e-9)
    candidate = next(record for record in records if abs(record["min_margin"] - 0.06000) < 1e-9)

    for record in records:
        record["delta_vs_builtin_reference"] = diff_metrics(record, reference_builtin)
        record["delta_vs_contract_baseline"] = diff_metrics(record, contract_baseline)

    best_record = rank_records(records)[0]

    return {
        "reviewed_on_utc": datetime.now(tz=UTC).isoformat(),
        "reference_builtin": reference_builtin,
        "contract_baseline": contract_baseline,
        "candidate_record": candidate,
        "best_record": best_record,
        "records": records,
    }


def render_markdown(payload: dict[str, Any]) -> str:
    built_in = payload["reference_builtin"]
    contract_baseline = payload["contract_baseline"]
    candidate = payload["candidate_record"]
    best = payload["best_record"]

    lines: list[str] = []
    lines.append("# Stage 41 Margin Bridge Confirmation")
    lines.append("")
    lines.append(f"- reviewed_on_utc: `{payload['reviewed_on_utc']}`")
    lines.append("- replay surface: `34D extended bridge contract-aligned confirmation on 2024.01.01 -> 2026.04.13`")
    lines.append("- comparison: `baseline min_margin=0.06750` versus `candidate min_margin=0.06000`")
    lines.append("")
    lines.append("## Executive Read")
    lines.append("")
    if best["label"] == candidate["label"]:
        lines.append("- the broader extended-bridge confirmation keeps `34D min_margin=0.06000` as the best tested contract-aligned operating candidate")
    else:
        lines.append("- the broader extended-bridge confirmation does not keep `0.06000` on top; the baseline held better on the wider carried path")
    lines.append(f"- candidate versus contract baseline: {render_delta(candidate['delta_vs_contract_baseline'])}")
    lines.append(f"- candidate versus built-in bridge reference: {render_delta(candidate['delta_vs_builtin_reference'])}")
    lines.append("")
    lines.append("## References")
    lines.append("")
    lines.append(
        f"- built-in bridge reference `34D` `min_margin=0.0675` "
        f"`net={fmt_num(built_in['net_profit'], 2)}` `return_pct={fmt_num(built_in['return_pct'], 3)}` "
        f"`trade_count={built_in['trade_count']}` `pf={fmt_num(built_in['profit_factor'])}` "
        f"`max_dd_pct={fmt_num(built_in['max_dd_pct'])}`"
    )
    lines.append("")
    lines.append("## Contract-Aligned Bridge Results")
    lines.append("")
    for record in payload["records"]:
        lines.append(render_record(record))
    lines.append("")
    lines.append("## Candidate Read")
    lines.append("")
    lines.append(render_record(candidate))
    lines.append(f"- versus contract baseline {render_delta(candidate['delta_vs_contract_baseline'])}")
    lines.append(f"- versus built-in bridge reference {render_delta(candidate['delta_vs_builtin_reference'])}")
    lines.append("")
    lines.append("## Interpretation")
    lines.append("")
    lines.append("- this check answers a broader operating question than the latest-window replay: whether the relaxed contract-aligned margin gate can survive a carried multi-year bridge rather than only a short recent slice")
    if best["label"] == candidate["label"]:
        lines.append("- the evidence now says the `0.06000` candidate is not only a latest-window patch; it also survives the wider carried contract-aligned bridge better than the contract baseline")
    else:
        lines.append("- the evidence says the latest-window winner does not generalize cleanly to the wider carried path, so the candidate should remain local-only until a better global setting is found")
    lines.append("- this still does not replace the built-in bridge as the current best absolute line by itself; it only tests whether the best contract-aligned candidate improves the carried contract-aligned lane")
    lines.append("")
    return "\n".join(lines)


def write_outputs(payload: dict[str, Any]) -> tuple[Path, Path]:
    json_path = REVIEW_STEM.with_suffix(".json")
    md_path = REVIEW_STEM.with_suffix(".md")
    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    md_path.write_text(render_markdown(payload), encoding="utf-8")
    return json_path, md_path


def main() -> None:
    payload = build_payload()
    json_path, md_path = write_outputs(payload)
    print(f"[done] json={json_path}")
    print(f"[done] markdown={md_path}")


if __name__ == "__main__":
    main()
