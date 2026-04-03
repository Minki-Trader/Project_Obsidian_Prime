#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pandas as pd

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from foundation.pipelines.experiment_bundle_models import ExperimentBundle
from foundation.pipelines.run_stage05_logic_family_probe import load_latest_family_summary
from foundation.pipelines.run_stage05_mt5_confirmation_batch import (
    CandidateSpec,
    ensure_bundle,
    extract_filter_param,
    run_tester,
)
from foundation.pipelines.show_experiment_leaderboard import BundleView, load_bundle_views, sort_bundle_views


FRONTIER_STAGE_IDS = {
    ("margin", 0): "05E",
    ("margin", 1): "05F",
    ("diff", 0): "05G",
    ("diff", 1): "05H",
}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the next Stage 05 MT5 validation frontier batch.")
    parser.add_argument("--stage-root", default="stages/05_optimization", help="Stage 05 root directory.")
    parser.add_argument(
        "--final-run-dir",
        default="stages/01_base_feature_ml/02_runs/active/01D_run_0001_final_h03_band000125_logreg",
        help="Stage 01 final model run directory used for bundle export.",
    )
    parser.add_argument("--split-name", default="validation", help="Logical split name for MT5 tester results.")
    parser.add_argument("--n-per-family", type=int, default=2, help="How many untested frontier values to run per family.")
    parser.add_argument("--rebuild-bundle", action="store_true", help="Force bundle rebuild when rerunning.")
    return parser


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_json(path: Path, payload: dict[str, Any]) -> None:
    write_text(path, json.dumps(payload, indent=2, ensure_ascii=False) + "\n")


def latest_probe_run_dir(stage_root: Path, family: str) -> Path:
    summary = load_latest_family_summary(stage_root, family)
    if summary is None:
        raise FileNotFoundError(f"missing latest Stage 05 {family} family summary")
    return stage_root / "02_runs" / summary["run_bucket"] / summary["run_name"]


def collect_tested_values(family: str) -> set[float]:
    tested: set[float] = set()
    for bundle_path in (ROOT_DIR / "stages").rglob("experiment_bundle.json"):
        bundle = ExperimentBundle.from_json(bundle_path.read_text(encoding="utf-8-sig"))
        for rule in bundle.rule_stack.filters:
            if not rule.enabled:
                continue
            if family == "margin" and rule.type == "max_probability_margin":
                value = rule.params.get("min_margin")
                if value is not None:
                    tested.add(round(float(value), 4))
            if family == "diff" and rule.type == "probability_difference":
                value = rule.params.get("min_probability_diff")
                if value is not None:
                    tested.add(round(float(value), 4))
    return tested


def load_frontier_values(stage_root: Path, family: str, n_per_family: int) -> list[float]:
    run_dir = latest_probe_run_dir(stage_root, family)
    csv_name = f"{family}_family_probe_stability_sorted.csv"
    csv_path = run_dir / csv_name
    if not csv_path.exists():
        raise FileNotFoundError(f"missing frontier csv: {csv_path}")
    df = pd.read_csv(csv_path)
    param_name = "min_margin" if family == "margin" else "min_probability_diff"
    tested_values = collect_tested_values(family)

    values: list[float] = []
    for value in df[param_name].tolist():
        normalized = round(float(value), 4)
        if normalized in tested_values:
            continue
        if normalized in values:
            continue
        values.append(normalized)
        if len(values) >= n_per_family:
            break
    if len(values) < n_per_family:
        raise ValueError(f"not enough untested {family} frontier values; found only {len(values)}")
    return values


def format_value_token(value: float) -> str:
    return f"{int(round(value * 100000)):05d}"


def build_candidate_specs(stage_root: Path, n_per_family: int) -> list[CandidateSpec]:
    specs: list[CandidateSpec] = []
    margin_values = load_frontier_values(stage_root, "margin", n_per_family)
    diff_values = load_frontier_values(stage_root, "diff", n_per_family)

    for index, value in enumerate(margin_values):
        stage_id = FRONTIER_STAGE_IDS[("margin", index)]
        token = format_value_token(value)
        specs.append(
            CandidateSpec(
                family="margin",
                candidate_role="frontier_validation",
                param_name="min_margin",
                param_value=value,
                run_name=f"{stage_id}_mt5_validation_margin_{token}_0001",
                experiment_id=f"exp_stage05_margin_frontier_{token}_validation_0001",
                stage_id=stage_id,
            )
        )
    for index, value in enumerate(diff_values):
        stage_id = FRONTIER_STAGE_IDS[("diff", index)]
        token = format_value_token(value)
        specs.append(
            CandidateSpec(
                family="diff",
                candidate_role="frontier_validation",
                param_name="min_probability_diff",
                param_value=value,
                run_name=f"{stage_id}_mt5_validation_diff_{token}_0001",
                experiment_id=f"exp_stage05_diff_frontier_{token}_validation_0001",
                stage_id=stage_id,
            )
        )
    return specs


def load_relevant_views(run_names: list[str], split_name: str) -> list[BundleView]:
    views = load_bundle_views(ROOT_DIR / "stages", split_name)
    filtered = [view for view in views if view.run_name in set(run_names)]
    return sort_bundle_views(filtered, "return_pct")


def build_review_payload(views: list[BundleView]) -> dict[str, Any]:
    ranked_runs: list[dict[str, Any]] = []
    for rank, view in enumerate(views, start=1):
        bundle = ExperimentBundle.from_json(view.bundle_path.read_text(encoding="utf-8-sig"))
        param_name, param_value = extract_filter_param(bundle)
        extra = view.execution.get("extra") or {}
        ranked_runs.append(
            {
                "rank": rank,
                "run_name": view.run_name,
                "stage_folder": view.stage_folder,
                "param_name": param_name,
                "param_value": param_value,
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
        "phase": "05E_mt5_frontier_validation_batch",
        "ranked_runs": ranked_runs,
    }


def build_review_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# 05E Stage 05 MT5 Frontier Validation Review",
        "",
        "## Scope",
        "",
        "- purpose: `keep exploring Stage 05 on MT5 validation without reopening holdout yet`",
        "- family-first logic remains in force",
        "- candidate values are the strongest untested entries from the latest Stage 05 family probe stability order",
        "",
        "## Ranking",
        "",
    ]
    for run in payload["ranked_runs"]:
        lines.append(
            f"- [{run['rank']}] `{run['run_name']}`: "
            f"{run['param_name']}={run['param_value']:.4f}, "
            f"return_pct={run['return_pct']:.3f}, "
            f"profit_factor={run['profit_factor']:.4f}, "
            f"max_dd_pct={run['max_dd_pct']:.4f}, "
            f"ulcer_index={run['ulcer_index']:.4f}, "
            f"trades={run['trade_count']}, "
            f"ready_gap={run['ready_row_gap']}, "
            f"unexpected_skips={run['unexpected_skip_count']}"
        )
    lines.extend(
        [
            "",
            "## Read",
            "",
            "- read: `treat this as validation-only frontier expansion; do not use holdout again unless a candidate materially improves the current frontier`",
        ]
    )
    return "\n".join(lines) + "\n"


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


def main() -> int:
    args = build_parser().parse_args()

    stage_root = ROOT_DIR / args.stage_root
    final_run_dir = ROOT_DIR / args.final_run_dir
    active_dir = stage_root / "02_runs" / "active"
    review_dir = stage_root / "03_reviews"
    active_dir.mkdir(parents=True, exist_ok=True)
    review_dir.mkdir(parents=True, exist_ok=True)

    candidate_specs = build_candidate_specs(stage_root, args.n_per_family)
    for spec in candidate_specs:
        run_dir = active_dir / spec.run_name
        run_dir.mkdir(parents=True, exist_ok=True)
        bundle_path = ensure_bundle(
            spec=spec,
            run_dir=run_dir,
            final_run_dir=final_run_dir,
            rebuild_bundle=args.rebuild_bundle,
        )
        run_tester(bundle_path, split_name=args.split_name, enable_trading=True)

    views = load_relevant_views([spec.run_name for spec in candidate_specs], args.split_name)
    review_payload = build_review_payload(views)
    write_json(review_dir / "05E_mt5_frontier_validation_review.json", review_payload)
    write_text(review_dir / "05E_mt5_frontier_validation_review.md", build_review_markdown(review_payload))
    update_review_index(review_dir)

    print(f"[done] review_json={review_dir / '05E_mt5_frontier_validation_review.json'}")
    print(f"[done] review_md={review_dir / '05E_mt5_frontier_validation_review.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
