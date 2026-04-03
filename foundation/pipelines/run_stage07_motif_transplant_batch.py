#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import joblib
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, balanced_accuracy_score, f1_score, log_loss

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from foundation.pipelines.experiment_bundle_models import ExperimentBundle, SplitBoundaries
from foundation.pipelines.export_experiment_bundle_assets import run_export_bundle_assets
from foundation.pipelines.run_stage05_mt5_05dp_output_shape_batch import class_counts
from foundation.pipelines.run_stage06_direction_split_segmented_overlay import (
    build_cross_segment_summary,
    build_segment_results,
    format_metric,
    load_attempt_summaries,
    utc_now_iso,
    write_json,
    write_text,
)
from foundation.pipelines.run_stage06_multi_window_pre_risk_batch import build_segment_scheme
from foundation.pipelines.run_stage06_pre_risk_pool_batch import run_tester


STAGE07_ROOT = ROOT_DIR / "stages" / "07_motif_transplant"
DEFAULT_SOURCE_MODEL_RUN = ROOT_DIR / "stages" / "05_optimization" / "02_runs" / "active" / "05DP_05ca_margin0675_hold5_0001"
DEFAULT_DATASET_PATH = ROOT_DIR / "stages" / "01_base_feature_ml" / "01_inputs" / "stage01c_h03_band000125_dataset.parquet"


@dataclass(frozen=True)
class CoreSpec:
    stage_id: str
    run_name: str
    rule_stack_source: Path
    label: str


@dataclass(frozen=True)
class MotifSpec:
    stage_id: str
    label: str
    source_run_name: str
    temperature: float
    class_biases: tuple[float, float, float]
    rationale: str


@dataclass(frozen=True)
class CandidateSpec:
    stage_id: str
    run_name: str
    experiment_id: str
    core: CoreSpec
    motif: MotifSpec


SHIFT_WINDOW_SPECS = [
    ("2401", "2022-09-01T00:00:00Z", "2024-01-01T00:00:00Z", "2024-10-01T00:00:00Z", "2025-03-01T00:00:00Z"),
    ("2407", "2022-09-01T00:00:00Z", "2024-07-01T00:00:00Z", "2025-04-01T00:00:00Z", "2025-09-01T00:00:00Z"),
    ("2501", "2022-09-01T00:00:00Z", "2025-01-01T00:00:00Z", "2025-10-01T00:00:00Z", "2026-03-01T00:00:00Z"),
]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Build and evaluate Stage 07 motif-transplant candidates by grafting 05FD/05FF output-shape motifs onto 05ER/05EM/05ET core rule stacks."
    )
    parser.add_argument("--stage-root", default=str(STAGE07_ROOT), help="Stage 07 root directory.")
    parser.add_argument("--source-model-run-dir", default=str(DEFAULT_SOURCE_MODEL_RUN), help="Source run directory providing model.joblib/config.json.")
    parser.add_argument("--dataset-path", default=str(DEFAULT_DATASET_PATH), help="Dataset parquet used for offline metrics and shifted-window counts.")
    parser.add_argument("--risk-pct", type=float, default=2.0, help="Balance risk percent.")
    parser.add_argument("--stop-atr-period", type=int, default=14, help="ATR period.")
    parser.add_argument("--stop-long-atr-mult", type=float, default=1.4, help="Long-side ATR multiplier.")
    parser.add_argument("--stop-short-atr-mult", type=float, default=2.0, help="Short-side ATR multiplier.")
    parser.add_argument("--rebuild-bundle", action="store_true", help="Force bundle rebuild for candidate and stress runs.")
    return parser


def parse_utc(raw_value: str) -> pd.Timestamp:
    ts = pd.Timestamp(raw_value)
    if ts.tzinfo is None:
        ts = ts.tz_localize("UTC")
    else:
        ts = ts.tz_convert("UTC")
    return ts


def standard_split_boundaries() -> SplitBoundaries:
    return SplitBoundaries(
        train_start_utc="2022-09-01T00:00:00Z",
        train_end_utc_exclusive="2025-01-01T00:00:00Z",
        validation_end_utc_exclusive="2025-10-01T00:00:00Z",
        test_end_utc_exclusive="2026-03-01T00:00:00Z",
    )


def build_candidate_specs() -> list[CandidateSpec]:
    core_specs = [
        CoreSpec(
            stage_id="05ER",
            run_name="05ER_05dp_short_bias_margin_hold4_0001",
            rule_stack_source=ROOT_DIR / "stages" / "05_optimization" / "02_runs" / "active" / "05ER_05dp_short_bias_margin_hold4_0001" / "rule_stack.json",
            label="core_short_bias_hold4",
        ),
        CoreSpec(
            stage_id="05EM",
            run_name="05EM_05dp_short_bias_margin_hold5_0001",
            rule_stack_source=ROOT_DIR / "stages" / "05_optimization" / "02_runs" / "active" / "05EM_05dp_short_bias_margin_hold5_0001" / "rule_stack.json",
            label="core_short_bias_hold5",
        ),
        CoreSpec(
            stage_id="05ET",
            run_name="05ET_05dp_stronger_long_suppression_hold4_0001",
            rule_stack_source=ROOT_DIR / "stages" / "05_optimization" / "02_runs" / "active" / "05ET_05dp_stronger_long_suppression_hold4_0001" / "rule_stack.json",
            label="core_long_suppression_hold4",
        ),
    ]
    motif_specs = [
        MotifSpec(
            stage_id="05FD",
            label="flat_up_long_down_bias",
            source_run_name="05FD_05ca_flatup_longdown_margin0675_hold5_0001",
            temperature=1.0,
            class_biases=(0.0, 0.1, -0.1),
            rationale="Prefer flat over long in ambiguous zones to defend weak holdout_b style regimes.",
        ),
        MotifSpec(
            stage_id="05FF",
            label="soft_temp_short_bias_combo",
            source_run_name="05FF_05ca_temp_shortbias_0001",
            temperature=1.1,
            class_biases=(0.08, 0.0, -0.08),
            rationale="Softer logits with a mild short-vs-long tilt to defend bad middle segments without hard blocking.",
        ),
    ]
    candidate_specs: list[CandidateSpec] = []
    stage_ids = ["07A", "07B", "07C", "07D", "07E", "07F"]
    index = 0
    for core in core_specs:
        for motif in motif_specs:
            stage_id = stage_ids[index]
            suffix = "fd" if motif.stage_id == "05FD" else "ff"
            candidate_specs.append(
                CandidateSpec(
                    stage_id=stage_id,
                    run_name=f"{stage_id}_{core.stage_id.lower()}_{suffix}_motif_0001",
                    experiment_id=f"exp_{stage_id.lower()}_{core.stage_id.lower()}_{suffix}_motif_v1",
                    core=core,
                    motif=motif,
                )
            )
            index += 1
    return candidate_specs


def stage_paths(stage_root: Path) -> dict[str, Path]:
    return {
        "spec": stage_root / "00_spec" / "stage_brief.md",
        "inputs": stage_root / "01_inputs" / "input_manifest.json",
        "review_index": stage_root / "03_reviews" / "review_index.md",
        "selection": stage_root / "04_selected" / "selection_status.md",
        "review_json": stage_root / "03_reviews" / "07MT_motif_transplant_review.json",
        "review_md": stage_root / "03_reviews" / "07MT_motif_transplant_review.md",
        "stress_json": stage_root / "03_reviews" / "07MT_motif_transplant_stress_review.json",
        "stress_md": stage_root / "03_reviews" / "07MT_motif_transplant_stress_review.md",
    }


def ensure_stage_scaffold(stage_root: Path, paths: dict[str, Path], args: argparse.Namespace, candidates: list[CandidateSpec]) -> None:
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
                    "- stage: `07_motif_transplant`",
                    "- goal: `graft defender output-shape motifs from 05FD/05FF onto robust 05ER/05EM/05ET core rule stacks`",
                    "- evaluation shape: `standard Stage 06 risk overlay first, then shifted-window stress on the strongest defenders`",
                    "- frozen overlay: `risk_pct=2.00, broker_native SL, direction_split(long=1.40, short=2.00), ATR14`",
                    "- main question: `can bad-segment defense improve without sacrificing the robust core shape?`",
                    "",
                ]
            ),
        )

    manifest = {
        "generated_at_utc": utc_now_iso(),
        "stage": "07_motif_transplant",
        "phase": "07MT_motif_transplant_batch",
        "source_model_run_dir": str(Path(args.source_model_run_dir).resolve()),
        "dataset_path": str(Path(args.dataset_path).resolve()),
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
        "standard_window": standard_split_boundaries().model_dump(),
        "shift_windows": [
            {
                "token": token,
                "train_start_utc": train_start,
                "train_end_utc_exclusive": train_end,
                "validation_end_utc_exclusive": validation_end,
                "test_end_utc_exclusive": test_end,
            }
            for token, train_start, train_end, validation_end, test_end in SHIFT_WINDOW_SPECS
        ],
        "candidates": [
            {
                "stage_id": spec.stage_id,
                "run_name": spec.run_name,
                "experiment_id": spec.experiment_id,
                "core": {"stage_id": spec.core.stage_id, "run_name": spec.core.run_name},
                "motif": {
                    "stage_id": spec.motif.stage_id,
                    "label": spec.motif.label,
                    "source_run_name": spec.motif.source_run_name,
                    "temperature": spec.motif.temperature,
                    "class_biases": list(spec.motif.class_biases),
                },
            }
            for spec in candidates
        ],
    }
    write_json(paths["inputs"], manifest)

    if not paths["review_index"].exists():
        write_text(paths["review_index"], "# Review Index\n\n- `07MT`: pending\n")

    if not paths["selection"].exists():
        write_text(
            paths["selection"],
            "\n".join(
                [
                    "# Selection Status",
                    "",
                    "- stage: `07_motif_transplant`",
                    "- status: `running`",
                    "- current thesis: `transplant 05FD/05FF defender motifs onto 05ER/05EM/05ET cores under the Stage 06 risk overlay`",
                    "",
                ]
            ),
        )


def load_source_artifacts(source_model_run_dir: Path) -> tuple[dict[str, Any], Any, pd.DataFrame, list[str]]:
    config = json.loads((source_model_run_dir / "config.json").read_text(encoding="utf-8-sig"))
    dataset_path = (ROOT_DIR / config["dataset_path"]).resolve()
    dataset = pd.read_parquet(dataset_path)
    dataset["timestamp"] = pd.to_datetime(dataset["timestamp"], utc=True)
    model = joblib.load(source_model_run_dir / "model.joblib")
    active_features = list(config["active_input_features"])
    return config, model, dataset, active_features


def clone_with_motif(source_model: Any, motif: MotifSpec) -> Any:
    model = copy.deepcopy(source_model)
    classifier = model.named_steps["classifier"]
    scale_vector = np.asarray((1.0, 1.0, 1.0), dtype=np.float64) / float(motif.temperature)
    bias_vector = np.asarray(motif.class_biases, dtype=np.float64)
    classifier.coef_ = np.asarray(classifier.coef_, dtype=np.float64) * scale_vector[:, None]
    classifier.intercept_ = np.asarray(classifier.intercept_, dtype=np.float64) * scale_vector + bias_vector
    return model


def evaluate_offline(model: Any, dataset: pd.DataFrame, active_features: list[str]) -> tuple[dict[str, Any], pd.DataFrame]:
    test_df = dataset[dataset["split"].eq("test")].copy()
    y_true = test_df["label"].to_numpy(dtype=np.int64)
    y_proba = np.asarray(model.predict_proba(test_df[active_features]), dtype=np.float64)
    y_pred = np.argmax(y_proba, axis=1)
    metrics = {
        "test_rows": int(len(test_df)),
        "test_macro_f1": float(f1_score(y_true, y_pred, average="macro")),
        "test_balanced_accuracy": float(balanced_accuracy_score(y_true, y_pred)),
        "test_accuracy": float(accuracy_score(y_true, y_pred)),
        "test_log_loss": float(log_loss(y_true, y_proba, labels=[0, 1, 2])),
        "predicted_share": {
            "short": float(np.mean(y_pred == 0)),
            "flat": float(np.mean(y_pred == 1)),
            "long": float(np.mean(y_pred == 2)),
        },
    }
    out = test_df[["timestamp", "split", "forward_return", "label"]].copy()
    out = out.rename(columns={"label": "label_true"})
    out["label_pred"] = y_pred
    out["p_short"] = y_proba[:, 0]
    out["p_flat"] = y_proba[:, 1]
    out["p_long"] = y_proba[:, 2]
    return metrics, out


def build_candidate_config(source_config: dict[str, Any], spec: CandidateSpec, dataset: pd.DataFrame) -> dict[str, Any]:
    config = dict(source_config)
    config.update(
        {
            "run_name": spec.run_name,
            "phase": "stage07_motif_transplant",
            "generated_at_utc": utc_now_iso(),
            "core_reference_run_name": spec.core.run_name,
            "motif_reference_run_name": spec.motif.source_run_name,
            "motif_transform": {
                "label": spec.motif.label,
                "temperature": spec.motif.temperature,
                "class_biases": [float(value) for value in spec.motif.class_biases],
                "rationale": spec.motif.rationale,
            },
            "row_counts": {
                "train_valid": int(dataset["split"].isin(["train", "valid"]).sum()),
                "test": int(dataset["split"].eq("test").sum()),
            },
            "class_counts": {
                "train_valid": class_counts(dataset.loc[dataset["split"].isin(["train", "valid"]), "label"]),
                "test": class_counts(dataset.loc[dataset["split"].eq("test"), "label"]),
            },
        }
    )
    return config


def export_bundle(
    *,
    source_run_dir: Path,
    output_dir: Path,
    stage_id: str,
    experiment_id: str,
    rule_stack_path: Path,
    args: argparse.Namespace,
) -> Path:
    export_args = argparse.Namespace(
        run_dir=str(source_run_dir),
        experiment_id=experiment_id,
        stage_id=stage_id,
        output_dir=str(output_dir),
        stage_name="motif_transplant",
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
        max_hold_bars=5,
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
    return output_dir / "experiment_bundle.json"


def resolve_artifact_paths(bundle: ExperimentBundle, bundle_path: Path) -> None:
    for artifact in bundle.artifacts:
        path = Path(artifact.path)
        if not path.is_absolute():
            artifact.path = str((bundle_path.parent / path).resolve())


def patch_bundle_window(
    *,
    bundle_path: Path,
    split_boundaries: SplitBoundaries,
    split_counts: dict[str, int],
    window_token: str,
    candidate_spec: CandidateSpec,
) -> ExperimentBundle:
    bundle = ExperimentBundle.from_json(bundle_path.read_text(encoding="utf-8-sig"))
    resolve_artifact_paths(bundle, bundle_path)
    bundle.data_snapshot.split_boundaries = split_boundaries
    bundle.data_snapshot.split_counts = split_counts
    bundle.data_snapshot.extra.update(
        {
            "stage07_shift_window_token": window_token,
            "stage07_candidate_stage_id": candidate_spec.stage_id,
            "stage07_core_reference_run_name": candidate_spec.core.run_name,
            "stage07_motif_reference_run_name": candidate_spec.motif.source_run_name,
        }
    )
    bundle.results.by_split = {}
    bundle.results.cross_split = bundle.results.cross_split.__class__()
    bundle.results.report_refs = []
    bundle.run_attempts = []
    bundle.compatibility.bundle_integrity_hash = hashlib.sha256(bundle.canonical_core_json().encode("utf-8")).hexdigest()
    bundle_path.write_text(bundle.to_json(indent=2), encoding="utf-8")
    return bundle


def split_counts_for_window(dataset: pd.DataFrame, split_boundaries: SplitBoundaries) -> dict[str, int]:
    ts = pd.to_datetime(dataset["timestamp"], utc=True)
    valid_mask = dataset["is_feature_row_valid"].fillna(False) if "is_feature_row_valid" in dataset.columns else pd.Series(True, index=dataset.index)
    usable = dataset[valid_mask].copy()
    usable["timestamp"] = ts[valid_mask]
    train_start = parse_utc(split_boundaries.train_start_utc)
    train_end = parse_utc(split_boundaries.train_end_utc_exclusive)
    validation_end = parse_utc(split_boundaries.validation_end_utc_exclusive)
    test_end = parse_utc(split_boundaries.test_end_utc_exclusive)
    return {
        "train": int(((usable["timestamp"] >= train_start) & (usable["timestamp"] < train_end)).sum()),
        "validation": int(((usable["timestamp"] >= train_end) & (usable["timestamp"] < validation_end)).sum()),
        "test": int(((usable["timestamp"] >= validation_end) & (usable["timestamp"] < test_end)).sum()),
    }


def payload_from_run(
    *,
    run_dir: Path,
    split_boundaries: SplitBoundaries,
    segment_scheme: dict[str, list[tuple[str, Any, Any]]],
    extra: dict[str, Any],
) -> dict[str, Any]:
    bundle = ExperimentBundle.from_json((run_dir / "experiment_bundle.json").read_text(encoding="utf-8-sig"))
    summaries = load_attempt_summaries(run_dir)
    segmented_results = {
        "validation": build_segment_results(bundle, "validation", summaries["validation"], scheme=segment_scheme),
        "test": build_segment_results(bundle, "test", summaries["test"], scheme=segment_scheme),
    }
    return {
        "generated_at_utc": utc_now_iso(),
        "stage": "07_motif_transplant",
        "run_name": run_dir.name,
        "split_boundaries": split_boundaries.model_dump(),
        "overlay": {
            "risk_pct": bundle.runtime_snapshot.risk_pct,
            "stop_execution_mode": bundle.runtime_snapshot.stop_execution_mode,
            "stop_policy": bundle.runtime_snapshot.stop_policy,
            "stop_long_atr_mult": bundle.runtime_snapshot.stop_long_atr_mult,
            "stop_short_atr_mult": bundle.runtime_snapshot.stop_short_atr_mult,
            "stop_atr_period": bundle.runtime_snapshot.stop_atr_period,
        },
        "split_runs": {
            "validation": bundle.results.by_split["validation"].model_dump(),
            "test": bundle.results.by_split["test"].model_dump(),
        },
        "segmented_results": segmented_results,
        "cross_segment_summary": build_cross_segment_summary(segmented_results),
        **extra,
    }


def get_segment_metric(payload: dict[str, Any], split_name: str, segment_name: str, metric: str) -> float | None:
    for row in payload["segmented_results"][split_name]["segments"]:
        if row["segment"] == segment_name:
            return row["headline"].get(metric)
    return None


def sort_standard_candidates(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted(
        rows,
        key=lambda row: (
            float(row.get("test_holdout_b_return_pct") or float("-inf")),
            float(row.get("test_return_pct") or float("-inf")),
            float(row.get("test_profit_factor") or float("-inf")),
        ),
        reverse=True,
    )


def sort_stress_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted(
        rows,
        key=lambda row: (
            float(row.get("avg_holdout_b_return_pct") or float("-inf")),
            float(row.get("avg_test_return_pct") or float("-inf")),
            float(row.get("min_holdout_b_return_pct") or float("-inf")),
        ),
        reverse=True,
    )


def build_standard_review(rows: list[dict[str, Any]]) -> dict[str, Any]:
    ranked = sort_standard_candidates(rows)
    return {
        "generated_at_utc": utc_now_iso(),
        "stage": "07_motif_transplant",
        "phase": "07MT_standard_screen",
        "ranked_candidates": [{"rank": index + 1, **row} for index, row in enumerate(ranked)],
        "selection_basis": "test_holdout_b_return_pct_then_test_return_pct",
    }


def build_standard_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Stage 07 Standard Screen",
        "",
        "- phase: `07MT_standard_screen`",
        "- ranking basis: `test holdout_b return_pct -> test return_pct -> PF`",
        "",
    ]
    for row in payload["ranked_candidates"]:
        lines.append(
            f"- [{row['rank']}] `{row['run_name']}`: core=`{row['core_stage_id']}`, motif=`{row['motif_stage_id']}`, "
            f"test_holdout_b=`{format_metric(row.get('test_holdout_b_return_pct'), 3)}`, "
            f"test_return=`{format_metric(row.get('test_return_pct'), 3)}`, "
            f"PF=`{format_metric(row.get('test_profit_factor'), 4)}`, DD=`{format_metric(row.get('test_max_dd_pct'), 4)}`"
        )
    return "\n".join(lines) + "\n"


def build_stress_review(rows: list[dict[str, Any]]) -> dict[str, Any]:
    ranked = sort_stress_rows(rows)
    return {
        "generated_at_utc": utc_now_iso(),
        "stage": "07_motif_transplant",
        "phase": "07MT_shifted_window_stress",
        "ranked_candidates": [{"rank": index + 1, **row} for index, row in enumerate(ranked)],
        "selection_basis": "avg_holdout_b_return_pct_then_avg_test_return_pct",
    }


def build_stress_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Stage 07 Shifted-Window Stress",
        "",
        "- phase: `07MT_shifted_window_stress`",
        "- ranking basis: `avg holdout_b return_pct -> avg test return_pct -> min holdout_b return_pct`",
        "",
    ]
    for row in payload["ranked_candidates"]:
        lines.append(
            f"- [{row['rank']}] `{row['candidate_run_name']}`: avg_holdout_b=`{format_metric(row.get('avg_holdout_b_return_pct'), 3)}`, "
            f"min_holdout_b=`{format_metric(row.get('min_holdout_b_return_pct'), 3)}`, avg_test_return=`{format_metric(row.get('avg_test_return_pct'), 3)}`, "
            f"best_window=`{row.get('best_window_token')}`, worst_window=`{row.get('worst_window_token')}`"
        )
    return "\n".join(lines) + "\n"


def update_review_index(path: Path) -> None:
    lines = path.read_text(encoding="utf-8").splitlines() if path.exists() else ["# Review Index", ""]
    entry = "- `07MT`: see `07MT_motif_transplant_review.md` and `07MT_motif_transplant_stress_review.md`"
    if entry not in lines:
        if any("pending" in line for line in lines):
            lines = [line for line in lines if "pending" not in line]
        lines.append(entry)
    write_text(path, "\n".join(lines).rstrip() + "\n")


def update_selection_status(path: Path, standard_payload: dict[str, Any], stress_payload: dict[str, Any]) -> None:
    standard_leader = standard_payload["ranked_candidates"][0]
    stress_leader = stress_payload["ranked_candidates"][0]
    write_text(
        path,
        "\n".join(
            [
                "# Selection Status",
                "",
                "- stage: `07_motif_transplant`",
                "- status: `completed`",
                f"- standard_screen_leader: `{standard_leader['run_name']}`",
                f"- standard_screen_basis: `holdout_b={format_metric(standard_leader.get('test_holdout_b_return_pct'), 3)}, test_return={format_metric(standard_leader.get('test_return_pct'), 3)}, PF={format_metric(standard_leader.get('test_profit_factor'), 4)}`",
                f"- shifted_window_leader: `{stress_leader['candidate_run_name']}`",
                f"- shifted_window_basis: `avg_holdout_b={format_metric(stress_leader.get('avg_holdout_b_return_pct'), 3)}, min_holdout_b={format_metric(stress_leader.get('min_holdout_b_return_pct'), 3)}, avg_test_return={format_metric(stress_leader.get('avg_test_return_pct'), 3)}`",
                "- next action: `promote the shifted-window leader only if its standard-window totals remain acceptable; otherwise keep it as a defender motif reference`",
                "",
            ]
        ),
    )


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    stage_root = Path(args.stage_root).resolve()
    paths = stage_paths(stage_root)
    candidates = build_candidate_specs()
    ensure_stage_scaffold(stage_root, paths, args, candidates)

    source_model_run_dir = Path(args.source_model_run_dir).resolve()
    source_config, source_model, dataset, active_features = load_source_artifacts(source_model_run_dir)
    standard_boundaries = standard_split_boundaries()
    standard_scheme = build_segment_scheme(
        parse_utc(standard_boundaries.train_end_utc_exclusive),
        parse_utc(standard_boundaries.validation_end_utc_exclusive),
        parse_utc(standard_boundaries.test_end_utc_exclusive),
    )

    standard_rows: list[dict[str, Any]] = []
    for spec in candidates:
        run_dir = stage_root / "02_runs" / "active" / spec.run_name
        run_dir.mkdir(parents=True, exist_ok=True)

        motif_model = clone_with_motif(source_model, spec.motif)
        joblib.dump(motif_model, run_dir / "model.joblib")
        offline_metrics, test_predictions = evaluate_offline(motif_model, dataset, active_features)
        test_predictions.to_parquet(run_dir / "test_predictions.parquet", index=False)
        write_json(run_dir / "metrics.json", offline_metrics)
        write_json(run_dir / "rule_stack.json", json.loads(spec.core.rule_stack_source.read_text(encoding="utf-8-sig")))
        write_json(
            run_dir / "candidate_manifest.json",
            {
                "generated_at_utc": utc_now_iso(),
                "candidate_type": "stage07_motif_transplant",
                "stage_id": spec.stage_id,
                "run_name": spec.run_name,
                "experiment_id": spec.experiment_id,
                "core_reference": {"stage_id": spec.core.stage_id, "run_name": spec.core.run_name},
                "motif_reference": {
                    "stage_id": spec.motif.stage_id,
                    "run_name": spec.motif.source_run_name,
                    "label": spec.motif.label,
                    "temperature": spec.motif.temperature,
                    "class_biases": [float(value) for value in spec.motif.class_biases],
                },
            },
        )
        write_json(run_dir / "config.json", build_candidate_config(source_config, spec, dataset))

        bundle_path = export_bundle(
            source_run_dir=run_dir,
            output_dir=run_dir,
            stage_id=spec.stage_id,
            experiment_id=spec.experiment_id,
            rule_stack_path=run_dir / "rule_stack.json",
            args=args,
        )
        run_tester(bundle_path, "validation")
        run_tester(bundle_path, "test")

        payload = payload_from_run(
            run_dir=run_dir,
            split_boundaries=standard_boundaries,
            segment_scheme=standard_scheme,
            extra={
                "core_reference": {"stage_id": spec.core.stage_id, "run_name": spec.core.run_name},
                "motif_reference": {"stage_id": spec.motif.stage_id, "run_name": spec.motif.source_run_name, "label": spec.motif.label},
                "offline_metrics": offline_metrics,
            },
        )
        write_json(run_dir / "segmented_results.json", payload)
        write_text(run_dir / "segmented_results.md", json.dumps(payload["cross_segment_summary"], ensure_ascii=False, indent=2) + "\n")

        standard_rows.append(
            {
                "run_name": spec.run_name,
                "core_stage_id": spec.core.stage_id,
                "motif_stage_id": spec.motif.stage_id,
                "motif_label": spec.motif.label,
                "offline_test_macro_f1": offline_metrics["test_macro_f1"],
                "offline_test_balanced_accuracy": offline_metrics["test_balanced_accuracy"],
                "offline_test_log_loss": offline_metrics["test_log_loss"],
                "test_return_pct": payload["split_runs"]["test"]["headline"]["return_pct"],
                "test_profit_factor": payload["split_runs"]["test"]["headline"]["profit_factor"],
                "test_trade_count": payload["split_runs"]["test"]["headline"]["trade_count"],
                "test_max_dd_pct": payload["split_runs"]["test"]["headline"]["max_dd_pct"],
                "test_holdout_b_return_pct": get_segment_metric(payload, "test", "holdout_b", "return_pct"),
                "test_holdout_b_profit_factor": get_segment_metric(payload, "test", "holdout_b", "profit_factor"),
                "validation_return_pct": payload["split_runs"]["validation"]["headline"]["return_pct"],
                "segmented_results_path": str(run_dir / "segmented_results.json"),
            }
        )

    standard_review = build_standard_review(standard_rows)
    write_json(paths["review_json"], standard_review)
    write_text(paths["review_md"], build_standard_markdown(standard_review))

    stress_rows: list[dict[str, Any]] = []
    for target in standard_review["ranked_candidates"][:2]:
        candidate_run_dir = stage_root / "02_runs" / "active" / target["run_name"]
        candidate_spec = next(spec for spec in candidates if spec.run_name == target["run_name"])
        window_rows: list[dict[str, Any]] = []

        for token, train_start, train_end, validation_end, test_end in SHIFT_WINDOW_SPECS:
            run_name = f"07W_{token}_{candidate_spec.stage_id.lower()}_01"
            experiment_id = f"exp_07w_{token}_{candidate_spec.stage_id.lower()}_v1"
            stress_run_dir = stage_root / "02_runs" / "active" / run_name
            stress_run_dir.mkdir(parents=True, exist_ok=True)
            bundle_path = export_bundle(
                source_run_dir=candidate_run_dir,
                output_dir=stress_run_dir,
                stage_id="07W",
                experiment_id=experiment_id,
                rule_stack_path=candidate_run_dir / "rule_stack.json",
                args=args,
            )

            split_boundaries = SplitBoundaries(
                train_start_utc=train_start,
                train_end_utc_exclusive=train_end,
                validation_end_utc_exclusive=validation_end,
                test_end_utc_exclusive=test_end,
            )
            patch_bundle_window(
                bundle_path=bundle_path,
                split_boundaries=split_boundaries,
                split_counts=split_counts_for_window(dataset, split_boundaries),
                window_token=token,
                candidate_spec=candidate_spec,
            )
            run_tester(bundle_path, "validation")
            run_tester(bundle_path, "test")
            scheme = build_segment_scheme(parse_utc(train_end), parse_utc(validation_end), parse_utc(test_end))
            payload = payload_from_run(
                run_dir=stress_run_dir,
                split_boundaries=split_boundaries,
                segment_scheme=scheme,
                extra={
                    "parent_candidate_run_name": candidate_spec.run_name,
                    "window_token": token,
                    "core_reference": {"stage_id": candidate_spec.core.stage_id, "run_name": candidate_spec.core.run_name},
                    "motif_reference": {"stage_id": candidate_spec.motif.stage_id, "run_name": candidate_spec.motif.source_run_name, "label": candidate_spec.motif.label},
                },
            )
            write_json(stress_run_dir / "segmented_results.json", payload)
            write_text(stress_run_dir / "segmented_results.md", json.dumps(payload["cross_segment_summary"], ensure_ascii=False, indent=2) + "\n")
            window_rows.append(
                {
                    "window_token": token,
                    "test_return_pct": payload["split_runs"]["test"]["headline"]["return_pct"],
                    "test_profit_factor": payload["split_runs"]["test"]["headline"]["profit_factor"],
                    "test_max_dd_pct": payload["split_runs"]["test"]["headline"]["max_dd_pct"],
                    "holdout_b_return_pct": get_segment_metric(payload, "test", "holdout_b", "return_pct"),
                    "holdout_b_profit_factor": get_segment_metric(payload, "test", "holdout_b", "profit_factor"),
                    "segmented_results_path": str(stress_run_dir / "segmented_results.json"),
                }
            )

        avg_test_return = float(np.mean([row["test_return_pct"] for row in window_rows]))
        avg_holdout_b = float(np.mean([row["holdout_b_return_pct"] for row in window_rows]))
        min_holdout_b_row = min(window_rows, key=lambda row: row["holdout_b_return_pct"])
        best_window_row = max(window_rows, key=lambda row: row["test_return_pct"])
        worst_window_row = min(window_rows, key=lambda row: row["test_return_pct"])
        stress_rows.append(
            {
                "candidate_run_name": candidate_spec.run_name,
                "core_stage_id": candidate_spec.core.stage_id,
                "motif_stage_id": candidate_spec.motif.stage_id,
                "avg_test_return_pct": avg_test_return,
                "avg_holdout_b_return_pct": avg_holdout_b,
                "min_holdout_b_return_pct": min_holdout_b_row["holdout_b_return_pct"],
                "best_window_token": best_window_row["window_token"],
                "worst_window_token": worst_window_row["window_token"],
                "window_rows": window_rows,
            }
        )

    stress_review = build_stress_review(stress_rows)
    write_json(paths["stress_json"], stress_review)
    write_text(paths["stress_md"], build_stress_markdown(stress_review))
    update_review_index(paths["review_index"])
    update_selection_status(paths["selection"], standard_review, stress_review)


if __name__ == "__main__":
    main()
