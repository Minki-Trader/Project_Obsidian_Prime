#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd


UTC = timezone.utc
ROOT_DIR = Path(__file__).resolve().parents[3]
STAGE_DIR = ROOT_DIR / "stages" / "41_targeted_feature_snapshot_audit"
DEFAULT_FEATURE_MATRIX = ROOT_DIR / "data" / "processed" / "fpmarkets_v2" / "features" / "extended_window" / "feature_matrix.parquet"
DEFAULT_FEATURE_SCHEMA = (
    ROOT_DIR
    / "stages"
    / "34_outside_bar_mainline_promotion"
    / "02_runs"
    / "active"
    / "34D_29s_outbarlong_0001"
    / "artifacts"
    / "feature_schema.json"
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Analyze MT5 feature snapshot JSONL against the shared Python feature surface.")
    parser.add_argument("--snapshot-jsonl", required=True, help="Path to the MT5 feature snapshot JSONL artifact")
    parser.add_argument("--feature-matrix", default=str(DEFAULT_FEATURE_MATRIX), help="Path to the shared feature_matrix.parquet")
    parser.add_argument("--feature-schema", default=str(DEFAULT_FEATURE_SCHEMA), help="Path to the active feature_schema.json")
    parser.add_argument("--symbol", default="US100", help="Symbol to filter inside the feature matrix")
    parser.add_argument(
        "--output-stem",
        help="Optional output stem without extension. Defaults to stages/41.../03_reviews/stage41_targeted_feature_snapshot_audit_<today>",
    )
    return parser


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def parse_bar_time_server(text: str) -> pd.Timestamp:
    return pd.Timestamp(text.replace(".", "-").replace(" ", "T") + "Z")


def fmt_num(value: float | int | None, digits: int = 6) -> str:
    if value is None:
        return "n/a"
    if isinstance(value, int):
        return str(value)
    return f"{value:.{digits}f}"


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


def load_snapshot_rows(path: Path) -> list[dict]:
    rows: list[dict] = []
    with path.open("r", encoding="utf-8-sig") as handle:
        for raw_line in handle:
            line = raw_line.strip()
            if not line:
                continue
            rows.append(json.loads(line))
    if not rows:
        raise ValueError(f"snapshot jsonl is empty: {path}")
    return rows


def build_output_paths(output_stem: str | None) -> tuple[Path, Path]:
    if output_stem:
        stem = Path(output_stem)
    else:
        stamp = datetime.now(tz=UTC).strftime("%Y%m%d")
        stem = STAGE_DIR / "03_reviews" / f"stage41_targeted_feature_snapshot_audit_{stamp}"
    return stem.with_suffix(".json"), stem.with_suffix(".md")


def normalize_feature_row(row: pd.Series | pd.DataFrame, feature_names: list[str]) -> pd.Series:
    if isinstance(row, pd.DataFrame):
        row = row.iloc[-1]
    return row[feature_names]


def build_payload(snapshot_rows: list[dict], feature_df: pd.DataFrame, feature_names: list[str]) -> dict[str, object]:
    per_feature_diffs: dict[str, list[float]] = defaultdict(list)
    per_feature_worst_ts: dict[str, tuple[float, str]] = {}
    external_status_counts: dict[str, Counter[str]] = defaultdict(Counter)
    row_records: list[dict[str, object]] = []
    missing_rows: list[dict[str, object]] = []
    ready_rows = 0
    skip_rows = 0
    rows_with_matrix_match = 0

    tolerance_counters = Counter()

    for snapshot in snapshot_rows:
        row_ready = bool(snapshot.get("row_ready"))
        if row_ready:
            ready_rows += 1
        else:
            skip_rows += 1

        timestamp = parse_bar_time_server(str(snapshot["bar_time_server"]))
        features = snapshot.get("features", [])
        feature_values = {
            str(item["name"]): item.get("value")
            for item in features
            if isinstance(item, dict) and "name" in item
        }

        for ext in snapshot.get("external_inputs", []):
            if not isinstance(ext, dict):
                continue
            symbol = str(ext.get("symbol", "unknown"))
            status = str(ext.get("status", "unknown"))
            external_status_counts[symbol][status] += 1

        if timestamp not in feature_df.index:
            missing_rows.append(
                {
                    "timestamp": timestamp.isoformat(),
                    "bar_time_server": snapshot["bar_time_server"],
                    "row_ready": row_ready,
                    "skip_reason": snapshot.get("skip_reason", ""),
                }
            )
            continue

        python_row = normalize_feature_row(feature_df.loc[timestamp], feature_names)
        rows_with_matrix_match += 1

        diffs: list[tuple[str, float, float, float]] = []
        for feature_name in feature_names:
            mt5_value = feature_values.get(feature_name)
            if mt5_value is None or pd.isna(mt5_value):
                continue
            py_value = python_row.get(feature_name)
            if py_value is None or pd.isna(py_value):
                continue
            diff = abs(float(py_value) - float(mt5_value))
            diffs.append((feature_name, diff, float(mt5_value), float(py_value)))
            per_feature_diffs[feature_name].append(diff)
            current_worst = per_feature_worst_ts.get(feature_name)
            if current_worst is None or diff > current_worst[0]:
                per_feature_worst_ts[feature_name] = (diff, timestamp.isoformat())

        if not diffs:
            row_records.append(
                {
                    "timestamp": timestamp.isoformat(),
                    "bar_time_server": snapshot["bar_time_server"],
                    "row_ready": row_ready,
                    "skip_reason": snapshot.get("skip_reason", ""),
                    "matched_feature_count": 0,
                    "max_abs_diff": None,
                    "mean_abs_diff": None,
                    "top_feature_diffs": [],
                }
            )
            continue

        diffs.sort(key=lambda item: (-item[1], item[0]))
        max_abs_diff = diffs[0][1]
        mean_abs_diff = float(np.mean([item[1] for item in diffs]))
        if max_abs_diff <= 1e-9:
            tolerance_counters["row_le_1e9"] += 1
        if max_abs_diff <= 1e-6:
            tolerance_counters["row_le_1e6"] += 1
        if max_abs_diff <= 1e-4:
            tolerance_counters["row_le_1e4"] += 1

        row_records.append(
            {
                "timestamp": timestamp.isoformat(),
                "bar_time_server": snapshot["bar_time_server"],
                "row_ready": row_ready,
                "skip_reason": snapshot.get("skip_reason", ""),
                "matched_feature_count": len(diffs),
                "max_abs_diff": max_abs_diff,
                "mean_abs_diff": mean_abs_diff,
                "top_feature_diffs": [
                    {
                        "feature": feature_name,
                        "abs_diff": diff,
                        "mt5_value": mt5_value,
                        "python_value": py_value,
                    }
                    for feature_name, diff, mt5_value, py_value in diffs[:5]
                ],
            }
        )

    row_records.sort(key=lambda item: (item["max_abs_diff"] is None, -(item["max_abs_diff"] or -1.0), item["timestamp"]))

    feature_records = []
    for feature_name in feature_names:
        diffs = per_feature_diffs.get(feature_name, [])
        summary = summarize_array(diffs)
        worst = per_feature_worst_ts.get(feature_name)
        feature_records.append(
            {
                "feature": feature_name,
                "count": summary["count"],
                "mean_abs_diff": summary["mean"],
                "median_abs_diff": summary["median"],
                "p90_abs_diff": summary["p90"],
                "max_abs_diff": summary["max"],
                "worst_timestamp": worst[1] if worst is not None else None,
            }
        )
    feature_records.sort(
        key=lambda item: (
            item["max_abs_diff"] is None,
            -(item["max_abs_diff"] or -1.0),
            -(item["mean_abs_diff"] or -1.0),
            item["feature"],
        )
    )

    row_max_abs_values = [float(item["max_abs_diff"]) for item in row_records if item["max_abs_diff"] is not None]
    payload = {
        "reviewed_on_utc": datetime.now(tz=UTC).isoformat(),
        "snapshot_row_count": len(snapshot_rows),
        "ready_row_count": ready_rows,
        "skip_row_count": skip_rows,
        "rows_with_feature_matrix_match": rows_with_matrix_match,
        "rows_missing_feature_matrix_timestamp": len(missing_rows),
        "row_max_abs_diff": summarize_array(row_max_abs_values),
        "row_tolerance_counts": {
            "le_1e-9": int(tolerance_counters["row_le_1e9"]),
            "le_1e-6": int(tolerance_counters["row_le_1e6"]),
            "le_1e-4": int(tolerance_counters["row_le_1e4"]),
        },
        "top_feature_drifts": feature_records[:20],
        "worst_rows": row_records[:15],
        "missing_rows": missing_rows[:15],
        "external_status_breakdown": {
            symbol: dict(counter)
            for symbol, counter in sorted(external_status_counts.items())
        },
    }
    return payload


def render_markdown(payload: dict[str, object], snapshot_path: Path) -> str:
    row_summary = payload["row_max_abs_diff"]
    tolerance_counts = payload["row_tolerance_counts"]
    lines = [
        "# Stage 41 Targeted Feature Snapshot Audit",
        "",
        f"- reviewed_on_utc: `{payload['reviewed_on_utc']}`",
        f"- snapshot_jsonl: `{snapshot_path}`",
        f"- snapshot rows: `{payload['snapshot_row_count']}`",
        f"- ready rows: `{payload['ready_row_count']}`",
        f"- skip rows: `{payload['skip_row_count']}`",
        f"- matched feature rows: `{payload['rows_with_feature_matrix_match']}`",
        f"- missing feature-matrix timestamps: `{payload['rows_missing_feature_matrix_timestamp']}`",
        "",
        "## Executive Read",
        "",
        f"- row max abs diff: `mean={fmt_num(row_summary['mean'])}` `median={fmt_num(row_summary['median'])}` `p90={fmt_num(row_summary['p90'])}` `max={fmt_num(row_summary['max'])}`",
        f"- tolerance counts: `le_1e-9={tolerance_counts['le_1e-9']}` `le_1e-6={tolerance_counts['le_1e-6']}` `le_1e-4={tolerance_counts['le_1e-4']}`",
        "",
        "## Top Feature Drifts",
        "",
    ]

    for row in payload["top_feature_drifts"]:
        lines.append(
            f"- `{row['feature']}` `count={row['count']}` `mean={fmt_num(row['mean_abs_diff'])}` "
            f"`p90={fmt_num(row['p90_abs_diff'])}` `max={fmt_num(row['max_abs_diff'])}` "
            f"`worst_ts={row['worst_timestamp'] or 'n/a'}`"
        )

    lines.extend(
        [
            "",
            "## Worst Rows",
            "",
        ]
    )
    for row in payload["worst_rows"]:
        top_parts = [
            f"{item['feature']}={fmt_num(item['abs_diff'])}"
            for item in row["top_feature_diffs"]
        ]
        lines.append(
            f"- `{row['bar_time_server']}` `ready={row['row_ready']}` `skip={row['skip_reason'] or 'n/a'}` "
            f"`matched={row['matched_feature_count']}` `max={fmt_num(row['max_abs_diff'])}` "
            f"`mean={fmt_num(row['mean_abs_diff'])}` `top={'; '.join(top_parts) if top_parts else 'n/a'}`"
        )

    lines.extend(
        [
            "",
            "## External Telemetry",
            "",
        ]
    )
    for symbol, counts in payload["external_status_breakdown"].items():
        formatted = " ".join(f"`{status}={count}`" for status, count in counts.items())
        lines.append(f"- `{symbol}` {formatted}")

    if payload["missing_rows"]:
        lines.extend(
            [
                "",
                "## Missing Timestamps",
                "",
            ]
        )
        for row in payload["missing_rows"]:
            lines.append(
                f"- `{row['bar_time_server']}` `ready={row['row_ready']}` `skip={row['skip_reason'] or 'n/a'}`"
            )

    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- Use the top feature drift table to identify the first exact-timestamp mismatch before touching model logic.",
            "- Use the external telemetry breakdown to decide whether the first divergence is driven by exact-match failures, stale fallback, or a downstream derived-feature calculation gap.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    args = build_parser().parse_args()
    snapshot_path = Path(args.snapshot_jsonl).resolve()
    feature_matrix_path = Path(args.feature_matrix).resolve()
    feature_schema_path = Path(args.feature_schema).resolve()
    output_json, output_md = build_output_paths(args.output_stem)

    if not snapshot_path.exists():
        raise FileNotFoundError(f"snapshot jsonl not found: {snapshot_path}")
    if not feature_matrix_path.exists():
        raise FileNotFoundError(f"feature matrix not found: {feature_matrix_path}")
    if not feature_schema_path.exists():
        raise FileNotFoundError(f"feature schema not found: {feature_schema_path}")

    feature_names = load_json(feature_schema_path)["feature_names"]
    snapshot_rows = load_snapshot_rows(snapshot_path)
    feature_df = pd.read_parquet(feature_matrix_path)
    feature_df["timestamp"] = pd.to_datetime(feature_df["timestamp"], utc=True)
    feature_df = (
        feature_df[feature_df["symbol"] == args.symbol]
        .drop_duplicates(subset="timestamp", keep="last")
        .set_index("timestamp")
        .sort_index()
    )

    payload = build_payload(snapshot_rows, feature_df, feature_names)
    payload["snapshot_jsonl"] = str(snapshot_path)
    payload["feature_matrix"] = str(feature_matrix_path)
    payload["feature_schema"] = str(feature_schema_path)

    write_json(output_json, payload)
    write_text(output_md, render_markdown(payload, snapshot_path))
    print(f"[done] json={output_json}")
    print(f"[done] md={output_md}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
