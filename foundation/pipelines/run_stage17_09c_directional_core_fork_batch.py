#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import joblib
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.multiclass import OneVsRestClassifier

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from foundation.pipelines.experiment_bundle_models import ExperimentBundle, SplitBoundaries
from foundation.pipelines.export_experiment_bundle_assets import run_export_bundle_assets
from foundation.pipelines.run_stage05_mt5_model_family_trial import build_trend_proxy_linear_pipeline, class_counts
from foundation.pipelines.run_stage06_direction_split_segmented_overlay import (
    build_cross_segment_summary,
    build_segment_results,
    format_metric,
    load_attempt_summaries,
    utc_now_iso,
    write_json,
    write_text,
)
from foundation.pipelines.run_stage06_early_wfo_lp_compare import (
    evaluate_split,
    parse_utc,
    patch_bundle,
    prepare_run_dir,
    split_dataset,
    wfo_segment_scheme,
)
from foundation.pipelines.run_stage06_pre_risk_pool_batch import run_tester


STAGE17_ROOT = ROOT_DIR / "stages" / "17_09c_directional_core_fork"
DEFAULT_DATASET_PATH = ROOT_DIR / "stages" / "01_base_feature_ml" / "01_inputs" / "stage01c_h03_band000125_dataset.parquet"
DEFAULT_MODEL_CONFIG_PATH = ROOT_DIR / "stages" / "09_05et_local_probe" / "02_runs" / "active" / "09C_2407_05et_margin0700_0001" / "config.json"
DEFAULT_RULE_STACK_PATH = ROOT_DIR / "stages" / "09_05et_local_probe" / "02_runs" / "active" / "09C_2407_05et_margin0700_0001" / "rule_stack.json"

WINDOW_SPECS = [
    ("2401", "2022-09-01T00:00:00Z", "2024-01-01T00:00:00Z", "2024-10-01T00:00:00Z", "2025-03-01T00:00:00Z"),
    ("2407", "2022-09-01T00:00:00Z", "2024-07-01T00:00:00Z", "2025-04-01T00:00:00Z", "2025-09-01T00:00:00Z"),
    ("2501", "2022-09-01T00:00:00Z", "2025-01-01T00:00:00Z", "2025-10-01T00:00:00Z", "2026-03-01T00:00:00Z"),
]

TARGET_WINDOW_TOKEN = "2407"
TARGET_SEGMENT = "holdout_b"


@dataclass(frozen=True)
class DirectionalSpec:
    stage_id: str
    base_name: str
    label: str
    rationale: str
    classifier_kind: str
    class_weight: Any
    c_value: float


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run strict-WFO directional/core learning forks around 09C to search for a new edge beyond overlay tuning."
    )
    parser.add_argument("--stage-root", default=str(STAGE17_ROOT), help="Stage 17 root directory.")
    parser.add_argument("--dataset-path", default=str(DEFAULT_DATASET_PATH), help="Shared dataset parquet.")
    parser.add_argument("--model-config-path", default=str(DEFAULT_MODEL_CONFIG_PATH), help="09C source config.json.")
    parser.add_argument("--rule-stack-path", default=str(DEFAULT_RULE_STACK_PATH), help="09C source rule_stack.json.")
    parser.add_argument("--batch-id", default="17DF", help="Stage 17 batch id.")
    parser.add_argument("--random-state", type=int, default=42, help="Random seed for retraining.")
    parser.add_argument("--risk-pct", type=float, default=2.0, help="Balance risk percent.")
    parser.add_argument("--stop-atr-period", type=int, default=14, help="ATR period.")
    parser.add_argument("--stop-long-atr-mult", type=float, default=1.4, help="Long ATR multiplier.")
    parser.add_argument("--stop-short-atr-mult", type=float, default=2.0, help="Short ATR multiplier.")
    parser.add_argument(
        "--review-basename",
        default="17DF_09c_directional_core_fork_review",
        help="Review basename written under 03_reviews.",
    )
    parser.add_argument("--rebuild-bundle", action="store_true", help="Force rerun even when segmented results already exist.")
    return parser


def stage17_paths(stage_root: Path) -> dict[str, Path]:
    return {
        "spec": stage_root / "00_spec" / "stage_brief.md",
        "inputs": stage_root / "01_inputs" / "input_manifest.json",
        "review_index": stage_root / "03_reviews" / "review_index.md",
        "selection": stage_root / "04_selected" / "selection_status.md",
    }


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def build_candidates() -> list[DirectionalSpec]:
    return [
        DirectionalSpec(
            stage_id="17A",
            base_name="ref_balanced",
            label="09C_reference_balanced",
            rationale="Reference 09C trend-proxy multinomial logistic with balanced class weights.",
            classifier_kind="multinomial",
            class_weight="balanced",
            c_value=0.70,
        ),
        DirectionalSpec(
            stage_id="17B",
            base_name="short_guard",
            label="09C_short_guard",
            rationale="Reduce marginal shorts by lifting flat weight and slightly lowering short urgency.",
            classifier_kind="multinomial",
            class_weight={0: 0.85, 1: 1.35, 2: 1.0},
            c_value=0.70,
        ),
        DirectionalSpec(
            stage_id="17C",
            base_name="short_specialist",
            label="09C_short_specialist",
            rationale="Sharpen genuine short separation by boosting the short class and relaxing long slightly.",
            classifier_kind="multinomial",
            class_weight={0: 1.35, 1: 1.0, 2: 0.95},
            c_value=0.65,
        ),
        DirectionalSpec(
            stage_id="17D",
            base_name="flat_guard",
            label="09C_flat_guard",
            rationale="Push more uncertain bars into flat globally to test whether abstention is the missing core edge.",
            classifier_kind="multinomial",
            class_weight={0: 1.0, 1: 1.45, 2: 1.0},
            c_value=0.70,
        ),
        DirectionalSpec(
            stage_id="17E",
            base_name="ovr_balanced",
            label="09C_ovr_balanced",
            rationale="Use balanced one-vs-rest direction specialists to test whether separate directional margins survive shifted windows better.",
            classifier_kind="ovr",
            class_weight="balanced",
            c_value=0.55,
        ),
    ]


def ensure_stage_scaffold(stage_root: Path, paths: dict[str, Path], args: argparse.Namespace, candidates: list[DirectionalSpec]) -> None:
    (stage_root / "02_runs" / "active").mkdir(parents=True, exist_ok=True)
    (stage_root / "02_runs" / "archived").mkdir(parents=True, exist_ok=True)
    (stage_root / "03_reviews").mkdir(parents=True, exist_ok=True)
    (stage_root / "04_selected").mkdir(parents=True, exist_ok=True)

    if not paths["spec"].exists():
        write_text(
            paths["spec"],
            "\n".join(
                [
                    "# Stage Brief",
                    "",
                    "- stage: `17_09c_directional_core_fork`",
                    "- goal: `search for a new core edge by changing the directional learning objective around 09C instead of more overlay micro-tuning`",
                    "- base core: `09C_05ET_margin0700_t30_l50_m0700_h4`",
                    "- windows: `2401, 2407, 2501`",
                    "- target segment: `2407 / holdout_b`",
                    "- ranking basis: `positive_test_windows -> positive_holdout_b_windows -> avg_test_return -> min_holdout_b -> avg_test_pf -> min_test`",
                    "- candidates: `reference_balanced, short_guard, short_specialist, flat_guard, ovr_balanced`",
                    "",
                ]
            ),
        )

    manifest = {
        "generated_at_utc": utc_now_iso(),
        "stage": "17_09c_directional_core_fork",
        "phase": args.batch_id,
        "dataset_path": str(Path(args.dataset_path).resolve()),
        "model_config_path": str(Path(args.model_config_path).resolve()),
        "rule_stack_path": str(Path(args.rule_stack_path).resolve()),
        "source_reference_run_name": "09C_05ET_margin0700_t30_l50_m0700_h4",
        "target_window_token": TARGET_WINDOW_TOKEN,
        "target_segment": TARGET_SEGMENT,
        "overlay_defaults": {
            "sizing_mode": "risk_pct",
            "risk_pct": args.risk_pct,
            "capital_base": "balance",
            "stop_model": "atr",
            "stop_execution_mode": "broker_native",
            "stop_policy": "direction_split",
            "stop_long_atr_mult": args.stop_long_atr_mult,
            "stop_short_atr_mult": args.stop_short_atr_mult,
            "stop_atr_period": args.stop_atr_period,
        },
        "window_specs": [
            {
                "token": token,
                "train_start_utc": train_start,
                "train_end_utc_exclusive": train_end,
                "validation_end_utc_exclusive": validation_end,
                "test_end_utc_exclusive": test_end,
            }
            for token, train_start, train_end, validation_end, test_end in WINDOW_SPECS
        ],
        "candidates": [
            {
                "stage_id": spec.stage_id,
                "label": spec.label,
                "rationale": spec.rationale,
                "classifier_kind": spec.classifier_kind,
                "class_weight": spec.class_weight,
                "c_value": spec.c_value,
            }
            for spec in candidates
        ],
    }
    write_json(paths["inputs"], manifest)

    if not paths["review_index"].exists():
        write_text(paths["review_index"], "# Review Index\n\n## Current Entries\n\n- `17DF`: pending\n")

    if not paths["selection"].exists():
        write_text(
            paths["selection"],
            "\n".join(
                [
                    "# Selection Status",
                    "",
                    "- stage: `17_09c_directional_core_fork`",
                    "- status: `running`",
                    "- active base: `09C_05ET_margin0700_t30_l50_m0700_h4`",
                    "- objective: `test whether a directional learning-objective fork creates a stronger core edge than the balanced 09C reference`",
                    "",
                ]
            ),
        )


def window_run_name(spec: DirectionalSpec, window_token: str) -> str:
    return f"{spec.stage_id}_{window_token}_{spec.base_name}_0001"


def build_classifier(spec: DirectionalSpec, random_state: int) -> object:
    if spec.classifier_kind == "multinomial":
        return LogisticRegression(
            solver="lbfgs",
            C=spec.c_value,
            class_weight=spec.class_weight,
            max_iter=2500,
            random_state=random_state,
        )
    if spec.classifier_kind == "ovr":
        return OneVsRestClassifier(
            LogisticRegression(
                solver="lbfgs",
                C=spec.c_value,
                class_weight=spec.class_weight,
                max_iter=2500,
                random_state=random_state,
            )
        )
    raise ValueError(f"unsupported classifier kind: {spec.classifier_kind}")


def fit_directional_model(
    train_df: pd.DataFrame,
    active_features: list[str],
    random_state: int,
    replacement_component_groups: dict[str, list[str]],
    spec: DirectionalSpec,
) -> object:
    x_train = train_df[active_features]
    y_train = train_df["label"]
    model = build_trend_proxy_linear_pipeline(
        active_features,
        random_state,
        replacement_component_groups,
        build_classifier(spec, random_state),
    )
    model.fit(x_train, y_train)
    return model


def build_candidate_config(
    base_config: dict[str, Any],
    *,
    spec: DirectionalSpec,
    window_token: str,
    split_boundaries: SplitBoundaries,
    train_df: pd.DataFrame,
    validation_df: pd.DataFrame,
    test_df: pd.DataFrame,
) -> dict[str, Any]:
    payload = dict(base_config)
    payload.update(
        {
            "run_name": window_run_name(spec, window_token),
            "phase": "stage17_09c_directional_core_fork",
            "generated_at_utc": utc_now_iso(),
            "refit_policy": "strict_wfo_train_only_then_mt5_validation_test",
            "source_reference_run_name": "09C_05ET_margin0700_t30_l50_m0700_h4",
            "model_family": "ovr_trend_proxy_logreg" if spec.classifier_kind == "ovr" else "trend_proxy_sector_logreg",
            "directional_core_fork": {
                "stage_id": spec.stage_id,
                "label": spec.label,
                "rationale": spec.rationale,
                "classifier_kind": spec.classifier_kind,
                "class_weight": spec.class_weight,
                "c_value": spec.c_value,
            },
            "window_token": window_token,
            "wfo_window": split_boundaries.model_dump(),
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
        }
    )
    return payload


def export_bundle_for_run(
    *,
    run_dir: Path,
    rule_stack_path: Path,
    args: argparse.Namespace,
    max_hold_bars: int,
    stage_id: str,
) -> Path:
    export_args = argparse.Namespace(
        run_dir=str(run_dir),
        experiment_id=f"exp_{run_dir.name.lower()}_v1",
        stage_id=stage_id,
        output_dir=str(run_dir),
        stage_name="09c_directional_core_fork",
        bundle_version="1.0.0",
        created_by="python_orchestrator",
        config_json=None,
        dataset_path=None,
        selection_json=None,
        logic_family=None,
        selection_key=None,
        rule_stack_json=str(rule_stack_path),
        smoke_split="test",
        smoke_row_index=0,
        max_hold_bars=max_hold_bars,
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
    return run_dir / "experiment_bundle.json"


def build_run_payload(
    *,
    run_dir: Path,
    spec: DirectionalSpec,
    window_token: str,
    split_boundaries: SplitBoundaries,
    segment_scheme: dict[str, list[tuple[str, Any, Any]]],
    offline_metrics: dict[str, Any],
) -> dict[str, Any]:
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
        "stage": "17_09c_directional_core_fork",
        "phase": "17DF_09c_directional_core_fork",
        "run_name": window_run_name(spec, window_token),
        "candidate_stage_id": spec.stage_id,
        "candidate_label": spec.label,
        "window_token": window_token,
        "directional_core_fork": {
            "label": spec.label,
            "rationale": spec.rationale,
            "classifier_kind": spec.classifier_kind,
            "class_weight": spec.class_weight,
            "c_value": spec.c_value,
        },
        "split_boundaries": split_boundaries.model_dump(),
        "offline_metrics": offline_metrics,
        "split_runs": {
            "validation": bundle.results.by_split["validation"].model_dump(),
            "test": bundle.results.by_split["test"].model_dump(),
        },
        "segmented_results": segmented_results,
        "cross_segment_summary": build_cross_segment_summary(segmented_results),
    }


def segment_metric(payload: dict[str, Any], split_name: str, segment_name: str, metric_name: str) -> float:
    segments = payload["segmented_results"][split_name]["segments"]
    segment = next(item for item in segments if str(item.get("segment") or "") == segment_name)
    return float(segment["headline"].get(metric_name) or 0.0)


def aggregate_candidates(payloads: list[dict[str, Any]], candidates: list[DirectionalSpec]) -> list[dict[str, Any]]:
    by_candidate = {spec.stage_id: [] for spec in candidates}
    spec_by_id = {spec.stage_id: spec for spec in candidates}
    for payload in payloads:
        by_candidate[payload["candidate_stage_id"]].append(payload)

    rows: list[dict[str, Any]] = []
    for stage_id, runs in by_candidate.items():
        if not runs:
            continue
        spec = spec_by_id[stage_id]
        test_returns = [float(run["split_runs"]["test"]["headline"].get("return_pct") or 0.0) for run in runs]
        test_pfs = [float(run["split_runs"]["test"]["headline"].get("profit_factor") or 0.0) for run in runs]
        holdout_b_returns = [segment_metric(run, "test", "holdout_b", "return_pct") for run in runs]
        target_run = next(run for run in runs if run["window_token"] == TARGET_WINDOW_TOKEN)
        rows.append(
            {
                "candidate_stage_id": stage_id,
                "candidate_label": spec.label,
                "rationale": spec.rationale,
                "classifier_kind": spec.classifier_kind,
                "class_weight": spec.class_weight,
                "avg_test_return_pct": float(np.mean(test_returns)),
                "min_test_return_pct": float(np.min(test_returns)),
                "avg_test_profit_factor": float(np.mean(test_pfs)),
                "avg_holdout_b_return_pct": float(np.mean(holdout_b_returns)),
                "min_holdout_b_return_pct": float(np.min(holdout_b_returns)),
                "target_window_test_return_pct": float(target_run["split_runs"]["test"]["headline"].get("return_pct") or 0.0),
                "target_window_test_profit_factor": float(target_run["split_runs"]["test"]["headline"].get("profit_factor") or 0.0),
                "target_holdout_b_return_pct": segment_metric(target_run, "test", TARGET_SEGMENT, "return_pct"),
                "target_holdout_b_profit_factor": segment_metric(target_run, "test", TARGET_SEGMENT, "profit_factor"),
                "positive_test_windows": int(sum(value > 0.0 for value in test_returns)),
                "positive_holdout_b_windows": int(sum(value > 0.0 for value in holdout_b_returns)),
                "per_window": [
                    {
                        "window_token": run["window_token"],
                        "validation_return_pct": float(run["split_runs"]["validation"]["headline"].get("return_pct") or 0.0),
                        "test_return_pct": float(run["split_runs"]["test"]["headline"].get("return_pct") or 0.0),
                        "test_profit_factor": float(run["split_runs"]["test"]["headline"].get("profit_factor") or 0.0),
                        "holdout_b_return_pct": segment_metric(run, "test", "holdout_b", "return_pct"),
                        "holdout_b_profit_factor": segment_metric(run, "test", "holdout_b", "profit_factor"),
                    }
                    for run in sorted(runs, key=lambda item: item["window_token"])
                ],
            }
        )

    rows.sort(
        key=lambda row: (
            int(row["positive_test_windows"]),
            int(row["positive_holdout_b_windows"]),
            float(row["avg_test_return_pct"]),
            float(row["min_holdout_b_return_pct"]),
            float(row["avg_test_profit_factor"]),
            float(row["min_test_return_pct"]),
        ),
        reverse=True,
    )
    for rank, row in enumerate(rows, start=1):
        row["rank"] = rank
    return rows


def build_review_markdown(rows: list[dict[str, Any]], payloads: list[dict[str, Any]]) -> str:
    lines = [
        "# Stage 17 09C Directional Core Fork Review",
        "",
        "- windows: `2401, 2407, 2501`",
        "- source core: `09C_05ET_margin0700_t30_l50_m0700_h4`",
        "- target: `2407 / holdout_b`",
        "- ranking basis: `positive_test_windows -> positive_holdout_b_windows -> avg_test_return -> min_holdout_b -> avg_test_pf -> min_test`",
        "",
        "## Candidate Ranking",
        "",
    ]
    for row in rows:
        lines.append(
            f"- [{row['rank']}] `{row['candidate_stage_id']}` `{row['candidate_label']}`: "
            f"avg_test=`{format_metric(row['avg_test_return_pct'], 3)}`, "
            f"min_test=`{format_metric(row['min_test_return_pct'], 3)}`, "
            f"target_holdout_b=`{format_metric(row['target_holdout_b_return_pct'], 3)}`, "
            f"target_holdout_b_PF=`{format_metric(row['target_holdout_b_profit_factor'], 4)}`, "
            f"min_holdout_b=`{format_metric(row['min_holdout_b_return_pct'], 3)}`, "
            f"positive_test_windows=`{row['positive_test_windows']}/3`, "
            f"positive_holdout_b_windows=`{row['positive_holdout_b_windows']}/3`"
        )
        lines.append(f"  - rationale: `{row['rationale']}`")
        lines.append(f"  - classifier_kind: `{row['classifier_kind']}`, class_weight: `{json.dumps(row['class_weight'], ensure_ascii=False, sort_keys=True)}`")
        for window_row in row["per_window"]:
            lines.append(
                f"  - `{window_row['window_token']}`: validation=`{format_metric(window_row['validation_return_pct'], 3)}`, "
                f"test=`{format_metric(window_row['test_return_pct'], 3)}`, PF=`{format_metric(window_row['test_profit_factor'], 4)}`, "
                f"holdout_b=`{format_metric(window_row['holdout_b_return_pct'], 3)}`, holdout_b_PF=`{format_metric(window_row['holdout_b_profit_factor'], 4)}`"
            )
        lines.append("")

    if rows:
        leader = rows[0]
        lines.extend(
            [
                "## Readout",
                "",
                f"- directional-core leader: `{leader['candidate_stage_id']}` `{leader['candidate_label']}`",
                f"- leader avg test return: `{format_metric(leader['avg_test_return_pct'], 3)}`",
                f"- leader min holdout_b: `{format_metric(leader['min_holdout_b_return_pct'], 3)}`",
                f"- leader target 2407 holdout_b: `{format_metric(leader['target_holdout_b_return_pct'], 3)}`",
                f"- total runs captured: `{len(payloads)}`",
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
    entry = f"- `17DF`: see `{review_name}`"
    if entry not in lines:
        lines.append(entry)
    write_text(review_index_path, "\n".join(lines).rstrip() + "\n")


def update_selection_status(selection_path: Path, leader: dict[str, Any]) -> None:
    lines = [
        "# Selection Status",
        "",
        "- stage: `17_09c_directional_core_fork`",
        "- status: `completed`",
        f"- directional-core leader: `{leader['candidate_stage_id']}` `{leader['candidate_label']}`",
        f"- leader basis: `positive_test_windows={leader['positive_test_windows']}/3, positive_holdout_b_windows={leader['positive_holdout_b_windows']}/3, avg_test_return={format_metric(leader['avg_test_return_pct'], 3)}, min_holdout_b={format_metric(leader['min_holdout_b_return_pct'], 3)}, target_2407_holdout_b={format_metric(leader['target_holdout_b_return_pct'], 3)}`",
        "- next action: `decide whether the directional learning fork creates a genuinely stronger core than 09C before re-layering the best practical overlay`",
        "",
    ]
    write_text(selection_path, "\n".join(lines))


def main() -> int:
    args = build_parser().parse_args()

    stage_root = Path(args.stage_root).resolve()
    dataset_path = Path(args.dataset_path).resolve()
    model_config_path = Path(args.model_config_path).resolve()
    rule_stack_path = Path(args.rule_stack_path).resolve()
    paths = stage17_paths(stage_root)
    candidates = build_candidates()
    ensure_stage_scaffold(stage_root, paths, args, candidates)

    dataset = pd.read_parquet(dataset_path)
    base_config = load_json(model_config_path)
    active_features = list(base_config["active_input_features"])
    replacement_component_groups = dict(base_config["replacement_sector_components"])
    base_rule_stack = load_json(rule_stack_path)
    max_hold_bars = int(base_rule_stack["exit"][0]["params"]["max_hold_bars"])
    payloads: list[dict[str, Any]] = []

    for window_token, train_start_raw, train_end_raw, validation_end_raw, test_end_raw in WINDOW_SPECS:
        train_start = parse_utc(train_start_raw)
        train_end = parse_utc(train_end_raw)
        validation_end = parse_utc(validation_end_raw)
        test_end = parse_utc(test_end_raw)
        split_boundaries = SplitBoundaries(
            train_start_utc=train_start.isoformat().replace("+00:00", "Z"),
            train_end_utc_exclusive=train_end.isoformat().replace("+00:00", "Z"),
            validation_end_utc_exclusive=validation_end.isoformat().replace("+00:00", "Z"),
            test_end_utc_exclusive=test_end.isoformat().replace("+00:00", "Z"),
        )
        segment_scheme = wfo_segment_scheme(train_end, validation_end, validation_end, test_end)
        splits = split_dataset(dataset, train_start, train_end, validation_end, test_end)
        train_df = splits["train"]
        validation_df = splits["validation"]
        test_df = splits["test"]
        if train_df.empty or validation_df.empty or test_df.empty:
            raise RuntimeError(f"empty strict WFO split for window {window_token}")

        for spec in candidates:
            run_dir = stage_root / "02_runs" / "active" / window_run_name(spec, window_token)
            segmented_path = run_dir / "segmented_results.json"
            if segmented_path.exists() and not args.rebuild_bundle:
                payloads.append(load_json(segmented_path))
                continue

            model = fit_directional_model(
                train_df,
                active_features,
                args.random_state,
                replacement_component_groups,
                spec,
            )

            prepare_run_dir(run_dir)
            validation_metrics, validation_predictions = evaluate_split(model, validation_df, active_features)
            test_metrics, test_predictions = evaluate_split(model, test_df, active_features)
            offline_metrics = {"validation": validation_metrics, "test": test_metrics}

            joblib.dump(copy.deepcopy(model), run_dir / "model.joblib")
            validation_predictions.to_parquet(run_dir / "validation_predictions.parquet", index=False)
            test_predictions.to_parquet(run_dir / "test_predictions.parquet", index=False)
            write_json(run_dir / "rule_stack.json", base_rule_stack)
            write_json(
                run_dir / "candidate_manifest.json",
                {
                    "generated_at_utc": utc_now_iso(),
                    "stage": "17_09c_directional_core_fork",
                    "window_token": window_token,
                    "stage_id": spec.stage_id,
                    "run_name": window_run_name(spec, window_token),
                    "candidate_label": spec.label,
                    "rationale": spec.rationale,
                    "classifier_kind": spec.classifier_kind,
                    "class_weight": spec.class_weight,
                    "c_value": spec.c_value,
                },
            )
            write_json(
                run_dir / "config.json",
                build_candidate_config(
                    base_config,
                    spec=spec,
                    window_token=window_token,
                    split_boundaries=split_boundaries,
                    train_df=train_df,
                    validation_df=validation_df,
                    test_df=test_df,
                ),
            )
            write_json(run_dir / "metrics.json", offline_metrics)

            bundle_path = run_dir / "experiment_bundle.json"
            if not bundle_path.exists() or args.rebuild_bundle:
                bundle_path = export_bundle_for_run(
                    run_dir=run_dir,
                    rule_stack_path=run_dir / "rule_stack.json",
                    args=args,
                    max_hold_bars=max_hold_bars,
                    stage_id=spec.stage_id,
                )

            patch_bundle(
                bundle_path=bundle_path,
                split_boundaries=split_boundaries,
                split_counts={
                    "train": int(len(train_df)),
                    "validation": int(len(validation_df)),
                    "test": int(len(test_df)),
                },
                runtime_extra={
                    "wfo_mode": "strict_retrain",
                    "window_token": window_token,
                    "candidate_stage_id": spec.stage_id,
                    "candidate_label": spec.label,
                },
                wfo_metadata={
                    "wfo_window_name": window_token,
                    "wfo_phase": "17DF_09c_directional_core_fork",
                    "candidate_stage_id": spec.stage_id,
                    "candidate_label": spec.label,
                },
            )

            run_tester(bundle_path, "validation")
            run_tester(bundle_path, "test")

            payload = build_run_payload(
                run_dir=run_dir,
                spec=spec,
                window_token=window_token,
                split_boundaries=split_boundaries,
                segment_scheme=segment_scheme,
                offline_metrics=offline_metrics,
            )
            write_json(segmented_path, payload)
            write_text(run_dir / "segmented_results.md", json.dumps(payload["cross_segment_summary"], ensure_ascii=False, indent=2) + "\n")
            payloads.append(payload)

    rows = aggregate_candidates(payloads, candidates)
    review_json_path = stage_root / "03_reviews" / f"{args.review_basename}.json"
    review_md_path = stage_root / "03_reviews" / f"{args.review_basename}.md"
    review_payload = {
        "generated_at_utc": utc_now_iso(),
        "stage": "17_09c_directional_core_fork",
        "phase": "17DF_09c_directional_core_fork",
        "target_window_token": TARGET_WINDOW_TOKEN,
        "target_segment": TARGET_SEGMENT,
        "aggregated_candidates": rows,
        "runs": payloads,
    }
    write_json(review_json_path, review_payload)
    write_text(review_md_path, build_review_markdown(rows, payloads))
    update_review_index(paths["review_index"], review_md_path.name)
    if rows:
        update_selection_status(paths["selection"], rows[0])

    print(f"[done] review={review_md_path}")
    for row in rows:
        print(
            f"[done] candidate={row['candidate_stage_id']} avg_test={row['avg_test_return_pct']:.3f} "
            f"min_holdout_b={row['min_holdout_b_return_pct']:.3f} target_holdout_b={row['target_holdout_b_return_pct']:.3f}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
