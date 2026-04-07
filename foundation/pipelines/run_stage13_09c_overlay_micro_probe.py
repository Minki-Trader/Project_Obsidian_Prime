#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from foundation.pipelines.run_stage06_direction_split_segmented_overlay import (
    format_metric,
    utc_now_iso,
    write_json,
    write_text,
)
from foundation.pipelines.run_stage06_early_wfo_lp_compare import parse_utc, wfo_segment_scheme
from foundation.pipelines.run_stage06_pre_risk_pool_batch import run_tester
from foundation.pipelines.run_stage10_09c_overlay_gate import (
    aggregate_variants,
    build_run_payload,
    build_source_item,
    ensure_bundle,
)
from foundation.pipelines.run_stage12_09c_overlay_fine_probe import (
    OverlayVariant,
    load_json,
    overlay_run_name,
    source_run_dir,
)


STAGE13_ROOT = ROOT_DIR / "stages" / "13_09c_overlay_micro_probe"
STAGE09_ROOT = ROOT_DIR / "stages" / "09_05et_local_probe" / "02_runs" / "active"
WINDOW_TOKENS = ["2401", "2407", "2501"]
TARGET_WINDOW_TOKEN = "2407"
TARGET_SEGMENT = "holdout_b"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run a tiny micro-probe around the Stage 12 Monday/post-cash pocket on top of the 09C core."
    )
    parser.add_argument("--stage-root", default=str(STAGE13_ROOT), help="Stage 13 root directory.")
    parser.add_argument("--source-root", default=str(STAGE09_ROOT), help="Stage 09 active runs root.")
    parser.add_argument("--batch-id", default="13OM", help="Stage 13 batch id.")
    parser.add_argument("--risk-pct", type=float, default=2.0, help="Risk percent for overlay runs.")
    parser.add_argument("--stop-atr-period", type=int, default=14, help="ATR period.")
    parser.add_argument("--stop-long-atr-mult", type=float, default=1.4, help="Long ATR multiplier.")
    parser.add_argument("--stop-short-atr-mult", type=float, default=2.0, help="Short ATR multiplier.")
    parser.add_argument(
        "--review-basename",
        default="13OM_09c_overlay_micro_probe_review",
        help="Review basename written under 03_reviews.",
    )
    parser.add_argument("--rebuild-bundle", action="store_true", help="Force bundle rebuild.")
    return parser


def stage13_paths(stage_root: Path) -> dict[str, Path]:
    return {
        "spec": stage_root / "00_spec" / "stage_brief.md",
        "inputs": stage_root / "01_inputs" / "input_manifest.json",
        "review_index": stage_root / "03_reviews" / "review_index.md",
        "selection": stage_root / "04_selected" / "selection_status.md",
    }


def format_mult_token(value: float) -> str:
    if abs(value - 0.6125) < 1e-9:
        return "06125"
    if abs(value - 0.625) < 1e-9:
        return "0625"
    if abs(value - 0.6375) < 1e-9:
        return "06375"
    if abs(value - 0.575) < 1e-9:
        return "0575"
    if abs(value - 0.55) < 1e-9:
        return "055"
    if abs(value - 0.60) < 1e-9:
        return "060"
    return str(value).replace(".", "")


def format_mult_label(value: float) -> str:
    if abs(value - 0.6125) < 1e-9:
        return "0.6125"
    if abs(value - 0.625) < 1e-9:
        return "0.625"
    if abs(value - 0.6375) < 1e-9:
        return "0.6375"
    if abs(value - 0.575) < 1e-9:
        return "0.575"
    if abs(value - 0.55) < 1e-9:
        return "0.550"
    if abs(value - 0.60) < 1e-9:
        return "0.600"
    return f"{value:.4f}"


def build_variants() -> list[OverlayVariant]:
    monday_values = [0.55, 0.575, 0.60]
    post_values = [0.6125, 0.625, 0.6375]
    stage_ids = ["13A", "13B", "13C", "13D", "13E", "13F", "13G", "13H", "13I"]
    variants: list[OverlayVariant] = []
    index = 0
    for monday_mult in monday_values:
        for post_mult in post_values:
            monday_label = format_mult_label(monday_mult)
            post_label = format_mult_label(post_mult)
            label = f"monday_{monday_label}_post_{post_label}"
            variants.append(
                OverlayVariant(
                    stage_id=stage_ids[index],
                    token=f"M{format_mult_token(monday_mult)}_P{format_mult_token(post_mult)}",
                    label=label,
                    description=f"Monday={monday_label}, post-cash={post_label}",
                    runtime_extra={
                        "monday_risk_pct_mult": monday_mult,
                        "ny_postcash_risk_pct_mult": post_mult,
                        "session_overlay_label": label,
                    },
                )
            )
            index += 1
    return variants


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
                    "- stage: `13_09c_overlay_micro_probe`",
                    "- goal: `run a micro-probe around the Stage 12 Monday/post-cash pocket on top of the 09C core`",
                    "- source core: `09C_05ET_margin0700_t30_l50_m0700_h4`",
                    "- windows: `2401, 2407, 2501`",
                    "- target: `2407 / holdout_b`",
                    "- local axes: `monday_risk_pct_mult in {0.55, 0.575, 0.60}`, `ny_postcash_risk_pct_mult in {0.6125, 0.625, 0.6375}`",
                    "",
                ]
            ),
        )

    manifest = {
        "generated_at_utc": utc_now_iso(),
        "stage": "13_09c_overlay_micro_probe",
        "phase": args.batch_id,
        "source_stage": "09_05et_local_probe",
        "source_core_run_name": "09C_05ET_margin0700_t30_l50_m0700_h4",
        "reference_stage12": "12B monday_0.600_post_00625",
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
        write_text(paths["review_index"], "# Review Index\n\n## Current Entries\n\n- `13OM`: pending\n")

    if not paths["selection"].exists():
        write_text(
            paths["selection"],
            "\n".join(
                [
                    "# Selection Status",
                    "",
                    "- stage: `13_09c_overlay_micro_probe`",
                    "- status: `running`",
                    "- source core: `09C_05ET_margin0700_t30_l50_m0700_h4`",
                    "- objective: `see whether the Stage 12 overlay pocket can improve 2407 holdout_b beyond 12B`",
                    "",
                ]
            ),
        )


def build_review_markdown(rows: list[dict[str, Any]], source_reference: dict[str, Any]) -> str:
    lines = [
        "# Stage 13 09C Overlay Micro Probe Review",
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
    entry = f"- `13OM`: see `{review_name}`"
    if entry not in lines:
        lines.append(entry)
    write_text(review_index_path, "\n".join(lines).rstrip() + "\n")


def update_selection_status(selection_path: Path, leader: dict[str, Any], source_reference: dict[str, Any]) -> None:
    lines = [
        "# Selection Status",
        "",
        "- stage: `13_09c_overlay_micro_probe`",
        "- status: `completed`",
        f"- overlay leader: `{leader['stage_id']}` `{leader['label']}`",
        f"- leader basis: `2407_holdout_b={format_metric(leader['target_holdout_b_return_pct'], 3)}, min_holdout_b={format_metric(leader['min_holdout_b_return_pct'], 3)}, avg_test_return={format_metric(leader['avg_test_return_pct'], 3)}`",
        f"- source baseline: `09C target_holdout_b={format_metric(source_reference['target_holdout_b_return_pct'], 3)}, avg_test_return={format_metric(source_reference['avg_test_return_pct'], 3)}`",
        "- next action: `decide whether this Stage 13 micro-probe overlay leader is strong enough to replace the Stage 12 winner`",
        "",
    ]
    write_text(selection_path, "\n".join(lines))


def main() -> int:
    args = build_parser().parse_args()
    stage_root = Path(args.stage_root).resolve()
    source_root = Path(args.source_root).resolve()
    paths = stage13_paths(stage_root)
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
        "stage": "13_09c_overlay_micro_probe",
        "phase": "13OM_09c_overlay_micro_probe",
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
