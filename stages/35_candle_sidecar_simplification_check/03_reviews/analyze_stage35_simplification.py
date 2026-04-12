#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[3]
STAGE_DIR = ROOT_DIR / "stages" / "35_candle_sidecar_simplification_check"
ACTIVE_RUNS_DIR = STAGE_DIR / "02_runs" / "active"
OUTPUT_JSON = STAGE_DIR / "03_reviews" / "stage35_simplification_20260412.json"
OUTPUT_MD = STAGE_DIR / "03_reviews" / "stage35_simplification_20260412.md"
RUN_ORDER = [
    "35A_34d_refcarry_0001",
    "35B_34b_simpleref_0001",
]
DISPLAY_LABELS = {
    "35A_34d_refcarry_0001": "35A verified 34D carry",
    "35B_34b_simpleref_0001": "35B governance-only simplification carry",
}
SPLIT_ORDER = ["validation", "test", "hist_2024"]


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def fmt_num(value: float | int | None, digits: int = 3) -> str:
    if value is None:
        return "n/a"
    if isinstance(value, int):
        return str(value)
    return f"{value:.{digits}f}"


def extract_split_metrics(bundle: dict, split_name: str) -> dict[str, float | int | None]:
    split = bundle.get("results", {}).get("by_split", {}).get(split_name, {})
    headline = split.get("headline", {})
    risk = split.get("risk", {})
    diagnostics = split.get("diagnostics", {})
    return {
        "return_pct": headline.get("return_pct"),
        "profit_factor": headline.get("profit_factor"),
        "max_dd_pct": risk.get("max_dd_pct"),
        "trade_count": headline.get("trade_count"),
        "long_expectancy": diagnostics.get("long_expectancy"),
        "short_expectancy": diagnostics.get("short_expectancy"),
    }


def load_run_record(run_name: str) -> dict:
    run_dir = ACTIVE_RUNS_DIR / run_name
    bundle = load_json(run_dir / "experiment_bundle.json")
    return {
        "run_name": run_name,
        "label": DISPLAY_LABELS.get(run_name, run_name),
        "experiment_id": bundle["identity"]["experiment_id"],
        "stage_id": bundle["identity"]["stage_id"],
        "runtime_extra": bundle.get("runtime_snapshot", {}).get("extra", {}),
        "splits": {
            split_name: extract_split_metrics(bundle, split_name)
            for split_name in SPLIT_ORDER
        },
    }


def compute_delta_summary(reference: dict, candidate: dict) -> dict:
    out: dict[str, dict[str, float | None]] = {}
    for split_name in SPLIT_ORDER:
        ref = reference["splits"][split_name]
        cand = candidate["splits"][split_name]
        out[split_name] = {
            "return_pct_delta": None if ref["return_pct"] is None or cand["return_pct"] is None else float(cand["return_pct"]) - float(ref["return_pct"]),
            "profit_factor_delta": None if ref["profit_factor"] is None or cand["profit_factor"] is None else float(cand["profit_factor"]) - float(ref["profit_factor"]),
            "max_dd_pct_delta": None if ref["max_dd_pct"] is None or cand["max_dd_pct"] is None else float(cand["max_dd_pct"]) - float(ref["max_dd_pct"]),
        }
    return out


def compute_score(reference: dict, candidate: dict) -> float:
    deltas = compute_delta_summary(reference, candidate)
    score = 0.0
    for split_name, weight in {"test": 3.0, "validation": 2.0, "hist_2024": 1.0}.items():
        split_delta = deltas[split_name]
        score += weight * float(split_delta["return_pct_delta"] or 0.0)
        score += weight * 20.0 * float(split_delta["profit_factor_delta"] or 0.0)
        score -= weight * 0.75 * max(float(split_delta["max_dd_pct_delta"] or 0.0), 0.0)
    return score


def is_test_non_regression(reference: dict, candidate: dict) -> bool:
    delta = compute_delta_summary(reference, candidate)["test"]
    return (
        float(delta["return_pct_delta"] or 0.0) >= -1.0
        and float(delta["profit_factor_delta"] or 0.0) >= -0.02
        and float(delta["max_dd_pct_delta"] or 0.0) <= 1.0
    )


def is_simplification_acceptable(reference: dict, candidate: dict) -> bool:
    deltas = compute_delta_summary(reference, candidate)
    return (
        is_test_non_regression(reference, candidate)
        and float(deltas["validation"]["return_pct_delta"] or 0.0) >= -1.0
        and float(deltas["validation"]["profit_factor_delta"] or 0.0) >= -0.02
        and float(deltas["hist_2024"]["return_pct_delta"] or 0.0) >= -2.0
        and float(deltas["hist_2024"]["profit_factor_delta"] or 0.0) >= -0.02
    )


def build_markdown(payload: dict) -> str:
    reference = payload["reference"]
    candidate = payload["candidate"]
    lines = [
        "# Stage 35 Simplification Review",
        "",
        f"- reviewed_on: `{payload['reviewed_on']}`",
        f"- stage: `35_candle_sidecar_simplification_check`",
        f"- inherited_regular_reference: `{reference['run_name']}`",
        f"- simplification_candidate: `{candidate['run_name']}`",
        f"- simplification_acceptable: `{str(candidate['simplification_acceptable']).lower()}`",
        "",
        "## Executive Read",
        "",
        "- Stage 35 asks the simplest next regular-lane question after the Stage 34 promotion and handoff verification",
        "- the only simplification candidate tested here is the full removal of the candle sidecar while keeping the `29S` governance backbone",
        "",
        "## Candidate Scoreboard",
        "",
        f"### {candidate['run_name']}",
        "",
        f"- label: `{candidate['label']}`",
        f"- test_non_regression: `{str(candidate['test_non_regression']).lower()}`",
        f"- simplification_acceptable: `{str(candidate['simplification_acceptable']).lower()}`",
        f"- weighted_score: `{fmt_num(candidate['score'])}`",
    ]
    for split_name in SPLIT_ORDER:
        split = candidate["splits"][split_name]
        delta = candidate["deltas"][split_name]
        lines.append(
            f"- {split_name}: `return_pct={fmt_num(split['return_pct'])}` `pf={fmt_num(split['profit_factor'], 4)}` `dd_pct={fmt_num(split['max_dd_pct'], 4)}` "
            f"`delta_return={fmt_num(delta['return_pct_delta'])}` `delta_pf={fmt_num(delta['profit_factor_delta'], 4)}` `delta_dd={fmt_num(delta['max_dd_pct_delta'], 4)}`"
        )
    lines.append("")
    return "\n".join(lines) + "\n"


def main() -> int:
    records = {run_name: load_run_record(run_name) for run_name in RUN_ORDER}
    reference = records["35A_34d_refcarry_0001"]
    candidate = records["35B_34b_simpleref_0001"]
    candidate["deltas"] = compute_delta_summary(reference, candidate)
    candidate["score"] = compute_score(reference, candidate)
    candidate["test_non_regression"] = is_test_non_regression(reference, candidate)
    candidate["simplification_acceptable"] = is_simplification_acceptable(reference, candidate)

    payload = {
        "reviewed_on": "2026-04-12",
        "reference": reference,
        "candidate": candidate,
    }
    write_json(OUTPUT_JSON, payload)
    write_text(OUTPUT_MD, build_markdown(payload))
    print(f"[done] wrote={OUTPUT_JSON}")
    print(f"[done] wrote={OUTPUT_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
