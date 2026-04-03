#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import joblib
import numpy as np
import pandas as pd
from lightgbm import LGBMClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, balanced_accuracy_score, f1_score, log_loss
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.utils.class_weight import compute_sample_weight

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from foundation.features.catalog import FEATURE_ORDER
from foundation.pipelines.export_experiment_bundle_assets import run_export_bundle_assets
from foundation.pipelines.run_stage05_mt5_confirmation_batch import run_tester
from foundation.pipelines.show_experiment_leaderboard import load_bundle_views, sort_bundle_views


UTC = timezone.utc
LABEL_MAP = {0: "short", 1: "flat", 2: "long"}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run a Stage 05 MT5 validation using an alternate Stage 01 model family.")
    parser.add_argument("--stage-root", default="stages/05_optimization", help="Stage 05 root directory.")
    parser.add_argument(
        "--stage01-root",
        default="stages/01_base_feature_ml",
        help="Stage 01 root containing the archived model candidates.",
    )
    parser.add_argument(
        "--candidate-json",
        default="stages/01_base_feature_ml/04_selected/01C_selected_final_candidate.json",
        help="Stage 01C candidate selection JSON.",
    )
    parser.add_argument(
        "--candidate-key",
        default="runner_up",
        help="Candidate block to promote from the candidate JSON.",
    )
    parser.add_argument(
        "--run-name",
        default="05I_mt5_validation_margin_lightgbm_modelswap_0001",
        help="Stage 05 run folder name for the alternate model trial.",
    )
    parser.add_argument(
        "--experiment-id",
        default="exp_stage05_margin_lightgbm_modelswap_validation_0001",
        help="Experiment id written into experiment_bundle.json.",
    )
    parser.add_argument("--stage-id", default="05I", help="Stage id written into experiment_bundle.json.")
    parser.add_argument("--split-name", default="validation", help="Logical split name for MT5 tester results.")
    parser.add_argument(
        "--logic-reference-run-name",
        default="03E_mt5_validation_baseline_0001",
        help="Existing MT5 incumbent used as the logic-side comparison baseline.",
    )
    parser.add_argument(
        "--min-margin",
        type=float,
        default=0.07,
        help="Margin filter value copied from the incumbent 03E logic.",
    )
    parser.add_argument("--random-state", type=int, default=42, help="Random state for deterministic model refit.")
    parser.add_argument("--rebuild-bundle", action="store_true", help="Force bundle rebuild even if present.")
    return parser


def utc_now_iso() -> str:
    return datetime.now(tz=UTC).isoformat()


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_json(path: Path, payload: dict[str, Any]) -> None:
    write_text(path, json.dumps(payload, indent=2, ensure_ascii=False) + "\n")


def class_counts(series: pd.Series) -> dict[str, int]:
    counts = series.value_counts().to_dict()
    return {LABEL_MAP[key]: int(counts.get(key, 0)) for key in LABEL_MAP}


def save_test_outputs(run_dir: Path, test_df: pd.DataFrame, y_pred: np.ndarray, y_proba: np.ndarray) -> None:
    out = test_df[["timestamp", "split", "forward_return", "label"]].copy()
    out = out.rename(columns={"label": "label_true"})
    out["label_pred"] = y_pred
    out["p_short"] = y_proba[:, 0]
    out["p_flat"] = y_proba[:, 1]
    out["p_long"] = y_proba[:, 2]
    out.to_parquet(run_dir / "test_predictions.parquet", index=False)

    confusion = (
        pd.DataFrame({"label_true": out["label_true"], "label_pred": out["label_pred"]})
        .groupby(["label_true", "label_pred"])
        .size()
        .unstack(fill_value=0)
        .reindex(index=[0, 1, 2], columns=[0, 1, 2], fill_value=0)
    )
    confusion.index = [LABEL_MAP[idx] for idx in confusion.index]
    confusion.columns = [LABEL_MAP[idx] for idx in confusion.columns]
    confusion.to_csv(run_dir / "test_confusion_matrix.csv")


def fit_logistic(train_valid_df: pd.DataFrame, random_state: int) -> Pipeline:
    x_train = train_valid_df[FEATURE_ORDER]
    y_train = train_valid_df["label"]
    model = Pipeline(
        steps=[
            ("scaler", StandardScaler()),
            (
                "classifier",
                LogisticRegression(
                    solver="lbfgs",
                    max_iter=3000,
                    class_weight="balanced",
                    random_state=random_state,
                ),
            ),
        ]
    )
    model.fit(x_train, y_train)
    return model


def fit_lightgbm(train_valid_df: pd.DataFrame, best_iteration: int, random_state: int) -> LGBMClassifier:
    x_train = train_valid_df[FEATURE_ORDER]
    y_train = train_valid_df["label"]
    sample_weight = compute_sample_weight(class_weight="balanced", y=y_train)
    n_estimators = best_iteration if best_iteration and best_iteration > 0 else 500
    model = LGBMClassifier(
        objective="multiclass",
        num_class=3,
        n_estimators=n_estimators,
        learning_rate=0.05,
        num_leaves=31,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=random_state,
        n_jobs=-1,
    )
    model.fit(x_train, y_train, sample_weight=sample_weight)
    return model


def resolve_source_run_dir(stage01_root: Path, run_name: str) -> Path:
    for bucket in ("active", "archived"):
        candidate = stage01_root / "02_runs" / bucket / run_name
        if candidate.exists():
            return candidate
    raise FileNotFoundError(f"missing Stage 01 source run directory for {run_name}")


def build_rule_stack(min_margin: float) -> dict[str, Any]:
    return {
        "entry": [
            {
                "rule_id": "entry_01",
                "type": "threshold_entry",
                "enabled": True,
                "params": {
                    "short_threshold": 1.0 / 3.0,
                    "long_threshold": 1.0 / 3.0,
                },
            }
        ],
        "filters": [
            {
                "rule_id": "filter_01",
                "type": "max_probability_margin",
                "enabled": True,
                "params": {
                    "min_margin": min_margin,
                },
            }
        ],
        "position": [
            {
                "rule_id": "position_01",
                "type": "single_position_only",
                "enabled": True,
                "params": {
                    "max_concurrent_positions": 1,
                },
            }
        ],
        "exit": [
            {
                "rule_id": "exit_01",
                "type": "time_exit",
                "enabled": True,
                "params": {
                    "max_hold_bars": 3,
                },
            }
        ],
    }


def load_view_map(split_name: str, run_names: set[str]) -> dict[str, Any]:
    views = load_bundle_views(ROOT_DIR / "stages", split_name)
    filtered = [view for view in views if view.run_name in run_names]
    return {view.run_name: view for view in sort_bundle_views(filtered, "return_pct")}


def update_review_index(review_dir: Path) -> None:
    lines = [
        "# Review Index",
        "",
        "## Current Entries",
        "",
        "- `MT5 leaderboard`: see `mt5_validation_leaderboard.md`",
        "- `05A`: see `05A_margin_family_probe_review.md`",
        "- `05B`: see `05B_diff_family_probe_review.md`",
        "- `05C`: see `05C_mt5_family_confirmation_review.md`",
        "- `05D`: see `05D_mt5_holdout_duel_review.md`",
        "- `05E`: see `05E_mt5_frontier_validation_review.md`",
        "- `05I`: see `05I_mt5_alt_model_lightgbm_review.md`",
        "",
        "## Review Rule",
        "",
        "For each completed Stage 05 family probe, add:",
        "",
        "- run folder name",
        "- single-family logic summary",
        "- split used for cheap search",
        "- headline result",
        "- whether the family stays in the sequential shortlist",
    ]
    write_text(review_dir / "review_index.md", "\n".join(lines) + "\n")


def build_review_payload(
    *,
    args: argparse.Namespace,
    candidate: dict[str, Any],
    source_run_dir: Path,
    baseline_stage01: dict[str, Any],
    alt_test_metrics: dict[str, Any],
    mt5_view_map: dict[str, Any],
) -> dict[str, Any]:
    ranked_runs: list[dict[str, Any]] = []
    for rank, run_name in enumerate(mt5_view_map, start=1):
        view = mt5_view_map[run_name]
        extra = view.execution.get("extra") or {}
        ranked_runs.append(
            {
                "rank": rank,
                "run_name": view.run_name,
                "stage_folder": view.stage_folder,
                "return_pct": view.headline.get("return_pct"),
                "profit_factor": view.headline.get("profit_factor"),
                "trade_count": view.headline.get("trade_count"),
                "max_dd_pct": view.headline.get("max_dd_pct"),
                "ulcer_index": view.risk.get("ulcer_index"),
                "ready_row_gap": extra.get("ready_row_gap"),
                "unexpected_skip_count": extra.get("unexpected_skip_count"),
            }
        )

    return {
        "generated_at_utc": utc_now_iso(),
        "phase": "05I_mt5_alt_model_validation",
        "candidate_key": args.candidate_key,
        "source_run_name": candidate["run_name"],
        "source_run_dir": str(source_run_dir),
        "model_family": candidate["model_family"],
        "logic_reference_run_name": args.logic_reference_run_name,
        "logic_filter": {"type": "max_probability_margin", "min_margin": args.min_margin},
        "baseline_stage01_test_confirmation": baseline_stage01["test_confirmation"],
        "alt_model_test_confirmation": alt_test_metrics,
        "ranked_validation_runs": ranked_runs,
    }


def build_review_markdown(payload: dict[str, Any]) -> str:
    baseline = payload["baseline_stage01_test_confirmation"]
    alt = payload["alt_model_test_confirmation"]
    lines = [
        "# 05I Stage 05 Alternate Model MT5 Review",
        "",
        f"Generated at: `{payload['generated_at_utc']}`",
        "",
        "## Scope",
        "",
        "- purpose: `swap the Stage 01 baseline learner while keeping the current 03E logic fixed on MT5 validation`",
        f"- source candidate: `{payload['source_run_name']}` ({payload['model_family']})",
        f"- logic reference: `{payload['logic_reference_run_name']}` with `min_margin={payload['logic_filter']['min_margin']:.4f}`",
        "- holdout policy: `remain closed unless the alternate model materially improves the current validation frontier`",
        "",
        "## Offline Test Confirmation",
        "",
        f"- incumbent Stage 01 test: macro_f1=`{baseline['test_macro_f1']:.4f}`, balanced_accuracy=`{baseline['test_balanced_accuracy']:.4f}`, accuracy=`{baseline['test_accuracy']:.4f}`, log_loss=`{baseline['test_log_loss']:.4f}`",
        f"- alternate model test: macro_f1=`{alt['test_macro_f1']:.4f}`, balanced_accuracy=`{alt['test_balanced_accuracy']:.4f}`, accuracy=`{alt['test_accuracy']:.4f}`, log_loss=`{alt['test_log_loss']:.4f}`",
        "",
        "## MT5 Validation Ranking",
        "",
    ]
    for run in payload["ranked_validation_runs"]:
        lines.append(
            f"- [{run['rank']}] `{run['run_name']}`: "
            f"return_pct={run['return_pct']:.3f}, "
            f"profit_factor={run['profit_factor']:.4f}, "
            f"max_dd_pct={run['max_dd_pct']:.4f}, "
            f"ulcer_index={run['ulcer_index']:.4f}, "
            f"trades={run['trade_count']}, "
            f"ready_gap={run['ready_row_gap']}, "
            f"unexpected_skips={run['unexpected_skip_count']}"
        )
    leader = payload["ranked_validation_runs"][0]
    lines.extend(
        [
            "",
            "## Read",
            "",
            f"- validation leader from this comparison: `{leader['run_name']}`",
            "- read: `use this as a model-family sanity check first; only reopen holdout if the alternate learner clearly upgrades the current MT5 frontier`",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    args = build_parser().parse_args()

    stage_root = ROOT_DIR / args.stage_root
    stage01_root = ROOT_DIR / args.stage01_root
    candidate_json_path = ROOT_DIR / args.candidate_json
    run_dir = stage_root / "02_runs" / "active" / args.run_name
    review_dir = stage_root / "03_reviews"
    run_dir.mkdir(parents=True, exist_ok=True)
    review_dir.mkdir(parents=True, exist_ok=True)

    candidate_payload = json.loads(candidate_json_path.read_text(encoding="utf-8"))
    if args.candidate_key not in candidate_payload:
        raise KeyError(f"candidate key {args.candidate_key!r} missing from {candidate_json_path}")
    candidate = candidate_payload[args.candidate_key]

    source_run_dir = resolve_source_run_dir(stage01_root, candidate["run_name"])
    source_config = json.loads((source_run_dir / "config.json").read_text(encoding="utf-8"))
    dataset_path = ROOT_DIR / str(source_config["dataset_path"])
    dataset = pd.read_parquet(dataset_path)
    train_valid_df = dataset[dataset["split"].isin(["train", "valid"])].copy()
    test_df = dataset[dataset["split"].eq("test")].copy()

    final_config = {
        "run_name": args.run_name,
        "phase": "05I_alt_model_validation",
        "generated_at_utc": utc_now_iso(),
        "source_candidate_json": str(candidate_json_path.relative_to(ROOT_DIR)),
        "source_candidate_key": args.candidate_key,
        "source_stage01_run_name": candidate["run_name"],
        "source_stage01_run_dir": str(source_run_dir.relative_to(ROOT_DIR)),
        "model_family": candidate["model_family"],
        "horizon_bars": int(candidate["horizon_bars"]),
        "band": float(candidate["band"]),
        "dataset_path": str(dataset_path.relative_to(ROOT_DIR)),
        "refit_policy": "train_plus_valid_refit_then_mt5_validation",
        "logic_reference_run_name": args.logic_reference_run_name,
        "logic_filter": {
            "type": "max_probability_margin",
            "min_margin": float(args.min_margin),
        },
        "row_counts": {
            "train_valid": int(len(train_valid_df)),
            "test": int(len(test_df)),
        },
        "class_counts": {
            "train_valid": class_counts(train_valid_df["label"]),
            "test": class_counts(test_df["label"]),
        },
    }
    write_json(run_dir / "config.json", final_config)

    model_family = str(candidate["model_family"])
    if model_family == "lightgbm":
        model = fit_lightgbm(train_valid_df, int(candidate.get("best_iteration", 0)), args.random_state)
    elif model_family == "logistic_regression":
        model = fit_logistic(train_valid_df, args.random_state)
    else:
        raise ValueError(f"unsupported alternate model family: {model_family}")

    x_test = test_df[FEATURE_ORDER]
    y_test = test_df["label"].to_numpy(dtype=np.int64)
    y_proba = model.predict_proba(x_test)
    y_pred = np.argmax(y_proba, axis=1)

    joblib.dump(model, run_dir / "model.joblib")
    save_test_outputs(run_dir, test_df, y_pred, y_proba)

    alt_test_metrics = {
        "run_name": args.run_name,
        "model_family": model_family,
        "test_rows": int(len(test_df)),
        "test_macro_f1": float(f1_score(y_test, y_pred, average="macro")),
        "test_balanced_accuracy": float(balanced_accuracy_score(y_test, y_pred)),
        "test_accuracy": float(accuracy_score(y_test, y_pred)),
        "test_log_loss": float(log_loss(y_test, y_proba, labels=[0, 1, 2])),
    }
    write_json(run_dir / "metrics.json", alt_test_metrics)

    rule_stack_path = run_dir / "rule_stack.json"
    write_json(rule_stack_path, build_rule_stack(args.min_margin))

    bundle_path = run_dir / "experiment_bundle.json"
    if not bundle_path.exists() or args.rebuild_bundle:
        export_args = argparse.Namespace(
            run_dir=str(run_dir),
            experiment_id=args.experiment_id,
            stage_id=args.stage_id,
            output_dir=str(run_dir),
            stage_name="ea_optimize",
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
            max_hold_bars=3,
            build_bundle=True,
        )
        run_export_bundle_assets(export_args)

    run_tester(bundle_path, split_name=args.split_name, enable_trading=True)

    baseline_stage01 = json.loads(
        (stage01_root / "04_selected" / "01D_final_stage01_selection.json").read_text(encoding="utf-8")
    )
    mt5_view_map = load_view_map(args.split_name, {args.logic_reference_run_name, args.run_name})
    review_payload = build_review_payload(
        args=args,
        candidate=candidate,
        source_run_dir=source_run_dir,
        baseline_stage01=baseline_stage01,
        alt_test_metrics=alt_test_metrics,
        mt5_view_map=mt5_view_map,
    )
    write_json(review_dir / "05I_mt5_alt_model_lightgbm_review.json", review_payload)
    write_text(review_dir / "05I_mt5_alt_model_lightgbm_review.md", build_review_markdown(review_payload))
    update_review_index(review_dir)

    print(f"[done] run_dir={run_dir}")
    print(f"[done] bundle={bundle_path}")
    print(f"[done] review_md={review_dir / '05I_mt5_alt_model_lightgbm_review.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
