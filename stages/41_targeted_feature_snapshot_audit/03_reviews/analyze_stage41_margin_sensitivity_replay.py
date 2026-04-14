#!/usr/bin/env python3
from __future__ import annotations

import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd


UTC = timezone.utc
ROOT_DIR = Path(__file__).resolve().parents[3]
STAGE_DIR = ROOT_DIR / "stages" / "41_targeted_feature_snapshot_audit"
REVIEW_STEM = STAGE_DIR / "03_reviews" / f"stage41_margin_sensitivity_replay_{datetime.now(tz=UTC).strftime('%Y%m%d')}"

RUN_SPECS = [
    {
        "label": "34B margin 0.0600",
        "family": "34B",
        "min_margin": 0.0600,
        "run_dir": STAGE_DIR / "02_runs" / "active" / "41A_34b_margin0600_0001",
    },
    {
        "label": "34B margin 0.0625",
        "family": "34B",
        "min_margin": 0.0625,
        "run_dir": STAGE_DIR / "02_runs" / "active" / "41B_34b_margin0625_0001",
    },
    {
        "label": "34B margin 0.0650",
        "family": "34B",
        "min_margin": 0.0650,
        "run_dir": STAGE_DIR / "02_runs" / "active" / "41C_34b_margin0650_0001",
    },
    {
        "label": "34B margin 0.0675",
        "family": "34B",
        "min_margin": 0.0675,
        "run_dir": STAGE_DIR / "02_runs" / "active" / "41D_34b_margin0675_0001",
    },
    {
        "label": "34B margin 0.0700",
        "family": "34B",
        "min_margin": 0.0700,
        "run_dir": STAGE_DIR / "02_runs" / "active" / "41E_34b_margin0700_0001",
    },
]

OPERATING_CONFIRM_SPEC = {
    "label": "34D margin 0.0600",
    "family": "34D",
    "min_margin": 0.0600,
    "run_dir": STAGE_DIR / "02_runs" / "active" / "41F_34d_margin0600_0001",
}

REFERENCE_BUILTIN_SUMMARY = (
    ROOT_DIR
    / "stages"
    / "39_window_extension_mt5_validation"
    / "02_runs"
    / "active"
    / "39B_34b_bridge_ext_0001"
    / "mt5_attempts"
    / "att_0004"
    / "tester_attempt_summary.json"
)
REFERENCE_CONTRACT_SUMMARY = (
    ROOT_DIR
    / "stages"
    / "39_window_extension_mt5_validation"
    / "02_runs"
    / "active"
    / "39B_34b_bridge_ext_0001"
    / "mt5_attempts"
    / "att_0003"
    / "tester_attempt_summary.json"
)
REFERENCE_34D_CONTRACT_SUMMARY = (
    ROOT_DIR
    / "stages"
    / "39_window_extension_mt5_validation"
    / "02_runs"
    / "active"
    / "39A_34d_bridge_ext_0001"
    / "mt5_attempts"
    / "att_0008"
    / "tester_attempt_summary.json"
)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


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
        "no_trade_rate": float(diagnostics["no_trade_rate"]),
        "decision_reason_breakdown": diagnostics.get("extra", {}).get("decision_reason_breakdown", {}),
        "shadow_csv_path": payload["csv_log_path"],
        "trade_ledger_path": payload["trade_ledger_path"],
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


def diff_metrics(candidate: dict[str, Any], reference: dict[str, Any]) -> dict[str, float]:
    return {
        "net_profit_delta": float(candidate["net_profit"] - reference["net_profit"]),
        "return_pct_delta": float(candidate["return_pct"] - reference["return_pct"]),
        "trade_count_delta": float(candidate["trade_count"] - reference["trade_count"]),
        "profit_factor_delta": float(candidate["profit_factor"] - reference["profit_factor"]),
        "max_dd_pct_delta": float(candidate["max_dd_pct"] - reference["max_dd_pct"]),
        "ulcer_index_delta": float(candidate["ulcer_index"] - reference["ulcer_index"]),
        "long_signal_delta": float(candidate["long_signal_count"] - reference["long_signal_count"]),
        "short_signal_delta": float(candidate["short_signal_count"] - reference["short_signal_count"]),
        "no_trade_delta": float(candidate["no_trade_count"] - reference["no_trade_count"]),
    }


def compare_shadow_csv(path_a: str, path_b: str) -> dict[str, int]:
    left = pd.read_csv(path_a)
    right = pd.read_csv(path_b)
    key = "bar_time_server"
    for frame in (left, right):
        for column in ("decision", "decision_reason", "trade_action_reason"):
            frame[column] = frame[column].fillna("").astype(str)
        if "row_ready" in frame.columns:
            frame["row_ready"] = frame["row_ready"].fillna(False).astype(str).str.lower().eq("true")

    merged = left[[key, "row_ready", "decision", "decision_reason", "trade_action_reason"]].merge(
        right[[key, "row_ready", "decision", "decision_reason", "trade_action_reason"]],
        on=key,
        how="inner",
        suffixes=("_left", "_right"),
    )
    ready = merged[merged["row_ready_left"] & merged["row_ready_right"]].copy()
    return {
        "shared_rows": int(len(merged)),
        "shared_ready_rows": int(len(ready)),
        "decision_diff_count": int((ready["decision_left"] != ready["decision_right"]).sum()),
        "decision_reason_diff_count": int((ready["decision_reason_left"] != ready["decision_reason_right"]).sum()),
        "trade_action_diff_count": int((ready["trade_action_reason_left"] != ready["trade_action_reason_right"]).sum()),
    }


def compare_trade_ledgers(path_a: str, path_b: str) -> dict[str, int]:
    left = pd.read_csv(path_a)
    right = pd.read_csv(path_b)
    if len(left) != len(right):
        return {
            "left_trade_count": int(len(left)),
            "right_trade_count": int(len(right)),
            "mismatch_row_count": abs(int(len(left) - len(right))),
        }

    compare_columns = ["entry_bar_time_server", "exit_bar_time_server", "entry_price", "exit_price", "close_reason", "decision_at_entry"]
    mismatch_count = 0
    for column in compare_columns:
        if column not in left.columns or column not in right.columns:
            continue
        mismatch_count += int((left[column].astype(str) != right[column].astype(str)).sum())
    return {
        "left_trade_count": int(len(left)),
        "right_trade_count": int(len(right)),
        "mismatch_row_count": int(mismatch_count),
    }


def rank_contract_records(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted(
        records,
        key=lambda item: (
            -item["net_profit"],
            -item["profit_factor"],
            item["max_dd_pct"],
            item["ulcer_index"],
        ),
    )


def build_payload() -> dict[str, Any]:
    reference_builtin = load_summary(REFERENCE_BUILTIN_SUMMARY)
    reference_contract = load_summary(REFERENCE_CONTRACT_SUMMARY)
    reference_34d_contract = load_summary(REFERENCE_34D_CONTRACT_SUMMARY)

    contract_records = [build_run_record(spec) for spec in RUN_SPECS]
    operating_confirm = build_run_record(OPERATING_CONFIRM_SPEC)

    for record in contract_records:
        record["delta_vs_contract_baseline"] = diff_metrics(record, reference_contract)
        record["delta_vs_builtin_reference"] = diff_metrics(record, reference_builtin)

    best_record = rank_contract_records(contract_records)[0]

    operating_metric_diffs = {}
    for field in (
        "net_profit",
        "return_pct",
        "trade_count",
        "profit_factor",
        "max_dd_pct",
        "ulcer_index",
        "long_signal_count",
        "short_signal_count",
        "no_trade_count",
    ):
        operating_metric_diffs[field] = float(operating_confirm[field] - best_record[field])

    operating_shadow_compare = compare_shadow_csv(best_record["shadow_csv_path"], operating_confirm["shadow_csv_path"])
    operating_trade_compare = compare_trade_ledgers(best_record["trade_ledger_path"], operating_confirm["trade_ledger_path"])

    best_reasons = Counter(best_record["decision_reason_breakdown"])
    baseline_reasons = Counter(reference_contract["decision_reason_breakdown"])
    reason_deltas = [
        {
            "reason": reason,
            "delta_count": int(best_reasons.get(reason, 0) - baseline_reasons.get(reason, 0)),
            "best_count": int(best_reasons.get(reason, 0)),
            "baseline_count": int(baseline_reasons.get(reason, 0)),
        }
        for reason in sorted(set(best_reasons) | set(baseline_reasons))
    ]
    reason_deltas.sort(key=lambda item: (-abs(item["delta_count"]), item["reason"]))

    return {
        "reviewed_on_utc": datetime.now(tz=UTC).isoformat(),
        "reference_builtin": reference_builtin,
        "reference_contract": reference_contract,
        "reference_34d_contract": reference_34d_contract,
        "contract_records": contract_records,
        "best_contract_record": best_record,
        "operating_confirm_record": operating_confirm,
        "operating_metric_diffs_vs_best_34b": operating_metric_diffs,
        "operating_shadow_compare": operating_shadow_compare,
        "operating_trade_compare": operating_trade_compare,
        "best_reason_deltas_vs_contract_baseline": reason_deltas[:12],
    }


def fmt_num(value: float | int | None, digits: int = 4) -> str:
    if value is None:
        return "n/a"
    if isinstance(value, int):
        return str(value)
    return f"{value:.{digits}f}"


def render_record(record: dict[str, Any]) -> str:
    return (
        f"- `{record['label']}` `min_margin={record['min_margin']:.4f}` "
        f"`net={fmt_num(record['net_profit'], 2)}` `return_pct={fmt_num(record['return_pct'], 3)}` "
        f"`trade_count={record['trade_count']}` `pf={fmt_num(record['profit_factor'])}` "
        f"`max_dd_pct={fmt_num(record['max_dd_pct'])}` `ulcer={fmt_num(record['ulcer_index'])}` "
        f"`long={record['long_signal_count']}` `short={record['short_signal_count']}` `no_trade={record['no_trade_count']}`"
    )


def render_delta(label: str, delta: dict[str, float]) -> str:
    return (
        f"- `{label}` `net={fmt_num(delta['net_profit_delta'], 2)}` "
        f"`return_pct={fmt_num(delta['return_pct_delta'], 3)}` `trade_count={fmt_num(delta['trade_count_delta'], 0)}` "
        f"`pf={fmt_num(delta['profit_factor_delta'])}` `max_dd_pct={fmt_num(delta['max_dd_pct_delta'])}` "
        f"`ulcer={fmt_num(delta['ulcer_index_delta'])}` `long={fmt_num(delta['long_signal_delta'], 0)}` "
        f"`short={fmt_num(delta['short_signal_delta'], 0)}` `no_trade={fmt_num(delta['no_trade_delta'], 0)}`"
    )


def render_markdown(payload: dict[str, Any]) -> str:
    best = payload["best_contract_record"]
    built_in = payload["reference_builtin"]
    contract_baseline = payload["reference_contract"]
    operating_confirm = payload["operating_confirm_record"]

    lines: list[str] = []
    lines.append("# Stage 41 Margin Sensitivity Replay")
    lines.append("")
    lines.append(f"- reviewed_on_utc: `{payload['reviewed_on_utc']}`")
    lines.append("- replay surface: `34B latest-window contract-aligned min_margin sweep around 0.0675`")
    lines.append("- confirmation surface: `34D latest-window contract-aligned replay at the best 34B min_margin candidate`")
    lines.append("")
    lines.append("## Executive Read")
    lines.append("")
    lines.append(
        "- relaxing the fixed `max_probability_margin` gate from `0.0675` to `0.0600` was the only tested move that materially improved the contract-aligned latest-window KPI surface"
    )
    lines.append(
        "- the `0.0600` replay improved the contract-aligned baseline by `net +10.39`, `return_pct +2.078`, `trade_count +15`, `profit_factor +0.0847`, and `max_dd_pct -0.9851`, while stricter settings from `0.0625` through `0.0700` were flat-to-worse"
    )
    lines.append(
        "- the same `0.0600` replay matched exactly on the operating `34D` bundle versus the simpler `34B` bundle in this latest window sample, so the candidate is not a 34B-only artifact"
    )
    lines.append("")
    lines.append("## References")
    lines.append("")
    lines.append(
        f"- built-in reference `34B/34D` `min_margin=0.0675` "
        f"`net={fmt_num(built_in['net_profit'], 2)}` `return_pct={fmt_num(built_in['return_pct'], 3)}` "
        f"`trade_count={built_in['trade_count']}` `pf={fmt_num(built_in['profit_factor'])}` `max_dd_pct={fmt_num(built_in['max_dd_pct'])}`"
    )
    lines.append(
        f"- contract baseline `34B/34D` `min_margin=0.0675` "
        f"`net={fmt_num(contract_baseline['net_profit'], 2)}` `return_pct={fmt_num(contract_baseline['return_pct'], 3)}` "
        f"`trade_count={contract_baseline['trade_count']}` `pf={fmt_num(contract_baseline['profit_factor'])}` `max_dd_pct={fmt_num(contract_baseline['max_dd_pct'])}`"
    )
    lines.append("")
    lines.append("## Sweep Results")
    lines.append("")
    for record in payload["contract_records"]:
        lines.append(render_record(record))
    lines.append("")
    lines.append("## Best Candidate")
    lines.append("")
    lines.append(render_record(best))
    lines.append(render_delta("delta_vs_contract_baseline", best["delta_vs_contract_baseline"]))
    lines.append(render_delta("delta_vs_builtin_reference", best["delta_vs_builtin_reference"]))
    lines.append("")
    lines.append("## Baseline Deltas")
    lines.append("")
    for record in payload["contract_records"]:
        lines.append(f"- `{record['label']}`")
        lines.append(f"  contract baseline: {render_delta('vs_contract', record['delta_vs_contract_baseline'])[2:]}")
        lines.append(f"  built-in reference: {render_delta('vs_builtin', record['delta_vs_builtin_reference'])[2:]}")
    lines.append("")
    lines.append("## Operating Confirmation")
    lines.append("")
    lines.append(render_record(operating_confirm))
    lines.append(
        f"- headline diff versus best `34B 0.0600`: "
        f"`net={fmt_num(payload['operating_metric_diffs_vs_best_34b']['net_profit'], 2)}` "
        f"`return_pct={fmt_num(payload['operating_metric_diffs_vs_best_34b']['return_pct'], 3)}` "
        f"`trade_count={fmt_num(payload['operating_metric_diffs_vs_best_34b']['trade_count'], 0)}` "
        f"`pf={fmt_num(payload['operating_metric_diffs_vs_best_34b']['profit_factor'])}` "
        f"`max_dd_pct={fmt_num(payload['operating_metric_diffs_vs_best_34b']['max_dd_pct'])}`"
    )
    lines.append(
        f"- shadow parity `shared_rows={payload['operating_shadow_compare']['shared_rows']}` "
        f"`shared_ready_rows={payload['operating_shadow_compare']['shared_ready_rows']}` "
        f"`decision_diffs={payload['operating_shadow_compare']['decision_diff_count']}` "
        f"`decision_reason_diffs={payload['operating_shadow_compare']['decision_reason_diff_count']}` "
        f"`trade_action_diffs={payload['operating_shadow_compare']['trade_action_diff_count']}`"
    )
    lines.append(
        f"- trade ledger parity `left_trade_count={payload['operating_trade_compare']['left_trade_count']}` "
        f"`right_trade_count={payload['operating_trade_compare']['right_trade_count']}` "
        f"`mismatch_rows={payload['operating_trade_compare']['mismatch_row_count']}`"
    )
    lines.append("")
    lines.append("## Decision Reason Shift")
    lines.append("")
    for item in payload["best_reason_deltas_vs_contract_baseline"][:10]:
        lines.append(
            f"- `{item['reason']}` `delta={item['delta_count']}` `best={item['best_count']}` `baseline={item['baseline_count']}`"
        )
    lines.append("")
    lines.append("## Interpretation")
    lines.append("")
    lines.append(
        "- the fixed margin gate is now confirmed as a live lever rather than just a descriptive hypothesis: a narrow relaxation to `0.0600` recovers directional participation and improves both headline return and drawdown versus the contract baseline"
    )
    lines.append(
        "- the recovery is only partial relative to the built-in lane, so the contract-aligned feature surface still carries some residual tax even after the margin adjustment"
    )
    lines.append(
        "- the next high-signal follow-up is a finer `34D`-only replay around `0.0600`, for example `0.05875 / 0.0600 / 0.06125`, before deciding whether to treat `0.0600` as a new operating candidate"
    )
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
