#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from foundation.pipelines.experiment_bundle_models import ExperimentBundle
from foundation.pipelines.export_experiment_bundle_assets import run_export_bundle_assets
from foundation.pipelines.run_mt5_bundle_tester import (
    classify_skip_reasons,
    parse_mt5_time,
    parse_shadow_csv,
    parse_trade_ledger,
    summarize_financial_metrics,
)


UTC = timezone.utc


def utc_now_iso() -> str:
    return datetime.now(tz=UTC).isoformat()


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_json(path: Path, payload: dict[str, Any]) -> None:
    write_text(path, json.dumps(payload, indent=2, ensure_ascii=False) + "\n")


def format_metric(value: Any, digits: int = 4) -> str:
    if value is None:
        return "n/a"
    return f"{float(value):.{digits}f}"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run Stage 06 segmented risk overlay on the 05DP base with the Stage 05 direction-split leader.")
    parser.add_argument("--stage-root", default="stages/06_segmented_risk_validation", help="Stage 06 root directory.")
    parser.add_argument(
        "--source-run-dir",
        default="stages/05_optimization/02_runs/active/05DP_05ca_margin0675_hold5_0001",
        help="Source trained run directory providing model.joblib.",
    )
    parser.add_argument("--run-name", default="06A_dirsplit2pct_0001", help="Stage 06 run folder name.")
    parser.add_argument("--experiment-id", default="exp_06a_dirsplit2pct_v1", help="Experiment id.")
    parser.add_argument("--stage-id", default="06A", help="Stage id.")
    parser.add_argument("--review-basename", default="06A_segmented_risk_review", help="Review basename.")
    parser.add_argument("--risk-pct", type=float, default=2.0, help="Percent of balance to risk.")
    parser.add_argument("--stop-atr-period", type=int, default=14, help="ATR period.")
    parser.add_argument("--stop-long-atr-mult", type=float, default=1.4, help="Long-side ATR multiplier.")
    parser.add_argument("--stop-short-atr-mult", type=float, default=2.0, help="Short-side ATR multiplier.")
    parser.add_argument("--rebuild-bundle", action="store_true", help="Force bundle rebuild.")
    return parser


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


def stage06_paths(stage_root: Path) -> dict[str, Path]:
    return {
        "spec": stage_root / "00_spec" / "stage_brief.md",
        "inputs": stage_root / "01_inputs" / "input_manifest.json",
        "review_index": stage_root / "03_reviews" / "review_index.md",
        "selection": stage_root / "04_selected" / "selection_status.md",
    }


def update_review_index(review_dir: Path, review_filename: str) -> None:
    review_index_path = review_dir / "review_index.md"
    lines = review_index_path.read_text(encoding="utf-8").splitlines() if review_index_path.exists() else []
    entry = f"- `06A`: see `{review_filename}`"
    if "pending" in "\n".join(lines):
        lines = [line for line in lines if "pending" not in line]
    if entry not in lines:
        insert_at = 4 if len(lines) >= 4 else len(lines)
        lines.insert(insert_at, entry)
    write_text(review_index_path, "\n".join(lines).rstrip() + "\n")


def update_selection_status(selection_path: Path, payload: dict[str, Any]) -> None:
    validation = payload["split_runs"]["validation"]["headline"]
    test = payload["split_runs"]["test"]["headline"]
    best_segment = payload["cross_segment_summary"]["best_segment"]
    overlay = payload["overlay"]
    lines = [
        "# Selection Status",
        "",
        "- stage: `06_segmented_risk_validation`",
        "- current phase complete: `06A`",
        f"- current promoted segmented risk run: `{payload['run_name']}`",
        "- current mode: `single-run segmented overlay verification`",
        f"- overlay config: `risk_pct={format_metric(overlay.get('risk_pct'), 2)}, broker_native SL, direction_split(long={format_metric(overlay.get('stop_long_atr_mult'), 2)}, short={format_metric(overlay.get('stop_short_atr_mult'), 2)}), ATR{int(overlay.get('stop_atr_period', 14))}`",
        f"- validation headline: `return_pct={format_metric(validation.get('return_pct'), 3)}, PF={format_metric(validation.get('profit_factor'), 4)}, trades={validation.get('trade_count')}, max_dd_pct={format_metric(validation.get('max_dd_pct'), 4)}`",
        f"- holdout headline: `return_pct={format_metric(test.get('return_pct'), 3)}, PF={format_metric(test.get('profit_factor'), 4)}, trades={test.get('trade_count')}, max_dd_pct={format_metric(test.get('max_dd_pct'), 4)}`",
        f"- best segment read: `{best_segment['split']}::{best_segment['segment']}`, `return_pct={format_metric(best_segment.get('return_pct'), 3)}`, `PF={format_metric(best_segment.get('profit_factor'), 4)}`",
        "- next action: `expand Stage 06 to multi-run batch coverage if this overlay shape is worth scaling across the pre-risk 05A~05FZ pool`",
    ]
    write_text(selection_path, "\n".join(lines) + "\n")


def ensure_stage_inputs_manifest(inputs_path: Path, args: argparse.Namespace) -> None:
    payload = {
        "generated_at_utc": utc_now_iso(),
        "stage": "06_segmented_risk_validation",
        "input_reference": {
            "model_source_run": args.source_run_dir,
            "risk_policy_reference_review": "stages/05_optimization/03_reviews/05GL_mt5_stop_policy_progression_review.md",
            "direction_split_leader_run": "stages/05_optimization/02_runs/active/05GK_05dp_dirsplit_l14_s20_riskpct300_0001",
        },
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
        "segment_scheme": {
            "validation": [
                ["validation_q1", "2025-01-01 00:00:00", "2025-04-01 00:00:00"],
                ["validation_q2", "2025-04-01 00:00:00", "2025-07-01 00:00:00"],
                ["validation_q3", "2025-07-01 00:00:00", "2025-10-01 00:00:00"],
            ],
            "test": [
                ["holdout_a", "2025-10-01 00:00:00", "2025-11-16 00:00:00"],
                ["holdout_b", "2025-11-16 00:00:00", "2026-01-01 00:00:00"],
                ["holdout_c", "2026-01-01 00:00:00", "2026-03-01 00:00:00"],
            ],
        },
    }
    write_json(inputs_path, payload)


def ensure_bundle(args: argparse.Namespace, run_dir: Path, source_run_dir: Path) -> Path:
    bundle_path = run_dir / "experiment_bundle.json"
    rule_stack_path = run_dir / "rule_stack.json"
    overlay_manifest_path = run_dir / "overlay_manifest.json"
    write_json(rule_stack_path, build_rule_stack())
    write_json(
        overlay_manifest_path,
        {
            "generated_at_utc": utc_now_iso(),
            "run_name": args.run_name,
            "experiment_id": args.experiment_id,
            "stage_id": args.stage_id,
            "source_run_dir": str(source_run_dir),
            "overlay": {
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
            "segment_scheme_name": "validation_q3_holdout_3way",
        },
    )

    if bundle_path.exists() and not args.rebuild_bundle:
        return bundle_path

    export_args = argparse.Namespace(
        run_dir=str(source_run_dir),
        experiment_id=args.experiment_id,
        stage_id=args.stage_id,
        output_dir=str(run_dir),
        stage_name="segmented_risk_validation",
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
    return bundle_path


def run_tester(bundle_path: Path, split_name: str) -> None:
    cmd = [
        sys.executable,
        str(ROOT_DIR / "foundation" / "pipelines" / "run_mt5_bundle_tester.py"),
        "--bundle-json",
        str(bundle_path),
        "--split-name",
        split_name,
        "--enable-trading",
    ]
    subprocess.run(cmd, cwd=ROOT_DIR, check=True)


def load_attempt_summaries(run_dir: Path) -> dict[str, dict[str, Any]]:
    attempts_root = run_dir / "mt5_attempts"
    out: dict[str, dict[str, Any]] = {}
    for attempt_dir in sorted(path for path in attempts_root.iterdir() if path.is_dir()):
        summary_path = attempt_dir / "tester_attempt_summary.json"
        if not summary_path.exists():
            continue
        payload = json.loads(summary_path.read_text(encoding="utf-8-sig"))
        split_name = str(payload.get("split_name", "")).strip().lower()
        if split_name:
            out[split_name] = payload
    return out


def parse_shadow_rows(rows: list[dict[str, str]]) -> dict[str, object]:
    if not rows:
        return {
            "row_count": 0,
            "ready_row_count": 0,
            "skip_row_count": 0,
            "ready_rate": 0.0,
            "long_signal_count": 0,
            "short_signal_count": 0,
            "no_trade_count": 0,
            "no_trade_rate": 1.0,
            "skip_reason_breakdown": {},
            "external_mismatch_count": 0,
            "data_readiness_failures": 0,
            "feature_ready_max": 0,
            "latest_bar_time_server": None,
            "contract_skip_breakdown": {},
            "contract_skip_count": 0,
            "startup_skip_breakdown": {},
            "startup_skip_count": 0,
            "unexpected_skip_breakdown": {},
            "unexpected_skip_count": 0,
            "rows": [],
        }

    total_rows = len(rows)
    ready_rows = [row for row in rows if row.get("row_ready", "").lower() == "true"]
    skipped_rows = [row for row in rows if row.get("row_ready", "").lower() != "true"]
    decisions = Counter(row.get("decision", "") for row in ready_rows)
    skip_reasons = Counter(row.get("skip_reason", "") for row in skipped_rows if row.get("skip_reason", ""))
    classified = classify_skip_reasons(skip_reasons)
    external_mismatch_count = sum(
        count for reason, count in skip_reasons.items() if reason.startswith("EXTERNAL_TIMESTAMP_MISMATCH")
    )
    data_readiness_failures = sum(
        count for reason, count in skip_reasons.items() if "NOT_READY" in reason or "WARMUP" in reason or "MODEL_NOT_READY" in reason
    )
    feature_ready_max = max(int(row.get("feature_ready_count", "0") or 0) for row in rows)
    ready_rate = (len(ready_rows) / total_rows) if total_rows else 0.0
    no_trade_rate = (decisions.get("NO_TRADE", 0) / len(ready_rows)) if ready_rows else 1.0
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
        "latest_bar_time_server": rows[-1].get("bar_time_server"),
        **classified,
        "rows": rows,
    }


def segment_scheme() -> dict[str, list[tuple[str, datetime, datetime]]]:
    return {
        "validation": [
            ("validation_q1", datetime(2025, 1, 1, 0, 0, 0), datetime(2025, 4, 1, 0, 0, 0)),
            ("validation_q2", datetime(2025, 4, 1, 0, 0, 0), datetime(2025, 7, 1, 0, 0, 0)),
            ("validation_q3", datetime(2025, 7, 1, 0, 0, 0), datetime(2025, 10, 1, 0, 0, 0)),
        ],
        "test": [
            ("holdout_a", datetime(2025, 10, 1, 0, 0, 0), datetime(2025, 11, 16, 0, 0, 0)),
            ("holdout_b", datetime(2025, 11, 16, 0, 0, 0), datetime(2026, 1, 1, 0, 0, 0)),
            ("holdout_c", datetime(2026, 1, 1, 0, 0, 0), datetime(2026, 3, 1, 0, 0, 0)),
        ],
    }


def filter_shadow_rows(rows: list[dict[str, str]], start: datetime, end: datetime) -> list[dict[str, str]]:
    out: list[dict[str, str]] = []
    for row in rows:
        bar_time = parse_mt5_time(row.get("bar_time_server"))
        if bar_time is None:
            continue
        if start <= bar_time < end:
            out.append(row)
    return out


def filter_trades(trades: list[dict[str, Any]], start: datetime, end: datetime) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for trade in trades:
        exit_bar_time = trade.get("exit_bar_time") or trade.get("exit_time")
        if not isinstance(exit_bar_time, datetime):
            continue
        if start <= exit_bar_time < end:
            out.append(trade)
    return out


def build_segment_results(
    bundle: ExperimentBundle,
    split_name: str,
    summary: dict[str, Any],
    scheme: dict[str, list[tuple[str, datetime, datetime]]] | None = None,
) -> dict[str, Any]:
    shadow_path = Path(summary["csv_log_path"])
    trade_ledger_path = Path(summary["trade_ledger_path"])
    parsed_shadow = parse_shadow_csv(shadow_path)
    trades = parse_trade_ledger(trade_ledger_path)
    active_scheme = scheme or segment_scheme()

    segment_payloads: list[dict[str, Any]] = []
    for segment_name, start, end in active_scheme[split_name]:
        segment_shadow_rows = filter_shadow_rows(parsed_shadow["rows"], start, end)
        segment_shadow = parse_shadow_rows(segment_shadow_rows)
        segment_trades = filter_trades(trades, start, end)
        segment_metrics = summarize_financial_metrics(
            bundle=bundle,
            shadow_rows=segment_shadow_rows,
            trades=segment_trades,
            parsed_shadow=segment_shadow,
        )
        segment_payloads.append(
            {
                "segment": segment_name,
                "start_server": start.strftime("%Y.%m.%d %H:%M:%S"),
                "end_server_exclusive": end.strftime("%Y.%m.%d %H:%M:%S"),
                "headline": segment_metrics["headline"],
                "risk": segment_metrics["risk"],
                "diagnostics": segment_metrics["diagnostics"],
                "execution": segment_metrics["execution"],
                "coverage": {
                    "row_count": segment_shadow["row_count"],
                    "ready_row_count": segment_shadow["ready_row_count"],
                    "skip_row_count": segment_shadow["skip_row_count"],
                },
            }
        )
    return {
        "summary_path": str(Path(summary["tester_ini_path"]).with_name("tester_attempt_summary.json")),
        "csv_log_path": summary["csv_log_path"],
        "trade_ledger_path": summary["trade_ledger_path"],
        "segments": segment_payloads,
    }


def build_cross_segment_summary(segmented: dict[str, Any]) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    for split_name, split_payload in segmented.items():
        for segment in split_payload["segments"]:
            headline = segment["headline"]
            risk = segment["risk"]
            rows.append(
                {
                    "split": split_name,
                    "segment": segment["segment"],
                    "return_pct": headline.get("return_pct"),
                    "profit_factor": headline.get("profit_factor"),
                    "trade_count": headline.get("trade_count"),
                    "max_dd_pct": risk.get("max_dd_pct"),
                    "ulcer_index": risk.get("ulcer_index"),
                }
            )

    def key_return(item: dict[str, Any]) -> float:
        value = item.get("return_pct")
        return float(value) if value is not None else float("-inf")

    best_segment = max(rows, key=key_return)
    worst_segment = min(rows, key=key_return)
    pf_values = [float(item["profit_factor"]) for item in rows if item.get("profit_factor") is not None]
    ulcer_values = [float(item["ulcer_index"]) for item in rows if item.get("ulcer_index") is not None]
    return {
        "best_segment": best_segment,
        "worst_segment": worst_segment,
        "profit_factor_range": {
            "min": min(pf_values) if pf_values else None,
            "max": max(pf_values) if pf_values else None,
        },
        "ulcer_range": {
            "min": min(ulcer_values) if ulcer_values else None,
            "max": max(ulcer_values) if ulcer_values else None,
        },
    }


def build_review_markdown(payload: dict[str, Any]) -> str:
    overlay = payload["overlay"]
    lines = [
        "# 06A Stage 06 Direction-Split Risk Overlay Review",
        "",
        f"Generated at: `{payload['generated_at_utc']}`",
        "",
        "## Scope",
        "",
        f"- run: `{payload['run_name']}`",
        f"- source_run_dir: `{payload['source_run_dir']}`",
        f"- overlay: `risk_pct={format_metric(overlay.get('risk_pct'), 2)}, broker_native SL, direction_split(long={format_metric(overlay.get('stop_long_atr_mult'), 2)}, short={format_metric(overlay.get('stop_short_atr_mult'), 2)}), ATR{int(overlay.get('stop_atr_period', 14))}`",
        "",
        "## Split Headline",
        "",
    ]

    for split_name in ["validation", "test"]:
        split_headline = payload["split_runs"][split_name]["headline"]
        split_risk = payload["split_runs"][split_name]["risk"]
        lines.append(
            f"- `{split_name}`: return_pct `{format_metric(split_headline.get('return_pct'), 3)}`, "
            f"PF `{format_metric(split_headline.get('profit_factor'), 4)}`, "
            f"trades `{split_headline.get('trade_count')}`, "
            f"max_dd_pct `{format_metric(split_headline.get('max_dd_pct'), 4)}`, "
            f"ulcer `{format_metric(split_risk.get('ulcer_index'), 4)}`"
        )

    lines.extend(["", "## Segments", ""])
    for split_name in ["validation", "test"]:
        lines.append(f"### {split_name}")
        lines.append("")
        for segment in payload["segmented_results"][split_name]["segments"]:
            headline = segment["headline"]
            risk = segment["risk"]
            lines.append(
                f"- `{segment['segment']}`: return_pct `{format_metric(headline.get('return_pct'), 3)}`, "
                f"PF `{format_metric(headline.get('profit_factor'), 4)}`, "
                f"trades `{headline.get('trade_count')}`, "
                f"max_dd_pct `{format_metric(risk.get('max_dd_pct'), 4)}`, "
                f"ulcer `{format_metric(risk.get('ulcer_index'), 4)}`"
            )
        lines.append("")

    best = payload["cross_segment_summary"]["best_segment"]
    worst = payload["cross_segment_summary"]["worst_segment"]
    lines.extend([
        "## Cross-Segment Summary",
        "",
        f"- best_segment: `{best['split']}::{best['segment']}`, return_pct `{format_metric(best.get('return_pct'), 3)}`, PF `{format_metric(best.get('profit_factor'), 4)}`",
        f"- worst_segment: `{worst['split']}::{worst['segment']}`, return_pct `{format_metric(worst.get('return_pct'), 3)}`, PF `{format_metric(worst.get('profit_factor'), 4)}`",
        "",
    ])
    return "\n".join(lines) + "\n"


def main() -> int:
    args = build_parser().parse_args()

    stage_root = ROOT_DIR / args.stage_root
    paths = stage06_paths(stage_root)
    ensure_stage_inputs_manifest(paths["inputs"], args)

    source_run_dir = (ROOT_DIR / args.source_run_dir).resolve()
    if not source_run_dir.exists():
        raise FileNotFoundError(f"source run dir not found: {source_run_dir}")

    run_dir = stage_root / "02_runs" / "active" / args.run_name
    review_dir = stage_root / "03_reviews"
    review_dir.mkdir(parents=True, exist_ok=True)

    bundle_path = ensure_bundle(args, run_dir, source_run_dir)
    run_tester(bundle_path, "validation")
    run_tester(bundle_path, "test")

    bundle = ExperimentBundle.from_json(bundle_path.read_text(encoding="utf-8-sig"))
    summaries = load_attempt_summaries(run_dir)
    if "validation" not in summaries or "test" not in summaries:
        raise FileNotFoundError("expected both validation and test attempt summaries in Stage 06 run")

    segmented_results = {
        "validation": build_segment_results(bundle, "validation", summaries["validation"]),
        "test": build_segment_results(bundle, "test", summaries["test"]),
    }
    cross_segment_summary = build_cross_segment_summary(segmented_results)

    payload = {
        "generated_at_utc": utc_now_iso(),
        "stage": "06_segmented_risk_validation",
        "run_name": args.run_name,
        "experiment_id": args.experiment_id,
        "source_run_dir": str(source_run_dir),
        "overlay": {
            "risk_pct": args.risk_pct,
            "stop_execution_mode": "broker_native",
            "stop_policy": "direction_split",
            "stop_long_atr_mult": args.stop_long_atr_mult,
            "stop_short_atr_mult": args.stop_short_atr_mult,
            "stop_atr_period": args.stop_atr_period,
        },
        "split_runs": {
            "validation": bundle.results.by_split["validation"].model_dump(),
            "test": bundle.results.by_split["test"].model_dump(),
        },
        "segmented_results": segmented_results,
        "cross_segment_summary": cross_segment_summary,
    }

    segmented_json_path = run_dir / "segmented_results.json"
    segmented_md_path = run_dir / "segmented_results.md"
    review_json_path = review_dir / f"{args.review_basename}.json"
    review_md_path = review_dir / f"{args.review_basename}.md"
    write_json(segmented_json_path, payload)
    write_text(segmented_md_path, build_review_markdown(payload))
    write_json(review_json_path, payload)
    write_text(review_md_path, build_review_markdown(payload))

    update_review_index(review_dir, review_md_path.name)
    update_selection_status(paths["selection"], payload)

    print(f"[done] bundle={bundle_path}")
    print(f"[done] segmented_json={segmented_json_path}")
    print(f"[done] segmented_md={segmented_md_path}")
    print(f"[done] review_md={review_md_path}")
    print(f"[done] review_json={review_json_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
