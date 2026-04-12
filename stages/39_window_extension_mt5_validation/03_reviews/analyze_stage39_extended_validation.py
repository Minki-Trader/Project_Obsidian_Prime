#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
from datetime import datetime
from pathlib import Path

import numpy as np
import onnxruntime as ort
import pandas as pd


ROOT_DIR = Path(__file__).resolve().parents[3]
STAGE_DIR = ROOT_DIR / "stages" / "39_window_extension_mt5_validation"
ACTIVE_RUNS_DIR = STAGE_DIR / "02_runs" / "active"
OUTPUT_JSON = STAGE_DIR / "03_reviews" / "stage39_extended_validation_20260413.json"
OUTPUT_MD = STAGE_DIR / "03_reviews" / "stage39_extended_validation_20260413.md"

RUN_ORDER = ["39A_34d_bridge_ext_0001", "39B_34b_bridge_ext_0001"]
DISPLAY_LABELS = {
    "39A_34d_bridge_ext_0001": "39A 34D extended bridge",
    "39B_34b_bridge_ext_0001": "39B 34B extended bridge",
}
BRIDGE_SPLIT = "bridge_2024_2026q2"
LATEST_AUDIT_SPLIT = "latest_shadow_2026q2"
YEAR_BUCKETS = [
    ("2024", datetime(2024, 1, 1), datetime(2025, 1, 1)),
    ("2025", datetime(2025, 1, 1), datetime(2026, 1, 1)),
    ("2026_ytd", datetime(2026, 1, 1), datetime(2026, 4, 13)),
]
FEATURE_MATRIX_PATH = ROOT_DIR / "data" / "processed" / "fpmarkets_v2" / "features" / "extended_window" / "feature_matrix.parquet"
FEATURE_SCHEMA_PATH = ROOT_DIR / "stages" / "34_outside_bar_mainline_promotion" / "02_runs" / "active" / "34D_29s_outbarlong_0001" / "artifacts" / "feature_schema.json"
MODEL_PATH = ROOT_DIR / "stages" / "34_outside_bar_mainline_promotion" / "02_runs" / "active" / "34D_29s_outbarlong_0001" / "artifacts" / "model_probonly.onnx"
FNV_PRIME = 16777619
FNV_MASK = (1 << 64) - 1


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


def parse_mt5_datetime(text: str) -> datetime:
    return datetime.strptime(text, "%Y.%m.%d %H:%M:%S")


def extract_split_metrics(bundle: dict, split_name: str) -> dict[str, float | int | None]:
    split = bundle.get("results", {}).get("by_split", {}).get(split_name, {})
    headline = split.get("headline", {})
    risk = split.get("risk", {})
    diagnostics = split.get("diagnostics", {})
    execution = split.get("execution", {})
    return {
        "net_profit": headline.get("net_profit"),
        "return_pct": headline.get("return_pct"),
        "trade_count": headline.get("trade_count"),
        "profit_factor": headline.get("profit_factor"),
        "expectancy_per_trade": headline.get("expectancy_per_trade"),
        "max_dd_pct": risk.get("max_dd_pct"),
        "ulcer_index": risk.get("ulcer_index"),
        "worst_week": risk.get("worst_week"),
        "long_expectancy": diagnostics.get("long_expectancy"),
        "short_expectancy": diagnostics.get("short_expectancy"),
        "no_trade_rate": diagnostics.get("no_trade_rate"),
        "external_mismatch_count": execution.get("external_mismatch_count"),
    }


def load_attempt_summary(run_dir: Path, split_name: str) -> dict:
    for summary_path in sorted((run_dir / "mt5_attempts").glob("att_*/tester_attempt_summary.json")):
        payload = load_json(summary_path)
        if payload.get("split_name") == split_name:
            payload["summary_path"] = str(summary_path)
            return payload
    raise FileNotFoundError(f"missing attempt summary for split={split_name} under {run_dir}")


def load_year_buckets(trade_ledger_path: Path) -> dict[str, dict[str, float | int]]:
    buckets = {
        name: {"net_profit": 0.0, "trade_count": 0, "long_count": 0, "short_count": 0}
        for name, _, _ in YEAR_BUCKETS
    }
    with trade_ledger_path.open("r", encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            exit_time = parse_mt5_datetime(row["exit_time_server"])
            direction = row["direction"]
            net_profit = float(row.get("net_profit") or 0.0)
            for name, start, end in YEAR_BUCKETS:
                if start <= exit_time < end:
                    buckets[name]["net_profit"] += net_profit
                    buckets[name]["trade_count"] += 1
                    if direction == "LONG":
                        buckets[name]["long_count"] += 1
                    elif direction == "SHORT":
                        buckets[name]["short_count"] += 1
                    break
    return buckets


def load_run_record(run_name: str) -> dict:
    run_dir = ACTIVE_RUNS_DIR / run_name
    bundle = load_json(run_dir / "experiment_bundle.json")
    attempt = load_attempt_summary(run_dir, BRIDGE_SPLIT)
    return {
        "run_name": run_name,
        "label": DISPLAY_LABELS.get(run_name, run_name),
        "experiment_id": bundle["identity"]["experiment_id"],
        "stage_id": bundle["identity"]["stage_id"],
        "bridge": extract_split_metrics(bundle, BRIDGE_SPLIT),
        "attempt": {
            "summary_path": attempt["summary_path"],
            "from_date": attempt["date_window"].get("from_date"),
            "to_date": attempt["date_window"].get("to_date"),
            "actual_ready_row_count": attempt.get("coverage_check", {}).get("actual_ready_row_count"),
        },
        "year_buckets": load_year_buckets(Path(attempt["trade_ledger_path"])),
    }


def compute_delta(reference: dict, candidate: dict) -> dict:
    return {
        "net_profit_delta": float(reference["bridge"]["net_profit"] or 0.0) - float(candidate["bridge"]["net_profit"] or 0.0),
        "return_pct_delta": float(reference["bridge"]["return_pct"] or 0.0) - float(candidate["bridge"]["return_pct"] or 0.0),
        "profit_factor_delta": float(reference["bridge"]["profit_factor"] or 0.0) - float(candidate["bridge"]["profit_factor"] or 0.0),
        "max_dd_pct_delta": float(reference["bridge"]["max_dd_pct"] or 0.0) - float(candidate["bridge"]["max_dd_pct"] or 0.0),
        "ulcer_index_delta": float(reference["bridge"]["ulcer_index"] or 0.0) - float(candidate["bridge"]["ulcer_index"] or 0.0),
        "long_expectancy_delta": float(reference["bridge"]["long_expectancy"] or 0.0) - float(candidate["bridge"]["long_expectancy"] or 0.0),
        "short_expectancy_delta": float(reference["bridge"]["short_expectancy"] or 0.0) - float(candidate["bridge"]["short_expectancy"] or 0.0),
        "year_buckets": {
            name: {
                "net_profit_delta": float(reference["year_buckets"][name]["net_profit"]) - float(candidate["year_buckets"][name]["net_profit"]),
                "trade_count_delta": int(reference["year_buckets"][name]["trade_count"]) - int(candidate["year_buckets"][name]["trade_count"]),
            }
            for name, _, _ in YEAR_BUCKETS
        },
    }


def feature_checksum(values: list[float]) -> int:
    h = 2166136261
    for value in values:
        token = f"{float(value):.8f}|"
        for ch in token:
            h ^= ord(ch)
            h = (h * FNV_PRIME) & FNV_MASK
    return h


def parse_server_ts(text: str) -> pd.Timestamp:
    return pd.Timestamp(text.replace(".", "-").replace(" ", "T") + "Z")


def summarize_array(values: list[float]) -> dict[str, float | int | None]:
    if not values:
        return {"count": 0, "mean": None, "median": None, "p90": None, "max": None}
    arr = np.asarray(values, dtype=float)
    return {
        "count": int(arr.size),
        "mean": float(arr.mean()),
        "median": float(np.median(arr)),
        "p90": float(np.quantile(arr, 0.9)),
        "max": float(arr.max()),
    }


def build_latest_parity_record(run_name: str) -> dict:
    run_dir = ACTIVE_RUNS_DIR / run_name
    bundle = load_json(run_dir / "experiment_bundle.json")
    attempt = load_attempt_summary(run_dir, LATEST_AUDIT_SPLIT)
    shadow_df = pd.read_csv(attempt["csv_log_path"])
    ready_rows = shadow_df[shadow_df["row_ready"].astype(str).str.lower() == "true"].copy()
    if len(ready_rows) > 100:
        ready_rows = ready_rows.tail(100)

    feature_names = load_json(FEATURE_SCHEMA_PATH)["feature_names"]
    feature_df = pd.read_parquet(FEATURE_MATRIX_PATH)
    feature_df["timestamp"] = pd.to_datetime(feature_df["timestamp"], utc=True)
    feature_df = feature_df[feature_df["symbol"] == "US100"].set_index("timestamp").sort_index()

    session = ort.InferenceSession(str(MODEL_PATH), providers=["CPUExecutionProvider"])
    input_name = session.get_inputs()[0].name

    exact_diffs: list[float] = []
    best_neighbor_diffs: list[float] = []
    exact_checksum_matches = 0
    best_neighbor_checksum_matches = 0

    for _, row in ready_rows.iterrows():
        base_ts = parse_server_ts(str(row["bar_time_server"]))
        mt5_probs = np.array([row["p_short"], row["p_flat"], row["p_long"]], dtype=np.float32)
        neighbor_diffs: list[float] = []
        checksum_hit = False
        exact_hit = False
        exact_diff = None
        for minute_shift in [0, -5, 5]:
            ts = base_ts + pd.Timedelta(minutes=minute_shift)
            if ts not in feature_df.index:
                continue
            values = feature_df.loc[ts, feature_names].tolist()
            if any(pd.isna(values)):
                continue
            feature_array = np.asarray(values, dtype=np.float32).reshape(1, -1)
            py_probs = session.run(None, {input_name: feature_array})[0][0]
            diff = float(np.max(np.abs(py_probs - mt5_probs)))
            neighbor_diffs.append(diff)
            checksum_value = feature_checksum(values)
            if minute_shift == 0:
                exact_diff = diff
                if checksum_value == int(row["feature_checksum"]):
                    exact_hit = True
            if checksum_value == int(row["feature_checksum"]):
                checksum_hit = True

        if exact_diff is not None:
            exact_diffs.append(exact_diff)
        if neighbor_diffs:
            best_neighbor_diffs.append(min(neighbor_diffs))
        if exact_hit:
            exact_checksum_matches += 1
        if checksum_hit:
            best_neighbor_checksum_matches += 1

    return {
        "run_name": run_name,
        "experiment_id": bundle["identity"]["experiment_id"],
        "latest_attempt": {
            "summary_path": attempt["summary_path"],
            "from_date": attempt["date_window"].get("from_date"),
            "to_date": attempt["date_window"].get("to_date"),
            "actual_ready_row_count": attempt.get("coverage_check", {}).get("actual_ready_row_count"),
            "shadow_csv_path": attempt.get("csv_log_path"),
        },
        "mt5_metrics": {
            "no_trade_rate": attempt.get("financial_metrics", {}).get("diagnostics", {}).get("no_trade_rate"),
            "external_mismatch_count": attempt.get("metrics", {}).get("external_mismatch_count"),
            "skip_reason_breakdown": attempt.get("metrics", {}).get("skip_reason_breakdown", {}),
        },
        "proxy_parity": {
            "exact_timestamp_prob_diff": summarize_array(exact_diffs),
            "best_neighbor_prob_diff": summarize_array(best_neighbor_diffs),
            "exact_timestamp_checksum_match_count": exact_checksum_matches,
            "best_neighbor_checksum_match_count": best_neighbor_checksum_matches,
            "sample_count": int(len(ready_rows)),
        },
    }


def build_markdown(payload: dict) -> str:
    reference = payload["reference"]
    candidate = payload["candidate"]
    delta = payload["delta"]
    latest = payload["latest_shadow_audit"]
    lines = [
        "# Stage 39 Extended Window MT5 Validation",
        "",
        f"- reviewed_on: `{payload['reviewed_on']}`",
        "- stage: `39_window_extension_mt5_validation`",
        f"- extended_window: `{payload['extended_window']}`",
        "",
        "## Executive Read",
        "",
        "- this stage extends the common window to the latest safe closed-bar date and then checks both the continuity story and the current-date MT5 runtime surface",
        f"- extended bridge result `39A minus 39B`: `net={fmt_num(delta['net_profit_delta'])}` `return_pct={fmt_num(delta['return_pct_delta'])}` `pf={fmt_num(delta['profit_factor_delta'], 4)}` `dd_pct={fmt_num(delta['max_dd_pct_delta'], 4)}`",
        f"- latest shadow audit sample: `ready_rows={latest['proxy_parity']['sample_count']}` `mean_max_abs={fmt_num(latest['proxy_parity']['exact_timestamp_prob_diff']['mean'], 4)}` `checksum_exact={latest['proxy_parity']['exact_timestamp_checksum_match_count']}`",
        "",
        "## Extended Bridge",
        "",
    ]
    for record in [reference, candidate]:
        bridge = record["bridge"]
        lines.append(f"### {record['run_name']}")
        lines.append("")
        lines.append(f"- label: `{record['label']}`")
        lines.append(
            f"- bridge headline: `net={fmt_num(bridge['net_profit'])}` `return_pct={fmt_num(bridge['return_pct'])}` "
            f"`pf={fmt_num(bridge['profit_factor'], 4)}` `dd_pct={fmt_num(bridge['max_dd_pct'], 4)}` `trades={fmt_num(bridge['trade_count'])}`"
        )
        lines.append(
            f"- bridge risk: `ulcer={fmt_num(bridge['ulcer_index'], 4)}` `worst_week={fmt_num(bridge['worst_week'])}` "
            f"`no_trade_rate={fmt_num(bridge['no_trade_rate'], 4)}` `external_mismatch_count={fmt_num(bridge['external_mismatch_count'])}`"
        )
        for bucket_name, _, _ in YEAR_BUCKETS:
            bucket = record["year_buckets"][bucket_name]
            lines.append(
                f"- {bucket_name}: `net={fmt_num(bucket['net_profit'])}` `trades={fmt_num(bucket['trade_count'])}` "
                f"`long={fmt_num(bucket['long_count'])}` `short={fmt_num(bucket['short_count'])}`"
            )
        lines.append("")
    lines.append("## Latest Shadow Audit")
    lines.append("")
    lines.append(
        f"- audit window: `{latest['latest_attempt']['from_date']} -> {latest['latest_attempt']['to_date']}` "
        f"`ready_rows={fmt_num(latest['latest_attempt']['actual_ready_row_count'])}`"
    )
    lines.append(
        f"- MT5 latest runtime: `no_trade_rate={fmt_num(latest['mt5_metrics']['no_trade_rate'], 4)}` "
        f"`external_mismatch_count={fmt_num(latest['mt5_metrics']['external_mismatch_count'])}`"
    )
    lines.append(
        f"- exact timestamp proxy: `mean_max_abs={fmt_num(latest['proxy_parity']['exact_timestamp_prob_diff']['mean'], 4)}` "
        f"`p90={fmt_num(latest['proxy_parity']['exact_timestamp_prob_diff']['p90'], 4)}` "
        f"`max={fmt_num(latest['proxy_parity']['exact_timestamp_prob_diff']['max'], 4)}`"
    )
    lines.append(
        f"- checksum matches: `exact={latest['proxy_parity']['exact_timestamp_checksum_match_count']}` "
        f"`best_neighbor={latest['proxy_parity']['best_neighbor_checksum_match_count']}`"
    )
    lines.append("")
    lines.append("## Follow-Up Bias")
    lines.append("")
    lines.append("- keep the historical frozen split scoreboard intact and treat this stage as a latest-window continuity and runtime-audit extension")
    lines.append("- if `34D` still leads on the extended bridge, keep simplification closed and carry the base-versus-incumbent story forward")
    lines.append("- use the fresh latest shadow logs as the next true parity-audit starting surface rather than leaning only on older handoff logs")
    return "\n".join(lines) + "\n"


def main() -> int:
    records = {run_name: load_run_record(run_name) for run_name in RUN_ORDER}
    reference = records["39A_34d_bridge_ext_0001"]
    candidate = records["39B_34b_bridge_ext_0001"]
    payload = {
        "reviewed_on": "2026-04-13",
        "extended_window": "2022-08-01 .. 2026-04-12 inclusive",
        "reference": reference,
        "candidate": candidate,
        "delta": compute_delta(reference, candidate),
        "latest_shadow_audit": build_latest_parity_record("39A_34d_bridge_ext_0001"),
    }
    write_json(OUTPUT_JSON, payload)
    write_text(OUTPUT_MD, build_markdown(payload))
    print(f"[done] wrote={OUTPUT_JSON}")
    print(f"[done] wrote={OUTPUT_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
