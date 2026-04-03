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
    "05AI_trend_proxy_light_pb_0001",
    "05AJ_trend_proxy_light_vb_0001",
]


@dataclass
class CrossSpec:
    stage_id: str
    run_name: str
    experiment_id: str
    review_basename: str
    source_run_name: str
    source_label: str
    mix_label: str
    short_threshold: float
    long_threshold: float
    min_margin: float | None = None
    min_probability_diff: float | None = None


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Cross lightweight proxy variants with alternate logic families.")
    parser.add_argument("--stage-root", default="stages/05_optimization", help="Stage 05 root directory.")
    parser.add_argument("--rebuild-bundle", action="store_true", help="Force bundle rebuild even if present.")
    parser.add_argument(
        "--skip-holdout",
        action="store_true",
        help="Run validation sweep only and do not open holdout for the top-two new cross candidates.",
    )
    return parser


def utc_now_iso() -> str:
    return datetime.now(tz=UTC).isoformat()


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_json(path: Path, payload: dict[str, Any]) -> None:
    write_text(path, json.dumps(payload, indent=2, ensure_ascii=False) + "\n")


def build_specs() -> list[CrossSpec]:
    return [
        CrossSpec("05AS", "05AS_05ai_thr_margin_0001", "exp_05as_05ai_thr_margin_v1", "05AS_mt5_logic_cross_review", "05AI_trend_proxy_light_pb_0001", "light_pb", "threshold_margin", 0.535, 0.400, min_margin=0.0700),
        CrossSpec("05AT", "05AT_05ai_thr_combo_0001", "exp_05at_05ai_thr_combo_v1", "05AT_mt5_logic_cross_review", "05AI_trend_proxy_light_pb_0001", "light_pb", "threshold_margin_diff", 0.535, 0.400, min_margin=0.0500, min_probability_diff=0.0700),
        CrossSpec("05AU", "05AU_05ai_diff_only_0001", "exp_05au_05ai_diff_only_v1", "05AU_mt5_logic_cross_review", "05AI_trend_proxy_light_pb_0001", "light_pb", "diff_only", 1.0 / 3.0, 1.0 / 3.0, min_probability_diff=0.0775),
        CrossSpec("05AV", "05AV_05ai_combo_loose_0001", "exp_05av_05ai_combo_loose_v1", "05AV_mt5_logic_cross_review", "05AI_trend_proxy_light_pb_0001", "light_pb", "margin_diff_loose", 1.0 / 3.0, 1.0 / 3.0, min_margin=0.0500, min_probability_diff=0.0700),
        CrossSpec("05AW", "05AW_05aj_thr_margin_0001", "exp_05aw_05aj_thr_margin_v1", "05AW_mt5_logic_cross_review", "05AJ_trend_proxy_light_vb_0001", "light_vb", "threshold_margin", 0.535, 0.400, min_margin=0.0700),
        CrossSpec("05AX", "05AX_05aj_thr_combo_0001", "exp_05ax_05aj_thr_combo_v1", "05AX_mt5_logic_cross_review", "05AJ_trend_proxy_light_vb_0001", "light_vb", "threshold_margin_diff", 0.535, 0.400, min_margin=0.0500, min_probability_diff=0.0700),
        CrossSpec("05AY", "05AY_05aj_diff_only_0001", "exp_05ay_05aj_diff_only_v1", "05AY_mt5_logic_cross_review", "05AJ_trend_proxy_light_vb_0001", "light_vb", "diff_only", 1.0 / 3.0, 1.0 / 3.0, min_probability_diff=0.0775),
        CrossSpec("05AZ", "05AZ_05aj_combo_loose_0001", "exp_05az_05aj_combo_loose_v1", "05AZ_mt5_logic_cross_review", "05AJ_trend_proxy_light_vb_0001", "light_vb", "margin_diff_loose", 1.0 / 3.0, 1.0 / 3.0, min_margin=0.0500, min_probability_diff=0.0700),
    ]


def build_rule_stack(spec: CrossSpec) -> dict[str, Any]:
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
                "params": {"max_hold_bars": 3},
            }
        ],
    }


def resolve_run_dir(run_name: str) -> Path:
    candidates = sorted((ROOT_DIR / "stages").glob(f"*/02_runs/active/{run_name}"))
    if not candidates:
        raise FileNotFoundError(f"could not locate source run dir: {run_name}")
    return candidates[0]


def ensure_bundle(spec: CrossSpec, run_dir: Path, source_run_dir: Path, rebuild_bundle: bool) -> Path:
    bundle_path = run_dir / "experiment_bundle.json"
    rule_stack_path = run_dir / "rule_stack.json"
    manifest_path = run_dir / "candidate_manifest.json"
    write_json(rule_stack_path, build_rule_stack(spec))
    write_json(
        manifest_path,
        {
            "generated_at_utc": utc_now_iso(),
            "candidate_type": "lightweight_proxy_logic_cross",
            "source_run_name": spec.source_run_name,
            "source_label": spec.source_label,
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


def extract_payload(view: BundleView, spec: CrossSpec | None, source_label: str, mix_label: str) -> dict[str, Any]:
    extra = view.execution.get("extra") or {}
    return {
        "run_name": view.run_name,
        "source_label": source_label,
        "mix_label": mix_label,
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
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "generated_at_utc": utc_now_iso(),
        "phase": "05BA_mt5_lightweight_proxy_logic_cross_batch",
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
                "reason": "cross candidate led both validation and holdout across the lightweight-proxy logic sweep",
            }
        elif holdout_winner not in REFERENCE_RUN_NAMES:
            payload["verdict"] = {
                "status": "mixed_holdout_win_keep_incumbent",
                "selected_run_name": "05W_no_trend_strength_0001",
                "reason": "cross candidate improved holdout but did not lead validation, so the incumbent stays promoted for now",
            }
        else:
            payload["verdict"] = {
                "status": "reject_keep_incumbent",
                "selected_run_name": "05W_no_trend_strength_0001",
                "reason": "no cross candidate cleared the current incumbents on holdout",
            }
    else:
        payload["verdict"] = {
            "status": "validation_only_pending_holdout",
            "selected_run_name": "05W_no_trend_strength_0001",
            "reason": "holdout not run yet, so the incumbent remains selected",
        }
    return payload


def format_metric(value: Any, digits: int = 4) -> str:
    if value is None:
        return "n/a"
    return f"{float(value):.{digits}f}"


def build_review_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# 05BA Stage 05 Lightweight Proxy Logic Cross Review",
        "",
        f"Generated at: `{payload['generated_at_utc']}`",
        "",
        "## Scope",
        "",
        "- purpose: `cross lightweight proxy variants with alternate logic families to widen the search instead of narrowing too early`",
        "- reference runs: `05W`, `05AI`, `05AJ`",
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
            f"source=`{row['source_label']}`, mix=`{row['mix_label']}`, Ts={ts_repr}, Tl={tl_repr}, margin={margin_repr}, diff={diff_repr}, "
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
                f"source=`{row['source_label']}`, mix=`{row['mix_label']}`, Ts={ts_repr}, Tl={tl_repr}, margin={margin_repr}, diff={diff_repr}, "
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
            "- read: `this cross batch is breadth-first by design; mixed holdout-positive results should stay as challengers until they also prove validation durability`",
        ]
    )
    return "\n".join(lines) + "\n"


def update_review_index(review_dir: Path) -> None:
    review_index_path = review_dir / "review_index.md"
    lines = review_index_path.read_text(encoding="utf-8").splitlines() if review_index_path.exists() else []
    entry = "- `05BA`: see `05BA_mt5_lightweight_proxy_logic_cross_review.md`"
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
    source_dirs = {spec.source_run_name: resolve_run_dir(spec.source_run_name) for spec in specs}

    for spec in specs:
        run_dir = active_dir / spec.run_name
        run_dir.mkdir(parents=True, exist_ok=True)
        bundle_path = ensure_bundle(spec, run_dir, source_dirs[spec.source_run_name], args.rebuild_bundle)
        run_tester(bundle_path, split_name="validation")

    validation_views = load_view_map(set(specs_by_run) | set(REFERENCE_RUN_NAMES), "validation")
    ranked_validation: list[dict[str, Any]] = []
    for run_name, view in validation_views.items():
        if run_name in specs_by_run:
            spec = specs_by_run[run_name]
            ranked_validation.append(extract_payload(view, spec, spec.source_label, spec.mix_label))
        elif run_name == "05W_no_trend_strength_0001":
            ranked_validation.append(extract_payload(view, None, "incumbent", "margin_only"))
        elif run_name == "05AI_trend_proxy_light_pb_0001":
            ranked_validation.append(extract_payload(view, None, "light_pb", "margin_only"))
        elif run_name == "05AJ_trend_proxy_light_vb_0001":
            ranked_validation.append(extract_payload(view, None, "light_vb", "margin_only"))

    ranked_holdout: list[dict[str, Any]] | None = None
    if ranked_validation and not args.skip_holdout:
        top_new_candidates = [row["run_name"] for row in ranked_validation if row["run_name"] not in REFERENCE_RUN_NAMES][:2]
        for run_name in top_new_candidates:
            run_tester(active_dir / run_name / "experiment_bundle.json", split_name="test")
        holdout_views = load_view_map(set(top_new_candidates) | set(REFERENCE_RUN_NAMES), "test")
        ranked_holdout = []
        for run_name, view in holdout_views.items():
            if run_name in specs_by_run:
                spec = specs_by_run[run_name]
                ranked_holdout.append(extract_payload(view, spec, spec.source_label, spec.mix_label))
            elif run_name == "05W_no_trend_strength_0001":
                ranked_holdout.append(extract_payload(view, None, "incumbent", "margin_only"))
            elif run_name == "05AI_trend_proxy_light_pb_0001":
                ranked_holdout.append(extract_payload(view, None, "light_pb", "margin_only"))
            elif run_name == "05AJ_trend_proxy_light_vb_0001":
                ranked_holdout.append(extract_payload(view, None, "light_vb", "margin_only"))

    review_payload = build_review_payload(
        ranked_validation=ranked_validation,
        ranked_holdout=ranked_holdout,
    )
    review_json_path = review_dir / "05BA_mt5_lightweight_proxy_logic_cross_review.json"
    review_md_path = review_dir / "05BA_mt5_lightweight_proxy_logic_cross_review.md"
    write_json(review_json_path, review_payload)
    write_text(review_md_path, build_review_markdown(review_payload))
    update_review_index(review_dir)

    print(f"[done] review_md={review_md_path}")
    print(f"[done] review_json={review_json_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
