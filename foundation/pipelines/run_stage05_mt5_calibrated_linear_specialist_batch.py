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
    "05DP_05ca_margin0675_hold5_0001",
    "05EM_05dp_short_bias_margin_hold5_0001",
    "05DL_05cc_margin_hold5_0001",
]
REFERENCE_LABELS = {
    "05DP_05ca_margin0675_hold5_0001": "promoted_05dp",
    "05EM_05dp_short_bias_margin_hold5_0001": "closest_short_bias_05em",
    "05DL_05cc_margin_hold5_0001": "lower_ulcer_alt_05dl",
}


@dataclass
class SpecialistSpec:
    stage_id: str
    run_name: str
    experiment_id: str
    review_basename: str
    variant_label: str
    model_family: str


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run calibration-aware linear specialist batches on the 05CA -> 05DP line.")
    parser.add_argument("--stage-root", default="stages/05_optimization", help="Stage 05 root directory.")
    parser.add_argument(
        "--logic-reference-run-name",
        default="05DP_05ca_margin0675_hold5_0001",
        help="Current promoted incumbent used for validation/holdout comparison.",
    )
    parser.add_argument("--rebuild-bundle", action="store_true", help="Force bundle rebuild even if present.")
    parser.add_argument(
        "--skip-holdout",
        action="store_true",
        help="Run validation sweep only and do not open holdout for the top-two new specialist candidates.",
    )
    return parser


def utc_now_iso() -> str:
    return datetime.now(tz=UTC).isoformat()


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_json(path: Path, payload: dict[str, Any]) -> None:
    write_text(path, json.dumps(payload, indent=2, ensure_ascii=False) + "\n")


def build_specs() -> list[SpecialistSpec]:
    return [
        SpecialistSpec(
            stage_id="05FN",
            run_name="05FN_ovr_proxy_0001",
            experiment_id="exp_05fn_ovr_proxy_v1",
            review_basename="05FN_mt5_model_family_trial_review",
            variant_label="ovr_trend_proxy_logreg",
            model_family="ovr_trend_proxy_logreg",
        ),
        SpecialistSpec(
            stage_id="05FO",
            run_name="05FO_cal_proxy_0001",
            experiment_id="exp_05fo_cal_proxy_v1",
            review_basename="05FO_mt5_model_family_trial_review",
            variant_label="calibrated_trend_proxy_sigmoid",
            model_family="calibrated_trend_proxy_sigmoid",
        ),
        SpecialistSpec(
            stage_id="05FP",
            run_name="05FP_cal_ovr_proxy_0001",
            experiment_id="exp_05fp_cal_ovr_proxy_v1",
            review_basename="05FP_mt5_model_family_trial_review",
            variant_label="calibrated_ovr_trend_proxy_sigmoid",
            model_family="calibrated_ovr_trend_proxy_sigmoid",
        ),
    ]


def tail_lines(text: str, max_lines: int = 12) -> str:
    lines = [line.rstrip() for line in text.splitlines() if line.strip()]
    if not lines:
        return ""
    return "\n".join(lines[-max_lines:])


def run_trial(spec: SpecialistSpec, args: argparse.Namespace, *, run_holdout: bool) -> dict[str, Any]:
    cmd = [
        sys.executable,
        str(ROOT_DIR / "foundation" / "pipelines" / "run_stage05_mt5_model_family_trial.py"),
        "--model-family",
        spec.model_family,
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
        "0.0675",
        "--max-hold-bars",
        "5",
        "--drop-sectors",
        "trend_strength",
        "--replacement-component-groups",
        "trend_proxy_persistence,trend_proxy_risk_off_confirmation",
    ]
    if args.rebuild_bundle:
        cmd.append("--rebuild-bundle")
    if run_holdout:
        cmd.append("--run-holdout")
    completed = subprocess.run(
        cmd,
        cwd=ROOT_DIR,
        check=False,
        capture_output=True,
        text=True,
    )
    result: dict[str, Any] = {
        "run_name": spec.run_name,
        "variant_label": spec.variant_label,
        "model_family": spec.model_family,
        "status": "success" if completed.returncode == 0 else "failed",
        "run_holdout": run_holdout,
        "returncode": completed.returncode,
    }
    if completed.returncode != 0:
        result["error_tail"] = tail_lines((completed.stdout or "") + "\n" + (completed.stderr or ""))
    return result


def load_view_map(run_names: set[str], split_name: str) -> dict[str, BundleView]:
    views = load_bundle_views(ROOT_DIR / "stages", split_name)
    filtered = [view for view in views if view.run_name in run_names]
    return {view.run_name: view for view in sort_bundle_views(filtered, "return_pct")}


def extract_payload(view: BundleView, spec: SpecialistSpec | None, label: str) -> dict[str, Any]:
    extra = view.execution.get("extra") or {}
    return {
        "run_name": view.run_name,
        "variant_label": label,
        "model_family": None if spec is None else spec.model_family,
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
    failures: list[dict[str, Any]],
    incumbent_name: str,
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "generated_at_utc": utc_now_iso(),
        "phase": "05FQ_mt5_calibrated_linear_specialist_batch",
        "ranked_validation_runs": [{"rank": index + 1, **row} for index, row in enumerate(ranked_validation)],
        "failed_runs": failures,
    }
    if ranked_holdout is not None:
        payload["ranked_test_runs"] = [{"rank": index + 1, **row} for index, row in enumerate(ranked_holdout)]
        holdout_winner = ranked_holdout[0]["run_name"]
        validation_winner = ranked_validation[0]["run_name"]
        if holdout_winner not in REFERENCE_RUN_NAMES and validation_winner == holdout_winner:
            payload["verdict"] = {
                "status": "promote_candidate",
                "selected_run_name": holdout_winner,
                "reason": "calibration-aware linear specialist led both validation and holdout versus promoted 05DP",
            }
        elif holdout_winner not in REFERENCE_RUN_NAMES:
            payload["verdict"] = {
                "status": "mixed_holdout_win_keep_incumbent",
                "selected_run_name": incumbent_name,
                "reason": "specialist linear model improved holdout but did not lead validation, so 05DP remains promoted",
            }
        else:
            payload["verdict"] = {
                "status": "reject_keep_incumbent",
                "selected_run_name": incumbent_name,
                "reason": "no calibration-aware linear specialist cleared 05DP on holdout",
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
        "# 05FQ Stage 05 Calibrated Linear Specialist Review",
        "",
        f"Generated at: `{payload['generated_at_utc']}`",
        "",
        "## Scope",
        "",
        "- purpose: `retrain export-safe linear specialists on the 05CA feature line instead of applying post-hoc probability edits`",
        "- feature line: `trend_proxy_persistence + trend_proxy_risk_off_confirmation over the no_trend_strength base`",
        "- promoted incumbent: `05DP`",
        "",
        "## MT5 Validation Ranking",
        "",
    ]
    for row in payload["ranked_validation_runs"]:
        family = row["model_family"] or "-"
        lines.append(
            f"- [{row['rank']}] `{row['run_name']}`: "
            f"variant=`{row['variant_label']}`, family=`{family}`, "
            f"return_pct={format_metric(row['return_pct'], 3)}, profit_factor={format_metric(row['profit_factor'], 4)}, "
            f"max_dd_pct={format_metric(row['max_dd_pct'], 4)}, ulcer_index={format_metric(row['ulcer_index'], 4)}, "
                f"trades={row['trade_count']}, ready_gap={row['ready_row_gap']}, unexpected_skips={row['unexpected_skip_count']}"
            )
    failed_runs = payload.get("failed_runs") or []
    if failed_runs:
        lines.extend(["", "## Export / Smoke Failures", ""])
        for row in failed_runs:
            lines.append(
                f"- `{row['run_name']}`: variant=`{row['variant_label']}`, family=`{row['model_family']}`, "
                f"status=`{row['status']}`, returncode=`{row['returncode']}`"
            )
            error_tail = row.get("error_tail")
            if error_tail:
                lines.extend(["", "```text", error_tail, "```"])
    ranked_test_runs = payload.get("ranked_test_runs")
    if ranked_test_runs:
        lines.extend(["", "## MT5 Holdout Ranking", ""])
        for row in ranked_test_runs:
            family = row["model_family"] or "-"
            lines.append(
                f"- [{row['rank']}] `{row['run_name']}`: "
                f"variant=`{row['variant_label']}`, family=`{family}`, "
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
            "- read: `this batch asks whether the 05CA edge needs retrained linear specialization and calibration, rather than post-hoc output surgery`",
        ]
    )
    return "\n".join(lines) + "\n"


def update_review_index(review_dir: Path) -> None:
    review_index_path = review_dir / "review_index.md"
    lines = review_index_path.read_text(encoding="utf-8").splitlines() if review_index_path.exists() else []
    entry = "- `05FQ`: see `05FQ_mt5_calibrated_linear_specialist_review.md`"
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
    successful_specs_by_run: dict[str, SpecialistSpec] = {}
    failures: list[dict[str, Any]] = []
    for spec in specs:
        result = run_trial(spec, args, run_holdout=False)
        if result["status"] == "success":
            successful_specs_by_run[spec.run_name] = spec
        else:
            failures.append(result)

    validation_views = load_view_map(set(successful_specs_by_run) | set(REFERENCE_RUN_NAMES), "validation")
    ranked_validation: list[dict[str, Any]] = []
    for run_name, view in validation_views.items():
        if run_name in successful_specs_by_run:
            ranked_validation.append(
                extract_payload(view, successful_specs_by_run[run_name], successful_specs_by_run[run_name].variant_label)
            )
        else:
            ranked_validation.append(extract_payload(view, None, REFERENCE_LABELS[run_name]))

    ranked_holdout: list[dict[str, Any]] | None = None
    if ranked_validation and not args.skip_holdout:
        top_two = [row["run_name"] for row in ranked_validation if row["run_name"] not in REFERENCE_RUN_NAMES][:2]
        for run_name in top_two:
            result = run_trial(successful_specs_by_run[run_name], args, run_holdout=True)
            if result["status"] != "success":
                failures.append(result)
        holdout_views = load_view_map(set(top_two) | set(REFERENCE_RUN_NAMES), "test")
        ranked_holdout = []
        for run_name, view in holdout_views.items():
            if run_name in successful_specs_by_run:
                ranked_holdout.append(
                    extract_payload(view, successful_specs_by_run[run_name], successful_specs_by_run[run_name].variant_label)
                )
            else:
                ranked_holdout.append(extract_payload(view, None, REFERENCE_LABELS[run_name]))

    review_payload = build_review_payload(
        ranked_validation=ranked_validation,
        ranked_holdout=ranked_holdout,
        failures=failures,
        incumbent_name=args.logic_reference_run_name,
    )
    review_json_path = review_dir / "05FQ_mt5_calibrated_linear_specialist_review.json"
    review_md_path = review_dir / "05FQ_mt5_calibrated_linear_specialist_review.md"
    write_json(review_json_path, review_payload)
    write_text(review_md_path, build_review_markdown(review_payload))
    update_review_index(review_dir)

    print(f"[done] review_md={review_md_path}")
    print(f"[done] review_json={review_json_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
