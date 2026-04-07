#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
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


STAGE10_ROOT = ROOT_DIR / "stages" / "10_09c_overlay_gate"
STAGE09_ROOT = ROOT_DIR / "stages" / "09_05et_local_probe" / "02_runs" / "active"
WINDOW_TOKENS = ["2401", "2407", "2501"]
TARGET_WINDOW_TOKEN = "2407"
TARGET_SEGMENT = "holdout_b"


@dataclass(frozen=True)
class OverlayVariant:
    stage_id: str
    token: str
    label: str
    description: str
    runtime_extra: dict[str, Any]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run a narrow overlay gate on top of the Stage 09 09C strict-WFO core."
    )
    parser.add_argument("--stage-root", default=str(STAGE10_ROOT), help="Stage 10 root directory.")
    parser.add_argument("--source-root", default=str(STAGE09_ROOT), help="Stage 09 active runs root.")
    parser.add_argument("--batch-id", default="10OG", help="Stage 10 batch id.")
    parser.add_argument("--risk-pct", type=float, default=2.0, help="Risk percent for overlay runs.")
    parser.add_argument("--stop-atr-period", type=int, default=14, help="ATR period.")
    parser.add_argument("--stop-long-atr-mult", type=float, default=1.4, help="Long ATR multiplier.")
    parser.add_argument("--stop-short-atr-mult", type=float, default=2.0, help="Short ATR multiplier.")
    parser.add_argument(
        "--review-basename",
        default="10OG_09c_overlay_gate_review",
        help="Review basename written under 03_reviews.",
    )
    parser.add_argument("--rebuild-bundle", action="store_true", help="Force bundle rebuild.")
    return parser


def stage10_paths(stage_root: Path) -> dict[str, Path]:
    return {
        "spec": stage_root / "00_spec" / "stage_brief.md",
        "inputs": stage_root / "01_inputs" / "input_manifest.json",
        "review_index": stage_root / "03_reviews" / "review_index.md",
        "selection": stage_root / "04_selected" / "selection_status.md",
    }


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def build_variants() -> list[OverlayVariant]:
    return [
        OverlayVariant(
            stage_id="10A",
            token="SD01",
            label="soft_decay_reference",
            description="06D-style soft session decay.",
            runtime_extra={
                "monday_risk_pct_mult": 0.75,
                "ny_postcash_risk_pct_mult": 0.70,
                "session_risk_overlay": "soft_decay",
                "session_overlay_label": "soft_decay_reference",
            },
        ),
        OverlayVariant(
            stage_id="10B",
            token="LP01",
            label="local_probe_a",
            description="Softer Monday, tighter post-cash decay.",
            runtime_extra={
                "monday_risk_pct_mult": 0.80,
                "ny_postcash_risk_pct_mult": 0.65,
                "session_overlay_label": "local_probe_a",
            },
        ),
        OverlayVariant(
            stage_id="10C",
            token="LP02",
            label="local_probe_b",
            description="Stronger Monday and post-cash decay.",
            runtime_extra={
                "monday_risk_pct_mult": 0.70,
                "ny_postcash_risk_pct_mult": 0.65,
                "session_overlay_label": "local_probe_b",
            },
        ),
    ]


def ensure_stage_scaffold(stage_root: Path, paths: dict[str, Path], args: argparse.Namespace, variants: list[OverlayVariant]) -> None:
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
                    "- stage: `10_09c_overlay_gate`",
                    "- goal: `test whether light session-risk overlays improve the Stage 09 09C core without breaking strict-WFO robustness`",
                    "- source core: `09C_05ET_margin0700_t30_l50_m0700_h4`",
                    "- windows: `2401, 2407, 2501`",
                    "- target: `2407 / holdout_b`",
                    "- variants: `06D soft decay, LP01, LP02`",
                    "",
                ]
            ),
        )

    manifest = {
        "generated_at_utc": utc_now_iso(),
        "stage": "10_09c_overlay_gate",
        "phase": args.batch_id,
        "source_stage": "09_05et_local_probe",
        "source_core_run_name": "09C_05ET_margin0700_t30_l50_m0700_h4",
        "risk_pct": args.risk_pct,
        "stop_policy": "direction_split",
        "stop_long_atr_mult": args.stop_long_atr_mult,
        "stop_short_atr_mult": args.stop_short_atr_mult,
        "stop_atr_period": args.stop_atr_period,
        "windows": WINDOW_TOKENS,
        "variants": [
            {
                "stage_id": variant.stage_id,
                "token": variant.token,
                "label": variant.label,
                "description": variant.description,
                "runtime_extra": variant.runtime_extra,
            }
            for variant in variants
        ],
    }
    write_json(paths["inputs"], manifest)

    if not paths["review_index"].exists():
        write_text(paths["review_index"], "# Review Index\n\n## Current Entries\n\n- `10OG`: pending\n")

    if not paths["selection"].exists():
        write_text(
            paths["selection"],
            "\n".join(
                [
                    "# Selection Status",
                    "",
                    "- stage: `10_09c_overlay_gate`",
                    "- status: `running`",
                    "- source core: `09C_05ET_margin0700_t30_l50_m0700_h4`",
                    "- objective: `see whether light session overlays can push 2407 holdout_b closer to zero without losing the improved 09C core profile`",
                    "",
                ]
            ),
        )


def source_run_dir(source_root: Path, window_token: str) -> Path:
    return source_root / f"09C_{window_token}_05et_margin0700_0001"


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


def overlay_run_name(variant: OverlayVariant, window_token: str) -> str:
    return f"{variant.stage_id}_{window_token}_{variant.token.lower()}_0001"


def ensure_bundle(
    *,
    source_item: dict[str, Any],
    run_dir: Path,
    run_name: str,
    experiment_id: str,
    variant: OverlayVariant,
    args: argparse.Namespace,
) -> Path:
    bundle_path, _ = prepare_overlay_bundle(
        source_item=source_item,
        run_dir=run_dir,
        run_name=run_name,
        experiment_id=experiment_id,
        batch_id=args.batch_id,
        risk_pct=args.risk_pct,
        stop_long_atr_mult=args.stop_long_atr_mult,
        stop_short_atr_mult=args.stop_short_atr_mult,
        stop_atr_period=args.stop_atr_period,
        rebuild_bundle=args.rebuild_bundle,
    )

    bundle = ExperimentBundle.from_json(bundle_path.read_text(encoding="utf-8-sig"))
    for key, value in variant.runtime_extra.items():
        bundle.runtime_snapshot.extra[key] = value
    bundle_path.write_text(bundle.to_json(indent=2), encoding="utf-8")

    write_json(
        run_dir / "overlay_manifest.json",
        {
            "generated_at_utc": utc_now_iso(),
            "run_name": run_name,
            "experiment_id": experiment_id,
            "source_run_dir": str(source_item["path"]),
            "source_run_name": source_item["run_name"],
            "overlay": {
                "risk_pct": args.risk_pct,
                "stop_policy": "direction_split",
                "stop_long_atr_mult": args.stop_long_atr_mult,
                "stop_short_atr_mult": args.stop_short_atr_mult,
                "stop_atr_period": args.stop_atr_period,
                **variant.runtime_extra,
            },
        },
    )
    return bundle_path


def build_run_payload(
    *,
    run_dir: Path,
    source_payload: dict[str, Any],
    variant: OverlayVariant,
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
        "stage": "10_09c_overlay_gate",
        "phase": "10OG_09c_overlay_gate",
        "run_name": run_dir.name,
        "source_run_name": source_payload["run_name"],
        "source_candidate_stage_id": source_payload["candidate_stage_id"],
        "window_token": window_token,
        "label": variant.label,
        "description": variant.description,
        "overlay": {
            "risk_pct": bundle.runtime_snapshot.risk_pct,
            "stop_execution_mode": bundle.runtime_snapshot.stop_execution_mode,
            "stop_policy": bundle.runtime_snapshot.stop_policy,
            "stop_long_atr_mult": bundle.runtime_snapshot.stop_long_atr_mult,
            "stop_short_atr_mult": bundle.runtime_snapshot.stop_short_atr_mult,
            "stop_atr_period": bundle.runtime_snapshot.stop_atr_period,
            **variant.runtime_extra,
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


def aggregate_variants(payloads: list[dict[str, Any]], variants: list[OverlayVariant]) -> list[dict[str, Any]]:
    by_variant = {variant.stage_id: [] for variant in variants}
    variant_by_id = {variant.stage_id: variant for variant in variants}
    for payload in payloads:
        by_variant[payload["run_name"].split("_", 1)[0]].append(payload)

    rows: list[dict[str, Any]] = []
    for stage_id, runs in by_variant.items():
        if not runs:
            continue
        variant = variant_by_id[stage_id]
        target_run = next(run for run in runs if run["window_token"] == TARGET_WINDOW_TOKEN)
        target_holdout_b = segment_metric(target_run, "test", TARGET_SEGMENT, "return_pct")
        holdout_b_returns = [segment_metric(run, "test", "holdout_b", "return_pct") for run in runs]
        test_returns = [float(run["split_runs"]["test"]["headline"].get("return_pct") or 0.0) for run in runs]
        test_pfs = [float(run["split_runs"]["test"]["headline"].get("profit_factor") or 0.0) for run in runs]
        rows.append(
            {
                "stage_id": variant.stage_id,
                "label": variant.label,
                "description": variant.description,
                "target_holdout_b_return_pct": target_holdout_b,
                "target_holdout_b_profit_factor": segment_metric(target_run, "test", TARGET_SEGMENT, "profit_factor"),
                "target_test_return_pct": float(target_run["split_runs"]["test"]["headline"].get("return_pct") or 0.0),
                "target_test_profit_factor": float(target_run["split_runs"]["test"]["headline"].get("profit_factor") or 0.0),
                "min_holdout_b_return_pct": float(min(holdout_b_returns)),
                "avg_holdout_b_return_pct": float(sum(holdout_b_returns) / len(holdout_b_returns)),
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
            float(row["target_holdout_b_return_pct"]),
            float(row["min_holdout_b_return_pct"]),
            float(row["avg_test_return_pct"]),
            float(row["avg_test_profit_factor"]),
        ),
        reverse=True,
    )
    for rank, row in enumerate(rows, start=1):
        row["rank"] = rank
    return rows


def build_review_markdown(rows: list[dict[str, Any]], source_reference: dict[str, Any]) -> str:
    lines = [
        "# Stage 10 09C Overlay Gate Review",
        "",
        "- source core: `09C_05ET_margin0700_t30_l50_m0700_h4`",
        f"- source target 2407 holdout_b: `{format_metric(source_reference['target_holdout_b_return_pct'], 3)}`",
        f"- source avg test return: `{format_metric(source_reference['avg_test_return_pct'], 3)}`",
        "- ranking basis: `2407 holdout_b return_pct -> min holdout_b return_pct -> avg test return_pct -> avg test PF`",
        "",
        "## Variant Ranking",
        "",
    ]
    for row in rows:
        lines.append(
            f"- [{row['rank']}] `{row['stage_id']}` `{row['label']}`: "
            f"target_holdout_b=`{format_metric(row['target_holdout_b_return_pct'], 3)}`, "
            f"target_holdout_b_PF=`{format_metric(row['target_holdout_b_profit_factor'], 4)}`, "
            f"min_holdout_b=`{format_metric(row['min_holdout_b_return_pct'], 3)}`, "
            f"avg_test=`{format_metric(row['avg_test_return_pct'], 3)}`, "
            f"positive_test_windows=`{row['positive_test_windows']}/3`, positive_holdout_b_windows=`{row['positive_holdout_b_windows']}/3`"
        )
        for window_row in row["per_window"]:
            lines.append(
                f"  - `{window_row['window_token']}`: test=`{format_metric(window_row['test_return_pct'], 3)}`, "
                f"PF=`{format_metric(window_row['test_profit_factor'], 4)}`, holdout_b=`{format_metric(window_row['holdout_b_return_pct'], 3)}`, "
                f"holdout_b_PF=`{format_metric(window_row['holdout_b_profit_factor'], 4)}`, "
                f"delta_test=`{format_metric(window_row['test_delta_return_pct'], 3)}`, delta_PF=`{format_metric(window_row['test_delta_profit_factor'], 4)}`"
            )
        lines.append("")

    if rows:
        leader = rows[0]
        lines.extend(
            [
                "## Readout",
                "",
                f"- overlay leader: `{leader['stage_id']}` `{leader['label']}`",
                f"- target 2407 holdout_b: `{format_metric(leader['target_holdout_b_return_pct'], 3)}`",
                f"- vs 09C target delta: `{format_metric(leader['target_holdout_b_return_pct'] - source_reference['target_holdout_b_return_pct'], 3)}`",
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
    entry = f"- `10OG`: see `{review_name}`"
    if entry not in lines:
        lines.append(entry)
    write_text(review_index_path, "\n".join(lines).rstrip() + "\n")


def update_selection_status(selection_path: Path, leader: dict[str, Any], source_reference: dict[str, Any]) -> None:
    lines = [
        "# Selection Status",
        "",
        "- stage: `10_09c_overlay_gate`",
        "- status: `completed`",
        f"- overlay leader: `{leader['stage_id']}` `{leader['label']}`",
        f"- leader basis: `2407_holdout_b={format_metric(leader['target_holdout_b_return_pct'], 3)}, min_holdout_b={format_metric(leader['min_holdout_b_return_pct'], 3)}, avg_test_return={format_metric(leader['avg_test_return_pct'], 3)}`",
        f"- source baseline: `09C target_holdout_b={format_metric(source_reference['target_holdout_b_return_pct'], 3)}, avg_test_return={format_metric(source_reference['avg_test_return_pct'], 3)}`",
        "- next action: `decide whether the 09C core should stay plain or move forward with the winning light overlay`",
        "",
    ]
    write_text(selection_path, "\n".join(lines))


def main() -> int:
    args = build_parser().parse_args()
    stage_root = Path(args.stage_root).resolve()
    source_root = Path(args.source_root).resolve()
    paths = stage10_paths(stage_root)
    variants = build_variants()
    ensure_stage_scaffold(stage_root, paths, args, variants)

    payloads: list[dict[str, Any]] = []
    source_payloads: dict[str, dict[str, Any]] = {}

    for window_token in WINDOW_TOKENS:
        source_dir = source_run_dir(source_root, window_token)
        source_item = build_source_item(source_dir)
        if not source_item["has_bundle"]:
            raise FileNotFoundError(f"source bundle missing for {window_token}: {source_dir}")
        source_payload = load_json(source_dir / "segmented_results.json")
        source_payloads[window_token] = source_payload
        boundaries = source_payload["split_boundaries"]
        train_end = parse_utc(boundaries["train_end_utc_exclusive"])
        validation_end = parse_utc(boundaries["validation_end_utc_exclusive"])
        test_end = parse_utc(boundaries["test_end_utc_exclusive"])
        segment_scheme = wfo_segment_scheme(train_end, validation_end, validation_end, test_end)

        for variant in variants:
            run_dir = stage_root / "02_runs" / "active" / overlay_run_name(variant, window_token)
            segmented_path = run_dir / "segmented_results.json"
            if segmented_path.exists() and not args.rebuild_bundle:
                payloads.append(load_json(segmented_path))
                continue

            run_dir.mkdir(parents=True, exist_ok=True)
            bundle_path = ensure_bundle(
                source_item=source_item,
                run_dir=run_dir,
                run_name=overlay_run_name(variant, window_token),
                experiment_id=f"exp_{overlay_run_name(variant, window_token).lower()}_v1",
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
            write_text(run_dir / "segmented_results.md", json.dumps(payload["cross_segment_summary"], ensure_ascii=False, indent=2) + "\n")
            payloads.append(payload)

    source_reference = {
        "target_holdout_b_return_pct": float(
            next(
                item["headline"]["return_pct"]
                for item in source_payloads[TARGET_WINDOW_TOKEN]["segmented_results"]["test"]["segments"]
                if item["segment"] == TARGET_SEGMENT
            )
        ),
        "avg_test_return_pct": float(
            sum(float(source_payloads[token]["split_runs"]["test"]["headline"].get("return_pct") or 0.0) for token in WINDOW_TOKENS)
            / len(WINDOW_TOKENS)
        ),
    }

    rows = aggregate_variants(payloads, variants)
    review_json_path = stage_root / "03_reviews" / f"{args.review_basename}.json"
    review_md_path = stage_root / "03_reviews" / f"{args.review_basename}.md"
    review_payload = {
        "generated_at_utc": utc_now_iso(),
        "stage": "10_09c_overlay_gate",
        "phase": "10OG_09c_overlay_gate",
        "source_reference": source_reference,
        "aggregated_variants": rows,
        "runs": payloads,
    }
    write_json(review_json_path, review_payload)
    write_text(review_md_path, build_review_markdown(rows, source_reference))
    update_review_index(paths["review_index"], review_md_path.name)
    if rows:
        update_selection_status(paths["selection"], rows[0], source_reference)

    print(f"[done] review={review_md_path}")
    for row in rows:
        print(
            f"[done] variant={row['stage_id']} target_holdout_b={row['target_holdout_b_return_pct']:.3f} "
            f"min_holdout_b={row['min_holdout_b_return_pct']:.3f} avg_test={row['avg_test_return_pct']:.3f}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
