#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from foundation.pipelines.export_experiment_bundle_assets import run_export_bundle_assets
from foundation.pipelines.run_stage05_mt5_confirmation_batch import run_tester
from foundation.pipelines.show_experiment_leaderboard import BundleView, load_bundle_views, sort_bundle_views


UTC = timezone.utc


@dataclass
class LogicMixSpec:
    stage_id: str
    run_name: str
    experiment_id: str
    mix_label: str
    short_threshold: float
    long_threshold: float
    min_margin: float | None = None
    min_probability_diff: float | None = None


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run Stage 05 MT5 validation for broad logic-mix candidates.")
    parser.add_argument("--stage-root", default="stages/05_optimization", help="Stage 05 root directory.")
    parser.add_argument(
        "--final-run-dir",
        default="stages/01_base_feature_ml/02_runs/active/01D_run_0001_final_h03_band000125_logreg",
        help="Stage 01 final model run directory used for bundle export.",
    )
    parser.add_argument("--split-name", default="validation", help="Logical split name for MT5 tester results.")
    parser.add_argument("--rebuild-bundle", action="store_true", help="Force bundle rebuild even if present.")
    return parser


def utc_now_iso() -> str:
    return datetime.now(tz=UTC).isoformat()


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_json(path: Path, payload: dict[str, Any]) -> None:
    write_text(path, json.dumps(payload, indent=2, ensure_ascii=False) + "\n")


def build_candidate_specs() -> list[LogicMixSpec]:
    return [
        LogicMixSpec(
            stage_id="05N",
            run_name="05N_thr_margin_mix_0001",
            experiment_id="exp_05N_thr_margin_mix_v1",
            mix_label="threshold_margin_mix",
            short_threshold=0.535,
            long_threshold=0.400,
            min_margin=0.0700,
        ),
        LogicMixSpec(
            stage_id="05O",
            run_name="05O_thr_diff_mix_0001",
            experiment_id="exp_05O_thr_diff_mix_v1",
            mix_label="threshold_diff_mix",
            short_threshold=0.535,
            long_threshold=0.400,
            min_probability_diff=0.0775,
        ),
        LogicMixSpec(
            stage_id="05P",
            run_name="05P_margin_diff_mix_0001",
            experiment_id="exp_05P_margin_diff_mix_v1",
            mix_label="margin_diff_mix",
            short_threshold=1.0 / 3.0,
            long_threshold=1.0 / 3.0,
            min_margin=0.0700,
            min_probability_diff=0.0775,
        ),
        LogicMixSpec(
            stage_id="05Q",
            run_name="05Q_thr_margin_diff_0001",
            experiment_id="exp_05Q_thr_margin_diff_v1",
            mix_label="threshold_margin_diff_mix",
            short_threshold=0.535,
            long_threshold=0.400,
            min_margin=0.0700,
            min_probability_diff=0.0775,
        ),
    ]


def build_rule_stack(spec: LogicMixSpec) -> dict[str, Any]:
    filters: list[dict[str, Any]] = []
    if spec.min_margin is not None and spec.min_probability_diff is not None:
        filters.append(
            {
                "rule_id": "filter_01",
                "type": "combo_probability_gate",
                "enabled": True,
                "params": {
                    "min_margin": spec.min_margin,
                    "min_probability_diff": spec.min_probability_diff,
                },
            }
        )
    elif spec.min_margin is not None:
        filters.append(
            {
                "rule_id": "filter_01",
                "type": "max_probability_margin",
                "enabled": True,
                "params": {"min_margin": spec.min_margin},
            }
        )
    elif spec.min_probability_diff is not None:
        filters.append(
            {
                "rule_id": "filter_01",
                "type": "probability_difference",
                "enabled": True,
                "params": {"min_probability_diff": spec.min_probability_diff},
            }
        )

    return {
        "entry": [
            {
                "rule_id": "entry_01",
                "type": "threshold_entry",
                "enabled": True,
                "params": {
                    "short_threshold": spec.short_threshold,
                    "long_threshold": spec.long_threshold,
                },
            }
        ],
        "filters": filters,
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
                "params": {"max_hold_bars": 3},
            }
        ],
    }


def ensure_bundle(*, spec: LogicMixSpec, run_dir: Path, final_run_dir: Path, rebuild_bundle: bool) -> Path:
    bundle_path = run_dir / "experiment_bundle.json"
    rule_stack_path = run_dir / "rule_stack.json"
    candidate_manifest_path = run_dir / "candidate_manifest.json"

    write_json(rule_stack_path, build_rule_stack(spec))
    write_json(
        candidate_manifest_path,
        {
            "generated_at_utc": utc_now_iso(),
            "candidate_type": "logic_mix",
            "mix_label": spec.mix_label,
            "run_name": spec.run_name,
            "experiment_id": spec.experiment_id,
            "stage_id": spec.stage_id,
            "short_threshold": spec.short_threshold,
            "long_threshold": spec.long_threshold,
            "min_margin": spec.min_margin,
            "min_probability_diff": spec.min_probability_diff,
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


def load_relevant_views(run_names: list[str], split_name: str) -> list[BundleView]:
    views = load_bundle_views(ROOT_DIR / "stages", split_name)
    filtered = [view for view in views if view.run_name in set(run_names)]
    return sort_bundle_views(filtered, "return_pct")


def build_review_payload(views: list[BundleView], specs: dict[str, LogicMixSpec]) -> dict[str, Any]:
    ranked_runs: list[dict[str, Any]] = []
    for rank, view in enumerate(views, start=1):
        spec = specs[view.run_name]
        extra = view.execution.get("extra") or {}
        ranked_runs.append(
            {
                "rank": rank,
                "run_name": view.run_name,
                "stage_folder": view.stage_folder,
                "mix_label": spec.mix_label,
                "short_threshold": spec.short_threshold,
                "long_threshold": spec.long_threshold,
                "min_margin": spec.min_margin,
                "min_probability_diff": spec.min_probability_diff,
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
        "generated_at_utc": utc_now_iso(),
        "phase": "05N_mt5_logic_mix_validation_batch",
        "ranked_runs": ranked_runs,
    }


def build_review_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# 05N Stage 05 MT5 Logic Mix Validation Review",
        "",
        f"Generated at: `{payload['generated_at_utc']}`",
        "",
        "## Scope",
        "",
        "- purpose: `scan broad Stage 05 logic mixes before narrowing the search again`",
        "- baseline model lineage remains the Stage 01 final logistic bundle",
        "- mixes combine tuned thresholds, tuned margin, and tuned probability-diff gates without forcing promotion yet",
        "",
        "## Ranking",
        "",
    ]
    for run in payload["ranked_runs"]:
        margin_repr = "-" if run["min_margin"] is None else f"{run['min_margin']:.4f}"
        diff_repr = "-" if run["min_probability_diff"] is None else f"{run['min_probability_diff']:.4f}"
        lines.append(
            f"- [{run['rank']}] `{run['run_name']}`: "
            f"mix={run['mix_label']}, "
            f"Ts={run['short_threshold']:.4f}, Tl={run['long_threshold']:.4f}, "
            f"margin={margin_repr}, diff={diff_repr}, "
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
            "- read: `use this as breadth-first validation scanning; only open holdout for a mix candidate if it looks materially stronger than the current same-model frontier`",
        ]
    )
    return "\n".join(lines) + "\n"


def update_review_index(review_dir: Path) -> None:
    review_index_path = review_dir / "review_index.md"
    lines = review_index_path.read_text(encoding="utf-8").splitlines() if review_index_path.exists() else []
    entry = "- `05N`: see `05N_mt5_logic_mix_validation_review.md`"
    if entry not in lines:
        insert_at = 8 if len(lines) >= 8 else len(lines)
        lines.insert(insert_at, entry)
    write_text(review_index_path, "\n".join(lines).rstrip() + "\n")


def main() -> int:
    args = build_parser().parse_args()

    stage_root = ROOT_DIR / args.stage_root
    final_run_dir = ROOT_DIR / args.final_run_dir
    active_dir = stage_root / "02_runs" / "active"
    review_dir = stage_root / "03_reviews"
    active_dir.mkdir(parents=True, exist_ok=True)
    review_dir.mkdir(parents=True, exist_ok=True)

    candidate_specs = build_candidate_specs()
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
    specs_by_run = {spec.run_name: spec for spec in candidate_specs}
    review_payload = build_review_payload(views, specs_by_run)
    review_json_path = review_dir / "05N_mt5_logic_mix_validation_review.json"
    review_md_path = review_dir / "05N_mt5_logic_mix_validation_review.md"
    write_json(review_json_path, review_payload)
    write_text(review_md_path, build_review_markdown(review_payload))
    update_review_index(review_dir)

    print(f"[done] review_json={review_json_path}")
    print(f"[done] review_md={review_md_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
