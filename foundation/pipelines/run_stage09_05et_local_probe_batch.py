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

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from foundation.pipelines.experiment_bundle_models import ExperimentBundle, SplitBoundaries
from foundation.pipelines.export_experiment_bundle_assets import run_export_bundle_assets
from foundation.pipelines.run_stage05_mt5_model_family_trial import class_counts, fit_trend_proxy_sector_logreg
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
    DEFAULT_DATASET_PATH,
    DEFAULT_MODEL_CONFIG_PATH,
    evaluate_split,
    parse_utc,
    patch_bundle,
    prepare_run_dir,
    split_dataset,
    wfo_segment_scheme,
)
from foundation.pipelines.run_stage06_pre_risk_pool_batch import run_tester


STAGE09_ROOT = ROOT_DIR / "stages" / "09_05et_local_probe"
BASE_RULE_STACK_PATH = (
    ROOT_DIR
    / "stages"
    / "05_optimization"
    / "02_runs"
    / "active"
    / "05ET_05dp_stronger_long_suppression_hold4_0001"
    / "rule_stack.json"
)

WINDOW_SPECS = [
    ("2401", "2022-09-01T00:00:00Z", "2024-01-01T00:00:00Z", "2024-10-01T00:00:00Z", "2025-03-01T00:00:00Z"),
    ("2407", "2022-09-01T00:00:00Z", "2024-07-01T00:00:00Z", "2025-04-01T00:00:00Z", "2025-09-01T00:00:00Z"),
    ("2501", "2022-09-01T00:00:00Z", "2025-01-01T00:00:00Z", "2025-10-01T00:00:00Z", "2026-03-01T00:00:00Z"),
]

TARGET_WINDOW_TOKEN = "2407"
TARGET_SEGMENT = "holdout_b"


@dataclass(frozen=True)
class ProbeSpec:
    stage_id: str
    base_name: str
    label: str
    short_threshold: float
    long_threshold: float
    min_margin: float
    max_hold_bars: int
    core_reference_run_name: str = "05ET_05dp_stronger_long_suppression_hold4_0001"
    standard_reference_run_name: str = "05ET_05dp_stronger_long_suppression_hold4_0001"
    motif_source_run_name: str | None = None


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run a narrow strict-retrain WFO local probe around 05ET to improve the 2407 holdout_b segment."
    )
    parser.add_argument("--stage-root", default=str(STAGE09_ROOT), help="Stage 09 root directory.")
    parser.add_argument("--dataset-path", default=str(DEFAULT_DATASET_PATH), help="Shared dataset parquet.")
    parser.add_argument("--model-config-path", default=str(DEFAULT_MODEL_CONFIG_PATH), help="Source model config path.")
    parser.add_argument("--batch-id", default="09LP", help="Stage 09 batch id.")
    parser.add_argument("--random-state", type=int, default=42, help="Random seed for retraining.")
    parser.add_argument("--risk-pct", type=float, default=2.0, help="Risk percent for the MT5 overlay.")
    parser.add_argument("--stop-atr-period", type=int, default=14, help="ATR period.")
    parser.add_argument("--stop-long-atr-mult", type=float, default=1.4, help="Long ATR multiplier.")
    parser.add_argument("--stop-short-atr-mult", type=float, default=2.0, help="Short ATR multiplier.")
    parser.add_argument(
        "--review-basename",
        default="09LP_05et_local_probe_review",
        help="Review basename written under 03_reviews.",
    )
    parser.add_argument("--rebuild-bundle", action="store_true", help="Force rerun even when segmented results already exist.")
    return parser


def stage09_paths(stage_root: Path) -> dict[str, Path]:
    return {
        "spec": stage_root / "00_spec" / "stage_brief.md",
        "inputs": stage_root / "01_inputs" / "input_manifest.json",
        "review_index": stage_root / "03_reviews" / "review_index.md",
        "selection": stage_root / "04_selected" / "selection_status.md",
    }


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def build_candidates() -> list[ProbeSpec]:
    return [
        ProbeSpec("09A", "05et_base", "05ET_base_t30_l50_m0675_h4", 0.30, 0.50, 0.0675, 4),
        ProbeSpec("09B", "05et_short325", "05ET_short325_t325_l50_m0675_h4", 0.325, 0.50, 0.0675, 4),
        ProbeSpec("09C", "05et_margin0700", "05ET_margin0700_t30_l50_m0700_h4", 0.30, 0.50, 0.0700, 4),
        ProbeSpec("09D", "05et_hold3", "05ET_hold3_t30_l50_m0675_h3", 0.30, 0.50, 0.0675, 3),
        ProbeSpec("09E", "05et_short325_margin0700", "05ET_short325_t325_l50_m0700_h4", 0.325, 0.50, 0.0700, 4),
        ProbeSpec("09F", "05et_short325_hold3", "05ET_short325_t325_l50_m0675_h3", 0.325, 0.50, 0.0675, 3),
        ProbeSpec("09G", "05et_long525_margin0700", "05ET_long525_t30_l525_m0700_h4", 0.30, 0.525, 0.0700, 4),
        ProbeSpec("09H", "05et_all_tight", "05ET_short325_long525_m0700_h3", 0.325, 0.525, 0.0700, 3),
    ]


def ensure_stage_scaffold(stage_root: Path, paths: dict[str, Path], args: argparse.Namespace, candidates: list[ProbeSpec]) -> None:
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
                    "- stage: `09_05et_local_probe`",
                    "- goal: `run a narrow strict-retrain WFO local probe around 05ET to improve the 2407 holdout_b segment`",
                    "- windows: `2401, 2407, 2501`",
                    "- target segment: `2407 / holdout_b`",
                    "- local probe axes: `short_threshold, long_threshold, min_margin, max_hold_bars`",
                    "- ranking focus: `2407 holdout_b first, then worst holdout_b, then average test return`",
                    "",
                ]
            ),
        )

    manifest = {
        "generated_at_utc": utc_now_iso(),
        "stage": "09_05et_local_probe",
        "phase": args.batch_id,
        "dataset_path": str(Path(args.dataset_path).resolve()),
        "model_config_path": str(Path(args.model_config_path).resolve()),
        "core_reference_run_name": "05ET_05dp_stronger_long_suppression_hold4_0001",
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
                "short_threshold": spec.short_threshold,
                "long_threshold": spec.long_threshold,
                "min_margin": spec.min_margin,
                "max_hold_bars": spec.max_hold_bars,
            }
            for spec in candidates
        ],
    }
    write_json(paths["inputs"], manifest)

    if not paths["review_index"].exists():
        write_text(paths["review_index"], "# Review Index\n\n## Current Entries\n\n- `09LP`: pending\n")

    if not paths["selection"].exists():
        write_text(
            paths["selection"],
            "\n".join(
                [
                    "# Selection Status",
                    "",
                    "- stage: `09_05et_local_probe`",
                    "- status: `running`",
                    "- active core: `05ET_05dp_stronger_long_suppression_hold4_0001`",
                    "- objective: `improve 2407 holdout_b without losing broad strict-WFO robustness`",
                    "",
                ]
            ),
        )


def window_run_name(spec: ProbeSpec, window_token: str) -> str:
    return f"{spec.stage_id}_{window_token}_{spec.base_name}_0001"


def build_rule_stack(spec: ProbeSpec) -> dict[str, Any]:
    rule_stack = load_json(BASE_RULE_STACK_PATH)
    rule_stack["entry"][0]["params"]["short_threshold"] = spec.short_threshold
    rule_stack["entry"][0]["params"]["long_threshold"] = spec.long_threshold
    rule_stack["filters"][0]["params"]["min_margin"] = spec.min_margin
    rule_stack["exit"][0]["params"]["max_hold_bars"] = spec.max_hold_bars
    return rule_stack


def build_candidate_config(
    base_config: dict[str, Any],
    *,
    spec: ProbeSpec,
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
            "phase": "stage09_05et_local_probe",
            "generated_at_utc": utc_now_iso(),
            "refit_policy": "strict_wfo_train_only_then_mt5_validation_test",
            "logic_reference_run_name": spec.core_reference_run_name,
            "core_reference_run_name": spec.core_reference_run_name,
            "standard_reference_run_name": spec.standard_reference_run_name,
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
            "logic_probe": {
                "short_threshold": spec.short_threshold,
                "long_threshold": spec.long_threshold,
                "min_margin": spec.min_margin,
                "max_hold_bars": spec.max_hold_bars,
            },
        }
    )
    return payload


def export_bundle_for_run(*, run_dir: Path, spec: ProbeSpec, args: argparse.Namespace) -> Path:
    export_args = argparse.Namespace(
        run_dir=str(run_dir),
        experiment_id=f"exp_{Path(run_dir).name.lower()}_v1",
        stage_id=spec.stage_id,
        output_dir=str(run_dir),
        stage_name="05et_local_probe",
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
        max_hold_bars=spec.max_hold_bars,
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
    spec: ProbeSpec,
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
        "stage": "09_05et_local_probe",
        "phase": "09LP_05et_local_probe",
        "run_name": window_run_name(spec, window_token),
        "candidate_stage_id": spec.stage_id,
        "candidate_label": spec.label,
        "core_reference_run_name": spec.core_reference_run_name,
        "standard_reference_run_name": spec.standard_reference_run_name,
        "window_token": window_token,
        "split_boundaries": split_boundaries.model_dump(),
        "logic_probe": {
            "short_threshold": spec.short_threshold,
            "long_threshold": spec.long_threshold,
            "min_margin": spec.min_margin,
            "max_hold_bars": spec.max_hold_bars,
        },
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


def aggregate_candidates(payloads: list[dict[str, Any]], candidates: list[ProbeSpec]) -> list[dict[str, Any]]:
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
                "logic_probe": {
                    "short_threshold": spec.short_threshold,
                    "long_threshold": spec.long_threshold,
                    "min_margin": spec.min_margin,
                    "max_hold_bars": spec.max_hold_bars,
                },
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
            float(row["target_holdout_b_return_pct"]),
            float(row["min_holdout_b_return_pct"]),
            float(row["avg_test_return_pct"]),
            float(row["avg_test_profit_factor"]),
        ),
        reverse=True,
    )
    for rank, row in enumerate(rows, start=1):
        row["rank"] = rank
    return rows


def build_review_markdown(rows: list[dict[str, Any]], payloads: list[dict[str, Any]]) -> str:
    lines = [
        "# Stage 09 05ET Local Probe Review",
        "",
        "- windows: `2401, 2407, 2501`",
        "- target: `2407 / holdout_b`",
        "- ranking basis: `2407 holdout_b return_pct -> min holdout_b return_pct -> avg test return_pct -> avg test PF`",
        "",
        "## Candidate Ranking",
        "",
    ]
    for row in rows:
        probe = row["logic_probe"]
        lines.append(
            f"- [{row['rank']}] `{row['candidate_stage_id']}` `{row['candidate_label']}`: "
            f"Ts=`{probe['short_threshold']:.3f}`, Tl=`{probe['long_threshold']:.3f}`, "
            f"margin=`{probe['min_margin']:.4f}`, hold=`{probe['max_hold_bars']}`, "
            f"target_holdout_b=`{format_metric(row['target_holdout_b_return_pct'], 3)}`, "
            f"target_holdout_b_PF=`{format_metric(row['target_holdout_b_profit_factor'], 4)}`, "
            f"min_holdout_b=`{format_metric(row['min_holdout_b_return_pct'], 3)}`, "
            f"avg_test=`{format_metric(row['avg_test_return_pct'], 3)}`, "
            f"positive_test_windows=`{row['positive_test_windows']}/3`, positive_holdout_b_windows=`{row['positive_holdout_b_windows']}/3`"
        )
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
                f"- probe leader: `{leader['candidate_stage_id']}` `{leader['candidate_label']}`",
                f"- target 2407 holdout_b: `{format_metric(leader['target_holdout_b_return_pct'], 3)}`",
                f"- min holdout_b: `{format_metric(leader['min_holdout_b_return_pct'], 3)}`",
                f"- avg test return: `{format_metric(leader['avg_test_return_pct'], 3)}`",
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
    entry = f"- `09LP`: see `{review_name}`"
    if entry not in lines:
        lines.append(entry)
    write_text(review_index_path, "\n".join(lines).rstrip() + "\n")


def update_selection_status(selection_path: Path, leader: dict[str, Any]) -> None:
    probe = leader["logic_probe"]
    lines = [
        "# Selection Status",
        "",
        "- stage: `09_05et_local_probe`",
        "- status: `completed`",
        f"- probe leader: `{leader['candidate_stage_id']}` `{leader['candidate_label']}`",
        f"- leader params: `Ts={probe['short_threshold']:.3f}, Tl={probe['long_threshold']:.3f}, margin={probe['min_margin']:.4f}, hold={probe['max_hold_bars']}`",
        f"- leader basis: `2407_holdout_b={format_metric(leader['target_holdout_b_return_pct'], 3)}, min_holdout_b={format_metric(leader['min_holdout_b_return_pct'], 3)}, avg_test_return={format_metric(leader['avg_test_return_pct'], 3)}`",
        "- next action: `decide whether this 05ET local-probe leader is strong enough to replace the plain 05ET core in the next strict-WFO gate`",
        "",
    ]
    write_text(selection_path, "\n".join(lines))


def main() -> int:
    args = build_parser().parse_args()

    stage_root = Path(args.stage_root).resolve()
    dataset_path = Path(args.dataset_path).resolve()
    model_config_path = Path(args.model_config_path).resolve()
    paths = stage09_paths(stage_root)
    candidates = build_candidates()
    ensure_stage_scaffold(stage_root, paths, args, candidates)

    dataset = pd.read_parquet(dataset_path)
    base_config = load_json(model_config_path)
    active_features = list(base_config["active_input_features"])
    replacement_component_groups = dict(base_config["replacement_sector_components"])
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

        base_model = fit_trend_proxy_sector_logreg(
            train_df,
            active_features,
            args.random_state,
            replacement_component_groups,
        )

        for spec in candidates:
            run_dir = stage_root / "02_runs" / "active" / window_run_name(spec, window_token)
            segmented_path = run_dir / "segmented_results.json"
            if segmented_path.exists() and not args.rebuild_bundle:
                payloads.append(load_json(segmented_path))
                continue

            prepare_run_dir(run_dir)
            validation_metrics, validation_predictions = evaluate_split(base_model, validation_df, active_features)
            test_metrics, test_predictions = evaluate_split(base_model, test_df, active_features)
            offline_metrics = {"validation": validation_metrics, "test": test_metrics}

            joblib.dump(copy.deepcopy(base_model), run_dir / "model.joblib")
            validation_predictions.to_parquet(run_dir / "validation_predictions.parquet", index=False)
            test_predictions.to_parquet(run_dir / "test_predictions.parquet", index=False)

            rule_stack = build_rule_stack(spec)
            write_json(run_dir / "rule_stack.json", rule_stack)
            write_json(
                run_dir / "candidate_manifest.json",
                {
                    "generated_at_utc": utc_now_iso(),
                    "stage": "09_05et_local_probe",
                    "window_token": window_token,
                    "stage_id": spec.stage_id,
                    "run_name": window_run_name(spec, window_token),
                    "candidate_label": spec.label,
                    "core_reference_run_name": spec.core_reference_run_name,
                    "short_threshold": spec.short_threshold,
                    "long_threshold": spec.long_threshold,
                    "min_margin": spec.min_margin,
                    "max_hold_bars": spec.max_hold_bars,
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
                bundle_path = export_bundle_for_run(run_dir=run_dir, spec=spec, args=args)

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
                    "wfo_phase": "09LP_05et_local_probe",
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
        "stage": "09_05et_local_probe",
        "phase": "09LP_05et_local_probe",
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
            f"[done] candidate={row['candidate_stage_id']} target_holdout_b={row['target_holdout_b_return_pct']:.3f} "
            f"min_holdout_b={row['min_holdout_b_return_pct']:.3f} avg_test={row['avg_test_return_pct']:.3f}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
