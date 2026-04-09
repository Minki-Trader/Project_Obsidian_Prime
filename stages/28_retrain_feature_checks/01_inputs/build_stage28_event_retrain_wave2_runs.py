#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import shutil
import subprocess
import sys
from collections import Counter
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import joblib
import pandas as pd
from pandas import Timestamp
from sklearn.metrics import accuracy_score, balanced_accuracy_score, f1_score, log_loss

ROOT_DIR = Path(__file__).resolve().parents[3]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from foundation.pipelines.experiment_bundle_models import ExperimentBundle, ResultsBlock, StatusEvent  # noqa: E402
from foundation.pipelines.export_experiment_bundle_assets import run_export_bundle_assets  # noqa: E402
from foundation.pipelines.run_mt5_bundle_tester import (  # noqa: E402
    classify_skip_reasons,
    parse_governance_csv,
    parse_shadow_csv,
    parse_trade_ledger,
    summarize_financial_metrics,
)
from foundation.pipelines.run_stage05_mt5_model_family_trial import (  # noqa: E402
    fit_ovr_trend_proxy_logreg,
    save_test_outputs,
)
from foundation.pipelines.stage_reporting import code, write_json, write_markdown  # noqa: E402


UTC = timezone.utc
STAGE_DIR = Path(__file__).resolve().parents[1]
ACTIVE_RUNS_DIR = STAGE_DIR / "02_runs" / "active"
SOURCE_RUN_DIR = ACTIVE_RUNS_DIR / "28B_18e_persist48_ph20_0001"
SOURCE_CONFIG = json.loads((SOURCE_RUN_DIR / "config.json").read_text(encoding="utf-8"))
SOURCE_BUNDLE = ExperimentBundle.from_json((SOURCE_RUN_DIR / "experiment_bundle.json").read_text(encoding="utf-8-sig"))
RULE_STACK_PATH = SOURCE_RUN_DIR / "rule_stack.json"
SOURCE_DATASET_PATH = ROOT_DIR / SOURCE_CONFIG["dataset_path"]
ACTIVE_FEATURE_SET = set(SOURCE_CONFIG["active_input_features"])
RETRAIN_REPLACEMENT_COMPONENTS = {
    group_name: [feature for feature in features if feature in ACTIVE_FEATURE_SET]
    for group_name, features in SOURCE_CONFIG["replacement_sector_components"].items()
}
RETRAIN_REPLACEMENT_COMPONENTS = {
    group_name: features for group_name, features in RETRAIN_REPLACEMENT_COMPONENTS.items() if features
}

WINDOW_START = Timestamp("2025-01-01T00:00:00Z")
WINDOW_END = Timestamp("2026-03-01T00:00:00Z")
LOOKBACK_TRADING_DAYS = 42
INITIAL_DEPOSIT = 500.0
RANDOM_STATE = 42

GOVERNANCE_ARGS = [
    "--enable-governance",
    "--governance-window-bars",
    "144",
    "--governance-min-samples",
    "48",
    "--governance-max-operational-skip-rate",
    "0.40",
    "--governance-max-external-skip-rate",
    "0.36",
    "--governance-max-feature-skip-rate",
    "0.10",
    "--governance-max-consecutive-operational-skips",
    "12",
    "--governance-max-argmax-class-share",
    "0.82",
    "--governance-max-extreme-confidence-rate",
    "0.60",
    "--governance-extreme-confidence-threshold",
    "0.97",
    "--governance-min-normalized-entropy",
    "0.88",
]

RUNS = [
    {
        "stage_id": "28E",
        "folder_name": "28E_28b_fixedcarry_long14m_0001",
        "experiment_prefix": "exp_28e_28b_fixedcarry",
        "label": "28B compact fixed-carry stitched reference",
        "mode": "fixed_carry",
        "trigger_label": "none",
    },
    {
        "stage_id": "28F",
        "folder_name": "28F_28b_2m_monthly_long14m_0001",
        "experiment_prefix": "exp_28f_28b_monthly2m",
        "label": "28B compact monthly 2M retrain stitched challenger",
        "mode": "monthly_retrain",
        "trigger_label": "always_retrain",
    },
    {
        "stage_id": "28G",
        "folder_name": "28G_28b_negpf_trigger_long14m_0001",
        "experiment_prefix": "exp_28g_28b_negpf",
        "label": "28B compact event-triggered 2M retrain stitched challenger",
        "mode": "event_triggered",
        "trigger_label": "prev_month_return_lt_0_or_pf_lt_1",
    },
]


def utc_now_iso() -> str:
    return datetime.now(tz=UTC).isoformat()


def month_start_range() -> list[Timestamp]:
    return list(pd.date_range(WINDOW_START, WINDOW_END, inclusive="left", freq="MS", tz="UTC"))


def month_token(month_start: Timestamp) -> str:
    return month_start.strftime("%Y_%m")


def month_dir_token(month_start: Timestamp) -> str:
    return f"m{month_start.strftime('%y%m')}"


def format_mt5_date(value: Timestamp) -> str:
    return value.strftime("%Y.%m.%d")


def build_status_history(reason: str) -> list[StatusEvent]:
    now = utc_now_iso()
    return [
        StatusEvent(status="draft", changed_at_utc=now, reason="bundle_initialized_from_stage28b_compact_reference"),
        StatusEvent(status="ready", changed_at_utc=now, reason=reason),
    ]


def evaluate_split(model: object, split_df: pd.DataFrame, active_features: list[str]) -> dict[str, float]:
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


def load_dataset() -> pd.DataFrame:
    dataset = pd.read_parquet(SOURCE_DATASET_PATH)
    return dataset.sort_values("timestamp").reset_index(drop=True)


def build_month_slice(dataset: pd.DataFrame, current_month_start: Timestamp) -> dict[str, Any]:
    current_month_end = current_month_start + pd.offsets.MonthBegin(1)
    prior_rows = dataset.loc[dataset["timestamp"] < current_month_start].copy()
    prior_trade_days = pd.DatetimeIndex(prior_rows["timestamp"].dt.normalize().drop_duplicates().sort_values())
    selected_trade_days = prior_trade_days[-LOOKBACK_TRADING_DAYS:]
    if len(selected_trade_days) != LOOKBACK_TRADING_DAYS:
        raise ValueError(f"insufficient trade days before {current_month_start} for lookback {LOOKBACK_TRADING_DAYS}")

    selected_day_set = set(selected_trade_days.tolist())
    train_df = prior_rows.loc[prior_rows["timestamp"].dt.normalize().isin(selected_day_set)].copy()
    test_df = dataset.loc[
        (dataset["timestamp"] >= current_month_start) & (dataset["timestamp"] < current_month_end)
    ].copy()
    if train_df.empty or test_df.empty:
        raise ValueError(f"empty train/test slice for month {month_token(current_month_start)}")

    return {
        "month_start": current_month_start,
        "month_end": current_month_end,
        "month_token": month_token(current_month_start),
        "month_dir_token": month_dir_token(current_month_start),
        "selected_trade_days": [day.isoformat() for day in selected_trade_days],
        "train_df": train_df,
        "test_df": test_df,
    }


def build_base_config(run_name: str) -> dict[str, Any]:
    payload = deepcopy(SOURCE_CONFIG)
    payload["run_name"] = run_name
    payload["phase"] = "stage28_retrain_feature_checks"
    payload["generated_at_utc"] = utc_now_iso()
    return payload


def build_month_config(
    *,
    run_name: str,
    arm: dict[str, Any],
    month_slice: dict[str, Any],
    model_origin: dict[str, Any],
    retrain_applied: bool,
    trigger_reason: str | None,
) -> dict[str, Any]:
    payload = build_base_config(run_name)
    payload["event_retrain_wave"] = {
        "wave": "event_triggered_retrain_wave1",
        "arm_stage_id": arm["stage_id"],
        "arm_label": arm["label"],
        "mode": arm["mode"],
        "month_token": month_slice["month_token"],
        "lookback_label": "2M",
        "lookback_mode": "trading_days",
        "lookback_trading_days": LOOKBACK_TRADING_DAYS,
        "retrain_applied": retrain_applied,
        "trigger_reason": trigger_reason,
        "model_origin": model_origin,
        "lineage_candidate": "28B_18e_persist48_ph20_0001",
    }
    return payload


def write_rule_stack(run_dir: Path) -> None:
    shutil.copy2(RULE_STACK_PATH, run_dir / "rule_stack.json")


def copy_model_artifacts(source_model_path: Path, run_dir: Path) -> None:
    shutil.copy2(source_model_path, run_dir / "model.joblib")


def write_offline_outputs(model: object, run_dir: Path, month_slice: dict[str, Any]) -> None:
    active_features = SOURCE_CONFIG["active_input_features"]
    test_df = month_slice["test_df"]
    test_proba = model.predict_proba(test_df[active_features])
    test_pred = model.predict(test_df[active_features])
    save_test_outputs(run_dir, test_df, test_pred, test_proba)
    offline_metrics = {
        "generated_at_utc": utc_now_iso(),
        "feature_count": len(active_features),
        "feature_names": active_features,
        "split_metrics": {
            "train": evaluate_split(model, month_slice["train_df"], active_features),
            "test": evaluate_split(model, test_df, active_features),
        },
    }
    write_json(run_dir / "offline_metrics.json", offline_metrics)


def train_month_model(
    *,
    run_dir: Path,
    month_slice: dict[str, Any],
    run_name: str,
    arm: dict[str, Any],
    trigger_reason: str | None,
) -> tuple[Path, dict[str, Any]]:
    model = fit_ovr_trend_proxy_logreg(
        month_slice["train_df"],
        SOURCE_CONFIG["active_input_features"],
        random_state=RANDOM_STATE,
        replacement_component_groups=RETRAIN_REPLACEMENT_COMPONENTS,
    )
    model_path = run_dir / "model.joblib"
    joblib.dump(model, model_path)
    model_origin = {
        "kind": "retrained",
        "source_run_name": "28B_18e_persist48_ph20_0001",
        "retrained_for_month": month_slice["month_token"],
        "trigger_reason": trigger_reason,
    }
    config_payload = build_month_config(
        run_name=run_name,
        arm=arm,
        month_slice=month_slice,
        model_origin=model_origin,
        retrain_applied=True,
        trigger_reason=trigger_reason,
    )
    write_json(run_dir / "config.json", config_payload)
    write_rule_stack(run_dir)
    write_offline_outputs(model, run_dir, month_slice)
    return model_path, model_origin


def prepare_carried_model(
    *,
    run_dir: Path,
    month_slice: dict[str, Any],
    run_name: str,
    arm: dict[str, Any],
    model_descriptor: dict[str, Any],
    trigger_reason: str | None,
) -> None:
    copy_model_artifacts(Path(model_descriptor["model_path"]), run_dir)
    config_payload = build_month_config(
        run_name=run_name,
        arm=arm,
        month_slice=month_slice,
        model_origin=model_descriptor["origin"],
        retrain_applied=False,
        trigger_reason=trigger_reason,
    )
    write_json(run_dir / "config.json", config_payload)
    write_rule_stack(run_dir)
    model = joblib.load(run_dir / "model.joblib")
    write_offline_outputs(model, run_dir, month_slice)


def export_month_bundle(
    *,
    run_dir: Path,
    arm: dict[str, Any],
    month_slice: dict[str, Any],
    deposit_in: float,
) -> Path:
    export_args = argparse.Namespace(
        run_dir=str(run_dir),
        experiment_id=f"{arm['experiment_prefix']}_{month_slice['month_start'].strftime('%Y%m')}_v1",
        stage_id=arm["stage_id"],
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
    bundle.status_history = build_status_history("stage28_event_retrain_wave1_prepared")
    bundle.results = ResultsBlock()
    bundle.run_attempts = []
    bundle.runtime_snapshot.deposit = float(deposit_in)
    bundle.runtime_snapshot.extra = deepcopy(SOURCE_BUNDLE.runtime_snapshot.extra)
    bundle.runtime_snapshot.extra.update(
        {
            "stage28_wave": "event_triggered_retrain_wave1",
            "lineage_candidate": "28B_18e_persist48_ph20_0001",
            "month_token": month_slice["month_token"],
            "window_token": "2501",
        }
    )
    bundle.data_snapshot.split_boundaries.train_start_utc = month_slice["train_df"]["timestamp"].min().isoformat()
    bundle.data_snapshot.split_boundaries.train_end_utc_exclusive = month_slice["month_start"].isoformat()
    bundle.data_snapshot.split_boundaries.validation_end_utc_exclusive = month_slice["month_start"].isoformat()
    bundle.data_snapshot.split_boundaries.test_end_utc_exclusive = month_slice["month_end"].isoformat()
    bundle.data_snapshot.split_counts = {
        "train": int(len(month_slice["train_df"])),
        "test": int(len(month_slice["test_df"])),
    }
    bundle.data_snapshot.extra = deepcopy(SOURCE_BUNDLE.data_snapshot.extra or {})
    bundle.data_snapshot.extra.update(
        {
            "month_token": month_slice["month_token"],
            "month_start_utc": month_slice["month_start"].isoformat(),
            "month_end_utc_exclusive": month_slice["month_end"].isoformat(),
            "lookback_label": "2M",
            "lookback_mode": "trading_days",
            "lookback_trading_days": LOOKBACK_TRADING_DAYS,
            "selected_trade_days_utc": month_slice["selected_trade_days"],
            "window_token": "2501",
        }
    )
    bundle_path.write_text(bundle.to_json(indent=2), encoding="utf-8")
    return bundle_path


def run_tester(bundle_path: Path, month_slice: dict[str, Any]) -> dict[str, Any]:
    cmd = [
        sys.executable,
        str(ROOT_DIR / "foundation" / "pipelines" / "run_mt5_bundle_tester.py"),
        "--bundle-json",
        str(bundle_path),
        "--split-name",
        "test",
        "--from-date",
        format_mt5_date(month_slice["month_start"]),
        "--to-date",
        format_mt5_date(month_slice["month_end"]),
        "--enable-trading",
        "--skip-leaderboard-refresh",
        *GOVERNANCE_ARGS,
    ]
    subprocess.run(cmd, cwd=ROOT_DIR, check=True)

    summary_path = bundle_path.parent / "mt5_attempts" / "att_0001" / "tester_attempt_summary.json"
    if not summary_path.exists():
        raise FileNotFoundError(f"missing attempt summary: {summary_path}")
    return json.loads(summary_path.read_text(encoding="utf-8"))


def trigger_next_month(summary: dict[str, Any]) -> tuple[bool, str]:
    headline = summary["financial_metrics"]["headline"]
    return_pct = float(headline.get("return_pct") or 0.0)
    profit_factor = float(headline.get("profit_factor") or 0.0)
    if return_pct < 0.0:
        return True, "prev_month_return_lt_0"
    if profit_factor < 1.0:
        return True, "prev_month_pf_lt_1"
    return False, "carry_forward"


def summarize_shadow_rows(rows: list[dict[str, str]]) -> dict[str, Any]:
    total_rows = len(rows)
    ready_rows = [row for row in rows if row.get("row_ready", "").lower() == "true"]
    skipped_rows = [row for row in rows if row.get("row_ready", "").lower() != "true"]
    decisions = Counter(row.get("decision", "") for row in ready_rows)
    skip_reasons = Counter(row.get("skip_reason", "") for row in skipped_rows if row.get("skip_reason", ""))

    external_mismatch_count = sum(
        count for reason, count in skip_reasons.items() if reason.startswith("EXTERNAL_TIMESTAMP_MISMATCH")
    )
    data_readiness_failures = sum(
        count
        for reason, count in skip_reasons.items()
        if "NOT_READY" in reason or "WARMUP" in reason or "MODEL_NOT_READY" in reason
    )
    feature_ready_max = max(int(row.get("feature_ready_count", "0") or 0) for row in rows) if rows else 0
    ready_rate = (len(ready_rows) / total_rows) if total_rows else 0.0
    no_trade_rate = (decisions.get("NO_TRADE", 0) / len(ready_rows)) if ready_rows else 1.0
    classified = classify_skip_reasons(skip_reasons)
    return {
        "row_count": total_rows,
        "ready_row_count": len(ready_rows),
        "skip_row_count": len(skipped_rows),
        "ready_rate": ready_rate,
        "long_signal_count": decisions.get("LONG", 0),
        "short_signal_count": decisions.get("SHORT", 0),
        "no_trade_count": decisions.get("NO_TRADE", 0),
        "no_trade_rate": no_trade_rate,
        "skip_reason_breakdown": dict(skip_reasons),
        "external_mismatch_count": external_mismatch_count,
        "data_readiness_failures": data_readiness_failures,
        "feature_ready_max": feature_ready_max,
        "latest_bar_time_server": rows[-1].get("bar_time_server") if rows else None,
        **classified,
        "rows": rows,
    }


def load_governance_rows(csv_path: Path) -> list[dict[str, str]]:
    if not csv_path.exists():
        return []
    with csv_path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def aggregate_governance_rows(rows: list[dict[str, str]]) -> dict[str, Any]:
    if not rows:
        return {
            "row_count": 0,
            "state_counts": {},
            "reason_counts": {},
            "blocked_entry_count": 0,
            "blocked_signal_count": 0,
            "latest_state": None,
            "latest_reason": None,
            "max_external_skip_rate": None,
            "max_argmax_class_share": None,
            "min_avg_signal_entropy_norm": None,
            "alert_or_block_rows": 0,
        }

    state_counts = Counter((row.get("governance_state") or "").strip() for row in rows if (row.get("governance_state") or "").strip())
    reason_counts = Counter((row.get("governance_reason") or "").strip() for row in rows if (row.get("governance_reason") or "").strip())
    external_rates = [float(row["external_skip_rate"]) for row in rows if row.get("external_skip_rate")]
    argmax_rates = [float(row["max_argmax_class_share"]) for row in rows if row.get("max_argmax_class_share")]
    entropy_values = [float(row["avg_signal_entropy_norm"]) for row in rows if row.get("avg_signal_entropy_norm")]
    blocked_entry_count = sum(1 for row in rows if (row.get("entry_blocked_this_bar") or "").lower() == "true")
    blocked_signal_count = sum(
        1
        for row in rows
        if (row.get("entry_blocked_this_bar") or "").lower() == "true"
        and (row.get("decision") or "").strip() in {"LONG", "SHORT"}
    )
    latest_row = rows[-1]
    return {
        "row_count": len(rows),
        "state_counts": dict(state_counts),
        "reason_counts": dict(reason_counts),
        "blocked_entry_count": blocked_entry_count,
        "blocked_signal_count": blocked_signal_count,
        "latest_state": (latest_row.get("governance_state") or "").strip() or None,
        "latest_reason": (latest_row.get("governance_reason") or "").strip() or None,
        "max_external_skip_rate": max(external_rates) if external_rates else None,
        "max_argmax_class_share": max(argmax_rates) if argmax_rates else None,
        "min_avg_signal_entropy_norm": min(entropy_values) if entropy_values else None,
        "alert_or_block_rows": sum(
            1 for row in rows if (row.get("governance_state") or "").strip() in {"ALERT", "BLOCKED"}
        ),
    }


def build_stitched_summary(run_dir: Path, arm: dict[str, Any], month_results: list[dict[str, Any]]) -> dict[str, Any]:
    combined_shadow_rows: list[dict[str, str]] = []
    combined_trades: list[dict[str, Any]] = []
    combined_governance_rows: list[dict[str, str]] = []

    for month_row in month_results:
        parsed_shadow = parse_shadow_csv(Path(month_row["csv_log_path"]))
        combined_shadow_rows.extend(parsed_shadow["rows"])
        combined_trades.extend(parse_trade_ledger(Path(month_row["trade_ledger_path"])))
        combined_governance_rows.extend(load_governance_rows(Path(month_row["governance_log_path"])))

    stitched_shadow = summarize_shadow_rows(combined_shadow_rows)
    stitched_governance = aggregate_governance_rows(combined_governance_rows)

    stitched_bundle = deepcopy(SOURCE_BUNDLE)
    stitched_bundle.runtime_snapshot.deposit = INITIAL_DEPOSIT
    stitched_financial = summarize_financial_metrics(
        bundle=stitched_bundle,
        shadow_rows=combined_shadow_rows,
        trades=combined_trades,
        parsed_shadow=stitched_shadow,
    )

    final_balance = month_results[-1]["final_balance"] if month_results else INITIAL_DEPOSIT
    positive_months = sum(1 for row in month_results if (row.get("return_pct") or 0.0) > 0.0)
    retrain_months = [row["month_token"] for row in month_results if row.get("retrain_applied")]

    summary = {
        "generated_at_utc": utc_now_iso(),
        "stage": "28_retrain_feature_checks",
        "wave": "event_triggered_retrain_wave1",
        "run_name": run_dir.name,
        "arm_stage_id": arm["stage_id"],
        "arm_label": arm["label"],
        "mode": arm["mode"],
        "trigger_label": arm["trigger_label"],
        "window_token": "2501",
        "months": [row["month_token"] for row in month_results],
        "initial_deposit": INITIAL_DEPOSIT,
        "final_balance": final_balance,
        "positive_months": positive_months,
        "retrain_month_count": len(retrain_months),
        "retrain_months": retrain_months,
        "month_results": month_results,
        "stitched_financial_metrics": stitched_financial,
        "stitched_governance_metrics": stitched_governance,
    }
    write_json(run_dir / "stitched_summary.json", summary)

    lines = [
        f"# {run_dir.name} Stitched Summary",
        "",
        f"- generated_at: {code(summary['generated_at_utc'])}",
        f"- arm: {code(arm['stage_id'])} {code(arm['label'])}",
        f"- mode: {code(arm['mode'])}",
        f"- trigger: {code(arm['trigger_label'])}",
        f"- stitched return_pct: {code(stitched_financial['headline']['return_pct'])}",
        f"- stitched net_profit: {code(stitched_financial['headline']['net_profit'])}",
        f"- stitched PF: {code(stitched_financial['headline']['profit_factor'], digits=4)}",
        f"- stitched trades: {code(stitched_financial['headline']['trade_count'])}",
        f"- stitched max_dd_pct: {code(stitched_financial['headline']['max_dd_pct'], digits=4)}",
        f"- final_balance: {code(final_balance)}",
        f"- positive months: {code(f'{positive_months}/{len(month_results)}')}",
        f"- retrain months: {code(', '.join(retrain_months) if retrain_months else 'none')}",
        "",
        "## Monthly Results",
        "",
    ]
    for row in month_results:
        lines.append(
            f"- {code(row['month_token'])}: deposit_in {code(row['deposit_in'])}, return_pct {code(row['return_pct'])}, "
            f"PF {code(row['profit_factor'], digits=4)}, trades {code(row['trade_count'])}, "
            f"max_dd_pct {code(row['max_dd_pct'], digits=4)}, retrain {code(row['retrain_applied'])}, "
            f"trigger_for_next {code(row['trigger_for_next'])}"
        )
    write_markdown(run_dir / "stitched_summary.md", lines, bom=True)
    return summary


def run_arm(dataset: pd.DataFrame, arm: dict[str, Any]) -> dict[str, Any]:
    run_dir = ACTIVE_RUNS_DIR / arm["folder_name"]
    if run_dir.exists():
        raise FileExistsError(f"target run directory already exists: {run_dir}")
    run_dir.mkdir(parents=True, exist_ok=False)

    current_model_descriptor = {
        "model_path": str(SOURCE_RUN_DIR / "model.joblib"),
        "origin": {
            "kind": "fixed_source",
            "source_run_name": "28B_18e_persist48_ph20_0001",
        },
    }
    carry_deposit = INITIAL_DEPOSIT
    month_results: list[dict[str, Any]] = []
    should_retrain_next = False
    next_trigger_reason = "initial_carry"

    for month_start in month_start_range():
        slice_payload = build_month_slice(dataset, month_start)
        month_dir = run_dir / slice_payload["month_dir_token"]
        month_dir.mkdir(parents=True, exist_ok=False)
        run_name = f"{arm['folder_name']}_{slice_payload['month_dir_token']}"

        retrain_applied = False
        trigger_reason = None
        if arm["mode"] == "monthly_retrain":
            retrain_applied = True
            trigger_reason = "always_retrain"
            model_path, model_origin = train_month_model(
                run_dir=month_dir,
                month_slice=slice_payload,
                run_name=run_name,
                arm=arm,
                trigger_reason=trigger_reason,
            )
            current_model_descriptor = {"model_path": str(model_path), "origin": model_origin}
        elif arm["mode"] == "event_triggered" and should_retrain_next:
            retrain_applied = True
            trigger_reason = next_trigger_reason
            model_path, model_origin = train_month_model(
                run_dir=month_dir,
                month_slice=slice_payload,
                run_name=run_name,
                arm=arm,
                trigger_reason=trigger_reason,
            )
            current_model_descriptor = {"model_path": str(model_path), "origin": model_origin}
        else:
            prepare_carried_model(
                run_dir=month_dir,
                month_slice=slice_payload,
                run_name=run_name,
                arm=arm,
                model_descriptor=current_model_descriptor,
                trigger_reason=next_trigger_reason if arm["mode"] == "event_triggered" else None,
            )

        bundle_path = export_month_bundle(
            run_dir=month_dir,
            arm=arm,
            month_slice=slice_payload,
            deposit_in=carry_deposit,
        )
        summary = run_tester(bundle_path, slice_payload)

        headline = summary["financial_metrics"]["headline"]
        final_balance = float(headline["extra"]["final_balance"])
        should_retrain_next, next_trigger_reason = (
            trigger_next_month(summary) if arm["mode"] == "event_triggered" else (False, "not_applicable")
        )

        month_row = {
            "month_token": slice_payload["month_token"],
            "month_dir": str(month_dir.relative_to(ROOT_DIR)).replace("\\", "/"),
            "deposit_in": carry_deposit,
            "final_balance": final_balance,
            "net_profit": float(headline.get("net_profit") or 0.0),
            "return_pct": float(headline.get("return_pct") or 0.0),
            "profit_factor": float(headline.get("profit_factor") or 0.0),
            "trade_count": int(headline.get("trade_count") or 0),
            "max_dd_pct": float(headline.get("max_dd_pct") or 0.0),
            "retrain_applied": retrain_applied,
            "model_origin": current_model_descriptor["origin"],
            "trigger_for_next": next_trigger_reason,
            "csv_log_path": summary["csv_log_path"],
            "trade_ledger_path": summary["trade_ledger_path"],
            "governance_log_path": summary.get("governance_log_path"),
        }
        month_manifest = {
            "generated_at_utc": utc_now_iso(),
            "month_token": slice_payload["month_token"],
            "lookback_label": "2M",
            "lookback_mode": "trading_days",
            "lookback_trading_days": LOOKBACK_TRADING_DAYS,
            "selected_trade_days_utc": slice_payload["selected_trade_days"],
            "train_start_utc": slice_payload["train_df"]["timestamp"].min().isoformat(),
            "train_end_utc_exclusive": slice_payload["month_start"].isoformat(),
            "test_start_utc": slice_payload["month_start"].isoformat(),
            "test_end_utc_exclusive": slice_payload["month_end"].isoformat(),
            "train_rows": int(len(slice_payload["train_df"])),
            "test_rows": int(len(slice_payload["test_df"])),
            "train_class_counts": {
                "short": int((slice_payload["train_df"]["label"] == 0).sum()),
                "flat": int((slice_payload["train_df"]["label"] == 1).sum()),
                "long": int((slice_payload["train_df"]["label"] == 2).sum()),
            },
            "test_class_counts": {
                "short": int((slice_payload["test_df"]["label"] == 0).sum()),
                "flat": int((slice_payload["test_df"]["label"] == 1).sum()),
                "long": int((slice_payload["test_df"]["label"] == 2).sum()),
            },
            "event_trigger": {
                "mode": arm["mode"],
                "trigger_label": arm["trigger_label"],
                "retrain_applied": retrain_applied,
                "trigger_reason": trigger_reason,
                "next_trigger_reason": next_trigger_reason,
            },
            "carry": {
                "deposit_in": carry_deposit,
                "final_balance": final_balance,
            },
        }
        write_json(month_dir / "month_manifest.json", month_manifest)
        month_results.append(month_row)
        carry_deposit = final_balance
        print(
            f"[{arm['stage_id']}] month={slice_payload['month_token']} retrain={retrain_applied} "
            f"return_pct={month_row['return_pct']:.3f} pf={month_row['profit_factor']:.4f} final_balance={final_balance:.2f}"
        )

    stitched_summary = build_stitched_summary(run_dir, arm, month_results)
    run_manifest = {
        "generated_at_utc": utc_now_iso(),
        "stage": "28_retrain_feature_checks",
        "run_name": run_dir.name,
        "assumption": arm["label"],
        "window_token": "2501",
        "lookback_label": "2M",
        "lookback_mode": "trading_days",
        "lookback_trading_days": LOOKBACK_TRADING_DAYS,
        "months": stitched_summary["months"],
        "runtime": {
            "sizing_mode": "risk_pct",
            "risk_pct": 2.0,
            "capital_base": "balance",
            "stop_model": "atr",
            "stop_policy": "direction_split",
            "stop_atr_period": 14,
            "stop_long_atr_mult": 1.4,
            "stop_short_atr_mult": 2.0,
            "monday_risk_pct_mult": 0.75,
            "ny_postcash_risk_pct_mult": 0.7,
            "ny_postcash_hold_cap_bars": 3,
            "session_overlay_label": "postcash_hold_cut",
        },
        "carry_mode": {
            "enabled": True,
            "initial_deposit": INITIAL_DEPOSIT,
        },
        "trigger_logic": {
            "mode": arm["mode"],
            "label": arm["trigger_label"],
        },
        "month_results": month_results,
    }
    write_json(run_dir / "run_manifest.json", run_manifest)
    return stitched_summary


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Build and execute Stage 28 event-triggered retrain wave 2 runs.")
    parser.add_argument(
        "--stage-ids",
        default="28E,28F,28G",
        help="Comma-separated stage ids to build/execute. Default: 28E,28F,28G",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    selected_ids = {item.strip() for item in args.stage_ids.split(",") if item.strip()}
    selected_runs = [run for run in RUNS if run["stage_id"] in selected_ids]
    if not selected_runs:
        raise ValueError("no Stage 28 wave 2 arms selected")

    dataset = load_dataset()
    summaries = []
    for arm in selected_runs:
        summaries.append(run_arm(dataset, arm))

    overview_lines = [
        "# Stage 28 Event-Triggered Retrain Wave 2 Build Summary",
        "",
    ]
    for payload in summaries:
        headline = payload["stitched_financial_metrics"]["headline"]
        overview_lines.append(
            f"- {code(payload['arm_stage_id'])} `{payload['run_name']}`: return_pct {code(headline['return_pct'])}, "
            f"PF {code(headline['profit_factor'], digits=4)}, trades {code(headline['trade_count'])}, "
            f"max_dd_pct {code(headline['max_dd_pct'], digits=4)}, retrain_months {code(payload['retrain_month_count'])}"
        )
    write_markdown(STAGE_DIR / "03_reviews" / "stage28_event_retrain_wave2_build_summary.md", overview_lines, bom=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
