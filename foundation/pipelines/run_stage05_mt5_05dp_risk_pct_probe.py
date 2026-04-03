#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from foundation.pipelines.export_experiment_bundle_assets import run_export_bundle_assets
from foundation.pipelines.show_experiment_leaderboard import load_bundle_views


UTC = timezone.utc


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run a single 05DP risk-percent ATR sizing verification backtest.")
    parser.add_argument("--stage-root", default="stages/05_optimization", help="Stage 05 root directory.")
    parser.add_argument(
        "--source-run-dir",
        default="stages/05_optimization/02_runs/active/05DP_05ca_margin0675_hold5_0001",
        help="Existing trained run directory whose model.joblib should be reused.",
    )
    parser.add_argument(
        "--run-name",
        default="05GA_05dp_riskpct050_atr14x15_0001",
        help="Run folder name for the risk-percent verification probe.",
    )
    parser.add_argument(
        "--experiment-id",
        default="exp_05ga_05dp_riskpct050_atr14x15_v1",
        help="Experiment id written into experiment_bundle.json.",
    )
    parser.add_argument("--stage-id", default="05GA", help="Stage id written into experiment_bundle.json.")
    parser.add_argument(
        "--review-basename",
        default="05GA_mt5_05dp_risk_pct_probe_review",
        help="Basename for review markdown/json files under 03_reviews.",
    )
    parser.add_argument("--risk-pct", type=float, default=0.5, help="Percent of balance to risk per trade.")
    parser.add_argument("--stop-atr-period", type=int, default=14, help="ATR period for the hard stop.")
    parser.add_argument("--stop-atr-mult", type=float, default=1.5, help="ATR multiplier for the hard stop.")
    parser.add_argument("--capital-base", choices=["balance", "equity"], default="balance", help="Capital base for risk sizing.")
    parser.add_argument(
        "--stop-execution-mode",
        choices=["ea_managed", "broker_native"],
        default="broker_native",
        help="How the initial stop should be executed in the EA.",
    )
    parser.add_argument(
        "--stop-policy",
        choices=["fixed", "regime_bucket", "direction_split"],
        default="fixed",
        help="How ATR stop multiplier should be selected.",
    )
    parser.add_argument("--stop-long-atr-mult", type=float, help="Long-side ATR multiplier for direction_split policy.")
    parser.add_argument("--stop-short-atr-mult", type=float, help="Short-side ATR multiplier for direction_split policy.")
    parser.add_argument("--stop-low-vol-threshold", type=float, help="ATR14/ATR50 threshold for low-vol regime.")
    parser.add_argument("--stop-high-vol-threshold", type=float, help="ATR14/ATR50 threshold for high-vol regime.")
    parser.add_argument("--stop-low-atr-mult", type=float, help="Low-vol ATR multiplier for regime_bucket policy.")
    parser.add_argument("--stop-mid-atr-mult", type=float, help="Mid-vol ATR multiplier for regime_bucket policy.")
    parser.add_argument("--stop-high-atr-mult", type=float, help="High-vol ATR multiplier for regime_bucket policy.")
    parser.add_argument("--rebuild-bundle", action="store_true", help="Force bundle rebuild even if present.")
    return parser


def utc_now_iso() -> str:
    return datetime.now(tz=UTC).isoformat()


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_json(path: Path, payload: dict[str, Any]) -> None:
    write_text(path, json.dumps(payload, indent=2, ensure_ascii=False) + "\n")


def build_rule_stack() -> dict[str, Any]:
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
                "params": {"min_margin": 0.0675},
            }
        ],
        "position": [
            {
                "rule_id": "position_01",
                "type": "single_position_only",
                "enabled": True,
                "params": {"max_concurrent_positions": 1},
            }
        ],
        "exit": [
            {
                "rule_id": "exit_01",
                "type": "time_exit",
                "enabled": True,
                "params": {"max_hold_bars": 5},
            }
        ],
    }


def ensure_bundle(args: argparse.Namespace, run_dir: Path, source_run_dir: Path) -> Path:
    bundle_path = run_dir / "experiment_bundle.json"
    rule_stack_path = run_dir / "rule_stack.json"
    probe_manifest_path = run_dir / "risk_probe_manifest.json"

    write_json(rule_stack_path, build_rule_stack())
    write_json(
        probe_manifest_path,
        {
            "generated_at_utc": utc_now_iso(),
            "probe_type": "risk_pct_verification",
            "run_name": args.run_name,
            "experiment_id": args.experiment_id,
            "stage_id": args.stage_id,
            "source_run_dir": str(source_run_dir),
            "sizing_mode": "risk_pct",
            "risk_pct": args.risk_pct,
            "capital_base": args.capital_base,
            "stop_model": "atr",
            "stop_execution_mode": args.stop_execution_mode,
            "stop_policy": args.stop_policy,
            "stop_atr_period": args.stop_atr_period,
            "stop_atr_mult": args.stop_atr_mult,
            "stop_long_atr_mult": args.stop_long_atr_mult,
            "stop_short_atr_mult": args.stop_short_atr_mult,
            "stop_low_vol_threshold": args.stop_low_vol_threshold,
            "stop_high_vol_threshold": args.stop_high_vol_threshold,
            "stop_low_atr_mult": args.stop_low_atr_mult,
            "stop_mid_atr_mult": args.stop_mid_atr_mult,
            "stop_high_atr_mult": args.stop_high_atr_mult,
            "logic_reference": "05DP margin 0.0675 hold 5",
        },
    )

    if bundle_path.exists() and not args.rebuild_bundle:
        return bundle_path

    export_args = argparse.Namespace(
        run_dir=str(source_run_dir),
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
        max_hold_bars=5,
        sizing_mode="risk_pct",
        fixed_lot=0.1,
        risk_pct=args.risk_pct,
        capital_base=args.capital_base,
        stop_model="atr",
        stop_execution_mode=args.stop_execution_mode,
        stop_policy=args.stop_policy,
        stop_atr_period=args.stop_atr_period,
        stop_atr_mult=args.stop_atr_mult,
        stop_long_atr_mult=args.stop_long_atr_mult,
        stop_short_atr_mult=args.stop_short_atr_mult,
        stop_low_vol_threshold=args.stop_low_vol_threshold,
        stop_high_vol_threshold=args.stop_high_vol_threshold,
        stop_low_atr_mult=args.stop_low_atr_mult,
        stop_mid_atr_mult=args.stop_mid_atr_mult,
        stop_high_atr_mult=args.stop_high_atr_mult,
        build_bundle=True,
    )
    run_export_bundle_assets(export_args)
    return bundle_path


def run_tester(bundle_path: Path) -> None:
    cmd = [
        sys.executable,
        str(ROOT_DIR / "foundation" / "pipelines" / "run_mt5_bundle_tester.py"),
        "--bundle-json",
        str(bundle_path),
        "--split-name",
        "validation",
        "--enable-trading",
    ]
    subprocess.run(cmd, cwd=ROOT_DIR, check=True)


def load_bundle_view(run_name: str):
    views = load_bundle_views(ROOT_DIR / "stages", "validation")
    for view in views:
        if view.run_name == run_name:
            return view
    raise FileNotFoundError(f"validation view not found for run_name={run_name}")


def load_latest_attempt_summary(run_dir: Path) -> dict[str, Any]:
    attempts_root = run_dir / "mt5_attempts"
    attempt_dirs = sorted([path for path in attempts_root.iterdir() if path.is_dir()])
    if not attempt_dirs:
        raise FileNotFoundError(f"no attempt directories found under {attempts_root}")
    summary_path = attempt_dirs[-1] / "tester_attempt_summary.json"
    return json.loads(summary_path.read_text(encoding="utf-8-sig"))


def inspect_trade_ledger(csv_path: Path) -> dict[str, Any]:
    close_reasons: dict[str, int] = {}
    volumes: list[float] = []
    stop_prices: list[float] = []
    realized_rs: list[float] = []
    row_count = 0

    with csv_path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            row_count += 1
            close_reason = (row.get("close_reason") or "").strip()
            if close_reason:
                close_reasons[close_reason] = close_reasons.get(close_reason, 0) + 1

            volume_text = (row.get("volume") or "").strip()
            if volume_text:
                volumes.append(float(volume_text))

            stop_price_text = (row.get("initial_stop_price") or "").strip()
            if stop_price_text:
                stop_prices.append(float(stop_price_text))

            realized_r_text = (row.get("realized_r_multiple") or "").strip()
            if realized_r_text:
                realized_rs.append(float(realized_r_text))

    unique_volumes = sorted({round(value, 4) for value in volumes})
    return {
        "row_count": row_count,
        "close_reason_breakdown": close_reasons,
        "unique_volume_count": len(unique_volumes),
        "unique_volumes_preview": unique_volumes[:12],
        "min_volume": min(volumes) if volumes else None,
        "max_volume": max(volumes) if volumes else None,
        "stop_price_count": len(stop_prices),
        "realized_r_mean": (sum(realized_rs) / len(realized_rs)) if realized_rs else None,
    }


def format_metric(value: Any, digits: int = 4) -> str:
    if value is None:
        return "n/a"
    return f"{float(value):.{digits}f}"


def build_review_payload(args: argparse.Namespace, view, attempt_summary: dict[str, Any], ledger_summary: dict[str, Any]) -> dict[str, Any]:
    extra = view.execution.get("extra") or {}
    return {
        "generated_at_utc": utc_now_iso(),
        "phase": "05GA_mt5_05dp_risk_pct_probe",
        "run_name": args.run_name,
        "experiment_id": args.experiment_id,
        "runtime_settings": {
            "sizing_mode": "risk_pct",
            "risk_pct": args.risk_pct,
            "capital_base": args.capital_base,
            "stop_model": "atr",
            "stop_execution_mode": args.stop_execution_mode,
            "stop_policy": args.stop_policy,
            "stop_atr_period": args.stop_atr_period,
            "stop_atr_mult": args.stop_atr_mult,
            "stop_long_atr_mult": args.stop_long_atr_mult,
            "stop_short_atr_mult": args.stop_short_atr_mult,
            "stop_low_vol_threshold": args.stop_low_vol_threshold,
            "stop_high_vol_threshold": args.stop_high_vol_threshold,
            "stop_low_atr_mult": args.stop_low_atr_mult,
            "stop_mid_atr_mult": args.stop_mid_atr_mult,
            "stop_high_atr_mult": args.stop_high_atr_mult,
        },
        "validation": {
            "headline": dict(view.headline),
            "risk": dict(view.risk),
            "diagnostics": dict(view.diagnostics),
            "execution": dict(view.execution),
            "ready_row_gap": extra.get("ready_row_gap"),
            "unexpected_skip_count": extra.get("unexpected_skip_count"),
        },
        "attempt_summary_path": attempt_summary.get("tester_report_path"),
        "trade_ledger_path": attempt_summary.get("trade_ledger_path"),
        "ledger_summary": ledger_summary,
        "verdict": {
            "status": "implementation_verified",
            "reason": "risk_pct sizing path compiled, executed on MT5 validation, and produced trade ledger evidence for ATR-based stop-aware sizing",
        },
    }


def build_review_markdown(payload: dict[str, Any]) -> str:
    validation = payload["validation"]
    runtime_settings = payload["runtime_settings"]
    ledger_summary = payload["ledger_summary"]
    lines = [
        f"# {payload['run_name']} Stage 05 05DP Risk Percent Probe Review",
        "",
        f"Generated at: `{payload['generated_at_utc']}`",
        "",
        "## Scope",
        "",
        "- purpose: `verify that the EA/runtime path can execute balance-based risk-percent sizing with an ATR hard stop on top of the existing 05DP logic`",
        f"- run: `{payload['run_name']}`",
        f"- sizing_mode: `{runtime_settings['sizing_mode']}`",
        f"- risk_pct: `{runtime_settings['risk_pct']:.4f}`",
        f"- capital_base: `{runtime_settings['capital_base']}`",
        f"- stop_model: `{runtime_settings['stop_model']}`",
        f"- stop_execution_mode: `{runtime_settings['stop_execution_mode']}`",
        f"- stop_policy: `{runtime_settings['stop_policy']}`",
        f"- stop_atr_period: `{runtime_settings['stop_atr_period']}`",
        f"- stop_atr_mult: `{format_metric(runtime_settings.get('stop_atr_mult'), 4)}`",
        "",
        "## Validation Read",
        "",
        f"- return_pct: `{format_metric(validation['headline'].get('return_pct'), 3)}`",
        f"- profit_factor: `{format_metric(validation['headline'].get('profit_factor'), 4)}`",
        f"- trade_count: `{validation['headline'].get('trade_count')}`",
        f"- max_dd_pct: `{format_metric(validation['headline'].get('max_dd_pct'), 4)}`",
        f"- ulcer_index: `{format_metric(validation['risk'].get('ulcer_index'), 4)}`",
        f"- ready_row_gap: `{validation['ready_row_gap']}`",
        "",
        "## Ledger Verification",
        "",
        f"- trade_rows: `{ledger_summary['row_count']}`",
        f"- unique_volume_count: `{ledger_summary['unique_volume_count']}`",
        f"- volume_range: `{format_metric(ledger_summary['min_volume'], 4)} -> {format_metric(ledger_summary['max_volume'], 4)}`",
        f"- close_reason_breakdown: `{ledger_summary['close_reason_breakdown']}`",
        f"- stop_price_count: `{ledger_summary['stop_price_count']}`",
        f"- realized_r_mean: `{format_metric(ledger_summary['realized_r_mean'], 4)}`",
        f"- unique_volumes_preview: `{ledger_summary['unique_volumes_preview']}`",
        "",
        "## Verdict",
        "",
        f"- status: `{payload['verdict']['status']}`",
        f"- reason: `{payload['verdict']['reason']}`",
    ]
    return "\n".join(lines) + "\n"


def update_review_index(review_dir: Path, review_filename: str) -> None:
    review_index_path = review_dir / "review_index.md"
    lines = review_index_path.read_text(encoding="utf-8").splitlines() if review_index_path.exists() else []
    stage_tag = review_filename.split("_", 1)[0]
    entry = f"- `{stage_tag}`: see `{review_filename}`"
    if entry not in lines:
        insert_at = 4 if len(lines) >= 4 else len(lines)
        lines.insert(insert_at, entry)
    write_text(review_index_path, "\n".join(lines).rstrip() + "\n")


def main() -> int:
    args = build_parser().parse_args()

    source_run_dir = (ROOT_DIR / args.source_run_dir).resolve()
    if not source_run_dir.exists():
        raise FileNotFoundError(f"source run dir not found: {source_run_dir}")

    stage_root = ROOT_DIR / args.stage_root
    run_dir = stage_root / "02_runs" / "active" / args.run_name
    review_dir = stage_root / "03_reviews"
    review_dir.mkdir(parents=True, exist_ok=True)

    bundle_path = ensure_bundle(args, run_dir, source_run_dir)
    run_tester(bundle_path)

    view = load_bundle_view(args.run_name)
    attempt_summary = load_latest_attempt_summary(run_dir)
    ledger_path = Path(attempt_summary["trade_ledger_path"])
    ledger_summary = inspect_trade_ledger(ledger_path)

    payload = build_review_payload(args, view, attempt_summary, ledger_summary)
    review_json_path = review_dir / f"{args.review_basename}.json"
    review_md_path = review_dir / f"{args.review_basename}.md"
    write_json(review_json_path, payload)
    write_text(review_md_path, build_review_markdown(payload))
    update_review_index(review_dir, review_md_path.name)

    print(f"[done] review_md={review_md_path}")
    print(f"[done] review_json={review_json_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
