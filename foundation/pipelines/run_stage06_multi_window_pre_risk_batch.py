#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import sys
import traceback
from collections import defaultdict
from pathlib import Path
from typing import Any

import pandas as pd

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from foundation.pipelines.experiment_bundle_models import ExperimentBundle, SplitBoundaries
from foundation.pipelines.run_stage06_direction_split_segmented_overlay import (
    build_cross_segment_summary,
    build_segment_results,
    format_metric,
    load_attempt_summaries,
    stage06_paths,
    utc_now_iso,
    write_json,
    write_text,
)
from foundation.pipelines.run_stage06_early_wfo_lp_compare import patch_bundle
from foundation.pipelines.run_stage06_pre_risk_pool_batch import (
    iter_pre_risk_runs,
    prepare_overlay_bundle,
    run_tester,
)


SOURCE_STAGE_ROOT = ROOT_DIR / "stages" / "05_optimization" / "02_runs" / "active"
STAGE06_ROOT = ROOT_DIR / "stages" / "06_segmented_risk_validation"
DEFAULT_DATASET_PATH = ROOT_DIR / "stages" / "01_base_feature_ml" / "01_inputs" / "stage01c_h03_band000125_dataset.parquet"

WINDOW_SPECS = [
    ("2310", "2022-09-01T00:00:00Z", "2023-10-01T00:00:00Z", "2024-07-01T00:00:00Z", "2024-12-01T00:00:00Z"),
    ("2401", "2022-09-01T00:00:00Z", "2024-01-01T00:00:00Z", "2024-10-01T00:00:00Z", "2025-03-01T00:00:00Z"),
    ("2404", "2022-09-01T00:00:00Z", "2024-04-01T00:00:00Z", "2025-01-01T00:00:00Z", "2025-06-01T00:00:00Z"),
    ("2407", "2022-09-01T00:00:00Z", "2024-07-01T00:00:00Z", "2025-04-01T00:00:00Z", "2025-09-01T00:00:00Z"),
    ("2410", "2022-09-01T00:00:00Z", "2024-10-01T00:00:00Z", "2025-07-01T00:00:00Z", "2025-12-01T00:00:00Z"),
    ("2501", "2022-09-01T00:00:00Z", "2025-01-01T00:00:00Z", "2025-10-01T00:00:00Z", "2026-03-01T00:00:00Z"),
]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run a sequential Stage 06 multi-window pre-risk batch across the 05A~05FZ source pool."
    )
    parser.add_argument("--stage-root", default=str(STAGE06_ROOT), help="Stage 06 root directory.")
    parser.add_argument("--source-root", default=str(SOURCE_STAGE_ROOT), help="Stage 05 active run directory.")
    parser.add_argument("--dataset-path", default=str(DEFAULT_DATASET_PATH), help="Shared dataset parquet for window counts.")
    parser.add_argument("--batch-id", default="06H", help="Batch id used for Stage 06 artifacts.")
    parser.add_argument("--risk-pct", type=float, default=2.0, help="Balance risk percent.")
    parser.add_argument("--stop-atr-period", type=int, default=14, help="ATR period.")
    parser.add_argument("--stop-long-atr-mult", type=float, default=1.4, help="Long-side ATR multiplier.")
    parser.add_argument("--stop-short-atr-mult", type=float, default=2.0, help="Short-side ATR multiplier.")
    parser.add_argument("--max-runs-per-window", type=int, help="Optional cap per window for smoke mode.")
    parser.add_argument("--rebuild-bundle", action="store_true", help="Force per-run bundle rebuild.")
    return parser


def parse_utc(raw_value: str) -> pd.Timestamp:
    ts = pd.Timestamp(raw_value)
    if ts.tzinfo is None:
        ts = ts.tz_localize("UTC")
    else:
        ts = ts.tz_convert("UTC")
    return ts


def label_rank(label: str) -> int:
    value = 0
    for char in label:
        value = (value * 26) + (ord(char) - ord("A") + 1)
    return value


def make_run_names(batch_id: str, window_token: str, stage_id: str, ordinal: int) -> tuple[str, str]:
    token = stage_id.lower()
    ordinal_token = f"{ordinal:02d}"
    return f"{batch_id}_{window_token}_{stage_id}_{ordinal_token}", f"exp_{batch_id.lower()}_{window_token}_{token}_{ordinal_token}"


def derive_window_catalog(dataset_path: Path) -> list[dict[str, Any]]:
    dataset = pd.read_parquet(dataset_path, columns=["timestamp", "is_feature_row_valid"])
    dataset["timestamp"] = pd.to_datetime(dataset["timestamp"], utc=True)
    dataset = dataset[dataset["is_feature_row_valid"].fillna(False)].copy()

    catalog: list[dict[str, Any]] = []
    for token, train_start_raw, train_end_raw, validation_end_raw, test_end_raw in WINDOW_SPECS:
        train_start = parse_utc(train_start_raw)
        train_end = parse_utc(train_end_raw)
        validation_end = parse_utc(validation_end_raw)
        test_end = parse_utc(test_end_raw)
        train_count = int(((dataset["timestamp"] >= train_start) & (dataset["timestamp"] < train_end)).sum())
        validation_count = int(((dataset["timestamp"] >= train_end) & (dataset["timestamp"] < validation_end)).sum())
        test_count = int(((dataset["timestamp"] >= validation_end) & (dataset["timestamp"] < test_end)).sum())
        catalog.append(
            {
                "token": token,
                "split_boundaries": SplitBoundaries(
                    train_start_utc=train_start.isoformat().replace("+00:00", "Z"),
                    train_end_utc_exclusive=train_end.isoformat().replace("+00:00", "Z"),
                    validation_end_utc_exclusive=validation_end.isoformat().replace("+00:00", "Z"),
                    test_end_utc_exclusive=test_end.isoformat().replace("+00:00", "Z"),
                ),
                "split_counts": {
                    "train": train_count,
                    "validation": validation_count,
                    "test": test_count,
                },
                "segment_scheme": build_segment_scheme(train_end, validation_end, test_end),
            }
        )
    return catalog


def build_segment_scheme(
    validation_start: pd.Timestamp,
    validation_end: pd.Timestamp,
    test_end: pd.Timestamp,
) -> dict[str, list[tuple[str, Any, Any]]]:
    validation_q1_end = validation_start + pd.DateOffset(months=3)
    validation_q2_end = validation_start + pd.DateOffset(months=6)
    test_start = validation_end
    holdout_a_end = test_start + pd.Timedelta(days=45)
    holdout_b_end = holdout_a_end + pd.Timedelta(days=46)
    return {
        "validation": [
            ("validation_q1", validation_start.to_pydatetime().replace(tzinfo=None), validation_q1_end.to_pydatetime().replace(tzinfo=None)),
            ("validation_q2", validation_q1_end.to_pydatetime().replace(tzinfo=None), validation_q2_end.to_pydatetime().replace(tzinfo=None)),
            ("validation_q3", validation_q2_end.to_pydatetime().replace(tzinfo=None), validation_end.to_pydatetime().replace(tzinfo=None)),
        ],
        "test": [
            ("holdout_a", test_start.to_pydatetime().replace(tzinfo=None), holdout_a_end.to_pydatetime().replace(tzinfo=None)),
            ("holdout_b", holdout_a_end.to_pydatetime().replace(tzinfo=None), holdout_b_end.to_pydatetime().replace(tzinfo=None)),
            ("holdout_c", holdout_b_end.to_pydatetime().replace(tzinfo=None), test_end.to_pydatetime().replace(tzinfo=None)),
        ],
    }


def review_paths(stage_root: Path, batch_id: str) -> dict[str, Path]:
    review_dir = stage_root / "03_reviews"
    slug = f"{batch_id}_multi_window_pre_risk_batch"
    return {
        "manifest": stage_root / "01_inputs" / f"{slug}_manifest.json",
        "status_json": review_dir / f"{slug}_status.json",
        "status_md": review_dir / f"{slug}_status.md",
        "review_json": review_dir / f"{slug}_review.json",
        "review_md": review_dir / f"{slug}_review.md",
        "stdout_log": review_dir / f"{slug}_stdout.log",
        "stderr_log": review_dir / f"{slug}_stderr.log",
    }


def build_manifest(
    *,
    path: Path,
    source_items: list[dict[str, Any]],
    windows: list[dict[str, Any]],
    risk_pct: float,
    stop_long_atr_mult: float,
    stop_short_atr_mult: float,
    stop_atr_period: int,
) -> None:
    write_json(
        path,
        {
            "generated_at_utc": utc_now_iso(),
            "stage": "06_segmented_risk_validation",
            "phase": "06H_multi_window_pre_risk_batch",
            "source_root": str(SOURCE_STAGE_ROOT),
            "source_run_count": len(source_items),
            "window_count": len(windows),
            "windows": [
                {
                    "token": item["token"],
                    "split_boundaries": item["split_boundaries"].model_dump(),
                    "split_counts": item["split_counts"],
                }
                for item in windows
            ],
            "overlay_defaults": {
                "sizing_mode": "risk_pct",
                "risk_pct": risk_pct,
                "capital_base": "balance",
                "stop_model": "atr",
                "stop_execution_mode": "broker_native",
                "stop_policy": "direction_split",
                "stop_long_atr_mult": stop_long_atr_mult,
                "stop_short_atr_mult": stop_short_atr_mult,
                "stop_atr_period": stop_atr_period,
            },
            "source_runs": [
                {"stage_id": item["stage_id"], "run_name": item["run_name"], "path": str(item["path"])}
                for item in source_items
            ],
        },
    )


def completed_row_from_payload(
    *,
    window_token: str,
    source_item: dict[str, Any],
    target_run_name: str,
    payload: dict[str, Any],
) -> dict[str, Any]:
    validation = payload["split_runs"]["validation"]["headline"]
    test = payload["split_runs"]["test"]["headline"]
    best_segment = payload["cross_segment_summary"]["best_segment"]
    worst_segment = payload["cross_segment_summary"]["worst_segment"]
    return {
        "window_token": window_token,
        "source_stage_id": source_item["stage_id"],
        "source_run_name": source_item["run_name"],
        "target_run_name": target_run_name,
        "status": "completed",
        "validation": {
            "return_pct": validation.get("return_pct"),
            "profit_factor": validation.get("profit_factor"),
            "trade_count": validation.get("trade_count"),
            "max_dd_pct": validation.get("max_dd_pct"),
        },
        "test": {
            "return_pct": test.get("return_pct"),
            "profit_factor": test.get("profit_factor"),
            "trade_count": test.get("trade_count"),
            "max_dd_pct": test.get("max_dd_pct"),
        },
        "best_segment": best_segment,
        "worst_segment": worst_segment,
        "segmented_results_path": payload.get("segmented_results_path"),
        "review_md_path": payload.get("review_md_path"),
    }


def failure_row(window_token: str, source_item: dict[str, Any], target_run_name: str, error_text: str) -> dict[str, Any]:
    return {
        "window_token": window_token,
        "source_stage_id": source_item["stage_id"],
        "source_run_name": source_item["run_name"],
        "target_run_name": target_run_name,
        "status": "failed",
        "error": error_text,
    }


def top_rows(rows: list[dict[str, Any]], key_path: tuple[str, str], limit: int = 10) -> list[dict[str, Any]]:
    completed = [row for row in rows if row.get("status") == "completed"]

    def key_fn(row: dict[str, Any]) -> float:
        value = row.get(key_path[0], {}).get(key_path[1])
        return float(value) if value is not None else float("-inf")

    return sorted(completed, key=key_fn, reverse=True)[:limit]


def window_progress(source_total: int, window_token: str, results: list[dict[str, Any]]) -> dict[str, Any]:
    rows = [row for row in results if row.get("window_token") == window_token]
    completed = sum(1 for row in rows if row.get("status") == "completed")
    failed = sum(1 for row in rows if row.get("status") == "failed")
    return {
        "completed_count": completed,
        "failed_count": failed,
        "pending_count": source_total - completed - failed,
    }


def build_status_payload(
    *,
    batch_id: str,
    source_items: list[dict[str, Any]],
    windows: list[dict[str, Any]],
    results: list[dict[str, Any]],
    current_window: str | None,
    current_source: str | None,
    started_at_utc: str,
    finished: bool,
) -> dict[str, Any]:
    completed_count = sum(1 for row in results if row.get("status") == "completed")
    failed_count = sum(1 for row in results if row.get("status") == "failed")
    total = len(source_items) * len(windows)
    return {
        "generated_at_utc": utc_now_iso(),
        "stage": "06_segmented_risk_validation",
        "phase": "06H_multi_window_pre_risk_batch",
        "batch_id": batch_id,
        "pid": os.getpid(),
        "status": "completed" if finished else "running",
        "started_at_utc": started_at_utc,
        "last_updated_at_utc": utc_now_iso(),
        "source_total": len(source_items),
        "window_total": len(windows),
        "run_total": total,
        "completed_count": completed_count,
        "failed_count": failed_count,
        "pending_count": total - completed_count - failed_count,
        "current_window_token": current_window,
        "current_source_run_name": current_source,
        "leaders": {
            "test_return_pct": top_rows(results, ("test", "return_pct"), limit=20),
            "validation_return_pct": top_rows(results, ("validation", "return_pct"), limit=20),
        },
        "window_progress": {
            window["token"]: window_progress(len(source_items), window["token"], results)
            for window in windows
        },
        "results": results,
    }


def build_status_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# 06H Multi-Window Pre-Risk Batch Status",
        "",
        f"- status: `{payload['status']}`",
        f"- batch_id: `{payload['batch_id']}`",
        f"- pid: `{payload['pid']}`",
        f"- started_at_utc: `{payload['started_at_utc']}`",
        f"- last_updated_at_utc: `{payload['last_updated_at_utc']}`",
        f"- source_total: `{payload['source_total']}`",
        f"- window_total: `{payload['window_total']}`",
        f"- run_total: `{payload['run_total']}`",
        f"- completed_count: `{payload['completed_count']}`",
        f"- failed_count: `{payload['failed_count']}`",
        f"- pending_count: `{payload['pending_count']}`",
    ]
    if payload.get("current_window_token"):
        lines.append(f"- current_window_token: `{payload['current_window_token']}`")
    if payload.get("current_source_run_name"):
        lines.append(f"- current_source_run_name: `{payload['current_source_run_name']}`")

    lines.extend(["", "## Window Progress", ""])
    for token, progress in payload["window_progress"].items():
        lines.append(
            f"- `{token}`: completed `{progress['completed_count']}`, failed `{progress['failed_count']}`, pending `{progress['pending_count']}`"
        )

    lines.extend(["", "## Top Holdout Returns", ""])
    for row in payload["leaders"]["test_return_pct"][:20]:
        test = row["test"]
        lines.append(
            f"- `{row['window_token']}` `{row['source_stage_id']}` -> `{row['target_run_name']}`: "
            f"return_pct `{format_metric(test.get('return_pct'), 3)}`, PF `{format_metric(test.get('profit_factor'), 4)}`, trades `{test.get('trade_count')}`"
        )
    lines.append("")
    return "\n".join(lines)


def build_final_review(payload: dict[str, Any]) -> dict[str, Any]:
    completed_rows = [row for row in payload["results"] if row.get("status") == "completed"]
    failed_rows = [row for row in payload["results"] if row.get("status") == "failed"]
    window_leaders: dict[str, dict[str, Any] | None] = {}
    for token in payload["window_progress"].keys():
        rows = [row for row in completed_rows if row.get("window_token") == token]
        if rows:
            window_leaders[token] = max(rows, key=lambda row: float(row["test"].get("return_pct") or float("-inf")))
        else:
            window_leaders[token] = None
    return {
        "generated_at_utc": utc_now_iso(),
        "stage": "06_segmented_risk_validation",
        "phase": "06H_multi_window_pre_risk_batch",
        "source_total": payload["source_total"],
        "window_total": payload["window_total"],
        "run_total": payload["run_total"],
        "completed_count": payload["completed_count"],
        "failed_count": payload["failed_count"],
        "best_holdout": payload["leaders"]["test_return_pct"][0] if payload["leaders"]["test_return_pct"] else None,
        "top_holdout": payload["leaders"]["test_return_pct"],
        "top_validation": payload["leaders"]["validation_return_pct"],
        "window_leaders": window_leaders,
        "failed_runs": failed_rows,
        "completed_runs": completed_rows,
    }


def build_final_review_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# 06H Multi-Window Pre-Risk Batch Review",
        "",
        f"- generated_at_utc: `{payload['generated_at_utc']}`",
        f"- run_total: `{payload['run_total']}`",
        f"- completed_count: `{payload['completed_count']}`",
        f"- failed_count: `{payload['failed_count']}`",
        "",
        "## Window Leaders",
        "",
    ]
    for token, row in payload["window_leaders"].items():
        if row is None:
            lines.append(f"- `{token}`: `no completed rows`")
            continue
        test = row["test"]
        lines.append(
            f"- `{token}`: `{row['source_stage_id']}` -> `{row['target_run_name']}`, return_pct `{format_metric(test.get('return_pct'), 3)}`, PF `{format_metric(test.get('profit_factor'), 4)}`, max_dd_pct `{format_metric(test.get('max_dd_pct'), 4)}`"
        )
    lines.extend(["", "## Top Holdout Overall", ""])
    for row in payload["top_holdout"][:20]:
        test = row["test"]
        lines.append(
            f"- `{row['window_token']}` `{row['source_stage_id']}` `{row['source_run_name']}` -> `{row['target_run_name']}`: "
            f"return_pct `{format_metric(test.get('return_pct'), 3)}`, PF `{format_metric(test.get('profit_factor'), 4)}`, trades `{test.get('trade_count')}`, max_dd_pct `{format_metric(test.get('max_dd_pct'), 4)}`"
        )
    if payload["failed_runs"]:
        lines.extend(["", "## Failed Runs", ""])
        for row in payload["failed_runs"][:50]:
            lines.append(f"- `{row['window_token']}` `{row['source_stage_id']}` `{row['source_run_name']}`: `{row['error']}`")
    lines.append("")
    return "\n".join(lines)


def update_review_index(review_index_path: Path) -> None:
    lines = review_index_path.read_text(encoding="utf-8").splitlines() if review_index_path.exists() else []
    wanted = "- `06H`: see `06H_multi_window_pre_risk_batch_status.md` and `06H_multi_window_pre_risk_batch_review.md`"
    if not lines:
        lines = ["# Review Index", "", "## Current Entries"]
    if "## Current Entries" not in lines:
        lines.extend(["", "## Current Entries"])
    if wanted not in lines:
        lines.append(wanted)
    write_text(review_index_path, "\n".join(lines).rstrip() + "\n")


def update_selection_status(selection_path: Path, status_payload: dict[str, Any], paths: dict[str, Path]) -> None:
    lines = [
        "# Selection Status",
        "",
        "- stage: `06_segmented_risk_validation`",
        f"- current phase active: `{status_payload['batch_id']}`",
        "- current mode: `sequential multi-window pre-risk overlay batch`",
        "- overlay config: `risk_pct=2.00, broker_native SL, direction_split(long=1.40, short=2.00), ATR14`",
        f"- batch progress: `completed={status_payload['completed_count']}/{status_payload['run_total']}`, `failed={status_payload['failed_count']}`, `pending={status_payload['pending_count']}`",
        f"- status file: `{paths['status_json'].name}`",
    ]
    best = status_payload["leaders"]["test_return_pct"][0] if status_payload["leaders"]["test_return_pct"] else None
    if best:
        test = best["test"]
        lines.append(
            f"- current best completed holdout row: `{best['window_token']}` `{best['source_stage_id']}` -> `{best['target_run_name']}`, `return_pct={format_metric(test.get('return_pct'), 3)}`, `PF={format_metric(test.get('profit_factor'), 4)}`"
        )
    lines.append("- next action: `let 06H finish, then compare window-by-window leaders and robustness across the six anchors`")
    write_text(selection_path, "\n".join(lines) + "\n")


def create_single_run_payload(
    *,
    source_item: dict[str, Any],
    run_name: str,
    experiment_id: str,
    run_dir: Path,
    risk_pct: float,
    stop_long_atr_mult: float,
    stop_short_atr_mult: float,
    stop_atr_period: int,
    window: dict[str, Any],
) -> dict[str, Any]:
    bundle = ExperimentBundle.from_json((run_dir / "experiment_bundle.json").read_text(encoding="utf-8-sig"))
    summaries = load_attempt_summaries(run_dir)
    if "validation" not in summaries or "test" not in summaries:
        raise FileNotFoundError(f"missing validation/test summaries in {run_dir}")

    segmented_results = {
        "validation": build_segment_results(bundle, "validation", summaries["validation"], scheme=window["segment_scheme"]),
        "test": build_segment_results(bundle, "test", summaries["test"], scheme=window["segment_scheme"]),
    }
    return {
        "generated_at_utc": utc_now_iso(),
        "stage": "06_segmented_risk_validation",
        "phase": "06H_multi_window_pre_risk_batch",
        "window_token": window["token"],
        "run_name": run_name,
        "experiment_id": experiment_id,
        "source_stage_id": source_item["stage_id"],
        "source_run_name": source_item["run_name"],
        "source_run_dir": str(source_item["path"]),
        "overlay": {
            "risk_pct": risk_pct,
            "stop_execution_mode": "broker_native",
            "stop_policy": "direction_split",
            "stop_long_atr_mult": stop_long_atr_mult,
            "stop_short_atr_mult": stop_short_atr_mult,
            "stop_atr_period": stop_atr_period,
        },
        "wfo_window": window["split_boundaries"].model_dump(),
        "split_runs": {
            "validation": bundle.results.by_split["validation"].model_dump(),
            "test": bundle.results.by_split["test"].model_dump(),
        },
        "segmented_results": segmented_results,
        "cross_segment_summary": build_cross_segment_summary(segmented_results),
    }


def main() -> int:
    args = build_parser().parse_args()

    stage_root = Path(args.stage_root).resolve()
    source_root = Path(args.source_root).resolve()
    dataset_path = Path(args.dataset_path).resolve()
    paths = review_paths(stage_root, args.batch_id)
    stage_paths = stage06_paths(stage_root)

    source_items = iter_pre_risk_runs(source_root)
    windows = derive_window_catalog(dataset_path)
    if args.max_runs_per_window:
        source_items = source_items[: args.max_runs_per_window]
    if not source_items:
        raise RuntimeError("no pre-risk Stage 05 runs found for 05A~05FZ")

    build_manifest(
        path=paths["manifest"],
        source_items=source_items,
        windows=windows,
        risk_pct=args.risk_pct,
        stop_long_atr_mult=args.stop_long_atr_mult,
        stop_short_atr_mult=args.stop_short_atr_mult,
        stop_atr_period=args.stop_atr_period,
    )
    update_review_index(stage_paths["review_index"])

    duplicate_counter: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    started_at_utc = utc_now_iso()
    results: list[dict[str, Any]] = []

    for window in windows:
        for source_item in source_items:
            duplicate_counter[window["token"]][source_item["stage_id"]] += 1
            run_name, experiment_id = make_run_names(
                args.batch_id,
                window["token"],
                source_item["stage_id"],
                duplicate_counter[window["token"]][source_item["stage_id"]],
            )

            status_payload = build_status_payload(
                batch_id=args.batch_id,
                source_items=source_items,
                windows=windows,
                results=results,
                current_window=window["token"],
                current_source=source_item["run_name"],
                started_at_utc=started_at_utc,
                finished=False,
            )
            write_json(paths["status_json"], status_payload)
            write_text(paths["status_md"], build_status_markdown(status_payload))
            update_selection_status(stage_paths["selection"], status_payload, paths)

            run_dir = stage_root / "02_runs" / "active" / run_name
            segmented_json_path = run_dir / "segmented_results.json"
            if segmented_json_path.exists() and not args.rebuild_bundle:
                payload = json.loads(segmented_json_path.read_text(encoding="utf-8-sig"))
                payload["segmented_results_path"] = str(segmented_json_path)
                payload["review_md_path"] = str(run_dir / "segmented_results.md")
                results.append(
                    completed_row_from_payload(
                        window_token=window["token"],
                        source_item=source_item,
                        target_run_name=run_name,
                        payload=payload,
                    )
                )
                continue

            try:
                bundle_path, _ = prepare_overlay_bundle(
                    source_item=source_item,
                    run_dir=run_dir,
                    run_name=run_name,
                    experiment_id=experiment_id,
                    batch_id=args.batch_id,
                    risk_pct=args.risk_pct,
                    stop_long_atr_mult=args.stop_long_atr_mult,
                    stop_short_atr_mult=args.stop_short_atr_mult,
                    stop_atr_period=args.stop_atr_period,
                    rebuild_bundle=args.rebuild_bundle,
                )
                patch_bundle(
                    bundle_path=bundle_path,
                    split_boundaries=window["split_boundaries"],
                    split_counts=window["split_counts"],
                    runtime_extra={
                        "window_token": window["token"],
                        "wfo_mode": "model_fixed_shifted_window",
                    },
                    wfo_metadata={
                        "window_token": window["token"],
                        "window_phase": "06H_multi_window_pre_risk_batch",
                    },
                )
                run_tester(bundle_path, "validation")
                run_tester(bundle_path, "test")

                payload = create_single_run_payload(
                    source_item=source_item,
                    run_name=run_name,
                    experiment_id=experiment_id,
                    run_dir=run_dir,
                    risk_pct=args.risk_pct,
                    stop_long_atr_mult=args.stop_long_atr_mult,
                    stop_short_atr_mult=args.stop_short_atr_mult,
                    stop_atr_period=args.stop_atr_period,
                    window=window,
                )
                payload["segmented_results_path"] = str(segmented_json_path)
                payload["review_md_path"] = str(run_dir / "segmented_results.md")
                write_json(segmented_json_path, payload)
                write_text(run_dir / "segmented_results.md", json.dumps(payload["cross_segment_summary"], ensure_ascii=False, indent=2) + "\n")
                results.append(
                    completed_row_from_payload(
                        window_token=window["token"],
                        source_item=source_item,
                        target_run_name=run_name,
                        payload=payload,
                    )
                )
            except Exception as exc:
                error_text = "".join(traceback.format_exception_only(type(exc), exc)).strip()
                results.append(failure_row(window["token"], source_item, run_name, error_text))

    final_status = build_status_payload(
        batch_id=args.batch_id,
        source_items=source_items,
        windows=windows,
        results=results,
        current_window=None,
        current_source=None,
        started_at_utc=started_at_utc,
        finished=True,
    )
    write_json(paths["status_json"], final_status)
    write_text(paths["status_md"], build_status_markdown(final_status))
    update_selection_status(stage_paths["selection"], final_status, paths)

    final_review = build_final_review(final_status)
    write_json(paths["review_json"], final_review)
    write_text(paths["review_md"], build_final_review_markdown(final_review))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
