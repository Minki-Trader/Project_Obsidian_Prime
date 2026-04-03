#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
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
from foundation.pipelines.experiment_bundle_models import ExperimentBundle
from foundation.pipelines.run_stage05_logic_family_probe import load_latest_family_summary
from foundation.pipelines.show_experiment_leaderboard import BundleView, load_bundle_views, sort_bundle_views


UTC = timezone.utc
BASELINE_RUN_NAMES = [
    "03E_mt5_validation_baseline_0001",
    "04C_mt5_validation_baseline_0001",
]


@dataclass
class CandidateSpec:
    family: str
    candidate_role: str
    param_name: str
    param_value: float
    run_name: str
    experiment_id: str
    stage_id: str


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run Stage 05 MT5 confirmation on family-first challengers.")
    parser.add_argument(
        "--stage-root",
        default="stages/05_optimization",
        help="Stage 05 root directory.",
    )
    parser.add_argument(
        "--final-run-dir",
        default="stages/01_base_feature_ml/02_runs/active/01D_run_0001_final_h03_band000125_logreg",
        help="Stage 01 final model run directory used for bundle export.",
    )
    parser.add_argument(
        "--split-name",
        default="validation",
        help="Logical split name for MT5 tester results.",
    )
    parser.add_argument(
        "--enable-trading",
        action="store_true",
        default=True,
        help="Enable MT5 market orders during tester confirmation.",
    )
    parser.add_argument(
        "--rebuild-bundle",
        action="store_true",
        help="Force bundle rebuild even if experiment_bundle.json already exists.",
    )
    return parser


def utc_now_iso() -> str:
    return datetime.now(tz=UTC).isoformat()


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_json(path: Path, payload: dict[str, Any]) -> None:
    write_text(path, json.dumps(payload, indent=2, ensure_ascii=False) + "\n")


def build_rule_stack(spec: CandidateSpec) -> dict[str, Any]:
    filter_type = "max_probability_margin" if spec.family == "margin" else "probability_difference"
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
                "type": filter_type,
                "enabled": True,
                "params": {
                    spec.param_name: spec.param_value,
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


def load_candidate_specs(stage_root: Path) -> list[CandidateSpec]:
    margin_summary = load_latest_family_summary(stage_root, "margin")
    diff_summary = load_latest_family_summary(stage_root, "diff")
    if margin_summary is None or diff_summary is None:
        raise FileNotFoundError("Stage 05 family summaries are missing; run the family probe step first")

    margin_gap = margin_summary["tight_gap_leader"]
    diff_gap = diff_summary["tight_gap_leader"]

    return [
        CandidateSpec(
            family="margin",
            candidate_role="tight_gap",
            param_name="min_margin",
            param_value=float(margin_gap["min_margin"]),
            run_name="05C_mt5_validation_margin_tightgap_0001",
            experiment_id="exp_stage05_margin_tightgap_validation_0001",
            stage_id="05C",
        ),
        CandidateSpec(
            family="diff",
            candidate_role="tight_gap",
            param_name="min_probability_diff",
            param_value=float(diff_gap["min_probability_diff"]),
            run_name="05D_mt5_validation_diff_tightgap_0001",
            experiment_id="exp_stage05_diff_tightgap_validation_0001",
            stage_id="05D",
        ),
    ]


def ensure_bundle(
    *,
    spec: CandidateSpec,
    run_dir: Path,
    final_run_dir: Path,
    rebuild_bundle: bool,
) -> Path:
    bundle_path = run_dir / "experiment_bundle.json"
    rule_stack_path = run_dir / "rule_stack.json"
    candidate_manifest_path = run_dir / "candidate_manifest.json"

    write_json(rule_stack_path, build_rule_stack(spec))
    write_json(
        candidate_manifest_path,
        {
            "generated_at_utc": utc_now_iso(),
            "family": spec.family,
            "candidate_role": spec.candidate_role,
            "run_name": spec.run_name,
            "experiment_id": spec.experiment_id,
            "stage_id": spec.stage_id,
            "param_name": spec.param_name,
            "param_value": spec.param_value,
            "source_final_run_dir": str(final_run_dir),
        },
    )

    if bundle_path.exists() and not rebuild_bundle:
        return bundle_path

    export_args = argparse.Namespace(
        run_dir=str(final_run_dir),
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
        max_hold_bars=3,
        build_bundle=True,
    )
    run_export_bundle_assets(export_args)
    return bundle_path


def run_tester(bundle_path: Path, *, split_name: str, enable_trading: bool) -> None:
    cmd = [
        sys.executable,
        str(ROOT_DIR / "foundation" / "pipelines" / "run_mt5_bundle_tester.py"),
        "--bundle-json",
        str(bundle_path),
        "--split-name",
        split_name,
    ]
    if enable_trading:
        cmd.append("--enable-trading")
    subprocess.run(cmd, cwd=ROOT_DIR, check=True)


def extract_filter_param(bundle: ExperimentBundle) -> tuple[str, float | None]:
    for rule in bundle.rule_stack.filters:
        if not rule.enabled:
            continue
        if rule.type == "max_probability_margin":
            return ("min_margin", float(rule.params.get("min_margin", 0.0)))
        if rule.type == "probability_difference":
            return ("min_probability_diff", float(rule.params.get("min_probability_diff", 0.0)))
    return ("-", None)


def load_relevant_views(stage_root: Path, split_name: str, extra_run_names: list[str]) -> list[BundleView]:
    bundle_views = load_bundle_views(ROOT_DIR / "stages", split_name)
    keep_names = set(BASELINE_RUN_NAMES) | set(extra_run_names)
    filtered = [view for view in bundle_views if view.run_name in keep_names]
    return sort_bundle_views(filtered, "return_pct")


def build_review_payload(views: list[BundleView]) -> dict[str, Any]:
    runs: list[dict[str, Any]] = []
    for rank, view in enumerate(views, start=1):
        bundle = ExperimentBundle.from_json(view.bundle_path.read_text(encoding="utf-8"))
        param_name, param_value = extract_filter_param(bundle)
        extra = view.execution.get("extra") or {}
        runs.append(
            {
                "rank": rank,
                "stage_folder": view.stage_folder,
                "run_name": view.run_name,
                "bundle_path": str(view.bundle_path),
                "family_param_name": param_name,
                "family_param_value": param_value,
                "return_pct": view.headline.get("return_pct"),
                "profit_factor": view.headline.get("profit_factor"),
                "trade_count": view.headline.get("trade_count"),
                "max_dd_pct": view.headline.get("max_dd_pct"),
                "ulcer_index": view.risk.get("ulcer_index"),
                "latest_attempt_id": view.latest_attempt_id,
                "ready_row_count": extra.get("ready_row_count"),
                "expected_ready_row_count": extra.get("expected_ready_row_count"),
                "ready_row_gap": extra.get("ready_row_gap"),
                "unexpected_skip_count": extra.get("unexpected_skip_count"),
            }
        )
    return {
        "generated_at_utc": utc_now_iso(),
        "phase": "05C_mt5_family_confirmation_batch",
        "baseline_run_names": BASELINE_RUN_NAMES,
        "ranked_runs": runs,
    }


def build_review_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# 05C Stage 05 MT5 Family Confirmation Review",
        "",
        f"Generated at: `{payload['generated_at_utc']}`",
        "",
        "## Scope",
        "",
        "- purpose: `promote the Stage 05 tight-gap challengers into MT5 validation without forcing rule synthesis`",
        "- existing MT5 leaders from Stage 03 and Stage 04 are used as baselines",
        "- only the new Stage 05 tight-gap challengers are freshly executed here",
        "",
        "## Ranking",
        "",
    ]
    for run in payload["ranked_runs"]:
        param_repr = (
            f"{run['family_param_name']}={run['family_param_value']:.4f}"
            if isinstance(run["family_param_value"], (float, int))
            else "-"
        )
        lines.append(
            f"- [{run['rank']}] `{run['run_name']}`: "
            f"{param_repr}, return_pct={run['return_pct']:.3f}, "
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
            "- read: `use this review to decide whether the original MT5 leader still stands or whether a tighter-gap challenger deserves holdout promotion`",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    args = build_parser().parse_args()

    stage_root = ROOT_DIR / args.stage_root
    final_run_dir = ROOT_DIR / args.final_run_dir
    review_dir = stage_root / "03_reviews"
    active_dir = stage_root / "02_runs" / "active"
    review_dir.mkdir(parents=True, exist_ok=True)
    active_dir.mkdir(parents=True, exist_ok=True)

    candidate_specs = load_candidate_specs(stage_root)
    executed_run_names: list[str] = []
    for spec in candidate_specs:
        run_dir = active_dir / spec.run_name
        run_dir.mkdir(parents=True, exist_ok=True)
        bundle_path = ensure_bundle(
            spec=spec,
            run_dir=run_dir,
            final_run_dir=final_run_dir,
            rebuild_bundle=args.rebuild_bundle,
        )
        run_tester(bundle_path, split_name=args.split_name, enable_trading=args.enable_trading)
        executed_run_names.append(spec.run_name)

    review_payload = build_review_payload(load_relevant_views(stage_root, args.split_name, executed_run_names))
    review_json_path = review_dir / "05C_mt5_family_confirmation_review.json"
    review_md_path = review_dir / "05C_mt5_family_confirmation_review.md"
    write_json(review_json_path, review_payload)
    write_text(review_md_path, build_review_markdown(review_payload))

    print(f"[done] review_json={review_json_path}")
    print(f"[done] review_md={review_md_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
