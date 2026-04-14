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
REVIEW_STEM = STAGE_DIR / "03_reviews" / f"stage41_margin_fine_replay_{datetime.now(tz=UTC).strftime('%Y%m%d')}"

RUN_SPECS = [
    {
        "label": "34D margin 0.05875",
        "family": "34D",
        "min_margin": 0.05875,
        "run_dir": STAGE_DIR / "02_runs" / "active" / "41G_34d_margin05875_0001",
    },
    {
        "label": "34D margin 0.06000",
        "family": "34D",
        "min_margin": 0.06000,
        "run_dir": STAGE_DIR / "02_runs" / "active" / "41F_34d_margin0600_0001",
    },
    {
        "label": "34D margin 0.06125",
        "family": "34D",
        "min_margin": 0.06125,
        "run_dir": STAGE_DIR / "02_runs" / "active" / "41H_34d_margin06125_0001",
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
    / "att_0007"
    / "tester_attempt_summary.json"
)
REFERENCE_CONTRACT_SUMMARY = (
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
    return (
        f"- `{record['label']}` `min_margin={record['min_margin']:.5f}` "
        f"`net={fmt_num(record['net_profit'], 2)}` `return_pct={fmt_num(record['return_pct'], 3)}` "
        f"`trade_count={record['trade_count']}` `pf={fmt_num(record['profit_factor'])}` "
        f"`max_dd_pct={fmt_num(record['max_dd_pct'])}` `ulcer={fmt_num(record['ulcer_index'])}` "
        f"`long={record['long_signal_count']}` `short={record['short_signal_count']}` `no_trade={record['no_trade_count']}`"
    )


def render_delta(delta: dict[str, float]) -> str:
    return (
        f"`net={fmt_num(delta['net_profit_delta'], 2)}` "
        f"`return_pct={fmt_num(delta['return_pct_delta'], 3)}` "
        f"`trade_count={fmt_num(delta['trade_count_delta'], 0)}` "
        f"`pf={fmt_num(delta['profit_factor_delta'])}` "
        f"`max_dd_pct={fmt_num(delta['max_dd_pct_delta'])}` "
        f"`ulcer={fmt_num(delta['ulcer_index_delta'])}` "
        f"`long={fmt_num(delta['long_signal_delta'], 0)}` "
        f"`short={fmt_num(delta['short_signal_delta'], 0)}` "
        f"`no_trade={fmt_num(delta['no_trade_delta'], 0)}`"
    )


def build_payload() -> dict[str, Any]:
    reference_builtin = load_summary(REFERENCE_BUILTIN_SUMMARY)
    reference_contract = load_summary(REFERENCE_CONTRACT_SUMMARY)
    records = [build_run_record(spec) for spec in RUN_SPECS]
    center_record = next(record for record in records if abs(record["min_margin"] - 0.06000) < 1e-9)

    for record in records:
        record["delta_vs_contract_baseline"] = diff_metrics(record, reference_contract)
        record["delta_vs_builtin_reference"] = diff_metrics(record, reference_builtin)
        record["delta_vs_center"] = diff_metrics(record, center_record)

    best_record = rank_records(records)[0]

    pairwise_compares = []
    for record in records:
        if record["label"] == center_record["label"]:
            continue
        pairwise_compares.append(
            {
                "label": record["label"],
                "delta_vs_center": record["delta_vs_center"],
                "shadow_compare_vs_center": compare_shadow_csv(center_record["shadow_csv_path"], record["shadow_csv_path"]),
                "trade_compare_vs_center": compare_trade_ledgers(center_record["trade_ledger_path"], record["trade_ledger_path"]),
            }
        )

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

    response_shape = {
        "best_label": best_record["label"],
        "best_min_margin": best_record["min_margin"],
        "center_is_best": bool(best_record["label"] == center_record["label"]),
        "left_vs_center_net_delta": float(records[0]["net_profit"] - center_record["net_profit"]),
        "right_vs_center_net_delta": float(records[2]["net_profit"] - center_record["net_profit"]),
    }

    return {
        "reviewed_on_utc": datetime.now(tz=UTC).isoformat(),
        "reference_builtin": reference_builtin,
        "reference_contract": reference_contract,
        "records": records,
        "center_record": center_record,
        "best_record": best_record,
        "pairwise_compares_vs_center": pairwise_compares,
        "best_reason_deltas_vs_contract_baseline": reason_deltas[:12],
        "response_shape": response_shape,
    }


def render_markdown(payload: dict[str, Any]) -> str:
    built_in = payload["reference_builtin"]
    contract_baseline = payload["reference_contract"]
    center = payload["center_record"]
    best = payload["best_record"]

    lines: list[str] = []
    lines.append("# Stage 41 Margin Fine Replay")
    lines.append("")
    lines.append(f"- reviewed_on_utc: `{payload['reviewed_on_utc']}`")
    lines.append("- replay surface: `34D latest-window contract-aligned fine min_margin replay around 0.06000`")
    lines.append("- centerpoint source: `reuse 41F / 34D margin 0.06000`")
    lines.append("")
    lines.append("## Executive Read")
    lines.append("")
    if payload["response_shape"]["center_is_best"]:
        lines.append("- the fine replay keeps `0.06000` as the local best point on the tested `34D` operating surface")
    else:
        lines.append(f"- the fine replay shifts the local best point away from `0.06000` toward `{best['min_margin']:.5f}` on the tested `34D` operating surface")
    lines.append(
        f"- versus the `34D` contract baseline at `0.0675`, the best tested point delivered {render_delta(best['delta_vs_contract_baseline'])}"
    )
    lines.append(
        f"- versus the `34D` built-in reference at `0.0675`, the best tested point delivered {render_delta(best['delta_vs_builtin_reference'])}"
    )
    lines.append("")
    lines.append("## References")
    lines.append("")
    lines.append(
        f"- built-in reference `34D` `min_margin=0.0675` "
        f"`net={fmt_num(built_in['net_profit'], 2)}` `return_pct={fmt_num(built_in['return_pct'], 3)}` "
        f"`trade_count={built_in['trade_count']}` `pf={fmt_num(built_in['profit_factor'])}` `max_dd_pct={fmt_num(built_in['max_dd_pct'])}`"
    )
    lines.append(
        f"- contract baseline `34D` `min_margin=0.0675` "
        f"`net={fmt_num(contract_baseline['net_profit'], 2)}` `return_pct={fmt_num(contract_baseline['return_pct'], 3)}` "
        f"`trade_count={contract_baseline['trade_count']}` `pf={fmt_num(contract_baseline['profit_factor'])}` `max_dd_pct={fmt_num(contract_baseline['max_dd_pct'])}`"
    )
    lines.append("")
    lines.append("## Fine Replay Results")
    lines.append("")
    for record in payload["records"]:
        lines.append(render_record(record))
    lines.append("")
    lines.append("## Centerpoint Read")
    lines.append("")
    lines.append(render_record(center))
    lines.append(f"- versus contract baseline {render_delta(center['delta_vs_contract_baseline'])}")
    lines.append(f"- versus built-in reference {render_delta(center['delta_vs_builtin_reference'])}")
    lines.append("")
    lines.append("## Pairwise Versus Center")
    lines.append("")
    for item in payload["pairwise_compares_vs_center"]:
        lines.append(f"- `{item['label']}`")
        lines.append(f"  headline delta: {render_delta(item['delta_vs_center'])}")
        lines.append(
            f"  ready-row diff: `shared_ready_rows={item['shadow_compare_vs_center']['shared_ready_rows']}` "
            f"`decision_diffs={item['shadow_compare_vs_center']['decision_diff_count']}` "
            f"`decision_reason_diffs={item['shadow_compare_vs_center']['decision_reason_diff_count']}` "
            f"`trade_action_diffs={item['shadow_compare_vs_center']['trade_action_diff_count']}`"
        )
        lines.append(
            f"  trade ledger diff: `left_trade_count={item['trade_compare_vs_center']['left_trade_count']}` "
            f"`right_trade_count={item['trade_compare_vs_center']['right_trade_count']}` "
            f"`mismatch_rows={item['trade_compare_vs_center']['mismatch_row_count']}`"
        )
    lines.append("")
    lines.append("## Best Reason Shift")
    lines.append("")
    for item in payload["best_reason_deltas_vs_contract_baseline"][:10]:
        lines.append(
            f"- `{item['reason']}` `delta={item['delta_count']}` `best={item['best_count']}` `baseline={item['baseline_count']}`"
        )
    lines.append("")
    lines.append("## Interpretation")
    lines.append("")
    lines.append("- the fine replay is meant to answer a narrow operating question: whether the coarse `0.0600` candidate was a stable local peak or just a coarse-grid artifact")
    if payload["response_shape"]["center_is_best"]:
        lines.append("- within the tested neighborhood, the centerpoint survived the local check, so the evidence now supports treating `0.06000` as the best tested operating candidate rather than only a coarse-sweep hypothesis")
    else:
        lines.append(f"- within the tested neighborhood, the centerpoint did not survive the local check, so the operating candidate should move to `{best['min_margin']:.5f}` before any broader confirmation claim")
    lines.append("- this still does not by itself resolve the remaining contract-versus-built-in residual tax; it only sharpens the best-tested operating gate on the contract-aligned lane")
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
