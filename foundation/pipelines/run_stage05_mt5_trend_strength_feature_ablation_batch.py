#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from foundation.pipelines.experiment_bundle_models import ExperimentBundle
from foundation.pipelines.show_experiment_leaderboard import BundleView, load_bundle_views, sort_bundle_views


UTC = timezone.utc
FEATURE_SPECS = [
    ("05AC", "adx_14", "05AC_drop_adx14_0001", "05AC_mt5_model_family_trial_review"),
    ("05AD", "di_spread_14", "05AD_drop_di_spread14_0001", "05AD_mt5_model_family_trial_review"),
    ("05AE", "supertrend_10_3", "05AE_drop_supertrend103_0001", "05AE_mt5_model_family_trial_review"),
    ("05AF", "vortex_indicator", "05AF_drop_vortex_indicator_0001", "05AF_mt5_model_family_trial_review"),
]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run Stage 05 MT5 single-feature ablations inside the trend_strength sector.")
    parser.add_argument("--stage-root", default="stages/05_optimization", help="Stage 05 root directory.")
    parser.add_argument(
        "--logic-reference-run-name",
        default="05W_no_trend_strength_0001",
        help="Current promoted incumbent used as the holdout comparison baseline.",
    )
    parser.add_argument("--min-margin", type=float, default=0.07, help="Margin filter value copied from the current incumbent logic.")
    parser.add_argument(
        "--holdout-feature",
        default="",
        help="Optional explicit feature name to open on holdout after validation ranking. Defaults to validation leader.",
    )
    parser.add_argument("--rebuild-bundle", action="store_true", help="Force bundle rebuild when rerunning.")
    parser.add_argument(
        "--skip-holdout",
        action="store_true",
        help="Run validation sweep only and do not open holdout for the top single-feature candidate.",
    )
    return parser


def utc_now_iso() -> str:
    return datetime.now(tz=UTC).isoformat()


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_json(path: Path, payload: dict[str, Any]) -> None:
    write_text(path, json.dumps(payload, indent=2, ensure_ascii=False) + "\n")


def feature_spec_map() -> dict[str, tuple[str, str, str]]:
    return {feature: (stage_id, run_name, review_basename) for stage_id, feature, run_name, review_basename in FEATURE_SPECS}


def run_trial(*, feature_name: str, stage_id: str, run_name: str, review_basename: str, run_holdout: bool, args: argparse.Namespace) -> None:
    experiment_id = f"exp_{stage_id.lower()}_{feature_name}_feature_ablation_v1"
    cmd = [
        sys.executable,
        str(ROOT_DIR / "foundation" / "pipelines" / "run_stage05_mt5_model_family_trial.py"),
        "--model-family",
        "logistic_regression",
        "--run-name",
        run_name,
        "--experiment-id",
        experiment_id,
        "--stage-id",
        stage_id,
        "--review-basename",
        review_basename,
        "--logic-reference-run-name",
        args.logic_reference_run_name,
        "--min-margin",
        f"{args.min_margin:.4f}",
        "--drop-features",
        feature_name,
    ]
    if args.rebuild_bundle:
        cmd.append("--rebuild-bundle")
    if run_holdout:
        cmd.append("--run-holdout")
    subprocess.run(cmd, cwd=ROOT_DIR, check=True)


def load_view_map(run_names: set[str], split_name: str) -> dict[str, BundleView]:
    views = load_bundle_views(ROOT_DIR / "stages", split_name)
    filtered = [view for view in views if view.run_name in run_names]
    return {view.run_name: view for view in sort_bundle_views(filtered, "return_pct")}


def extract_payload(view: BundleView, feature_name: str) -> dict[str, Any]:
    extra = view.execution.get("extra") or {}
    bundle = ExperimentBundle.from_json(view.bundle_path.read_text(encoding="utf-8-sig"))
    config_artifacts = [artifact for artifact in bundle.artifacts if artifact.role == "run_config"]
    config_payload: dict[str, Any] = {}
    if config_artifacts:
        config_path = view.bundle_path.parent / config_artifacts[0].path
        if config_path.exists():
            config_payload = json.loads(config_path.read_text(encoding="utf-8"))
    metrics_path = view.bundle_path.parent / "metrics.json"
    metrics_payload: dict[str, Any] = {}
    if metrics_path.exists():
        metrics_payload = json.loads(metrics_path.read_text(encoding="utf-8"))

    return {
        "stage_folder": view.stage_folder,
        "run_name": view.run_name,
        "feature_name": feature_name,
        "remaining_feature_count": len(config_payload.get("active_input_features", [])),
        "offline_test_macro_f1": metrics_payload.get("test_macro_f1"),
        "return_pct": view.headline.get("return_pct"),
        "profit_factor": view.headline.get("profit_factor"),
        "trade_count": view.headline.get("trade_count"),
        "max_dd_pct": view.headline.get("max_dd_pct"),
        "ulcer_index": view.risk.get("ulcer_index"),
        "ready_row_gap": extra.get("ready_row_gap"),
        "unexpected_skip_count": extra.get("unexpected_skip_count"),
        "bundle_path": str(view.bundle_path),
    }


def resolve_holdout_feature(args: argparse.Namespace, ranked_validation: list[dict[str, Any]]) -> str:
    if args.holdout_feature:
        if args.holdout_feature not in feature_spec_map():
            raise ValueError(f"unknown holdout feature: {args.holdout_feature}")
        return args.holdout_feature
    return ranked_validation[0]["feature_name"]


def build_review_payload(
    *,
    ranked_validation: list[dict[str, Any]],
    holdout_result: dict[str, Any] | None,
    incumbent_holdout: dict[str, Any] | None,
    logic_reference_run_name: str,
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "generated_at_utc": utc_now_iso(),
        "phase": "05AG_mt5_trend_strength_feature_ablation_batch",
        "logic_reference_run_name": logic_reference_run_name,
        "ranked_validation_runs": [
            {"rank": index + 1, **row}
            for index, row in enumerate(ranked_validation)
        ],
    }
    if holdout_result is not None and incumbent_holdout is not None:
        ranked_test = [holdout_result, incumbent_holdout]
        ranked_test.sort(key=lambda item: (item["return_pct"] is not None, item["return_pct"]), reverse=True)
        payload["ranked_test_runs"] = [
            {"rank": index + 1, **row}
            for index, row in enumerate(ranked_test)
        ]
        incumbent_wins = (
            incumbent_holdout["return_pct"] > holdout_result["return_pct"]
            or incumbent_holdout["profit_factor"] > holdout_result["profit_factor"]
            or incumbent_holdout["max_dd_pct"] < holdout_result["max_dd_pct"]
        )
        payload["verdict"] = {
            "status": "reject_keep_incumbent" if incumbent_wins else "promote_candidate",
            "selected_run_name": incumbent_holdout["run_name"] if incumbent_wins else holdout_result["run_name"],
            "reason": (
                "holdout still favors the current feature-side incumbent"
                if incumbent_wins
                else "single-feature ablation candidate cleared the holdout gate versus the current incumbent"
            ),
        }
    else:
        payload["verdict"] = {
            "status": "validation_only_pending_holdout",
            "selected_run_name": logic_reference_run_name,
            "reason": "holdout not opened for the single-feature ablation batch, so the incumbent remains selected",
        }
    return payload


def format_metric(value: Any, digits: int = 4) -> str:
    if value is None:
        return "n/a"
    return f"{float(value):.{digits}f}"


def build_review_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# 05AG Stage 05 Trend-Strength Feature Ablation Review",
        "",
        f"Generated at: `{payload['generated_at_utc']}`",
        "",
        "## Scope",
        "",
        "- purpose: `drop one trend_strength feature at a time to see whether a single toxic feature explains the 05W sector-ablation win`",
        "- model family: `logistic_regression`",
        "- logic: `margin-only (min_margin=0.0700)`",
        f"- incumbent reference: `{payload['logic_reference_run_name']}`",
        "",
        "## MT5 Validation Ranking",
        "",
    ]
    for row in payload["ranked_validation_runs"]:
        lines.append(
            f"- [{row['rank']}] `{row['run_name']}`: "
            f"drop_feature=`{row['feature_name']}`, "
            f"offline_test_macro_f1={format_metric(row['offline_test_macro_f1'], 4)}, "
            f"return_pct={format_metric(row['return_pct'], 3)}, "
            f"profit_factor={format_metric(row['profit_factor'], 4)}, "
            f"max_dd_pct={format_metric(row['max_dd_pct'], 4)}, "
            f"ulcer_index={format_metric(row['ulcer_index'], 4)}, "
            f"trades={row['trade_count']}, "
            f"remaining_features={row['remaining_feature_count']}, "
            f"ready_gap={row['ready_row_gap']}, "
            f"unexpected_skips={row['unexpected_skip_count']}"
        )

    if "ranked_test_runs" in payload:
        lines.extend(["", "## MT5 Holdout Ranking", ""])
        for row in payload["ranked_test_runs"]:
            lines.append(
                f"- [{row['rank']}] `{row['run_name']}`: "
                f"drop_feature=`{row.get('feature_name', '-')}`, "
                f"return_pct={format_metric(row['return_pct'], 3)}, "
                f"profit_factor={format_metric(row['profit_factor'], 4)}, "
                f"max_dd_pct={format_metric(row['max_dd_pct'], 4)}, "
                f"ulcer_index={format_metric(row['ulcer_index'], 4)}, "
                f"trades={row['trade_count']}, "
                f"ready_gap={row['ready_row_gap']}, "
                f"unexpected_skips={row['unexpected_skip_count']}"
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
            "- read: `if no single-feature drop beats the sector-level incumbent, the edge likely comes from removing a correlated cluster rather than one obviously toxic feature`",
        ]
    )
    return "\n".join(lines) + "\n"


def update_review_index(review_dir: Path, run_tag: str, review_basename: str) -> None:
    existing_lines = []
    review_index_path = review_dir / "review_index.md"
    if review_index_path.exists():
        existing_lines = review_index_path.read_text(encoding="utf-8").splitlines()
    bullet = f"- `{run_tag}`: see `{review_basename}.md`"
    if bullet not in existing_lines:
        insert_at = 4 if len(existing_lines) >= 4 else len(existing_lines)
        existing_lines.insert(insert_at, bullet)
    write_text(review_index_path, "\n".join(existing_lines).rstrip() + "\n")


def main() -> int:
    args = build_parser().parse_args()

    stage_root = ROOT_DIR / args.stage_root
    review_dir = stage_root / "03_reviews"
    review_dir.mkdir(parents=True, exist_ok=True)

    run_name_to_feature: dict[str, str] = {}
    spec_map = feature_spec_map()
    for feature_name, (stage_id, run_name, review_basename) in spec_map.items():
        run_name_to_feature[run_name] = feature_name
        run_trial(
            feature_name=feature_name,
            stage_id=stage_id,
            run_name=run_name,
            review_basename=review_basename,
            run_holdout=False,
            args=args,
        )

    validation_views = load_view_map(set(run_name_to_feature), "validation")
    ranked_validation = [extract_payload(validation_views[run_name], run_name_to_feature[run_name]) for run_name in validation_views]

    holdout_result: dict[str, Any] | None = None
    incumbent_holdout: dict[str, Any] | None = None
    if ranked_validation and not args.skip_holdout:
        holdout_feature = resolve_holdout_feature(args, ranked_validation)
        stage_id, run_name, review_basename = spec_map[holdout_feature]
        run_trial(
            feature_name=holdout_feature,
            stage_id=stage_id,
            run_name=run_name,
            review_basename=review_basename,
            run_holdout=True,
            args=args,
        )
        holdout_views = load_view_map({run_name, args.logic_reference_run_name}, "test")
        holdout_result = extract_payload(holdout_views[run_name], holdout_feature)
        incumbent_holdout = extract_payload(holdout_views[args.logic_reference_run_name], "incumbent")

    review_payload = build_review_payload(
        ranked_validation=ranked_validation,
        holdout_result=holdout_result,
        incumbent_holdout=incumbent_holdout,
        logic_reference_run_name=args.logic_reference_run_name,
    )
    review_json_path = review_dir / "05AG_mt5_trend_strength_feature_ablation_review.json"
    review_md_path = review_dir / "05AG_mt5_trend_strength_feature_ablation_review.md"
    write_json(review_json_path, review_payload)
    write_text(review_md_path, build_review_markdown(review_payload))
    update_review_index(review_dir, "05AG", "05AG_mt5_trend_strength_feature_ablation_review")

    print(f"[done] review_md={review_md_path}")
    print(f"[done] review_json={review_json_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
