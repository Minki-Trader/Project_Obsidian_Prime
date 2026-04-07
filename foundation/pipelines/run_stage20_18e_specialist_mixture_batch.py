#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import VotingClassifier
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


STAGE20_ROOT = ROOT_DIR / "stages" / "20_18e_specialist_mixture"
STAGE18_SOURCE_ROOT = ROOT_DIR / "stages" / "18_directional_core_overlay_matrix" / "02_runs" / "active"
DEFAULT_DATASET_PATH = ROOT_DIR / "stages" / "01_base_feature_ml" / "01_inputs" / "stage01c_h03_band000125_dataset.parquet"
DEFAULT_MODEL_CONFIG_PATH = (
    ROOT_DIR / "stages" / "17_09c_directional_core_fork" / "02_runs" / "active" / "17E_2407_ovr_balanced_0001" / "config.json"
)
DEFAULT_RULE_STACK_PATH = (
    ROOT_DIR / "stages" / "17_09c_directional_core_fork" / "02_runs" / "active" / "17E_2407_ovr_balanced_0001" / "rule_stack.json"
)

WINDOW_SPECS = [
    ("2401", "2022-09-01T00:00:00Z", "2024-01-01T00:00:00Z", "2024-10-01T00:00:00Z", "2025-03-01T00:00:00Z"),
    ("2407", "2022-09-01T00:00:00Z", "2024-07-01T00:00:00Z", "2025-04-01T00:00:00Z", "2025-09-01T00:00:00Z"),
    ("2501", "2022-09-01T00:00:00Z", "2025-01-01T00:00:00Z", "2025-10-01T00:00:00Z", "2026-03-01T00:00:00Z"),
]

TARGET_WINDOW_TOKEN = "2407"
TARGET_SEGMENT = "holdout_b"
SOURCE_REFERENCE_STAGE_ID = "18E"
SOURCE_REFERENCE_LABEL = "17E_postcash_hold_cut"

PH20_OVERLAY = {
    "monday_risk_pct_mult": 0.75,
    "ny_postcash_risk_pct_mult": 0.70,
    "ny_postcash_hold_cap_bars": 3,
    "session_overlay_label": "postcash_hold_cut",
}

BD20_OVERLAY = {
    "monday_risk_pct_mult": 0.575,
    "ny_postcash_risk_pct_mult": 0.6125,
    "session_overlay_label": "balanced_micro",
}


@dataclass(frozen=True)
class DirectionalComponent:
    component_id: str
    classifier_kind: str
    class_weight: Any
    c_value: float


@dataclass(frozen=True)
class MixtureSpec:
    stage_id: str
    base_name: str
    label: str
    rationale: str
    model_kind: str
    component_ids: tuple[str, ...]
    voter_weights: tuple[float, ...]
    runtime_extra: dict[str, Any]


COMPONENTS: dict[str, DirectionalComponent] = {
    "17E": DirectionalComponent("17E", "ovr", "balanced", 0.55),
    "17C": DirectionalComponent("17C", "multinomial", {0: 1.35, 1: 1.0, 2: 0.95}, 0.65),
    "17D": DirectionalComponent("17D", "multinomial", {0: 1.0, 1: 1.45, 2: 1.0}, 0.70),
}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run strict-WFO specialist-mixture forks around 18E by combining the 17E robust core with 17C/17D directional specialists."
    )
    parser.add_argument("--stage-root", default=str(STAGE20_ROOT), help="Stage 20 root directory.")
    parser.add_argument("--source-root", default=str(STAGE18_SOURCE_ROOT), help="Stage 18 active run root.")
    parser.add_argument("--dataset-path", default=str(DEFAULT_DATASET_PATH), help="Shared dataset parquet.")
    parser.add_argument("--model-config-path", default=str(DEFAULT_MODEL_CONFIG_PATH), help="17E source config.json.")
    parser.add_argument("--rule-stack-path", default=str(DEFAULT_RULE_STACK_PATH), help="17E source rule_stack.json.")
    parser.add_argument("--batch-id", default="20SM", help="Stage 20 batch id.")
    parser.add_argument("--random-state", type=int, default=42, help="Random seed for retraining.")
    parser.add_argument("--risk-pct", type=float, default=2.0, help="Balance risk percent.")
    parser.add_argument("--stop-atr-period", type=int, default=14, help="ATR period.")
    parser.add_argument("--stop-long-atr-mult", type=float, default=1.4, help="Long ATR multiplier.")
    parser.add_argument("--stop-short-atr-mult", type=float, default=2.0, help="Short ATR multiplier.")
    parser.add_argument(
        "--review-basename",
        default="20SM_18e_specialist_mixture_review",
        help="Review basename written under 03_reviews.",
    )
    parser.add_argument("--rebuild-bundle", action="store_true", help="Force rerun even when segmented results already exist.")
    return parser


def stage20_paths(stage_root: Path) -> dict[str, Path]:
    return {
        "spec": stage_root / "00_spec" / "stage_brief.md",
        "inputs": stage_root / "01_inputs" / "input_manifest.json",
        "review_index": stage_root / "03_reviews" / "review_index.md",
        "selection": stage_root / "04_selected" / "selection_status.md",
    }


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def source_reference_run_name(window_token: str) -> str:
    return f"18E_{window_token}_17e_ph20_0001"


def build_candidates() -> list[MixtureSpec]:
    return [
        MixtureSpec(
            stage_id="20A",
            base_name="ref_17e_ph20",
            label="18E_reference",
            rationale="Exact 18E reference so the mixture family is ranked against the current practical operating leader.",
            model_kind="reference",
            component_ids=("17E",),
            voter_weights=(1.0,),
            runtime_extra=dict(PH20_OVERLAY),
        ),
        MixtureSpec(
            stage_id="20B",
            base_name="ref_17c_bd20",
            label="17C_balanced_micro_reference",
            rationale="18J-style practical short specialist reference with the balanced-micro operating overlay.",
            model_kind="reference",
            component_ids=("17C",),
            voter_weights=(1.0,),
            runtime_extra=dict(BD20_OVERLAY),
        ),
        MixtureSpec(
            stage_id="20C",
            base_name="ref_17c_ph20",
            label="17C_postcash_hold_cut_reference",
            rationale="18K-style practical short specialist reference with the post-cash hold-cut operating overlay.",
            model_kind="reference",
            component_ids=("17C",),
            voter_weights=(1.0,),
            runtime_extra=dict(PH20_OVERLAY),
        ),
        MixtureSpec(
            stage_id="20D",
            base_name="vote_e85_c15_ph20",
            label="17E_17C_vote_85_15_ph20",
            rationale="Conservative soft mixture that keeps 17E dominant while letting 17C nudge short probabilities in bad regimes.",
            model_kind="vote",
            component_ids=("17E", "17C"),
            voter_weights=(0.85, 0.15),
            runtime_extra=dict(PH20_OVERLAY),
        ),
        MixtureSpec(
            stage_id="20E",
            base_name="vote_e80_c20_ph20",
            label="17E_17C_vote_80_20_ph20",
            rationale="Mid-strength specialist blend under the proven 18E operating overlay.",
            model_kind="vote",
            component_ids=("17E", "17C"),
            voter_weights=(0.80, 0.20),
            runtime_extra=dict(PH20_OVERLAY),
        ),
        MixtureSpec(
            stage_id="20F",
            base_name="vote_e75_c25_ph20",
            label="17E_17C_vote_75_25_ph20",
            rationale="More aggressive specialist share to test whether 2407-like windows need a stronger short-specialist contribution.",
            model_kind="vote",
            component_ids=("17E", "17C"),
            voter_weights=(0.75, 0.25),
            runtime_extra=dict(PH20_OVERLAY),
        ),
        MixtureSpec(
            stage_id="20G",
            base_name="vote_e80_c20_bd20",
            label="17E_17C_vote_80_20_bd20",
            rationale="Blend the robust core with the short specialist while switching to the balanced-micro operating overlay used by 18J.",
            model_kind="vote",
            component_ids=("17E", "17C"),
            voter_weights=(0.80, 0.20),
            runtime_extra=dict(BD20_OVERLAY),
        ),
        MixtureSpec(
            stage_id="20H",
            base_name="vote_e75_c25_bd20",
            label="17E_17C_vote_75_25_bd20",
            rationale="Stronger specialist blend under the balanced-micro operating overlay to see whether the practical defender and the model-side specialist reinforce each other.",
            model_kind="vote",
            component_ids=("17E", "17C"),
            voter_weights=(0.75, 0.25),
            runtime_extra=dict(BD20_OVERLAY),
        ),
        MixtureSpec(
            stage_id="20I",
            base_name="vote_e75_c20_d05_ph20",
            label="17E_17C_17D_vote_75_20_05_ph20",
            rationale="Three-way mixture that keeps 17E as the core, adds 17C short specialization, and lets 17D contribute a small abstention bias.",
            model_kind="vote",
            component_ids=("17E", "17C", "17D"),
            voter_weights=(0.75, 0.20, 0.05),
            runtime_extra=dict(PH20_OVERLAY),
        ),
        MixtureSpec(
            stage_id="20J",
            base_name="vote_e70_c20_d10_bd20",
            label="17E_17C_17D_vote_70_20_10_bd20",
            rationale="Broader mixture with a slightly larger flat-guard share under the balanced-micro overlay for a more defensive practical fork.",
            model_kind="vote",
            component_ids=("17E", "17C", "17D"),
            voter_weights=(0.70, 0.20, 0.10),
            runtime_extra=dict(BD20_OVERLAY),
        ),
    ]


def ensure_stage_scaffold(stage_root: Path, paths: dict[str, Path], args: argparse.Namespace, candidates: list[MixtureSpec]) -> None:
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
                    "- stage: `20_18e_specialist_mixture`",
                    "- goal: `test whether 18E can be improved by mixing in the 17C short specialist (and optionally 17D flat guard) instead of more recency weighting`",
                    "- source operating reference: `18E = 17E + PH20`",
                    "- windows: `2401, 2407, 2501`",
                    "- target segment: `2407 / holdout_b`",
                    "- ranking basis: `positive_test_windows -> positive_holdout_b_windows -> avg_test_return -> min_holdout_b -> target_holdout_b -> avg_test_pf`",
                    "- candidate matrix: `18E ref, 17C practical refs, 17E+17C soft vote, 17E+17C+17D tri-vote`",
                    "- operating overlays: `PH20, BD20`",
                    "",
                ]
            ),
        )

    manifest = {
        "generated_at_utc": utc_now_iso(),
        "stage": "20_18e_specialist_mixture",
        "phase": args.batch_id,
        "dataset_path": str(Path(args.dataset_path).resolve()),
        "model_config_path": str(Path(args.model_config_path).resolve()),
        "rule_stack_path": str(Path(args.rule_stack_path).resolve()),
        "source_root": str(Path(args.source_root).resolve()),
        "source_reference_stage_id": SOURCE_REFERENCE_STAGE_ID,
        "source_reference_label": SOURCE_REFERENCE_LABEL,
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
                "source_reference_run_name": source_reference_run_name(token),
            }
            for token, train_start, train_end, validation_end, test_end in WINDOW_SPECS
        ],
        "candidates": [
            {
                "stage_id": spec.stage_id,
                "label": spec.label,
                "rationale": spec.rationale,
                "model_kind": spec.model_kind,
                "component_ids": list(spec.component_ids),
                "voter_weights": list(spec.voter_weights),
                "runtime_extra": dict(spec.runtime_extra),
            }
            for spec in candidates
        ],
    }
    write_json(paths["inputs"], manifest)

    if not paths["review_index"].exists():
        write_text(paths["review_index"], "# Review Index\n\n## Current Entries\n\n- `20SM`: pending\n")

    if not paths["selection"].exists():
        write_text(
            paths["selection"],
            "\n".join(
                [
                    "# Selection Status",
                    "",
                    "- stage: `20_18e_specialist_mixture`",
                    "- status: `running`",
                    "- active operating reference: `18E` `17E + PH20`",
                    "- objective: `test whether model-side specialist mixtures improve 18E more than recent-regime weighting did`",
                    "",
                ]
            ),
        )


def window_run_name(spec: MixtureSpec, window_token: str) -> str:
    return f"{spec.stage_id}_{window_token}_{spec.base_name}_0001"


def build_component_classifier(component: DirectionalComponent, random_state: int) -> object:
    if component.classifier_kind == "multinomial":
        return LogisticRegression(
            solver="lbfgs",
            C=component.c_value,
            class_weight=component.class_weight,
            max_iter=2500,
            random_state=random_state,
        )
    if component.classifier_kind == "ovr":
        return OneVsRestClassifier(
            LogisticRegression(
                solver="lbfgs",
                C=component.c_value,
                class_weight=component.class_weight,
                max_iter=2500,
                random_state=random_state,
            )
        )
    raise ValueError(f"unsupported classifier kind: {component.classifier_kind}")


def build_component_estimator(
    component_id: str,
    active_features: list[str],
    random_state: int,
    replacement_component_groups: dict[str, list[str]],
) -> object:
    component = COMPONENTS[component_id]
    return build_trend_proxy_linear_pipeline(
        active_features,
        random_state,
        replacement_component_groups,
        build_component_classifier(component, random_state),
    )


def fit_mixture_model(
    train_df: pd.DataFrame,
    active_features: list[str],
    random_state: int,
    replacement_component_groups: dict[str, list[str]],
    spec: MixtureSpec,
) -> object:
    x_train = train_df[active_features]
    y_train = train_df["label"]
    if spec.model_kind == "reference":
        model = build_component_estimator(spec.component_ids[0], active_features, random_state, replacement_component_groups)
        model.fit(x_train, y_train)
        return model

    estimators = []
    for component_id in spec.component_ids:
        estimators.append(
            (
                component_id.lower(),
                build_component_estimator(component_id, active_features, random_state, replacement_component_groups),
            )
        )
    model = VotingClassifier(
        estimators=estimators,
        voting="soft",
        weights=np.asarray(spec.voter_weights, dtype=np.float64),
        flatten_transform=False,
    )
    model.fit(x_train, y_train)
    return model


def build_candidate_config(
    base_config: dict[str, Any],
    *,
    spec: MixtureSpec,
    window_token: str,
    source_reference_run: str,
    split_boundaries: SplitBoundaries,
    train_df: pd.DataFrame,
    validation_df: pd.DataFrame,
    test_df: pd.DataFrame,
) -> dict[str, Any]:
    payload = dict(base_config)
    payload.update(
        {
            "run_name": window_run_name(spec, window_token),
            "phase": "stage20_18e_specialist_mixture",
            "generated_at_utc": utc_now_iso(),
            "refit_policy": "strict_wfo_train_only_then_mt5_validation_test",
            "source_reference_run_name": source_reference_run,
            "operating_reference_run_name": source_reference_run,
            "model_family": "directional_specialist_voter" if spec.model_kind == "vote" else "trend_proxy_sector_logreg",
            "specialist_mixture": {
                "stage_id": spec.stage_id,
                "label": spec.label,
                "rationale": spec.rationale,
                "model_kind": spec.model_kind,
                "component_ids": list(spec.component_ids),
                "voter_weights": list(spec.voter_weights),
            },
            "overlay_reference": dict(spec.runtime_extra),
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
        stage_name="18e_specialist_mixture",
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
    spec: MixtureSpec,
    source_payload: dict[str, Any],
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

    def metric_delta(split_name: str, layer: str, metric_name: str) -> float:
        new_value = bundle.results.by_split[split_name].model_dump()[layer].get(metric_name) or 0.0
        base_value = source_payload["split_runs"][split_name][layer].get(metric_name) or 0.0
        return float(new_value - base_value)

    def segment_delta(split_name: str, segment_name: str, metric_name: str) -> float:
        new_value = segment_metric({"segmented_results": segmented_results}, split_name, segment_name, metric_name)
        base_value = segment_metric(source_payload, split_name, segment_name, metric_name)
        return float(new_value - base_value)

    return {
        "generated_at_utc": utc_now_iso(),
        "stage": "20_18e_specialist_mixture",
        "phase": "20SM_18e_specialist_mixture",
        "run_name": window_run_name(spec, window_token),
        "candidate_stage_id": spec.stage_id,
        "candidate_label": spec.label,
        "window_token": window_token,
        "source_reference_stage_id": SOURCE_REFERENCE_STAGE_ID,
        "source_reference_label": SOURCE_REFERENCE_LABEL,
        "source_reference_run_name": source_payload["run_name"],
        "specialist_mixture": {
            "label": spec.label,
            "rationale": spec.rationale,
            "model_kind": spec.model_kind,
            "component_ids": list(spec.component_ids),
            "voter_weights": list(spec.voter_weights),
        },
        "overlay": {
            "risk_pct": bundle.runtime_snapshot.risk_pct,
            "stop_execution_mode": bundle.runtime_snapshot.stop_execution_mode,
            "stop_policy": bundle.runtime_snapshot.stop_policy,
            "stop_long_atr_mult": bundle.runtime_snapshot.stop_long_atr_mult,
            "stop_short_atr_mult": bundle.runtime_snapshot.stop_short_atr_mult,
            "stop_atr_period": bundle.runtime_snapshot.stop_atr_period,
            **spec.runtime_extra,
        },
        "split_boundaries": split_boundaries.model_dump(),
        "offline_metrics": offline_metrics,
        "source_split_runs": source_payload["split_runs"],
        "split_runs": {
            "validation": bundle.results.by_split["validation"].model_dump(),
            "test": bundle.results.by_split["test"].model_dump(),
        },
        "segmented_results": segmented_results,
        "cross_segment_summary": build_cross_segment_summary(segmented_results),
        "delta_vs_18e": {
            "validation": {
                "return_pct": metric_delta("validation", "headline", "return_pct"),
                "profit_factor": metric_delta("validation", "headline", "profit_factor"),
                "max_dd_pct": metric_delta("validation", "headline", "max_dd_pct"),
                "ulcer_index": metric_delta("validation", "risk", "ulcer_index"),
                "validation_q2_return_pct": segment_delta("validation", "validation_q2", "return_pct"),
            },
            "test": {
                "return_pct": metric_delta("test", "headline", "return_pct"),
                "profit_factor": metric_delta("test", "headline", "profit_factor"),
                "max_dd_pct": metric_delta("test", "headline", "max_dd_pct"),
                "ulcer_index": metric_delta("test", "risk", "ulcer_index"),
                "holdout_b_return_pct": segment_delta("test", "holdout_b", "return_pct"),
            },
        },
    }


def segment_metric(payload: dict[str, Any], split_name: str, segment_name: str, metric_name: str) -> float:
    segments = payload["segmented_results"][split_name]["segments"]
    segment = next(item for item in segments if str(item.get("segment") or "") == segment_name)
    return float(segment["headline"].get(metric_name) or 0.0)


def aggregate_candidates(payloads: list[dict[str, Any]], candidates: list[MixtureSpec]) -> list[dict[str, Any]]:
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
        test_deltas = [float(run["delta_vs_18e"]["test"]["return_pct"]) for run in runs]
        holdout_b_deltas = [float(run["delta_vs_18e"]["test"]["holdout_b_return_pct"]) for run in runs]
        target_run = next(run for run in runs if run["window_token"] == TARGET_WINDOW_TOKEN)
        rows.append(
            {
                "candidate_stage_id": stage_id,
                "candidate_label": spec.label,
                "rationale": spec.rationale,
                "model_kind": spec.model_kind,
                "component_ids": list(spec.component_ids),
                "voter_weights": list(spec.voter_weights),
                "avg_test_return_pct": float(np.mean(test_returns)),
                "min_test_return_pct": float(np.min(test_returns)),
                "avg_test_profit_factor": float(np.mean(test_pfs)),
                "avg_holdout_b_return_pct": float(np.mean(holdout_b_returns)),
                "min_holdout_b_return_pct": float(np.min(holdout_b_returns)),
                "target_window_test_return_pct": float(target_run["split_runs"]["test"]["headline"].get("return_pct") or 0.0),
                "target_window_test_profit_factor": float(target_run["split_runs"]["test"]["headline"].get("profit_factor") or 0.0),
                "target_holdout_b_return_pct": segment_metric(target_run, "test", TARGET_SEGMENT, "return_pct"),
                "target_holdout_b_profit_factor": segment_metric(target_run, "test", TARGET_SEGMENT, "profit_factor"),
                "avg_test_delta_vs_18e_return_pct": float(np.mean(test_deltas)),
                "avg_holdout_b_delta_vs_18e_return_pct": float(np.mean(holdout_b_deltas)),
                "target_holdout_b_delta_vs_18e_return_pct": float(target_run["delta_vs_18e"]["test"]["holdout_b_return_pct"]),
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
                        "test_delta_return_pct": float(run["delta_vs_18e"]["test"]["return_pct"]),
                        "holdout_b_delta_return_pct": float(run["delta_vs_18e"]["test"]["holdout_b_return_pct"]),
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
            float(row["target_holdout_b_return_pct"]),
            float(row["avg_test_profit_factor"]),
        ),
        reverse=True,
    )
    for rank, row in enumerate(rows, start=1):
        row["rank"] = rank
    return rows


def build_review_markdown(rows: list[dict[str, Any]], payloads: list[dict[str, Any]]) -> str:
    lines = [
        "# Stage 20 18E Specialist Mixture Review",
        "",
        "- windows: `2401, 2407, 2501`",
        "- source operating reference: `18E = 17E + PH20`",
        "- target: `2407 / holdout_b`",
        "- ranking basis: `positive_test_windows -> positive_holdout_b_windows -> avg_test_return -> min_holdout_b -> target_holdout_b -> avg_test_pf`",
        "",
        "## Candidate Ranking",
        "",
    ]
    for row in rows:
        lines.append(
            f"- [{row['rank']}] `{row['candidate_stage_id']}` `{row['candidate_label']}`: "
            f"avg_test=`{format_metric(row['avg_test_return_pct'], 3)}`, "
            f"avg_test_delta_vs_18E=`{format_metric(row['avg_test_delta_vs_18e_return_pct'], 3)}`, "
            f"target_holdout_b=`{format_metric(row['target_holdout_b_return_pct'], 3)}`, "
            f"target_holdout_b_delta_vs_18E=`{format_metric(row['target_holdout_b_delta_vs_18e_return_pct'], 3)}`, "
            f"min_holdout_b=`{format_metric(row['min_holdout_b_return_pct'], 3)}`, "
            f"positive_test_windows=`{row['positive_test_windows']}/3`, "
            f"positive_holdout_b_windows=`{row['positive_holdout_b_windows']}/3`"
        )
        lines.append(f"  - rationale: `{row['rationale']}`")
        lines.append(
            f"  - components: `{', '.join(row['component_ids'])}` / weights=`{', '.join(f'{weight:.2f}' for weight in row['voter_weights'])}`"
        )
        for window_row in row["per_window"]:
            lines.append(
                f"  - `{window_row['window_token']}`: validation=`{format_metric(window_row['validation_return_pct'], 3)}`, "
                f"test=`{format_metric(window_row['test_return_pct'], 3)}`, PF=`{format_metric(window_row['test_profit_factor'], 4)}`, "
                f"holdout_b=`{format_metric(window_row['holdout_b_return_pct'], 3)}`, holdout_b_PF=`{format_metric(window_row['holdout_b_profit_factor'], 4)}`, "
                f"test_delta_vs_18E=`{format_metric(window_row['test_delta_return_pct'], 3)}`, "
                f"holdout_b_delta_vs_18E=`{format_metric(window_row['holdout_b_delta_return_pct'], 3)}`"
            )
        lines.append("")

    if rows:
        leader = rows[0]
        lines.extend(
            [
                "## Readout",
                "",
                f"- specialist-mixture leader: `{leader['candidate_stage_id']}` `{leader['candidate_label']}`",
                f"- leader avg test return: `{format_metric(leader['avg_test_return_pct'], 3)}`",
                f"- leader avg delta vs 18E: `{format_metric(leader['avg_test_delta_vs_18e_return_pct'], 3)}`",
                f"- leader target 2407 holdout_b: `{format_metric(leader['target_holdout_b_return_pct'], 3)}`",
                f"- leader target holdout_b delta vs 18E: `{format_metric(leader['target_holdout_b_delta_vs_18e_return_pct'], 3)}`",
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
    entry = f"- `20SM`: see `{review_name}`"
    if entry not in lines:
        lines.append(entry)
    write_text(review_index_path, "\n".join(lines).rstrip() + "\n")


def update_selection_status(selection_path: Path, leader: dict[str, Any]) -> None:
    lines = [
        "# Selection Status",
        "",
        "- stage: `20_18e_specialist_mixture`",
        "- status: `completed`",
        f"- specialist-mixture leader: `{leader['candidate_stage_id']}` `{leader['candidate_label']}`",
        f"- source operating reference: `{SOURCE_REFERENCE_STAGE_ID}` `{SOURCE_REFERENCE_LABEL}`",
        f"- leader basis: `positive_test_windows={leader['positive_test_windows']}/3, positive_holdout_b_windows={leader['positive_holdout_b_windows']}/3, avg_test_return={format_metric(leader['avg_test_return_pct'], 3)}, avg_test_delta_vs_18E={format_metric(leader['avg_test_delta_vs_18e_return_pct'], 3)}, min_holdout_b={format_metric(leader['min_holdout_b_return_pct'], 3)}, target_2407_holdout_b={format_metric(leader['target_holdout_b_return_pct'], 3)}`",
        "- next action: `decide whether the leader is strong enough to replace 18E as the practical operating reference, or whether 18E should stay the core with the new mixture kept as a challenger`",
        "",
    ]
    write_text(selection_path, "\n".join(lines))


def main() -> int:
    args = build_parser().parse_args()

    stage_root = Path(args.stage_root).resolve()
    source_root = Path(args.source_root).resolve()
    dataset_path = Path(args.dataset_path).resolve()
    model_config_path = Path(args.model_config_path).resolve()
    rule_stack_path = Path(args.rule_stack_path).resolve()
    paths = stage20_paths(stage_root)
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
        source_payload_path = source_root / source_reference_run_name(window_token) / "segmented_results.json"
        if not source_payload_path.exists():
            raise FileNotFoundError(f"missing source reference payload: {source_payload_path}")
        source_payload = load_json(source_payload_path)

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

            model = fit_mixture_model(
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

            joblib.dump(model, run_dir / "model.joblib")
            validation_predictions.to_parquet(run_dir / "validation_predictions.parquet", index=False)
            test_predictions.to_parquet(run_dir / "test_predictions.parquet", index=False)
            write_json(run_dir / "rule_stack.json", base_rule_stack)
            write_json(
                run_dir / "candidate_manifest.json",
                {
                    "generated_at_utc": utc_now_iso(),
                    "stage": "20_18e_specialist_mixture",
                    "window_token": window_token,
                    "stage_id": spec.stage_id,
                    "run_name": window_run_name(spec, window_token),
                    "candidate_label": spec.label,
                    "rationale": spec.rationale,
                    "model_kind": spec.model_kind,
                    "component_ids": list(spec.component_ids),
                    "voter_weights": list(spec.voter_weights),
                    "runtime_extra": dict(spec.runtime_extra),
                    "source_reference_run_name": source_payload["run_name"],
                },
            )
            write_json(
                run_dir / "config.json",
                build_candidate_config(
                    base_config,
                    spec=spec,
                    window_token=window_token,
                    source_reference_run=source_payload["run_name"],
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
                split_counts={"train": int(len(train_df)), "validation": int(len(validation_df)), "test": int(len(test_df))},
                runtime_extra={
                    "wfo_mode": "strict_retrain",
                    "window_token": window_token,
                    "candidate_stage_id": spec.stage_id,
                    "candidate_label": spec.label,
                    "source_reference_stage_id": SOURCE_REFERENCE_STAGE_ID,
                    "source_reference_run_name": source_payload["run_name"],
                    "specialist_mixture_label": spec.label,
                    **spec.runtime_extra,
                },
                wfo_metadata={
                    "wfo_window_name": window_token,
                    "wfo_phase": "20SM_18e_specialist_mixture",
                    "candidate_stage_id": spec.stage_id,
                    "candidate_label": spec.label,
                    "source_reference_run_name": source_payload["run_name"],
                },
            )

            run_tester(bundle_path, "validation")
            run_tester(bundle_path, "test")

            payload = build_run_payload(
                run_dir=run_dir,
                spec=spec,
                source_payload=source_payload,
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
        "stage": "20_18e_specialist_mixture",
        "phase": "20SM_18e_specialist_mixture",
        "source_reference_stage_id": SOURCE_REFERENCE_STAGE_ID,
        "source_reference_label": SOURCE_REFERENCE_LABEL,
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
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
