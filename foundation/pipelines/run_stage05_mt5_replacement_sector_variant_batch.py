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


@dataclass
class ReplacementVariantSpec:
    stage_id: str
    run_name: str
    experiment_id: str
    review_basename: str
    variant_label: str
    component_groups: list[str]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run lightweight replacement-sector variants for Stage 05 broad exploration.")
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
        help="Run validation sweep only and do not open holdout for the top-two validation variants.",
    )
    return parser


def utc_now_iso() -> str:
    return datetime.now(tz=UTC).isoformat()


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_json(path: Path, payload: dict[str, Any]) -> None:
    write_text(path, json.dumps(payload, indent=2, ensure_ascii=False) + "\n")


def build_specs() -> list[ReplacementVariantSpec]:
    return [
        ReplacementVariantSpec(
            stage_id="05AI",
            run_name="05AI_trend_proxy_light_pb_0001",
            experiment_id="exp_05ai_trend_proxy_light_pb_v1",
            review_basename="05AI_mt5_model_family_trial_review",
            variant_label="light_persistence_breakout",
            component_groups=["trend_proxy_persistence", "trend_proxy_breakout_pressure"],
        ),
        ReplacementVariantSpec(
            stage_id="05AJ",
            run_name="05AJ_trend_proxy_light_vb_0001",
            experiment_id="exp_05aj_trend_proxy_light_vb_v1",
            review_basename="05AJ_mt5_model_family_trial_review",
            variant_label="light_volatility_breadth",
            component_groups=["trend_proxy_volatility_regime", "trend_proxy_breadth_confirmation"],
        ),
        ReplacementVariantSpec(
            stage_id="05AK",
            run_name="05AK_trend_proxy_light_core3_0001",
            experiment_id="exp_05ak_trend_proxy_light_core3_v1",
            review_basename="05AK_mt5_model_family_trial_review",
            variant_label="light_core_three",
            component_groups=[
                "trend_proxy_persistence",
                "trend_proxy_volatility_regime",
                "trend_proxy_breakout_pressure",
            ],
        ),
        ReplacementVariantSpec(
            stage_id="05AL",
            run_name="05AL_trend_proxy_light_pc_0001",
            experiment_id="exp_05al_trend_proxy_light_pc_v1",
            review_basename="05AL_mt5_model_family_trial_review",
            variant_label="light_persistence_confirmation",
            component_groups=["trend_proxy_persistence", "trend_proxy_breadth_confirmation"],
        ),
    ]


def run_trial(spec: ReplacementVariantSpec, args: argparse.Namespace, *, run_holdout: bool) -> None:
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


def extract_payload(view: BundleView, spec: ReplacementVariantSpec | None, label: str) -> dict[str, Any]:
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
    incumbent_validation: dict[str, Any],
    incumbent_name: str,
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "generated_at_utc": utc_now_iso(),
        "phase": "05AM_mt5_replacement_sector_variant_batch",
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
        top_variant = ranked_validation[0]
        variant_beats_incumbent_validation = (
            top_variant["return_pct"] is not None
            and incumbent_validation["return_pct"] is not None
            and top_variant["profit_factor"] is not None
            and incumbent_validation["profit_factor"] is not None
            and top_variant["return_pct"] > incumbent_validation["return_pct"]
            and top_variant["profit_factor"] > incumbent_validation["profit_factor"]
        )
        if holdout_winner != incumbent_name and validation_winner == holdout_winner and variant_beats_incumbent_validation:
            payload["verdict"] = {
                "status": "promote_candidate",
                "selected_run_name": holdout_winner,
                "reason": "lightweight replacement variant led both validation and holdout versus the incumbent",
            }
        elif holdout_winner != incumbent_name:
            payload["verdict"] = {
                "status": "mixed_holdout_win_keep_incumbent",
                "selected_run_name": incumbent_name,
                "reason": "a lightweight variant won holdout but did not lead validation, so the incumbent stays promoted for now",
            }
        else:
            payload["verdict"] = {
                "status": "reject_keep_incumbent",
                "selected_run_name": incumbent_name,
                "reason": "no lightweight replacement variant cleared the incumbent on holdout",
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
        "# 05AM Stage 05 Replacement Sector Variant Review",
        "",
        f"Generated at: `{payload['generated_at_utc']}`",
        "",
        "## Scope",
        "",
        "- purpose: `scan lighter replacement-sector variants before deciding whether the full 05AH proxy block is too heavy`",
        "- model family: `trend_proxy_sector_logreg`",
        "- incumbent reference: `05W_no_trend_strength_0001`",
        "",
        "## MT5 Validation Ranking",
        "",
    ]
    for row in payload["ranked_validation_runs"]:
        lines.append(
            f"- [{row['rank']}] `{row['run_name']}`: "
            f"variant=`{row['variant_label']}`, groups=`{', '.join(row['component_groups'])}`, "
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
            lines.append(
                f"- [{row['rank']}] `{row['run_name']}`: "
                f"variant=`{row['variant_label']}`, groups=`{', '.join(row['component_groups'])}`, "
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
            "- read: `lighter replacement sectors are useful if they keep 05W's validation edge while borrowing some of 05AH's holdout strength`",
        ]
    )
    return "\n".join(lines) + "\n"


def update_review_index(review_dir: Path) -> None:
    review_index_path = review_dir / "review_index.md"
    lines = review_index_path.read_text(encoding="utf-8").splitlines() if review_index_path.exists() else []
    entry = "- `05AM`: see `05AM_mt5_replacement_sector_variant_review.md`"
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

    validation_views = load_view_map(set(specs_by_run) | {args.logic_reference_run_name}, "validation")
    ranked_validation = [extract_payload(validation_views[run_name], specs_by_run[run_name], specs_by_run[run_name].variant_label) for run_name in validation_views]
    ranked_validation = [row for row in ranked_validation if row["run_name"] != args.logic_reference_run_name]
    incumbent_validation = extract_payload(validation_views[args.logic_reference_run_name], None, "incumbent")

    ranked_holdout: list[dict[str, Any]] | None = None
    if ranked_validation and not args.skip_holdout:
        top_two = [row["run_name"] for row in ranked_validation[:2]]
        for run_name in top_two:
            run_trial(specs_by_run[run_name], args, run_holdout=True)
        holdout_views = load_view_map(set(top_two) | {args.logic_reference_run_name}, "test")
        ranked_holdout = []
        for run_name, view in holdout_views.items():
            if run_name == args.logic_reference_run_name:
                ranked_holdout.append(extract_payload(view, None, "incumbent"))
            else:
                ranked_holdout.append(extract_payload(view, specs_by_run[run_name], specs_by_run[run_name].variant_label))

    review_payload = build_review_payload(
        ranked_validation=ranked_validation,
        ranked_holdout=ranked_holdout,
        incumbent_validation=incumbent_validation,
        incumbent_name=args.logic_reference_run_name,
    )
    review_json_path = review_dir / "05AM_mt5_replacement_sector_variant_review.json"
    review_md_path = review_dir / "05AM_mt5_replacement_sector_variant_review.md"
    write_json(review_json_path, review_payload)
    write_text(review_md_path, build_review_markdown(review_payload))
    update_review_index(review_dir)

    print(f"[done] review_md={review_md_path}")
    print(f"[done] review_json={review_json_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
