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

from foundation.pipelines.show_experiment_leaderboard import BundleView, load_bundle_views, sort_bundle_views


UTC = timezone.utc
REFERENCE_RUN_NAMES = [
    "05W_no_trend_strength_0001",
    "05BB_trend_proxy_persistence_only_0001",
    "05BF_trend_proxy_persistence_volatility_0001",
    "05AH_trend_proxy_sector_replacement_0001",
    "05AI_trend_proxy_light_pb_0001",
]
REFERENCE_LABELS = {
    "05W_no_trend_strength_0001": "incumbent_05w",
    "05BB_trend_proxy_persistence_only_0001": "persistence_only_reference",
    "05BF_trend_proxy_persistence_volatility_0001": "persistence_volatility_reference",
    "05AH_trend_proxy_sector_replacement_0001": "full_proxy_reference",
    "05AI_trend_proxy_light_pb_0001": "light_pb_reference",
}


@dataclass
class DownsideProxySpec:
    stage_id: str
    run_name: str
    experiment_id: str
    review_basename: str
    variant_label: str
    component_groups: list[str]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run downside-aware persistence proxy variants on top of the 05W feature base.")
    parser.add_argument("--stage-root", default="stages/05_optimization", help="Stage 05 root directory.")
    parser.add_argument(
        "--logic-reference-run-name",
        default="05W_no_trend_strength_0001",
        help="Current promoted incumbent used for validation/holdout comparison.",
    )
    parser.add_argument("--min-margin", type=float, default=0.07, help="Margin filter value copied from the incumbent logic.")
    parser.add_argument("--rebuild-bundle", action="store_true", help="Force bundle rebuild even if present.")
    parser.add_argument(
        "--skip-holdout",
        action="store_true",
        help="Run validation sweep only and do not open holdout for the top-two new proxy variants.",
    )
    return parser


def utc_now_iso() -> str:
    return datetime.now(tz=UTC).isoformat()


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_json(path: Path, payload: dict[str, Any]) -> None:
    write_text(path, json.dumps(payload, indent=2, ensure_ascii=False) + "\n")


def build_specs() -> list[DownsideProxySpec]:
    return [
        DownsideProxySpec(
            stage_id="05BZ",
            run_name="05BZ_trend_proxy_persistence_downside_0001",
            experiment_id="exp_05bz_trend_proxy_persistence_downside_v1",
            review_basename="05BZ_mt5_model_family_trial_review",
            variant_label="persistence_downside",
            component_groups=["trend_proxy_persistence", "trend_proxy_downside_pressure"],
        ),
        DownsideProxySpec(
            stage_id="05CA",
            run_name="05CA_trend_proxy_persistence_riskoff_0001",
            experiment_id="exp_05ca_trend_proxy_persistence_riskoff_v1",
            review_basename="05CA_mt5_model_family_trial_review",
            variant_label="persistence_riskoff",
            component_groups=["trend_proxy_persistence", "trend_proxy_risk_off_confirmation"],
        ),
        DownsideProxySpec(
            stage_id="05CB",
            run_name="05CB_trend_proxy_persistence_leader_drag_0001",
            experiment_id="exp_05cb_trend_proxy_persistence_leader_drag_v1",
            review_basename="05CB_mt5_model_family_trial_review",
            variant_label="persistence_leader_drag",
            component_groups=["trend_proxy_persistence", "trend_proxy_leader_drag"],
        ),
        DownsideProxySpec(
            stage_id="05CC",
            run_name="05CC_trend_proxy_persistence_downside_riskoff_0001",
            experiment_id="exp_05cc_trend_proxy_persistence_downside_riskoff_v1",
            review_basename="05CC_mt5_model_family_trial_review",
            variant_label="persistence_downside_riskoff",
            component_groups=["trend_proxy_persistence", "trend_proxy_downside_pressure", "trend_proxy_risk_off_confirmation"],
        ),
        DownsideProxySpec(
            stage_id="05CD",
            run_name="05CD_trend_proxy_persistence_session_riskoff_0001",
            experiment_id="exp_05cd_trend_proxy_persistence_session_riskoff_v1",
            review_basename="05CD_mt5_model_family_trial_review",
            variant_label="persistence_session_riskoff",
            component_groups=["trend_proxy_persistence", "trend_proxy_session_pressure", "trend_proxy_risk_off_confirmation"],
        ),
    ]


def run_trial(spec: DownsideProxySpec, args: argparse.Namespace, *, run_holdout: bool) -> None:
    cmd = [
        sys.executable,
        str(ROOT_DIR / "foundation" / "pipelines" / "run_stage05_mt5_model_family_trial.py"),
        "--model-family",
        "trend_proxy_sector_logreg",
        "--run-name",
        spec.run_name,
        "--experiment-id",
        spec.experiment_id,
        "--stage-id",
        spec.stage_id,
        "--review-basename",
        spec.review_basename,
        "--logic-reference-run-name",
        args.logic_reference_run_name,
        "--min-margin",
        f"{args.min_margin:.4f}",
        "--drop-sectors",
        "trend_strength",
        "--replacement-component-groups",
        ",".join(spec.component_groups),
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


def extract_payload(view: BundleView, spec: DownsideProxySpec | None, label: str) -> dict[str, Any]:
    extra = view.execution.get("extra") or {}
    return {
        "run_name": view.run_name,
        "variant_label": label,
        "component_groups": [] if spec is None else spec.component_groups,
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
        "phase": "05CE_mt5_downside_proxy_batch",
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
        holdout_winner = ranked_holdout[0]["run_name"]
        validation_winner = ranked_validation[0]["run_name"]
        if holdout_winner not in REFERENCE_RUN_NAMES and validation_winner == holdout_winner:
            payload["verdict"] = {
                "status": "promote_candidate",
                "selected_run_name": holdout_winner,
                "reason": "downside-aware persistence proxy led both validation and holdout across the current frontier",
            }
        elif holdout_winner not in REFERENCE_RUN_NAMES:
            payload["verdict"] = {
                "status": "mixed_holdout_win_keep_incumbent",
                "selected_run_name": incumbent_name,
                "reason": "downside-aware persistence proxy improved holdout but did not lead validation, so the incumbent stays promoted for now",
            }
        else:
            payload["verdict"] = {
                "status": "reject_keep_incumbent",
                "selected_run_name": incumbent_name,
                "reason": "no downside-aware persistence proxy cleared the current frontier on holdout",
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
        "# 05CE Stage 05 Downside Proxy Batch Review",
        "",
        f"Generated at: `{payload['generated_at_utc']}`",
        "",
        "## Scope",
        "",
        "- purpose: `extend the persistence-family frontier with downside, risk-off, leader-drag, and session-aware semantic proxies`",
        "- model family: `trend_proxy_sector_logreg`",
        "- reference runs: `05W`, `05BB`, `05BF`, `05AH`, `05AI`",
        "",
        "## MT5 Validation Ranking",
        "",
    ]
    for row in payload["ranked_validation_runs"]:
        groups = ", ".join(row["component_groups"]) if row["component_groups"] else "-"
        lines.append(
            f"- [{row['rank']}] `{row['run_name']}`: "
            f"variant=`{row['variant_label']}`, groups=`{groups}`, "
            f"return_pct={format_metric(row['return_pct'], 3)}, "
            f"profit_factor={format_metric(row['profit_factor'], 4)}, "
            f"max_dd_pct={format_metric(row['max_dd_pct'], 4)}, "
            f"ulcer_index={format_metric(row['ulcer_index'], 4)}, "
            f"trades={row['trade_count']}, ready_gap={row['ready_row_gap']}, unexpected_skips={row['unexpected_skip_count']}"
        )
    ranked_test_runs = payload.get("ranked_test_runs")
    if ranked_test_runs:
        lines.extend(["", "## MT5 Holdout Ranking", ""])
        for row in ranked_test_runs:
            groups = ", ".join(row["component_groups"]) if row["component_groups"] else "-"
            lines.append(
                f"- [{row['rank']}] `{row['run_name']}`: "
                f"variant=`{row['variant_label']}`, groups=`{groups}`, "
                f"return_pct={format_metric(row['return_pct'], 3)}, "
                f"profit_factor={format_metric(row['profit_factor'], 4)}, "
                f"max_dd_pct={format_metric(row['max_dd_pct'], 4)}, "
                f"ulcer_index={format_metric(row['ulcer_index'], 4)}, "
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
            "- read: `this batch asks whether the persistence edge improves when downside/risk-off structure is added instead of reintroducing the old trend-strength cluster`",
        ]
    )
    return "\n".join(lines) + "\n"


def update_review_index(review_dir: Path) -> None:
    review_index_path = review_dir / "review_index.md"
    lines = review_index_path.read_text(encoding="utf-8").splitlines() if review_index_path.exists() else []
    entry = "- `05CE`: see `05CE_mt5_downside_proxy_batch_review.md`"
    if entry not in lines:
        insert_at = 4 if len(lines) >= 4 else len(lines)
        lines.insert(insert_at, entry)
    write_text(review_index_path, "\n".join(lines).rstrip() + "\n")


def main() -> int:
    args = build_parser().parse_args()

    stage_root = ROOT_DIR / args.stage_root
    review_dir = stage_root / "03_reviews"
    review_dir.mkdir(parents=True, exist_ok=True)

    specs = build_specs()
    specs_by_run = {spec.run_name: spec for spec in specs}
    for spec in specs:
        run_trial(spec, args, run_holdout=False)

    validation_views = load_view_map(set(specs_by_run) | set(REFERENCE_RUN_NAMES), "validation")
    ranked_validation: list[dict[str, Any]] = []
    for run_name, view in validation_views.items():
        if run_name in specs_by_run:
            ranked_validation.append(extract_payload(view, specs_by_run[run_name], specs_by_run[run_name].variant_label))
        else:
            ranked_validation.append(extract_payload(view, None, REFERENCE_LABELS[run_name]))

    ranked_holdout: list[dict[str, Any]] | None = None
    if ranked_validation and not args.skip_holdout:
        top_two = [row["run_name"] for row in ranked_validation if row["run_name"] not in REFERENCE_RUN_NAMES][:2]
        for run_name in top_two:
            run_trial(specs_by_run[run_name], args, run_holdout=True)
        holdout_views = load_view_map(set(top_two) | set(REFERENCE_RUN_NAMES), "test")
        ranked_holdout = []
        for run_name, view in holdout_views.items():
            if run_name in specs_by_run:
                ranked_holdout.append(extract_payload(view, specs_by_run[run_name], specs_by_run[run_name].variant_label))
            else:
                ranked_holdout.append(extract_payload(view, None, REFERENCE_LABELS[run_name]))

    review_payload = build_review_payload(
        ranked_validation=ranked_validation,
        ranked_holdout=ranked_holdout,
        incumbent_name=args.logic_reference_run_name,
    )
    review_json_path = review_dir / "05CE_mt5_downside_proxy_batch_review.json"
    review_md_path = review_dir / "05CE_mt5_downside_proxy_batch_review.md"
    write_json(review_json_path, review_payload)
    write_text(review_md_path, build_review_markdown(review_payload))
    update_review_index(review_dir)

    print(f"[done] review_md={review_md_path}")
    print(f"[done] review_json={review_json_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
