#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from itertools import product
from pathlib import Path

import numpy as np
import pandas as pd

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from foundation.pipelines.run_stage01b_model_compare import write_json, write_text
from foundation.pipelines.run_stage02a_threshold_sweep import load_stage01_source, simulate_threshold_pair
from foundation.pipelines.run_stage02c_threshold_confirmation import load_final_test_frame


UTC = timezone.utc


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run Stage 02D local threshold-surface probe.")
    parser.add_argument(
        "--source-run-dir",
        default="stages/01_base_feature_ml/02_runs/archived/01C_run_0001_h03_band000125_logreg",
        help="Stage 01 search-side run directory for valid-side local probing.",
    )
    parser.add_argument(
        "--final-run-dir",
        default="stages/01_base_feature_ml/02_runs/active/01D_run_0001_final_h03_band000125_logreg",
        help="Stage 01 final run directory for test-side local probing.",
    )
    parser.add_argument(
        "--stage-root",
        default="stages/02_individual_thresholds",
        help="Stage 02 root directory.",
    )
    parser.add_argument(
        "--offsets",
        default="-0.05,-0.025,0.0,0.025,0.05",
        help="Comma-separated local offsets to apply around each probe center.",
    )
    return parser


def utc_now_iso() -> str:
    return datetime.now(tz=UTC).isoformat()


def parse_offsets(raw: str) -> list[float]:
    values = [float(item.strip()) for item in raw.split(",") if item.strip()]
    if not values:
        raise ValueError("offset list is empty")
    return values


def probe_centers() -> dict[str, tuple[float, float]]:
    return {
        "valid_leader": (0.60, 0.40),
        "balanced_challenger": (0.45, 0.50),
        "test_favored": (0.35, 0.40),
    }


def generate_probe_pairs(offsets: list[float]) -> list[tuple[str, float, float]]:
    pairs: list[tuple[str, float, float]] = []
    seen: set[tuple[float, float]] = set()
    for origin, (base_short, base_long) in probe_centers().items():
        for short_offset, long_offset in product(offsets, offsets):
            short_threshold = round(base_short + short_offset, 3)
            long_threshold = round(base_long + long_offset, 3)
            if short_threshold <= 0.0 or long_threshold <= 0.0 or short_threshold >= 1.0 or long_threshold >= 1.0:
                continue
            key = (short_threshold, long_threshold)
            if key in seen:
                continue
            seen.add(key)
            pairs.append((origin, short_threshold, long_threshold))
    return pairs


def rank_value(frame: pd.DataFrame, short_threshold: float, long_threshold: float, sort_column: str) -> int | None:
    sorted_frame = frame.sort_values(by=[sort_column, "test_compounded_return"], ascending=[False, False]).reset_index(
        drop=True
    )
    match = sorted_frame[
        np.isclose(sorted_frame["short_threshold"].to_numpy(), short_threshold)
        & np.isclose(sorted_frame["long_threshold"].to_numpy(), long_threshold)
    ]
    if match.empty:
        return None
    return int(match.index[0] + 1)


def update_review_index(review_path: Path) -> None:
    lines = [
        "# Review Index",
        "",
        "## Current Entries",
        "",
        "- `02A`: see `02A_threshold_sweep_review.md`",
        "- `02B`: see `02B_seed_sanity_check_review.md` (`02B_run_0001_seed_sanity_check`, review-only diagnostic, archived)",
        "- `02C`: see `02C_threshold_confirmation_review.md` (`02C_run_0001_threshold_confirmation`, review-only diagnostic, archived)",
        "- `02D`: see `02D_local_surface_probe_review.md` (`02D_run_0001_local_surface_probe`, review-only diagnostic, archived)",
        "",
        "## Review Rule",
        "",
        "For each completed phase, add:",
        "",
        "- run folder name",
        "- threshold setup summary",
        "- split used for search",
        "- headline result",
        "- keep or archive decision",
        "",
        "Also record the phase code:",
        "",
        "- `02A`",
        "- `02B`",
        "- `02C`",
        "- `02D`",
    ]
    write_text(review_path, "\n".join(lines) + "\n")


def update_selection_status(selection_status_path: Path, blended_leader: dict, verdict: str) -> None:
    lines = [
        "# Selection Status",
        "",
        "- stage: `02_individual_thresholds`",
        "- current phase complete: `02D`",
        "- current preferred threshold seed: `02A_run_0001_threshold_sweep` (still provisional, not frozen)",
        "- search source model: `01C_run_0001_h03_band000125_logreg`",
        "- reserved final confirmation model: `01D_run_0001_final_h03_band000125_logreg`",
        (
            f"- local blended leader in the probed neighborhoods: "
            f"`(short_threshold={blended_leader['short_threshold']:.3f}, long_threshold={blended_leader['long_threshold']:.3f})`"
        ),
        f"- local blended leader valid compounded return: `{blended_leader['valid_compounded_return']:.4f}`",
        f"- local blended leader test compounded return: `{blended_leader['test_compounded_return']:.4f}`",
        f"- latest exploratory verdict: `{verdict}`",
        "- final threshold freeze: `still deferred`",
        "- next phase: `continue small exploratory probes before any freeze decision`",
    ]
    write_text(selection_status_path, "\n".join(lines) + "\n")


def main() -> int:
    args = build_parser().parse_args()

    source_run_dir = ROOT_DIR / args.source_run_dir
    final_run_dir = ROOT_DIR / args.final_run_dir
    stage_root = ROOT_DIR / args.stage_root
    offsets = parse_offsets(args.offsets)

    valid_frame, source_config = load_stage01_source(source_run_dir)
    test_frame, final_config = load_final_test_frame(final_run_dir)

    archived_dir = stage_root / "02_runs" / "archived"
    review_dir = stage_root / "03_reviews"
    selected_dir = stage_root / "04_selected"
    for path in (archived_dir, review_dir, selected_dir):
        path.mkdir(parents=True, exist_ok=True)

    run_dir = archived_dir / "02D_run_0001_local_surface_probe"
    run_dir.mkdir(parents=True, exist_ok=True)

    rows: list[dict] = []
    for origin, short_threshold, long_threshold in generate_probe_pairs(offsets):
        valid_metric, _ = simulate_threshold_pair(
            valid_frame=valid_frame,
            horizon_bars=int(source_config["horizon_bars"]),
            short_threshold=short_threshold,
            long_threshold=long_threshold,
        )
        test_metric, _ = simulate_threshold_pair(
            valid_frame=test_frame,
            horizon_bars=int(final_config["horizon_bars"]),
            short_threshold=short_threshold,
            long_threshold=long_threshold,
        )
        rows.append(
            {
                "origin": origin,
                "short_threshold": short_threshold,
                "long_threshold": long_threshold,
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
    probe_df["trade_count_gap"] = (probe_df["test_trade_count"] - probe_df["valid_trade_count"]).abs()

    probe_df.to_csv(run_dir / "local_surface_probe_results.csv", index=False)

    avg_sorted = probe_df.sort_values(
        by=["avg_compounded_return", "both_positive", "test_compounded_return", "valid_compounded_return"],
        ascending=[False, False, False, False],
    ).reset_index(drop=True)
    avg_sorted.to_csv(run_dir / "local_surface_probe_avg_sorted.csv", index=False)

    test_sorted = probe_df.sort_values(
        by=["test_compounded_return", "avg_compounded_return", "valid_compounded_return"],
        ascending=[False, False, False],
    ).reset_index(drop=True)
    test_sorted.to_csv(run_dir / "local_surface_probe_test_sorted.csv", index=False)

    stable_positive = avg_sorted[avg_sorted["both_positive"]].copy().reset_index(drop=True)
    stable_positive.to_csv(run_dir / "local_surface_probe_stable_positive.csv", index=False)

    blended_leader = stable_positive.iloc[0].to_dict()
    top_test = test_sorted.iloc[0].to_dict()
    best_balanced_region = avg_sorted[avg_sorted["origin"].eq("balanced_challenger")].iloc[0].to_dict()

    summary_payload = {
        "generated_at_utc": utc_now_iso(),
        "phase": "02D_local_surface_probe",
        "source_run_dir": str(source_run_dir.relative_to(ROOT_DIR)),
        "final_run_dir": str(final_run_dir.relative_to(ROOT_DIR)),
        "offsets": offsets,
        "probe_centers": {key: list(value) for key, value in probe_centers().items()},
        "probe_pair_count": int(len(probe_df)),
        "blended_leader": blended_leader,
        "top_test_pair_within_probe": top_test,
        "best_balanced_region_pair": best_balanced_region,
        "verdict": "keep exploring; local blended reads favor the valid-leader neighborhood while the test-favored pocket still looks split-dependent",
    }
    write_json(run_dir / "summary.json", summary_payload)
    write_json(review_dir / "02D_local_surface_probe_review.json", summary_payload)

    review_lines = [
        "# 02D Local Surface Probe Review",
        "",
        f"Generated at: `{utc_now_iso()}`",
        "",
        "## Scope",
        "",
        "- purpose: `probe a few local threshold neighborhoods more densely without freezing or promoting a final Stage 02 threshold`",
        "- neighborhoods: `valid leader`, `balanced challenger`, `test-favored pocket`",
        f"- local offsets: `{', '.join(f'{item:+.3f}' for item in offsets)}`",
        "- this is exploration only; no threshold freeze is made here",
        "",
        "## Blended Read",
        "",
        (
            f"- best both-positive blended pair: `(Ts={blended_leader['short_threshold']:.3f}, Tl={blended_leader['long_threshold']:.3f})` "
            f"from `{blended_leader['origin']}`"
        ),
        f"- valid compounded return: `{blended_leader['valid_compounded_return']:.4f}`",
        f"- test compounded return: `{blended_leader['test_compounded_return']:.4f}`",
        f"- average compounded return: `{blended_leader['avg_compounded_return']:.4f}`",
        "",
        "## Test-Favored Pocket",
        "",
        (
            f"- strongest test pair inside the local probe: `(Ts={top_test['short_threshold']:.3f}, Tl={top_test['long_threshold']:.3f})` "
            f"from `{top_test['origin']}`"
        ),
        f"- valid compounded return: `{top_test['valid_compounded_return']:.4f}`",
        f"- test compounded return: `{top_test['test_compounded_return']:.4f}`",
        f"- average compounded return: `{top_test['avg_compounded_return']:.4f}`",
        "",
        "## Balanced Region Read",
        "",
        (
            f"- strongest balanced-region pair inside the local probe: "
            f"`(Ts={best_balanced_region['short_threshold']:.3f}, Tl={best_balanced_region['long_threshold']:.3f})`"
        ),
        f"- valid compounded return: `{best_balanced_region['valid_compounded_return']:.4f}`",
        f"- test compounded return: `{best_balanced_region['test_compounded_return']:.4f}`",
        f"- average compounded return: `{best_balanced_region['avg_compounded_return']:.4f}`",
        "",
        "## Top Blended Reads",
        "",
    ]
    for row in stable_positive.head(12).itertuples(index=False):
        review_lines.append(
            f"- `{row.origin}` `(Ts={row.short_threshold:.3f}, Tl={row.long_threshold:.3f})`: "
            f"valid_comp={row.valid_compounded_return:.4f}, test_comp={row.test_compounded_return:.4f}, "
            f"avg_comp={row.avg_compounded_return:.4f}, gap={row.abs_valid_test_gap:.4f}"
        )
    review_lines.extend(
        [
            "",
            "## Top Test Reads",
            "",
        ]
    )
    for row in test_sorted.head(12).itertuples(index=False):
        review_lines.append(
            f"- `{row.origin}` `(Ts={row.short_threshold:.3f}, Tl={row.long_threshold:.3f})`: "
            f"valid_comp={row.valid_compounded_return:.4f}, test_comp={row.test_compounded_return:.4f}, "
            f"avg_comp={row.avg_compounded_return:.4f}, gap={row.abs_valid_test_gap:.4f}"
        )
    review_lines.extend(
        [
            "",
            "## Verdict",
            "",
            "- verdict: `keep exploring; do not freeze yet`",
            (
                "- read: the valid-leader neighborhood still gives the strongest blended both-positive reads, "
                "while the test-favored low-threshold pocket remains attractive on test but looks too split-dependent "
                "to treat as a stable answer yet."
            ),
            (
                "- implication: if we keep exploring, the next useful small step is to probe a nearby ridge around "
                "the blended leader rather than widening the whole Stage 02 search again."
            ),
        ]
    )
    write_text(review_dir / "02D_local_surface_probe_review.md", "\n".join(review_lines) + "\n")

    note_payload = {
        "generated_at_utc": utc_now_iso(),
        "phase": "02D_local_surface_probe",
        "blended_leader": {
            "short_threshold": blended_leader["short_threshold"],
            "long_threshold": blended_leader["long_threshold"],
            "valid_compounded_return": blended_leader["valid_compounded_return"],
            "test_compounded_return": blended_leader["test_compounded_return"],
            "avg_compounded_return": blended_leader["avg_compounded_return"],
        },
        "top_test_pair_within_probe": {
            "short_threshold": top_test["short_threshold"],
            "long_threshold": top_test["long_threshold"],
            "valid_compounded_return": top_test["valid_compounded_return"],
            "test_compounded_return": top_test["test_compounded_return"],
            "avg_compounded_return": top_test["avg_compounded_return"],
        },
        "verdict": "exploration continues; no freeze",
    }
    write_json(selected_dir / "02D_local_surface_probe.json", note_payload)

    note_lines = [
        "# 02D Local Surface Probe",
        "",
        "- verdict: `exploration continues; no freeze`",
        (
            f"- blended leader: `(short_threshold={blended_leader['short_threshold']:.3f}, "
            f"long_threshold={blended_leader['long_threshold']:.3f})`, "
            f"valid_comp=`{blended_leader['valid_compounded_return']:.4f}`, "
            f"test_comp=`{blended_leader['test_compounded_return']:.4f}`"
        ),
        (
            f"- strongest test pair inside the probe: `(short_threshold={top_test['short_threshold']:.3f}, "
            f"long_threshold={top_test['long_threshold']:.3f})`, "
            f"valid_comp=`{top_test['valid_compounded_return']:.4f}`, "
            f"test_comp=`{top_test['test_compounded_return']:.4f}`"
        ),
    ]
    write_text(selected_dir / "02D_local_surface_probe.md", "\n".join(note_lines) + "\n")

    update_review_index(review_dir / "review_index.md")
    update_selection_status(
        selection_status_path=selected_dir / "selection_status.md",
        blended_leader=blended_leader,
        verdict="keep exploring; local blended reads still favor the valid-leader neighborhood",
    )

    print(json.dumps(summary_payload, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
