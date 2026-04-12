#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[3]
STAGE_DIR = ROOT_DIR / "stages" / "33_outside_bar_state_exit_followup"
ACTIVE_RUNS_DIR = STAGE_DIR / "02_runs" / "active"
REFERENCE_RUN_DIR = (
    ROOT_DIR
    / "stages"
    / "29_fusion_long_repair"
    / "02_runs"
    / "active"
    / "29N_25o_sxh2_0001"
)
OUTPUT_JSON = STAGE_DIR / "03_reviews" / "stage33_outside_bar_followup_20260412.json"
OUTPUT_MD = STAGE_DIR / "03_reviews" / "stage33_outside_bar_followup_20260412.md"
RUN_ORDER = [
    "29N_25o_sxh2_0001",
    "33A_29n_refcarry_0001",
    "33B_29n_outbar_both_0001",
    "33C_29n_outbar_long_0001",
    "33D_29n_outbar_short_0001",
    "33E_29n_outbar_both_a125_0001",
    "33F_29n_outbar_long_a125_0001",
]
DISPLAY_LABELS = {
    "29N_25o_sxh2_0001": "29N reference",
    "33A_29n_refcarry_0001": "33A carry rerun",
    "33B_29n_outbar_both_0001": "33B both",
    "33C_29n_outbar_long_0001": "33C long-only",
    "33D_29n_outbar_short_0001": "33D short-only",
    "33E_29n_outbar_both_a125_0001": "33E both + ATR1.25",
    "33F_29n_outbar_long_a125_0001": "33F long-only + ATR1.25",
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


def count_suppressions(csv_path: Path) -> int:
    if not csv_path.exists():
        return 0
    count = 0
    with csv_path.open("r", encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            trade_action_reason = row.get("trade_action_reason") or ""
            if "STATE_EXIT_SUPPRESSED_OUTSIDE_BAR" in trade_action_reason:
                count += 1
    return count


def load_attempt_summaries(run_dir: Path) -> dict[str, dict]:
    attempts_dir = run_dir / "mt5_attempts"
    out: dict[str, dict] = {}
    if not attempts_dir.exists():
        return out
    for summary_path in sorted(attempts_dir.glob("att_*/tester_attempt_summary.json")):
        payload = load_json(summary_path)
        split_name = payload.get("split_name")
        if split_name:
            payload["summary_path"] = str(summary_path)
            payload["suppression_count"] = count_suppressions(Path(payload["csv_log_path"]))
            out[str(split_name)] = payload
    return out


def extract_split_metrics(bundle: dict, split_name: str) -> dict[str, float | int | None]:
    split = bundle.get("results", {}).get("by_split", {}).get(split_name, {})
    headline = split.get("headline", {})
    risk = split.get("risk", {})
    diagnostics = split.get("diagnostics", {})
    execution = split.get("execution", {})
    return {
        "return_pct": headline.get("return_pct"),
        "profit_factor": headline.get("profit_factor"),
        "max_dd_pct": risk.get("max_dd_pct"),
        "trade_count": headline.get("trade_count"),
        "long_expectancy": diagnostics.get("long_expectancy"),
        "short_expectancy": diagnostics.get("short_expectancy"),
        "external_mismatch_count": execution.get("external_mismatch_count"),
    }


def load_run_record(run_name: str, run_dir: Path) -> dict:
    bundle = load_json(run_dir / "experiment_bundle.json")
    attempts = load_attempt_summaries(run_dir)
    splits = {}
    for split_name in SPLIT_ORDER:
        split_metrics = extract_split_metrics(bundle, split_name)
        attempt = attempts.get(split_name, {})
        split_metrics["suppression_count"] = attempt.get("suppression_count", 0)
        split_metrics["summary_path"] = attempt.get("summary_path")
        splits[split_name] = split_metrics
    return {
        "run_name": run_name,
        "label": DISPLAY_LABELS.get(run_name, run_name),
        "experiment_id": bundle["identity"]["experiment_id"],
        "stage_id": bundle["identity"]["stage_id"],
        "runtime_extra": bundle.get("runtime_snapshot", {}).get("extra", {}),
        "splits": splits,
    }


def compute_delta_summary(reference: dict, candidate: dict) -> dict:
    out: dict[str, dict[str, float | int | None]] = {}
    for split_name in SPLIT_ORDER:
        ref_metrics = reference["splits"][split_name]
        cand_metrics = candidate["splits"][split_name]
        out[split_name] = {
            "return_pct_delta": (
                None
                if ref_metrics["return_pct"] is None or cand_metrics["return_pct"] is None
                else float(cand_metrics["return_pct"]) - float(ref_metrics["return_pct"])
            ),
            "profit_factor_delta": (
                None
                if ref_metrics["profit_factor"] is None or cand_metrics["profit_factor"] is None
                else float(cand_metrics["profit_factor"]) - float(ref_metrics["profit_factor"])
            ),
            "max_dd_pct_delta": (
                None
                if ref_metrics["max_dd_pct"] is None or cand_metrics["max_dd_pct"] is None
                else float(cand_metrics["max_dd_pct"]) - float(ref_metrics["max_dd_pct"])
            ),
            "suppression_count_delta": int(cand_metrics["suppression_count"]) - int(ref_metrics["suppression_count"]),
        }
    return out


def compute_candidate_score(reference: dict, candidate: dict) -> float:
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


def build_markdown(payload: dict) -> str:
    reference = payload["reference"]
    carry = payload["carry_check"]
    candidates = payload["candidate_summaries"]
    best = payload.get("best_non_regression_run")

    lines = [
        "# Stage 33 Outside Bar Follow-Up Review",
        "",
        f"- reviewed_on: `{payload['reviewed_on']}`",
        f"- stage: `33_outside_bar_state_exit_followup`",
        f"- inherited_regular_reference: `{reference['run_name']}`",
        f"- carry_check_run: `{carry['run_name']}`",
        f"- best_non_regression_run: `{best or 'none'}`",
        "",
        "## Executive Read",
        "",
        "- this wave converts the Stage 32 `outside_adverse_bar` diagnosis into a live MT5 runtime sidecar",
        "- the runtime change is intentionally narrow: suppress `STATE_EXIT_MARGIN` only when the closed bar is an adverse outside bar",
        "- the main question is whether that diagnosis survives real path-dependent tester runs, not just counterfactual trade-ledger rewrites",
        "",
        "## Carry Check",
        "",
        f"- `33A` exists only to rerun the inherited `29N` logic through the updated EA path",
        f"- carry check summary: `test_return_delta={fmt_num(carry['deltas']['test']['return_pct_delta'])}`, `validation_return_delta={fmt_num(carry['deltas']['validation']['return_pct_delta'])}`, `hist_return_delta={fmt_num(carry['deltas']['hist_2024']['return_pct_delta'])}`",
        "",
        "## Candidate Scoreboard",
        "",
    ]

    for candidate in candidates:
        run_name = candidate["run_name"]
        lines.append(f"### {run_name}")
        lines.append("")
        lines.append(f"- label: `{candidate['label']}`")
        lines.append(f"- test_non_regression: `{str(candidate['test_non_regression']).lower()}`")
        lines.append(f"- weighted_score: `{fmt_num(candidate['score'])}`")
        for split_name in SPLIT_ORDER:
            split = candidate["splits"][split_name]
            delta = candidate["deltas"][split_name]
            lines.append(
                f"- {split_name}: `return_pct={fmt_num(split['return_pct'])}` `pf={fmt_num(split['profit_factor'], 4)}` `dd_pct={fmt_num(split['max_dd_pct'], 4)}` "
                f"`delta_return={fmt_num(delta['return_pct_delta'])}` `delta_pf={fmt_num(delta['profit_factor_delta'], 4)}` `delta_dd={fmt_num(delta['max_dd_pct_delta'], 4)}` "
                f"`suppressed={fmt_num(split['suppression_count'])}`"
            )
        lines.append("")

    lines.extend(
        [
            "## Decision Bias",
            "",
            "- prefer only candidates that preserve the current test window while adding value elsewhere",
            "- if no candidate clears that bar, keep `29N` unchanged and treat the candle sidecar as informative but non-promoted",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    run_dirs = {"29N_25o_sxh2_0001": REFERENCE_RUN_DIR}
    for run_name in RUN_ORDER[1:]:
        run_dirs[run_name] = ACTIVE_RUNS_DIR / run_name

    records = {run_name: load_run_record(run_name, run_dir) for run_name, run_dir in run_dirs.items()}
    reference = records["29N_25o_sxh2_0001"]
    carry = records["33A_29n_refcarry_0001"]
    carry["deltas"] = compute_delta_summary(reference, carry)

    candidate_summaries = []
    for run_name in RUN_ORDER[2:]:
        record = records[run_name]
        record["deltas"] = compute_delta_summary(reference, record)
        record["score"] = compute_candidate_score(reference, record)
        record["test_non_regression"] = is_test_non_regression(reference, record)
        candidate_summaries.append(record)

    non_regression = [candidate for candidate in candidate_summaries if candidate["test_non_regression"]]
    best_non_regression_run = max(non_regression, key=lambda item: item["score"])["run_name"] if non_regression else None

    payload = {
        "reviewed_on": "2026-04-12",
        "reference": reference,
        "carry_check": carry,
        "candidate_summaries": candidate_summaries,
        "best_non_regression_run": best_non_regression_run,
    }
    write_json(OUTPUT_JSON, payload)
    write_text(OUTPUT_MD, build_markdown(payload))
    print(f"[done] wrote={OUTPUT_JSON}")
    print(f"[done] wrote={OUTPUT_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
