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
from foundation.pipelines.show_experiment_leaderboard import BundleView, load_bundle_views, sort_bundle_views


UTC = timezone.utc
REFERENCE_RUN_NAMES = [
    "05DP_05ca_margin0675_hold5_0001",
    "05EM_05dp_short_bias_margin_hold5_0001",
    "05EA_05ca_margin0675_hold4_0001",
    "05DL_05cc_margin_hold5_0001",
]
REFERENCE_LABELS = {
    "05DP_05ca_margin0675_hold5_0001": "promoted_05dp",
    "05EM_05dp_short_bias_margin_hold5_0001": "short_bias_ref_05em",
    "05EA_05ca_margin0675_hold4_0001": "hold4_ref_05ea",
    "05DL_05cc_margin_hold5_0001": "risk_alt_05dl",
}


@dataclass
class PlateauResponseSpec:
    stage_id: str
    run_name: str
    experiment_id: str
    review_basename: str
    mix_label: str
    short_threshold: float
    long_threshold: float
    max_hold_bars: int
    min_margin: float | None = None
    min_probability_diff: float | None = None


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run plateau-response logic exploration on top of promoted 05DP.")
    parser.add_argument("--stage-root", default="stages/05_optimization", help="Stage 05 root directory.")
    parser.add_argument(
        "--source-run-dir",
        default="stages/05_optimization/02_runs/active/05DP_05ca_margin0675_hold5_0001",
        help="Existing trained run directory whose model/joblib should be reused.",
    )
    parser.add_argument(
        "--logic-reference-run-name",
        default="05DP_05ca_margin0675_hold5_0001",
        help="Current promoted incumbent used for comparison.",
    )
    parser.add_argument("--rebuild-bundle", action="store_true", help="Force bundle rebuild even if present.")
    parser.add_argument(
        "--skip-holdout",
        action="store_true",
        help="Run validation sweep only and do not open holdout for the top-two new plateau-response candidates.",
    )
    return parser


def utc_now_iso() -> str:
    return datetime.now(tz=UTC).isoformat()


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_json(path: Path, payload: dict[str, Any]) -> None:
    write_text(path, json.dumps(payload, indent=2, ensure_ascii=False) + "\n")


def build_specs() -> list[PlateauResponseSpec]:
    return [
        PlateauResponseSpec(
            stage_id="05ER",
            run_name="05ER_05dp_short_bias_margin_hold4_0001",
            experiment_id="exp_05er_05dp_short_bias_margin_hold4_v1",
            review_basename="05ER_mt5_plateau_response_review",
            mix_label="short_bias_margin_hold4",
            short_threshold=0.3000,
            long_threshold=0.4500,
            min_margin=0.0675,
            max_hold_bars=4,
        ),
        PlateauResponseSpec(
            stage_id="05ES",
            run_name="05ES_05dp_stronger_long_suppression_hold5_0001",
            experiment_id="exp_05es_05dp_stronger_long_suppression_hold5_v1",
            review_basename="05ES_mt5_plateau_response_review",
            mix_label="short_bias_margin_long050_hold5",
            short_threshold=0.3000,
            long_threshold=0.5000,
            min_margin=0.0675,
            max_hold_bars=5,
        ),
        PlateauResponseSpec(
            stage_id="05ET",
            run_name="05ET_05dp_stronger_long_suppression_hold4_0001",
            experiment_id="exp_05et_05dp_stronger_long_suppression_hold4_v1",
            review_basename="05ET_mt5_plateau_response_review",
            mix_label="short_bias_margin_long050_hold4",
            short_threshold=0.3000,
            long_threshold=0.5000,
            min_margin=0.0675,
            max_hold_bars=4,
        ),
        PlateauResponseSpec(
            stage_id="05EU",
            run_name="05EU_05dp_near_short_only_hold5_0001",
            experiment_id="exp_05eu_05dp_near_short_only_hold5_v1",
            review_basename="05EU_mt5_plateau_response_review",
            mix_label="near_short_only_margin_hold5",
            short_threshold=0.3000,
            long_threshold=0.6000,
            min_margin=0.0675,
            max_hold_bars=5,
        ),
        PlateauResponseSpec(
            stage_id="05EV",
            run_name="05EV_05dp_short_bias_combo_hold4_0001",
            experiment_id="exp_05ev_05dp_short_bias_combo_hold4_v1",
            review_basename="05EV_mt5_plateau_response_review",
            mix_label="short_bias_combo_hold4",
            short_threshold=0.3000,
            long_threshold=0.4500,
            min_margin=0.0500,
            min_probability_diff=0.0700,
            max_hold_bars=4,
        ),
        PlateauResponseSpec(
            stage_id="05EW",
            run_name="05EW_05dp_balanced_tight_combo_hold5_0001",
            experiment_id="exp_05ew_05dp_balanced_tight_combo_hold5_v1",
            review_basename="05EW_mt5_plateau_response_review",
            mix_label="balanced_tight_combo_hold5",
            short_threshold=0.4500,
            long_threshold=0.4500,
            min_margin=0.0500,
            min_probability_diff=0.0700,
            max_hold_bars=5,
        ),
    ]


def build_rule_stack(spec: PlateauResponseSpec) -> dict[str, Any]:
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
                "params": {"max_hold_bars": spec.max_hold_bars},
            }
        ],
    }


def ensure_bundle(spec: PlateauResponseSpec, run_dir: Path, source_run_dir: Path, rebuild_bundle: bool) -> Path:
    bundle_path = run_dir / "experiment_bundle.json"
    rule_stack_path = run_dir / "rule_stack.json"
    manifest_path = run_dir / "candidate_manifest.json"
    write_json(rule_stack_path, build_rule_stack(spec))
    write_json(
        manifest_path,
        {
            "generated_at_utc": utc_now_iso(),
            "candidate_type": "05dp_plateau_response",
            "mix_label": spec.mix_label,
            "run_name": spec.run_name,
            "experiment_id": spec.experiment_id,
            "stage_id": spec.stage_id,
            "short_threshold": spec.short_threshold,
            "long_threshold": spec.long_threshold,
            "min_margin": spec.min_margin,
            "min_probability_diff": spec.min_probability_diff,
            "max_hold_bars": spec.max_hold_bars,
            "source_run_dir": str(source_run_dir),
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
        max_hold_bars=spec.max_hold_bars,
        build_bundle=True,
    )
    run_export_bundle_assets(export_args)
    return bundle_path


def run_tester(bundle_path: Path, *, split_name: str) -> None:
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


def load_view_map(run_names: set[str], split_name: str) -> dict[str, BundleView]:
    views = load_bundle_views(ROOT_DIR / "stages", split_name)
    filtered = [view for view in views if view.run_name in run_names]
    return {view.run_name: view for view in sort_bundle_views(filtered, "return_pct")}


def extract_payload(view: BundleView, spec: PlateauResponseSpec | None, label: str) -> dict[str, Any]:
    extra = view.execution.get("extra") or {}
    return {
        "run_name": view.run_name,
        "mix_label": label,
        "short_threshold": None if spec is None else spec.short_threshold,
        "long_threshold": None if spec is None else spec.long_threshold,
        "min_margin": None if spec is None else spec.min_margin,
        "min_probability_diff": None if spec is None else spec.min_probability_diff,
        "max_hold_bars": None if spec is None else spec.max_hold_bars,
        "return_pct": view.headline.get("return_pct"),
        "profit_factor": view.headline.get("profit_factor"),
        "trade_count": view.headline.get("trade_count"),
        "max_dd_pct": view.headline.get("max_dd_pct"),
        "ulcer_index": view.risk.get("ulcer_index"),
        "ready_row_gap": extra.get("ready_row_gap"),
        "unexpected_skip_count": extra.get("unexpected_skip_count"),
    }


def build_review_payload(
    *,
    ranked_validation: list[dict[str, Any]],
    ranked_holdout: list[dict[str, Any]] | None,
    incumbent_name: str,
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "generated_at_utc": utc_now_iso(),
        "phase": "05EX_mt5_05dp_plateau_response_batch",
        "ranked_validation_runs": [{"rank": index + 1, **row} for index, row in enumerate(ranked_validation)],
    }
    if ranked_holdout is not None:
        payload["ranked_test_runs"] = [{"rank": index + 1, **row} for index, row in enumerate(ranked_holdout)]
        holdout_winner = ranked_holdout[0]["run_name"]
        validation_winner = ranked_validation[0]["run_name"]
        if holdout_winner not in REFERENCE_RUN_NAMES and validation_winner == holdout_winner:
            payload["verdict"] = {
                "status": "promote_candidate",
                "selected_run_name": holdout_winner,
                "reason": "plateau-response candidate led both validation and holdout versus promoted 05DP",
            }
        elif holdout_winner not in REFERENCE_RUN_NAMES:
            payload["verdict"] = {
                "status": "mixed_holdout_win_keep_incumbent",
                "selected_run_name": incumbent_name,
                "reason": "plateau-response candidate improved holdout but did not lead validation, so 05DP remains promoted",
            }
        else:
            payload["verdict"] = {
                "status": "reject_keep_incumbent",
                "selected_run_name": incumbent_name,
                "reason": "no plateau-response candidate cleared 05DP on holdout",
            }
    else:
        payload["verdict"] = {
            "status": "validation_only_pending_holdout",
            "selected_run_name": incumbent_name,
            "reason": "holdout not run yet, so 05DP remains selected",
        }
    return payload


def format_metric(value: Any, digits: int = 4) -> str:
    if value is None:
        return "n/a"
    return f"{float(value):.{digits}f}"


def build_review_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# 05EX Stage 05 05DP Plateau Response Review",
        "",
        f"Generated at: `{payload['generated_at_utc']}`",
        "",
        "## Scope",
        "",
        "- purpose: `target the observed plateau behavior directly by suppressing longs, shortening hold, and adding light flat-regime avoidance while keeping the 05DP feature/model bundle fixed`",
        "- promoted incumbent: `05DP`",
        "",
        "## MT5 Validation Ranking",
        "",
    ]
    for row in payload["ranked_validation_runs"]:
        margin_repr = "-" if row["min_margin"] is None else f"{row['min_margin']:.4f}"
        diff_repr = "-" if row["min_probability_diff"] is None else f"{row['min_probability_diff']:.4f}"
        short_repr = "-" if row["short_threshold"] is None else f"{row['short_threshold']:.4f}"
        long_repr = "-" if row["long_threshold"] is None else f"{row['long_threshold']:.4f}"
        hold_repr = "-" if row["max_hold_bars"] is None else str(int(row["max_hold_bars"]))
        lines.append(
            f"- [{row['rank']}] `{row['run_name']}`: "
            f"mix=`{row['mix_label']}`, short_thr={short_repr}, long_thr={long_repr}, hold={hold_repr}, margin={margin_repr}, diff={diff_repr}, "
            f"return_pct={format_metric(row['return_pct'], 3)}, profit_factor={format_metric(row['profit_factor'], 4)}, "
            f"max_dd_pct={format_metric(row['max_dd_pct'], 4)}, ulcer_index={format_metric(row['ulcer_index'], 4)}, "
            f"trades={row['trade_count']}, ready_gap={row['ready_row_gap']}, unexpected_skips={row['unexpected_skip_count']}"
        )
    ranked_test_runs = payload.get("ranked_test_runs")
    if ranked_test_runs:
        lines.extend(["", "## MT5 Holdout Ranking", ""])
        for row in ranked_test_runs:
            margin_repr = "-" if row["min_margin"] is None else f"{row['min_margin']:.4f}"
            diff_repr = "-" if row["min_probability_diff"] is None else f"{row['min_probability_diff']:.4f}"
            short_repr = "-" if row["short_threshold"] is None else f"{row['short_threshold']:.4f}"
            long_repr = "-" if row["long_threshold"] is None else f"{row['long_threshold']:.4f}"
            hold_repr = "-" if row["max_hold_bars"] is None else str(int(row["max_hold_bars"]))
            lines.append(
                f"- [{row['rank']}] `{row['run_name']}`: "
                f"mix=`{row['mix_label']}`, short_thr={short_repr}, long_thr={long_repr}, hold={hold_repr}, margin={margin_repr}, diff={diff_repr}, "
                f"return_pct={format_metric(row['return_pct'], 3)}, profit_factor={format_metric(row['profit_factor'], 4)}, "
                f"max_dd_pct={format_metric(row['max_dd_pct'], 4)}, ulcer_index={format_metric(row['ulcer_index'], 4)}, "
                f"trades={row['trade_count']}, ready_gap={row['ready_row_gap']}, unexpected_skips={row['unexpected_skip_count']}"
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
            "## Read",
            "",
            "- read: `this batch asks whether the plateau is mainly a long-side drag problem, a hold-length problem, or a flat-regime gating problem`",
        ]
    )
    return "\n".join(lines) + "\n"


def update_review_index(review_dir: Path) -> None:
    review_index_path = review_dir / "review_index.md"
    lines = review_index_path.read_text(encoding="utf-8").splitlines() if review_index_path.exists() else []
    entry = "- `05EX`: see `05EX_mt5_05dp_plateau_response_review.md`"
    if entry not in lines:
        insert_at = 4 if len(lines) >= 4 else len(lines)
        lines.insert(insert_at, entry)
    write_text(review_index_path, "\n".join(lines).rstrip() + "\n")


def main() -> int:
    args = build_parser().parse_args()

    source_run_dir = (ROOT_DIR / args.source_run_dir).resolve()
    if not source_run_dir.exists():
        raise FileNotFoundError(f"source run dir not found: {source_run_dir}")

    review_dir = ROOT_DIR / args.stage_root / "03_reviews"
    run_root = ROOT_DIR / args.stage_root / "02_runs" / "active"
    review_dir.mkdir(parents=True, exist_ok=True)
    run_root.mkdir(parents=True, exist_ok=True)

    specs = build_specs()
    specs_by_run = {spec.run_name: spec for spec in specs}
    for spec in specs:
        run_dir = run_root / spec.run_name
        bundle_path = ensure_bundle(spec, run_dir, source_run_dir, args.rebuild_bundle)
        run_tester(bundle_path, split_name="validation")

    validation_views = load_view_map(set(specs_by_run) | set(REFERENCE_RUN_NAMES), "validation")
    ranked_validation: list[dict[str, Any]] = []
    for run_name, view in validation_views.items():
        if run_name in specs_by_run:
            ranked_validation.append(extract_payload(view, specs_by_run[run_name], specs_by_run[run_name].mix_label))
        else:
            ranked_validation.append(extract_payload(view, None, REFERENCE_LABELS[run_name]))

    ranked_holdout: list[dict[str, Any]] | None = None
    if ranked_validation and not args.skip_holdout:
        top_two = [row["run_name"] for row in ranked_validation if row["run_name"] not in REFERENCE_RUN_NAMES][:2]
        for run_name in top_two:
            run_dir = run_root / run_name
            bundle_path = run_dir / "experiment_bundle.json"
            run_tester(bundle_path, split_name="test")
        holdout_views = load_view_map(set(top_two) | set(REFERENCE_RUN_NAMES), "test")
        ranked_holdout = []
        for run_name, view in holdout_views.items():
            if run_name in specs_by_run:
                ranked_holdout.append(extract_payload(view, specs_by_run[run_name], specs_by_run[run_name].mix_label))
            else:
                ranked_holdout.append(extract_payload(view, None, REFERENCE_LABELS[run_name]))

    review_payload = build_review_payload(
        ranked_validation=ranked_validation,
        ranked_holdout=ranked_holdout,
        incumbent_name=args.logic_reference_run_name,
    )
    review_json_path = review_dir / "05EX_mt5_05dp_plateau_response_review.json"
    review_md_path = review_dir / "05EX_mt5_05dp_plateau_response_review.md"
    write_json(review_json_path, review_payload)
    write_text(review_md_path, build_review_markdown(review_payload))
    update_review_index(review_dir)

    print(f"[done] review_md={review_md_path}")
    print(f"[done] review_json={review_json_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
