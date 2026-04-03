#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import sys
import traceback
from pathlib import Path
from typing import Any

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

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
from foundation.pipelines.run_stage06_pre_risk_pool_batch import (
    prepare_overlay_bundle,
    run_tester,
)
from foundation.pipelines.experiment_bundle_models import ExperimentBundle


STAGE06_ROOT = ROOT_DIR / "stages" / "06_segmented_risk_validation"
DEFAULT_SOURCE_RUN = (
    ROOT_DIR
    / "stages"
    / "05_optimization"
    / "02_runs"
    / "active"
    / "05ER_05dp_short_bias_margin_hold4_0001"
)
PROFILE_REGISTRY = {
    "practical": {
        "token": "R",
        "name": "practical",
        "label_ko": "실전형",
        "stop_long_atr_mult": 1.4,
        "stop_short_atr_mult": 2.0,
    },
    "aggressive": {
        "token": "A",
        "name": "aggressive",
        "label_ko": "공격형",
        "stop_long_atr_mult": 1.2,
        "stop_short_atr_mult": 1.8,
    },
    "conservative": {
        "token": "C",
        "name": "conservative",
        "label_ko": "보수형",
        "stop_long_atr_mult": 1.7,
        "stop_short_atr_mult": 2.4,
    },
}
DEFAULT_PROFILE_ORDER = ["practical", "aggressive", "conservative"]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run the Stage 06C risk ladder batch on the 05ER source with three stop profiles."
    )
    parser.add_argument("--stage-root", default=str(STAGE06_ROOT), help="Stage 06 root directory.")
    parser.add_argument(
        "--source-run-dir",
        default=str(DEFAULT_SOURCE_RUN),
        help="Source Stage 05 run providing the bundle/model artifacts.",
    )
    parser.add_argument("--batch-id", default="06C", help="Batch id used for Stage 06 artifacts.")
    parser.add_argument("--profiles", default="practical,aggressive,conservative", help="Comma-separated profile names.")
    parser.add_argument(
        "--risk-start",
        type=float,
        default=0.5,
        help="Risk ladder start percent. Used only when --risk-values is not supplied.",
    )
    parser.add_argument(
        "--risk-step",
        type=float,
        default=0.25,
        help="Risk ladder step percent. Used only when --risk-values is not supplied.",
    )
    parser.add_argument(
        "--risk-count",
        type=int,
        default=10,
        help="Number of ladder points. Default is 10 to honor the requested 10 x 3 batch.",
    )
    parser.add_argument(
        "--risk-values",
        help="Optional comma-separated explicit risk values. Overrides risk-start/step/count.",
    )
    parser.add_argument(
        "--requested-risk-end",
        type=float,
        default=3.0,
        help="Requested end of the range for documentation; effective ladder still follows the count.",
    )
    parser.add_argument("--stop-atr-period", type=int, default=14, help="ATR period.")
    parser.add_argument("--max-runs", type=int, help="Optional cap for smoke runs.")
    parser.add_argument("--rebuild-bundle", action="store_true", help="Force per-run bundle rebuild.")
    return parser


def parse_profiles(value: str) -> list[dict[str, Any]]:
    names = [item.strip().lower() for item in value.split(",") if item.strip()]
    if not names:
        raise ValueError("no profiles selected")
    profiles: list[dict[str, Any]] = []
    for name in names:
        if name not in PROFILE_REGISTRY:
            raise ValueError(f"unknown profile: {name}")
        profiles.append(dict(PROFILE_REGISTRY[name]))
    return profiles


def parse_risk_values(args: argparse.Namespace) -> list[float]:
    if args.risk_values:
        return [round(float(item.strip()), 4) for item in args.risk_values.split(",") if item.strip()]
    return [round(args.risk_start + (index * args.risk_step), 4) for index in range(args.risk_count)]


def build_source_item(source_run_dir: Path) -> dict[str, Any]:
    source_run_dir = source_run_dir.resolve()
    return {
        "stage_id": source_run_dir.name.split("_", 1)[0],
        "run_name": source_run_dir.name,
        "path": source_run_dir,
        "has_bundle": (source_run_dir / "experiment_bundle.json").exists(),
        "has_config": (source_run_dir / "config.json").exists(),
        "has_model_joblib": (source_run_dir / "model.joblib").exists(),
        "has_rule_stack": (source_run_dir / "rule_stack.json").exists(),
    }


def build_combos(profiles: list[dict[str, Any]], risk_values: list[float]) -> list[dict[str, Any]]:
    combos: list[dict[str, Any]] = []
    for profile in profiles:
        for risk_pct in risk_values:
            risk_token = int(round(risk_pct * 100))
            combos.append(
                {
                    "profile_token": profile["token"],
                    "profile_name": profile["name"],
                    "profile_label_ko": profile["label_ko"],
                    "risk_pct": risk_pct,
                    "risk_token": risk_token,
                    "stop_long_atr_mult": profile["stop_long_atr_mult"],
                    "stop_short_atr_mult": profile["stop_short_atr_mult"],
                    "run_name": f"06C_{profile['token']}{risk_token:03d}",
                    "experiment_id": f"exp_06c_{profile['name']}_{risk_token:03d}",
                }
            )
    return combos


def review_paths(stage_root: Path, batch_id: str) -> dict[str, Path]:
    review_dir = stage_root / "03_reviews"
    slug = f"{batch_id}_risk_profile_ladder"
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
    path: Path,
    *,
    source_item: dict[str, Any],
    profiles: list[dict[str, Any]],
    risk_values: list[float],
    requested_risk_end: float,
    stop_atr_period: int,
) -> None:
    payload = {
        "generated_at_utc": utc_now_iso(),
        "stage": "06_segmented_risk_validation",
        "phase": "06C_risk_profile_ladder_batch",
        "source_stage_id": source_item["stage_id"],
        "source_run_name": source_item["run_name"],
        "source_run_dir": str(source_item["path"]),
        "assumption": {
            "requested_range_pct": [risk_values[0], requested_risk_end],
            "effective_ladder_pct": risk_values,
            "reason": "user requested 10x3 so the effective 0.25-step ladder uses 10 points",
        },
        "profiles": [
            {
                "token": profile["token"],
                "name": profile["name"],
                "label_ko": profile["label_ko"],
                "stop_long_atr_mult": profile["stop_long_atr_mult"],
                "stop_short_atr_mult": profile["stop_short_atr_mult"],
            }
            for profile in profiles
        ],
        "overlay_defaults": {
            "sizing_mode": "risk_pct",
            "capital_base": "balance",
            "stop_model": "atr",
            "stop_execution_mode": "broker_native",
            "stop_policy": "direction_split",
            "stop_atr_period": stop_atr_period,
        },
    }
    write_json(path, payload)


def completed_row(combo: dict[str, Any], payload: dict[str, Any]) -> dict[str, Any]:
    validation = payload["split_runs"]["validation"]
    test = payload["split_runs"]["test"]
    return {
        "profile_token": combo["profile_token"],
        "profile_name": combo["profile_name"],
        "profile_label_ko": combo["profile_label_ko"],
        "risk_pct": combo["risk_pct"],
        "target_run_name": combo["run_name"],
        "status": "completed",
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
        "best_segment": payload["cross_segment_summary"]["best_segment"],
        "worst_segment": payload["cross_segment_summary"]["worst_segment"],
    }


def failure_row(combo: dict[str, Any], error_text: str) -> dict[str, Any]:
    return {
        "profile_token": combo["profile_token"],
        "profile_name": combo["profile_name"],
        "profile_label_ko": combo["profile_label_ko"],
        "risk_pct": combo["risk_pct"],
        "target_run_name": combo["run_name"],
        "status": "failed",
        "error": error_text,
    }


def sort_completed(rows: list[dict[str, Any]], group: str, key: str, limit: int = 10) -> list[dict[str, Any]]:
    completed = [row for row in rows if row.get("status") == "completed"]
    return sorted(
        completed,
        key=lambda row: float(row.get(group, {}).get(key) or float("-inf")),
        reverse=True,
    )[:limit]


def build_profile_summary(results: list[dict[str, Any]], profiles: list[dict[str, Any]]) -> dict[str, Any]:
    summary: dict[str, Any] = {}
    for profile in profiles:
        rows = [row for row in results if row.get("profile_name") == profile["name"]]
        completed = [row for row in rows if row.get("status") == "completed"]
        failed = [row for row in rows if row.get("status") == "failed"]
        best_holdout = sort_completed(completed, "test", "return_pct", limit=1)
        best_validation = sort_completed(completed, "validation", "return_pct", limit=1)
        summary[profile["name"]] = {
            "token": profile["token"],
            "label_ko": profile["label_ko"],
            "completed_count": len(completed),
            "failed_count": len(failed),
            "best_holdout": best_holdout[0] if best_holdout else None,
            "best_validation": best_validation[0] if best_validation else None,
        }
    return summary


def build_status_payload(
    *,
    batch_id: str,
    profiles: list[dict[str, Any]],
    risk_values: list[float],
    combos: list[dict[str, Any]],
    results: list[dict[str, Any]],
    started_at_utc: str,
    current_target_run_name: str | None,
    finished: bool,
) -> dict[str, Any]:
    completed_count = sum(1 for row in results if row.get("status") == "completed")
    failed_count = sum(1 for row in results if row.get("status") == "failed")
    pending_count = len(combos) - completed_count - failed_count
    return {
        "generated_at_utc": utc_now_iso(),
        "stage": "06_segmented_risk_validation",
        "phase": "06C_risk_profile_ladder_batch",
        "batch_id": batch_id,
        "pid": os.getpid(),
        "status": "completed" if finished else "running",
        "started_at_utc": started_at_utc,
        "last_updated_at_utc": utc_now_iso(),
        "combo_total": len(combos),
        "completed_count": completed_count,
        "failed_count": failed_count,
        "pending_count": pending_count,
        "risk_values": risk_values,
        "profiles": profiles,
        "current_target_run_name": current_target_run_name,
        "leaders": {
            "test_return_pct": sort_completed(results, "test", "return_pct", limit=10),
            "validation_return_pct": sort_completed(results, "validation", "return_pct", limit=10),
        },
        "profile_summary": build_profile_summary(results, profiles),
        "results": results,
    }


def build_status_markdown(status_payload: dict[str, Any]) -> str:
    lines = [
        "# 06C Risk Profile Ladder Status",
        "",
        f"- status: `{status_payload['status']}`",
        f"- batch_id: `{status_payload['batch_id']}`",
        f"- pid: `{status_payload['pid']}`",
        f"- started_at_utc: `{status_payload['started_at_utc']}`",
        f"- last_updated_at_utc: `{status_payload['last_updated_at_utc']}`",
        f"- combo_total: `{status_payload['combo_total']}`",
        f"- completed_count: `{status_payload['completed_count']}`",
        f"- failed_count: `{status_payload['failed_count']}`",
        f"- pending_count: `{status_payload['pending_count']}`",
    ]
    if status_payload.get("current_target_run_name"):
        lines.append(f"- current_target_run_name: `{status_payload['current_target_run_name']}`")
    lines.extend(["", "## Profile Leaders", ""])
    for profile_name, summary in status_payload["profile_summary"].items():
        best_holdout = summary.get("best_holdout")
        if best_holdout:
            lines.append(
                f"- `{summary['label_ko']}` `{profile_name}`: best holdout `{best_holdout['target_run_name']}`, "
                f"risk `{format_metric(best_holdout['risk_pct'], 2)}%`, "
                f"return_pct `{format_metric(best_holdout['test'].get('return_pct'), 3)}`, "
                f"PF `{format_metric(best_holdout['test'].get('profit_factor'), 4)}`"
            )
        else:
            lines.append(f"- `{summary['label_ko']}` `{profile_name}`: no completed runs yet")
    lines.extend(["", "## Top Holdout Returns", ""])
    for row in status_payload["leaders"]["test_return_pct"][:10]:
        lines.append(
            f"- `{row['target_run_name']}` `{row['profile_label_ko']}` "
            f"risk `{format_metric(row['risk_pct'], 2)}%`: "
            f"return_pct `{format_metric(row['test'].get('return_pct'), 3)}`, "
            f"PF `{format_metric(row['test'].get('profit_factor'), 4)}`, "
            f"DD `{format_metric(row['test'].get('max_dd_pct'), 4)}`"
        )
    lines.append("")
    return "\n".join(lines)


def build_final_review(status_payload: dict[str, Any]) -> dict[str, Any]:
    top_holdout = status_payload["leaders"]["test_return_pct"][:20]
    top_validation = status_payload["leaders"]["validation_return_pct"][:20]
    return {
        "generated_at_utc": utc_now_iso(),
        "stage": "06_segmented_risk_validation",
        "phase": "06C_risk_profile_ladder_batch",
        "combo_total": status_payload["combo_total"],
        "completed_count": status_payload["completed_count"],
        "failed_count": status_payload["failed_count"],
        "profiles": status_payload["profiles"],
        "risk_values": status_payload["risk_values"],
        "best_holdout": top_holdout[0] if top_holdout else None,
        "best_validation": top_validation[0] if top_validation else None,
        "top_holdout": top_holdout,
        "top_validation": top_validation,
        "profile_summary": status_payload["profile_summary"],
        "failed_runs": [row for row in status_payload["results"] if row.get("status") == "failed"],
        "completed_runs": [row for row in status_payload["results"] if row.get("status") == "completed"],
    }


def build_final_review_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# 06C Risk Profile Ladder Review",
        "",
        f"- generated_at_utc: `{payload['generated_at_utc']}`",
        f"- combo_total: `{payload['combo_total']}`",
        f"- completed_count: `{payload['completed_count']}`",
        f"- failed_count: `{payload['failed_count']}`",
        "",
        "## Profile Leaders",
        "",
    ]
    for profile_name, summary in payload["profile_summary"].items():
        best_holdout = summary.get("best_holdout")
        if best_holdout:
            lines.append(
                f"- `{summary['label_ko']}` `{profile_name}`: `{best_holdout['target_run_name']}`, "
                f"risk `{format_metric(best_holdout['risk_pct'], 2)}%`, "
                f"holdout return_pct `{format_metric(best_holdout['test'].get('return_pct'), 3)}`, "
                f"PF `{format_metric(best_holdout['test'].get('profit_factor'), 4)}`"
            )
    lines.extend(["", "## Top Holdout", ""])
    for row in payload["top_holdout"][:15]:
        lines.append(
            f"- `{row['target_run_name']}` `{row['profile_label_ko']}` "
            f"risk `{format_metric(row['risk_pct'], 2)}%`: "
            f"return_pct `{format_metric(row['test'].get('return_pct'), 3)}`, "
            f"PF `{format_metric(row['test'].get('profit_factor'), 4)}`, "
            f"trades `{row['test'].get('trade_count')}`, "
            f"max_dd_pct `{format_metric(row['test'].get('max_dd_pct'), 4)}`"
        )
    lines.extend(["", "## Top Validation", ""])
    for row in payload["top_validation"][:15]:
        lines.append(
            f"- `{row['target_run_name']}` `{row['profile_label_ko']}` "
            f"risk `{format_metric(row['risk_pct'], 2)}%`: "
            f"return_pct `{format_metric(row['validation'].get('return_pct'), 3)}`, "
            f"PF `{format_metric(row['validation'].get('profit_factor'), 4)}`, "
            f"trades `{row['validation'].get('trade_count')}`, "
            f"max_dd_pct `{format_metric(row['validation'].get('max_dd_pct'), 4)}`"
        )
    if payload["failed_runs"]:
        lines.extend(["", "## Failed Runs", ""])
        for row in payload["failed_runs"]:
            lines.append(
                f"- `{row['target_run_name']}` `{row['profile_label_ko']}` "
                f"risk `{format_metric(row['risk_pct'], 2)}%`: `{row['error']}`"
            )
    lines.append("")
    return "\n".join(lines)


def update_review_index(review_index_path: Path) -> None:
    lines = review_index_path.read_text(encoding="utf-8").splitlines() if review_index_path.exists() else []
    wanted = [
        "- `06A`: see `06A_segmented_risk_review.md`",
        "- `06B`: see `06B_pre_risk_pool_batch_status.md` and `06B_pre_risk_pool_batch_review.md`",
        "- `06C`: see `06C_risk_profile_ladder_status.md` and `06C_risk_profile_ladder_review.md`",
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
    risk_values: list[float],
) -> None:
    best_holdout = status_payload["leaders"]["test_return_pct"][0] if status_payload["leaders"]["test_return_pct"] else None
    lines = [
        "# Selection Status",
        "",
        "- stage: `06_segmented_risk_validation`",
        f"- current phase active: `{status_payload['batch_id']}`",
        "- last completed reference batch: `06B_pre_risk_pool_batch`",
        "- current mode: `05ER source risk ladder with three direction-split profiles`",
        f"- ladder assumption: `requested 0.50~3.00 step 0.25, effective 10-point ladder {', '.join(f'{value:.2f}' for value in risk_values)}`",
        "- profile presets: `공격형 long=1.20 short=1.80 | 실전형 long=1.40 short=2.00 | 보수형 long=1.70 short=2.40`",
        f"- batch progress: `completed={status_payload['completed_count']}/{status_payload['combo_total']}`, `failed={status_payload['failed_count']}`, `pending={status_payload['pending_count']}`",
        "- batch status file: `06C_risk_profile_ladder_status.json`",
    ]
    if best_holdout:
        lines.append(
            f"- current best completed holdout row: `{best_holdout['target_run_name']}` `{best_holdout['profile_label_ko']}`, "
            f"`risk_pct={format_metric(best_holdout['risk_pct'], 2)}%`, "
            f"`return_pct={format_metric(best_holdout['test'].get('return_pct'), 3)}`, "
            f"`PF={format_metric(best_holdout['test'].get('profit_factor'), 4)}`"
        )
    lines.append("- next action: `let 06C finish, then shortlist the top risk/profile combinations by holdout and segment consistency`")
    write_text(selection_path, "\n".join(lines) + "\n")


def create_single_run_payload(
    *,
    source_item: dict[str, Any],
    combo: dict[str, Any],
    run_dir: Path,
) -> dict[str, Any]:
    bundle = ExperimentBundle.from_json((run_dir / "experiment_bundle.json").read_text(encoding="utf-8-sig"))
    summaries = load_attempt_summaries(run_dir)
    if "validation" not in summaries or "test" not in summaries:
        raise FileNotFoundError(f"missing validation/test summaries in {run_dir}")

    segmented_results = {
        "validation": build_segment_results(bundle, "validation", summaries["validation"]),
        "test": build_segment_results(bundle, "test", summaries["test"]),
    }
    return {
        "generated_at_utc": utc_now_iso(),
        "stage": "06_segmented_risk_validation",
        "phase": "06C_risk_profile_ladder_batch",
        "run_name": combo["run_name"],
        "experiment_id": combo["experiment_id"],
        "source_stage_id": source_item["stage_id"],
        "source_run_dir": str(source_item["path"]),
        "profile": {
            "token": combo["profile_token"],
            "name": combo["profile_name"],
            "label_ko": combo["profile_label_ko"],
        },
        "overlay": {
            "risk_pct": combo["risk_pct"],
            "stop_execution_mode": "broker_native",
            "stop_policy": "direction_split",
            "stop_long_atr_mult": combo["stop_long_atr_mult"],
            "stop_short_atr_mult": combo["stop_short_atr_mult"],
            "stop_atr_period": 14,
        },
        "split_runs": {
            "validation": bundle.results.by_split["validation"].model_dump(),
            "test": bundle.results.by_split["test"].model_dump(),
        },
        "segmented_results": segmented_results,
        "cross_segment_summary": build_cross_segment_summary(segmented_results),
    }


def build_run_markdown(payload: dict[str, Any]) -> str:
    validation = payload["split_runs"]["validation"]
    test = payload["split_runs"]["test"]
    best_segment = payload["cross_segment_summary"]["best_segment"]
    worst_segment = payload["cross_segment_summary"]["worst_segment"]
    return "\n".join(
        [
            f"# {payload['run_name']} Stage 06C Overlay Summary",
            "",
            f"- source_stage_id: `{payload['source_stage_id']}`",
            f"- profile: `{payload['profile']['label_ko']}` `{payload['profile']['name']}`",
            f"- overlay: `risk_pct={format_metric(payload['overlay']['risk_pct'], 2)}%, broker_native SL, direction_split(long={format_metric(payload['overlay']['stop_long_atr_mult'], 2)}, short={format_metric(payload['overlay']['stop_short_atr_mult'], 2)}), ATR{payload['overlay']['stop_atr_period']}`",
            "",
            "## Split Headline",
            "",
            f"- `validation`: return_pct `{format_metric(validation['headline'].get('return_pct'), 3)}`, PF `{format_metric(validation['headline'].get('profit_factor'), 4)}`, trades `{validation['headline'].get('trade_count')}`",
            f"- `test`: return_pct `{format_metric(test['headline'].get('return_pct'), 3)}`, PF `{format_metric(test['headline'].get('profit_factor'), 4)}`, trades `{test['headline'].get('trade_count')}`",
            "",
            f"- best_segment: `{best_segment['split']}::{best_segment['segment']}`, return_pct `{format_metric(best_segment.get('return_pct'), 3)}`, PF `{format_metric(best_segment.get('profit_factor'), 4)}`",
            f"- worst_segment: `{worst_segment['split']}::{worst_segment['segment']}`, return_pct `{format_metric(worst_segment.get('return_pct'), 3)}`, PF `{format_metric(worst_segment.get('profit_factor'), 4)}`",
            "",
        ]
    )


def main() -> int:
    args = build_parser().parse_args()

    stage_root = Path(args.stage_root).resolve()
    source_item = build_source_item(Path(args.source_run_dir))
    if not source_item["has_bundle"]:
        raise FileNotFoundError(f"source bundle not found: {source_item['path']}")

    profiles = parse_profiles(args.profiles)
    risk_values = parse_risk_values(args)
    combos = build_combos(profiles, risk_values)
    if args.max_runs:
        combos = combos[: args.max_runs]
    if not combos:
        raise RuntimeError("no risk/profile combos selected")

    paths = review_paths(stage_root, args.batch_id)
    stage_paths = stage06_paths(stage_root)
    build_manifest(
        paths["manifest"],
        source_item=source_item,
        profiles=profiles,
        risk_values=risk_values,
        requested_risk_end=args.requested_risk_end,
        stop_atr_period=args.stop_atr_period,
    )
    update_review_index(stage_paths["review_index"])

    started_at_utc = utc_now_iso()
    results: list[dict[str, Any]] = []

    for combo in combos:
        status_payload = build_status_payload(
            batch_id=args.batch_id,
            profiles=profiles,
            risk_values=risk_values,
            combos=combos,
            results=results,
            started_at_utc=started_at_utc,
            current_target_run_name=combo["run_name"],
            finished=False,
        )
        write_json(paths["status_json"], status_payload)
        write_text(paths["status_md"], build_status_markdown(status_payload))
        update_selection_status(stage_paths["selection"], status_payload=status_payload, risk_values=risk_values)

        run_dir = stage_root / "02_runs" / "active" / combo["run_name"]
        segmented_json_path = run_dir / "segmented_results.json"
        segmented_md_path = run_dir / "segmented_results.md"

        if segmented_json_path.exists():
            existing_payload = json.loads(segmented_json_path.read_text(encoding="utf-8-sig"))
            results.append(completed_row(combo, existing_payload))
            continue

        try:
            bundle_path, _ = prepare_overlay_bundle(
                source_item=source_item,
                run_dir=run_dir,
                run_name=combo["run_name"],
                experiment_id=combo["experiment_id"],
                batch_id=args.batch_id,
                risk_pct=combo["risk_pct"],
                stop_long_atr_mult=combo["stop_long_atr_mult"],
                stop_short_atr_mult=combo["stop_short_atr_mult"],
                stop_atr_period=args.stop_atr_period,
                rebuild_bundle=args.rebuild_bundle,
            )
            run_tester(bundle_path, "validation")
            run_tester(bundle_path, "test")

            payload = create_single_run_payload(source_item=source_item, combo=combo, run_dir=run_dir)
            write_json(segmented_json_path, payload)
            write_text(segmented_md_path, build_run_markdown(payload))
            results.append(completed_row(combo, payload))
            print(f"[done] {combo['run_name']}")
        except Exception as exc:
            error_text = f"{type(exc).__name__}: {exc}"
            traceback.print_exc()
            results.append(failure_row(combo, error_text))
            print(f"[fail] {combo['run_name']}: {error_text}")

    final_status = build_status_payload(
        batch_id=args.batch_id,
        profiles=profiles,
        risk_values=risk_values,
        combos=combos,
        results=results,
        started_at_utc=started_at_utc,
        current_target_run_name=None,
        finished=True,
    )
    final_review = build_final_review(final_status)

    write_json(paths["status_json"], final_status)
    write_text(paths["status_md"], build_status_markdown(final_status))
    write_json(paths["review_json"], final_review)
    write_text(paths["review_md"], build_final_review_markdown(final_review))
    update_selection_status(stage_paths["selection"], status_payload=final_status, risk_values=risk_values)

    print(f"[done] status_json={paths['status_json']}")
    print(f"[done] review_json={paths['review_json']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
