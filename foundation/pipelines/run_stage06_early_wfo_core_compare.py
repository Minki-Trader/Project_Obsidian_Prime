#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import joblib
import pandas as pd

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from foundation.pipelines.experiment_bundle_models import SplitBoundaries
from foundation.pipelines.export_experiment_bundle_assets import run_export_bundle_assets
from foundation.pipelines.run_stage05_mt5_model_family_trial import class_counts, fit_trend_proxy_sector_logreg
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
from foundation.pipelines.run_stage06_early_wfo_lp_compare import (
    DEFAULT_DATASET_PATH,
    DEFAULT_LOGIC_RULE_STACK_PATH,
    DEFAULT_MODEL_CONFIG_PATH,
    evaluate_split,
    parse_utc,
    patch_bundle,
    prepare_run_dir,
    split_dataset,
    wfo_segment_scheme,
)
from foundation.pipelines.run_stage06_pre_risk_pool_batch import run_tester


STAGE06_ROOT = ROOT_DIR / "stages" / "06_segmented_risk_validation"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Retrain the 06C/06D source model on an earlier WFO window and compare the base vs soft-decay overlays."
    )
    parser.add_argument("--stage-root", default=str(STAGE06_ROOT), help="Stage 06 root directory.")
    parser.add_argument("--dataset-path", default=str(DEFAULT_DATASET_PATH), help="Shared dataset parquet.")
    parser.add_argument("--model-config-path", default=str(DEFAULT_MODEL_CONFIG_PATH), help="Source 05DP config.json.")
    parser.add_argument(
        "--logic-rule-stack-path",
        default=str(DEFAULT_LOGIC_RULE_STACK_PATH),
        help="Source 05ER rule_stack.json used as the base logic.",
    )
    parser.add_argument("--batch-id", default="06G", help="Stage 06 batch id.")
    parser.add_argument("--random-state", type=int, default=42, help="Random seed for retraining.")
    parser.add_argument("--risk-pct", type=float, default=2.5, help="Base risk percent.")
    parser.add_argument("--stop-atr-period", type=int, default=14, help="ATR period.")
    parser.add_argument("--stop-long-atr-mult", type=float, default=1.4, help="Long ATR multiplier.")
    parser.add_argument("--stop-short-atr-mult", type=float, default=2.0, help="Short ATR multiplier.")
    parser.add_argument("--train-start", default="2022-09-01T00:00:00Z", help="Train start UTC.")
    parser.add_argument("--train-end", default="2024-07-01T00:00:00Z", help="Train end UTC exclusive.")
    parser.add_argument("--validation-end", default="2025-04-01T00:00:00Z", help="Validation end UTC exclusive.")
    parser.add_argument("--test-end", default="2025-09-01T00:00:00Z", help="Test end UTC exclusive.")
    parser.add_argument(
        "--review-basename",
        default="06G_early_wfo_core_compare_review",
        help="Stage 06 review basename.",
    )
    parser.add_argument("--rebuild-bundle", action="store_true", help="Force bundle rebuild.")
    return parser


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def overlay_variants(batch_id: str) -> list[dict[str, Any]]:
    return [
        {
            "token": "BASE",
            "run_name": f"{batch_id}_WFO_C",
            "experiment_id": f"exp_{batch_id.lower()}_early_wfo_06c_v1",
            "label": "plain_direction_split",
            "description": "06C baseline without session decay.",
            "standard_reference_run": "06C_R250",
            "runtime_extra": {},
        },
        {
            "token": "SD01",
            "run_name": f"{batch_id}_WFO_D",
            "experiment_id": f"exp_{batch_id.lower()}_early_wfo_06d_v1",
            "label": "soft_decay_reference",
            "description": "06D soft session decay reference.",
            "standard_reference_run": "06D_R250_SD01",
            "runtime_extra": {
                "monday_risk_pct_mult": 0.75,
                "ny_postcash_risk_pct_mult": 0.70,
            },
        },
    ]


def build_run_payload(
    *,
    run_dir: Path,
    variant: dict[str, Any],
    offline_metrics: dict[str, Any],
    split_boundaries: SplitBoundaries,
    segment_scheme: dict[str, list[tuple[str, Any, Any]]],
    source_model_config_path: Path,
    logic_rule_stack_path: Path,
) -> dict[str, Any]:
    from foundation.pipelines.experiment_bundle_models import ExperimentBundle

    bundle = ExperimentBundle.from_json((run_dir / "experiment_bundle.json").read_text(encoding="utf-8-sig"))
    summaries = load_attempt_summaries(run_dir)
    if "validation" not in summaries or "test" not in summaries:
        raise FileNotFoundError(f"missing validation/test summaries in {run_dir}")

    segmented_results = {
        "validation": build_segment_results(bundle, "validation", summaries["validation"], scheme=segment_scheme),
        "test": build_segment_results(bundle, "test", summaries["test"], scheme=segment_scheme),
    }
    return {
        "generated_at_utc": utc_now_iso(),
        "stage": "06_segmented_risk_validation",
        "phase": "06G_early_wfo_core_compare",
        "run_name": variant["run_name"],
        "experiment_id": variant["experiment_id"],
        "label": variant["label"],
        "description": variant["description"],
        "standard_reference_run": variant["standard_reference_run"],
        "source_model_config_path": str(source_model_config_path),
        "logic_rule_stack_path": str(logic_rule_stack_path),
        "wfo_window": {
            "train_start_utc": split_boundaries.train_start_utc,
            "train_end_utc_exclusive": split_boundaries.train_end_utc_exclusive,
            "validation_end_utc_exclusive": split_boundaries.validation_end_utc_exclusive,
            "test_end_utc_exclusive": split_boundaries.test_end_utc_exclusive,
        },
        "overlay": {
            "risk_pct": bundle.runtime_snapshot.risk_pct,
            "stop_execution_mode": bundle.runtime_snapshot.stop_execution_mode,
            "stop_policy": bundle.runtime_snapshot.stop_policy,
            "stop_long_atr_mult": bundle.runtime_snapshot.stop_long_atr_mult,
            "stop_short_atr_mult": bundle.runtime_snapshot.stop_short_atr_mult,
            "stop_atr_period": bundle.runtime_snapshot.stop_atr_period,
            **variant["runtime_extra"],
        },
        "offline_metrics": offline_metrics,
        "split_runs": {
            "validation": bundle.results.by_split["validation"].model_dump(),
            "test": bundle.results.by_split["test"].model_dump(),
        },
        "segmented_results": segmented_results,
        "cross_segment_summary": build_cross_segment_summary(segmented_results),
    }


def build_batch_review_markdown(payloads: list[dict[str, Any]], split_boundaries: SplitBoundaries) -> str:
    leader = max(
        payloads,
        key=lambda item: float(item["split_runs"]["test"]["headline"].get("return_pct") or float("-inf")),
    )
    lines = [
        "# 06G Early WFO Core Compare Review",
        "",
        f"- window: `train={split_boundaries.train_start_utc} .. {split_boundaries.train_end_utc_exclusive}`, `validation={split_boundaries.train_end_utc_exclusive} .. {split_boundaries.validation_end_utc_exclusive}`, `test={split_boundaries.validation_end_utc_exclusive} .. {split_boundaries.test_end_utc_exclusive}`",
        f"- leader_by_holdout_return: `{leader['run_name']}` `{leader['label']}`",
        "",
        "## Runs",
        "",
    ]
    for payload in payloads:
        validation = payload["split_runs"]["validation"]["headline"]
        test = payload["split_runs"]["test"]["headline"]
        validation_offline = payload["offline_metrics"]["validation"]
        test_offline = payload["offline_metrics"]["test"]
        lines.extend(
            [
                f"### {payload['run_name']} `{payload['label']}`",
                "",
                f"- description: `{payload['description']}`",
                f"- overlay: `{json.dumps(payload['overlay'], ensure_ascii=False, sort_keys=True)}`",
                f"- offline validation: `macro_f1={format_metric(validation_offline['macro_f1'], 4)}`, `balanced_accuracy={format_metric(validation_offline['balanced_accuracy'], 4)}`, `log_loss={format_metric(validation_offline['log_loss'], 4)}`",
                f"- offline test: `macro_f1={format_metric(test_offline['macro_f1'], 4)}`, `balanced_accuracy={format_metric(test_offline['balanced_accuracy'], 4)}`, `log_loss={format_metric(test_offline['log_loss'], 4)}`",
                f"- MT5 validation: `return_pct={format_metric(validation.get('return_pct'), 3)}`, `PF={format_metric(validation.get('profit_factor'), 4)}`, `trades={validation.get('trade_count')}`, `max_dd_pct={format_metric(validation.get('max_dd_pct'), 4)}`",
                f"- MT5 test: `return_pct={format_metric(test.get('return_pct'), 3)}`, `PF={format_metric(test.get('profit_factor'), 4)}`, `trades={test.get('trade_count')}`, `max_dd_pct={format_metric(test.get('max_dd_pct'), 4)}`",
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
    entry = f"- `06G`: see `{review_name}`"
    if entry not in lines:
        lines.append(entry)
    write_text(review_index_path, "\n".join(lines).rstrip() + "\n")


def update_selection_status(selection_path: Path, leader: dict[str, Any], split_boundaries: SplitBoundaries) -> None:
    holdout = leader["split_runs"]["test"]["headline"]
    lines = [
        "# Selection Status",
        "",
        "- stage: `06_segmented_risk_validation`",
        "- current phase complete: `06G`",
        "- standard-window leaders remain: `06D_R250_SD01` vs `06E_R250_LP01/LP02`",
        f"- early WFO core leader: `{leader['run_name']}` `{leader['label']}`",
        f"- WFO window: `train={split_boundaries.train_start_utc} .. {split_boundaries.train_end_utc_exclusive}`, `validation={split_boundaries.train_end_utc_exclusive} .. {split_boundaries.validation_end_utc_exclusive}`, `test={split_boundaries.validation_end_utc_exclusive} .. {split_boundaries.test_end_utc_exclusive}`",
        f"- early WFO core holdout headline: `return_pct={format_metric(holdout.get('return_pct'), 3)}`, `PF={format_metric(holdout.get('profit_factor'), 4)}`, `trades={holdout.get('trade_count')}`, `max_dd_pct={format_metric(holdout.get('max_dd_pct'), 4)}`",
        "- next action: `decide whether session decay as a family is robust enough, or should stay standard-window-only`",
    ]
    write_text(selection_path, "\n".join(lines) + "\n")


def main() -> int:
    args = build_parser().parse_args()

    stage_root = Path(args.stage_root).resolve()
    dataset_path = Path(args.dataset_path).resolve()
    model_config_path = Path(args.model_config_path).resolve()
    logic_rule_stack_path = Path(args.logic_rule_stack_path).resolve()
    stage_paths = stage06_paths(stage_root)

    train_start = parse_utc(args.train_start)
    train_end = parse_utc(args.train_end)
    validation_end = parse_utc(args.validation_end)
    test_end = parse_utc(args.test_end)
    if not (train_start < train_end < validation_end < test_end):
        raise ValueError("expected train_start < train_end < validation_end < test_end")

    split_boundaries = SplitBoundaries(
        train_start_utc=train_start.isoformat().replace("+00:00", "Z"),
        train_end_utc_exclusive=train_end.isoformat().replace("+00:00", "Z"),
        validation_end_utc_exclusive=validation_end.isoformat().replace("+00:00", "Z"),
        test_end_utc_exclusive=test_end.isoformat().replace("+00:00", "Z"),
    )
    segment_scheme = wfo_segment_scheme(train_end, validation_end, validation_end, test_end)

    base_config = load_json(model_config_path)
    logic_rule_stack = load_json(logic_rule_stack_path)
    dataset = pd.read_parquet(dataset_path)
    splits = split_dataset(dataset, train_start, train_end, validation_end, test_end)
    train_df = splits["train"]
    validation_df = splits["validation"]
    test_df = splits["test"]
    if train_df.empty or validation_df.empty or test_df.empty:
        raise RuntimeError("one or more WFO splits are empty")

    active_features = list(base_config["active_input_features"])
    replacement_component_groups = dict(base_config["replacement_sector_components"])
    model = fit_trend_proxy_sector_logreg(
        train_df,
        active_features,
        args.random_state,
        replacement_component_groups,
    )

    validation_metrics, validation_predictions = evaluate_split(model, validation_df, active_features)
    test_metrics, test_predictions = evaluate_split(model, test_df, active_features)
    offline_metrics = {"validation": validation_metrics, "test": test_metrics}

    review_payloads: list[dict[str, Any]] = []
    for variant in overlay_variants(args.batch_id):
        run_dir = stage_root / "02_runs" / "active" / variant["run_name"]
        prepare_run_dir(run_dir)
        joblib.dump(model, run_dir / "model.joblib")
        validation_predictions.to_parquet(run_dir / "validation_predictions.parquet", index=False)
        test_predictions.to_parquet(run_dir / "test_predictions.parquet", index=False)
        write_json(run_dir / "rule_stack.json", logic_rule_stack)
        config_payload = {
            **base_config,
            "run_name": variant["run_name"],
            "phase": "stage06_early_wfo_core_compare",
            "generated_at_utc": utc_now_iso(),
            "refit_policy": "strict_wfo_train_only_then_mt5_validation_test",
            "dataset_path": str(dataset_path.relative_to(ROOT_DIR)),
            "logic_reference_run_name": logic_rule_stack_path.parent.name,
            "logic_filter": logic_rule_stack["filters"][0],
            "logic_exit": logic_rule_stack["exit"][0],
            "row_counts": {
                "train": int(len(train_df)),
                "validation": int(len(validation_df)),
                "test": int(len(test_df)),
            },
            "class_counts": {
                "train": class_counts(train_df["label"]),
                "validation": class_counts(validation_df["label"]),
                "test": class_counts(test_df["label"]),
            },
            "wfo_window": {
                "train_start_utc": split_boundaries.train_start_utc,
                "train_end_utc_exclusive": split_boundaries.train_end_utc_exclusive,
                "validation_end_utc_exclusive": split_boundaries.validation_end_utc_exclusive,
                "test_end_utc_exclusive": split_boundaries.test_end_utc_exclusive,
            },
            "overlay_label": variant["label"],
            "overlay_runtime_extra": variant["runtime_extra"],
        }
        write_json(run_dir / "config.json", config_payload)

        bundle_path = run_dir / "experiment_bundle.json"
        if not bundle_path.exists() or args.rebuild_bundle:
            export_args = argparse.Namespace(
                run_dir=str(run_dir),
                experiment_id=variant["experiment_id"],
                stage_id=args.batch_id,
                output_dir=str(run_dir),
                stage_name="segmented_risk_validation",
                bundle_version="1.0.0",
                created_by="python_orchestrator",
                config_json=None,
                dataset_path=None,
                selection_json=None,
                logic_family=None,
                selection_key=None,
                rule_stack_json=str(run_dir / "rule_stack.json"),
                smoke_split="test",
                smoke_row_index=0,
                max_hold_bars=int(logic_rule_stack["exit"][0]["params"]["max_hold_bars"]),
                sizing_mode="risk_pct",
                fixed_lot=0.1,
                risk_pct=args.risk_pct,
                capital_base="balance",
                stop_model="atr",
                stop_execution_mode="broker_native",
                stop_policy="direction_split",
                stop_atr_period=args.stop_atr_period,
                stop_atr_mult=1.0,
                stop_long_atr_mult=args.stop_long_atr_mult,
                stop_short_atr_mult=args.stop_short_atr_mult,
                stop_low_vol_threshold=None,
                stop_high_vol_threshold=None,
                stop_low_atr_mult=None,
                stop_mid_atr_mult=None,
                stop_high_atr_mult=None,
                build_bundle=True,
            )
            run_export_bundle_assets(export_args)

        patch_bundle(
            bundle_path=bundle_path,
            split_boundaries=split_boundaries,
            split_counts={
                "train": int(len(train_df)),
                "validation": int(len(validation_df)),
                "test": int(len(test_df)),
            },
            runtime_extra={
                **variant["runtime_extra"],
                "session_overlay_label": variant["label"],
                "wfo_mode": "strict_retrain",
            },
            wfo_metadata={
                "wfo_window_name": "early_shift_2024q3_2025q3",
                "wfo_phase": "06G_early_wfo_core_compare",
                "overlay_label": variant["label"],
            },
        )

        run_tester(bundle_path, "validation")
        run_tester(bundle_path, "test")

        payload = build_run_payload(
            run_dir=run_dir,
            variant=variant,
            offline_metrics=offline_metrics,
            split_boundaries=split_boundaries,
            segment_scheme=segment_scheme,
            source_model_config_path=model_config_path,
            logic_rule_stack_path=logic_rule_stack_path,
        )
        write_json(run_dir / "segmented_results.json", payload)
        write_text(run_dir / "segmented_results.md", build_batch_review_markdown([payload], split_boundaries))
        review_payloads.append(payload)

    review_md_path = stage_root / "03_reviews" / f"{args.review_basename}.md"
    review_json_path = stage_root / "03_reviews" / f"{args.review_basename}.json"
    batch_payload = {
        "generated_at_utc": utc_now_iso(),
        "stage": "06_segmented_risk_validation",
        "phase": "06G_early_wfo_core_compare",
        "window": {
            "train_start_utc": split_boundaries.train_start_utc,
            "train_end_utc_exclusive": split_boundaries.train_end_utc_exclusive,
            "validation_end_utc_exclusive": split_boundaries.validation_end_utc_exclusive,
            "test_end_utc_exclusive": split_boundaries.test_end_utc_exclusive,
        },
        "runs": review_payloads,
    }
    write_json(review_json_path, batch_payload)
    write_text(review_md_path, build_batch_review_markdown(review_payloads, split_boundaries))
    update_review_index(stage_paths["review_index"], review_md_path.name)

    leader = max(
        review_payloads,
        key=lambda item: float(item["split_runs"]["test"]["headline"].get("return_pct") or float("-inf")),
    )
    update_selection_status(stage_paths["selection"], leader, split_boundaries)
    write_json(
        stage_root / "01_inputs" / "06G_early_wfo_manifest.json",
        {
            "generated_at_utc": utc_now_iso(),
            "phase": "06G_early_wfo_core_compare",
            "model_config_path": str(model_config_path),
            "logic_rule_stack_path": str(logic_rule_stack_path),
            "dataset_path": str(dataset_path),
            "wfo_window": batch_payload["window"],
            "variants": [
                {"run_name": payload["run_name"], "label": payload["label"], "overlay": payload["overlay"]}
                for payload in review_payloads
            ],
        },
    )

    print(f"[done] review={review_md_path}")
    for payload in review_payloads:
        print(f"[done] run={payload['run_name']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
