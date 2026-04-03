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
]
REFERENCE_LABELS = {
    "05W_no_trend_strength_0001": "incumbent_05w",
    "05BB_trend_proxy_persistence_only_0001": "persistence_only_reference",
    "05BF_trend_proxy_persistence_volatility_0001": "persistence_volatility_reference",
    "05AH_trend_proxy_sector_replacement_0001": "full_proxy_reference",
}


@dataclass
class VoteSpec:
    stage_id: str
    run_name: str
    experiment_id: str
    review_basename: str
    variant_label: str
    voter_components: list[str]
    voter_weights: list[float]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run persistence-heavy frontier soft-voting experiments for Stage 05.")
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
        help="Run validation sweep only and do not open holdout for the top-two new vote candidates.",
    )
    return parser


def utc_now_iso() -> str:
    return datetime.now(tz=UTC).isoformat()


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_json(path: Path, payload: dict[str, Any]) -> None:
    write_text(path, json.dumps(payload, indent=2, ensure_ascii=False) + "\n")


def build_specs() -> list[VoteSpec]:
    return [
        VoteSpec(
            stage_id="05BP",
            run_name="05BP_frontier_vote_w_bb_0001",
            experiment_id="exp_05bp_frontier_vote_w_bb_v1",
            review_basename="05BP_mt5_model_family_trial_review",
            variant_label="vote_05w_bb_equal",
            voter_components=["base_05w", "persistence_only"],
            voter_weights=[1.0, 1.0],
        ),
        VoteSpec(
            stage_id="05BQ",
            run_name="05BQ_frontier_vote_w_bf_0001",
            experiment_id="exp_05bq_frontier_vote_w_bf_v1",
            review_basename="05BQ_mt5_model_family_trial_review",
            variant_label="vote_05w_bf_equal",
            voter_components=["base_05w", "persistence_volatility"],
            voter_weights=[1.0, 1.0],
        ),
        VoteSpec(
            stage_id="05BR",
            run_name="05BR_frontier_vote_w_bb_bf_0001",
            experiment_id="exp_05br_frontier_vote_w_bb_bf_v1",
            review_basename="05BR_mt5_model_family_trial_review",
            variant_label="vote_05w_bb_bf_equal",
            voter_components=["base_05w", "persistence_only", "persistence_volatility"],
            voter_weights=[1.0, 1.0, 1.0],
        ),
        VoteSpec(
            stage_id="05BS",
            run_name="05BS_frontier_vote_w_bb_ah_0001",
            experiment_id="exp_05bs_frontier_vote_w_bb_ah_v1",
            review_basename="05BS_mt5_model_family_trial_review",
            variant_label="vote_05w_bb_fullproxy_weighted",
            voter_components=["base_05w", "persistence_only", "full_proxy"],
            voter_weights=[2.0, 2.0, 1.0],
        ),
    ]


def run_trial(spec: VoteSpec, args: argparse.Namespace, *, run_holdout: bool) -> None:
    cmd = [
        sys.executable,
        str(ROOT_DIR / "foundation" / "pipelines" / "run_stage05_mt5_model_family_trial.py"),
        "--model-family",
        "persistence_frontier_voter",
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
        "--voter-components",
        ",".join(spec.voter_components),
        "--voter-weights",
        ",".join(f"{weight:.6f}" for weight in spec.voter_weights),
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


def extract_payload(view: BundleView, spec: VoteSpec | None, label: str) -> dict[str, Any]:
    extra = view.execution.get("extra") or {}
    return {
        "run_name": view.run_name,
        "variant_label": label,
        "voter_components": [] if spec is None else spec.voter_components,
        "voter_weights": [] if spec is None else spec.voter_weights,
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
        "phase": "05BT_mt5_persistence_frontier_vote_batch",
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
                "reason": "persistence-heavy voting blend led both validation and holdout across the current frontier",
            }
        elif holdout_winner not in REFERENCE_RUN_NAMES:
            payload["verdict"] = {
                "status": "mixed_holdout_win_keep_incumbent",
                "selected_run_name": incumbent_name,
                "reason": "voting blend improved holdout but did not lead validation, so the incumbent stays promoted for now",
            }
        else:
            payload["verdict"] = {
                "status": "reject_keep_incumbent",
                "selected_run_name": incumbent_name,
                "reason": "no persistence-heavy voting blend cleared the current frontier on holdout",
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
        "# 05BT Stage 05 Persistence Frontier Vote Review",
        "",
        f"Generated at: `{payload['generated_at_utc']}`",
        "",
        "## Scope",
        "",
        "- purpose: `probe soft-voting blends built from the persistence-heavy frontier instead of narrowing too early to one feature-side line`",
        "- model family: `persistence_frontier_voter`",
        "- reference runs: `05W`, `05BB`, `05BF`, `05AH`",
        "",
        "## MT5 Validation Ranking",
        "",
    ]
    for row in payload["ranked_validation_runs"]:
        components = ", ".join(row["voter_components"]) if row["voter_components"] else "-"
        weights = ", ".join(f"{weight:.3f}" for weight in row["voter_weights"]) if row["voter_weights"] else "-"
        lines.append(
            f"- [{row['rank']}] `{row['run_name']}`: "
            f"variant=`{row['variant_label']}`, components=`{components}`, weights=`{weights}`, "
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
            components = ", ".join(row["voter_components"]) if row["voter_components"] else "-"
            weights = ", ".join(f"{weight:.3f}" for weight in row["voter_weights"]) if row["voter_weights"] else "-"
            lines.append(
                f"- [{row['rank']}] `{row['run_name']}`: "
                f"variant=`{row['variant_label']}`, components=`{components}`, weights=`{weights}`, "
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
            "- read: `these voting blends are breadth-first ensemble probes; keep any holdout-positive mix as a challenger unless it also proves validation durability`",
        ]
    )
    return "\n".join(lines) + "\n"


def update_review_index(review_dir: Path) -> None:
    review_index_path = review_dir / "review_index.md"
    lines = review_index_path.read_text(encoding="utf-8").splitlines() if review_index_path.exists() else []
    entry = "- `05BT`: see `05BT_mt5_persistence_frontier_vote_review.md`"
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
    review_json_path = review_dir / "05BT_mt5_persistence_frontier_vote_review.json"
    review_md_path = review_dir / "05BT_mt5_persistence_frontier_vote_review.md"
    write_json(review_json_path, review_payload)
    write_text(review_md_path, build_review_markdown(review_payload))
    update_review_index(review_dir)

    print(f"[done] review_md={review_md_path}")
    print(f"[done] review_json={review_json_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
