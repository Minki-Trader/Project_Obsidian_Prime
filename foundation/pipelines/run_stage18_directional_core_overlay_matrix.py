#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import string
import sys
import traceback
from dataclasses import dataclass
from pathlib import Path
from typing import Any

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from foundation.pipelines.experiment_bundle_models import ExperimentBundle
from foundation.pipelines.run_stage06_direction_split_segmented_overlay import (
    build_cross_segment_summary,
    build_segment_results,
    format_metric,
    load_attempt_summaries,
    utc_now_iso,
    write_json,
    write_text,
)
from foundation.pipelines.run_stage06_early_wfo_lp_compare import parse_utc, wfo_segment_scheme
from foundation.pipelines.run_stage06_pre_risk_pool_batch import prepare_overlay_bundle, run_tester


STAGE18_ROOT = ROOT_DIR / "stages" / "18_directional_core_overlay_matrix"
STAGE17_ROOT = ROOT_DIR / "stages" / "17_09c_directional_core_fork" / "02_runs" / "active"
WINDOW_TOKENS = ["2401", "2407", "2501"]
TARGET_WINDOW_TOKEN = "2407"
TARGET_SEGMENT = "holdout_b"


@dataclass(frozen=True)
class CoreSpec:
    stage_id: str
    base_name: str
    label: str
    rationale: str


@dataclass(frozen=True)
class OverlaySpec:
    token: str
    label: str
    description: str
    risk_pct: float
    runtime_extra: dict[str, Any]


@dataclass(frozen=True)
class MatrixVariant:
    stage_id: str
    core: CoreSpec
    overlay: OverlaySpec

    @property
    def label(self) -> str:
        return f"{self.core.stage_id}_{self.overlay.label}"

    @property
    def description(self) -> str:
        return f"{self.core.label} + {self.overlay.description}"

    @property
    def token(self) -> str:
        return f"{self.core.stage_id.lower()}_{self.overlay.token.lower()}"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run a broad strict-WFO overlay matrix on top of the Stage 17 directional cores."
    )
    parser.add_argument("--stage-root", default=str(STAGE18_ROOT), help="Stage 18 root directory.")
    parser.add_argument("--source-root", default=str(STAGE17_ROOT), help="Stage 17 active run root.")
    parser.add_argument("--batch-id", default="18MX", help="Stage 18 batch id.")
    parser.add_argument("--stop-atr-period", type=int, default=14, help="ATR period.")
    parser.add_argument("--stop-long-atr-mult", type=float, default=1.4, help="Long ATR multiplier.")
    parser.add_argument("--stop-short-atr-mult", type=float, default=2.0, help="Short ATR multiplier.")
    parser.add_argument(
        "--review-basename",
        default="18MX_directional_core_overlay_matrix_review",
        help="Review basename written under 03_reviews.",
    )
    parser.add_argument("--rebuild-bundle", action="store_true", help="Force bundle rebuild.")
    return parser


def stage18_paths(stage_root: Path, batch_id: str) -> dict[str, Path]:
    slug = f"{batch_id.lower()}_directional_core_overlay_matrix"
    review_dir = stage_root / "03_reviews"
    return {
        "spec": stage_root / "00_spec" / "stage_brief.md",
        "inputs": stage_root / "01_inputs" / "input_manifest.json",
        "review_index": review_dir / "review_index.md",
        "selection": stage_root / "04_selected" / "selection_status.md",
        "status_json": review_dir / f"{slug}_status.json",
        "status_md": review_dir / f"{slug}_status.md",
        "review_json": review_dir / f"{slug}_review.json",
        "review_md": review_dir / f"{slug}_review.md",
    }


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def build_cores() -> list[CoreSpec]:
    return [
        CoreSpec(
            stage_id="17E",
            base_name="ovr_balanced",
            label="09C_ovr_balanced",
            rationale="Current directional-core leader with 3/3 positive test windows.",
        ),
        CoreSpec(
            stage_id="17C",
            base_name="short_specialist",
            label="09C_short_specialist",
            rationale="Aggressive short-side specialist that uniquely flips 2407 holdout_b positive.",
        ),
        CoreSpec(
            stage_id="17D",
            base_name="flat_guard",
            label="09C_flat_guard",
            rationale="Abstention-heavy core that improves 2407 holdout_b without directional specialization.",
        ),
    ]


def build_overlays() -> list[OverlaySpec]:
    return [
        OverlaySpec(
            token="PLAIN20",
            label="plain_core",
            description="Plain directional core with no extra session overlay at 2.0% risk.",
            risk_pct=2.0,
            runtime_extra={"session_overlay_label": "plain_core"},
        ),
        OverlaySpec(
            token="SD20",
            label="soft_decay",
            description="06D-style soft session decay at 2.0% risk.",
            risk_pct=2.0,
            runtime_extra={
                "monday_risk_pct_mult": 0.75,
                "ny_postcash_risk_pct_mult": 0.70,
                "session_overlay_label": "soft_decay",
            },
        ),
        OverlaySpec(
            token="LP20",
            label="local_probe_b",
            description="LP02-style stronger Monday and post-cash decay at 2.0% risk.",
            risk_pct=2.0,
            runtime_extra={
                "monday_risk_pct_mult": 0.70,
                "ny_postcash_risk_pct_mult": 0.65,
                "session_overlay_label": "local_probe_b",
            },
        ),
        OverlaySpec(
            token="BD20",
            label="balanced_micro",
            description="13D-style balanced Monday/post-cash micro overlay at 2.0% risk.",
            risk_pct=2.0,
            runtime_extra={
                "monday_risk_pct_mult": 0.575,
                "ny_postcash_risk_pct_mult": 0.6125,
                "session_overlay_label": "balanced_micro",
            },
        ),
        OverlaySpec(
            token="PH20",
            label="postcash_hold_cut",
            description="Soft decay plus post-cash hold cut to 3 bars at 2.0% risk.",
            risk_pct=2.0,
            runtime_extra={
                "monday_risk_pct_mult": 0.75,
                "ny_postcash_risk_pct_mult": 0.70,
                "ny_postcash_hold_cap_bars": 3,
                "session_overlay_label": "postcash_hold_cut",
            },
        ),
        OverlaySpec(
            token="CT20",
            label="clock_taper",
            description="Gradual NY clock taper instead of a single hard post-cash multiplier at 2.0% risk.",
            risk_pct=2.0,
            runtime_extra={
                "monday_risk_pct_mult": 0.75,
                "ny_postcash_risk_pct_mult": 1.0,
                "ny_clock_taper_start_minute": 930,
                "ny_clock_taper_mid_minute": 960,
                "ny_clock_taper_late_minute": 1080,
                "ny_clock_taper_start_mult": 0.90,
                "ny_clock_taper_mid_mult": 0.75,
                "ny_clock_taper_late_mult": 0.60,
                "session_overlay_label": "clock_taper",
            },
        ),
    ]


def build_variants(cores: list[CoreSpec], overlays: list[OverlaySpec]) -> list[MatrixVariant]:
    letters = iter(string.ascii_uppercase)
    variants: list[MatrixVariant] = []
    for core in cores:
        for overlay in overlays:
            variants.append(MatrixVariant(stage_id=f"18{next(letters)}", core=core, overlay=overlay))
    return variants


def ensure_stage_scaffold(
    stage_root: Path,
    paths: dict[str, Path],
    args: argparse.Namespace,
    cores: list[CoreSpec],
    overlays: list[OverlaySpec],
    variants: list[MatrixVariant],
) -> None:
    (stage_root / "02_runs" / "active").mkdir(parents=True, exist_ok=True)
    (stage_root / "02_runs" / "archived").mkdir(parents=True, exist_ok=True)
    (stage_root / "03_reviews").mkdir(parents=True, exist_ok=True)
    (stage_root / "04_selected").mkdir(parents=True, exist_ok=True)

    if not paths["spec"].exists():
        write_text(
            paths["spec"],
            "\n".join(
                [
                    "# Stage Brief",
                    "",
                    "- stage: `18_directional_core_overlay_matrix`",
                    "- goal: `scale out practical session/risk overlays across the new Stage 17 directional cores instead of continuing narrow micro-probes`",
                    "- source cores: `17E ovr_balanced`, `17C short_specialist`, `17D flat_guard`",
                    "- windows: `2401, 2407, 2501`",
                    "- ranking basis: `positive_test_windows -> positive_holdout_b_windows -> avg_test_return -> target_2407_holdout_b -> min_holdout_b -> avg_test_pf`",
                    "- broad matrix: `plain, soft_decay, LP02, 13D-balanced, postcash_hold_cut, clock_taper`",
                    "",
                ]
            ),
        )

    manifest = {
        "generated_at_utc": utc_now_iso(),
        "stage": "18_directional_core_overlay_matrix",
        "phase": args.batch_id,
        "source_stage": "17_09c_directional_core_fork",
        "source_root": str(Path(args.source_root).resolve()),
        "windows": WINDOW_TOKENS,
        "target_window_token": TARGET_WINDOW_TOKEN,
        "target_segment": TARGET_SEGMENT,
        "overlay_defaults": {
            "sizing_mode": "risk_pct",
            "capital_base": "balance",
            "stop_model": "atr",
            "stop_execution_mode": "broker_native",
            "stop_policy": "direction_split",
            "stop_long_atr_mult": args.stop_long_atr_mult,
            "stop_short_atr_mult": args.stop_short_atr_mult,
            "stop_atr_period": args.stop_atr_period,
        },
        "cores": [core.__dict__ for core in cores],
        "overlays": [
            {
                "token": overlay.token,
                "label": overlay.label,
                "description": overlay.description,
                "risk_pct": overlay.risk_pct,
                "runtime_extra": overlay.runtime_extra,
            }
            for overlay in overlays
        ],
        "variants": [
            {
                "stage_id": variant.stage_id,
                "label": variant.label,
                "description": variant.description,
                "core_stage_id": variant.core.stage_id,
                "overlay_token": variant.overlay.token,
                "risk_pct": variant.overlay.risk_pct,
                "runtime_extra": variant.overlay.runtime_extra,
            }
            for variant in variants
        ],
    }
    write_json(paths["inputs"], manifest)

    if not paths["review_index"].exists():
        write_text(paths["review_index"], "# Review Index\n\n## Current Entries\n\n- `18MX`: pending\n")

    if not paths["selection"].exists():
        write_text(
            paths["selection"],
            "\n".join(
                [
                    "# Selection Status",
                    "",
                    "- stage: `18_directional_core_overlay_matrix`",
                    "- status: `running`",
                    "- active source leader: `17E` `09C_ovr_balanced`",
                    "- objective: `see whether a broader practical overlay/risk matrix can convert the new Stage 17 core edge into a stronger and more practical strict-WFO profile`",
                    "",
                ]
            ),
        )


def source_run_dir(source_root: Path, core: CoreSpec, window_token: str) -> Path:
    return source_root / f"{core.stage_id}_{window_token}_{core.base_name}_0001"


def build_source_item(source_dir: Path) -> dict[str, Any]:
    source_dir = source_dir.resolve()
    return {
        "stage_id": source_dir.name.split("_", 1)[0],
        "run_name": source_dir.name,
        "path": source_dir,
        "has_bundle": (source_dir / "experiment_bundle.json").exists(),
        "has_config": (source_dir / "config.json").exists(),
        "has_model_joblib": (source_dir / "model.joblib").exists(),
        "has_rule_stack": (source_dir / "rule_stack.json").exists(),
    }


def variant_run_name(variant: MatrixVariant, window_token: str) -> str:
    return f"{variant.stage_id}_{window_token}_{variant.token}_0001"


def ensure_bundle(
    *,
    source_item: dict[str, Any],
    run_dir: Path,
    run_name: str,
    experiment_id: str,
    variant: MatrixVariant,
    args: argparse.Namespace,
) -> Path:
    bundle_path, _ = prepare_overlay_bundle(
        source_item=source_item,
        run_dir=run_dir,
        run_name=run_name,
        experiment_id=experiment_id,
        batch_id=args.batch_id,
        risk_pct=variant.overlay.risk_pct,
        stop_long_atr_mult=args.stop_long_atr_mult,
        stop_short_atr_mult=args.stop_short_atr_mult,
        stop_atr_period=args.stop_atr_period,
        rebuild_bundle=args.rebuild_bundle,
    )

    bundle = ExperimentBundle.from_json(bundle_path.read_text(encoding="utf-8-sig"))
    for key, value in variant.overlay.runtime_extra.items():
        bundle.runtime_snapshot.extra[key] = value
    bundle.compatibility.bundle_integrity_hash = hashlib.sha256(
        bundle.canonical_core_json().encode("utf-8")
    ).hexdigest()
    bundle_path.write_text(bundle.to_json(indent=2), encoding="utf-8")

    write_json(
        run_dir / "overlay_manifest.json",
        {
            "generated_at_utc": utc_now_iso(),
            "run_name": run_name,
            "experiment_id": experiment_id,
            "source_run_dir": str(source_item["path"]),
            "source_run_name": source_item["run_name"],
            "source_core_stage_id": variant.core.stage_id,
            "source_core_label": variant.core.label,
            "overlay_token": variant.overlay.token,
            "overlay_label": variant.overlay.label,
            "overlay": {
                "risk_pct": variant.overlay.risk_pct,
                "stop_policy": "direction_split",
                "stop_long_atr_mult": args.stop_long_atr_mult,
                "stop_short_atr_mult": args.stop_short_atr_mult,
                "stop_atr_period": args.stop_atr_period,
                **variant.overlay.runtime_extra,
            },
        },
    )
    return bundle_path


def build_run_payload(
    *,
    run_dir: Path,
    source_payload: dict[str, Any],
    variant: MatrixVariant,
    window_token: str,
    segment_scheme: dict[str, list[tuple[str, Any, Any]]],
) -> dict[str, Any]:
    bundle = ExperimentBundle.from_json((run_dir / "experiment_bundle.json").read_text(encoding="utf-8-sig"))
    summaries = load_attempt_summaries(run_dir)
    if "validation" not in summaries or "test" not in summaries:
        raise FileNotFoundError(f"missing validation/test summaries in {run_dir}")

    segmented_results = {
        "validation": build_segment_results(bundle, "validation", summaries["validation"], scheme=segment_scheme),
        "test": build_segment_results(bundle, "test", summaries["test"], scheme=segment_scheme),
    }

    def delta(split_name: str, layer: str, metric_name: str) -> float:
        new_value = bundle.results.by_split[split_name].model_dump()[layer].get(metric_name) or 0.0
        base_value = source_payload["split_runs"][split_name][layer].get(metric_name) or 0.0
        return float(new_value - base_value)

    return {
        "generated_at_utc": utc_now_iso(),
        "stage": "18_directional_core_overlay_matrix",
        "phase": "18MX_directional_core_overlay_matrix",
        "run_name": run_dir.name,
        "source_run_name": source_payload["run_name"],
        "source_candidate_stage_id": source_payload["candidate_stage_id"],
        "source_candidate_label": source_payload["candidate_label"],
        "window_token": window_token,
        "variant_stage_id": variant.stage_id,
        "core_stage_id": variant.core.stage_id,
        "core_label": variant.core.label,
        "overlay_token": variant.overlay.token,
        "overlay_label": variant.overlay.label,
        "label": variant.label,
        "description": variant.description,
        "overlay": {
            "risk_pct": bundle.runtime_snapshot.risk_pct,
            "stop_execution_mode": bundle.runtime_snapshot.stop_execution_mode,
            "stop_policy": bundle.runtime_snapshot.stop_policy,
            "stop_long_atr_mult": bundle.runtime_snapshot.stop_long_atr_mult,
            "stop_short_atr_mult": bundle.runtime_snapshot.stop_short_atr_mult,
            "stop_atr_period": bundle.runtime_snapshot.stop_atr_period,
            **variant.overlay.runtime_extra,
        },
        "source_split_runs": source_payload["split_runs"],
        "split_runs": {
            "validation": bundle.results.by_split["validation"].model_dump(),
            "test": bundle.results.by_split["test"].model_dump(),
        },
        "segmented_results": segmented_results,
        "cross_segment_summary": build_cross_segment_summary(segmented_results),
        "delta_vs_source": {
            "validation": {
                "return_pct": delta("validation", "headline", "return_pct"),
                "profit_factor": delta("validation", "headline", "profit_factor"),
                "max_dd_pct": delta("validation", "headline", "max_dd_pct"),
                "ulcer_index": delta("validation", "risk", "ulcer_index"),
            },
            "test": {
                "return_pct": delta("test", "headline", "return_pct"),
                "profit_factor": delta("test", "headline", "profit_factor"),
                "max_dd_pct": delta("test", "headline", "max_dd_pct"),
                "ulcer_index": delta("test", "risk", "ulcer_index"),
            },
        },
    }


def segment_metric(payload: dict[str, Any], split_name: str, segment_name: str, metric_name: str) -> float:
    segments = payload["segmented_results"][split_name]["segments"]
    segment = next(item for item in segments if str(item.get("segment") or "") == segment_name)
    return float(segment["headline"].get(metric_name) or 0.0)


def aggregate_variants(payloads: list[dict[str, Any]], variants: list[MatrixVariant]) -> list[dict[str, Any]]:
    by_variant = {variant.stage_id: [] for variant in variants}
    variant_by_id = {variant.stage_id: variant for variant in variants}
    for payload in payloads:
        by_variant[payload["variant_stage_id"]].append(payload)

    rows: list[dict[str, Any]] = []
    for stage_id, runs in by_variant.items():
        if not runs:
            continue
        variant = variant_by_id[stage_id]
        target_run = next(run for run in runs if run["window_token"] == TARGET_WINDOW_TOKEN)
        holdout_b_returns = [segment_metric(run, "test", "holdout_b", "return_pct") for run in runs]
        test_returns = [float(run["split_runs"]["test"]["headline"].get("return_pct") or 0.0) for run in runs]
        test_pfs = [float(run["split_runs"]["test"]["headline"].get("profit_factor") or 0.0) for run in runs]
        rows.append(
            {
                "stage_id": variant.stage_id,
                "core_stage_id": variant.core.stage_id,
                "core_label": variant.core.label,
                "overlay_token": variant.overlay.token,
                "overlay_label": variant.overlay.label,
                "risk_pct": variant.overlay.risk_pct,
                "label": variant.label,
                "description": variant.description,
                "target_holdout_b_return_pct": segment_metric(target_run, "test", TARGET_SEGMENT, "return_pct"),
                "target_holdout_b_profit_factor": segment_metric(target_run, "test", TARGET_SEGMENT, "profit_factor"),
                "target_test_return_pct": float(target_run["split_runs"]["test"]["headline"].get("return_pct") or 0.0),
                "target_test_profit_factor": float(target_run["split_runs"]["test"]["headline"].get("profit_factor") or 0.0),
                "min_holdout_b_return_pct": float(min(holdout_b_returns)),
                "avg_holdout_b_return_pct": float(sum(holdout_b_returns) / len(holdout_b_returns)),
                "min_test_return_pct": float(min(test_returns)),
                "avg_test_return_pct": float(sum(test_returns) / len(test_returns)),
                "avg_test_profit_factor": float(sum(test_pfs) / len(test_pfs)),
                "positive_test_windows": int(sum(value > 0.0 for value in test_returns)),
                "positive_holdout_b_windows": int(sum(value > 0.0 for value in holdout_b_returns)),
                "per_window": [
                    {
                        "window_token": run["window_token"],
                        "test_return_pct": float(run["split_runs"]["test"]["headline"].get("return_pct") or 0.0),
                        "test_profit_factor": float(run["split_runs"]["test"]["headline"].get("profit_factor") or 0.0),
                        "holdout_b_return_pct": segment_metric(run, "test", "holdout_b", "return_pct"),
                        "holdout_b_profit_factor": segment_metric(run, "test", "holdout_b", "profit_factor"),
                        "test_delta_return_pct": float(run["delta_vs_source"]["test"]["return_pct"]),
                        "test_delta_profit_factor": float(run["delta_vs_source"]["test"]["profit_factor"]),
                    }
                    for run in sorted(runs, key=lambda item: item["window_token"])
                ],
            }
        )

    rows.sort(
        key=lambda row: (
            int(row["positive_test_windows"]),
            int(row["positive_holdout_b_windows"]),
            float(row["avg_test_return_pct"]),
            float(row["target_holdout_b_return_pct"]),
            float(row["min_holdout_b_return_pct"]),
            float(row["avg_test_profit_factor"]),
        ),
        reverse=True,
    )
    for rank, row in enumerate(rows, start=1):
        row["rank"] = rank
    return rows


def build_review_markdown(rows: list[dict[str, Any]], cores: list[CoreSpec], overlays: list[OverlaySpec]) -> str:
    core_leaders: dict[str, dict[str, Any]] = {}
    for core in cores:
        matches = [row for row in rows if row["core_stage_id"] == core.stage_id]
        if matches:
            core_leaders[core.stage_id] = matches[0]

    overlay_leaders: dict[str, dict[str, Any]] = {}
    for overlay in overlays:
        matches = [row for row in rows if row["overlay_token"] == overlay.token]
        if matches:
            overlay_leaders[overlay.token] = matches[0]

    lines = [
        "# Stage 18 Directional Core Overlay Matrix Review",
        "",
        "- source stage: `17_09c_directional_core_fork`",
        "- source cores: `17E ovr_balanced`, `17C short_specialist`, `17D flat_guard`",
        "- windows: `2401, 2407, 2501`",
        "- ranking basis: `positive_test_windows -> positive_holdout_b_windows -> avg_test_return -> target_2407_holdout_b -> min_holdout_b -> avg_test_pf`",
        f"- total variants: `{len(rows)}`",
        "",
        "## Core Leaders",
        "",
    ]
    for core in cores:
        leader = core_leaders.get(core.stage_id)
        if leader is None:
            continue
        lines.append(
            f"- `{core.stage_id}` `{core.label}` -> best `{leader['stage_id']}` `{leader['overlay_label']}`: "
            f"avg_test=`{format_metric(leader['avg_test_return_pct'], 3)}`, "
            f"target_holdout_b=`{format_metric(leader['target_holdout_b_return_pct'], 3)}`, "
            f"min_holdout_b=`{format_metric(leader['min_holdout_b_return_pct'], 3)}`, "
            f"positive_test_windows=`{leader['positive_test_windows']}/3`, "
            f"positive_holdout_b_windows=`{leader['positive_holdout_b_windows']}/3`"
        )

    lines.extend(["", "## Overlay Readout", ""])
    for overlay in overlays:
        leader = overlay_leaders.get(overlay.token)
        if leader is None:
            continue
        lines.append(
            f"- `{overlay.token}` `{overlay.label}` -> best core `{leader['core_stage_id']}`: "
            f"avg_test=`{format_metric(leader['avg_test_return_pct'], 3)}`, "
            f"target_holdout_b=`{format_metric(leader['target_holdout_b_return_pct'], 3)}`, "
            f"min_holdout_b=`{format_metric(leader['min_holdout_b_return_pct'], 3)}`"
        )

    lines.extend(["", "## Variant Ranking", ""])
    for row in rows:
        lines.append(
            f"- [{row['rank']}] `{row['stage_id']}` `{row['core_stage_id']} + {row['overlay_token']}`: "
            f"avg_test=`{format_metric(row['avg_test_return_pct'], 3)}`, "
            f"min_test=`{format_metric(row['min_test_return_pct'], 3)}`, "
            f"target_holdout_b=`{format_metric(row['target_holdout_b_return_pct'], 3)}`, "
            f"min_holdout_b=`{format_metric(row['min_holdout_b_return_pct'], 3)}`, "
            f"avg_test_PF=`{format_metric(row['avg_test_profit_factor'], 4)}`, "
            f"positive_test_windows=`{row['positive_test_windows']}/3`, "
            f"positive_holdout_b_windows=`{row['positive_holdout_b_windows']}/3`"
        )
        for window_row in row["per_window"]:
            lines.append(
                f"  - `{window_row['window_token']}`: test=`{format_metric(window_row['test_return_pct'], 3)}`, "
                f"PF=`{format_metric(window_row['test_profit_factor'], 4)}`, "
                f"holdout_b=`{format_metric(window_row['holdout_b_return_pct'], 3)}`, "
                f"holdout_b_PF=`{format_metric(window_row['holdout_b_profit_factor'], 4)}`, "
                f"delta_test=`{format_metric(window_row['test_delta_return_pct'], 3)}`, "
                f"delta_PF=`{format_metric(window_row['test_delta_profit_factor'], 4)}`"
            )
        lines.append("")

    if rows:
        leader = rows[0]
        lines.extend(
            [
                "## Readout",
                "",
                f"- overall leader: `{leader['stage_id']}` `{leader['core_stage_id']} + {leader['overlay_token']}`",
                f"- leader avg_test: `{format_metric(leader['avg_test_return_pct'], 3)}`",
                f"- leader target_2407_holdout_b: `{format_metric(leader['target_holdout_b_return_pct'], 3)}`",
                f"- leader min_holdout_b: `{format_metric(leader['min_holdout_b_return_pct'], 3)}`",
                "",
            ]
        )
    return "\n".join(lines)


def update_review_index(review_index_path: Path, review_name: str) -> None:
    lines = review_index_path.read_text(encoding="utf-8").splitlines() if review_index_path.exists() else []
    if not lines:
        lines = ["# Review Index", "", "## Current Entries"]
    if "## Current Entries" not in lines:
        lines.extend(["", "## Current Entries"])
    entry = f"- `18MX`: see `{review_name}`"
    if entry not in lines:
        lines.append(entry)
    write_text(review_index_path, "\n".join(lines).rstrip() + "\n")


def update_selection_status(selection_path: Path, rows: list[dict[str, Any]], cores: list[CoreSpec]) -> None:
    lines = [
        "# Selection Status",
        "",
        "- stage: `18_directional_core_overlay_matrix`",
        "- status: `completed`",
    ]
    if rows:
        leader = rows[0]
        lines.extend(
            [
                f"- overall leader: `{leader['stage_id']}` `{leader['core_stage_id']} + {leader['overlay_token']}`",
                f"- leader basis: `avg_test={format_metric(leader['avg_test_return_pct'], 3)}, target_2407_holdout_b={format_metric(leader['target_holdout_b_return_pct'], 3)}, min_holdout_b={format_metric(leader['min_holdout_b_return_pct'], 3)}, positive_test_windows={leader['positive_test_windows']}/3, positive_holdout_b_windows={leader['positive_holdout_b_windows']}/3`",
            ]
        )
    lines.append("- per-core leaders:")
    for core in cores:
        matches = [row for row in rows if row["core_stage_id"] == core.stage_id]
        if not matches:
            continue
        row = matches[0]
        lines.append(
            f"  - `{core.stage_id}` -> `{row['stage_id']}` `{row['overlay_token']}` `avg_test={format_metric(row['avg_test_return_pct'], 3)}`, `target_2407_holdout_b={format_metric(row['target_holdout_b_return_pct'], 3)}`"
        )
    lines.extend(
        [
            "- next action: `decide whether the best Stage 18 practical overlay should replace plain 17E as the new operating reference, or whether 17C/17D should stay as regime specialists only`",
            "",
        ]
    )
    write_text(selection_path, "\n".join(lines))


def build_status_payload(
    *,
    stage_root: Path,
    variants: list[MatrixVariant],
    payloads: list[dict[str, Any]],
    failures: list[dict[str, Any]],
    current_run: str | None,
) -> dict[str, Any]:
    total_runs = len(variants) * len(WINDOW_TOKENS)
    completed_runs = len(payloads)
    failed_runs = len(failures)
    pending_runs = max(total_runs - completed_runs - failed_runs, 0)
    return {
        "generated_at_utc": utc_now_iso(),
        "stage": "18_directional_core_overlay_matrix",
        "phase": "18MX_directional_core_overlay_matrix",
        "stage_root": str(stage_root),
        "total_runs": total_runs,
        "completed_runs": completed_runs,
        "failed_runs": failed_runs,
        "pending_runs": pending_runs,
        "current_run": current_run,
        "completed_run_names": [payload["run_name"] for payload in payloads[-10:]],
        "failures": failures[-10:],
    }


def build_status_markdown(status: dict[str, Any]) -> str:
    lines = [
        "# Stage 18 Status",
        "",
        f"- generated_at_utc: `{status['generated_at_utc']}`",
        f"- total_runs: `{status['total_runs']}`",
        f"- completed_runs: `{status['completed_runs']}`",
        f"- failed_runs: `{status['failed_runs']}`",
        f"- pending_runs: `{status['pending_runs']}`",
        f"- current_run: `{status['current_run'] or 'idle'}`",
        "",
    ]
    if status["completed_run_names"]:
        lines.append("## Recent Completed")
        lines.append("")
        for name in status["completed_run_names"]:
            lines.append(f"- `{name}`")
        lines.append("")
    if status["failures"]:
        lines.append("## Recent Failures")
        lines.append("")
        for item in status["failures"]:
            lines.append(f"- `{item['run_name']}` `{item['error']}`")
        lines.append("")
    return "\n".join(lines)


def write_status(paths: dict[str, Path], status: dict[str, Any]) -> None:
    write_json(paths["status_json"], status)
    write_text(paths["status_md"], build_status_markdown(status))


def main() -> int:
    args = build_parser().parse_args()
    stage_root = Path(args.stage_root).resolve()
    source_root = Path(args.source_root).resolve()
    paths = stage18_paths(stage_root, args.batch_id)
    cores = build_cores()
    overlays = build_overlays()
    variants = build_variants(cores, overlays)
    ensure_stage_scaffold(stage_root, paths, args, cores, overlays, variants)

    payloads: list[dict[str, Any]] = []
    failures: list[dict[str, Any]] = []
    write_status(
        paths,
        build_status_payload(stage_root=stage_root, variants=variants, payloads=payloads, failures=failures, current_run=None),
    )

    for variant in variants:
        for window_token in WINDOW_TOKENS:
            run_name = variant_run_name(variant, window_token)
            run_dir = stage_root / "02_runs" / "active" / run_name
            segmented_path = run_dir / "segmented_results.json"
            write_status(
                paths,
                build_status_payload(
                    stage_root=stage_root,
                    variants=variants,
                    payloads=payloads,
                    failures=failures,
                    current_run=run_name,
                ),
            )
            try:
                if segmented_path.exists() and not args.rebuild_bundle:
                    payloads.append(load_json(segmented_path))
                    continue

                source_dir = source_run_dir(source_root, variant.core, window_token)
                source_item = build_source_item(source_dir)
                if not source_item["has_bundle"]:
                    raise FileNotFoundError(f"source bundle missing: {source_dir}")

                source_payload = load_json(source_dir / "segmented_results.json")
                boundaries = source_payload["split_boundaries"]
                validation_start = parse_utc(boundaries["train_end_utc_exclusive"])
                validation_end = parse_utc(boundaries["validation_end_utc_exclusive"])
                test_end = parse_utc(boundaries["test_end_utc_exclusive"])
                segment_scheme = wfo_segment_scheme(validation_start, validation_end, validation_end, test_end)

                run_dir.mkdir(parents=True, exist_ok=True)
                bundle_path = ensure_bundle(
                    source_item=source_item,
                    run_dir=run_dir,
                    run_name=run_name,
                    experiment_id=f"exp_{run_name.lower()}_v1",
                    variant=variant,
                    args=args,
                )
                run_tester(bundle_path, "validation")
                run_tester(bundle_path, "test")
                payload = build_run_payload(
                    run_dir=run_dir,
                    source_payload=source_payload,
                    variant=variant,
                    window_token=window_token,
                    segment_scheme=segment_scheme,
                )
                write_json(segmented_path, payload)
                write_text(
                    run_dir / "segmented_results.md",
                    json.dumps(payload["cross_segment_summary"], ensure_ascii=False, indent=2) + "\n",
                )
                payloads.append(payload)
            except Exception as exc:
                failures.append(
                    {
                        "run_name": run_name,
                        "core_stage_id": variant.core.stage_id,
                        "overlay_token": variant.overlay.token,
                        "window_token": window_token,
                        "error": str(exc),
                        "traceback": traceback.format_exc(),
                    }
                )
            finally:
                write_status(
                    paths,
                    build_status_payload(
                        stage_root=stage_root,
                        variants=variants,
                        payloads=payloads,
                        failures=failures,
                        current_run=run_name,
                    ),
                )

    rows = aggregate_variants(payloads, variants)
    review_payload = {
        "generated_at_utc": utc_now_iso(),
        "stage": "18_directional_core_overlay_matrix",
        "phase": "18MX_directional_core_overlay_matrix",
        "variants": [
            {
                "stage_id": variant.stage_id,
                "core_stage_id": variant.core.stage_id,
                "core_label": variant.core.label,
                "overlay_token": variant.overlay.token,
                "overlay_label": variant.overlay.label,
                "risk_pct": variant.overlay.risk_pct,
            }
            for variant in variants
        ],
        "aggregated_variants": rows,
        "runs": payloads,
        "failures": failures,
    }
    write_json(paths["review_json"], review_payload)
    write_text(paths["review_md"], build_review_markdown(rows, cores, overlays))
    update_review_index(paths["review_index"], paths["review_md"].name)
    update_selection_status(paths["selection"], rows, cores)
    write_status(
        paths,
        build_status_payload(stage_root=stage_root, variants=variants, payloads=payloads, failures=failures, current_run=None),
    )

    print(f"[done] review={paths['review_md']}")
    print(f"[done] completed={len(payloads)} failed={len(failures)} total={len(variants) * len(WINDOW_TOKENS)}")
    for row in rows[:5]:
        print(
            f"[top] {row['stage_id']} {row['core_stage_id']}+{row['overlay_token']} "
            f"avg_test={format_metric(row['avg_test_return_pct'], 3)} "
            f"target_holdout_b={format_metric(row['target_holdout_b_return_pct'], 3)} "
            f"min_holdout_b={format_metric(row['min_holdout_b_return_pct'], 3)}"
        )
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
