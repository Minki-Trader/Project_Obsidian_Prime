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
DEFAULT_REFERENCE_RUN = STAGE06_ROOT / "02_runs" / "active" / "06D_R250_SD01"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run a small suite of session-aware overlays on top of the 06C_R250 practical 2.5% reference."
    )
    parser.add_argument("--stage-root", default=str(STAGE06_ROOT), help="Stage 06 root directory.")
    parser.add_argument("--source-run-dir", default=str(DEFAULT_SOURCE_RUN), help="Source Stage 06 run directory.")
    parser.add_argument(
        "--reference-run-dir",
        default=str(DEFAULT_REFERENCE_RUN),
        help="Optional reference run directory used for comparison in the review.",
    )
    parser.add_argument("--batch-id", default="06E", help="Batch id used for run naming.")
    parser.add_argument("--risk-pct", type=float, default=2.5, help="Base risk percent.")
    parser.add_argument("--stop-atr-period", type=int, default=14, help="ATR period.")
    parser.add_argument("--stop-long-atr-mult", type=float, default=1.4, help="Long ATR multiplier.")
    parser.add_argument("--stop-short-atr-mult", type=float, default=2.0, help="Short ATR multiplier.")
    parser.add_argument(
        "--review-basename",
        default="06E_r250_overlay_suite_review",
        help="Output review basename.",
    )
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


def suite_variants(batch_id: str) -> list[dict[str, Any]]:
    return [
        {
            "token": "LP01",
            "run_name": f"{batch_id}_R250_LP01",
            "experiment_id": f"exp_{batch_id.lower()}_r250_lp01_v1",
            "label": "local_probe_a",
            "description": "Softer Monday, tighter post-cash decay.",
            "runtime_extra": {
                "monday_risk_pct_mult": 0.80,
                "ny_postcash_risk_pct_mult": 0.65,
            },
        },
        {
            "token": "LP02",
            "run_name": f"{batch_id}_R250_LP02",
            "experiment_id": f"exp_{batch_id.lower()}_r250_lp02_v1",
            "label": "local_probe_b",
            "description": "Stronger Monday and post-cash decay.",
            "runtime_extra": {
                "monday_risk_pct_mult": 0.70,
                "ny_postcash_risk_pct_mult": 0.65,
            },
        },
        {
            "token": "MD01",
            "run_name": f"{batch_id}_R250_MD01",
            "experiment_id": f"exp_{batch_id.lower()}_r250_md01_v1",
            "label": "monday_direction_split",
            "description": "Decay Monday longs only while leaving Monday shorts intact.",
            "runtime_extra": {
                "monday_risk_pct_mult": 1.0,
                "monday_long_risk_pct_mult": 0.60,
                "monday_short_risk_pct_mult": 1.0,
                "ny_postcash_risk_pct_mult": 0.70,
            },
        },
        {
            "token": "PH01",
            "run_name": f"{batch_id}_R250_PH01",
            "experiment_id": f"exp_{batch_id.lower()}_r250_ph01_v1",
            "label": "postcash_hold_cut",
            "description": "Keep the 06D soft decay and shorten post-cash hold time.",
            "runtime_extra": {
                "monday_risk_pct_mult": 0.75,
                "ny_postcash_risk_pct_mult": 0.70,
                "ny_postcash_hold_cap_bars": 3,
            },
        },
        {
            "token": "CT01",
            "run_name": f"{batch_id}_R250_CT01",
            "experiment_id": f"exp_{batch_id.lower()}_r250_ct01_v1",
            "label": "clock_taper",
            "description": "Use a gradual NY-local taper instead of one hard post-cash multiplier.",
            "runtime_extra": {
                "monday_risk_pct_mult": 0.75,
                "ny_postcash_risk_pct_mult": 1.0,
                "ny_clock_taper_start_minute": 930,
                "ny_clock_taper_mid_minute": 960,
                "ny_clock_taper_late_minute": 1080,
                "ny_clock_taper_start_mult": 0.90,
                "ny_clock_taper_mid_mult": 0.75,
                "ny_clock_taper_late_mult": 0.60,
            },
        },
    ]


def ensure_bundle(
    *,
    source_item: dict[str, Any],
    run_dir: Path,
    variant: dict[str, Any],
    args: argparse.Namespace,
) -> Path:
    bundle_path, _ = prepare_overlay_bundle(
        source_item=source_item,
        run_dir=run_dir,
        run_name=variant["run_name"],
        experiment_id=variant["experiment_id"],
        batch_id=args.batch_id,
        risk_pct=args.risk_pct,
        stop_long_atr_mult=args.stop_long_atr_mult,
        stop_short_atr_mult=args.stop_short_atr_mult,
        stop_atr_period=args.stop_atr_period,
        rebuild_bundle=args.rebuild_bundle,
    )

    bundle = ExperimentBundle.from_json(bundle_path.read_text(encoding="utf-8-sig"))
    for key, value in variant["runtime_extra"].items():
        bundle.runtime_snapshot.extra[key] = value
    bundle.runtime_snapshot.extra["session_overlay_label"] = variant["label"]
    bundle.compatibility.bundle_integrity_hash = sha256_text(bundle.canonical_core_json())
    bundle_path.write_text(bundle.to_json(indent=2), encoding="utf-8")

    write_json(
        run_dir / "overlay_manifest.json",
        {
            "generated_at_utc": utc_now_iso(),
            "batch_id": args.batch_id,
            "run_name": variant["run_name"],
            "experiment_id": variant["experiment_id"],
            "source_run_dir": str(source_item["path"]),
            "source_run_name": source_item["run_name"],
            "label": variant["label"],
            "description": variant["description"],
            "overlay": {
                "risk_pct": args.risk_pct,
                "stop_policy": "direction_split",
                "stop_long_atr_mult": args.stop_long_atr_mult,
                "stop_short_atr_mult": args.stop_short_atr_mult,
                "stop_atr_period": args.stop_atr_period,
                **variant["runtime_extra"],
            },
        },
    )
    return bundle_path


def split_delta(
    base_segmented: dict[str, Any],
    payload: dict[str, Any],
) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for split_name in ("validation", "test"):
        base_headline = base_segmented["split_runs"][split_name]["headline"]
        base_risk = base_segmented["split_runs"][split_name]["risk"]
        new_headline = payload["split_runs"][split_name]
        new_risk = payload["split_runs"][split_name]
        out[split_name] = {
            "base_run_name": base_segmented["run_name"],
            "base_return_pct": base_headline.get("return_pct"),
            "base_profit_factor": base_headline.get("profit_factor"),
            "base_max_dd_pct": base_headline.get("max_dd_pct"),
            "base_ulcer_index": base_risk.get("ulcer_index"),
            "return_pct_delta": (new_headline["headline"].get("return_pct") or 0.0)
            - (base_headline.get("return_pct") or 0.0),
            "profit_factor_delta": (new_headline["headline"].get("profit_factor") or 0.0)
            - (base_headline.get("profit_factor") or 0.0),
            "max_dd_pct_delta": (new_headline["headline"].get("max_dd_pct") or 0.0)
            - (base_headline.get("max_dd_pct") or 0.0),
            "ulcer_index_delta": (new_risk["risk"].get("ulcer_index") or 0.0)
            - (base_risk.get("ulcer_index") or 0.0),
        }
    return out


def build_payload(
    *,
    run_dir: Path,
    source_item: dict[str, Any],
    variant: dict[str, Any],
    args: argparse.Namespace,
    base_segmented: dict[str, Any],
) -> dict[str, Any]:
    bundle = ExperimentBundle.from_json((run_dir / "experiment_bundle.json").read_text(encoding="utf-8-sig"))
    summaries = load_attempt_summaries(run_dir)
    if "validation" not in summaries or "test" not in summaries:
        raise FileNotFoundError(f"missing validation/test summaries in {run_dir}")

    segmented_results = {
        "validation": build_segment_results(bundle, "validation", summaries["validation"]),
        "test": build_segment_results(bundle, "test", summaries["test"]),
    }
    payload = {
        "generated_at_utc": utc_now_iso(),
        "stage": "06_segmented_risk_validation",
        "phase": "06E_r250_overlay_suite",
        "run_name": variant["run_name"],
        "experiment_id": variant["experiment_id"],
        "source_stage_id": source_item["stage_id"],
        "source_run_name": source_item["run_name"],
        "source_run_dir": str(source_item["path"]),
        "label": variant["label"],
        "description": variant["description"],
        "overlay": {
            "risk_pct": args.risk_pct,
            "stop_execution_mode": "broker_native",
            "stop_policy": "direction_split",
            "stop_long_atr_mult": args.stop_long_atr_mult,
            "stop_short_atr_mult": args.stop_short_atr_mult,
            "stop_atr_period": args.stop_atr_period,
            **variant["runtime_extra"],
        },
        "split_runs": {
            "validation": bundle.results.by_split["validation"].model_dump(),
            "test": bundle.results.by_split["test"].model_dump(),
        },
        "segmented_results": segmented_results,
        "cross_segment_summary": build_cross_segment_summary(segmented_results),
    }
    payload["comparison_to_source"] = split_delta(base_segmented, payload)
    return payload


def top_holdout_return(rows: list[dict[str, Any]]) -> dict[str, Any]:
    return max(rows, key=lambda row: float(row["split_runs"]["test"]["headline"].get("return_pct") or float("-inf")))


def load_reference_payload(reference_run_dir: Path) -> dict[str, Any] | None:
    segmented_path = reference_run_dir / "segmented_results.json"
    if not segmented_path.exists():
        return None
    return json.loads(segmented_path.read_text(encoding="utf-8-sig"))


def build_review_markdown(
    *,
    source_item: dict[str, Any],
    base_segmented: dict[str, Any],
    reference_payload: dict[str, Any] | None,
    rows: list[dict[str, Any]],
) -> str:
    leader = top_holdout_return(rows)
    lines = [
        "# 06E R250 Session Overlay Suite Review",
        "",
        f"- source_run: `{source_item['run_name']}`",
        f"- source_run_dir: `{source_item['path']}`",
    ]
    if reference_payload is not None:
        ref_test = reference_payload["split_runs"]["test"]["headline"]
        lines.append(
            f"- reference_soft_decay: `{reference_payload['run_name']}` holdout `return_pct={format_metric(ref_test.get('return_pct'), 3)}`, `PF={format_metric(ref_test.get('profit_factor'), 4)}`, `max_dd_pct={format_metric(ref_test.get('max_dd_pct'), 4)}`"
        )
    lines.extend(
        [
            "",
            "## Batch Summary",
            "",
            f"- best_holdout_run: `{leader['run_name']}` `{leader['label']}`",
            f"- best_holdout_headline: `return_pct={format_metric(leader['split_runs']['test']['headline'].get('return_pct'), 3)}`, `PF={format_metric(leader['split_runs']['test']['headline'].get('profit_factor'), 4)}`, `max_dd_pct={format_metric(leader['split_runs']['test']['headline'].get('max_dd_pct'), 4)}`, `ulcer={format_metric(leader['split_runs']['test']['risk'].get('ulcer_index'), 4)}`",
            "",
            "## Runs",
            "",
        ]
    )
    for row in rows:
        test = row["split_runs"]["test"]["headline"]
        test_risk = row["split_runs"]["test"]["risk"]
        delta = row["comparison_to_source"]["test"]
        lines.extend(
            [
                f"### {row['run_name']} `{row['label']}`",
                "",
                f"- description: `{row['description']}`",
                f"- holdout: `return_pct={format_metric(test.get('return_pct'), 3)}`, `PF={format_metric(test.get('profit_factor'), 4)}`, `trades={test.get('trade_count')}`, `max_dd_pct={format_metric(test.get('max_dd_pct'), 4)}`, `ulcer={format_metric(test_risk.get('ulcer_index'), 4)}`",
                f"- vs 06C_R250: `return_pct_delta={format_metric(delta['return_pct_delta'], 3)}`, `PF_delta={format_metric(delta['profit_factor_delta'], 4)}`, `max_dd_pct_delta={format_metric(delta['max_dd_pct_delta'], 4)}`, `ulcer_delta={format_metric(delta['ulcer_index_delta'], 4)}`",
                f"- overlay: `{json.dumps(row['overlay'], ensure_ascii=False, sort_keys=True)}`",
                "",
            ]
        )
    base_test = base_segmented["split_runs"]["test"]["headline"]
    lines.extend(
        [
            "## Baseline",
            "",
            f"- 06C_R250 holdout: `return_pct={format_metric(base_test.get('return_pct'), 3)}`, `PF={format_metric(base_test.get('profit_factor'), 4)}`, `max_dd_pct={format_metric(base_test.get('max_dd_pct'), 4)}`",
            "",
        ]
    )
    return "\n".join(lines)


def update_review_index(review_index_path: Path, review_name: str) -> None:
    lines = review_index_path.read_text(encoding="utf-8").splitlines() if review_index_path.exists() else []
    if not lines:
        lines = ["# Review Index", "", "## Current Entries"]
    if "## Current Entries" not in lines:
        lines.extend(["", "## Current Entries"])
    entry = f"- `06E`: see `{review_name}`"
    if entry not in lines:
        lines.append(entry)
    write_text(review_index_path, "\n".join(lines).rstrip() + "\n")


def update_selection_status(
    selection_path: Path,
    leader: dict[str, Any],
    reference_payload: dict[str, Any] | None,
) -> None:
    holdout = leader["split_runs"]["test"]["headline"]
    delta = leader["comparison_to_source"]["test"]
    lines = [
        "# Selection Status",
        "",
        "- stage: `06_segmented_risk_validation`",
        "- current phase complete: `06E`",
        f"- current best session overlay run: `{leader['run_name']}`",
        f"- current best label: `{leader['label']}`",
        f"- holdout headline: `return_pct={format_metric(holdout.get('return_pct'), 3)}`, `PF={format_metric(holdout.get('profit_factor'), 4)}`, `trades={holdout.get('trade_count')}`, `max_dd_pct={format_metric(holdout.get('max_dd_pct'), 4)}`",
        f"- vs 06C_R250: `return_pct_delta={format_metric(delta['return_pct_delta'], 3)}`, `PF_delta={format_metric(delta['profit_factor_delta'], 4)}`, `max_dd_pct_delta={format_metric(delta['max_dd_pct_delta'], 4)}`, `ulcer_delta={format_metric(delta['ulcer_index_delta'], 4)}`",
    ]
    if reference_payload is not None:
        ref_test = reference_payload["split_runs"]["test"]["headline"]
        lines.append(
            f"- prior soft-decay reference: `{reference_payload['run_name']}` `return_pct={format_metric(ref_test.get('return_pct'), 3)}`, `PF={format_metric(ref_test.get('profit_factor'), 4)}`, `max_dd_pct={format_metric(ref_test.get('max_dd_pct'), 4)}`"
        )
    lines.append("- next action: `decide whether to local-probe the current best session overlay or port it to nearby risk profiles`")
    write_text(selection_path, "\n".join(lines) + "\n")


def main() -> int:
    args = build_parser().parse_args()
    stage_root = Path(args.stage_root).resolve()
    source_item = build_source_item(Path(args.source_run_dir))
    if not source_item["has_bundle"]:
        raise FileNotFoundError(f"source bundle not found: {source_item['path']}")

    base_segmented = json.loads((source_item["path"] / "segmented_results.json").read_text(encoding="utf-8-sig"))
    reference_payload = load_reference_payload(Path(args.reference_run_dir).resolve())
    rows: list[dict[str, Any]] = []

    for variant in suite_variants(args.batch_id):
        run_dir = stage_root / "02_runs" / "active" / variant["run_name"]
        bundle_path = ensure_bundle(source_item=source_item, run_dir=run_dir, variant=variant, args=args)
        run_tester(bundle_path, "validation")
        run_tester(bundle_path, "test")

        payload = build_payload(
            run_dir=run_dir,
            source_item=source_item,
            variant=variant,
            args=args,
            base_segmented=base_segmented,
        )
        write_json(run_dir / "segmented_results.json", payload)
        write_text(run_dir / "segmented_results.md", build_review_markdown(
            source_item=source_item,
            base_segmented=base_segmented,
            reference_payload=reference_payload,
            rows=[payload],
        ))
        rows.append(payload)

    review_md_path = stage_root / "03_reviews" / f"{args.review_basename}.md"
    review_json_path = stage_root / "03_reviews" / f"{args.review_basename}.json"
    review_payload = {
        "generated_at_utc": utc_now_iso(),
        "stage": "06_segmented_risk_validation",
        "phase": "06E_r250_overlay_suite",
        "source_run_name": source_item["run_name"],
        "source_run_dir": str(source_item["path"]),
        "reference_run_name": reference_payload["run_name"] if reference_payload else None,
        "runs": rows,
        "leader": top_holdout_return(rows),
    }
    write_json(review_json_path, review_payload)
    write_text(
        review_md_path,
        build_review_markdown(
            source_item=source_item,
            base_segmented=base_segmented,
            reference_payload=reference_payload,
            rows=rows,
        )
        + "\n",
    )

    stage_paths = stage06_paths(stage_root)
    update_review_index(stage_paths["review_index"], review_md_path.name)
    update_selection_status(stage_paths["selection"], review_payload["leader"], reference_payload)

    print(f"[done] review={review_md_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
