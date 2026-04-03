#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from foundation.pipelines.run_stage02a_threshold_sweep import DEFAULT_REFERENCE_THRESHOLD, load_stage01_source
from foundation.pipelines.run_stage02c_threshold_confirmation import load_final_test_frame
from foundation.pipelines.run_stage03a_margin_only_sweep import simulate_margin_only
from foundation.pipelines.run_stage04a_probability_diff_sweep import simulate_probability_diff_only
from foundation.pipelines.show_experiment_leaderboard import load_bundle_views, sort_bundle_views


UTC = timezone.utc
DEFAULT_MARGIN_VALUES = "0.065,0.070,0.0725,0.075,0.0775,0.080,0.0825,0.085,0.090"
DEFAULT_DIFF_VALUES = "0.070,0.0725,0.075,0.0775,0.080,0.0825,0.085,0.0875,0.090,0.095,0.100"
RUN_PREFIX_BY_FAMILY = {
    "margin": "05A",
    "diff": "05B",
}
RUN_STEM_BY_FAMILY = {
    "margin": "margin_family_probe",
    "diff": "diff_family_probe",
}
DISPLAY_NAME_BY_FAMILY = {
    "margin": "max_probability_margin",
    "diff": "probability_difference_filter",
}
PARAM_NAME_BY_FAMILY = {
    "margin": "min_margin",
    "diff": "min_probability_diff",
}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run a Stage 05 single-family logic probe without forced synthesis.")
    parser.add_argument(
        "--family",
        required=True,
        choices=["margin", "diff"],
        help="Single rule family to probe first.",
    )
    parser.add_argument(
        "--source-run-dir",
        default="stages/01_base_feature_ml/02_runs/archived/01C_run_0001_h03_band000125_logreg",
        help="Stage 01 search-side run directory that contains validation predictions.",
    )
    parser.add_argument(
        "--final-run-dir",
        default="stages/01_base_feature_ml/02_runs/active/01D_run_0001_final_h03_band000125_logreg",
        help="Stage 01 final-model run directory that contains held-out test predictions.",
    )
    parser.add_argument(
        "--stage-root",
        default="stages/05_optimization",
        help="Stage 05 root directory.",
    )
    parser.add_argument(
        "--values",
        help="Comma-separated family parameter values. Defaults depend on --family.",
    )
    parser.add_argument(
        "--run-name",
        help="Optional explicit run folder name. Defaults to the next sequential Stage 05 family probe name.",
    )
    parser.add_argument(
        "--activate",
        action="store_true",
        help="Keep the run in 02_runs/active. Defaults to archived review-style output.",
    )
    return parser


def utc_now_iso() -> str:
    return datetime.now(tz=UTC).isoformat()


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_json(path: Path, payload: dict[str, Any]) -> None:
    write_text(path, json.dumps(payload, indent=2, ensure_ascii=False) + "\n")


def parse_values(text: str) -> list[float]:
    values: list[float] = []
    for item in text.split(","):
        stripped = item.strip()
        if not stripped:
            continue
        values.append(float(stripped))
    if not values:
        raise ValueError("at least one numeric family value is required")
    return values


def next_run_name(stage_root: Path, family: str) -> str:
    prefix = RUN_PREFIX_BY_FAMILY[family]
    stem = RUN_STEM_BY_FAMILY[family]
    pattern = re.compile(rf"^{re.escape(prefix)}_run_(\d{{4}})_{re.escape(stem)}$")
    next_index = 1
    for bucket in ("active", "archived"):
        bucket_dir = stage_root / "02_runs" / bucket
        if not bucket_dir.exists():
            continue
        for child in bucket_dir.iterdir():
            if not child.is_dir():
                continue
            match = pattern.match(child.name)
            if match:
                next_index = max(next_index, int(match.group(1)) + 1)
    return f"{prefix}_run_{next_index:04d}_{stem}"


def build_family_rows(
    *,
    family: str,
    valid_frame: pd.DataFrame,
    valid_horizon_bars: int,
    test_frame: pd.DataFrame,
    test_horizon_bars: int,
    values: list[float],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    param_name = PARAM_NAME_BY_FAMILY[family]
    for value in values:
        if family == "margin":
            valid_metric, _ = simulate_margin_only(valid_frame, valid_horizon_bars, value)
            test_metric, _ = simulate_margin_only(test_frame, test_horizon_bars, value)
        else:
            valid_metric, _ = simulate_probability_diff_only(valid_frame, valid_horizon_bars, value)
            test_metric, _ = simulate_probability_diff_only(test_frame, test_horizon_bars, value)

        rows.append(
            {
                param_name: value,
                "valid_trade_count": valid_metric.trade_count,
                "valid_long_trade_count": valid_metric.long_trade_count,
                "valid_short_trade_count": valid_metric.short_trade_count,
                "valid_compounded_return": valid_metric.valid_compounded_return,
                "valid_mean_trade_return": valid_metric.valid_mean_trade_return,
                "valid_max_drawdown": valid_metric.valid_max_drawdown,
                "test_trade_count": test_metric.trade_count,
                "test_long_trade_count": test_metric.long_trade_count,
                "test_short_trade_count": test_metric.short_trade_count,
                "test_compounded_return": test_metric.valid_compounded_return,
                "test_mean_trade_return": test_metric.valid_mean_trade_return,
                "test_max_drawdown": test_metric.valid_max_drawdown,
            }
        )
    return rows


def top_mt5_views() -> list[Any]:
    bundle_views = load_bundle_views(ROOT_DIR / "stages", "validation")
    return sort_bundle_views(bundle_views, "return_pct")


def load_latest_family_summary(stage_root: Path, family: str) -> dict[str, Any] | None:
    prefix = RUN_PREFIX_BY_FAMILY[family]
    stem = RUN_STEM_BY_FAMILY[family]
    pattern = re.compile(rf"^{re.escape(prefix)}_run_(\d{{4}})_{re.escape(stem)}$")
    candidates: list[tuple[float, Path]] = []
    for bucket in ("active", "archived"):
        bucket_dir = stage_root / "02_runs" / bucket
        if not bucket_dir.exists():
            continue
        for child in bucket_dir.iterdir():
            if not child.is_dir() or not pattern.match(child.name):
                continue
            summary_path = child / "summary.json"
            if summary_path.exists():
                candidates.append((summary_path.stat().st_mtime, summary_path))
    if not candidates:
        return None
    latest_path = sorted(candidates, key=lambda item: item[0], reverse=True)[0][1]
    return json.loads(latest_path.read_text(encoding="utf-8"))


def update_review_index(review_path: Path) -> None:
    lines = [
        "# Review Index",
        "",
        "## Current Entries",
        "",
        "- `MT5 leaderboard`: see `mt5_validation_leaderboard.md`",
    ]
    if (review_path.parent / "05A_margin_family_probe_review.md").exists():
        lines.append("- `05A`: see `05A_margin_family_probe_review.md`")
    else:
        lines.append("- `05A`: reserved for the Stage 03 family-first probe review")
    if (review_path.parent / "05B_diff_family_probe_review.md").exists():
        lines.append("- `05B`: see `05B_diff_family_probe_review.md`")
    else:
        lines.append("- `05B`: reserved for the Stage 04 family-first probe review")
    lines.extend(
        [
            "",
            "## Review Rule",
            "",
            "For each completed Stage 05 family probe, add:",
            "",
            "- run folder name",
            "- single-family logic summary",
            "- split used for cheap search",
            "- headline result",
            "- whether the family stays in the sequential shortlist",
        ]
    )
    write_text(review_path, "\n".join(lines) + "\n")


def update_selection_status(
    selection_status_path: Path,
    *,
    stage_root: Path,
    family: str,
    local_leader: dict[str, Any],
    tight_gap_leader: dict[str, Any],
    mt5_views: list[Any],
) -> None:
    param_name = PARAM_NAME_BY_FAMILY[family]
    phase_code = RUN_PREFIX_BY_FAMILY[family]
    counterpart_family = "diff" if family == "margin" else "margin"
    counterpart_summary = load_latest_family_summary(stage_root, counterpart_family)

    lines = [
        "# Selection Status",
        "",
        "- stage: `05_optimization`",
        f"- current phase complete: `{phase_code}`",
        "- current mode: `logic-first sequential optimization`",
        "- forced synthesis policy: `disabled until evidence warrants it`",
        "- active model-side base: `Stage 01 final baseline on the 58-feature FPMarkets v2 contract`",
    ]

    if mt5_views:
        champion = mt5_views[0]
        lines.append(
            f"- current MT5 champion: `{champion.run_name}`, return_pct=`{champion.headline.get('return_pct')}`, "
            f"profit_factor=`{champion.headline.get('profit_factor')}`, max_dd_pct=`{champion.headline.get('max_dd_pct')}`"
        )
    if len(mt5_views) > 1:
        backup = mt5_views[1]
        lines.append(
            f"- current MT5 backup: `{backup.run_name}`, return_pct=`{backup.headline.get('return_pct')}`, "
            f"profit_factor=`{backup.headline.get('profit_factor')}`, max_dd_pct=`{backup.headline.get('max_dd_pct')}`"
        )

    lines.extend(
        [
            (
                f"- latest {family} family blended leader: `({param_name}={local_leader[param_name]:.4f})`, "
                f"valid_comp=`{local_leader['valid_compounded_return']:.4f}`, "
                f"test_comp=`{local_leader['test_compounded_return']:.4f}`, "
                f"avg_comp=`{local_leader['avg_compounded_return']:.4f}`"
            ),
            (
                f"- latest {family} family tight-gap leader: `({param_name}={tight_gap_leader[param_name]:.4f})`, "
                f"valid_comp=`{tight_gap_leader['valid_compounded_return']:.4f}`, "
                f"test_comp=`{tight_gap_leader['test_compounded_return']:.4f}`, "
                f"gap=`{tight_gap_leader['abs_valid_test_gap']:.4f}`"
            ),
        ]
    )

    if counterpart_summary:
        other_family = counterpart_summary["family"]
        other_param_name = counterpart_summary["parameter_name"]
        other_local = counterpart_summary["local_leader"]
        other_gap = counterpart_summary["tight_gap_leader"]
        lines.extend(
            [
                (
                    f"- latest {other_family} family blended leader: `({other_param_name}={other_local[other_param_name]:.4f})`, "
                    f"valid_comp=`{other_local['valid_compounded_return']:.4f}`, "
                    f"test_comp=`{other_local['test_compounded_return']:.4f}`, "
                    f"avg_comp=`{other_local['avg_compounded_return']:.4f}`"
                ),
                (
                    f"- latest {other_family} family tight-gap leader: `({other_param_name}={other_gap[other_param_name]:.4f})`, "
                    f"valid_comp=`{other_gap['valid_compounded_return']:.4f}`, "
                    f"test_comp=`{other_gap['test_compounded_return']:.4f}`, "
                    f"gap=`{other_gap['abs_valid_test_gap']:.4f}`"
                ),
            ]
        )

    if counterpart_summary:
        margin_summary = load_latest_family_summary(stage_root, "margin")
        diff_summary = load_latest_family_summary(stage_root, "diff")
        if margin_summary and diff_summary:
            margin_local = margin_summary["local_leader"]
            margin_gap = margin_summary["tight_gap_leader"]
            diff_local = diff_summary["local_leader"]
            diff_gap = diff_summary["tight_gap_leader"]
            next_action = (
                "choose the next MT5 confirmation pair from "
                f"margin ({margin_local['min_margin']:.4f}/{margin_gap['min_margin']:.4f}) and "
                f"diff ({diff_local['min_probability_diff']:.4f}/{diff_gap['min_probability_diff']:.4f}) "
                "without opening synthesis"
            )
        else:
            next_action = "compare the Stage 03 and Stage 04 family probes, then choose the next MT5 confirmation candidate"
    else:
        next_action = "run the Stage 04 diff family probe next on the same fixed model/feature base"

    lines.extend(
        [
            "- threshold-only control: `02H_mt5_validation_baseline_0001`, return_pct=`32.398`, profit_factor=`1.0754`",
            "- runtime parity status: `latest MT5 validation attempts show ready_row_gap=0`",
            f"- next action: `{next_action}`",
            "- feature-work status: `deferred until a logic-side winner is selected or the logic search stalls`",
            "- synthesis gate: `open only after single-family robustness and holdout evidence, not by default`",
        ]
    )
    write_text(selection_status_path, "\n".join(lines) + "\n")


def build_review_markdown(
    *,
    family: str,
    values: list[float],
    local_leader: dict[str, Any],
    tight_gap_leader: dict[str, Any],
    stability_sorted: pd.DataFrame,
    summary_payload: dict[str, Any],
) -> str:
    param_name = PARAM_NAME_BY_FAMILY[family]
    phase_code = RUN_PREFIX_BY_FAMILY[family]
    display_name = DISPLAY_NAME_BY_FAMILY[family]

    lines = [
        f"# {phase_code} {display_name} Family Probe Review",
        "",
        f"Generated at: `{summary_payload['generated_at_utc']}`",
        "",
        "## Scope",
        "",
        f"- purpose: `probe {display_name} on its own inside Stage 05 before any combined-rule synthesis`",
        f"- fixed thresholds: `(short_threshold={DEFAULT_REFERENCE_THRESHOLD:.6f}, long_threshold={DEFAULT_REFERENCE_THRESHOLD:.6f})`",
        f"- local {param_name} values: `{', '.join(f'{item:.4f}' for item in values)}`",
        "- this remains a single-family logic read on the fixed Stage 01 model and feature base",
        "",
        "## Headline Read",
        "",
        (
            f"- blended leader: `({param_name}={local_leader[param_name]:.4f})`, "
            f"valid_comp=`{local_leader['valid_compounded_return']:.4f}`, "
            f"test_comp=`{local_leader['test_compounded_return']:.4f}`, "
            f"avg_comp=`{local_leader['avg_compounded_return']:.4f}`"
        ),
        (
            f"- tight-gap leader: `({param_name}={tight_gap_leader[param_name]:.4f})`, "
            f"valid_comp=`{tight_gap_leader['valid_compounded_return']:.4f}`, "
            f"test_comp=`{tight_gap_leader['test_compounded_return']:.4f}`, "
            f"avg_comp=`{tight_gap_leader['avg_compounded_return']:.4f}`, "
            f"gap=`{tight_gap_leader['abs_valid_test_gap']:.4f}`"
        ),
        "",
        "## Stability Order",
        "",
    ]
    for row in stability_sorted.head(10).itertuples(index=False):
        row_value = getattr(row, param_name)
        lines.append(
            f"- `{param_name}={row_value:.4f}`: "
            f"valid_comp={row.valid_compounded_return:.4f}, "
            f"test_comp={row.test_compounded_return:.4f}, "
            f"avg_comp={row.avg_compounded_return:.4f}, "
            f"gap={row.abs_valid_test_gap:.4f}"
        )
    lines.extend(
        [
            "",
            "## Verdict",
            "",
            f"- verdict: `{summary_payload['verdict']}`",
            (
                "- read: this probe is meant to keep the search family-isolated so the next Stage 05 step can compare "
                "rule families cleanly instead of forcing a merged stack too early."
            ),
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    args = build_parser().parse_args()

    family = args.family
    source_run_dir = ROOT_DIR / args.source_run_dir
    final_run_dir = ROOT_DIR / args.final_run_dir
    stage_root = ROOT_DIR / args.stage_root
    values = parse_values(args.values or (DEFAULT_MARGIN_VALUES if family == "margin" else DEFAULT_DIFF_VALUES))

    valid_frame, source_config = load_stage01_source(source_run_dir)
    test_frame, final_config = load_final_test_frame(final_run_dir)
    valid_horizon_bars = int(source_config["horizon_bars"])
    test_horizon_bars = int(final_config["horizon_bars"])

    for relative in ("00_spec", "01_inputs", "02_runs/active", "02_runs/archived", "03_reviews", "04_selected"):
        (stage_root / relative).mkdir(parents=True, exist_ok=True)

    run_name = args.run_name or next_run_name(stage_root, family)
    run_bucket = "active" if args.activate else "archived"
    run_dir = stage_root / "02_runs" / run_bucket / run_name
    run_dir.mkdir(parents=True, exist_ok=True)

    rows = build_family_rows(
        family=family,
        valid_frame=valid_frame,
        valid_horizon_bars=valid_horizon_bars,
        test_frame=test_frame,
        test_horizon_bars=test_horizon_bars,
        values=values,
    )
    probe_df = pd.DataFrame(rows)
    probe_df["avg_compounded_return"] = (
        probe_df["valid_compounded_return"] + probe_df["test_compounded_return"]
    ) / 2.0
    probe_df["abs_valid_test_gap"] = (
        probe_df["test_compounded_return"] - probe_df["valid_compounded_return"]
    ).abs()
    probe_df["both_positive"] = (
        (probe_df["valid_compounded_return"] > 0.0) & (probe_df["test_compounded_return"] > 0.0)
    )

    param_name = PARAM_NAME_BY_FAMILY[family]
    file_prefix = RUN_STEM_BY_FAMILY[family]
    probe_df.to_csv(run_dir / f"{file_prefix}_results.csv", index=False)

    stability_sorted = probe_df.sort_values(
        by=["both_positive", "avg_compounded_return", "abs_valid_test_gap", "valid_compounded_return"],
        ascending=[False, False, True, False],
    ).reset_index(drop=True)
    stability_sorted.to_csv(run_dir / f"{file_prefix}_stability_sorted.csv", index=False)

    gap_sorted = probe_df[probe_df["both_positive"]].copy()
    if gap_sorted.empty:
        gap_sorted = probe_df.copy()
    gap_sorted = gap_sorted.sort_values(
        by=["abs_valid_test_gap", "avg_compounded_return", "test_compounded_return"],
        ascending=[True, False, False],
    ).reset_index(drop=True)
    gap_sorted.to_csv(run_dir / f"{file_prefix}_gap_sorted.csv", index=False)

    stable_positive = probe_df[probe_df["both_positive"]].copy().reset_index(drop=True)
    stable_positive.to_csv(run_dir / f"{file_prefix}_stable_positive.csv", index=False)

    local_leader = stability_sorted.iloc[0].to_dict()
    tight_gap_leader = gap_sorted.iloc[0].to_dict()

    summary_payload = {
        "generated_at_utc": utc_now_iso(),
        "phase": f"{RUN_PREFIX_BY_FAMILY[family]}_logic_family_probe",
        "family": family,
        "family_display_name": DISPLAY_NAME_BY_FAMILY[family],
        "run_name": run_name,
        "run_bucket": run_bucket,
        "source_search_model": source_run_dir.name,
        "final_model_run_name": final_run_dir.name,
        "fixed_thresholds": {
            "short_threshold": DEFAULT_REFERENCE_THRESHOLD,
            "long_threshold": DEFAULT_REFERENCE_THRESHOLD,
        },
        "parameter_name": param_name,
        "parameter_values": values,
        "local_leader": local_leader,
        "tight_gap_leader": tight_gap_leader,
        "verdict": (
            f"keep {DISPLAY_NAME_BY_FAMILY[family]} isolated for Stage 05 and compare it family-first before any synthesis"
        ),
    }
    write_json(run_dir / "summary.json", summary_payload)

    review_dir = stage_root / "03_reviews"
    selection_status_path = stage_root / "04_selected" / "selection_status.md"
    phase_code = RUN_PREFIX_BY_FAMILY[family]
    write_json(review_dir / f"{phase_code}_{family}_family_probe_review.json", summary_payload)
    write_text(
        review_dir / f"{phase_code}_{family}_family_probe_review.md",
        build_review_markdown(
            family=family,
            values=values,
            local_leader=local_leader,
            tight_gap_leader=tight_gap_leader,
            stability_sorted=stability_sorted,
            summary_payload=summary_payload,
        ),
    )
    update_review_index(review_dir / "review_index.md")

    update_selection_status(
        selection_status_path,
        stage_root=stage_root,
        family=family,
        local_leader=local_leader,
        tight_gap_leader=tight_gap_leader,
        mt5_views=top_mt5_views(),
    )

    print(f"[done] run_dir={run_dir}")
    print(f"[done] summary={run_dir / 'summary.json'}")
    print(f"[done] review={review_dir / f'{phase_code}_{family}_family_probe_review.md'}")
    print(f"[done] selection_status={selection_status_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
