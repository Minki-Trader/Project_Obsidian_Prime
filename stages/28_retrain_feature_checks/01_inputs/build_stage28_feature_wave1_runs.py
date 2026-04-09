#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
import sys
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path

import joblib
import pandas as pd
from sklearn.metrics import accuracy_score, balanced_accuracy_score, f1_score, log_loss

ROOT_DIR = Path(__file__).resolve().parents[3]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from foundation.pipelines.experiment_bundle_models import ExperimentBundle, ResultsBlock, StatusEvent  # noqa: E402
from foundation.pipelines.export_experiment_bundle_assets import run_export_bundle_assets  # noqa: E402
from foundation.pipelines.run_stage05_mt5_model_family_trial import (  # noqa: E402
    fit_ovr_trend_proxy_logreg,
    save_test_outputs,
)
from foundation.pipelines.stage_reporting import write_json  # noqa: E402


UTC = timezone.utc
STAGE_DIR = Path(__file__).resolve().parents[1]
ACTIVE_RUNS_DIR = STAGE_DIR / "02_runs" / "active"
BASE_OVERLAY_RUN_DIR = (
    ROOT_DIR
    / "stages"
    / "18_directional_core_overlay_matrix"
    / "02_runs"
    / "active"
    / "18E_2501_17e_ph20_0001"
)
SOURCE_CORE_RUN_DIR = (
    ROOT_DIR
    / "stages"
    / "17_09c_directional_core_fork"
    / "02_runs"
    / "active"
    / "17E_2501_ovr_balanced_0001"
)

SOURCE_CONFIG = json.loads((SOURCE_CORE_RUN_DIR / "config.json").read_text(encoding="utf-8"))
BASE_BUNDLE = ExperimentBundle.from_json(
    (BASE_OVERLAY_RUN_DIR / "experiment_bundle.json").read_text(encoding="utf-8-sig")
)

PERSISTENCE_ONLY_DROP = {
    "vix_change_1",
    "vix_zscore_20",
    "us10yr_change_1",
    "us10yr_zscore_20",
    "usdx_change_1",
    "usdx_zscore_20",
}
SESSIONLESS_DROP = {
    "is_us_cash_open",
    "minutes_from_cash_open",
    "is_first_30m_after_open",
    "is_last_30m_before_cash_close",
}
EXTERNAL_BREADTHLESS_DROP = {
    "nvda_xnas_log_return_1",
    "aapl_xnas_log_return_1",
    "msft_xnas_log_return_1",
    "amzn_xnas_log_return_1",
    "mega8_equal_return_1",
    "top3_weighted_return_1",
    "mega8_pos_breadth_1",
    "mega8_dispersion_5",
    "us100_minus_mega8_equal_return_1",
    "us100_minus_top3_weighted_return_1",
}

RUNS = [
    {
        "stage_id": "28A",
        "folder_name": "28A_18e_full54_ph20_0001",
        "experiment_id": "exp_28a_18e_full54_ph20_v1",
        "label": "full 17E feature reference under 18E PH20 overlay",
        "drop_features": set(),
        "replacement_component_groups": {
            "trend_proxy_persistence": SOURCE_CONFIG["replacement_sector_components"]["trend_proxy_persistence"],
            "trend_proxy_risk_off_confirmation": SOURCE_CONFIG["replacement_sector_components"][
                "trend_proxy_risk_off_confirmation"
            ],
        },
        "feature_variant": "full54",
    },
    {
        "stage_id": "28B",
        "folder_name": "28B_18e_persist48_ph20_0001",
        "experiment_id": "exp_28b_18e_persist48_ph20_v1",
        "label": "persistence-only compact fork under 18E PH20 overlay",
        "drop_features": PERSISTENCE_ONLY_DROP,
        "replacement_component_groups": {
            "trend_proxy_persistence": SOURCE_CONFIG["replacement_sector_components"]["trend_proxy_persistence"],
        },
        "feature_variant": "persistence_only_48",
    },
    {
        "stage_id": "28C",
        "folder_name": "28C_18e_sessionless50_ph20_0001",
        "experiment_id": "exp_28c_18e_sessionless50_ph20_v1",
        "label": "sessionless compact fork under 18E PH20 overlay",
        "drop_features": SESSIONLESS_DROP,
        "replacement_component_groups": {
            "trend_proxy_persistence": SOURCE_CONFIG["replacement_sector_components"]["trend_proxy_persistence"],
            "trend_proxy_risk_off_confirmation": SOURCE_CONFIG["replacement_sector_components"][
                "trend_proxy_risk_off_confirmation"
            ],
        },
        "feature_variant": "sessionless_50",
    },
    {
        "stage_id": "28D",
        "folder_name": "28D_18e_extless44_ph20_0001",
        "experiment_id": "exp_28d_18e_extless44_ph20_v1",
        "label": "external-breadthless compact fork under 18E PH20 overlay",
        "drop_features": EXTERNAL_BREADTHLESS_DROP,
        "replacement_component_groups": {
            "trend_proxy_persistence": SOURCE_CONFIG["replacement_sector_components"]["trend_proxy_persistence"],
            "trend_proxy_risk_off_confirmation": SOURCE_CONFIG["replacement_sector_components"][
                "trend_proxy_risk_off_confirmation"
            ],
        },
        "feature_variant": "external_breadthless_44",
    },
]


def utc_now_iso() -> str:
    return datetime.now(tz=UTC).isoformat()


def build_status_history() -> list[StatusEvent]:
    now = utc_now_iso()
    return [
        StatusEvent(status="draft", changed_at_utc=now, reason="bundle_initialized_from_18E_lineage_reference"),
        StatusEvent(status="ready", changed_at_utc=now, reason="stage28_feature_wave1_prepared"),
    ]


def variant_features(drop_features: set[str]) -> list[str]:
    return [feature for feature in SOURCE_CONFIG["active_input_features"] if feature not in drop_features]


def evaluate_split(model, split_df: pd.DataFrame, active_features: list[str]) -> dict[str, float]:
    x_frame = split_df[active_features]
    y_true = split_df["label"]
    y_proba = model.predict_proba(x_frame)
    y_pred = model.predict(x_frame)
    return {
        "rows": int(len(split_df)),
        "macro_f1": float(f1_score(y_true, y_pred, average="macro")),
        "balanced_accuracy": float(balanced_accuracy_score(y_true, y_pred)),
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "log_loss": float(log_loss(y_true, y_proba, labels=[0, 1, 2])),
    }


def build_config(run: dict[str, object], active_features: list[str]) -> dict[str, object]:
    config = deepcopy(SOURCE_CONFIG)
    config["run_name"] = run["folder_name"]
    config["phase"] = "stage28_retrain_feature_checks"
    config["generated_at_utc"] = utc_now_iso()
    config["active_input_features"] = active_features
    config["feature_simplification_check"] = {
        "source_core_run_name": SOURCE_CONFIG["run_name"],
        "source_overlay_run_name": BASE_OVERLAY_RUN_DIR.name,
        "feature_variant": run["feature_variant"],
        "drop_features": sorted(run["drop_features"]),
    }
    return config


def main() -> int:
    dataset_path = ROOT_DIR / SOURCE_CONFIG["dataset_path"]
    dataset = pd.read_parquet(dataset_path)
    train_df = dataset.loc[dataset["split"].eq("train")].copy()
    valid_df = dataset.loc[dataset["split"].eq("valid")].copy()
    test_df = dataset.loc[dataset["split"].eq("test")].copy()

    rule_stack_payload = BASE_BUNDLE.rule_stack.model_dump(mode="json", exclude_none=False)

    for run in RUNS:
        run_dir = ACTIVE_RUNS_DIR / str(run["folder_name"])
        if run_dir.exists():
            raise FileExistsError(f"target run directory already exists: {run_dir}")

        run_dir.mkdir(parents=True, exist_ok=False)

        active_features = variant_features(run["drop_features"])
        model = fit_ovr_trend_proxy_logreg(
            train_df,
            active_features,
            random_state=42,
            replacement_component_groups=run["replacement_component_groups"],
        )

        config_payload = build_config(run, active_features)
        write_json(run_dir / "config.json", config_payload)
        write_json(run_dir / "rule_stack.json", rule_stack_payload)
        joblib.dump(model, run_dir / "model.joblib")

        test_proba = model.predict_proba(test_df[active_features])
        test_pred = model.predict(test_df[active_features])
        save_test_outputs(run_dir, test_df, test_pred, test_proba)

        offline_metrics = {
            "generated_at_utc": utc_now_iso(),
            "feature_count": len(active_features),
            "feature_names": active_features,
            "split_metrics": {
                "train": evaluate_split(model, train_df, active_features),
                "validation": evaluate_split(model, valid_df, active_features),
                "test": evaluate_split(model, test_df, active_features),
            },
        }
        write_json(run_dir / "offline_metrics.json", offline_metrics)

        export_args = argparse.Namespace(
            run_dir=str(run_dir),
            experiment_id=run["experiment_id"],
            stage_id=run["stage_id"],
            output_dir=str(run_dir),
            stage_name="retrain_feature_checks",
            bundle_version="1.0.0",
            created_by="python_orchestrator",
            config_json=str(run_dir / "config.json"),
            dataset_path=None,
            selection_json=None,
            logic_family=None,
            selection_key=None,
            rule_stack_json=str(run_dir / "rule_stack.json"),
            smoke_split="test",
            smoke_row_index=0,
            max_hold_bars=4,
            sizing_mode="risk_pct",
            fixed_lot=0.1,
            risk_pct=2.0,
            capital_base="balance",
            stop_model="atr",
            stop_execution_mode="broker_native",
            stop_policy="direction_split",
            stop_atr_period=14,
            stop_atr_mult=None,
            stop_long_atr_mult=1.4,
            stop_short_atr_mult=2.0,
            stop_low_vol_threshold=None,
            stop_high_vol_threshold=None,
            stop_low_atr_mult=None,
            stop_mid_atr_mult=None,
            stop_high_atr_mult=None,
            build_bundle=True,
        )
        run_export_bundle_assets(export_args)

        bundle_path = run_dir / "experiment_bundle.json"
        bundle = ExperimentBundle.from_json(bundle_path.read_text(encoding="utf-8-sig"))
        bundle.identity.stage_name = "retrain_feature_checks"
        bundle.identity.bundle_status = "ready"
        bundle.identity.created_at_utc = utc_now_iso()
        bundle.status_history = build_status_history()
        bundle.results = ResultsBlock()
        bundle.run_attempts = []
        bundle.runtime_snapshot.extra = deepcopy(BASE_BUNDLE.runtime_snapshot.extra)
        bundle.runtime_snapshot.extra.update(
            {
                "source_core_run_name": SOURCE_CONFIG["run_name"],
                "source_overlay_run_name": BASE_OVERLAY_RUN_DIR.name,
                "feature_variant": run["feature_variant"],
            }
        )
        bundle.data_snapshot.extra = deepcopy(BASE_BUNDLE.data_snapshot.extra or {})
        bundle.data_snapshot.extra.update(
            {
                "run_name": str(run["folder_name"]),
                "candidate_stage_id": run["stage_id"],
                "candidate_label": run["label"],
                "source_overlay_run_name": BASE_OVERLAY_RUN_DIR.name,
                "source_core_run_name": SOURCE_CONFIG["run_name"],
                "feature_variant": run["feature_variant"],
            }
        )
        bundle_path.write_text(bundle.to_json(indent=2), encoding="utf-8")

        overlay_manifest = {
            "generated_at_utc": utc_now_iso(),
            "run_name": run["folder_name"],
            "experiment_id": run["experiment_id"],
            "source_run_dir": str(SOURCE_CORE_RUN_DIR),
            "source_run_name": SOURCE_CONFIG["run_name"],
            "source_core_stage_id": "17E",
            "source_core_label": "09C_ovr_balanced",
            "overlay_token": "PH20",
            "overlay_label": "postcash_hold_cut",
            "overlay": {
                "risk_pct": 2.0,
                "stop_policy": "direction_split",
                "stop_long_atr_mult": 1.4,
                "stop_short_atr_mult": 2.0,
                "stop_atr_period": 14,
                "monday_risk_pct_mult": 0.75,
                "ny_postcash_risk_pct_mult": 0.7,
                "ny_postcash_hold_cap_bars": 3,
                "session_overlay_label": "postcash_hold_cut",
            },
            "feature_variant": run["feature_variant"],
        }
        write_json(run_dir / "overlay_manifest.json", overlay_manifest)
        print(f"[done] created={run_dir}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
