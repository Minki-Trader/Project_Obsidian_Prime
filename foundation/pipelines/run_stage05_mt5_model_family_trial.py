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
from sklearn.calibration import CalibratedClassifierCV
from catboost import CatBoostClassifier
from lightgbm import LGBMClassifier
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import ExtraTreesClassifier, RandomForestClassifier, StackingClassifier
from sklearn.ensemble import VotingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, balanced_accuracy_score, f1_score, log_loss
from sklearn.decomposition import PCA
from sklearn.multiclass import OneVsRestClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.utils.class_weight import compute_sample_weight
from xgboost import XGBClassifier

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from foundation.features.catalog import FEATURE_ORDER
from foundation.features.replacement_sectors import (
    TREND_PROXY_REPLACEMENT_COMPONENT_GROUPS,
    TREND_PROXY_REPLACEMENT_NAME,
    parse_replacement_component_groups,
    resolve_replacement_component_groups,
)
from foundation.features.sector_map import SECTOR_MAP, feature_order_without_sectors
from foundation.pipelines.export_experiment_bundle_assets import run_export_bundle_assets
from foundation.pipelines.run_stage05_mt5_confirmation_batch import run_tester


UTC = timezone.utc
LABEL_MAP = {0: "short", 1: "flat", 2: "long"}
SEMANTIC_INTERACTION_FEATURES = [
    "ema9_ema20_diff",
    "ema20_ema50_diff",
    "ema50_ema200_diff",
    "close_ema20_ratio",
    "close_ema50_ratio",
    "atr_50",
    "historical_vol_20",
    "atr_14_over_atr_50",
    "hl_range",
    "return_1_over_atr_14",
    "log_return_1",
    "trix_15",
    "top3_weighted_return_1",
    "nvda_xnas_log_return_1",
    "minutes_from_cash_open",
    "mega8_dispersion_5",
]
REPLACEMENT_SECTOR_MODEL_FAMILIES = {
    "trend_proxy_sector_logreg",
    "ovr_trend_proxy_logreg",
    "calibrated_trend_proxy_sigmoid",
    "calibrated_ovr_trend_proxy_sigmoid",
}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run a Stage 05 MT5 trial for a freshly trained model family.")
    parser.add_argument("--stage-root", default="stages/05_optimization", help="Stage 05 root directory.")
    parser.add_argument(
        "--dataset-path",
        default="stages/01_base_feature_ml/01_inputs/stage01c_h03_band000125_dataset.parquet",
        help="Dataset parquet used for the model-family trial.",
    )
    parser.add_argument(
        "--model-family",
        default="catboost",
        choices=[
            "logistic_regression",
            "elasticnet_logreg",
            "pca_logreg",
            "regularized_logreg_voter",
            "lightgbm",
            "catboost",
            "xgboost",
            "random_forest",
            "extra_trees",
            "semantic_interaction_logreg",
            "trend_proxy_sector_logreg",
            "ovr_trend_proxy_logreg",
            "calibrated_trend_proxy_sigmoid",
            "calibrated_ovr_trend_proxy_sigmoid",
            "persistence_frontier_voter",
            "persistence_frontier_stacker",
        ],
        help="Model family to train on the frozen dataset.",
    )
    parser.add_argument("--horizon-bars", type=int, default=3, help="Label horizon carried into config metadata.")
    parser.add_argument("--band", type=float, default=0.00125, help="Band carried into config metadata.")
    parser.add_argument(
        "--run-name",
        default="05J_mt5_validation_margin_catboost_modelswap_0001",
        help="Stage 05 run folder name for this model-family trial.",
    )
    parser.add_argument(
        "--experiment-id",
        default="exp_stage05_margin_catboost_modelswap_validation_0001",
        help="Experiment id written into experiment_bundle.json.",
    )
    parser.add_argument("--stage-id", default="05J", help="Stage id written into experiment_bundle.json.")
    parser.add_argument(
        "--review-basename",
        default="05J_mt5_model_family_trial_review",
        help="Basename for review markdown/json files under 03_reviews.",
    )
    parser.add_argument(
        "--logic-reference-run-name",
        default="03E_mt5_validation_baseline_0001",
        help="Existing MT5 incumbent used as the logic-side comparison baseline.",
    )
    parser.add_argument("--min-margin", type=float, default=0.07, help="Margin filter value copied from 03E logic.")
    parser.add_argument("--max-hold-bars", type=int, default=3, help="Exit max_hold_bars copied into the rule stack.")
    parser.add_argument("--random-state", type=int, default=42, help="Random state for deterministic training.")
    parser.add_argument("--rebuild-bundle", action="store_true", help="Force bundle rebuild even if present.")
    parser.add_argument("--run-holdout", action="store_true", help="Also execute the MT5 holdout split after validation.")
    parser.add_argument(
        "--drop-sectors",
        default="",
        help="Comma-separated feature sectors to remove from the base 58-feature contract for this trial.",
    )
    parser.add_argument(
        "--drop-features",
        default="",
        help="Comma-separated individual feature names to remove from the active feature set for this trial.",
    )
    parser.add_argument(
        "--replacement-component-groups",
        default="",
        help="Comma-separated replacement-sector component groups to include for trend_proxy_sector_logreg. Defaults to all groups.",
    )
    parser.add_argument(
        "--voter-components",
        default="",
        help="Comma-separated submodels for persistence_frontier_voter. Allowed: base_05w,persistence_only,persistence_breakout,persistence_volatility,full_proxy.",
    )
    parser.add_argument(
        "--voter-weights",
        default="",
        help="Comma-separated positive weights for persistence_frontier_voter, matching --voter-components.",
    )
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


def fit_logistic(train_valid_df: pd.DataFrame, active_features: list[str], random_state: int) -> Pipeline:
    x_train = train_valid_df[active_features]
    y_train = train_valid_df["label"]
    model = build_logistic_pipeline(random_state)
    model.fit(x_train, y_train)
    return model


def build_logistic_pipeline(
    random_state: int,
    *,
    c: float = 1.0,
    penalty: str | None = None,
    solver: str = "lbfgs",
    l1_ratio: float | None = None,
    max_iter: int = 3000,
) -> Pipeline:
    classifier_kwargs: dict[str, Any] = {
        "solver": solver,
        "C": c,
        "max_iter": max_iter,
        "class_weight": "balanced",
        "random_state": random_state,
    }
    if penalty is not None:
        classifier_kwargs["penalty"] = penalty
    if l1_ratio is not None:
        classifier_kwargs["l1_ratio"] = l1_ratio
    return Pipeline(
        steps=[
            ("scaler", StandardScaler()),
            (
                "classifier",
                LogisticRegression(**classifier_kwargs),
            ),
        ]
    )


def fit_elasticnet_logreg(train_valid_df: pd.DataFrame, active_features: list[str], random_state: int) -> Pipeline:
    x_train = train_valid_df[active_features]
    y_train = train_valid_df["label"]
    model = build_logistic_pipeline(
        random_state,
        c=0.45,
        penalty="elasticnet",
        solver="saga",
        l1_ratio=0.15,
        max_iter=5000,
    )
    model.fit(x_train, y_train)
    return model


def fit_pca_logreg(train_valid_df: pd.DataFrame, active_features: list[str], random_state: int) -> Pipeline:
    x_train = train_valid_df[active_features]
    y_train = train_valid_df["label"]
    n_components = min(24, max(8, len(active_features) // 2))
    model = Pipeline(
        steps=[
            ("scale_raw", StandardScaler()),
            ("pca", PCA(n_components=n_components, random_state=random_state)),
            (
                "classifier",
                LogisticRegression(
                    solver="lbfgs",
                    C=0.8,
                    class_weight="balanced",
                    max_iter=4000,
                    random_state=random_state,
                ),
            ),
        ]
    )
    model.fit(x_train, y_train)
    return model


def fit_regularized_logreg_voter(
    train_valid_df: pd.DataFrame, active_features: list[str], random_state: int
) -> VotingClassifier:
    x_train = train_valid_df[active_features]
    y_train = train_valid_df["label"]
    estimators = [
        ("ridge_tight", build_logistic_pipeline(random_state, c=0.35)),
        ("ridge_mid", build_logistic_pipeline(random_state, c=0.7)),
        (
            "elastic_sparse",
            build_logistic_pipeline(
                random_state,
                c=0.45,
                penalty="elasticnet",
                solver="saga",
                l1_ratio=0.10,
                max_iter=5000,
            ),
        ),
    ]
    model = VotingClassifier(
        estimators=estimators,
        voting="soft",
        weights=np.asarray([1.0, 2.0, 1.0], dtype=np.float64),
        flatten_transform=False,
    )
    model.fit(x_train, y_train)
    return model


def fit_lightgbm(train_valid_df: pd.DataFrame, active_features: list[str], random_state: int) -> LGBMClassifier:
    x_train = train_valid_df[active_features]
    y_train = train_valid_df["label"]
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
    model.fit(x_train, y_train, sample_weight=sample_weight)
    return model


def fit_catboost(train_valid_df: pd.DataFrame, active_features: list[str], random_state: int) -> CatBoostClassifier:
    x_train = train_valid_df[active_features]
    y_train = train_valid_df["label"]
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
    model.fit(x_train, y_train, sample_weight=sample_weight, verbose=False)
    return model


def fit_xgboost(train_valid_df: pd.DataFrame, active_features: list[str], random_state: int) -> XGBClassifier:
    x_train = train_valid_df[active_features].to_numpy(dtype=np.float32)
    y_train = train_valid_df["label"].to_numpy(dtype=np.int64)
    sample_weight = compute_sample_weight(class_weight="balanced", y=y_train)
    model = XGBClassifier(
        objective="multi:softprob",
        num_class=3,
        n_estimators=500,
        learning_rate=0.05,
        max_depth=4,
        subsample=0.8,
        colsample_bytree=0.8,
        reg_lambda=1.0,
        min_child_weight=1.0,
        random_state=random_state,
        n_jobs=-1,
        tree_method="hist",
        eval_metric="mlogloss",
    )
    model.fit(x_train, y_train, sample_weight=sample_weight)
    return model


def fit_random_forest(train_valid_df: pd.DataFrame, active_features: list[str], random_state: int) -> RandomForestClassifier:
    x_train = train_valid_df[active_features]
    y_train = train_valid_df["label"]
    sample_weight = compute_sample_weight(class_weight="balanced", y=y_train)
    model = RandomForestClassifier(
        n_estimators=500,
        max_depth=8,
        min_samples_leaf=20,
        max_features="sqrt",
        class_weight="balanced_subsample",
        random_state=random_state,
        n_jobs=-1,
    )
    model.fit(x_train, y_train, sample_weight=sample_weight)
    return model


def fit_extra_trees(train_valid_df: pd.DataFrame, active_features: list[str], random_state: int) -> ExtraTreesClassifier:
    x_train = train_valid_df[active_features]
    y_train = train_valid_df["label"]
    sample_weight = compute_sample_weight(class_weight="balanced", y=y_train)
    model = ExtraTreesClassifier(
        n_estimators=700,
        max_depth=10,
        min_samples_leaf=15,
        max_features="sqrt",
        class_weight="balanced",
        random_state=random_state,
        n_jobs=-1,
    )
    model.fit(x_train, y_train, sample_weight=sample_weight)
    return model


def fit_semantic_interaction_logreg(
    train_valid_df: pd.DataFrame, active_features: list[str], random_state: int
) -> Pipeline:
    x_train = train_valid_df[active_features]
    y_train = train_valid_df["label"]
    model = Pipeline(
        steps=[
            ("scale_raw", StandardScaler()),
            ("poly", PolynomialFeatures(degree=2, interaction_only=True, include_bias=False)),
            ("scale_poly", StandardScaler()),
            (
                "classifier",
                LogisticRegression(
                    solver="lbfgs",
                    C=0.5,
                    class_weight="balanced",
                    max_iter=1200,
                    random_state=random_state,
                ),
            ),
        ]
    )
    model.fit(x_train, y_train)
    return model


def fit_trend_proxy_sector_logreg(
    train_valid_df: pd.DataFrame,
    active_features: list[str],
    random_state: int,
    replacement_component_groups: dict[str, list[str]],
) -> Pipeline:
    missing = sorted(
        {
            feature
            for features in replacement_component_groups.values()
            for feature in features
            if feature not in active_features
        }
    )
    if missing:
        raise ValueError(f"trend proxy replacement groups require missing features: {missing}")
    x_train = train_valid_df[active_features]
    y_train = train_valid_df["label"]
    model = build_trend_proxy_sector_pipeline(active_features, random_state, replacement_component_groups)
    model.fit(x_train, y_train)
    return model


def build_trend_proxy_preprocessor(
    active_features: list[str],
    random_state: int,
    replacement_component_groups: dict[str, list[str]],
) -> ColumnTransformer:
    feature_index = {feature: idx for idx, feature in enumerate(active_features)}
    transformer_specs: list[tuple[str, object, list[int]]] = [
        ("base_raw", "passthrough", list(range(len(active_features)))),
    ]
    for component_name, source_features in replacement_component_groups.items():
        transformer_specs.append(
            (
                component_name,
                Pipeline(
                    steps=[
                        ("scale", StandardScaler()),
                        ("pca", PCA(n_components=1, random_state=random_state)),
                    ]
                ),
                [feature_index[feature] for feature in source_features],
            )
        )
    return ColumnTransformer(
        transformers=transformer_specs,
        remainder="drop",
        verbose_feature_names_out=False,
    )


def build_trend_proxy_linear_pipeline(
    active_features: list[str],
    random_state: int,
    replacement_component_groups: dict[str, list[str]],
    classifier: object,
) -> Pipeline:
    return Pipeline(
        steps=[
            (
                "feature_blocks",
                build_trend_proxy_preprocessor(active_features, random_state, replacement_component_groups),
            ),
            ("scale_all", StandardScaler()),
            ("classifier", classifier),
        ]
    )


def build_trend_proxy_sector_pipeline(
    active_features: list[str],
    random_state: int,
    replacement_component_groups: dict[str, list[str]],
) -> Pipeline:
    return build_trend_proxy_linear_pipeline(
        active_features,
        random_state,
        replacement_component_groups,
        LogisticRegression(
            solver="lbfgs",
            C=0.7,
            class_weight="balanced",
            max_iter=2500,
            random_state=random_state,
        ),
    )


def build_trend_proxy_ovr_classifier(random_state: int) -> OneVsRestClassifier:
    return OneVsRestClassifier(
        LogisticRegression(
            solver="lbfgs",
            C=0.55,
            class_weight="balanced",
            max_iter=2500,
            random_state=random_state,
        )
    )


def fit_ovr_trend_proxy_logreg(
    train_valid_df: pd.DataFrame,
    active_features: list[str],
    random_state: int,
    replacement_component_groups: dict[str, list[str]],
) -> Pipeline:
    x_train = train_valid_df[active_features]
    y_train = train_valid_df["label"]
    model = build_trend_proxy_linear_pipeline(
        active_features,
        random_state,
        replacement_component_groups,
        build_trend_proxy_ovr_classifier(random_state),
    )
    model.fit(x_train, y_train)
    return model


def fit_calibrated_trend_proxy_sigmoid(
    train_valid_df: pd.DataFrame,
    active_features: list[str],
    random_state: int,
    replacement_component_groups: dict[str, list[str]],
) -> CalibratedClassifierCV:
    x_train = train_valid_df[active_features]
    y_train = train_valid_df["label"]
    base_model = build_trend_proxy_sector_pipeline(active_features, random_state, replacement_component_groups)
    model = CalibratedClassifierCV(estimator=base_model, method="sigmoid", cv=3)
    model.fit(x_train, y_train)
    return model


def fit_calibrated_ovr_trend_proxy_sigmoid(
    train_valid_df: pd.DataFrame,
    active_features: list[str],
    random_state: int,
    replacement_component_groups: dict[str, list[str]],
) -> CalibratedClassifierCV:
    x_train = train_valid_df[active_features]
    y_train = train_valid_df["label"]
    base_model = build_trend_proxy_linear_pipeline(
        active_features,
        random_state,
        replacement_component_groups,
        build_trend_proxy_ovr_classifier(random_state),
    )
    model = CalibratedClassifierCV(estimator=base_model, method="sigmoid", cv=3)
    model.fit(x_train, y_train)
    return model


def parse_voter_components(raw_value: str) -> list[str]:
    items = [item.strip() for item in raw_value.split(",") if item.strip()]
    if not items:
        raise ValueError("voter component list is empty")
    allowed = {
        "base_05w",
        "persistence_only",
        "persistence_breakout",
        "persistence_volatility",
        "full_proxy",
    }
    missing = [item for item in items if item not in allowed]
    if missing:
        raise ValueError(f"unknown voter components: {missing}")
    return items


def parse_voter_weights(raw_value: str, expected_len: int) -> list[float]:
    items = [item.strip() for item in raw_value.split(",") if item.strip()]
    if len(items) != expected_len:
        raise ValueError(f"expected {expected_len} voter weights, got {len(items)}")
    weights = [float(item) for item in items]
    if any(weight <= 0.0 for weight in weights):
        raise ValueError("all voter weights must be positive")
    return weights


def fit_persistence_frontier_voter(
    train_valid_df: pd.DataFrame,
    active_features: list[str],
    random_state: int,
    voter_components: list[str],
    voter_weights: list[float],
) -> VotingClassifier:
    estimators = build_persistence_frontier_estimators(active_features, random_state, voter_components)
    model = VotingClassifier(
        estimators=estimators,
        voting="soft",
        weights=np.asarray(voter_weights, dtype=np.float64),
        flatten_transform=False,
    )
    x_train = train_valid_df[active_features]
    y_train = train_valid_df["label"]
    model.fit(x_train, y_train)
    return model


def build_persistence_frontier_estimators(
    active_features: list[str],
    random_state: int,
    voter_components: list[str],
) -> list[tuple[str, object]]:
    component_groups_map = {
        "persistence_only": ["trend_proxy_persistence"],
        "persistence_breakout": ["trend_proxy_persistence", "trend_proxy_breakout_pressure"],
        "persistence_volatility": ["trend_proxy_persistence", "trend_proxy_volatility_regime"],
        "full_proxy": list(TREND_PROXY_REPLACEMENT_COMPONENT_GROUPS.keys()),
    }
    estimators: list[tuple[str, object]] = []
    for component_name in voter_components:
        if component_name == "base_05w":
            estimators.append((component_name, build_logistic_pipeline(random_state)))
            continue
        estimators.append(
            (
                component_name,
                build_trend_proxy_sector_pipeline(
                    active_features,
                    random_state,
                    resolve_replacement_component_groups(component_groups_map[component_name]),
                ),
            )
        )
    return estimators


def fit_persistence_frontier_stacker(
    train_valid_df: pd.DataFrame,
    active_features: list[str],
    random_state: int,
    voter_components: list[str],
) -> StackingClassifier:
    estimators = build_persistence_frontier_estimators(active_features, random_state, voter_components)
    model = StackingClassifier(
        estimators=estimators,
        final_estimator=LogisticRegression(
            solver="lbfgs",
            C=0.7,
            class_weight="balanced",
            max_iter=2500,
            random_state=random_state,
        ),
        stack_method="predict_proba",
        passthrough=True,
        cv=3,
    )
    x_train = train_valid_df[active_features]
    y_train = train_valid_df["label"]
    model.fit(x_train, y_train)
    return model


def feature_matrix(df: pd.DataFrame, model_family: str, active_features: list[str]) -> pd.DataFrame | np.ndarray:
    features = df[active_features]
    if model_family == "xgboost":
        return features.to_numpy(dtype=np.float32)
    return features


def parse_drop_sectors(raw_value: str) -> list[str]:
    sectors = [item.strip() for item in raw_value.split(",") if item.strip()]
    missing = [name for name in sectors if name not in SECTOR_MAP]
    if missing:
        raise ValueError(f"unknown drop sectors: {missing}")
    return sectors


def parse_drop_features(raw_value: str) -> list[str]:
    features = [item.strip() for item in raw_value.split(",") if item.strip()]
    missing = [name for name in features if name not in FEATURE_ORDER]
    if missing:
        raise ValueError(f"unknown drop features: {missing}")
    return features


def resolve_active_features(model_family: str, drop_sectors: list[str], drop_features: list[str]) -> list[str]:
    if model_family == "semantic_interaction_logreg":
        removed = set(drop_features)
        if drop_sectors:
            removed.update(feature for sector in drop_sectors for feature in SECTOR_MAP[sector])
        active_features = [feature for feature in SEMANTIC_INTERACTION_FEATURES if feature not in removed]
        if not active_features:
            raise ValueError("semantic interaction feature set became empty after removing requested sectors/features")
        return active_features
    if not drop_sectors:
        active_features = list(FEATURE_ORDER)
    else:
        active_features = feature_order_without_sectors(drop_sectors)
    if drop_features:
        removed = set(drop_features)
        active_features = [feature for feature in active_features if feature not in removed]
    if not active_features:
        raise ValueError("active feature set is empty after removing requested sectors/features")
    return active_features


def build_rule_stack(min_margin: float, max_hold_bars: int) -> dict[str, Any]:
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
                    "max_hold_bars": int(max_hold_bars),
                },
            }
        ],
    }


def load_bundle_metrics(bundle_path: Path, split_name: str) -> dict[str, Any]:
    bundle = json.loads(bundle_path.read_text(encoding="utf-8-sig"))
    split = bundle["results"]["by_split"].get(split_name, {})
    execution_extra = split.get("execution", {}).get("extra", {})
    return {
        "return_pct": split.get("headline", {}).get("return_pct"),
        "profit_factor": split.get("headline", {}).get("profit_factor"),
        "trade_count": split.get("headline", {}).get("trade_count"),
        "max_dd_pct": split.get("headline", {}).get("max_dd_pct"),
        "ulcer_index": split.get("risk", {}).get("ulcer_index"),
        "ready_row_gap": execution_extra.get("ready_row_gap"),
        "unexpected_skip_count": execution_extra.get("unexpected_skip_count"),
    }


def resolve_reference_bundle_path(run_name: str) -> Path:
    candidate_paths = sorted((ROOT_DIR / "stages").glob(f"*/02_runs/active/{run_name}/experiment_bundle.json"))
    if not candidate_paths:
        raise FileNotFoundError(f"could not locate experiment_bundle.json for reference run: {run_name}")
    return candidate_paths[0]


def format_metric(value: Any, digits: int = 4) -> str:
    if value is None:
        return "n/a"
    return f"{float(value):.{digits}f}"


def format_count(value: Any) -> str:
    if value is None:
        return "n/a"
    return str(int(value))


def build_review_payload(
    *,
    args: argparse.Namespace,
    test_metrics: dict[str, Any],
    baseline_stage01: dict[str, Any],
    validation_metrics: dict[str, Any],
    baseline_validation_metrics: dict[str, Any],
    holdout_metrics: dict[str, Any] | None,
    baseline_holdout_metrics: dict[str, Any] | None,
) -> dict[str, Any]:
    ranked_validation = [
        {"run_name": args.run_name, **validation_metrics},
        {"run_name": args.logic_reference_run_name, **baseline_validation_metrics},
    ]
    ranked_validation.sort(key=lambda item: (item["return_pct"] is not None, item["return_pct"]), reverse=True)
    payload: dict[str, Any] = {
        "generated_at_utc": utc_now_iso(),
        "phase": "stage05_mt5_model_family_trial",
        "model_family": args.model_family,
        "logic_reference_run_name": args.logic_reference_run_name,
        "logic_filter": {"type": "max_probability_margin", "min_margin": args.min_margin},
        "logic_exit": {"type": "time_exit", "max_hold_bars": int(args.max_hold_bars)},
        "dropped_sectors": parse_drop_sectors(args.drop_sectors),
        "dropped_features": parse_drop_features(args.drop_features),
        "replacement_sector_name": (
            TREND_PROXY_REPLACEMENT_NAME if args.model_family in REPLACEMENT_SECTOR_MODEL_FAMILIES else None
        ),
        "replacement_sector_components": (
            resolve_replacement_component_groups(parse_replacement_component_groups(args.replacement_component_groups))
            if args.model_family in REPLACEMENT_SECTOR_MODEL_FAMILIES
            else None
        ),
        "voter_components": (
            parse_voter_components(args.voter_components)
            if args.model_family in {"persistence_frontier_voter", "persistence_frontier_stacker"}
            else None
        ),
        "voter_weights": (
            parse_voter_weights(args.voter_weights, len(parse_voter_components(args.voter_components)))
            if args.model_family == "persistence_frontier_voter"
            else None
        ),
        "baseline_stage01_test_confirmation": baseline_stage01["test_confirmation"],
        "trial_model_test_confirmation": test_metrics,
        "ranked_validation_runs": [
            {"rank": index + 1, **item}
            for index, item in enumerate(ranked_validation)
        ],
    }
    if holdout_metrics is not None and baseline_holdout_metrics is not None:
        ranked = [
            {"run_name": args.run_name, **holdout_metrics},
            {"run_name": args.logic_reference_run_name, **baseline_holdout_metrics},
        ]
        ranked.sort(key=lambda item: (item["return_pct"] is not None, item["return_pct"]), reverse=True)
        payload["ranked_test_runs"] = [
            {"rank": index + 1, **item}
            for index, item in enumerate(ranked)
        ]
        trial_holdout_wins = (
            holdout_metrics["return_pct"] is not None
            and baseline_holdout_metrics["return_pct"] is not None
            and holdout_metrics["profit_factor"] is not None
            and baseline_holdout_metrics["profit_factor"] is not None
            and holdout_metrics["return_pct"] > baseline_holdout_metrics["return_pct"]
            and holdout_metrics["profit_factor"] > baseline_holdout_metrics["profit_factor"]
        )
        trial_validation_wins = (
            validation_metrics["return_pct"] is not None
            and baseline_validation_metrics["return_pct"] is not None
            and validation_metrics["profit_factor"] is not None
            and baseline_validation_metrics["profit_factor"] is not None
            and validation_metrics["return_pct"] > baseline_validation_metrics["return_pct"]
            and validation_metrics["profit_factor"] > baseline_validation_metrics["profit_factor"]
        )
        if trial_holdout_wins and trial_validation_wins:
            payload["verdict"] = {
                "status": "promote_candidate",
                "selected_run_name": args.run_name,
                "reason": "trial model improved both validation and holdout versus the incumbent",
            }
        elif trial_holdout_wins and not trial_validation_wins:
            payload["verdict"] = {
                "status": "mixed_holdout_win_keep_incumbent",
                "selected_run_name": args.logic_reference_run_name,
                "reason": "trial model improved holdout return/PF but trailed the incumbent on validation, so the incumbent stays promoted for now",
            }
        else:
            payload["verdict"] = {
                "status": "reject_keep_incumbent",
                "selected_run_name": args.logic_reference_run_name,
                "reason": "trial model did not clear the incumbent on the holdout gate",
            }
    else:
        payload["verdict"] = {
            "status": "validation_only_pending_holdout",
            "selected_run_name": args.logic_reference_run_name,
            "reason": "holdout not run yet, so the incumbent remains the selected bundle",
        }
    return payload


def build_review_markdown(payload: dict[str, Any], run_name: str) -> str:
    baseline = payload["baseline_stage01_test_confirmation"]
    trial = payload["trial_model_test_confirmation"]
    dropped_sectors = payload.get("dropped_sectors") or []
    dropped_features = payload.get("dropped_features") or []
    replacement_sector_name = payload.get("replacement_sector_name")
    replacement_sector_components = payload.get("replacement_sector_components") or {}
    voter_components = payload.get("voter_components") or []
    voter_weights = payload.get("voter_weights") or []
    lines = [
        f"# {run_name} Stage 05 Model Family Trial Review",
        "",
        f"Generated at: `{payload['generated_at_utc']}`",
        "",
        "## Scope",
        "",
        f"- purpose: `train a fresh {payload['model_family']} model on the frozen h/band dataset and run the current reference logic on MT5`",
        f"- logic reference: `{payload['logic_reference_run_name']}` with `min_margin={payload['logic_filter']['min_margin']:.4f}`",
    ]
    if dropped_sectors:
        lines.append(f"- dropped sectors: `{', '.join(dropped_sectors)}`")
    if dropped_features:
        lines.append(f"- dropped features: `{', '.join(dropped_features)}`")
    if replacement_sector_name:
        lines.append(f"- replacement sector: `{replacement_sector_name}`")
        for component_name, source_features in replacement_sector_components.items():
            lines.append(f"- {component_name}: `{', '.join(source_features)}`")
    if voter_components:
        lines.append(f"- voter components: `{', '.join(voter_components)}`")
        lines.append(f"- voter weights: `{', '.join(f'{weight:.3f}' for weight in voter_weights)}`")
    lines.extend(
        [
            "",
            "## Offline Test Confirmation",
            "",
            f"- incumbent Stage 01 test: macro_f1=`{baseline['test_macro_f1']:.4f}`, balanced_accuracy=`{baseline['test_balanced_accuracy']:.4f}`, accuracy=`{baseline['test_accuracy']:.4f}`, log_loss=`{baseline['test_log_loss']:.4f}`",
            f"- trial model test: macro_f1=`{trial['test_macro_f1']:.4f}`, balanced_accuracy=`{trial['test_balanced_accuracy']:.4f}`, accuracy=`{trial['test_accuracy']:.4f}`, log_loss=`{trial['test_log_loss']:.4f}`",
            "",
            "## MT5 Validation Ranking",
            "",
        ]
    )
    for row in payload["ranked_validation_runs"]:
        lines.append(
            f"- [{row['rank']}] `{row['run_name']}`: "
            f"return_pct={format_metric(row['return_pct'], 3)}, profit_factor={format_metric(row['profit_factor'], 4)}, "
            f"max_dd_pct={format_metric(row['max_dd_pct'], 4)}, ulcer_index={format_metric(row['ulcer_index'], 4)}, "
            f"trades={format_count(row['trade_count'])}, ready_gap={row['ready_row_gap']}, unexpected_skips={row['unexpected_skip_count']}"
        )
    ranked_test_runs = payload.get("ranked_test_runs")
    if ranked_test_runs:
        lines.extend(["", "## MT5 Holdout Ranking", ""])
        for row in ranked_test_runs:
            lines.append(
                f"- [{row['rank']}] `{row['run_name']}`: "
                f"return_pct={format_metric(row['return_pct'], 3)}, profit_factor={format_metric(row['profit_factor'], 4)}, "
                f"max_dd_pct={format_metric(row['max_dd_pct'], 4)}, ulcer_index={format_metric(row['ulcer_index'], 4)}, "
                f"trades={format_count(row['trade_count'])}, ready_gap={row['ready_row_gap']}, unexpected_skips={row['unexpected_skip_count']}"
            )
    verdict = payload.get("verdict", {})
    if verdict:
        lines.extend(["", "## Verdict", ""])
        lines.append(f"- status: `{verdict.get('status')}`")
        lines.append(f"- selected_run_name: `{verdict.get('selected_run_name')}`")
        lines.append(f"- reason: `{verdict.get('reason')}`")
    lines.extend(["", "## Read", ""])
    validation_leader = payload["ranked_validation_runs"][0]["run_name"]
    lines.append(f"- validation leader: `{validation_leader}`")
    if ranked_test_runs:
        lines.append(f"- holdout winner: `{ranked_test_runs[0]['run_name']}`")
    lines.append("- read: `treat model-family swaps with the same holdout gate as logic sweeps; validation spikes alone are not enough`")
    return "\n".join(lines) + "\n"


def update_review_index(review_dir: Path, run_tag: str, review_basename: str) -> None:
    existing_lines = []
    review_index_path = review_dir / "review_index.md"
    if review_index_path.exists():
        existing_lines = review_index_path.read_text(encoding="utf-8").splitlines()
    bullet = f"- `{run_tag}`: see `{review_basename}.md`"
    if bullet not in existing_lines:
        existing_lines.insert(8 if len(existing_lines) >= 8 else len(existing_lines), bullet)
    write_text(review_index_path, "\n".join(existing_lines).rstrip() + "\n")


def main() -> int:
    args = build_parser().parse_args()
    drop_sectors = parse_drop_sectors(args.drop_sectors)
    drop_features = parse_drop_features(args.drop_features)
    active_features = resolve_active_features(args.model_family, drop_sectors, drop_features)
    replacement_component_groups = resolve_replacement_component_groups(
        parse_replacement_component_groups(args.replacement_component_groups)
    )
    voter_components = (
        parse_voter_components(args.voter_components)
        if args.model_family in {"persistence_frontier_voter", "persistence_frontier_stacker"}
        else []
    )
    voter_weights = (
        parse_voter_weights(args.voter_weights, len(voter_components))
        if args.model_family == "persistence_frontier_voter"
        else []
    )

    stage_root = ROOT_DIR / args.stage_root
    dataset_path = ROOT_DIR / args.dataset_path
    run_dir = stage_root / "02_runs" / "active" / args.run_name
    review_dir = stage_root / "03_reviews"
    run_dir.mkdir(parents=True, exist_ok=True)
    review_dir.mkdir(parents=True, exist_ok=True)

    dataset = pd.read_parquet(dataset_path)
    train_valid_df = dataset[dataset["split"].isin(["train", "valid"])].copy()
    test_df = dataset[dataset["split"].eq("test")].copy()

    config = {
        "run_name": args.run_name,
        "phase": "stage05_model_family_trial",
        "generated_at_utc": utc_now_iso(),
        "model_family": args.model_family,
        "horizon_bars": int(args.horizon_bars),
        "band": float(args.band),
        "dataset_path": str(dataset_path.relative_to(ROOT_DIR)),
        "refit_policy": "train_plus_valid_refit_then_mt5_validation",
        "logic_reference_run_name": args.logic_reference_run_name,
        "logic_filter": {"type": "max_probability_margin", "min_margin": float(args.min_margin)},
        "logic_exit": {"type": "time_exit", "max_hold_bars": int(args.max_hold_bars)},
        "dropped_sectors": drop_sectors,
        "dropped_features": drop_features,
        "replacement_sector_name": (
            TREND_PROXY_REPLACEMENT_NAME if args.model_family in REPLACEMENT_SECTOR_MODEL_FAMILIES else None
        ),
        "replacement_sector_components": (
            replacement_component_groups if args.model_family in REPLACEMENT_SECTOR_MODEL_FAMILIES else None
        ),
        "voter_components": voter_components if args.model_family in {"persistence_frontier_voter", "persistence_frontier_stacker"} else None,
        "voter_weights": voter_weights if args.model_family == "persistence_frontier_voter" else None,
        "active_input_features": active_features,
        "row_counts": {"train_valid": int(len(train_valid_df)), "test": int(len(test_df))},
        "class_counts": {
            "train_valid": class_counts(train_valid_df["label"]),
            "test": class_counts(test_df["label"]),
        },
    }
    write_json(run_dir / "config.json", config)

    if args.model_family == "logistic_regression":
        model = fit_logistic(train_valid_df, active_features, args.random_state)
    elif args.model_family == "elasticnet_logreg":
        model = fit_elasticnet_logreg(train_valid_df, active_features, args.random_state)
    elif args.model_family == "pca_logreg":
        model = fit_pca_logreg(train_valid_df, active_features, args.random_state)
    elif args.model_family == "regularized_logreg_voter":
        model = fit_regularized_logreg_voter(train_valid_df, active_features, args.random_state)
    elif args.model_family == "lightgbm":
        model = fit_lightgbm(train_valid_df, active_features, args.random_state)
    elif args.model_family == "catboost":
        model = fit_catboost(train_valid_df, active_features, args.random_state)
    elif args.model_family == "xgboost":
        model = fit_xgboost(train_valid_df, active_features, args.random_state)
    elif args.model_family == "random_forest":
        model = fit_random_forest(train_valid_df, active_features, args.random_state)
    elif args.model_family == "extra_trees":
        model = fit_extra_trees(train_valid_df, active_features, args.random_state)
    elif args.model_family == "semantic_interaction_logreg":
        model = fit_semantic_interaction_logreg(train_valid_df, active_features, args.random_state)
    elif args.model_family == "trend_proxy_sector_logreg":
        model = fit_trend_proxy_sector_logreg(
            train_valid_df,
            active_features,
            args.random_state,
            replacement_component_groups,
        )
    elif args.model_family == "ovr_trend_proxy_logreg":
        model = fit_ovr_trend_proxy_logreg(
            train_valid_df,
            active_features,
            args.random_state,
            replacement_component_groups,
        )
    elif args.model_family == "calibrated_trend_proxy_sigmoid":
        model = fit_calibrated_trend_proxy_sigmoid(
            train_valid_df,
            active_features,
            args.random_state,
            replacement_component_groups,
        )
    elif args.model_family == "calibrated_ovr_trend_proxy_sigmoid":
        model = fit_calibrated_ovr_trend_proxy_sigmoid(
            train_valid_df,
            active_features,
            args.random_state,
            replacement_component_groups,
        )
    elif args.model_family == "persistence_frontier_voter":
        model = fit_persistence_frontier_voter(
            train_valid_df,
            active_features,
            args.random_state,
            voter_components,
            voter_weights,
        )
    elif args.model_family == "persistence_frontier_stacker":
        model = fit_persistence_frontier_stacker(
            train_valid_df,
            active_features,
            args.random_state,
            voter_components,
        )
    else:
        raise ValueError(f"unsupported model family: {args.model_family}")

    x_test = feature_matrix(test_df, args.model_family, active_features)
    y_test = test_df["label"].to_numpy(dtype=np.int64)
    y_proba = model.predict_proba(x_test)
    y_pred = np.argmax(y_proba, axis=1)

    joblib.dump(model, run_dir / "model.joblib")
    save_test_outputs(run_dir, test_df, y_pred, y_proba)

    test_metrics = {
        "run_name": args.run_name,
        "model_family": args.model_family,
        "test_rows": int(len(test_df)),
        "test_macro_f1": float(f1_score(y_test, y_pred, average="macro")),
        "test_balanced_accuracy": float(balanced_accuracy_score(y_test, y_pred)),
        "test_accuracy": float(accuracy_score(y_test, y_pred)),
        "test_log_loss": float(log_loss(y_test, y_proba, labels=[0, 1, 2])),
    }
    write_json(run_dir / "metrics.json", test_metrics)

    rule_stack_path = run_dir / "rule_stack.json"
    write_json(rule_stack_path, build_rule_stack(args.min_margin, args.max_hold_bars))

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
            max_hold_bars=args.max_hold_bars,
            build_bundle=True,
        )
        run_export_bundle_assets(export_args)

    run_tester(bundle_path, split_name="validation", enable_trading=True)
    if args.run_holdout:
        run_tester(bundle_path, split_name="test", enable_trading=True)

    baseline_stage01 = json.loads(
        (ROOT_DIR / "stages" / "01_base_feature_ml" / "04_selected" / "01D_final_stage01_selection.json").read_text(
            encoding="utf-8"
        )
    )
    baseline_bundle_path = resolve_reference_bundle_path(args.logic_reference_run_name)

    validation_metrics = load_bundle_metrics(bundle_path, "validation")
    baseline_validation_metrics = load_bundle_metrics(baseline_bundle_path, "validation")
    holdout_metrics = load_bundle_metrics(bundle_path, "test") if args.run_holdout else None
    baseline_holdout_metrics = load_bundle_metrics(baseline_bundle_path, "test") if args.run_holdout else None

    review_payload = build_review_payload(
        args=args,
        test_metrics=test_metrics,
        baseline_stage01=baseline_stage01,
        validation_metrics=validation_metrics,
        baseline_validation_metrics=baseline_validation_metrics,
        holdout_metrics=holdout_metrics,
        baseline_holdout_metrics=baseline_holdout_metrics,
    )
    review_json_path = review_dir / f"{args.review_basename}.json"
    review_md_path = review_dir / f"{args.review_basename}.md"
    write_json(review_json_path, review_payload)
    write_text(review_md_path, build_review_markdown(review_payload, args.stage_id))

    update_review_index(review_dir, args.stage_id, args.review_basename)

    print(f"[done] run_dir={run_dir}")
    print(f"[done] bundle={bundle_path}")
    print(f"[done] review_md={review_md_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
