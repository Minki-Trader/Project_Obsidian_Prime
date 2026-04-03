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
    "05DJ_05bf_margin_hold5_0001",
    "05DN_05ca_margin_hold5_0001",
    "05DL_05cc_margin_hold5_0001",
]
REFERENCE_LABELS = {
    "05DJ_05bf_margin_hold5_0001": "promoted_05dj",
    "05DN_05ca_margin_hold5_0001": "cross_05ca_hold5",
    "05DL_05cc_margin_hold5_0001": "cross_05cc_hold5",
}


@dataclass
class LocalProbeSpec:
    stage_id: str
    run_name: str
    experiment_id: str
    review_basename: str
    variant_label: str
    component_groups: list[str]
    min_margin: float
    max_hold_bars: int


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run a narrow local probe around the 05CA/05CC hold5 line.")
    parser.add_argument("--stage-root", default="stages/05_optimization", help="Stage 05 root directory.")
    parser.add_argument(
        "--logic-reference-run-name",
        default="05DJ_05bf_margin_hold5_0001",
        help="Current promoted incumbent used for validation/holdout comparison.",
    )
    parser.add_argument("--rebuild-bundle", action="store_true", help="Force bundle rebuild even if present.")
    parser.add_argument(
        "--skip-holdout",
        action="store_true",
        help="Run validation sweep only and do not open holdout for the top-two local-probe candidates.",
    )
    return parser


def utc_now_iso() -> str:
    return datetime.now(tz=UTC).isoformat()


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_json(path: Path, payload: dict[str, Any]) -> None:
    write_text(path, json.dumps(payload, indent=2, ensure_ascii=False) + "\n")


def build_specs() -> list[LocalProbeSpec]:
    group_05ca = ["trend_proxy_persistence", "trend_proxy_risk_off_confirmation"]
    group_05cc = ["trend_proxy_persistence", "trend_proxy_downside_pressure", "trend_proxy_risk_off_confirmation"]
    return [
        LocalProbeSpec(
            stage_id="05DP",
            run_name="05DP_05ca_margin0675_hold5_0001",
            experiment_id="exp_05dp_05ca_margin0675_hold5_v1",
            review_basename="05DP_mt5_model_family_trial_review",
            variant_label="05ca_m0675_h5",
            component_groups=group_05ca,
            min_margin=0.0675,
            max_hold_bars=5,
        ),
        LocalProbeSpec(
            stage_id="05DQ",
            run_name="05DQ_05ca_margin0725_hold5_0001",
            experiment_id="exp_05dq_05ca_margin0725_hold5_v1",
            review_basename="05DQ_mt5_model_family_trial_review",
            variant_label="05ca_m0725_h5",
            component_groups=group_05ca,
            min_margin=0.0725,
            max_hold_bars=5,
        ),
        LocalProbeSpec(
            stage_id="05DR",
            run_name="05DR_05cc_margin0675_hold5_0001",
            experiment_id="exp_05dr_05cc_margin0675_hold5_v1",
            review_basename="05DR_mt5_model_family_trial_review",
            variant_label="05cc_m0675_h5",
            component_groups=group_05cc,
            min_margin=0.0675,
            max_hold_bars=5,
        ),
        LocalProbeSpec(
            stage_id="05DS",
            run_name="05DS_05cc_margin0725_hold5_0001",
            experiment_id="exp_05ds_05cc_margin0725_hold5_v1",
            review_basename="05DS_mt5_model_family_trial_review",
            variant_label="05cc_m0725_h5",
            component_groups=group_05cc,
            min_margin=0.0725,
            max_hold_bars=5,
        ),
        LocalProbeSpec(
            stage_id="05DT",
            run_name="05DT_05ca_margin0700_hold6_0001",
            experiment_id="exp_05dt_05ca_margin0700_hold6_v1",
            review_basename="05DT_mt5_model_family_trial_review",
            variant_label="05ca_m0700_h6",
            component_groups=group_05ca,
            min_margin=0.0700,
            max_hold_bars=6,
        ),
        LocalProbeSpec(
            stage_id="05DU",
            run_name="05DU_05cc_margin0700_hold6_0001",
            experiment_id="exp_05du_05cc_margin0700_hold6_v1",
            review_basename="05DU_mt5_model_family_trial_review",
            variant_label="05cc_m0700_h6",
            component_groups=group_05cc,
            min_margin=0.0700,
            max_hold_bars=6,
        ),
    ]


def run_trial(spec: LocalProbeSpec, args: argparse.Namespace, *, run_holdout: bool) -> None:
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
        f"{spec.min_margin:.4f}",
        "--max-hold-bars",
        str(spec.max_hold_bars),
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


def extract_payload(view: BundleView, spec: LocalProbeSpec | None, label: str) -> dict[str, Any]:
    extra = view.execution.get("extra") or {}
    return {
        "run_name": view.run_name,
        "variant_label": label,
        "component_groups": [] if spec is None else spec.component_groups,
        "min_margin": None if spec is None else spec.min_margin,
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
        "phase": "05DV_mt5_downside_local_probe_batch",
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
                "reason": "local-probe candidate led both validation and holdout versus the promoted incumbent",
            }
        elif holdout_winner not in REFERENCE_RUN_NAMES:
            payload["verdict"] = {
                "status": "mixed_holdout_win_keep_incumbent",
                "selected_run_name": incumbent_name,
                "reason": "local-probe candidate improved holdout but did not lead validation, so the promoted incumbent stays in place",
            }
        else:
            payload["verdict"] = {
                "status": "reject_keep_incumbent",
                "selected_run_name": incumbent_name,
                "reason": "no local-probe candidate cleared the promoted incumbent on holdout",
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
        "# 05DV Stage 05 Downside Local Probe Review",
        "",
        f"Generated at: `{payload['generated_at_utc']}`",
        "",
        "## Scope",
        "",
        "- purpose: `run a narrow local probe around the 05CA/05CC hold5 line using only mild margin and hold-window tweaks`",
        "- promoted incumbent: `05DJ`",
        "",
        "## MT5 Validation Ranking",
        "",
    ]
    for row in payload["ranked_validation_runs"]:
        groups = ", ".join(row["component_groups"]) if row["component_groups"] else "-"
        margin_repr = "-" if row["min_margin"] is None else f"{row['min_margin']:.4f}"
        hold_repr = "-" if row["max_hold_bars"] is None else str(int(row["max_hold_bars"]))
        lines.append(
            f"- [{row['rank']}] `{row['run_name']}`: "
            f"variant=`{row['variant_label']}`, groups=`{groups}`, margin={margin_repr}, hold={hold_repr}, "
            f"return_pct={format_metric(row['return_pct'], 3)}, profit_factor={format_metric(row['profit_factor'], 4)}, "
            f"max_dd_pct={format_metric(row['max_dd_pct'], 4)}, ulcer_index={format_metric(row['ulcer_index'], 4)}, "
            f"trades={row['trade_count']}, ready_gap={row['ready_row_gap']}, unexpected_skips={row['unexpected_skip_count']}"
        )
    ranked_test_runs = payload.get("ranked_test_runs")
    if ranked_test_runs:
        lines.extend(["", "## MT5 Holdout Ranking", ""])
        for row in ranked_test_runs:
            groups = ", ".join(row["component_groups"]) if row["component_groups"] else "-"
            margin_repr = "-" if row["min_margin"] is None else f"{row['min_margin']:.4f}"
            hold_repr = "-" if row["max_hold_bars"] is None else str(int(row["max_hold_bars"]))
            lines.append(
                f"- [{row['rank']}] `{row['run_name']}`: "
                f"variant=`{row['variant_label']}`, groups=`{groups}`, margin={margin_repr}, hold={hold_repr}, "
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
            "- read: `this is a local neighborhood test, not a new family; the goal is to see whether the near-tie versus 05DJ can be resolved with small changes only`",
        ]
    )
    return "\n".join(lines) + "\n"


def update_review_index(review_dir: Path) -> None:
    review_index_path = review_dir / "review_index.md"
    lines = review_index_path.read_text(encoding="utf-8").splitlines() if review_index_path.exists() else []
    entry = "- `05DV`: see `05DV_mt5_downside_local_probe_review.md`"
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
    review_json_path = review_dir / "05DV_mt5_downside_local_probe_review.json"
    review_md_path = review_dir / "05DV_mt5_downside_local_probe_review.md"
    write_json(review_json_path, review_payload)
    write_text(review_md_path, build_review_markdown(review_payload))
    update_review_index(review_dir)

    print(f"[done] review_md={review_md_path}")
    print(f"[done] review_json={review_json_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
