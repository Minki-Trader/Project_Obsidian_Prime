#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import shutil
import subprocess
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import joblib
import pandas as pd
from sklearn.base import clone

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from foundation.pipelines.experiment_bundle_models import ExperimentBundle, SplitBoundaries
from foundation.pipelines.export_experiment_bundle_assets import run_export_bundle_assets
from foundation.pipelines.run_mt5_bundle_tester import parse_shadow_csv, parse_trade_ledger, summarize_financial_metrics


STAGE21_ROOT = ROOT_DIR / "stages" / "21_retrain_cadence_wfo"
DEFAULT_DATASET_PATH = ROOT_DIR / "stages" / "01_base_feature_ml" / "01_inputs" / "stage01c_h03_band000125_dataset.parquet"
DEFAULT_SOURCE_MODEL_PATH = (
    ROOT_DIR / "stages" / "17_09c_directional_core_fork" / "02_runs" / "active" / "17E_2407_ovr_balanced_0001" / "model.joblib"
)
DEFAULT_SOURCE_CONFIG_PATH = (
    ROOT_DIR / "stages" / "17_09c_directional_core_fork" / "02_runs" / "active" / "17E_2407_ovr_balanced_0001" / "config.json"
)

MONTH_SPECS = [
    ("2025_04", "2025-04-01T00:00:00Z", "2025-05-01T00:00:00Z"),
    ("2025_05", "2025-05-01T00:00:00Z", "2025-06-01T00:00:00Z"),
    ("2025_06", "2025-06-01T00:00:00Z", "2025-07-01T00:00:00Z"),
    ("2025_07", "2025-07-01T00:00:00Z", "2025-08-01T00:00:00Z"),
    ("2025_08", "2025-08-01T00:00:00Z", "2025-09-01T00:00:00Z"),
]

OVERLAY_EXTRA = {
    "monday_risk_pct_mult": 0.75,
    "ny_postcash_risk_pct_mult": 0.70,
    "ny_postcash_hold_cap_bars": 3,
    "session_overlay_label": "postcash_hold_cut",
}


@dataclass(frozen=True)
class LookbackSpec:
    name: str
    stage_id: str
    root_run_name: str
    folder_token: str
    trading_days: int


LOOKBACK_SPECS = {
    "1D": LookbackSpec(name="1D", stage_id="21H", root_run_name="21H_2407_mt5_1d_0001", folder_token="1d", trading_days=1),
    "5D": LookbackSpec(name="5D", stage_id="21I", root_run_name="21I_2407_mt5_5d_0001", folder_token="5d", trading_days=5),
    "1W": LookbackSpec(name="1W", stage_id="21J", root_run_name="21J_2407_mt5_1w_0001", folder_token="1w", trading_days=7),
}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run direct MT5 monthly carry-stitch backtests for short trailing-lookback 17E retrains."
    )
    parser.add_argument(
        "--lookbacks",
        nargs="+",
        default=["1D", "5D", "1W"],
        help="Lookback labels to run. Supported: 1D 5D 1W",
    )
    parser.add_argument("--stage-root", default=str(STAGE21_ROOT), help="Stage 21 root directory.")
    parser.add_argument("--dataset-path", default=str(DEFAULT_DATASET_PATH), help="Shared dataset parquet.")
    parser.add_argument("--source-model-path", default=str(DEFAULT_SOURCE_MODEL_PATH), help="17E source model.joblib.")
    parser.add_argument("--source-config-path", default=str(DEFAULT_SOURCE_CONFIG_PATH), help="17E source config.json.")
    parser.add_argument("--window-token", default="2407", help="Logical comparison window token written into manifests.")
    parser.add_argument(
        "--logic-reference-run-name",
        default="18E_2407_17e_ph20_0001",
        help="Overlay shell reference label written into configs/manifests.",
    )
    parser.add_argument("--initial-deposit", type=float, default=500.0, help="Initial carried deposit.")
    parser.add_argument("--risk-pct", type=float, default=2.0, help="Risk percent for ATR sizing.")
    parser.add_argument("--stop-atr-period", type=int, default=14, help="ATR period.")
    parser.add_argument("--stop-long-atr-mult", type=float, default=1.4, help="Long ATR multiplier.")
    parser.add_argument("--stop-short-atr-mult", type=float, default=2.0, help="Short ATR multiplier.")
    parser.add_argument("--rebuild", action="store_true", help="Delete and rebuild the requested lookback run roots.")
    return parser


def utc_now_iso() -> str:
    return pd.Timestamp.now(tz="UTC").isoformat()


def parse_utc(raw_value: str) -> pd.Timestamp:
    ts = pd.Timestamp(raw_value)
    if ts.tzinfo is None:
        ts = ts.tz_localize("UTC")
    else:
        ts = ts.tz_convert("UTC")
    return ts


def month_dir_name(test_start: pd.Timestamp) -> str:
    return f"m{test_start.strftime('%y%m')}"


def month_run_name(spec: LookbackSpec, month_token: str, window_token: str) -> str:
    return f"{spec.stage_id}_{window_token}_mt5_{spec.folder_token}_{month_token}_0001"


def month_experiment_id(spec: LookbackSpec, month_token: str, window_token: str) -> str:
    compact = month_token.replace("_", "")
    return f"exp_{spec.stage_id.lower()}_{window_token}_{spec.folder_token}_{compact}_v1"


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def format_metric(value: float | int | None, digits: int = 3) -> str:
    if value is None:
        return "na"
    return f"{float(value):.{digits}f}"


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8-sig")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def build_rule_stack() -> dict[str, Any]:
    return {
        "entry": [
            {
                "rule_id": "entry_01",
                "type": "threshold_entry",
                "enabled": True,
                "params": {
                    "short_threshold": 0.3,
                    "long_threshold": 0.5,
                },
            }
        ],
        "filters": [
            {
                "rule_id": "filter_01",
                "type": "max_probability_margin",
                "enabled": True,
                "params": {
                    "min_margin": 0.07,
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
                    "max_hold_bars": 4,
                },
            }
        ],
    }


def load_dataset(dataset_path: Path, feature_names: list[str]) -> pd.DataFrame:
    required_columns = ["timestamp", "label", "is_feature_row_valid", *feature_names]
    dataset = pd.read_parquet(dataset_path, columns=required_columns)
    valid_mask = dataset["is_feature_row_valid"].fillna(False)
    base = dataset.loc[valid_mask, ["timestamp", "label", *feature_names]].copy()
    base["timestamp"] = pd.to_datetime(base["timestamp"], utc=True)
    base = base.sort_values("timestamp").reset_index(drop=True)
    base["trade_day"] = base["timestamp"].dt.normalize()
    return base


def select_trailing_training_slice(
    dataset: pd.DataFrame,
    *,
    anchor_utc: pd.Timestamp,
    trading_days: int,
) -> tuple[pd.DataFrame, list[pd.Timestamp]]:
    history = dataset[dataset["timestamp"] < anchor_utc].copy()
    unique_days = sorted(pd.Timestamp(value) for value in history["trade_day"].drop_duplicates().tolist())
    if len(unique_days) < trading_days:
        raise ValueError(f"not enough history before {anchor_utc.isoformat()} for {trading_days} trading days")

    selected_days = unique_days[-trading_days:]
    train_df = history[history["trade_day"].isin(selected_days)].copy()
    if train_df.empty:
        raise ValueError(f"empty training slice for anchor {anchor_utc.isoformat()} and lookback {trading_days} trading days")

    class_values = sorted(int(value) for value in train_df["label"].dropna().unique().tolist())
    if class_values != [0, 1, 2]:
        raise ValueError(
            f"training slice for anchor {anchor_utc.isoformat()} does not contain all classes; got {class_values}"
        )
    return train_df, selected_days


def select_test_slice(dataset: pd.DataFrame, *, test_start_utc: pd.Timestamp, test_end_utc: pd.Timestamp) -> pd.DataFrame:
    return dataset[(dataset["timestamp"] >= test_start_utc) & (dataset["timestamp"] < test_end_utc)].copy()


def class_counts(frame: pd.DataFrame) -> dict[str, int]:
    labels = frame["label"].value_counts().to_dict()
    return {
        "short": int(labels.get(0, 0)),
        "flat": int(labels.get(1, 0)),
        "long": int(labels.get(2, 0)),
    }


def build_month_config(
    source_config: dict[str, Any],
    *,
    spec: LookbackSpec,
    window_token: str,
    logic_reference_run_name: str,
    month_token: str,
    train_df: pd.DataFrame,
    test_df: pd.DataFrame,
    selected_days: list[pd.Timestamp],
    test_start_utc: pd.Timestamp,
    test_end_utc: pd.Timestamp,
) -> dict[str, Any]:
    payload = copy.deepcopy(source_config)
    payload.update(
        {
            "run_name": month_run_name(spec, month_token, window_token),
            "phase": "stage21_mt5_short_lookback_retrain",
            "generated_at_utc": utc_now_iso(),
            "refit_policy": "monthly_tradingday_retrain_then_real_tick_month_test_atr_carry_stitch",
            "logic_reference_run_name": logic_reference_run_name,
            "row_counts": {
                "train": int(len(train_df)),
                "test": int(len(test_df)),
            },
            "class_counts": {
                "train": class_counts(train_df),
                "test": class_counts(test_df),
            },
            "monthly_token": month_token,
            "monthly_window": {
                "train_start_utc": train_df["timestamp"].min().isoformat(),
                "train_end_utc_exclusive": test_start_utc.isoformat(),
                "test_start_utc": test_start_utc.isoformat(),
                "test_end_utc_exclusive": test_end_utc.isoformat(),
            },
            "retrain_lookback": {
                "label": spec.name,
                "mode": "trading_days",
                "trading_days": spec.trading_days,
                "selected_trade_days_utc": [value.isoformat() for value in selected_days],
            },
        }
    )
    return payload


def build_month_manifest(
    *,
    spec: LookbackSpec,
    window_token: str,
    month_token: str,
    train_df: pd.DataFrame,
    test_df: pd.DataFrame,
    selected_days: list[pd.Timestamp],
    test_start_utc: pd.Timestamp,
    test_end_utc: pd.Timestamp,
) -> dict[str, Any]:
    return {
        "generated_at_utc": utc_now_iso(),
        "month_token": month_token,
        "lookback_label": spec.name,
        "lookback_mode": "trading_days",
        "lookback_trading_days": spec.trading_days,
        "selected_trade_days_utc": [value.isoformat() for value in selected_days],
        "train_start_utc": train_df["timestamp"].min().isoformat(),
        "train_end_utc_exclusive": test_start_utc.isoformat(),
        "test_start_utc": test_start_utc.isoformat(),
        "test_end_utc_exclusive": test_end_utc.isoformat(),
        "train_rows": int(len(train_df)),
        "test_rows": int(len(test_df)),
        "train_class_counts": class_counts(train_df),
        "test_class_counts": class_counts(test_df),
        "overlay_runtime_extra": {
            "wfo_mode": "strict_retrain_monthly_mt5_atr_carry",
            "window_token": window_token,
            "candidate_stage_id": spec.stage_id,
            "candidate_label": f"{spec.name}_monthly_retrain_mt5_atr_carry",
            "source_overlay_stage_id": "18E",
            "source_overlay_label": "postcash_hold_cut",
            **OVERLAY_EXTRA,
        },
    }


def prepare_run_root(run_root: Path, *, rebuild: bool) -> None:
    if rebuild and run_root.exists():
        shutil.rmtree(run_root)
    run_root.mkdir(parents=True, exist_ok=True)


def patch_bundle(
    *,
    bundle_path: Path,
    spec: LookbackSpec,
    window_token: str,
    month_token: str,
    train_df: pd.DataFrame,
    test_df: pd.DataFrame,
    test_start_utc: pd.Timestamp,
    test_end_utc: pd.Timestamp,
    deposit: float,
) -> ExperimentBundle:
    bundle = ExperimentBundle.from_json(bundle_path.read_text(encoding="utf-8-sig"))
    bundle.identity.stage_id = "21RC"
    bundle.identity.stage_name = "retrain_cadence_wfo_mt5_short_lookback"
    bundle.identity.created_at_utc = utc_now_iso()
    bundle.runtime_snapshot.deposit = float(deposit)
    bundle.data_snapshot.split_boundaries = SplitBoundaries(
        train_start_utc=train_df["timestamp"].min().isoformat(),
        train_end_utc_exclusive=test_start_utc.isoformat(),
        validation_end_utc_exclusive=test_start_utc.isoformat(),
        test_end_utc_exclusive=test_end_utc.isoformat(),
    )
    bundle.data_snapshot.split_counts = {
        "train": int(len(train_df)),
        "valid": 0,
        "test": int(len(test_df)),
    }
    bundle.data_snapshot.extra.update(
        {
            "run_name": bundle_path.parent.name,
            "run_dir": str(bundle_path.parent),
            "month_token": month_token,
            "lookback_label": spec.name,
            "lookback_mode": "trading_days",
            "lookback_trading_days": spec.trading_days,
        }
    )
    bundle.runtime_snapshot.extra.update(
        {
            "wfo_mode": "strict_retrain_monthly_mt5_atr_carry",
            "window_token": window_token,
            "candidate_stage_id": spec.stage_id,
            "candidate_label": f"{spec.name}_monthly_retrain_mt5_atr_carry",
            "source_overlay_stage_id": "18E",
            "source_overlay_label": "postcash_hold_cut",
            "retrain_schedule": "monthly",
            "retrain_lookback": spec.name,
            "lookback_mode": "trading_days",
            "lookback_trading_days": spec.trading_days,
            "month_token": month_token,
            "train_start_utc": train_df["timestamp"].min().isoformat(),
            "train_end_utc_exclusive": test_start_utc.isoformat(),
            "month_test_start_utc": test_start_utc.isoformat(),
            "month_test_end_utc_exclusive": test_end_utc.isoformat(),
            "fixed_lot_stitch_mode": False,
            "atr_risk_carry_stitch_mode": True,
            **OVERLAY_EXTRA,
        }
    )
    bundle.compatibility.bundle_integrity_hash = sha256_text(bundle.canonical_core_json())
    bundle_path.write_text(bundle.to_json(indent=2), encoding="utf-8")
    return bundle


def run_month_tester(bundle_path: Path, *, test_start_utc: pd.Timestamp, test_end_utc: pd.Timestamp) -> None:
    cmd = [
        sys.executable,
        str(ROOT_DIR / "foundation" / "pipelines" / "run_mt5_bundle_tester.py"),
        "--bundle-json",
        str(bundle_path),
        "--split-name",
        "test",
        "--from-date",
        test_start_utc.strftime("%Y.%m.%d"),
        "--to-date",
        test_end_utc.strftime("%Y.%m.%d"),
        "--enable-trading",
        "--skip-leaderboard-refresh",
    ]
    subprocess.run(cmd, cwd=ROOT_DIR, check=True)


def latest_attempt_summary(month_run_dir: Path) -> dict[str, Any]:
    attempts_root = month_run_dir / "mt5_attempts"
    attempt_dirs = sorted(path for path in attempts_root.iterdir() if path.is_dir() and path.name.startswith("att_"))
    if not attempt_dirs:
        raise FileNotFoundError(f"no MT5 attempt directories found under {attempts_root}")
    summary_path = attempt_dirs[-1] / "tester_attempt_summary.json"
    return load_json(summary_path)


def aggregate_shadow_parsed(parsed_items: list[dict[str, Any]]) -> tuple[dict[str, Any], list[dict[str, str]]]:
    rows: list[dict[str, str]] = []
    skip_reasons: Counter[str] = Counter()
    contract_skip_breakdown: Counter[str] = Counter()
    startup_skip_breakdown: Counter[str] = Counter()
    unexpected_skip_breakdown: Counter[str] = Counter()
    row_count = 0
    ready_row_count = 0
    skip_row_count = 0
    long_signal_count = 0
    short_signal_count = 0
    no_trade_count = 0
    external_mismatch_count = 0
    data_readiness_failures = 0
    feature_ready_max = 0
    latest_bar_time_server: str | None = None

    for parsed in parsed_items:
        rows.extend(parsed["rows"])
        row_count += int(parsed["row_count"])
        ready_row_count += int(parsed["ready_row_count"])
        skip_row_count += int(parsed["skip_row_count"])
        long_signal_count += int(parsed["long_signal_count"])
        short_signal_count += int(parsed["short_signal_count"])
        no_trade_count += int(parsed["no_trade_count"])
        external_mismatch_count += int(parsed["external_mismatch_count"])
        data_readiness_failures += int(parsed["data_readiness_failures"])
        feature_ready_max = max(feature_ready_max, int(parsed["feature_ready_max"]))
        latest_bar_time_server = parsed.get("latest_bar_time_server") or latest_bar_time_server
        skip_reasons.update(parsed["skip_reason_breakdown"])
        contract_skip_breakdown.update(parsed["contract_skip_breakdown"])
        startup_skip_breakdown.update(parsed["startup_skip_breakdown"])
        unexpected_skip_breakdown.update(parsed["unexpected_skip_breakdown"])

    return (
        {
            "row_count": row_count,
            "ready_row_count": ready_row_count,
            "skip_row_count": skip_row_count,
            "ready_rate": (ready_row_count / row_count) if row_count else 0.0,
            "long_signal_count": long_signal_count,
            "short_signal_count": short_signal_count,
            "no_trade_count": no_trade_count,
            "no_trade_rate": (no_trade_count / ready_row_count) if ready_row_count else 1.0,
            "skip_reason_breakdown": dict(skip_reasons),
            "external_mismatch_count": external_mismatch_count,
            "data_readiness_failures": data_readiness_failures,
            "feature_ready_max": feature_ready_max,
            "latest_bar_time_server": latest_bar_time_server,
            "contract_skip_breakdown": dict(contract_skip_breakdown),
            "contract_skip_count": int(sum(contract_skip_breakdown.values())),
            "startup_skip_breakdown": dict(startup_skip_breakdown),
            "startup_skip_count": int(sum(startup_skip_breakdown.values())),
            "unexpected_skip_breakdown": dict(unexpected_skip_breakdown),
            "unexpected_skip_count": int(sum(unexpected_skip_breakdown.values())),
        },
        rows,
    )


def stitch_summary(
    *,
    run_root: Path,
    spec: LookbackSpec,
    month_results: list[dict[str, Any]],
    initial_deposit: float,
) -> dict[str, Any]:
    parsed_items: list[dict[str, Any]] = []
    trades: list[dict[str, object]] = []

    for month in month_results:
        parsed_items.append(parse_shadow_csv(Path(month["csv_log_path"])))
        trades.extend(parse_trade_ledger(Path(month["trade_ledger_path"])))

    combined_parsed, shadow_rows = aggregate_shadow_parsed(parsed_items)
    bundle_path = Path(month_results[0]["bundle_path"])
    bundle = ExperimentBundle.from_json(bundle_path.read_text(encoding="utf-8-sig"))
    bundle.runtime_snapshot.deposit = float(initial_deposit)
    stitched_financial = summarize_financial_metrics(
        bundle=bundle,
        shadow_rows=shadow_rows,
        trades=trades,
        parsed_shadow=combined_parsed,
    )

    positive_months = sum(1 for month in month_results if float(month["return_pct"]) > 0.0)
    best_month = max(month_results, key=lambda item: float(item["return_pct"]))
    worst_month = min(month_results, key=lambda item: float(item["return_pct"]))

    return {
        "generated_at_utc": utc_now_iso(),
        "stage": "21_retrain_cadence_wfo",
        "run_name": run_root.name,
        "mode": "monthly_mt5_atr_risk_carry_stitch",
        "source_reference": "18E shell + monthly retrained 17E core",
        "window_token": "2407",
        "lookback_label": spec.name,
        "lookback_mode": "trading_days",
        "lookback_trading_days": spec.trading_days,
        "months": month_results,
        "stitched_financial_metrics": stitched_financial,
        "monthly_consistency": {
            "month_count": len(month_results),
            "positive_months": positive_months,
            "negative_months": len(month_results) - positive_months,
            "best_month": best_month,
            "worst_month": worst_month,
        },
    }


def build_stitched_markdown(payload: dict[str, Any]) -> str:
    headline = payload["stitched_financial_metrics"]["headline"]
    lines = [
        f"# {payload['lookback_label']} MT5 Short-Lookback Stitch",
        "",
        f"Generated at: `{payload['generated_at_utc']}`",
        "",
        f"- run: `{payload['run_name']}`",
        f"- lookback: `{payload['lookback_label']} = {payload['lookback_trading_days']} trailing trading days`",
        f"- stitched return_pct: `{format_metric(headline['return_pct'], 3)}`",
        f"- stitched net_profit: `{format_metric(headline['net_profit'], 2)}`",
        f"- stitched PF: `{format_metric(headline['profit_factor'], 4)}`",
        f"- stitched trades: `{headline['trade_count']}`",
        f"- stitched max_dd_pct: `{format_metric(headline['max_dd_pct'], 3)}`",
        f"- positive months: `{payload['monthly_consistency']['positive_months']}/{payload['monthly_consistency']['month_count']}`",
        "",
        "## Monthly Results",
        "",
    ]
    for month in payload["months"]:
        lines.append(
            f"- `{month['month_token']}`: deposit_in `{format_metric(month['deposit_in'], 2)}`, "
            f"final_balance `{format_metric(month['final_balance'], 2)}`, "
            f"return_pct `{format_metric(month['return_pct'], 3)}`, "
            f"net_profit `{format_metric(month['net_profit'], 2)}`, "
            f"PF `{format_metric(month['profit_factor'], 4)}`, "
            f"trades `{month['trade_count']}`, "
            f"max_dd_pct `{format_metric(month['max_dd_pct'], 3)}`"
        )
    lines.extend(
        [
            "",
            "## Assumption",
            "",
            "- `1D/5D/1W` are interpreted as trailing trading-day lookbacks at each monthly refit point so weekend month starts still produce a valid train slice.",
            "",
        ]
    )
    return "\n".join(lines)


def run_single_lookback(
    *,
    spec: LookbackSpec,
    args: argparse.Namespace,
    dataset: pd.DataFrame,
    source_model_template: object,
    source_config: dict[str, Any],
    active_features: list[str],
) -> Path:
    run_root = Path(args.stage_root) / "02_runs" / "active" / spec.root_run_name
    if run_root.exists() and not args.rebuild and (run_root / "stitched_summary.json").exists():
        return run_root

    prepare_run_root(run_root, rebuild=args.rebuild)
    write_json(
        run_root / "run_manifest.json",
        {
            "generated_at_utc": utc_now_iso(),
            "stage": "21_retrain_cadence_wfo",
            "run_name": spec.root_run_name,
            "assumption": f"ATR+risk_pct month stitching on the {args.window_token} test window using short trailing trading-day retrained 17E core and 18E PH20 shell with carried monthly deposit",
            "window_token": args.window_token,
            "lookback_label": spec.name,
            "lookback_mode": "trading_days",
            "lookback_trading_days": spec.trading_days,
            "months": [token for token, _, _ in MONTH_SPECS],
            "runtime": {
                "sizing_mode": "risk_pct",
                "risk_pct": args.risk_pct,
                "capital_base": "balance",
                "stop_model": "atr",
                "stop_policy": "direction_split",
                "stop_atr_period": args.stop_atr_period,
                "stop_long_atr_mult": args.stop_long_atr_mult,
                "stop_short_atr_mult": args.stop_short_atr_mult,
                **OVERLAY_EXTRA,
            },
            "carry_mode": {
                "enabled": True,
                "initial_deposit": args.initial_deposit,
            },
        },
    )

    carry_deposit = float(args.initial_deposit)
    month_results: list[dict[str, Any]] = []

    for month_token, test_start_raw, test_end_raw in MONTH_SPECS:
        test_start_utc = parse_utc(test_start_raw)
        test_end_utc = parse_utc(test_end_raw)
        train_df, selected_days = select_trailing_training_slice(
            dataset,
            anchor_utc=test_start_utc,
            trading_days=spec.trading_days,
        )
        test_df = select_test_slice(dataset, test_start_utc=test_start_utc, test_end_utc=test_end_utc)
        if test_df.empty:
            raise ValueError(f"empty month test slice for {month_token}")

        month_run_dir = run_root / month_dir_name(test_start_utc)
        if args.rebuild and month_run_dir.exists():
            shutil.rmtree(month_run_dir)
        month_run_dir.mkdir(parents=True, exist_ok=True)

        model = clone(source_model_template)
        model.fit(train_df[active_features], train_df["label"])
        joblib.dump(model, month_run_dir / "model.joblib")

        write_json(
            month_run_dir / "config.json",
            build_month_config(
                source_config,
                spec=spec,
                window_token=args.window_token,
                logic_reference_run_name=args.logic_reference_run_name,
                month_token=month_token,
                train_df=train_df,
                test_df=test_df,
                selected_days=selected_days,
                test_start_utc=test_start_utc,
                test_end_utc=test_end_utc,
            ),
        )
        write_json(
            month_run_dir / "month_manifest.json",
            build_month_manifest(
                spec=spec,
                window_token=args.window_token,
                month_token=month_token,
                train_df=train_df,
                test_df=test_df,
                selected_days=selected_days,
                test_start_utc=test_start_utc,
                test_end_utc=test_end_utc,
            ),
        )
        write_json(month_run_dir / "rule_stack.json", build_rule_stack())

        export_args = argparse.Namespace(
            run_dir=str(month_run_dir),
            experiment_id=month_experiment_id(spec, month_token, args.window_token),
            stage_id="21RC",
            output_dir=str(month_run_dir),
            stage_name="retrain_cadence_wfo_mt5_short_lookback",
            bundle_version="1.0.0",
            created_by="python_orchestrator",
            config_json=str(month_run_dir / "config.json"),
            dataset_path=str(args.dataset_path),
            selection_json=None,
            logic_family=None,
            selection_key=None,
            rule_stack_json=str(month_run_dir / "rule_stack.json"),
            smoke_split="test",
            smoke_row_index=0,
            max_hold_bars=4,
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
        bundle_path = month_run_dir / "experiment_bundle.json"
        patch_bundle(
            bundle_path=bundle_path,
            spec=spec,
            window_token=args.window_token,
            month_token=month_token,
            train_df=train_df,
            test_df=test_df,
            test_start_utc=test_start_utc,
            test_end_utc=test_end_utc,
            deposit=carry_deposit,
        )
        run_month_tester(bundle_path, test_start_utc=test_start_utc, test_end_utc=test_end_utc)
        attempt_summary = latest_attempt_summary(month_run_dir)
        financial = attempt_summary["financial_metrics"]
        headline = financial["headline"]
        risk = financial["risk"]
        carry_deposit = float(headline["extra"]["final_balance"])
        month_results.append(
            {
                "month_token": month_token,
                "train_start_utc": train_df["timestamp"].min().isoformat(),
                "train_end_utc_exclusive": test_start_utc.isoformat(),
                "test_start_utc": test_start_utc.isoformat(),
                "test_end_utc_exclusive": test_end_utc.isoformat(),
                "deposit_in": float(headline["extra"]["initial_deposit"]),
                "final_balance": carry_deposit,
                "net_profit": float(headline["net_profit"]),
                "return_pct": float(headline["return_pct"]),
                "trade_count": int(headline["trade_count"]),
                "win_rate": float(headline["win_rate"]) if headline["win_rate"] is not None else None,
                "profit_factor": float(headline["profit_factor"]) if headline["profit_factor"] is not None else None,
                "expectancy_per_trade": float(headline["expectancy_per_trade"]) if headline["expectancy_per_trade"] is not None else None,
                "max_dd_pct": float(risk["max_dd_pct"]) if risk["max_dd_pct"] is not None else None,
                "ulcer_index": float(risk["ulcer_index"]) if risk["ulcer_index"] is not None else None,
                "csv_log_path": attempt_summary["csv_log_path"],
                "trade_ledger_path": attempt_summary["trade_ledger_path"],
                "bundle_path": str(bundle_path),
            }
        )

    stitched_payload = stitch_summary(
        run_root=run_root,
        spec=spec,
        month_results=month_results,
        initial_deposit=args.initial_deposit,
    )
    write_json(run_root / "stitched_summary.json", stitched_payload)
    write_text(run_root / "stitched_summary.md", build_stitched_markdown(stitched_payload))
    return run_root


def latest_attempt_summary_from_run(run_root: Path) -> dict[str, Any] | None:
    attempts_root = run_root / "mt5_attempts"
    if not attempts_root.exists():
        return None
    attempt_dirs = sorted(path for path in attempts_root.iterdir() if path.is_dir() and path.name.startswith("att_"))
    if not attempt_dirs:
        return None
    summary_path = attempt_dirs[-1] / "tester_attempt_summary.json"
    return load_json(summary_path)


def collect_direct_mt5_summaries(stage_root: Path) -> list[dict[str, Any]]:
    collected: list[dict[str, Any]] = []
    for spec in LOOKBACK_SPECS.values():
        summary_path = stage_root / "02_runs" / "active" / spec.root_run_name / "stitched_summary.json"
        if not summary_path.exists():
            continue
        payload = load_json(summary_path)
        collected.append({"spec": spec, "path": summary_path, "payload": payload})
    collected.sort(key=lambda item: float(item["payload"]["stitched_financial_metrics"]["headline"]["return_pct"]), reverse=True)
    return collected


def build_stage_review_payload(stage_root: Path) -> dict[str, Any]:
    baseline_summary = latest_attempt_summary_from_run(stage_root / "02_runs" / "active" / "21e18")
    monthly_1m_path = stage_root / "02_runs" / "active" / "21m1a" / "stitched_summary.json"
    monthly_1m_summary = load_json(monthly_1m_path) if monthly_1m_path.exists() else None
    direct_mt5 = collect_direct_mt5_summaries(stage_root)

    def pack_direct(item: dict[str, Any]) -> dict[str, Any]:
        payload = item["payload"]
        headline = payload["stitched_financial_metrics"]["headline"]
        return {
            "run_name": payload["run_name"],
            "stage_id": item["spec"].stage_id,
            "lookback_label": payload["lookback_label"],
            "lookback_trading_days": payload["lookback_trading_days"],
            "return_pct": float(headline["return_pct"]),
            "net_profit": float(headline["net_profit"]),
            "profit_factor": float(headline["profit_factor"]) if headline["profit_factor"] is not None else None,
            "trade_count": int(headline["trade_count"]),
            "max_dd_pct": float(headline["max_dd_pct"]) if headline["max_dd_pct"] is not None else None,
            "positive_months": int(payload["monthly_consistency"]["positive_months"]),
            "path": str(item["path"]),
        }

    return {
        "generated_at_utc": utc_now_iso(),
        "stage": "21_retrain_cadence_wfo",
        "mode": "direct_mt5_short_lookback_monthly_carry",
        "assumption": "1D/5D/1W use trailing trading-day lookbacks at each monthly refit point",
        "comparison_window": "2025-04-01 <= t < 2025-09-01",
        "baseline_18e_same_period": baseline_summary,
        "monthly_1m_atr_carry": monthly_1m_summary,
        "direct_mt5_short_lookbacks": [pack_direct(item) for item in direct_mt5],
        "leader": pack_direct(direct_mt5[0]) if direct_mt5 else None,
    }


def build_stage_review_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Stage 21 Direct MT5 Short-Lookback Review",
        "",
        f"Generated at: `{payload['generated_at_utc']}`",
        "",
        f"- mode: `{payload['mode']}`",
        f"- comparison window: `{payload['comparison_window']}`",
        f"- assumption: `{payload['assumption']}`",
        "",
    ]

    baseline = payload.get("baseline_18e_same_period")
    if baseline:
        headline = baseline["financial_metrics"]["headline"]
        lines.extend(
            [
                "## Same-Period 18E Baseline",
                "",
                "- run: `21e18`",
                f"- return_pct: `{format_metric(headline['return_pct'], 3)}`",
                f"- net_profit: `{format_metric(headline['net_profit'], 2)}`",
                f"- PF: `{format_metric(headline['profit_factor'], 4)}`",
                f"- trades: `{headline['trade_count']}`",
                f"- max_dd_pct: `{format_metric(headline['max_dd_pct'], 3)}`",
                "",
            ]
        )

    monthly_1m = payload.get("monthly_1m_atr_carry")
    if monthly_1m:
        headline = monthly_1m["stitched_financial_metrics"]["headline"]
        lines.extend(
            [
                "## Existing 1M ATR Carry Reference",
                "",
                f"- run: `{monthly_1m['run_name']}`",
                f"- return_pct: `{format_metric(headline['return_pct'], 3)}`",
                f"- net_profit: `{format_metric(headline['net_profit'], 2)}`",
                f"- PF: `{format_metric(headline['profit_factor'], 4)}`",
                f"- trades: `{headline['trade_count']}`",
                f"- max_dd_pct: `{format_metric(headline['max_dd_pct'], 3)}`",
                "",
            ]
        )

    lines.extend(["## Direct MT5 Short-Lookback Results", ""])
    if not payload["direct_mt5_short_lookbacks"]:
        lines.append("- pending")
    else:
        for row in payload["direct_mt5_short_lookbacks"]:
            lines.append(
                f"- `{row['stage_id']}` `{row['lookback_label']}` ({row['lookback_trading_days']} trading days): "
                f"return_pct `{format_metric(row['return_pct'], 3)}`, "
                f"net_profit `{format_metric(row['net_profit'], 2)}`, "
                f"PF `{format_metric(row['profit_factor'], 4)}`, "
                f"trades `{row['trade_count']}`, "
                f"max_dd_pct `{format_metric(row['max_dd_pct'], 3)}`, "
                f"positive_months `{row['positive_months']}/5`"
            )

    leader = payload.get("leader")
    if leader:
        lines.extend(
            [
                "",
                "## Readout",
                "",
                f"- direct-MT5 short-lookback leader: `{leader['stage_id']} / {leader['lookback_label']}`",
            ]
        )
        if baseline:
            baseline_return = float(baseline["financial_metrics"]["headline"]["return_pct"])
            if leader["return_pct"] > baseline_return:
                lines.append("- note: `short-lookback leader exceeds the same-period 18E baseline`")
            else:
                lines.append("- note: `same-period 18E baseline still remains stronger than every direct MT5 short-lookback retrain tested so far`")
        if monthly_1m:
            monthly_1m_return = float(monthly_1m["stitched_financial_metrics"]["headline"]["return_pct"])
            if leader["return_pct"] > monthly_1m_return:
                lines.append("- note: `short-lookback leader improves on the prior 1M ATR carry retrain reference`")
    lines.append("")
    return "\n".join(lines)


def update_stage_docs(stage_root: Path) -> None:
    review_payload = build_stage_review_payload(stage_root)
    write_text(stage_root / "03_reviews" / "21RC_mt5_short_lookback_review.md", build_stage_review_markdown(review_payload))
    write_json(stage_root / "03_reviews" / "21RC_mt5_short_lookback_review.json", review_payload)
    write_text(
        stage_root / "03_reviews" / "review_index.md",
        "\n".join(
            [
                "# Review Index",
                "",
                "## Current Entries",
                "",
                "- `21RC`: see `21RC_retrain_cadence_wfo_review.md`",
                "- `21RC_MT5_FIXEDLOT`: see `21RC_monthly_mt5_fixedlot_stitch_review.md`",
                "- `21RC_MT5_SHORT`: see `21RC_mt5_short_lookback_review.md`",
                "",
            ]
        ),
    )

    baseline = review_payload.get("baseline_18e_same_period")
    monthly_1m = review_payload.get("monthly_1m_atr_carry")
    leader = review_payload.get("leader")
    selection_lines = [
        "# Selection Status",
        "",
        "- stage: `21_retrain_cadence_wfo`",
    ]
    if leader:
        selection_lines.extend(
            [
                f"- direct mt5 short-lookback leader: `{leader['stage_id']} / {leader['lookback_label']}`",
                f"- direct leader return_pct: `{format_metric(leader['return_pct'], 3)}`",
                f"- direct leader net_profit: `{format_metric(leader['net_profit'], 2)}`",
                f"- direct leader PF: `{format_metric(leader['profit_factor'], 4)}`",
                f"- direct leader trades: `{leader['trade_count']}`",
                f"- direct leader max_dd_pct: `{format_metric(leader['max_dd_pct'], 3)}`",
                f"- direct leader positive months: `{leader['positive_months']}/5`",
            ]
        )
    else:
        selection_lines.append("- direct mt5 short-lookback leader: `pending`")

    if baseline:
        headline = baseline["financial_metrics"]["headline"]
        selection_lines.extend(
            [
                "- baseline same-period 18E run: `21e18`",
                f"- baseline 18E return_pct: `{format_metric(headline['return_pct'], 3)}`",
                f"- baseline 18E net_profit: `{format_metric(headline['net_profit'], 2)}`",
                f"- baseline 18E PF: `{format_metric(headline['profit_factor'], 4)}`",
                f"- baseline 18E trades: `{headline['trade_count']}`",
                f"- baseline 18E max_dd_pct: `{format_metric(headline['max_dd_pct'], 3)}`",
            ]
        )

    if monthly_1m:
        headline = monthly_1m["stitched_financial_metrics"]["headline"]
        selection_lines.extend(
            [
                "- mt5 atr-carry 1M run: `21m1a`",
                f"- 1M atr-carry return_pct: `{format_metric(headline['return_pct'], 3)}`",
                f"- 1M atr-carry PF: `{format_metric(headline['profit_factor'], 4)}`",
            ]
        )

    selection_lines.append("- assumption: `1D/5D/1W are trailing trading-day lookbacks at each monthly refit point`")
    if leader and baseline:
        baseline_return = float(baseline["financial_metrics"]["headline"]["return_pct"])
        if leader["return_pct"] > baseline_return:
            selection_lines.append("- note: `direct MT5 short-lookback leader currently exceeds the same-period 18E rerun`")
            selection_lines.append("- next action: `stress the leader on a longer out-of-sample window before any promotion decision`")
        else:
            selection_lines.append("- note: `same five-month window still favors the original 18E fixed model over every direct MT5 short-lookback retrain tested`")
            selection_lines.append("- next action: `if retraining stays interesting, test a slower lookback family like 2W or 1M under the same direct MT5 path`")
    write_text(stage_root / "04_selected" / "selection_status.md", "\n".join(selection_lines) + "\n")


def main() -> int:
    args = build_parser().parse_args()
    requested_specs: list[LookbackSpec] = []
    for label in args.lookbacks:
        normalized = label.upper()
        if normalized not in LOOKBACK_SPECS:
            raise ValueError(f"unsupported lookback {label!r}; choose from {sorted(LOOKBACK_SPECS)}")
        requested_specs.append(LOOKBACK_SPECS[normalized])

    dataset_path = Path(args.dataset_path).resolve()
    source_model_path = Path(args.source_model_path).resolve()
    source_config_path = Path(args.source_config_path).resolve()
    if not dataset_path.exists():
        raise FileNotFoundError(f"missing dataset: {dataset_path}")
    if not source_model_path.exists():
        raise FileNotFoundError(f"missing source model: {source_model_path}")
    if not source_config_path.exists():
        raise FileNotFoundError(f"missing source config: {source_config_path}")

    source_model_template = joblib.load(source_model_path)
    source_config = load_json(source_config_path)
    active_features = [str(value) for value in source_config["active_input_features"]]
    dataset = load_dataset(dataset_path, active_features)

    for spec in requested_specs:
        run_single_lookback(
            spec=spec,
            args=args,
            dataset=dataset,
            source_model_template=source_model_template,
            source_config=source_config,
            active_features=active_features,
        )

    update_stage_docs(Path(args.stage_root))
    print("[done] stage review updated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
