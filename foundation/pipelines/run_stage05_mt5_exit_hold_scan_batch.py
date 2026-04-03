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
    "05W_no_trend_strength_0001",
    "05BB_trend_proxy_persistence_only_0001",
    "05BF_trend_proxy_persistence_volatility_0001",
]
REFERENCE_LABELS = {
    "05W_no_trend_strength_0001": "incumbent_05w",
    "05BB_trend_proxy_persistence_only_0001": "persistence_only_reference",
    "05BF_trend_proxy_persistence_volatility_0001": "persistence_volatility_reference",
}


@dataclass
class ExitHoldSpec:
    stage_id: str
    run_name: str
    experiment_id: str
    variant_label: str
    source_run_name: str
    min_margin: float
    max_hold_bars: int


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run exit-discipline scans on persistence-heavy Stage 05 challengers.")
    parser.add_argument("--stage-root", default="stages/05_optimization", help="Stage 05 root directory.")
    parser.add_argument(
        "--logic-reference-run-name",
        default="05W_no_trend_strength_0001",
        help="Current promoted incumbent used for validation/holdout comparison.",
    )
    parser.add_argument("--rebuild-bundle", action="store_true", help="Force bundle rebuild even if present.")
    parser.add_argument(
        "--skip-holdout",
        action="store_true",
        help="Run validation sweep only and do not open holdout for the top-two new exit-discipline candidates.",
    )
    return parser


def utc_now_iso() -> str:
    return datetime.now(tz=UTC).isoformat()


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_json(path: Path, payload: dict[str, Any]) -> None:
    write_text(path, json.dumps(payload, indent=2, ensure_ascii=False) + "\n")


def build_specs() -> list[ExitHoldSpec]:
    return [
        ExitHoldSpec(
            stage_id="05DE",
            run_name="05DE_05bb_margin_hold2_0001",
            experiment_id="exp_05de_05bb_margin_hold2_v1",
            variant_label="05bb_hold2",
            source_run_name="05BB_trend_proxy_persistence_only_0001",
            min_margin=0.07,
            max_hold_bars=2,
        ),
        ExitHoldSpec(
            stage_id="05DF",
            run_name="05DF_05bb_margin_hold4_0001",
            experiment_id="exp_05df_05bb_margin_hold4_v1",
            variant_label="05bb_hold4",
            source_run_name="05BB_trend_proxy_persistence_only_0001",
            min_margin=0.07,
            max_hold_bars=4,
        ),
        ExitHoldSpec(
            stage_id="05DG",
            run_name="05DG_05bb_margin_hold5_0001",
            experiment_id="exp_05dg_05bb_margin_hold5_v1",
            variant_label="05bb_hold5",
            source_run_name="05BB_trend_proxy_persistence_only_0001",
            min_margin=0.07,
            max_hold_bars=5,
        ),
        ExitHoldSpec(
            stage_id="05DH",
            run_name="05DH_05bf_margin_hold2_0001",
            experiment_id="exp_05dh_05bf_margin_hold2_v1",
            variant_label="05bf_hold2",
            source_run_name="05BF_trend_proxy_persistence_volatility_0001",
            min_margin=0.07,
            max_hold_bars=2,
        ),
        ExitHoldSpec(
            stage_id="05DI",
            run_name="05DI_05bf_margin_hold4_0001",
            experiment_id="exp_05di_05bf_margin_hold4_v1",
            variant_label="05bf_hold4",
            source_run_name="05BF_trend_proxy_persistence_volatility_0001",
            min_margin=0.07,
            max_hold_bars=4,
        ),
        ExitHoldSpec(
            stage_id="05DJ",
            run_name="05DJ_05bf_margin_hold5_0001",
            experiment_id="exp_05dj_05bf_margin_hold5_v1",
            variant_label="05bf_hold5",
            source_run_name="05BF_trend_proxy_persistence_volatility_0001",
            min_margin=0.07,
            max_hold_bars=5,
        ),
    ]


def build_rule_stack(spec: ExitHoldSpec) -> dict[str, Any]:
    return {
        "entry": [
            {
                "rule_id": "entry_01",
                "type": "threshold_entry",
                "enabled": True,
                "params": {
                    "short_threshold": 1.0 / 3.0,
                    "long_threshold": 1.0 / 3.0,
                },
            }
        ],
        "filters": [
            {
                "rule_id": "filter_01",
                "type": "max_probability_margin",
                "enabled": True,
                "params": {"min_margin": spec.min_margin},
            }
        ],
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


def resolve_source_run_dir(source_run_name: str) -> Path:
    candidate_paths = sorted((ROOT_DIR / "stages").glob(f"*/02_runs/active/{source_run_name}"))
    if not candidate_paths:
        raise FileNotFoundError(f"could not locate source run dir for {source_run_name}")
    return candidate_paths[0]


def ensure_bundle(spec: ExitHoldSpec, run_dir: Path, rebuild_bundle: bool) -> Path:
    source_run_dir = resolve_source_run_dir(spec.source_run_name)
    bundle_path = run_dir / "experiment_bundle.json"
    rule_stack_path = run_dir / "rule_stack.json"
    manifest_path = run_dir / "candidate_manifest.json"
    write_json(rule_stack_path, build_rule_stack(spec))
    write_json(
        manifest_path,
        {
            "generated_at_utc": utc_now_iso(),
            "candidate_type": "exit_hold_scan",
            "variant_label": spec.variant_label,
            "run_name": spec.run_name,
            "experiment_id": spec.experiment_id,
            "stage_id": spec.stage_id,
            "source_run_name": spec.source_run_name,
            "min_margin": spec.min_margin,
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


def extract_payload(view: BundleView, spec: ExitHoldSpec | None, label: str) -> dict[str, Any]:
    extra = view.execution.get("extra") or {}
    return {
        "run_name": view.run_name,
        "variant_label": label,
        "source_run_name": None if spec is None else spec.source_run_name,
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
        "phase": "05DK_mt5_exit_hold_scan_batch",
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
                "reason": "exit-discipline candidate led both validation and holdout across the current logic frontier",
            }
        elif holdout_winner not in REFERENCE_RUN_NAMES:
            payload["verdict"] = {
                "status": "mixed_holdout_win_keep_incumbent",
                "selected_run_name": incumbent_name,
                "reason": "exit-discipline candidate improved holdout but did not lead validation, so the incumbent stays promoted for now",
            }
        else:
            payload["verdict"] = {
                "status": "reject_keep_incumbent",
                "selected_run_name": incumbent_name,
                "reason": "no exit-discipline candidate cleared the current frontier on holdout",
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
        "# 05DK Stage 05 Exit Hold Scan Review",
        "",
        f"Generated at: `{payload['generated_at_utc']}`",
        "",
        "## Scope",
        "",
        "- purpose: `shift logic exploration away from extra entry filtering and toward exit discipline on persistence-heavy challengers`",
        "- reference runs: `05W`, `05BB`, `05BF`",
        "",
        "## MT5 Validation Ranking",
        "",
    ]
    for row in payload["ranked_validation_runs"]:
        margin_repr = "-" if row["min_margin"] is None else f"{row['min_margin']:.4f}"
        hold_repr = "-" if row["max_hold_bars"] is None else str(int(row["max_hold_bars"]))
        source_repr = row["source_run_name"] or "-"
        lines.append(
            f"- [{row['rank']}] `{row['run_name']}`: "
            f"variant=`{row['variant_label']}`, source=`{source_repr}`, margin={margin_repr}, hold={hold_repr}, "
            f"return_pct={format_metric(row['return_pct'], 3)}, profit_factor={format_metric(row['profit_factor'], 4)}, "
            f"max_dd_pct={format_metric(row['max_dd_pct'], 4)}, ulcer_index={format_metric(row['ulcer_index'], 4)}, "
            f"trades={row['trade_count']}, ready_gap={row['ready_row_gap']}, unexpected_skips={row['unexpected_skip_count']}"
        )
    ranked_test_runs = payload.get("ranked_test_runs")
    if ranked_test_runs:
        lines.extend(["", "## MT5 Holdout Ranking", ""])
        for row in ranked_test_runs:
            margin_repr = "-" if row["min_margin"] is None else f"{row['min_margin']:.4f}"
            hold_repr = "-" if row["max_hold_bars"] is None else str(int(row["max_hold_bars"]))
            source_repr = row["source_run_name"] or "-"
            lines.append(
                f"- [{row['rank']}] `{row['run_name']}`: "
                f"variant=`{row['variant_label']}`, source=`{source_repr}`, margin={margin_repr}, hold={hold_repr}, "
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
            "- read: `this batch asks whether persistence-heavy challengers were underperforming mainly because of exit timing rather than entry quality`",
        ]
    )
    return "\n".join(lines) + "\n"


def update_review_index(review_dir: Path) -> None:
    review_index_path = review_dir / "review_index.md"
    lines = review_index_path.read_text(encoding="utf-8").splitlines() if review_index_path.exists() else []
    entry = "- `05DK`: see `05DK_mt5_exit_hold_scan_review.md`"
    if entry not in lines:
        insert_at = 4 if len(lines) >= 4 else len(lines)
        lines.insert(insert_at, entry)
    write_text(review_index_path, "\n".join(lines).rstrip() + "\n")


def main() -> int:
    args = build_parser().parse_args()

    stage_root = ROOT_DIR / args.stage_root
    active_dir = stage_root / "02_runs" / "active"
    review_dir = stage_root / "03_reviews"
    active_dir.mkdir(parents=True, exist_ok=True)
    review_dir.mkdir(parents=True, exist_ok=True)

    specs = build_specs()
    specs_by_run = {spec.run_name: spec for spec in specs}
    for spec in specs:
        run_dir = active_dir / spec.run_name
        run_dir.mkdir(parents=True, exist_ok=True)
        bundle_path = ensure_bundle(spec, run_dir, args.rebuild_bundle)
        run_tester(bundle_path, split_name="validation")

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
            run_tester(active_dir / run_name / "experiment_bundle.json", split_name="test")
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
    review_json_path = review_dir / "05DK_mt5_exit_hold_scan_review.json"
    review_md_path = review_dir / "05DK_mt5_exit_hold_scan_review.md"
    write_json(review_json_path, review_payload)
    write_text(review_md_path, build_review_markdown(review_payload))
    update_review_index(review_dir)

    print(f"[done] review_md={review_md_path}")
    print(f"[done] review_json={review_json_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
