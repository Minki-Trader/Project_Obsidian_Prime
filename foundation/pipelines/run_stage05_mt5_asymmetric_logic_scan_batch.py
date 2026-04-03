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


@dataclass
class AsymmetricLogicSpec:
    stage_id: str
    run_name: str
    experiment_id: str
    review_basename: str
    mix_label: str
    short_threshold: float
    long_threshold: float
    min_margin: float | None = None
    min_probability_diff: float | None = None


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run asymmetric threshold logic exploration on top of the 05W base.")
    parser.add_argument("--stage-root", default="stages/05_optimization", help="Stage 05 root directory.")
    parser.add_argument(
        "--source-run-dir",
        default="stages/05_optimization/02_runs/active/05W_no_trend_strength_0001",
        help="Existing trained run directory whose model/joblib should be reused.",
    )
    parser.add_argument(
        "--logic-reference-run-name",
        default="05W_no_trend_strength_0001",
        help="Current promoted incumbent used for comparison.",
    )
    parser.add_argument("--rebuild-bundle", action="store_true", help="Force bundle rebuild even if present.")
    parser.add_argument(
        "--skip-holdout",
        action="store_true",
        help="Run validation sweep only and do not open holdout for the top-two asymmetric candidates.",
    )
    return parser


def utc_now_iso() -> str:
    return datetime.now(tz=UTC).isoformat()


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_json(path: Path, payload: dict[str, Any]) -> None:
    write_text(path, json.dumps(payload, indent=2, ensure_ascii=False) + "\n")


def build_specs() -> list[AsymmetricLogicSpec]:
    return [
        AsymmetricLogicSpec(
            stage_id="05BI",
            run_name="05BI_05w_short_bias_margin_0001",
            experiment_id="exp_05bi_05w_short_bias_margin_v1",
            review_basename="05BI_mt5_asymmetric_logic_review",
            mix_label="short_bias_margin",
            short_threshold=0.3000,
            long_threshold=0.4500,
            min_margin=0.0700,
        ),
        AsymmetricLogicSpec(
            stage_id="05BJ",
            run_name="05BJ_05w_short_bias_diff_0001",
            experiment_id="exp_05bj_05w_short_bias_diff_v1",
            review_basename="05BJ_mt5_asymmetric_logic_review",
            mix_label="short_bias_diff",
            short_threshold=0.3000,
            long_threshold=0.4500,
            min_probability_diff=0.0775,
        ),
        AsymmetricLogicSpec(
            stage_id="05BK",
            run_name="05BK_05w_long_bias_margin_0001",
            experiment_id="exp_05bk_05w_long_bias_margin_v1",
            review_basename="05BK_mt5_asymmetric_logic_review",
            mix_label="long_bias_margin",
            short_threshold=0.5750,
            long_threshold=0.3750,
            min_margin=0.0700,
        ),
        AsymmetricLogicSpec(
            stage_id="05BL",
            run_name="05BL_05w_long_bias_diff_0001",
            experiment_id="exp_05bl_05w_long_bias_diff_v1",
            review_basename="05BL_mt5_asymmetric_logic_review",
            mix_label="long_bias_diff",
            short_threshold=0.5750,
            long_threshold=0.3750,
            min_probability_diff=0.0775,
        ),
        AsymmetricLogicSpec(
            stage_id="05BM",
            run_name="05BM_05w_balanced_tight_margin_0001",
            experiment_id="exp_05bm_05w_balanced_tight_margin_v1",
            review_basename="05BM_mt5_asymmetric_logic_review",
            mix_label="balanced_tight_margin",
            short_threshold=0.4500,
            long_threshold=0.4500,
            min_margin=0.0700,
        ),
        AsymmetricLogicSpec(
            stage_id="05BN",
            run_name="05BN_05w_balanced_tight_diff_0001",
            experiment_id="exp_05bn_05w_balanced_tight_diff_v1",
            review_basename="05BN_mt5_asymmetric_logic_review",
            mix_label="balanced_tight_diff",
            short_threshold=0.4500,
            long_threshold=0.4500,
            min_probability_diff=0.0775,
        ),
    ]


def build_rule_stack(spec: AsymmetricLogicSpec) -> dict[str, Any]:
    filters: list[dict[str, Any]] = []
    if spec.min_margin is not None:
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


def ensure_bundle(spec: AsymmetricLogicSpec, run_dir: Path, source_run_dir: Path, rebuild_bundle: bool) -> Path:
    bundle_path = run_dir / "experiment_bundle.json"
    rule_stack_path = run_dir / "rule_stack.json"
    manifest_path = run_dir / "candidate_manifest.json"
    write_json(rule_stack_path, build_rule_stack(spec))
    write_json(
        manifest_path,
        {
            "generated_at_utc": utc_now_iso(),
            "candidate_type": "asymmetric_logic_scan",
            "mix_label": spec.mix_label,
            "run_name": spec.run_name,
            "experiment_id": spec.experiment_id,
            "stage_id": spec.stage_id,
            "short_threshold": spec.short_threshold,
            "long_threshold": spec.long_threshold,
            "min_margin": spec.min_margin,
            "min_probability_diff": spec.min_probability_diff,
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
        max_hold_bars=3,
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


def extract_payload(view: BundleView, spec: AsymmetricLogicSpec | None, label: str) -> dict[str, Any]:
    extra = view.execution.get("extra") or {}
    return {
        "run_name": view.run_name,
        "mix_label": label,
        "short_threshold": None if spec is None else spec.short_threshold,
        "long_threshold": None if spec is None else spec.long_threshold,
        "min_margin": None if spec is None else spec.min_margin,
        "min_probability_diff": None if spec is None else spec.min_probability_diff,
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
        "phase": "05BO_mt5_asymmetric_logic_scan_batch",
        "ranked_validation_runs": [
            {"rank": index + 1, **row}
            for index, row in enumerate(ranked_validation)
        ],
    }
    if ranked_holdout is not None:
        payload["ranked_test_runs"] = [
            {"rank": index + 1, **row}
            for index, row in enumerate(ranked_holdout)
        ]
        validation_winner = ranked_validation[0]["run_name"]
        holdout_winner = ranked_holdout[0]["run_name"]
        if holdout_winner != incumbent_name and validation_winner == holdout_winner:
            payload["verdict"] = {
                "status": "promote_candidate",
                "selected_run_name": holdout_winner,
                "reason": "asymmetric logic candidate led both validation and holdout versus the incumbent",
            }
        elif holdout_winner != incumbent_name:
            payload["verdict"] = {
                "status": "mixed_holdout_win_keep_incumbent",
                "selected_run_name": incumbent_name,
                "reason": "asymmetric logic candidate improved holdout but did not lead validation, so the incumbent stays promoted for now",
            }
        else:
            payload["verdict"] = {
                "status": "reject_keep_incumbent",
                "selected_run_name": incumbent_name,
                "reason": "no asymmetric logic candidate cleared the incumbent on holdout",
            }
    else:
        payload["verdict"] = {
            "status": "validation_only_pending_holdout",
            "selected_run_name": incumbent_name,
            "reason": "holdout not run yet, so the incumbent remains selected",
        }
    return payload


def format_metric(value: Any, digits: int = 4) -> str:
    if value is None:
        return "n/a"
    return f"{float(value):.{digits}f}"


def build_review_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# 05BO Stage 05 Asymmetric Logic Scan Review",
        "",
        f"Generated at: `{payload['generated_at_utc']}`",
        "",
        "## Scope",
        "",
        "- purpose: `widen logic-side exploration with directional threshold asymmetry instead of repeating symmetric copies of the same gate`",
        "- source model lineage: `05W_no_trend_strength_0001`",
        "",
        "## MT5 Validation Ranking",
        "",
    ]
    for row in payload["ranked_validation_runs"]:
        margin_repr = "-" if row["min_margin"] is None else f"{row['min_margin']:.4f}"
        diff_repr = "-" if row["min_probability_diff"] is None else f"{row['min_probability_diff']:.4f}"
        ts_repr = "-" if row["short_threshold"] is None else f"{row['short_threshold']:.4f}"
        tl_repr = "-" if row["long_threshold"] is None else f"{row['long_threshold']:.4f}"
        lines.append(
            f"- [{row['rank']}] `{row['run_name']}`: "
            f"mix=`{row['mix_label']}`, Ts={ts_repr}, Tl={tl_repr}, margin={margin_repr}, diff={diff_repr}, "
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
            ts_repr = "-" if row["short_threshold"] is None else f"{row['short_threshold']:.4f}"
            tl_repr = "-" if row["long_threshold"] is None else f"{row['long_threshold']:.4f}"
            lines.append(
                f"- [{row['rank']}] `{row['run_name']}`: "
                f"mix=`{row['mix_label']}`, Ts={ts_repr}, Tl={tl_repr}, margin={margin_repr}, diff={diff_repr}, "
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
            "- read: `asymmetric threshold scans are meant to test whether the strong short-side holdout behavior can be harvested without sacrificing too much validation durability`",
        ]
    )
    return "\n".join(lines) + "\n"


def update_review_index(review_dir: Path) -> None:
    review_index_path = review_dir / "review_index.md"
    lines = review_index_path.read_text(encoding="utf-8").splitlines() if review_index_path.exists() else []
    entry = "- `05BO`: see `05BO_mt5_asymmetric_logic_scan_review.md`"
    if entry not in lines:
        insert_at = 4 if len(lines) >= 4 else len(lines)
        lines.insert(insert_at, entry)
    write_text(review_index_path, "\n".join(lines).rstrip() + "\n")


def main() -> int:
    args = build_parser().parse_args()

    stage_root = ROOT_DIR / args.stage_root
    source_run_dir = ROOT_DIR / args.source_run_dir
    active_dir = stage_root / "02_runs" / "active"
    review_dir = stage_root / "03_reviews"
    active_dir.mkdir(parents=True, exist_ok=True)
    review_dir.mkdir(parents=True, exist_ok=True)

    specs = build_specs()
    specs_by_run = {spec.run_name: spec for spec in specs}
    for spec in specs:
        run_dir = active_dir / spec.run_name
        run_dir.mkdir(parents=True, exist_ok=True)
        bundle_path = ensure_bundle(spec, run_dir, source_run_dir, args.rebuild_bundle)
        run_tester(bundle_path, split_name="validation")

    validation_views = load_view_map(set(specs_by_run) | {args.logic_reference_run_name}, "validation")
    ranked_validation: list[dict[str, Any]] = []
    for run_name, view in validation_views.items():
        if run_name == args.logic_reference_run_name:
            ranked_validation.append(extract_payload(view, None, "incumbent"))
        else:
            ranked_validation.append(extract_payload(view, specs_by_run[run_name], specs_by_run[run_name].mix_label))

    ranked_holdout: list[dict[str, Any]] | None = None
    if ranked_validation and not args.skip_holdout:
        top_two = [row["run_name"] for row in ranked_validation if row["run_name"] != args.logic_reference_run_name][:2]
        for run_name in top_two:
            run_tester(active_dir / run_name / "experiment_bundle.json", split_name="test")
        holdout_views = load_view_map(set(top_two) | {args.logic_reference_run_name}, "test")
        ranked_holdout = []
        for run_name, view in holdout_views.items():
            if run_name == args.logic_reference_run_name:
                ranked_holdout.append(extract_payload(view, None, "incumbent"))
            else:
                ranked_holdout.append(extract_payload(view, specs_by_run[run_name], specs_by_run[run_name].mix_label))

    review_payload = build_review_payload(
        ranked_validation=ranked_validation,
        ranked_holdout=ranked_holdout,
        incumbent_name=args.logic_reference_run_name,
    )
    review_json_path = review_dir / "05BO_mt5_asymmetric_logic_scan_review.json"
    review_md_path = review_dir / "05BO_mt5_asymmetric_logic_scan_review.md"
    write_json(review_json_path, review_payload)
    write_text(review_md_path, build_review_markdown(review_payload))
    update_review_index(review_dir)

    print(f"[done] review_md={review_md_path}")
    print(f"[done] review_json={review_json_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
