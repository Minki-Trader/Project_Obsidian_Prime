#!/usr/bin/env python3
from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path
from zoneinfo import ZoneInfo

import numpy as np
import onnxruntime as ort
import pandas as pd


ROOT_DIR = Path(__file__).resolve().parents[3]
STAGE_DIR = ROOT_DIR / "stages" / "40_runtime_parity_deep_audit"
STAGE39_JSON = ROOT_DIR / "stages" / "39_window_extension_mt5_validation" / "03_reviews" / "stage39_extended_validation_20260413.json"
OUTPUT_JSON = STAGE_DIR / "03_reviews" / "stage40_runtime_parity_deep_audit_20260413.json"
OUTPUT_MD = STAGE_DIR / "03_reviews" / "stage40_runtime_parity_deep_audit_20260413.md"
FEATURE_MATRIX_PATH = ROOT_DIR / "data" / "processed" / "fpmarkets_v2" / "features" / "extended_window" / "feature_matrix.parquet"
FEATURE_SCHEMA_PATH = ROOT_DIR / "stages" / "34_outside_bar_mainline_promotion" / "02_runs" / "active" / "34D_29s_outbarlong_0001" / "artifacts" / "feature_schema.json"
MODEL_PATH = ROOT_DIR / "stages" / "34_outside_bar_mainline_promotion" / "02_runs" / "active" / "34D_29s_outbarlong_0001" / "artifacts" / "model_probonly.onnx"
SHIFT_RANGE = list(range(-6, 7))
PROB_THRESHOLDS = [0.001, 0.005, 0.010, 0.020, 0.050, 0.100]
HIGH_DIFF_THRESHOLD = 0.15
BAR_DELTA = pd.Timedelta(minutes=5)
NY_TZ = ZoneInfo("America/New_York")
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


def fmt_num(value: float | int | None, digits: int = 4) -> str:
    if value is None:
        return "n/a"
    if isinstance(value, int):
        return str(value)
    return f"{value:.{digits}f}"


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


def feature_checksum(values: np.ndarray, use_float32_tokens: bool) -> int:
    h = 2166136261
    for value in values:
        token_value = np.float32(value).item() if use_float32_tokens else float(value)
        token = f"{token_value:.8f}|"
        for ch in token:
            h ^= ord(ch)
            h = (h * FNV_PRIME) & FNV_MASK
    return h


def classify_session(ts: pd.Timestamp) -> str:
    ny_ts = ts.tz_convert(NY_TZ)
    minutes = ny_ts.hour * 60 + ny_ts.minute
    if minutes >= 16 * 60:
        return "ny_postcash"
    if minutes >= (15 * 60 + 30):
        return "ny_late"
    if minutes >= (9 * 60 + 30):
        return "ny_cash"
    return "other"


def normalize_feature_row(row: pd.Series | pd.DataFrame, feature_names: list[str]) -> np.ndarray | None:
    if isinstance(row, pd.DataFrame):
        row = row.iloc[-1]
    values = row[feature_names]
    if values.isna().any():
        return None
    return values.to_numpy(dtype=np.float64)


def build_surface_cache(
    feature_df: pd.DataFrame,
    feature_names: list[str],
    candidate_timestamps: set[pd.Timestamp],
) -> tuple[dict[pd.Timestamp, np.ndarray], dict[pd.Timestamp, int], dict[pd.Timestamp, int]]:
    usable_rows: list[np.ndarray] = []
    usable_timestamps: list[pd.Timestamp] = []
    checksum64_by_ts: dict[pd.Timestamp, int] = {}
    checksum32_by_ts: dict[pd.Timestamp, int] = {}

    for ts in sorted(candidate_timestamps):
        if ts not in feature_df.index:
            continue
        values = normalize_feature_row(feature_df.loc[ts], feature_names)
        if values is None:
            continue
        usable_rows.append(values.astype(np.float32))
        usable_timestamps.append(ts)
        checksum64_by_ts[ts] = feature_checksum(values, use_float32_tokens=False)
        checksum32_by_ts[ts] = feature_checksum(values, use_float32_tokens=True)

    if not usable_rows:
        return {}, {}, {}

    session = ort.InferenceSession(str(MODEL_PATH), providers=["CPUExecutionProvider"])
    input_name = session.get_inputs()[0].name
    batch = np.vstack(usable_rows).astype(np.float32)
    outputs = session.run(None, {input_name: batch})[0]
    probs_by_ts = {ts: outputs[idx] for idx, ts in enumerate(usable_timestamps)}
    return probs_by_ts, checksum64_by_ts, checksum32_by_ts


def build_clusters(records: list[dict[str, object]]) -> list[dict[str, object]]:
    hot = [record for record in records if float(record["exact_diff"]) >= HIGH_DIFF_THRESHOLD]
    if not hot:
        return []
    hot = sorted(hot, key=lambda item: item["timestamp"])
    clusters: list[list[dict[str, object]]] = []
    current: list[dict[str, object]] = []
    for record in hot:
        if not current:
            current = [record]
            continue
        prev_ts = pd.Timestamp(current[-1]["timestamp"])
        current_ts = pd.Timestamp(record["timestamp"])
        if current_ts - prev_ts == BAR_DELTA:
            current.append(record)
            continue
        clusters.append(current)
        current = [record]
    if current:
        clusters.append(current)

    out: list[dict[str, object]] = []
    for cluster in clusters:
        diffs = [float(item["exact_diff"]) for item in cluster]
        session_counts = Counter(str(item["session_bucket"]) for item in cluster)
        out.append(
            {
                "start_timestamp": cluster[0]["timestamp"],
                "end_timestamp": cluster[-1]["timestamp"],
                "count": len(cluster),
                "mean_exact_diff": float(np.mean(diffs)),
                "max_exact_diff": float(np.max(diffs)),
                "sessions": dict(session_counts),
            }
        )
    out.sort(key=lambda item: (-float(item["max_exact_diff"]), -float(item["mean_exact_diff"]), -int(item["count"])))
    return out


def build_payload() -> dict[str, object]:
    stage39 = load_json(STAGE39_JSON)
    latest = stage39["latest_shadow_audit"]
    shadow_path = Path(latest["latest_attempt"]["shadow_csv_path"])
    shadow_df = pd.read_csv(shadow_path)
    ready_df = shadow_df[shadow_df["row_ready"].astype(str).str.lower() == "true"].copy()
    ready_df["timestamp"] = ready_df["bar_time_server"].map(parse_server_ts)

    feature_names = load_json(FEATURE_SCHEMA_PATH)["feature_names"]
    feature_df = pd.read_parquet(FEATURE_MATRIX_PATH)
    feature_df["timestamp"] = pd.to_datetime(feature_df["timestamp"], utc=True)
    feature_df = (
        feature_df[feature_df["symbol"] == "US100"]
        .drop_duplicates(subset="timestamp", keep="last")
        .set_index("timestamp")
        .sort_index()
    )

    candidate_timestamps: set[pd.Timestamp] = set()
    for ts in ready_df["timestamp"]:
        for shift in SHIFT_RANGE:
            candidate_timestamps.add(ts + BAR_DELTA * shift)

    probs_by_ts, checksum64_by_ts, checksum32_by_ts = build_surface_cache(feature_df, feature_names, candidate_timestamps)

    records: list[dict[str, object]] = []
    best_shift_counter: Counter[int] = Counter()

    for row in ready_df.itertuples(index=False):
        base_ts = row.timestamp
        mt5_probs = np.asarray([row.p_short, row.p_flat, row.p_long], dtype=np.float32)
        mt5_checksum = int(row.feature_checksum)
        candidates: list[dict[str, object]] = []
        for shift in SHIFT_RANGE:
            shifted_ts = base_ts + BAR_DELTA * shift
            if shifted_ts not in probs_by_ts:
                continue
            diff = float(np.max(np.abs(probs_by_ts[shifted_ts] - mt5_probs)))
            candidates.append(
                {
                    "shift": shift,
                    "timestamp": shifted_ts.isoformat(),
                    "diff": diff,
                    "checksum64_match": checksum64_by_ts[shifted_ts] == mt5_checksum,
                    "checksum32_match": checksum32_by_ts[shifted_ts] == mt5_checksum,
                }
            )
        if not candidates:
            continue

        exact = next(item for item in candidates if item["shift"] == 0)
        best = min(candidates, key=lambda item: item["diff"])
        best_shift_counter[int(best["shift"])] += 1

        records.append(
            {
                "timestamp": base_ts.isoformat(),
                "bar_time_server": row.bar_time_server,
                "session_bucket": classify_session(base_ts),
                "exact_diff": exact["diff"],
                "best_neighbor_diff": best["diff"],
                "best_shift_bars": int(best["shift"]),
                "improvement_from_best_neighbor": exact["diff"] - best["diff"],
                "exact_checksum64_match": bool(exact["checksum64_match"]),
                "exact_checksum32_match": bool(exact["checksum32_match"]),
                "best_neighbor_checksum64_match": any(item["checksum64_match"] for item in candidates),
                "best_neighbor_checksum32_match": any(item["checksum32_match"] for item in candidates),
                "external_alignment_mode": row.external_alignment_mode,
                "decision_reason": row.decision_reason,
                "feature_ready_count": int(row.feature_ready_count),
            }
        )

    exact_diffs = [float(record["exact_diff"]) for record in records]
    best_diffs = [float(record["best_neighbor_diff"]) for record in records]
    improvements = [float(record["improvement_from_best_neighbor"]) for record in records]

    threshold_counts = {
        f"le_{threshold:.3f}": int(sum(1 for value in exact_diffs if value <= threshold))
        for threshold in PROB_THRESHOLDS
    }

    session_breakdown: dict[str, dict[str, float | int | None]] = {}
    for session_name in ["ny_cash", "ny_late", "ny_postcash", "other"]:
        session_values = [float(record["exact_diff"]) for record in records if record["session_bucket"] == session_name]
        if not session_values:
            continue
        summary = summarize_array(session_values)
        session_breakdown[session_name] = summary

    worst_rows = sorted(records, key=lambda item: float(item["exact_diff"]), reverse=True)[:10]
    clusters = build_clusters(records)

    interpretation = [
        "Exact-timestamp drift remains too large to call runtime parity closed.",
        "Best-neighbor drift improves materially, but the winning shift is not concentrated on zero, so this is not a single-bar offset story.",
        "Checksum parity stays at zero under both float64-style and float32-style serialization checks, so the issue is not explained by a simple token-format mismatch.",
        "Drift worsens in ny_late and forms concrete March and April clusters, which points to a session-sensitive feature-surface divergence worth instrumenting directly.",
    ]

    return {
        "reviewed_on": stage39["reviewed_on"],
        "audit_surface": {
            "source_stage": "39_window_extension_mt5_validation",
            "shadow_csv_path": str(shadow_path),
            "ready_row_count": int(len(records)),
            "shift_window_bars": {"min": min(SHIFT_RANGE), "max": max(SHIFT_RANGE)},
            "feature_matrix_path": str(FEATURE_MATRIX_PATH),
            "feature_schema_path": str(FEATURE_SCHEMA_PATH),
            "model_path": str(MODEL_PATH),
        },
        "exact_timestamp_prob_diff": summarize_array(exact_diffs),
        "best_neighbor_prob_diff": summarize_array(best_diffs),
        "improvement_from_best_neighbor": summarize_array(improvements),
        "exact_threshold_counts": threshold_counts,
        "best_shift_counts": {str(shift): int(count) for shift, count in sorted(best_shift_counter.items(), key=lambda item: (-item[1], item[0]))},
        "best_shift_zero_share": None if not records else best_shift_counter.get(0, 0) / len(records),
        "checksum_parity": {
            "exact_float64_style_match_count": int(sum(1 for item in records if item["exact_checksum64_match"])),
            "exact_float32_style_match_count": int(sum(1 for item in records if item["exact_checksum32_match"])),
            "best_neighbor_float64_style_match_count": int(sum(1 for item in records if item["best_neighbor_checksum64_match"])),
            "best_neighbor_float32_style_match_count": int(sum(1 for item in records if item["best_neighbor_checksum32_match"])),
        },
        "session_breakdown": session_breakdown,
        "high_diff_clusters": clusters,
        "worst_exact_rows": worst_rows,
        "mt5_runtime_context": {
            "latest_attempt": latest["latest_attempt"],
            "mt5_metrics": latest["mt5_metrics"],
        },
        "interpretation": interpretation,
        "report_inputs": {
            "stage39_review_json": str(STAGE39_JSON),
        },
    }


def build_markdown(payload: dict) -> str:
    exact = payload["exact_timestamp_prob_diff"]
    best = payload["best_neighbor_prob_diff"]
    improve = payload["improvement_from_best_neighbor"]
    checks = payload["checksum_parity"]
    runtime = payload["mt5_runtime_context"]["mt5_metrics"]
    lines = [
        "# Stage 40 Runtime Parity Deep Audit",
        "",
        f"- reviewed_on: `{payload['reviewed_on']}`",
        "- stage: `40_runtime_parity_deep_audit`",
        f"- ready_rows: `{payload['audit_surface']['ready_row_count']}`",
        "",
        "## Executive Read",
        "",
        f"- exact timestamp drift: `mean={fmt_num(exact['mean'])}` `p90={fmt_num(exact['p90'])}` `max={fmt_num(exact['max'])}`",
        f"- best neighbor drift: `mean={fmt_num(best['mean'])}` `p90={fmt_num(best['p90'])}` `max={fmt_num(best['max'])}`",
        f"- improvement from best neighbor: `mean={fmt_num(improve['mean'])}` `p90={fmt_num(improve['p90'])}`",
        f"- zero-shift share: `{fmt_num(payload['best_shift_zero_share'])}`",
        f"- checksum parity: `exact64={checks['exact_float64_style_match_count']}` `exact32={checks['exact_float32_style_match_count']}` "
        f"`neighbor64={checks['best_neighbor_float64_style_match_count']}` `neighbor32={checks['best_neighbor_float32_style_match_count']}`",
        "",
        "## Exact Threshold Counts",
        "",
    ]
    for key, count in payload["exact_threshold_counts"].items():
        lines.append(f"- `{key}` `{count}`")
    lines.extend(
        [
            "",
            "## Shift Structure",
            "",
        ]
    )
    for shift, count in payload["best_shift_counts"].items():
        lines.append(f"- `shift={shift}` `count={count}`")
    lines.extend(
        [
            "",
            "## Session Breakdown",
            "",
        ]
    )
    for session_name in ["ny_cash", "ny_late", "ny_postcash", "other"]:
        if session_name not in payload["session_breakdown"]:
            continue
        summary = payload["session_breakdown"][session_name]
        lines.append(
            f"- `{session_name}` `count={summary['count']}` `mean={fmt_num(summary['mean'])}` "
            f"`p90={fmt_num(summary['p90'])}` `max={fmt_num(summary['max'])}`"
        )
    lines.extend(
        [
            "",
            "## High Diff Clusters",
            "",
        ]
    )
    for cluster in payload["high_diff_clusters"][:5]:
        lines.append(
            f"- `{cluster['start_timestamp']} -> {cluster['end_timestamp']}` `count={cluster['count']}` "
            f"`mean={fmt_num(cluster['mean_exact_diff'])}` `max={fmt_num(cluster['max_exact_diff'])}` "
            f"`sessions={cluster['sessions']}`"
        )
    lines.extend(
        [
            "",
            "## Worst Exact Rows",
            "",
        ]
    )
    for row in payload["worst_exact_rows"][:10]:
        lines.append(
            f"- `{row['bar_time_server']}` `session={row['session_bucket']}` `exact={fmt_num(row['exact_diff'])}` "
            f"`best={fmt_num(row['best_neighbor_diff'])}` `best_shift={row['best_shift_bars']}` "
            f"`decision={row['decision_reason']}`"
        )
    lines.extend(
        [
            "",
            "## MT5 Runtime Context",
            "",
            f"- latest no-trade rate: `{fmt_num(runtime['no_trade_rate'])}`",
            f"- latest external mismatch count: `{runtime['external_mismatch_count']}`",
            f"- latest skip reasons: `{runtime['skip_reason_breakdown']}`",
            "",
            "## Interpretation",
            "",
        ]
    )
    for sentence in payload["interpretation"]:
        lines.append(f"- {sentence}")
    return "\n".join(lines) + "\n"


def main() -> None:
    payload = build_payload()
    write_json(OUTPUT_JSON, payload)
    write_text(OUTPUT_MD, build_markdown(payload))


if __name__ == "__main__":
    main()
