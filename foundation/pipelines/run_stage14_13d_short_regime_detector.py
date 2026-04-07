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


STAGE14_ROOT = ROOT_DIR / "stages" / "14_13d_short_regime_detector"
STAGE09_ROOT = ROOT_DIR / "stages" / "09_05et_local_probe" / "02_runs" / "active"
STAGE13_ROOT = ROOT_DIR / "stages" / "13_09c_overlay_micro_probe" / "02_runs" / "active"
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
        description="Run a small short-only regime detector batch on top of the 13D overlay baseline."
    )
    parser.add_argument("--stage-root", default=str(STAGE14_ROOT), help="Stage 14 root directory.")
    parser.add_argument("--source-root", default=str(STAGE09_ROOT), help="Stage 09 active runs root.")
    parser.add_argument("--reference-root", default=str(STAGE13_ROOT), help="Stage 13 active runs root.")
    parser.add_argument("--batch-id", default="14SR", help="Stage 14 batch id.")
    parser.add_argument("--risk-pct", type=float, default=2.0, help="Risk percent for overlay runs.")
    parser.add_argument("--stop-atr-period", type=int, default=14, help="ATR period.")
    parser.add_argument("--stop-long-atr-mult", type=float, default=1.4, help="Long ATR multiplier.")
    parser.add_argument("--stop-short-atr-mult", type=float, default=2.0, help="Short ATR multiplier.")
    parser.add_argument(
        "--review-basename",
        default="14SR_13d_short_regime_detector_review",
        help="Review basename written under 03_reviews.",
    )
    parser.add_argument("--rebuild-bundle", action="store_true", help="Force bundle rebuild.")
    return parser


def stage14_paths(stage_root: Path) -> dict[str, Path]:
    return {
        "spec": stage_root / "00_spec" / "stage_brief.md",
        "inputs": stage_root / "01_inputs" / "input_manifest.json",
        "review_index": stage_root / "03_reviews" / "review_index.md",
        "selection": stage_root / "04_selected" / "selection_status.md",
    }


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def base_runtime_extra(label: str) -> dict[str, Any]:
    return {
        "monday_risk_pct_mult": 0.575,
        "ny_postcash_risk_pct_mult": 0.6125,
        "ny_tuewed_cash_short_risk_pct_mult": 1.0,
        "ny_tuewed_cash_short_hour12_risk_pct_mult": 1.0,
        "ny_tuewed_cash_short_hour14_risk_pct_mult": 1.0,
        "session_overlay_label": label,
    }


def build_variants() -> list[OverlayVariant]:
    variants: list[OverlayVariant] = []

    baseline = base_runtime_extra("stage13d_reference")
    variants.append(
        OverlayVariant(
            stage_id="14A",
            token="REF",
            label="stage13d_reference",
            description="Reference 13D overlay without new short-regime detector.",
            runtime_extra=baseline,
        )
    )

    tw75 = base_runtime_extra("tuewed_cash_short_075")
    tw75["ny_tuewed_cash_short_risk_pct_mult"] = 0.75
    variants.append(
        OverlayVariant(
            stage_id="14B",
            token="TW75",
            label="tuewed_cash_short_075",
            description="Reduce all Tue/Wed NY cash shorts to 0.75x.",
            runtime_extra=tw75,
        )
    )

    tw50 = base_runtime_extra("tuewed_cash_short_050")
    tw50["ny_tuewed_cash_short_risk_pct_mult"] = 0.50
    variants.append(
        OverlayVariant(
            stage_id="14C",
            token="TW50",
            label="tuewed_cash_short_050",
            description="Reduce all Tue/Wed NY cash shorts to 0.50x.",
            runtime_extra=tw50,
        )
    )

    tw35 = base_runtime_extra("tuewed_cash_short_035")
    tw35["ny_tuewed_cash_short_risk_pct_mult"] = 0.35
    variants.append(
        OverlayVariant(
            stage_id="14D",
            token="TW35",
            label="tuewed_cash_short_035",
            description="Reduce all Tue/Wed NY cash shorts to 0.35x.",
            runtime_extra=tw35,
        )
    )

    h35 = base_runtime_extra("tuewed_cash_short_h12h14_035")
    h35["ny_tuewed_cash_short_hour12_risk_pct_mult"] = 0.35
    h35["ny_tuewed_cash_short_hour14_risk_pct_mult"] = 0.35
    variants.append(
        OverlayVariant(
            stage_id="14E",
            token="H35",
            label="tuewed_cash_short_h12h14_035",
            description="Only suppress Tue/Wed NY cash short entries at NY hours 12 and 14 to 0.35x.",
            runtime_extra=h35,
        )
    )

    tw75h35 = base_runtime_extra("tuewed_cash_short_075_h12h14_035")
    tw75h35["ny_tuewed_cash_short_risk_pct_mult"] = 0.75
    tw75h35["ny_tuewed_cash_short_hour12_risk_pct_mult"] = 0.35
    tw75h35["ny_tuewed_cash_short_hour14_risk_pct_mult"] = 0.35
    variants.append(
        OverlayVariant(
            stage_id="14F",
            token="TW75H35",
            label="tuewed_cash_short_075_h12h14_035",
            description="Light Tue/Wed NY cash short decay plus extra cuts at NY hours 12 and 14.",
            runtime_extra=tw75h35,
        )
    )
    return variants


def source_run_dir(source_root: Path, window_token: str) -> Path:
    return source_root / f"09C_{window_token}_05et_margin0700_0001"


def reference_run_dir(reference_root: Path, window_token: str) -> Path:
    return reference_root / f"13D_{window_token}_m0575_p06125_0001"


def overlay_run_name(variant: OverlayVariant, window_token: str) -> str:
    return f"{variant.stage_id}_{window_token}_{variant.token.lower()}_0001"


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
                    "- stage: `14_13d_short_regime_detector`",
                    "- goal: `test whether a Tue/Wed NY cash short-only detector can improve the 13D failure regime without breaking the better windows`",
                    "- source core: `09C_05ET_margin0700_t30_l50_m0700_h4`",
                    "- reference overlay: `13D monday=0.575, post-cash=0.6125`",
                    "- windows: `2401, 2407, 2501`",
                    "- target: `2407 / holdout_b`",
                    "- detector focus: `Tue/Wed NY cash shorts, especially NY 12:00 and 14:00`",
                    "",
                ]
            ),
        )

    manifest = {
        "generated_at_utc": utc_now_iso(),
        "stage": "14_13d_short_regime_detector",
        "phase": args.batch_id,
        "source_stage": "09_05et_local_probe",
        "source_core_run_name": "09C_05ET_margin0700_t30_l50_m0700_h4",
        "reference_overlay_stage13": "13D monday_0.575_post_0.6125",
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
        write_text(paths["review_index"], "# Review Index\n\n## Current Entries\n\n- `14SR`: pending\n")

    if not paths["selection"].exists():
        write_text(
            paths["selection"],
            "\n".join(
                [
                    "# Selection Status",
                    "",
                    "- stage: `14_13d_short_regime_detector`",
                    "- status: `running`",
                    "- source core: `09C_05ET_margin0700_t30_l50_m0700_h4`",
                    "- reference overlay: `13D monday=0.575, post-cash=0.6125`",
                    "- objective: `see whether a Tue/Wed NY cash short-only detector can lift 2407 holdout_b beyond the 13D baseline`",
                    "",
                ]
            ),
        )


def build_review_markdown(rows: list[dict[str, Any]], source_reference: dict[str, Any]) -> str:
    lines = [
        "# Stage 14 13D Short Regime Detector Review",
        "",
        "- source core: `09C_05ET_margin0700_t30_l50_m0700_h4`",
        "- reference overlay: `13D monday=0.575, post-cash=0.6125`",
        f"- reference target 2407 holdout_b: `{format_metric(source_reference['target_holdout_b_return_pct'], 3)}`",
        f"- reference avg test return: `{format_metric(source_reference['avg_test_return_pct'], 3)}`",
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
                f"- detector leader: `{leader['stage_id']}` `{leader['label']}`",
                f"- target 2407 holdout_b: `{format_metric(leader['target_holdout_b_return_pct'], 3)}`",
                f"- vs 13D target delta: `{format_metric(leader['target_holdout_b_return_pct'] - source_reference['target_holdout_b_return_pct'], 3)}`",
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
    entry = f"- `14SR`: see `{review_name}`"
    if entry not in lines:
        lines.append(entry)
    write_text(review_index_path, "\n".join(lines).rstrip() + "\n")


def update_selection_status(selection_path: Path, leader: dict[str, Any], source_reference: dict[str, Any]) -> None:
    lines = [
        "# Selection Status",
        "",
        "- stage: `14_13d_short_regime_detector`",
        "- status: `completed`",
        f"- detector leader: `{leader['stage_id']}` `{leader['label']}`",
        f"- leader basis: `2407_holdout_b={format_metric(leader['target_holdout_b_return_pct'], 3)}, min_holdout_b={format_metric(leader['min_holdout_b_return_pct'], 3)}, avg_test_return={format_metric(leader['avg_test_return_pct'], 3)}`",
        f"- reference baseline: `13D target_holdout_b={format_metric(source_reference['target_holdout_b_return_pct'], 3)}, avg_test_return={format_metric(source_reference['avg_test_return_pct'], 3)}`",
        "- next action: `decide whether the 13D baseline should stay generic or move forward with the short-only failure detector`",
        "",
    ]
    write_text(selection_path, "\n".join(lines))


def main() -> int:
    args = build_parser().parse_args()
    stage_root = Path(args.stage_root).resolve()
    source_root = Path(args.source_root).resolve()
    reference_root = Path(args.reference_root).resolve()
    paths = stage14_paths(stage_root)
    variants = build_variants()
    ensure_stage_scaffold(stage_root, paths, args, variants)

    payloads: list[dict[str, Any]] = []
    reference_payloads: dict[str, dict[str, Any]] = {}

    for window_token in WINDOW_TOKENS:
        source_dir = source_run_dir(source_root, window_token)
        source_item = build_source_item(source_dir)
        if not source_item["has_bundle"]:
            raise FileNotFoundError(f"source bundle missing for {window_token}: {source_dir}")
        source_stage09_payload = load_json(source_dir / "segmented_results.json")

        reference_dir = reference_run_dir(reference_root, window_token)
        reference_payload = load_json(reference_dir / "segmented_results.json")
        reference_payload = dict(reference_payload)
        reference_payload["candidate_stage_id"] = "13D"
        reference_payloads[window_token] = reference_payload

        boundaries = source_stage09_payload["split_boundaries"]
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
                source_payload=reference_payload,
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
                for item in reference_payloads[TARGET_WINDOW_TOKEN]["segmented_results"]["test"]["segments"]
                if item["segment"] == TARGET_SEGMENT
            )
        ),
        "avg_test_return_pct": float(
            sum(float(reference_payloads[token]["split_runs"]["test"]["headline"].get("return_pct") or 0.0) for token in WINDOW_TOKENS)
            / len(WINDOW_TOKENS)
        ),
    }

    rows = aggregate_variants(payloads, variants)
    review_json_path = stage_root / "03_reviews" / f"{args.review_basename}.json"
    review_md_path = stage_root / "03_reviews" / f"{args.review_basename}.md"
    review_payload = {
        "generated_at_utc": utc_now_iso(),
        "stage": "14_13d_short_regime_detector",
        "phase": "14SR_13d_short_regime_detector",
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
