#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import traceback
from collections import Counter, defaultdict
from pathlib import Path
from types import SimpleNamespace
from typing import Any

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from foundation.pipelines.experiment_bundle_models import CrossSplitResults, ExperimentBundle, ResultsBlock, StatusEvent
from foundation.pipelines.export_experiment_bundle_assets import run_export_bundle_assets
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


SOURCE_STAGE_ROOT = ROOT_DIR / "stages" / "05_optimization" / "02_runs" / "active"
STAGE06_ROOT = ROOT_DIR / "stages" / "06_segmented_risk_validation"
PRE_RISK_MAX_SUFFIX = "FZ"
STAGE_ID_PATTERN = re.compile(r"^(05)([A-Z]{1,2})$")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run the Stage 06 direction-split risk overlay batch across the pre-risk 05A~05FZ pool."
    )
    parser.add_argument("--stage-root", default=str(STAGE06_ROOT), help="Stage 06 root directory.")
    parser.add_argument("--source-root", default=str(SOURCE_STAGE_ROOT), help="Stage 05 active run directory.")
    parser.add_argument("--batch-id", default="06B", help="Batch id used for Stage 06 artifacts.")
    parser.add_argument("--risk-pct", type=float, default=2.0, help="Balance risk percent.")
    parser.add_argument("--stop-atr-period", type=int, default=14, help="ATR period.")
    parser.add_argument("--stop-long-atr-mult", type=float, default=1.4, help="Long-side ATR multiplier.")
    parser.add_argument("--stop-short-atr-mult", type=float, default=2.0, help="Short-side ATR multiplier.")
    parser.add_argument("--max-runs", type=int, help="Optional cap for smoke/range runs.")
    parser.add_argument("--rebuild-bundle", action="store_true", help="Force per-run bundle rebuild.")
    return parser


def label_rank(label: str) -> int:
    value = 0
    for char in label:
        value = (value * 26) + (ord(char) - ord("A") + 1)
    return value


def iter_pre_risk_runs(source_root: Path) -> list[dict[str, Any]]:
    max_rank = label_rank(PRE_RISK_MAX_SUFFIX)
    items: list[dict[str, Any]] = []
    for path in sorted(source_root.iterdir()):
        if not path.is_dir():
            continue
        stage_id = path.name.split("_", 1)[0]
        match = STAGE_ID_PATTERN.match(stage_id)
        if not match:
            continue
        suffix = match.group(2)
        if label_rank(suffix) > max_rank:
            continue
        resolved = path.resolve()
        items.append(
            {
                "stage_id": stage_id,
                "suffix": suffix,
                "suffix_rank": label_rank(suffix),
                "run_name": path.name,
                "path": resolved,
                "has_bundle": (resolved / "experiment_bundle.json").exists(),
                "has_config": (resolved / "config.json").exists(),
                "has_model_joblib": (resolved / "model.joblib").exists(),
                "has_rule_stack": (resolved / "rule_stack.json").exists(),
            }
        )
    items.sort(key=lambda item: (item["suffix_rank"], item["stage_id"], item["run_name"]))
    return items


def build_batch_input_manifest(
    path: Path,
    *,
    source_items: list[dict[str, Any]],
    risk_pct: float,
    stop_long_atr_mult: float,
    stop_short_atr_mult: float,
    stop_atr_period: int,
) -> None:
    payload = {
        "generated_at_utc": utc_now_iso(),
        "stage": "06_segmented_risk_validation",
        "phase": "06B_pre_risk_pool_batch",
        "source_root": str(SOURCE_STAGE_ROOT),
        "source_run_count": len(source_items),
        "source_runs": [
            {"stage_id": item["stage_id"], "run_name": item["run_name"], "path": str(item["path"])}
            for item in source_items
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
        "segment_scheme_name": "validation_q3_holdout_3way",
    }
    write_json(path, payload)


def batch_paths(stage_root: Path, batch_id: str) -> dict[str, Path]:
    review_dir = stage_root / "03_reviews"
    slug = f"{batch_id}_pre_risk_pool_batch"
    return {
        "status_json": review_dir / f"{slug}_status.json",
        "status_md": review_dir / f"{slug}_status.md",
        "review_json": review_dir / f"{slug}_review.json",
        "review_md": review_dir / f"{slug}_review.md",
        "manifest": stage_root / "01_inputs" / f"{slug}_manifest.json",
    }


def make_target_names(batch_id: str, stage_id: str, ordinal: int) -> tuple[str, str]:
    stage_token = stage_id.lower()
    ordinal_token = f"{ordinal:02d}"
    run_name = f"{batch_id}_{stage_id}_{ordinal_token}"
    experiment_id = f"exp_{batch_id.lower()}_{stage_token}_{ordinal_token}"
    return run_name, experiment_id


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def run_tester(bundle_path: Path, split_name: str) -> None:
    cmd = [
        sys.executable,
        str(ROOT_DIR / "foundation" / "pipelines" / "run_mt5_bundle_tester.py"),
        "--bundle-json",
        str(bundle_path),
        "--split-name",
        split_name,
        "--enable-trading",
        "--skip-leaderboard-refresh",
    ]
    subprocess.run(cmd, cwd=ROOT_DIR, check=True)


def resolve_bundle_artifact_path(bundle_path: Path, artifact_path: str) -> Path:
    path = Path(artifact_path)
    if path.is_absolute():
        return path
    return (bundle_path.parent / path).resolve()


def reset_bundle_for_stage06(
    bundle: ExperimentBundle,
    *,
    experiment_id: str,
    batch_id: str,
    risk_pct: float,
    stop_long_atr_mult: float,
    stop_short_atr_mult: float,
    stop_atr_period: int,
) -> None:
    bundle.identity.experiment_id = experiment_id
    bundle.identity.stage_id = batch_id
    bundle.identity.stage_name = "segmented_risk_validation"
    bundle.identity.created_at_utc = utc_now_iso()
    bundle.identity.created_by = "python_orchestrator"
    bundle.identity.bundle_status = "ready"
    bundle.status_history = [
        StatusEvent(status="draft", changed_at_utc=utc_now_iso(), reason="stage06_overlay_initialized"),
        StatusEvent(status="ready", changed_at_utc=utc_now_iso(), reason="stage06_overlay_ready"),
    ]
    bundle.results = ResultsBlock(by_split={}, cross_split=CrossSplitResults(), report_refs=[])
    bundle.run_attempts = []
    bundle.runtime_snapshot.sizing_mode = "risk_pct"
    bundle.runtime_snapshot.risk_pct = risk_pct
    bundle.runtime_snapshot.capital_base = "balance"
    bundle.runtime_snapshot.stop_model = "atr"
    bundle.runtime_snapshot.stop_execution_mode = "broker_native"
    bundle.runtime_snapshot.stop_policy = "direction_split"
    bundle.runtime_snapshot.stop_atr_period = stop_atr_period
    bundle.runtime_snapshot.stop_atr_mult = 1.0
    bundle.runtime_snapshot.stop_long_atr_mult = stop_long_atr_mult
    bundle.runtime_snapshot.stop_short_atr_mult = stop_short_atr_mult
    bundle.compatibility.bundle_integrity_hash = sha256_text(bundle.canonical_core_json())


def write_overlay_manifest(
    path: Path,
    *,
    source_item: dict[str, Any],
    experiment_id: str,
    run_name: str,
    risk_pct: float,
    stop_long_atr_mult: float,
    stop_short_atr_mult: float,
    stop_atr_period: int,
    source_mode: str,
) -> None:
    write_json(
        path,
        {
            "generated_at_utc": utc_now_iso(),
            "phase": "06B_pre_risk_pool_batch",
            "run_name": run_name,
            "experiment_id": experiment_id,
            "source_stage_id": source_item["stage_id"],
            "source_run_name": source_item["run_name"],
            "source_mode": source_mode,
            "source_run_dir": str(source_item["path"]),
            "overlay": {
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
        },
    )


def prepare_overlay_bundle(
    *,
    source_item: dict[str, Any],
    run_dir: Path,
    run_name: str,
    experiment_id: str,
    batch_id: str,
    risk_pct: float,
    stop_long_atr_mult: float,
    stop_short_atr_mult: float,
    stop_atr_period: int,
    rebuild_bundle: bool,
) -> tuple[Path, str]:
    bundle_path = run_dir / "experiment_bundle.json"
    overlay_manifest_path = run_dir / "overlay_manifest.json"
    run_dir.mkdir(parents=True, exist_ok=True)

    if bundle_path.exists() and not rebuild_bundle:
        source_mode = "existing_stage06_bundle"
        write_overlay_manifest(
            overlay_manifest_path,
            source_item=source_item,
            experiment_id=experiment_id,
            run_name=run_name,
            risk_pct=risk_pct,
            stop_long_atr_mult=stop_long_atr_mult,
            stop_short_atr_mult=stop_short_atr_mult,
            stop_atr_period=stop_atr_period,
            source_mode=source_mode,
        )
        return bundle_path, source_mode

    source_bundle_path = source_item["path"] / "experiment_bundle.json"
    if source_item["has_bundle"]:
        bundle = ExperimentBundle.from_json(source_bundle_path.read_text(encoding="utf-8-sig"))
        for artifact in bundle.artifacts:
            artifact.path = str(resolve_bundle_artifact_path(source_bundle_path, artifact.path))
        reset_bundle_for_stage06(
            bundle,
            experiment_id=experiment_id,
            batch_id=batch_id,
            risk_pct=risk_pct,
            stop_long_atr_mult=stop_long_atr_mult,
            stop_short_atr_mult=stop_short_atr_mult,
            stop_atr_period=stop_atr_period,
        )
        bundle_path.write_text(bundle.to_json(indent=2), encoding="utf-8")
        source_mode = "source_bundle_clone"
        write_overlay_manifest(
            overlay_manifest_path,
            source_item=source_item,
            experiment_id=experiment_id,
            run_name=run_name,
            risk_pct=risk_pct,
            stop_long_atr_mult=stop_long_atr_mult,
            stop_short_atr_mult=stop_short_atr_mult,
            stop_atr_period=stop_atr_period,
            source_mode=source_mode,
        )
        return bundle_path, source_mode

    if source_item["has_config"] and source_item["has_model_joblib"] and source_item["has_rule_stack"]:
        source_mode = "source_export"
        export_args = SimpleNamespace(
            run_dir=str(source_item["path"]),
            experiment_id=experiment_id,
            stage_id=batch_id,
            output_dir=str(run_dir),
            stage_name="segmented_risk_validation",
            bundle_version="1.0.0",
            created_by="python_orchestrator",
            config_json=None,
            dataset_path=None,
            selection_json=None,
            logic_family=None,
            selection_key=None,
            rule_stack_json=str(source_item["path"] / "rule_stack.json"),
            smoke_split="test",
            smoke_row_index=0,
            max_hold_bars=5,
            sizing_mode="risk_pct",
            fixed_lot=0.1,
            risk_pct=risk_pct,
            capital_base="balance",
            stop_model="atr",
            stop_execution_mode="broker_native",
            stop_policy="direction_split",
            stop_atr_period=stop_atr_period,
            stop_atr_mult=1.0,
            stop_long_atr_mult=stop_long_atr_mult,
            stop_short_atr_mult=stop_short_atr_mult,
            stop_low_vol_threshold=None,
            stop_high_vol_threshold=None,
            stop_low_atr_mult=None,
            stop_mid_atr_mult=None,
            stop_high_atr_mult=None,
            build_bundle=True,
        )
        run_export_bundle_assets(export_args)
        write_overlay_manifest(
            overlay_manifest_path,
            source_item=source_item,
            experiment_id=experiment_id,
            run_name=run_name,
            risk_pct=risk_pct,
            stop_long_atr_mult=stop_long_atr_mult,
            stop_short_atr_mult=stop_short_atr_mult,
            stop_atr_period=stop_atr_period,
            source_mode=source_mode,
        )
        return bundle_path, source_mode

    raise FileNotFoundError(
        f"unsupported source layout: bundle={source_item['has_bundle']} config={source_item['has_config']} "
        f"model={source_item['has_model_joblib']} rule_stack={source_item['has_rule_stack']}"
    )


def completed_row_from_payload(source_item: dict[str, Any], target_run_name: str, payload: dict[str, Any]) -> dict[str, Any]:
    validation = payload["split_runs"]["validation"]
    test = payload["split_runs"]["test"]
    best_segment = payload["cross_segment_summary"]["best_segment"]
    worst_segment = payload["cross_segment_summary"]["worst_segment"]
    return {
        "source_stage_id": source_item["stage_id"],
        "source_run_name": source_item["run_name"],
        "target_run_name": target_run_name,
        "status": "completed",
        "source_mode": payload.get("source_mode"),
        "validation": {
            "return_pct": validation["headline"].get("return_pct"),
            "profit_factor": validation["headline"].get("profit_factor"),
            "trade_count": validation["headline"].get("trade_count"),
            "max_dd_pct": validation["headline"].get("max_dd_pct"),
            "ulcer_index": validation["risk"].get("ulcer_index"),
        },
        "test": {
            "return_pct": test["headline"].get("return_pct"),
            "profit_factor": test["headline"].get("profit_factor"),
            "trade_count": test["headline"].get("trade_count"),
            "max_dd_pct": test["headline"].get("max_dd_pct"),
            "ulcer_index": test["risk"].get("ulcer_index"),
        },
        "best_segment": best_segment,
        "worst_segment": worst_segment,
        "segmented_results_path": payload.get("segmented_results_path"),
        "review_md_path": payload.get("review_md_path"),
    }


def failure_row(source_item: dict[str, Any], target_run_name: str, error_text: str) -> dict[str, Any]:
    return {
        "source_stage_id": source_item["stage_id"],
        "source_run_name": source_item["run_name"],
        "target_run_name": target_run_name,
        "status": "failed",
        "source_mode": (
            "source_bundle_clone"
            if source_item.get("has_bundle")
            else "source_export"
            if source_item.get("has_config") and source_item.get("has_model_joblib") and source_item.get("has_rule_stack")
            else "unsupported"
        ),
        "error": error_text,
    }


def top_rows(rows: list[dict[str, Any]], key_path: tuple[str, str], limit: int = 10) -> list[dict[str, Any]]:
    completed = [row for row in rows if row.get("status") == "completed"]
    def key_fn(row: dict[str, Any]) -> float:
        group = row.get(key_path[0], {})
        value = group.get(key_path[1])
        return float(value) if value is not None else float("-inf")
    return sorted(completed, key=key_fn, reverse=True)[:limit]


def build_status_payload(
    *,
    batch_id: str,
    source_items: list[dict[str, Any]],
    results: list[dict[str, Any]],
    current_index: int,
    current_source: str | None,
    started_at_utc: str,
    finished: bool,
) -> dict[str, Any]:
    completed_count = sum(1 for row in results if row.get("status") == "completed")
    failed_count = sum(1 for row in results if row.get("status") == "failed")
    pending_count = len(source_items) - completed_count - failed_count
    return {
        "generated_at_utc": utc_now_iso(),
        "stage": "06_segmented_risk_validation",
        "phase": "06B_pre_risk_pool_batch",
        "batch_id": batch_id,
        "pid": os.getpid(),
        "status": "completed" if finished else "running",
        "started_at_utc": started_at_utc,
        "last_updated_at_utc": utc_now_iso(),
        "source_total": len(source_items),
        "completed_count": completed_count,
        "failed_count": failed_count,
        "pending_count": pending_count,
        "current_index": current_index,
        "current_source_run_name": current_source,
        "leaders": {
            "test_return_pct": top_rows(results, ("test", "return_pct"), limit=10),
            "validation_return_pct": top_rows(results, ("validation", "return_pct"), limit=10),
        },
        "results": results,
    }


def build_status_markdown(status_payload: dict[str, Any]) -> str:
    lines = [
        "# 06B Pre-Risk Pool Batch Status",
        "",
        f"- status: `{status_payload['status']}`",
        f"- batch_id: `{status_payload['batch_id']}`",
        f"- pid: `{status_payload['pid']}`",
        f"- started_at_utc: `{status_payload['started_at_utc']}`",
        f"- last_updated_at_utc: `{status_payload['last_updated_at_utc']}`",
        f"- source_total: `{status_payload['source_total']}`",
        f"- completed_count: `{status_payload['completed_count']}`",
        f"- failed_count: `{status_payload['failed_count']}`",
        f"- pending_count: `{status_payload['pending_count']}`",
    ]
    current_source = status_payload.get("current_source_run_name")
    if current_source:
        lines.append(f"- current_source_run_name: `{current_source}`")

    lines.extend(["", "## Top Holdout Returns", ""])
    for row in status_payload["leaders"]["test_return_pct"][:10]:
        test = row["test"]
        lines.append(
            f"- `{row['source_stage_id']}` `{row['source_run_name']}` -> `{row['target_run_name']}`: "
            f"return_pct `{format_metric(test.get('return_pct'), 3)}`, "
            f"PF `{format_metric(test.get('profit_factor'), 4)}`, "
            f"trades `{test.get('trade_count')}`"
        )
    lines.extend(["", "## Top Validation Returns", ""])
    for row in status_payload["leaders"]["validation_return_pct"][:10]:
        validation = row["validation"]
        lines.append(
            f"- `{row['source_stage_id']}` `{row['source_run_name']}` -> `{row['target_run_name']}`: "
            f"return_pct `{format_metric(validation.get('return_pct'), 3)}`, "
            f"PF `{format_metric(validation.get('profit_factor'), 4)}`, "
            f"trades `{validation.get('trade_count')}`"
        )
    lines.append("")
    return "\n".join(lines)


def build_final_review(status_payload: dict[str, Any]) -> dict[str, Any]:
    top_holdout = status_payload["leaders"]["test_return_pct"][:20]
    top_validation = status_payload["leaders"]["validation_return_pct"][:20]
    completed = [row for row in status_payload["results"] if row.get("status") == "completed"]
    best_holdout = top_holdout[0] if top_holdout else None
    best_validation = top_validation[0] if top_validation else None
    return {
        "generated_at_utc": utc_now_iso(),
        "stage": "06_segmented_risk_validation",
        "phase": "06B_pre_risk_pool_batch",
        "source_total": status_payload["source_total"],
        "completed_count": status_payload["completed_count"],
        "failed_count": status_payload["failed_count"],
        "best_holdout": best_holdout,
        "best_validation": best_validation,
        "top_holdout": top_holdout,
        "top_validation": top_validation,
        "failed_runs": [row for row in status_payload["results"] if row.get("status") == "failed"],
        "completed_runs": completed,
    }


def build_final_review_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# 06B Pre-Risk Pool Batch Review",
        "",
        f"- generated_at_utc: `{payload['generated_at_utc']}`",
        f"- source_total: `{payload['source_total']}`",
        f"- completed_count: `{payload['completed_count']}`",
        f"- failed_count: `{payload['failed_count']}`",
        "",
    ]
    best_holdout = payload.get("best_holdout")
    best_validation = payload.get("best_validation")
    if best_holdout:
        test = best_holdout["test"]
        lines.append(
            f"- best_holdout: `{best_holdout['source_stage_id']}` `{best_holdout['source_run_name']}` -> `{best_holdout['target_run_name']}`, "
            f"return_pct `{format_metric(test.get('return_pct'), 3)}`, PF `{format_metric(test.get('profit_factor'), 4)}`"
        )
    if best_validation:
        validation = best_validation["validation"]
        lines.append(
            f"- best_validation: `{best_validation['source_stage_id']}` `{best_validation['source_run_name']}` -> `{best_validation['target_run_name']}`, "
            f"return_pct `{format_metric(validation.get('return_pct'), 3)}`, PF `{format_metric(validation.get('profit_factor'), 4)}`"
        )
    lines.extend(["", "## Top Holdout", ""])
    for row in payload["top_holdout"][:20]:
        test = row["test"]
        lines.append(
            f"- `{row['source_stage_id']}` `{row['source_run_name']}` -> `{row['target_run_name']}`: "
            f"return_pct `{format_metric(test.get('return_pct'), 3)}`, "
            f"PF `{format_metric(test.get('profit_factor'), 4)}`, "
            f"trades `{test.get('trade_count')}`, "
            f"max_dd_pct `{format_metric(test.get('max_dd_pct'), 4)}`"
        )
    lines.extend(["", "## Top Validation", ""])
    for row in payload["top_validation"][:20]:
        validation = row["validation"]
        lines.append(
            f"- `{row['source_stage_id']}` `{row['source_run_name']}` -> `{row['target_run_name']}`: "
            f"return_pct `{format_metric(validation.get('return_pct'), 3)}`, "
            f"PF `{format_metric(validation.get('profit_factor'), 4)}`, "
            f"trades `{validation.get('trade_count')}`, "
            f"max_dd_pct `{format_metric(validation.get('max_dd_pct'), 4)}`"
        )
    if payload["failed_runs"]:
        lines.extend(["", "## Failed Runs", ""])
        for row in payload["failed_runs"]:
            lines.append(f"- `{row['source_stage_id']}` `{row['source_run_name']}`: `{row['error']}`")
    lines.append("")
    return "\n".join(lines)


def update_review_index(review_index_path: Path) -> None:
    lines = review_index_path.read_text(encoding="utf-8").splitlines() if review_index_path.exists() else []
    wanted = [
        "- `06A`: see `06A_segmented_risk_review.md`",
        "- `06B`: see `06B_pre_risk_pool_batch_status.md` and `06B_pre_risk_pool_batch_review.md`",
    ]
    if not lines:
        lines = ["# Review Index", "", "## Current Entries"]
    if "## Current Entries" not in lines:
        lines.extend(["", "## Current Entries"])
    existing = set(lines)
    for entry in wanted:
        if entry not in existing:
            lines.append(entry)
    write_text(review_index_path, "\n".join(lines).rstrip() + "\n")


def update_selection_status(
    selection_path: Path,
    *,
    status_payload: dict[str, Any],
    review_paths: dict[str, Path],
) -> None:
    best_holdout = status_payload["leaders"]["test_return_pct"][0] if status_payload["leaders"]["test_return_pct"] else None
    lines = [
        "# Selection Status",
        "",
        "- stage: `06_segmented_risk_validation`",
        f"- current phase active: `{status_payload['batch_id']}`",
        "- last completed reference run: `06A_dirsplit2pct_0001`",
        "- current mode: `sequential pre-risk pool overlay batch`",
        "- overlay config: `risk_pct=2.00, broker_native SL, direction_split(long=1.40, short=2.00), ATR14`",
        f"- batch progress: `completed={status_payload['completed_count']}/{status_payload['source_total']}`, `failed={status_payload['failed_count']}`, `pending={status_payload['pending_count']}`",
        f"- batch status file: `{review_paths['status_json'].name}`",
    ]
    if best_holdout:
        test = best_holdout["test"]
        lines.append(
            f"- current best completed holdout row: `{best_holdout['source_stage_id']}` -> `{best_holdout['target_run_name']}`, "
            f"`return_pct={format_metric(test.get('return_pct'), 3)}`, `PF={format_metric(test.get('profit_factor'), 4)}`"
        )
    lines.append("- next action: `let 06B finish, then rank the completed Stage 06 overlays by holdout and segment consistency`")
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
) -> dict[str, Any]:
    bundle = ExperimentBundle.from_json((run_dir / "experiment_bundle.json").read_text(encoding="utf-8-sig"))
    summaries = load_attempt_summaries(run_dir)
    if "validation" not in summaries or "test" not in summaries:
        raise FileNotFoundError(f"missing validation/test summaries in {run_dir}")

    segmented_results = {
        "validation": build_segment_results(bundle, "validation", summaries["validation"]),
        "test": build_segment_results(bundle, "test", summaries["test"]),
    }
    cross_segment_summary = build_cross_segment_summary(segmented_results)
    payload = {
        "generated_at_utc": utc_now_iso(),
        "stage": "06_segmented_risk_validation",
        "phase": "06B_pre_risk_pool_batch",
        "run_name": run_name,
        "experiment_id": experiment_id,
        "source_stage_id": source_item["stage_id"],
        "source_run_dir": str(source_item["path"]),
        "source_mode": "source_bundle_clone" if source_item["has_bundle"] else "source_export",
        "overlay": {
            "risk_pct": risk_pct,
            "stop_execution_mode": "broker_native",
            "stop_policy": "direction_split",
            "stop_long_atr_mult": stop_long_atr_mult,
            "stop_short_atr_mult": stop_short_atr_mult,
            "stop_atr_period": stop_atr_period,
        },
        "split_runs": {
            "validation": bundle.results.by_split["validation"].model_dump(),
            "test": bundle.results.by_split["test"].model_dump(),
        },
        "segmented_results": segmented_results,
        "cross_segment_summary": cross_segment_summary,
    }
    return payload


def build_run_markdown(payload: dict[str, Any]) -> str:
    validation = payload["split_runs"]["validation"]
    test = payload["split_runs"]["test"]
    lines = [
        f"# {payload['run_name']} Stage 06 Overlay Summary",
        "",
        f"- source_stage_id: `{payload['source_stage_id']}`",
        f"- source_run_dir: `{payload['source_run_dir']}`",
        f"- overlay: `risk_pct={format_metric(payload['overlay']['risk_pct'], 2)}, broker_native SL, direction_split(long={format_metric(payload['overlay']['stop_long_atr_mult'], 2)}, short={format_metric(payload['overlay']['stop_short_atr_mult'], 2)}), ATR{payload['overlay']['stop_atr_period']}`",
        "",
        "## Split Headline",
        "",
        f"- `validation`: return_pct `{format_metric(validation['headline'].get('return_pct'), 3)}`, PF `{format_metric(validation['headline'].get('profit_factor'), 4)}`, trades `{validation['headline'].get('trade_count')}`",
        f"- `test`: return_pct `{format_metric(test['headline'].get('return_pct'), 3)}`, PF `{format_metric(test['headline'].get('profit_factor'), 4)}`, trades `{test['headline'].get('trade_count')}`",
        "",
    ]
    best_segment = payload["cross_segment_summary"]["best_segment"]
    worst_segment = payload["cross_segment_summary"]["worst_segment"]
    lines.append(
        f"- best_segment: `{best_segment['split']}::{best_segment['segment']}`, return_pct `{format_metric(best_segment.get('return_pct'), 3)}`, PF `{format_metric(best_segment.get('profit_factor'), 4)}`"
    )
    lines.append(
        f"- worst_segment: `{worst_segment['split']}::{worst_segment['segment']}`, return_pct `{format_metric(worst_segment.get('return_pct'), 3)}`, PF `{format_metric(worst_segment.get('profit_factor'), 4)}`"
    )
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    args = build_parser().parse_args()

    stage_root = Path(args.stage_root).resolve()
    source_root = Path(args.source_root).resolve()
    review_paths = batch_paths(stage_root, args.batch_id)
    stage_paths = stage06_paths(stage_root)

    source_items = iter_pre_risk_runs(source_root)
    if args.max_runs:
        source_items = source_items[: args.max_runs]
    if not source_items:
        raise RuntimeError("no pre-risk Stage 05 runs found for 05A~05FZ")

    build_batch_input_manifest(
        review_paths["manifest"],
        source_items=source_items,
        risk_pct=args.risk_pct,
        stop_long_atr_mult=args.stop_long_atr_mult,
        stop_short_atr_mult=args.stop_short_atr_mult,
        stop_atr_period=args.stop_atr_period,
    )
    update_review_index(stage_paths["review_index"])

    duplicate_counter: dict[str, int] = defaultdict(int)
    started_at_utc = utc_now_iso()
    results: list[dict[str, Any]] = []

    for index, source_item in enumerate(source_items, start=1):
        status_payload = build_status_payload(
            batch_id=args.batch_id,
            source_items=source_items,
            results=results,
            current_index=index,
            current_source=source_item["run_name"],
            started_at_utc=started_at_utc,
            finished=False,
        )
        write_json(review_paths["status_json"], status_payload)
        write_text(review_paths["status_md"], build_status_markdown(status_payload))
        update_selection_status(stage_paths["selection"], status_payload=status_payload, review_paths=review_paths)

        duplicate_counter[source_item["stage_id"]] += 1
        run_name, experiment_id = make_target_names(args.batch_id, source_item["stage_id"], duplicate_counter[source_item["stage_id"]])
        run_dir = stage_root / "02_runs" / "active" / run_name
        segmented_json_path = run_dir / "segmented_results.json"
        segmented_md_path = run_dir / "segmented_results.md"

        if segmented_json_path.exists():
            existing_payload = json.loads(segmented_json_path.read_text(encoding="utf-8-sig"))
            existing_payload["segmented_results_path"] = str(segmented_json_path)
            existing_payload["review_md_path"] = str(segmented_md_path)
            results.append(completed_row_from_payload(source_item, run_name, existing_payload))
            continue

        try:
            bundle_path, source_mode = prepare_overlay_bundle(
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
            )
            payload["source_mode"] = source_mode
            payload["segmented_results_path"] = str(segmented_json_path)
            payload["review_md_path"] = str(segmented_md_path)
            write_json(segmented_json_path, payload)
            write_text(segmented_md_path, build_run_markdown(payload))
            results.append(completed_row_from_payload(source_item, run_name, payload))
            print(f"[done] {source_item['stage_id']} -> {run_name}")
        except Exception as exc:
            error_text = f"{type(exc).__name__}: {exc}"
            if not (
                isinstance(exc, FileNotFoundError)
                and str(exc).startswith("unsupported source layout:")
            ):
                traceback.print_exc()
            results.append(failure_row(source_item, run_name, error_text))
            print(f"[fail] {source_item['stage_id']} -> {run_name}: {error_text}")

    final_status = build_status_payload(
        batch_id=args.batch_id,
        source_items=source_items,
        results=results,
        current_index=len(source_items),
        current_source=None,
        started_at_utc=started_at_utc,
        finished=True,
    )
    final_review = build_final_review(final_status)

    write_json(review_paths["status_json"], final_status)
    write_text(review_paths["status_md"], build_status_markdown(final_status))
    write_json(review_paths["review_json"], final_review)
    write_text(review_paths["review_md"], build_final_review_markdown(final_review))
    update_selection_status(stage_paths["selection"], status_payload=final_status, review_paths=review_paths)

    print(f"[done] status_json={review_paths['status_json']}")
    print(f"[done] review_json={review_paths['review_json']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
