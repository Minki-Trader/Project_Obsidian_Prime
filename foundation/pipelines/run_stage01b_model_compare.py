#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from catboost import CatBoostClassifier
from lightgbm import LGBMClassifier, early_stopping, log_evaluation
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, balanced_accuracy_score, f1_score, log_loss
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.utils.class_weight import compute_sample_weight
from xgboost import XGBClassifier

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from foundation.features.catalog import FEATURE_ORDER


UTC = timezone.utc
LABEL_MAP = {0: "short", 1: "flat", 2: "long"}


@dataclass
class RunMetric:
    run_name: str
    model_family: str
    train_rows: int
    valid_rows: int
    test_rows: int
    valid_macro_f1: float
    valid_balanced_accuracy: float
    valid_accuracy: float
    valid_log_loss: float
    best_iteration: int


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run Stage 01B learning-tool comparison.")
    parser.add_argument(
        "--selected-label-json",
        default="stages/01_base_feature_ml/04_selected/01A_selected_label.json",
        help="Selected Stage 01A label JSON",
    )
    parser.add_argument(
        "--base-dataset",
        default="stages/01_base_feature_ml/01_inputs/stage01a_h06_dataset.parquet",
        help="Stage 01A base dataset without the frozen label column",
    )
    parser.add_argument(
        "--stage-root",
        default="stages/01_base_feature_ml",
        help="Stage 01 root",
    )
    parser.add_argument(
        "--random-state",
        type=int,
        default=42,
        help="Random state for the compared models",
    )
    return parser


def utc_now_iso() -> str:
    return datetime.now(tz=UTC).isoformat()


def write_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")


def make_label(forward_return: pd.Series, band: float) -> pd.Series:
    label = np.where(forward_return <= -band, 0, np.where(forward_return >= band, 2, 1))
    return pd.Series(label, index=forward_return.index, dtype="int64")


def class_counts(series: pd.Series) -> dict[str, int]:
    counts = series.value_counts().to_dict()
    return {LABEL_MAP[key]: int(counts.get(key, 0)) for key in LABEL_MAP}


def collect_metrics(
    run_name: str,
    model_family: str,
    y_valid: np.ndarray,
    valid_proba: np.ndarray,
    valid_pred: np.ndarray,
    train_rows: int,
    valid_rows: int,
    test_rows: int,
    best_iteration: int,
) -> RunMetric:
    return RunMetric(
        run_name=run_name,
        model_family=model_family,
        train_rows=train_rows,
        valid_rows=valid_rows,
        test_rows=test_rows,
        valid_macro_f1=float(f1_score(y_valid, valid_pred, average="macro")),
        valid_balanced_accuracy=float(balanced_accuracy_score(y_valid, valid_pred)),
        valid_accuracy=float(accuracy_score(y_valid, valid_pred)),
        valid_log_loss=float(log_loss(y_valid, valid_proba, labels=[0, 1, 2])),
        best_iteration=int(best_iteration),
    )


def save_predictions(
    run_dir: Path,
    valid_df: pd.DataFrame,
    valid_pred: np.ndarray,
    valid_proba: np.ndarray,
) -> None:
    out = valid_df[["timestamp", "split", "forward_return", "label"]].copy()
    out = out.rename(columns={"label": "label_true"})
    out["label_pred"] = valid_pred
    out["p_short"] = valid_proba[:, 0]
    out["p_flat"] = valid_proba[:, 1]
    out["p_long"] = valid_proba[:, 2]
    out.to_parquet(run_dir / "valid_predictions.parquet", index=False)

    confusion = (
        pd.DataFrame({"label_true": out["label_true"], "label_pred": out["label_pred"]})
        .groupby(["label_true", "label_pred"])
        .size()
        .unstack(fill_value=0)
        .reindex(index=[0, 1, 2], columns=[0, 1, 2], fill_value=0)
    )
    confusion.index = [LABEL_MAP[idx] for idx in confusion.index]
    confusion.columns = [LABEL_MAP[idx] for idx in confusion.columns]
    confusion.to_csv(run_dir / "valid_confusion_matrix.csv")


def fit_lightgbm(
    train_df: pd.DataFrame,
    valid_df: pd.DataFrame,
    run_dir: Path,
    random_state: int,
) -> RunMetric:
    x_train = train_df[FEATURE_ORDER]
    y_train = train_df["label"]
    x_valid = valid_df[FEATURE_ORDER]
    y_valid = valid_df["label"]
    sample_weight = compute_sample_weight(class_weight="balanced", y=y_train)

    model = LGBMClassifier(
        objective="multiclass",
        num_class=3,
        n_estimators=500,
        learning_rate=0.05,
        num_leaves=31,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=random_state,
        n_jobs=-1,
    )
    model.fit(
        x_train,
        y_train,
        sample_weight=sample_weight,
        eval_set=[(x_valid, y_valid)],
        eval_metric="multi_logloss",
        callbacks=[early_stopping(stopping_rounds=50, verbose=False), log_evaluation(period=0)],
    )
    valid_proba = model.predict_proba(x_valid)
    valid_pred = np.argmax(valid_proba, axis=1)
    joblib.dump(model, run_dir / "model.joblib")
    pd.DataFrame({"feature": FEATURE_ORDER, "importance": model.feature_importances_}).sort_values(
        "importance", ascending=False
    ).to_csv(run_dir / "feature_importance.csv", index=False)
    save_predictions(run_dir, valid_df, valid_pred, valid_proba)
    return collect_metrics(
        run_name=run_dir.name,
        model_family="lightgbm",
        y_valid=y_valid.to_numpy(),
        valid_proba=valid_proba,
        valid_pred=valid_pred,
        train_rows=len(train_df),
        valid_rows=len(valid_df),
        test_rows=0,
        best_iteration=getattr(model, "best_iteration_", 0) or model.n_estimators,
    )


def fit_xgboost(
    train_df: pd.DataFrame,
    valid_df: pd.DataFrame,
    run_dir: Path,
    random_state: int,
) -> RunMetric:
    x_train = train_df[FEATURE_ORDER]
    y_train = train_df["label"]
    x_valid = valid_df[FEATURE_ORDER]
    y_valid = valid_df["label"]
    sample_weight = compute_sample_weight(class_weight="balanced", y=y_train)

    model = XGBClassifier(
        objective="multi:softprob",
        num_class=3,
        n_estimators=500,
        learning_rate=0.05,
        max_depth=6,
        subsample=0.8,
        colsample_bytree=0.8,
        reg_lambda=1.0,
        min_child_weight=1.0,
        random_state=random_state,
        n_jobs=-1,
        eval_metric="mlogloss",
        tree_method="hist",
    )
    model.fit(
        x_train,
        y_train,
        sample_weight=sample_weight,
        eval_set=[(x_valid, y_valid)],
        verbose=False,
    )
    valid_proba = model.predict_proba(x_valid)
    valid_pred = np.argmax(valid_proba, axis=1)
    joblib.dump(model, run_dir / "model.joblib")
    pd.DataFrame({"feature": FEATURE_ORDER, "importance": model.feature_importances_}).sort_values(
        "importance", ascending=False
    ).to_csv(run_dir / "feature_importance.csv", index=False)
    save_predictions(run_dir, valid_df, valid_pred, valid_proba)
    return collect_metrics(
        run_name=run_dir.name,
        model_family="xgboost",
        y_valid=y_valid.to_numpy(),
        valid_proba=valid_proba,
        valid_pred=valid_pred,
        train_rows=len(train_df),
        valid_rows=len(valid_df),
        test_rows=0,
        best_iteration=getattr(model, "best_iteration", 0) or model.n_estimators,
    )


def fit_catboost(
    train_df: pd.DataFrame,
    valid_df: pd.DataFrame,
    run_dir: Path,
    random_state: int,
) -> RunMetric:
    x_train = train_df[FEATURE_ORDER]
    y_train = train_df["label"]
    x_valid = valid_df[FEATURE_ORDER]
    y_valid = valid_df["label"]
    sample_weight = compute_sample_weight(class_weight="balanced", y=y_train)

    model = CatBoostClassifier(
        loss_function="MultiClass",
        eval_metric="MultiClass",
        iterations=500,
        learning_rate=0.05,
        depth=6,
        random_seed=random_state,
        verbose=False,
    )
    model.fit(
        x_train,
        y_train,
        sample_weight=sample_weight,
        eval_set=(x_valid, y_valid),
        use_best_model=True,
        early_stopping_rounds=50,
        verbose=False,
    )
    valid_proba = model.predict_proba(x_valid)
    valid_pred = np.argmax(valid_proba, axis=1)
    joblib.dump(model, run_dir / "model.joblib")
    pd.DataFrame({"feature": FEATURE_ORDER, "importance": model.get_feature_importance()}).sort_values(
        "importance", ascending=False
    ).to_csv(run_dir / "feature_importance.csv", index=False)
    save_predictions(run_dir, valid_df, valid_pred, valid_proba)
    return collect_metrics(
        run_name=run_dir.name,
        model_family="catboost",
        y_valid=y_valid.to_numpy(),
        valid_proba=valid_proba,
        valid_pred=valid_pred,
        train_rows=len(train_df),
        valid_rows=len(valid_df),
        test_rows=0,
        best_iteration=model.get_best_iteration() if model.get_best_iteration() is not None else model.tree_count_,
    )


def fit_logistic(
    train_df: pd.DataFrame,
    valid_df: pd.DataFrame,
    run_dir: Path,
    random_state: int,
) -> RunMetric:
    x_train = train_df[FEATURE_ORDER]
    y_train = train_df["label"]
    x_valid = valid_df[FEATURE_ORDER]
    y_valid = valid_df["label"]

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
    valid_proba = model.predict_proba(x_valid)
    valid_pred = np.argmax(valid_proba, axis=1)
    joblib.dump(model, run_dir / "model.joblib")
    save_predictions(run_dir, valid_df, valid_pred, valid_proba)
    coef = model.named_steps["classifier"].coef_
    coef_df = pd.DataFrame(coef.T, index=FEATURE_ORDER, columns=["short", "flat", "long"])
    coef_df["mean_abs_coef"] = np.mean(np.abs(coef), axis=0)
    coef_df.to_csv(run_dir / "feature_coefficients.csv")
    return collect_metrics(
        run_name=run_dir.name,
        model_family="logistic_regression",
        y_valid=y_valid.to_numpy(),
        valid_proba=valid_proba,
        valid_pred=valid_pred,
        train_rows=len(train_df),
        valid_rows=len(valid_df),
        test_rows=0,
        best_iteration=0,
    )


def model_specs() -> list[tuple[str, str, callable]]:
    return [
        ("0001", "lightgbm", fit_lightgbm),
        ("0002", "xgboost", fit_xgboost),
        ("0003", "catboost", fit_catboost),
        ("0004", "logreg", fit_logistic),
    ]


def band_tag(value: float) -> str:
    return f"{value:.5f}".replace(".", "")


def main() -> int:
    args = build_parser().parse_args()

    selected_label_path = ROOT_DIR / args.selected_label_json
    base_dataset_path = ROOT_DIR / args.base_dataset
    stage_root = ROOT_DIR / args.stage_root

    selection = json.loads(selected_label_path.read_text(encoding="utf-8"))
    band = float(selection["selected_band"])
    horizon_bars = int(selection["selected_horizon_bars"])

    inputs_dir = stage_root / "01_inputs"
    active_dir = stage_root / "02_runs" / "active"
    archived_dir = stage_root / "02_runs" / "archived"
    review_dir = stage_root / "03_reviews"
    selected_dir = stage_root / "04_selected"
    inputs_dir.mkdir(parents=True, exist_ok=True)
    active_dir.mkdir(parents=True, exist_ok=True)
    archived_dir.mkdir(parents=True, exist_ok=True)
    review_dir.mkdir(parents=True, exist_ok=True)
    selected_dir.mkdir(parents=True, exist_ok=True)

    dataset = pd.read_parquet(base_dataset_path)
    dataset["label"] = make_label(dataset["forward_return"], band)
    tag = f"h{horizon_bars:02d}_band{band_tag(band)}"
    labeled_path = inputs_dir / f"stage01b_{tag}_dataset.parquet"
    labeled_summary_path = inputs_dir / f"stage01b_{tag}_dataset_summary.json"
    compare_plan_path = inputs_dir / "01B_model_compare_plan.json"

    dataset.to_parquet(labeled_path, index=False)
    write_json(
        labeled_summary_path,
        {
            "generated_at_utc": utc_now_iso(),
            "source_selected_label_json": str(selected_label_path.relative_to(ROOT_DIR)),
            "source_base_dataset": str(base_dataset_path.relative_to(ROOT_DIR)),
            "row_count": int(len(dataset)),
            "horizon_bars": horizon_bars,
            "band": band,
            "split_counts": {key: int(value) for key, value in dataset["split"].value_counts().to_dict().items()},
            "class_counts": {
                split_name: class_counts(frame["label"])
                for split_name, frame in dataset.groupby("split")
            },
        },
    )
    write_json(
        compare_plan_path,
        {
            "generated_at_utc": utc_now_iso(),
            "phase": "01B_model_compare",
            "horizon_bars": horizon_bars,
            "band": band,
            "frozen_items": [
                "[p_short, p_flat, p_long]",
                "US100 M5 base frame",
                "chronological split ordering",
                "shared FPMarkets v2 feature contract",
                f"selected horizon={horizon_bars}",
                f"selected band={band:.5f}",
            ],
            "models_to_compare": ["lightgbm", "xgboost", "catboost", "logistic_regression"],
            "selection_metric": "valid_macro_f1",
            "carry_forward_count_for_01C": 2,
        },
    )

    train_df = dataset[dataset["split"].eq("train")].copy()
    valid_df = dataset[dataset["split"].eq("valid")].copy()
    test_df = dataset[dataset["split"].eq("test")].copy()

    results: list[RunMetric] = []
    run_paths: dict[str, Path] = {}
    for ordinal, model_tag, fit_fn in model_specs():
        run_name = f"01B_run_{ordinal}_{tag}_{model_tag}"
        run_dir = active_dir / run_name
        run_dir.mkdir(parents=True, exist_ok=True)
        run_paths[run_name] = run_dir

        config = {
            "run_name": run_name,
            "phase": "01B_model_compare",
            "generated_at_utc": utc_now_iso(),
            "model_family": model_tag,
            "horizon_bars": horizon_bars,
            "band": band,
            "dataset_path": str(labeled_path.relative_to(ROOT_DIR)),
            "selection_source": str(selected_label_path.relative_to(ROOT_DIR)),
            "split_counts": {
                "train": int(len(train_df)),
                "valid": int(len(valid_df)),
                "test": int(len(test_df)),
            },
            "class_counts": {
                "train": class_counts(train_df["label"]),
                "valid": class_counts(valid_df["label"]),
                "test": class_counts(test_df["label"]),
            },
            "selection_metric": "valid_macro_f1",
        }
        write_json(run_dir / "config.json", config)

        metric = fit_fn(
            train_df=train_df,
            valid_df=valid_df,
            run_dir=run_dir,
            random_state=args.random_state,
        )
        metric.test_rows = int(len(test_df))
        write_json(run_dir / "metrics.json", asdict(metric))
        results.append(metric)

    results_df = pd.DataFrame([asdict(item) for item in results]).sort_values(
        by=["valid_macro_f1", "valid_balanced_accuracy", "valid_accuracy", "valid_log_loss"],
        ascending=[False, False, False, True],
    )
    results_df.to_csv(review_dir / "01B_model_compare_results.csv", index=False)

    top_two = results_df.head(2).copy()
    keep_names = set(top_two["run_name"].tolist())
    archived_names: list[str] = []
    for run_name, run_dir in run_paths.items():
        if run_name in keep_names:
            continue
        target = archived_dir / run_name
        if target.exists():
            for child in target.iterdir():
                if child.is_file():
                    child.unlink()
            target.rmdir()
        run_dir.rename(target)
        archived_names.append(run_name)

    review_lines = [
        "# 01B Model Compare Review",
        "",
        f"Generated at: `{utc_now_iso()}`",
        "",
        "## Frozen Label Setup",
        "",
        f"- horizon: `{horizon_bars}` bars",
        f"- band: `{band:.5f}`",
        f"- train rows: `{len(train_df)}`",
        f"- valid rows: `{len(valid_df)}`",
        f"- test rows kept untouched for later confirmation: `{len(test_df)}`",
        "",
        "## Ranked Results",
        "",
    ]
    for row in results_df.itertuples(index=False):
        review_lines.append(
            f"- `{row.run_name}` ({row.model_family}): macro_f1={row.valid_macro_f1:.4f}, "
            f"balanced_acc={row.valid_balanced_accuracy:.4f}, accuracy={row.valid_accuracy:.4f}, "
            f"log_loss={row.valid_log_loss:.4f}"
        )
    review_lines.extend(
        [
            "",
            "## Selected For 01C",
            "",
            f"- primary candidate: `{top_two.iloc[0]['run_name']}`",
            f"- secondary candidate: `{top_two.iloc[1]['run_name']}`",
            f"- archived this phase: `{', '.join(archived_names) if archived_names else 'none'}`",
        ]
    )
    write_text(review_dir / "01B_model_compare_review.md", "\n".join(review_lines) + "\n")

    selected_payload = {
        "generated_at_utc": utc_now_iso(),
        "phase": "01B_model_compare",
        "frozen_horizon_bars": horizon_bars,
        "frozen_band": band,
        "selection_metric": "valid_macro_f1",
        "primary_candidate": results_df.iloc[0].to_dict(),
        "secondary_candidate": results_df.iloc[1].to_dict(),
        "archived_runs": archived_names,
        "next_phase": "01C_expanded_search",
    }
    write_json(selected_dir / "01B_selected_models.json", selected_payload)

    selected_note = [
        "# 01B Selected Models",
        "",
        f"- frozen horizon: `{horizon_bars}` bars",
        f"- frozen band: `{band:.5f}`",
        f"- primary candidate: `{top_two.iloc[0]['run_name']}`",
        f"- secondary candidate: `{top_two.iloc[1]['run_name']}`",
        f"- next phase: `01C_expanded_search`",
    ]
    write_text(selected_dir / "01B_selected_models.md", "\n".join(selected_note) + "\n")

    print(json.dumps(selected_payload, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
