#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
from datetime import datetime
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[3]
STAGE_DIR = ROOT_DIR / "stages" / "37_long_horizon_bridge_read"
ACTIVE_RUNS_DIR = STAGE_DIR / "02_runs" / "active"
OUTPUT_JSON = STAGE_DIR / "03_reviews" / "stage37_bridge_20260412.json"
OUTPUT_MD = STAGE_DIR / "03_reviews" / "stage37_bridge_20260412.md"
RUN_ORDER = [
    "37A_34d_bridge_0001",
    "37B_34b_bridge_0001",
]
DISPLAY_LABELS = {
    "37A_34d_bridge_0001": "37A 34D continuous bridge",
    "37B_34b_bridge_0001": "37B 34B continuous bridge",
}
BRIDGE_SPLIT = "bridge_2024_2026q1"
YEAR_BUCKETS = [
    ("2024", datetime(2024, 1, 1), datetime(2025, 1, 1)),
    ("2025", datetime(2025, 1, 1), datetime(2026, 1, 1)),
    ("2026_ytd", datetime(2026, 1, 1), datetime(2026, 3, 1)),
]


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


def extract_bridge_metrics(bundle: dict) -> dict[str, float | int | None]:
    split = bundle.get("results", {}).get("by_split", {}).get(BRIDGE_SPLIT, {})
    headline = split.get("headline", {})
    risk = split.get("risk", {})
    diagnostics = split.get("diagnostics", {})
    execution = split.get("execution", {})
    return {
        "net_profit": headline.get("net_profit"),
        "return_pct": headline.get("return_pct"),
        "trade_count": headline.get("trade_count"),
        "win_rate": headline.get("win_rate"),
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
        "bridge": extract_bridge_metrics(bundle),
        "attempt": {
            "summary_path": attempt["summary_path"],
            "from_date": attempt["date_window"].get("from_date"),
            "to_date": attempt["date_window"].get("to_date"),
            "ready_row_gap": attempt.get("coverage_check", {}).get("ready_row_gap"),
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


def build_markdown(payload: dict) -> str:
    reference = payload["reference"]
    candidate = payload["candidate"]
    delta = payload["delta"]
    lines = [
        "# Stage 37 Long-Horizon Bridge Review",
        "",
        f"- reviewed_on: `{payload['reviewed_on']}`",
        f"- stage: `37_long_horizon_bridge_read`",
        f"- bridge_window: `{payload['bridge_window']}`",
        f"- operating_reference: `{reference['run_name']}`",
        f"- simplification_shadow: `{candidate['run_name']}`",
        "",
        "## Executive Read",
        "",
        "- this stage keeps the frozen split scoreboard untouched and asks only whether the Stage 35 simplification story survives one uninterrupted risk_pct equity path",
        f"- bridge result `37A minus 37B`: `net={fmt_num(delta['net_profit_delta'])}` `return_pct={fmt_num(delta['return_pct_delta'])}` `pf={fmt_num(delta['profit_factor_delta'], 4)}` `dd_pct={fmt_num(delta['max_dd_pct_delta'], 4)}`",
        f"- the yearly contribution shape was: `2024={fmt_num(delta['year_buckets']['2024']['net_profit_delta'])}` `2025={fmt_num(delta['year_buckets']['2025']['net_profit_delta'])}` `2026_ytd={fmt_num(delta['year_buckets']['2026_ytd']['net_profit_delta'])}`",
        "",
        "## Scoreboard",
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
        lines.append(
            f"- bridge expectancy: `long={fmt_num(bridge['long_expectancy'], 4)}` `short={fmt_num(bridge['short_expectancy'], 4)}` "
            f"`per_trade={fmt_num(bridge['expectancy_per_trade'], 4)}`"
        )
        for bucket_name, _, _ in YEAR_BUCKETS:
            bucket = record["year_buckets"][bucket_name]
            lines.append(
                f"- {bucket_name}: `net={fmt_num(bucket['net_profit'])}` `trades={fmt_num(bucket['trade_count'])}` "
                f"`long={fmt_num(bucket['long_count'])}` `short={fmt_num(bucket['short_count'])}`"
            )
        lines.append("")
    lines.extend(
        [
            "## Bridge Read",
            "",
            "- use this read as continuity evidence only; it does not replace `hist_2024 / validation / test`",
            "- if the bridge still prefers `34D`, then the Stage 35 and Stage 36 conclusions become more robust because they survive both reset and continuous-account views",
            "- if the bridge narrows the gap materially, that still points toward a narrower future simplification pass, not blanket sidecar removal",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    records = {run_name: load_run_record(run_name) for run_name in RUN_ORDER}
    reference = records["37A_34d_bridge_0001"]
    candidate = records["37B_34b_bridge_0001"]
    delta = compute_delta(reference, candidate)
    payload = {
        "reviewed_on": "2026-04-12",
        "bridge_window": "2024-01-01 .. 2026-02-28 inclusive",
        "reference": reference,
        "candidate": candidate,
        "delta": delta,
    }
    write_json(OUTPUT_JSON, payload)
    write_text(OUTPUT_MD, build_markdown(payload))
    print(f"[done] wrote={OUTPUT_JSON}")
    print(f"[done] wrote={OUTPUT_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
