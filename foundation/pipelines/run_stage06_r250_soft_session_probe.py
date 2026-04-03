#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from foundation.pipelines.experiment_bundle_models import ExperimentBundle
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
from foundation.pipelines.run_stage06_pre_risk_pool_batch import prepare_overlay_bundle, run_tester


STAGE06_ROOT = ROOT_DIR / "stages" / "06_segmented_risk_validation"
DEFAULT_SOURCE_RUN = STAGE06_ROOT / "02_runs" / "active" / "06C_R250"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run one soft session-decay probe on top of the 06C_R250 practical 2.5% overlay."
    )
    parser.add_argument("--stage-root", default=str(STAGE06_ROOT), help="Stage 06 root directory.")
    parser.add_argument("--source-run-dir", default=str(DEFAULT_SOURCE_RUN), help="Source Stage 06 run directory.")
    parser.add_argument("--run-name", default="06D_R250_SD01", help="Target run folder name.")
    parser.add_argument("--experiment-id", default="exp_06d_r250_softsession_v1", help="Experiment id.")
    parser.add_argument("--stage-id", default="06D", help="Stage id.")
    parser.add_argument("--review-basename", default="06D_r250_soft_session_review", help="Review basename.")
    parser.add_argument("--risk-pct", type=float, default=2.5, help="Base risk percent.")
    parser.add_argument("--stop-atr-period", type=int, default=14, help="ATR period.")
    parser.add_argument("--stop-long-atr-mult", type=float, default=1.4, help="Long ATR multiplier.")
    parser.add_argument("--stop-short-atr-mult", type=float, default=2.0, help="Short ATR multiplier.")
    parser.add_argument("--monday-risk-mult", type=float, default=0.75, help="Monday risk multiplier.")
    parser.add_argument("--ny-postcash-risk-mult", type=float, default=0.70, help="New York post-cash risk multiplier.")
    parser.add_argument("--rebuild-bundle", action="store_true", help="Force bundle rebuild.")
    return parser


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


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def ensure_bundle(
    *,
    source_item: dict[str, Any],
    run_dir: Path,
    args: argparse.Namespace,
) -> Path:
    bundle_path, _ = prepare_overlay_bundle(
        source_item=source_item,
        run_dir=run_dir,
        run_name=args.run_name,
        experiment_id=args.experiment_id,
        batch_id=args.stage_id,
        risk_pct=args.risk_pct,
        stop_long_atr_mult=args.stop_long_atr_mult,
        stop_short_atr_mult=args.stop_short_atr_mult,
        stop_atr_period=args.stop_atr_period,
        rebuild_bundle=args.rebuild_bundle,
    )

    bundle = ExperimentBundle.from_json(bundle_path.read_text(encoding="utf-8-sig"))
    bundle.runtime_snapshot.extra["monday_risk_pct_mult"] = args.monday_risk_mult
    bundle.runtime_snapshot.extra["ny_postcash_risk_pct_mult"] = args.ny_postcash_risk_mult
    bundle.runtime_snapshot.extra["session_risk_overlay"] = "soft_decay"
    bundle.compatibility.bundle_integrity_hash = sha256_text(bundle.canonical_core_json())
    bundle_path.write_text(bundle.to_json(indent=2), encoding="utf-8")

    overlay_manifest = {
        "generated_at_utc": utc_now_iso(),
        "run_name": args.run_name,
        "experiment_id": args.experiment_id,
        "source_run_dir": str(source_item["path"]),
        "source_stage_id": source_item["stage_id"],
        "overlay": {
            "risk_pct": args.risk_pct,
            "stop_policy": "direction_split",
            "stop_long_atr_mult": args.stop_long_atr_mult,
            "stop_short_atr_mult": args.stop_short_atr_mult,
            "monday_risk_pct_mult": args.monday_risk_mult,
            "ny_postcash_risk_pct_mult": args.ny_postcash_risk_mult,
        },
    }
    write_json(run_dir / "overlay_manifest.json", overlay_manifest)
    return bundle_path


def build_payload(
    *,
    run_dir: Path,
    source_item: dict[str, Any],
    args: argparse.Namespace,
) -> dict[str, Any]:
    bundle = ExperimentBundle.from_json((run_dir / "experiment_bundle.json").read_text(encoding="utf-8-sig"))
    summaries = load_attempt_summaries(run_dir)
    if "validation" not in summaries or "test" not in summaries:
        raise FileNotFoundError(f"missing validation/test summaries in {run_dir}")

    segmented_results = {
        "validation": build_segment_results(bundle, "validation", summaries["validation"]),
        "test": build_segment_results(bundle, "test", summaries["test"]),
    }
    source_segmented_path = source_item["path"] / "segmented_results.json"
    source_segmented = json.loads(source_segmented_path.read_text(encoding="utf-8-sig"))

    comparison: dict[str, Any] = {}
    for split_name in ("validation", "test"):
        base_headline = source_segmented["split_runs"][split_name]["headline"]
        base_risk = source_segmented["split_runs"][split_name]["risk"]
        new_headline = bundle.results.by_split[split_name].headline.model_dump()
        new_risk = bundle.results.by_split[split_name].risk.model_dump()
        comparison[split_name] = {
            "base_run_name": source_segmented["run_name"],
            "base_return_pct": base_headline.get("return_pct"),
            "base_profit_factor": base_headline.get("profit_factor"),
            "base_max_dd_pct": base_headline.get("max_dd_pct"),
            "base_ulcer_index": base_risk.get("ulcer_index"),
            "return_pct_delta": (
                (new_headline.get("return_pct") or 0.0) - (base_headline.get("return_pct") or 0.0)
            ),
            "profit_factor_delta": (
                (new_headline.get("profit_factor") or 0.0) - (base_headline.get("profit_factor") or 0.0)
            ),
            "max_dd_pct_delta": (
                (new_headline.get("max_dd_pct") or 0.0) - (base_headline.get("max_dd_pct") or 0.0)
            ),
            "ulcer_index_delta": (
                (new_risk.get("ulcer_index") or 0.0) - (base_risk.get("ulcer_index") or 0.0)
            ),
        }

    return {
        "generated_at_utc": utc_now_iso(),
        "stage": "06_segmented_risk_validation",
        "phase": "06D_r250_soft_session_probe",
        "run_name": args.run_name,
        "experiment_id": args.experiment_id,
        "source_stage_id": source_item["stage_id"],
        "source_run_name": source_item["run_name"],
        "source_run_dir": str(source_item["path"]),
        "overlay": {
            "risk_pct": args.risk_pct,
            "stop_execution_mode": "broker_native",
            "stop_policy": "direction_split",
            "stop_long_atr_mult": args.stop_long_atr_mult,
            "stop_short_atr_mult": args.stop_short_atr_mult,
            "stop_atr_period": args.stop_atr_period,
            "monday_risk_pct_mult": args.monday_risk_mult,
            "ny_postcash_risk_pct_mult": args.ny_postcash_risk_mult,
        },
        "split_runs": {
            "validation": bundle.results.by_split["validation"].model_dump(),
            "test": bundle.results.by_split["test"].model_dump(),
        },
        "segmented_results": segmented_results,
        "cross_segment_summary": build_cross_segment_summary(segmented_results),
        "comparison_to_source": comparison,
    }


def build_review_markdown(payload: dict[str, Any]) -> str:
    validation = payload["split_runs"]["validation"]["headline"]
    test = payload["split_runs"]["test"]["headline"]
    cmp_validation = payload["comparison_to_source"]["validation"]
    cmp_test = payload["comparison_to_source"]["test"]
    lines = [
        "# 06D R250 Soft Session Probe",
        "",
        f"- source_run: `{payload['source_run_name']}`",
        f"- source_run_dir: `{payload['source_run_dir']}`",
        f"- overlay: `risk_pct={format_metric(payload['overlay']['risk_pct'], 2)}%, direction_split(long={format_metric(payload['overlay']['stop_long_atr_mult'], 2)}, short={format_metric(payload['overlay']['stop_short_atr_mult'], 2)}), monday_mult={format_metric(payload['overlay']['monday_risk_pct_mult'], 2)}, ny_postcash_mult={format_metric(payload['overlay']['ny_postcash_risk_pct_mult'], 2)}`",
        "",
        "## Headline",
        "",
        f"- validation: `return_pct={format_metric(validation.get('return_pct'), 3)}`, `PF={format_metric(validation.get('profit_factor'), 4)}`, `trades={validation.get('trade_count')}`, `max_dd_pct={format_metric(validation.get('max_dd_pct'), 4)}`",
        f"- holdout: `return_pct={format_metric(test.get('return_pct'), 3)}`, `PF={format_metric(test.get('profit_factor'), 4)}`, `trades={test.get('trade_count')}`, `max_dd_pct={format_metric(test.get('max_dd_pct'), 4)}`",
        "",
        "## Delta Vs 06C_R250",
        "",
        f"- validation delta: `return_pct={format_metric(cmp_validation['return_pct_delta'], 3)}`, `PF={format_metric(cmp_validation['profit_factor_delta'], 4)}`, `max_dd_pct={format_metric(cmp_validation['max_dd_pct_delta'], 4)}`, `ulcer={format_metric(cmp_validation['ulcer_index_delta'], 4)}`",
        f"- holdout delta: `return_pct={format_metric(cmp_test['return_pct_delta'], 3)}`, `PF={format_metric(cmp_test['profit_factor_delta'], 4)}`, `max_dd_pct={format_metric(cmp_test['max_dd_pct_delta'], 4)}`, `ulcer={format_metric(cmp_test['ulcer_index_delta'], 4)}`",
        "",
    ]
    return "\n".join(lines)


def update_review_index(review_index_path: Path, review_name: str) -> None:
    lines = review_index_path.read_text(encoding="utf-8").splitlines() if review_index_path.exists() else []
    if not lines:
        lines = ["# Review Index", "", "## Current Entries"]
    if "## Current Entries" not in lines:
        lines.extend(["", "## Current Entries"])
    entry = f"- `06D`: see `{review_name}`"
    if entry not in lines:
        lines.append(entry)
    write_text(review_index_path, "\n".join(lines).rstrip() + "\n")


def update_selection_status(selection_path: Path, payload: dict[str, Any]) -> None:
    test = payload["split_runs"]["test"]["headline"]
    cmp_test = payload["comparison_to_source"]["test"]
    lines = [
        "# Selection Status",
        "",
        "- stage: `06_segmented_risk_validation`",
        "- current phase active: `06D`",
        "- reference batch: `06C_risk_profile_ladder_batch`",
        f"- current probe run: `{payload['run_name']}` from `{payload['source_run_name']}`",
        f"- overlay config: `risk_pct={format_metric(payload['overlay']['risk_pct'], 2)}%, monday_mult={format_metric(payload['overlay']['monday_risk_pct_mult'], 2)}, ny_postcash_mult={format_metric(payload['overlay']['ny_postcash_risk_pct_mult'], 2)}, direction_split(long={format_metric(payload['overlay']['stop_long_atr_mult'], 2)}, short={format_metric(payload['overlay']['stop_short_atr_mult'], 2)})`",
        f"- holdout headline: `return_pct={format_metric(test.get('return_pct'), 3)}`, `PF={format_metric(test.get('profit_factor'), 4)}`, `trades={test.get('trade_count')}`, `max_dd_pct={format_metric(test.get('max_dd_pct'), 4)}`",
        f"- vs source 06C_R250: `return_pct_delta={format_metric(cmp_test['return_pct_delta'], 3)}`, `PF_delta={format_metric(cmp_test['profit_factor_delta'], 4)}`, `max_dd_pct_delta={format_metric(cmp_test['max_dd_pct_delta'], 4)}`, `ulcer_delta={format_metric(cmp_test['ulcer_index_delta'], 4)}`",
        "- next action: `decide whether soft session decay should be explored further or discarded against the plain 06C_R250 baseline`",
    ]
    write_text(selection_path, "\n".join(lines) + "\n")


def main() -> int:
    args = build_parser().parse_args()

    stage_root = Path(args.stage_root).resolve()
    source_item = build_source_item(Path(args.source_run_dir))
    if not source_item["has_bundle"]:
        raise FileNotFoundError(f"source bundle not found: {source_item['path']}")

    run_dir = stage_root / "02_runs" / "active" / args.run_name
    bundle_path = ensure_bundle(source_item=source_item, run_dir=run_dir, args=args)
    run_tester(bundle_path, "validation")
    run_tester(bundle_path, "test")

    payload = build_payload(run_dir=run_dir, source_item=source_item, args=args)
    segmented_results_path = run_dir / "segmented_results.json"
    review_md_path = stage_root / "03_reviews" / f"{args.review_basename}.md"
    review_json_path = stage_root / "03_reviews" / f"{args.review_basename}.json"

    write_json(segmented_results_path, payload)
    write_text(run_dir / "segmented_results.md", build_review_markdown(payload))
    write_json(review_json_path, payload)
    write_text(review_md_path, build_review_markdown(payload))

    stage_paths = stage06_paths(stage_root)
    update_review_index(stage_paths["review_index"], review_md_path.name)
    update_selection_status(stage_paths["selection"], payload)

    print(f"[done] segmented_results={segmented_results_path}")
    print(f"[done] review={review_md_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
