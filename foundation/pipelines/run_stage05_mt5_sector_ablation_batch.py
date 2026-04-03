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

from foundation.features.sector_map import SECTOR_MAP, validate_sector_map
from foundation.pipelines.experiment_bundle_models import ExperimentBundle
from foundation.pipelines.show_experiment_leaderboard import BundleView, load_bundle_views, sort_bundle_views


UTC = timezone.utc
VALIDATION_STAGE_SPECS = [
    ("05S", "price_return", "05S_no_price_return_0001", "05S_mt5_model_family_trial_review"),
    ("05T", "moving_average_trend", "05T_no_ma_trend_0001", "05T_mt5_model_family_trial_review"),
    ("05U", "momentum_oscillator", "05U_no_momentum_osc_0001", "05U_mt5_model_family_trial_review"),
    ("05V", "volatility_band", "05V_no_vol_band_0001", "05V_mt5_model_family_trial_review"),
    ("05W", "trend_strength", "05W_no_trend_strength_0001", "05W_mt5_model_family_trial_review"),
    ("05X", "session_context", "05X_no_session_ctx_0001", "05X_mt5_model_family_trial_review"),
    ("05Y", "risk_proxy", "05Y_no_risk_proxy_0001", "05Y_mt5_model_family_trial_review"),
    ("05Z", "leader_relative", "05Z_no_leader_rel_0001", "05Z_mt5_model_family_trial_review"),
    ("05AA", "breadth_dispersion", "05AA_no_breadth_disp_0001", "05AA_mt5_model_family_trial_review"),
]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run Stage 05 MT5 leave-one-sector-out feature ablation batch.")
    parser.add_argument("--stage-root", default="stages/05_optimization", help="Stage 05 root directory.")
    parser.add_argument(
        "--logic-reference-run-name",
        default="03E_mt5_validation_baseline_0001",
        help="Existing MT5 incumbent used as the logic-side comparison baseline.",
    )
    parser.add_argument("--min-margin", type=float, default=0.07, help="Margin filter value copied from 03E logic.")
    parser.add_argument(
        "--holdout-sector",
        default="",
        help="Optional explicit sector name to open on holdout after validation ranking. Defaults to validation leader.",
    )
    parser.add_argument("--rebuild-bundle", action="store_true", help="Force bundle rebuild when rerunning.")
    parser.add_argument(
        "--skip-holdout",
        action="store_true",
        help="Run validation sweep only and do not open holdout for the top sector-ablation candidate.",
    )
    return parser


def utc_now_iso() -> str:
    return datetime.now(tz=UTC).isoformat()


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_json(path: Path, payload: dict[str, Any]) -> None:
    write_text(path, json.dumps(payload, indent=2, ensure_ascii=False) + "\n")


def stage_spec_map() -> dict[str, tuple[str, str, str]]:
    return {sector: (stage_id, run_name, review_basename) for stage_id, sector, run_name, review_basename in VALIDATION_STAGE_SPECS}


def run_trial(*, sector: str, stage_id: str, run_name: str, review_basename: str, run_holdout: bool, args: argparse.Namespace) -> None:
    experiment_id = f"exp_{stage_id.lower()}_{sector}_sector_ablation_v1"
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
        "--drop-sectors",
        sector,
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


def extract_payload(view: BundleView, sector: str) -> dict[str, Any]:
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

    removed_feature_count = len(SECTOR_MAP[sector]) if sector in SECTOR_MAP else None
    return {
        "stage_folder": view.stage_folder,
        "run_name": view.run_name,
        "sector": sector,
        "removed_feature_count": removed_feature_count,
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


def resolve_holdout_sector(args: argparse.Namespace, ranked_validation: list[dict[str, Any]]) -> str:
    if args.holdout_sector:
        if args.holdout_sector not in stage_spec_map():
            raise ValueError(f"unknown holdout sector: {args.holdout_sector}")
        return args.holdout_sector
    return ranked_validation[0]["sector"]


def build_review_payload(
    *,
    ranked_validation: list[dict[str, Any]],
    holdout_result: dict[str, Any] | None,
    incumbent_holdout: dict[str, Any] | None,
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "generated_at_utc": utc_now_iso(),
        "phase": "05AB_mt5_sector_ablation_batch",
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
                "holdout still favors the incumbent logic/model bundle"
                if incumbent_wins
                else "sector-ablation candidate cleared the holdout gate versus the incumbent"
            ),
        }
    else:
        payload["verdict"] = {
            "status": "validation_only_pending_holdout",
            "selected_run_name": "03E_mt5_validation_baseline_0001",
            "reason": "holdout not opened for the sector-ablation batch, so the incumbent remains selected",
        }
    return payload


def format_metric(value: Any, digits: int = 4) -> str:
    if value is None:
        return "n/a"
    return f"{float(value):.{digits}f}"


def build_review_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# 05AB Stage 05 MT5 Sector Ablation Review",
        "",
        f"Generated at: `{payload['generated_at_utc']}`",
        "",
        "## Scope",
        "",
        "- purpose: `remove one Stage 01 base-feature sector at a time and see which omissions improve or damage MT5 behavior under the current 03E logic`",
        "- model family: `logistic_regression`",
        "- logic: `03E margin-only (min_margin=0.0700)`",
        "",
        "## MT5 Validation Ranking",
        "",
    ]
    for row in payload["ranked_validation_runs"]:
        lines.append(
            f"- [{row['rank']}] `{row['run_name']}`: "
            f"sector=`{row['sector']}`, "
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
                f"sector=`{row.get('sector', '-')}`, "
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
            "- read: `sector ablation is useful for finding redundancy, but promotion still requires the same holdout gate as every other Stage 05 exploration path`",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    args = build_parser().parse_args()
    validate_sector_map()

    stage_root = ROOT_DIR / args.stage_root
    review_dir = stage_root / "03_reviews"
    review_dir.mkdir(parents=True, exist_ok=True)

    run_name_to_sector: dict[str, str] = {}
    spec_map = stage_spec_map()
    for sector, (stage_id, run_name, review_basename) in spec_map.items():
        run_name_to_sector[run_name] = sector
        run_trial(
            sector=sector,
            stage_id=stage_id,
            run_name=run_name,
            review_basename=review_basename,
            run_holdout=False,
            args=args,
        )

    validation_views = load_view_map(set(run_name_to_sector), "validation")
    ranked_validation = [extract_payload(validation_views[run_name], run_name_to_sector[run_name]) for run_name in validation_views]

    holdout_result: dict[str, Any] | None = None
    incumbent_holdout: dict[str, Any] | None = None
    if ranked_validation and not args.skip_holdout:
        holdout_sector = resolve_holdout_sector(args, ranked_validation)
        stage_id, run_name, review_basename = spec_map[holdout_sector]
        run_trial(
            sector=holdout_sector,
            stage_id=stage_id,
            run_name=run_name,
            review_basename=review_basename,
            run_holdout=True,
            args=args,
        )
        holdout_views = load_view_map({run_name, args.logic_reference_run_name}, "test")
        holdout_result = extract_payload(holdout_views[run_name], holdout_sector)
        incumbent_holdout = extract_payload(holdout_views[args.logic_reference_run_name], "incumbent")

    review_payload = build_review_payload(
        ranked_validation=ranked_validation,
        holdout_result=holdout_result,
        incumbent_holdout=incumbent_holdout,
    )
    review_json_path = review_dir / "05AB_mt5_sector_ablation_review.json"
    review_md_path = review_dir / "05AB_mt5_sector_ablation_review.md"
    write_json(review_json_path, review_payload)
    write_text(review_md_path, build_review_markdown(review_payload))

    print(f"[done] review_md={review_md_path}")
    print(f"[done] review_json={review_json_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
