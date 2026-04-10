#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import math
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from foundation.pipelines.export_experiment_bundle_assets import run_export_bundle_assets


UTC = timezone.utc


@dataclass(frozen=True)
class WindowSpec:
    window_id: str
    label: str
    split_name: str
    from_date: str
    to_date: str
    use_for_point_derivation: bool = True


@dataclass(frozen=True)
class CandidateSpec:
    stage_id: str
    run_name: str
    experiment_id: str
    variant_label: str
    exit_rule: dict[str, Any] | None


WINDOW_SPECS = [
    WindowSpec(
        window_id="hist_2024",
        label="2024 historical",
        split_name="hist_2024",
        from_date="2024.01.01",
        to_date="2025.01.01",
    ),
    WindowSpec(
        window_id="val_2501",
        label="2025 validation (Jan-Sep)",
        split_name="val_2501",
        from_date="2025.01.01",
        to_date="2025.10.01",
    ),
    WindowSpec(
        window_id="oos_2501",
        label="2501 OOS",
        split_name="oos_2501",
        from_date="2025.10.01",
        to_date="2026.03.01",
        use_for_point_derivation=False,
    ),
]


def utc_now_iso() -> str:
    return datetime.now(tz=UTC).isoformat()


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_json(path: Path, payload: dict[str, Any]) -> None:
    write_text(path, json.dumps(payload, indent=2, ensure_ascii=False) + "\n")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def percentile(values: list[float], quantile: float) -> float:
    ordered = sorted(values)
    if not ordered:
        raise ValueError("cannot compute percentile on empty input")
    if len(ordered) == 1:
        return float(ordered[0])
    position = (len(ordered) - 1) * quantile
    lower = int(math.floor(position))
    upper = int(math.ceil(position))
    if lower == upper:
        return float(ordered[lower])
    weight = position - lower
    return float(ordered[lower] * (1.0 - weight) + ordered[upper] * weight)


def round_to_step(value: float, step: float = 5.0) -> float:
    return round(value / step) * step


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run Stage 22 point-exit management experiments on top of 05DP.")
    parser.add_argument("--stage-root", default="stages/22_point_exit_management", help="Stage 22 root directory.")
    parser.add_argument(
        "--source-run-dir",
        default="stages/05_optimization/02_runs/active/05DP_05ca_margin0675_hold5_0001",
        help="Promoted 05DP source run reused for bundle exports.",
    )
    parser.add_argument("--rebuild-bundle", action="store_true", help="Force bundle rebuilds for every Stage 22 run.")
    return parser


def build_base_rule_stack(extra_exit_rule: dict[str, Any] | None = None) -> dict[str, Any]:
    exit_rules: list[dict[str, Any]] = [
        {
            "rule_id": "exit_01",
            "type": "time_exit",
            "enabled": True,
            "params": {"max_hold_bars": 5},
        }
    ]
    if extra_exit_rule is not None:
        exit_rules.append(extra_exit_rule)

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
        "exit": exit_rules,
    }


def build_baseline_spec() -> CandidateSpec:
    return CandidateSpec(
        stage_id="22A",
        run_name="22A_05dp_base_hold5_0001",
        experiment_id="exp_22a_05dp_base_hold5_v1",
        variant_label="baseline_time_exit",
        exit_rule=None,
    )


def build_candidate_specs(derived_points: dict[str, float]) -> list[CandidateSpec]:
    be_trigger = int(derived_points["break_even_trigger_points"])
    be_offset = int(derived_points["break_even_offset_points"])
    trail_trigger = int(derived_points["trailing_activate_points"])
    trail_distance = int(derived_points["trailing_distance_points"])
    partial_sl_trigger = int(derived_points["partial_stop_loss_trigger_points"])
    partial_tp_trigger = int(derived_points["partial_take_profit_trigger_points"])

    return [
        CandidateSpec(
            stage_id="22B",
            run_name=f"22B_05dp_be{be_trigger:02d}_lock{be_offset:02d}_0001",
            experiment_id=f"exp_22b_05dp_be{be_trigger:02d}_lock{be_offset:02d}_v1",
            variant_label="break_even",
            exit_rule={
                "rule_id": "exit_02",
                "type": "break_even",
                "enabled": True,
                "params": {
                    "trigger_points": derived_points["break_even_trigger_points"],
                    "offset_points": derived_points["break_even_offset_points"],
                },
            },
        ),
        CandidateSpec(
            stage_id="22C",
            run_name=f"22C_05dp_trail{trail_trigger:02d}_dist{trail_distance:02d}_0001",
            experiment_id=f"exp_22c_05dp_trail{trail_trigger:02d}_dist{trail_distance:02d}_v1",
            variant_label="trailing_stop",
            exit_rule={
                "rule_id": "exit_02",
                "type": "trailing_stop",
                "enabled": True,
                "params": {
                    "trigger_points": derived_points["trailing_activate_points"],
                    "distance_points": derived_points["trailing_distance_points"],
                },
            },
        ),
        CandidateSpec(
            stage_id="22D",
            run_name=f"22D_05dp_psl{partial_sl_trigger:02d}_half_0001",
            experiment_id=f"exp_22d_05dp_psl{partial_sl_trigger:02d}_half_v1",
            variant_label="partial_stop_loss",
            exit_rule={
                "rule_id": "exit_02",
                "type": "partial_stop_loss",
                "enabled": True,
                "params": {
                    "trigger_points": derived_points["partial_stop_loss_trigger_points"],
                    "close_fraction": 0.5,
                },
            },
        ),
        CandidateSpec(
            stage_id="22E",
            run_name=f"22E_05dp_ptp{partial_tp_trigger:02d}_half_0001",
            experiment_id=f"exp_22e_05dp_ptp{partial_tp_trigger:02d}_half_v1",
            variant_label="partial_take_profit",
            exit_rule={
                "rule_id": "exit_02",
                "type": "partial_take_profit",
                "enabled": True,
                "params": {
                    "trigger_points": derived_points["partial_take_profit_trigger_points"],
                    "close_fraction": 0.5,
                },
            },
        ),
    ]


def ensure_stage_layout(stage_root: Path) -> None:
    for relative in [
        "00_spec",
        "01_inputs",
        "02_runs/active",
        "02_runs/archived",
        "03_reviews",
        "04_selected",
    ]:
        (stage_root / relative).mkdir(parents=True, exist_ok=True)


def write_stage_brief(stage_root: Path) -> None:
    write_text(
        stage_root / "00_spec" / "stage_brief.md",
        "\n".join(
            [
                "# Stage 22 Point Exit Management",
                "",
                "- goal: `test whether 05DP benefits from simple point-based management exits when each rule is applied individually`",
                "- source run: `05DP_05ca_margin0675_hold5_0001`",
                "- windows: `2024 historical`, `2025 validation Jan-Sep`, `2501 OOS`",
                "- candidates: `break_even`, `trailing_stop`, `partial_stop_loss`, `partial_take_profit`",
                "",
            ]
        ),
    )


def ensure_bundle(
    spec: CandidateSpec,
    *,
    run_root: Path,
    source_run_dir: Path,
    rebuild_bundle: bool,
) -> Path:
    run_dir = run_root / spec.run_name
    run_dir.mkdir(parents=True, exist_ok=True)

    bundle_path = run_dir / "experiment_bundle.json"
    rule_stack_path = run_dir / "rule_stack.json"
    candidate_manifest_path = run_dir / "candidate_manifest.json"

    write_json(rule_stack_path, build_base_rule_stack(spec.exit_rule))
    write_json(
        candidate_manifest_path,
        {
            "generated_at_utc": utc_now_iso(),
            "candidate_type": "05dp_point_exit_management",
            "stage_id": spec.stage_id,
            "run_name": spec.run_name,
            "experiment_id": spec.experiment_id,
            "variant_label": spec.variant_label,
            "source_run_dir": str(source_run_dir),
            "exit_rule": spec.exit_rule,
        },
    )

    if bundle_path.exists() and not rebuild_bundle:
        return bundle_path

    export_args = argparse.Namespace(
        run_dir=str(source_run_dir),
        experiment_id=spec.experiment_id,
        stage_id=spec.stage_id,
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
        sizing_mode="fixed_lot",
        fixed_lot=0.1,
        risk_pct=None,
        capital_base="balance",
        stop_model=None,
        stop_execution_mode="ea_managed",
        stop_policy="fixed",
        stop_atr_period=14,
        stop_atr_mult=None,
        stop_long_atr_mult=None,
        stop_short_atr_mult=None,
        stop_low_vol_threshold=None,
        stop_high_vol_threshold=None,
        stop_low_atr_mult=None,
        stop_mid_atr_mult=None,
        stop_high_atr_mult=None,
        build_bundle=True,
    )
    run_export_bundle_assets(export_args)
    return bundle_path


def parse_attempt_id(stdout_text: str) -> str:
    for line in stdout_text.splitlines():
        if line.startswith("[done] attempt_id="):
            return line.split("=", 1)[1].strip()
    raise ValueError("attempt_id not found in tester output")


def run_window(bundle_path: Path, window: WindowSpec, runtime_id: str) -> tuple[str, Path]:
    cmd = [
        sys.executable,
        str(ROOT_DIR / "foundation" / "pipelines" / "run_mt5_bundle_tester.py"),
        "--bundle-json",
        str(bundle_path),
        "--from-date",
        window.from_date,
        "--to-date",
        window.to_date,
        "--split-name",
        window.split_name,
        "--runtime-id",
        runtime_id,
        "--enable-trading",
        "--skip-leaderboard-refresh",
    ]
    completed = subprocess.run(
        cmd,
        cwd=ROOT_DIR,
        check=True,
        capture_output=True,
        text=True,
    )
    attempt_id = parse_attempt_id(completed.stdout)
    summary_path = bundle_path.parent / "mt5_attempts" / attempt_id / "tester_attempt_summary.json"
    return attempt_id, summary_path


def load_trade_rows(csv_path: Path) -> list[dict[str, Any]]:
    with csv_path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def infer_currency_per_price_point(rows: list[dict[str, Any]]) -> float:
    ratios: list[float] = []
    for row in rows:
        entry_price = float(row["entry_price"])
        exit_price = float(row["exit_price"])
        net_profit = float(row["net_profit"])
        price_distance = abs(exit_price - entry_price)
        if price_distance <= 0.0 or abs(net_profit) <= 0.0:
            continue
        ratios.append(abs(net_profit) / price_distance)
    if not ratios:
        return 0.1
    return percentile(ratios, 0.50)


def build_price_point_distribution(summary_paths: list[Path]) -> dict[str, Any]:
    mfe_points: list[float] = []
    mae_points: list[float] = []
    trade_count = 0
    point_values: list[float] = []

    for summary_path in summary_paths:
        summary = read_json(summary_path)
        trade_rows = load_trade_rows(Path(summary["trade_ledger_path"]))
        if not trade_rows:
            continue
        point_value = infer_currency_per_price_point(trade_rows)
        point_values.append(point_value)
        for row in trade_rows:
            mfe_points.append(max(0.0, float(row["max_floating_profit"])) / point_value)
            mae_points.append(max(0.0, -float(row["min_floating_profit"])) / point_value)
            trade_count += 1

    if not mfe_points or not mae_points:
        raise ValueError("failed to derive point distributions from baseline trades")

    return {
        "trade_count": trade_count,
        "currency_per_price_point": percentile(point_values, 0.50),
        "mfe": {
            "p25": percentile(mfe_points, 0.25),
            "p50": percentile(mfe_points, 0.50),
            "p60": percentile(mfe_points, 0.60),
            "p75": percentile(mfe_points, 0.75),
            "p90": percentile(mfe_points, 0.90),
            "mean": sum(mfe_points) / len(mfe_points),
        },
        "mae": {
            "p25": percentile(mae_points, 0.25),
            "p50": percentile(mae_points, 0.50),
            "p60": percentile(mae_points, 0.60),
            "p75": percentile(mae_points, 0.75),
            "p90": percentile(mae_points, 0.90),
            "mean": sum(mae_points) / len(mae_points),
        },
    }


def derive_point_plan(distribution: dict[str, Any]) -> dict[str, float]:
    mfe = distribution["mfe"]
    mae = distribution["mae"]
    return {
        "break_even_trigger_points": round_to_step((float(mfe["p50"]) + float(mfe["p60"])) / 2.0),
        "break_even_offset_points": round_to_step(max(10.0, float(mfe["p25"]) * 0.4)),
        "trailing_activate_points": round_to_step(float(mfe["p60"])),
        "trailing_distance_points": round_to_step(max(20.0, float(mae["p50"]) * 0.85)),
        "partial_stop_loss_trigger_points": round_to_step((float(mae["p50"]) + float(mae["p60"])) / 2.0),
        "partial_take_profit_trigger_points": round_to_step(float(mfe["p60"])),
        "partial_close_fraction": 0.5,
    }


def format_metric(value: Any, digits: int = 3) -> str:
    if value is None:
        return "n/a"
    return f"{float(value):.{digits}f}"


def collect_window_result(spec: CandidateSpec, window: WindowSpec, summary_path: Path) -> dict[str, Any]:
    summary = read_json(summary_path)
    headline = summary["financial_metrics"]["headline"]
    return {
        "stage_id": spec.stage_id,
        "run_name": spec.run_name,
        "variant_label": spec.variant_label,
        "window_id": window.window_id,
        "window_label": window.label,
        "summary_path": str(summary_path),
        "trade_ledger_path": summary["trade_ledger_path"],
        "return_pct": headline.get("return_pct"),
        "profit_factor": headline.get("profit_factor"),
        "trade_count": headline.get("trade_count"),
        "max_dd_pct": headline.get("max_dd_pct"),
        "net_profit": headline.get("net_profit"),
        "final_balance": (headline.get("extra") or {}).get("final_balance"),
        "attempt_id": summary["attempt_id"],
    }


def build_review_payload(
    *,
    baseline_spec: CandidateSpec,
    candidate_specs: list[CandidateSpec],
    window_results: dict[str, list[dict[str, Any]]],
    distribution: dict[str, Any],
    derived_points: dict[str, float],
) -> dict[str, Any]:
    all_specs = [baseline_spec, *candidate_specs]
    aggregate_rows: list[dict[str, Any]] = []
    baseline_lookup: dict[str, dict[str, Any]] = {}

    for result in window_results.values():
        for row in result:
            if row["run_name"] == baseline_spec.run_name:
                baseline_lookup[row["window_id"]] = row

    for spec in all_specs:
        rows = [row for result in window_results.values() for row in result if row["run_name"] == spec.run_name]
        window_wins = 0
        for row in rows:
            baseline = baseline_lookup[row["window_id"]]
            if float(row["return_pct"] or 0.0) > float(baseline["return_pct"] or 0.0):
                window_wins += 1
        aggregate_rows.append(
            {
                "stage_id": spec.stage_id,
                "run_name": spec.run_name,
                "variant_label": spec.variant_label,
                "window_wins": window_wins,
                "avg_return_pct": sum(float(row["return_pct"] or 0.0) for row in rows) / len(rows),
                "avg_profit_factor": sum(float(row["profit_factor"] or 0.0) for row in rows) / len(rows),
                "worst_max_dd_pct": max(float(row["max_dd_pct"] or 0.0) for row in rows),
            }
        )

    aggregate_rows.sort(
        key=lambda row: (
            int(row["window_wins"]),
            float(row["avg_return_pct"]),
            float(row["avg_profit_factor"]),
            -float(row["worst_max_dd_pct"]),
        ),
        reverse=True,
    )

    baseline_aggregate = next(row for row in aggregate_rows if row["run_name"] == baseline_spec.run_name)
    best_row = aggregate_rows[0]
    if (
        best_row["run_name"] != baseline_spec.run_name
        and int(best_row["window_wins"]) >= 2
        and float(best_row["avg_return_pct"]) > float(baseline_aggregate["avg_return_pct"])
        and float(best_row["worst_max_dd_pct"]) <= float(baseline_aggregate["worst_max_dd_pct"]) + 5.0
    ):
        verdict = {
            "status": "promote_candidate",
            "selected_run_name": best_row["run_name"],
            "reason": "candidate beat the baseline in at least two windows without materially worse worst-window drawdown",
        }
    else:
        verdict = {
            "status": "reject_keep_incumbent",
            "selected_run_name": baseline_spec.run_name,
            "reason": "no point-exit candidate cleared the baseline across the three-window check",
        }

    ranked_windows: dict[str, list[dict[str, Any]]] = {}
    for window in WINDOW_SPECS:
        ranked = sorted(
            window_results[window.window_id],
            key=lambda row: (
                float(row["return_pct"] or float("-inf")),
                float(row["profit_factor"] or float("-inf")),
            ),
            reverse=True,
        )
        ranked_windows[window.window_id] = [{"rank": idx + 1, **row} for idx, row in enumerate(ranked)]

    return {
        "generated_at_utc": utc_now_iso(),
        "phase": "22_point_exit_management_batch",
        "source_run_name": "05DP_05ca_margin0675_hold5_0001",
        "windows": [window.__dict__ for window in WINDOW_SPECS],
        "distribution": distribution,
        "derived_points": derived_points,
        "ranked_by_window": ranked_windows,
        "aggregate": aggregate_rows,
        "verdict": verdict,
    }


def build_review_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# 22 Point Exit Management Review",
        "",
        f"Generated at: `{payload['generated_at_utc']}`",
        "",
        "## Scope",
        "",
        "- source: `05DP_05ca_margin0675_hold5_0001`",
        "- experiment style: `keep time_exit hold5 and add one point-based management rule at a time`",
        "- windows: `2024 historical`, `2025 validation Jan-Sep`, `2501 OOS`",
        "",
        "## Derived Point Plan",
        "",
        f"- baseline trade count used for sizing: `{payload['distribution']['trade_count']}`",
        f"- combined MFE p50/p60: `{format_metric(payload['distribution']['mfe']['p50'], 1)}` / `{format_metric(payload['distribution']['mfe']['p60'], 1)}`",
        f"- combined MAE p50/p60: `{format_metric(payload['distribution']['mae']['p50'], 1)}` / `{format_metric(payload['distribution']['mae']['p60'], 1)}`",
        f"- break-even: `trigger={format_metric(payload['derived_points']['break_even_trigger_points'], 0)}` `lock={format_metric(payload['derived_points']['break_even_offset_points'], 0)}`",
        f"- trailing stop: `activate={format_metric(payload['derived_points']['trailing_activate_points'], 0)}` `distance={format_metric(payload['derived_points']['trailing_distance_points'], 0)}`",
        f"- partial stop loss: `trigger={format_metric(payload['derived_points']['partial_stop_loss_trigger_points'], 0)}` `close_fraction=0.50`",
        f"- partial take profit: `trigger={format_metric(payload['derived_points']['partial_take_profit_trigger_points'], 0)}` `close_fraction=0.50`",
        "",
    ]

    for window in WINDOW_SPECS:
        lines.extend([f"## {window.label}", ""])
        for row in payload["ranked_by_window"][window.window_id]:
            lines.append(
                f"- [{row['rank']}] `{row['run_name']}` `{row['variant_label']}`: "
                f"return_pct `{format_metric(row['return_pct'], 3)}`, "
                f"PF `{format_metric(row['profit_factor'], 4)}`, "
                f"trades `{row['trade_count']}`, "
                f"max_dd_pct `{format_metric(row['max_dd_pct'], 3)}`"
            )
        lines.append("")

    lines.extend(["## Aggregate", ""])
    for row in payload["aggregate"]:
        lines.append(
            f"- `{row['run_name']}` `{row['variant_label']}`: "
            f"window_wins `{row['window_wins']}`, "
            f"avg_return_pct `{format_metric(row['avg_return_pct'], 3)}`, "
            f"avg_PF `{format_metric(row['avg_profit_factor'], 4)}`, "
            f"worst_max_dd_pct `{format_metric(row['worst_max_dd_pct'], 3)}`"
        )

    verdict = payload["verdict"]
    lines.extend(
        [
            "",
            "## Verdict",
            "",
            f"- status: `{verdict['status']}`",
            f"- selected_run_name: `{verdict['selected_run_name']}`",
            f"- reason: `{verdict['reason']}`",
            "",
        ]
    )
    return "\n".join(lines)


def build_selection_markdown(payload: dict[str, Any]) -> str:
    verdict = payload["verdict"]
    return "\n".join(
        [
            "# Stage 22 Selection Status",
            "",
            f"- generated_at_utc: `{payload['generated_at_utc']}`",
            f"- selected_run_name: `{verdict['selected_run_name']}`",
            f"- status: `{verdict['status']}`",
            f"- reason: `{verdict['reason']}`",
            "",
            "## Derived Points",
            "",
            f"- break_even: `trigger={format_metric(payload['derived_points']['break_even_trigger_points'], 0)}` `lock={format_metric(payload['derived_points']['break_even_offset_points'], 0)}`",
            f"- trailing_stop: `activate={format_metric(payload['derived_points']['trailing_activate_points'], 0)}` `distance={format_metric(payload['derived_points']['trailing_distance_points'], 0)}`",
            f"- partial_stop_loss: `trigger={format_metric(payload['derived_points']['partial_stop_loss_trigger_points'], 0)}` `close_fraction=0.50`",
            f"- partial_take_profit: `trigger={format_metric(payload['derived_points']['partial_take_profit_trigger_points'], 0)}` `close_fraction=0.50`",
            "",
        ]
    )


def update_review_index(stage_root: Path) -> None:
    review_index_path = stage_root / "03_reviews" / "review_index.md"
    entry = "- `22PE`: see `22PE_05dp_point_exit_management_review.md`"
    lines = review_index_path.read_text(encoding="utf-8").splitlines() if review_index_path.exists() else []
    if entry not in lines:
        lines.append(entry)
    write_text(review_index_path, "\n".join(lines).rstrip() + "\n")


def main() -> int:
    args = build_parser().parse_args()
    stage_root = (ROOT_DIR / args.stage_root).resolve()
    source_run_dir = (ROOT_DIR / args.source_run_dir).resolve()
    if not source_run_dir.exists():
        raise FileNotFoundError(f"source run dir not found: {source_run_dir}")

    ensure_stage_layout(stage_root)
    write_stage_brief(stage_root)

    run_root = stage_root / "02_runs" / "active"
    baseline_spec = build_baseline_spec()
    baseline_bundle = ensure_bundle(
        baseline_spec,
        run_root=run_root,
        source_run_dir=source_run_dir,
        rebuild_bundle=args.rebuild_bundle,
    )

    baseline_summary_paths: list[Path] = []
    baseline_window_results: dict[str, dict[str, Any]] = {}
    for window in WINDOW_SPECS:
        runtime_id = f"exp_22a_05dp_base_{window.window_id}_v1"
        _, summary_path = run_window(baseline_bundle, window, runtime_id)
        if window.use_for_point_derivation:
            baseline_summary_paths.append(summary_path)
        baseline_window_results[window.window_id] = collect_window_result(baseline_spec, window, summary_path)

    distribution = build_price_point_distribution(baseline_summary_paths)
    derived_points = derive_point_plan(distribution)

    input_manifest = {
        "generated_at_utc": utc_now_iso(),
        "source_run_name": "05DP_05ca_margin0675_hold5_0001",
        "source_run_dir": str(source_run_dir),
        "windows": [window.__dict__ for window in WINDOW_SPECS],
        "distribution": distribution,
        "derived_points": derived_points,
    }
    write_json(stage_root / "01_inputs" / "input_manifest.json", input_manifest)

    candidate_specs = build_candidate_specs(derived_points)
    window_results: dict[str, list[dict[str, Any]]] = {window.window_id: [baseline_window_results[window.window_id]] for window in WINDOW_SPECS}

    for spec in candidate_specs:
        bundle_path = ensure_bundle(
            spec,
            run_root=run_root,
            source_run_dir=source_run_dir,
            rebuild_bundle=args.rebuild_bundle,
        )
        for window in WINDOW_SPECS:
            runtime_id = f"{spec.experiment_id}_{window.window_id}"
            _, summary_path = run_window(bundle_path, window, runtime_id)
            window_results[window.window_id].append(collect_window_result(spec, window, summary_path))

    review_payload = build_review_payload(
        baseline_spec=baseline_spec,
        candidate_specs=candidate_specs,
        window_results=window_results,
        distribution=distribution,
        derived_points=derived_points,
    )
    review_json_path = stage_root / "03_reviews" / "22PE_05dp_point_exit_management_review.json"
    review_md_path = stage_root / "03_reviews" / "22PE_05dp_point_exit_management_review.md"
    write_json(review_json_path, review_payload)
    write_text(review_md_path, build_review_markdown(review_payload) + "\n")
    update_review_index(stage_root)

    selection_path = stage_root / "04_selected" / "selection_status.md"
    write_text(selection_path, build_selection_markdown(review_payload) + "\n")

    print(f"[done] input_manifest={stage_root / '01_inputs' / 'input_manifest.json'}")
    print(f"[done] review_json={review_json_path}")
    print(f"[done] review_md={review_md_path}")
    print(f"[done] selection={selection_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
