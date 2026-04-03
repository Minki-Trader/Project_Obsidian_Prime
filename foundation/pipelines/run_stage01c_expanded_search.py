#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from foundation.pipelines.run_stage01a_smoke import (
    build_base_dataset,
    load_us100_target_frame,
    parse_utc,
)
from foundation.pipelines.run_stage01b_model_compare import (
    class_counts,
    fit_lightgbm,
    fit_logistic,
    make_label,
    write_json,
    write_text,
)


UTC = timezone.utc


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run Stage 01C expanded horizon/band search.")
    parser.add_argument(
        "--feature-path",
        default="data/processed/fpmarkets_v2/features/extended_window/feature_matrix.parquet",
        help="Shared feature matrix parquet",
    )
    parser.add_argument(
        "--validity-path",
        default="data/processed/fpmarkets_v2/features/extended_window/feature_validity.parquet",
        help="Shared feature validity parquet",
    )
    parser.add_argument(
        "--us100-raw-root",
        default="data/raw/mt5_bars/m5/US100",
        help="US100 raw M5 parquet root",
    )
    parser.add_argument(
        "--selected-models-json",
        default="stages/01_base_feature_ml/04_selected/01B_selected_models.json",
        help="Stage 01B selected models JSON",
    )
    parser.add_argument(
        "--stage-root",
        default="stages/01_base_feature_ml",
        help="Stage 01 root directory",
    )
    parser.add_argument(
        "--modeling-start",
        default="2022-09-01T00:00:00Z",
        help="Inclusive modeling start timestamp in UTC",
    )
    parser.add_argument(
        "--train-end",
        default="2025-01-01T00:00:00Z",
        help="Exclusive train end timestamp in UTC",
    )
    parser.add_argument(
        "--valid-end",
        default="2025-10-01T00:00:00Z",
        help="Exclusive valid end timestamp in UTC",
    )
    parser.add_argument(
        "--test-end",
        default="2026-03-01T00:00:00Z",
        help="Exclusive test end timestamp in UTC",
    )
    parser.add_argument(
        "--horizons",
        default="3,6,12",
        help="Comma-separated candidate horizons in bars",
    )
    parser.add_argument(
        "--bands",
        default="0.00100,0.00125,0.00150",
        help="Comma-separated candidate absolute-return bands",
    )
    parser.add_argument(
        "--random-state",
        type=int,
        default=42,
        help="Random seed for compared models",
    )
    return parser


def utc_now_iso() -> str:
    return datetime.now(tz=UTC).isoformat()


def horizon_tag(horizon: int) -> str:
    return f"h{horizon:02d}"


def band_tag(value: float) -> str:
    return f"{value:.5f}".replace(".", "")


def selected_model_families(payload: dict) -> list[str]:
    ordered = [
        payload["primary_candidate"]["model_family"],
        payload["secondary_candidate"]["model_family"],
    ]
    seen: set[str] = set()
    result: list[str] = []
    for item in ordered:
        if item not in seen:
            result.append(item)
            seen.add(item)
    return result


def model_specs(selected_families: list[str]) -> list[tuple[str, str, callable]]:
    available = {
        "logistic_regression": ("logreg", fit_logistic),
        "lightgbm": ("lightgbm", fit_lightgbm),
    }
    result: list[tuple[str, str, callable]] = []
    for family in selected_families:
        tag, fn = available[family]
        result.append((tag, family, fn))
    return result


def main() -> int:
    args = build_parser().parse_args()

    feature_path = ROOT_DIR / args.feature_path
    validity_path = ROOT_DIR / args.validity_path
    us100_raw_root = ROOT_DIR / args.us100_raw_root
    selected_models_path = ROOT_DIR / args.selected_models_json
    stage_root = ROOT_DIR / args.stage_root

    modeling_start = parse_utc(args.modeling_start)
    train_end = parse_utc(args.train_end)
    valid_end = parse_utc(args.valid_end)
    test_end = parse_utc(args.test_end)

    horizons = [int(item) for item in args.horizons.split(",") if item.strip()]
    bands = [float(item) for item in args.bands.split(",") if item.strip()]

    selected_models = json.loads(selected_models_path.read_text(encoding="utf-8"))
    families = selected_model_families(selected_models)
    specs = model_specs(families)

    inputs_dir = stage_root / "01_inputs"
    active_dir = stage_root / "02_runs" / "active"
    archived_dir = stage_root / "02_runs" / "archived"
    review_dir = stage_root / "03_reviews"
    selected_dir = stage_root / "04_selected"
    inputs_dir.mkdir(parents=True, exist_ok=True)
    active_dir.mkdir(parents=True, exist_ok=True)
    archived_dir.mkdir(parents=True, exist_ok=True)
    review_dir.mkdir(parents=True, exist_ok=True)
    selected_dir.mkdir(parents=True, exist_ok=True)

    write_json(
        inputs_dir / "01C_expanded_search_plan.json",
        {
            "generated_at_utc": utc_now_iso(),
            "phase": "01C_expanded_search",
            "horizons": horizons,
            "bands": bands,
            "models": families,
            "modeling_start_utc": modeling_start.isoformat(),
            "train_end_utc_exclusive": train_end.isoformat(),
            "valid_end_utc_exclusive": valid_end.isoformat(),
            "test_end_utc_exclusive": test_end.isoformat(),
            "selection_metric": "valid_macro_f1",
            "note": "Validation-only search. Test remains untouched until 01D.",
        },
    )

    results_payloads: list[dict] = []
    run_paths: dict[str, Path] = {}

    for horizon in horizons:
        target_frame = load_us100_target_frame(us100_raw_root, horizon)
        base = build_base_dataset(
            feature_path=feature_path,
            validity_path=validity_path,
            us100_target=target_frame,
            modeling_start=modeling_start,
            train_end=train_end,
            valid_end=valid_end,
            test_end=test_end,
        )
        base_path = inputs_dir / f"stage01c_{horizon_tag(horizon)}_base_dataset.parquet"
        summary_path = inputs_dir / f"stage01c_{horizon_tag(horizon)}_base_dataset_summary.json"
        base.to_parquet(base_path, index=False)
        write_json(
            summary_path,
            {
                "generated_at_utc": utc_now_iso(),
                "horizon_bars": horizon,
                "row_count": int(len(base)),
                "split_counts": {key: int(value) for key, value in base["split"].value_counts().to_dict().items()},
            },
        )

        for band in bands:
            labeled = base.copy()
            labeled["label"] = make_label(labeled["forward_return"], band)

            train_df = labeled[labeled["split"].eq("train")].copy()
            valid_df = labeled[labeled["split"].eq("valid")].copy()
            test_df = labeled[labeled["split"].eq("test")].copy()

            labeled_path = inputs_dir / f"stage01c_{horizon_tag(horizon)}_band{band_tag(band)}_dataset.parquet"
            labeled.to_parquet(labeled_path, index=False)

            for ordinal, family, fit_fn in [(idx + 1, fam, fn) for idx, (tag, fam, fn) in enumerate(specs)]:
                model_tag = "logreg" if family == "logistic_regression" else "lightgbm"
                run_name = f"01C_run_{ordinal:04d}_{horizon_tag(horizon)}_band{band_tag(band)}_{model_tag}"
                run_dir = active_dir / run_name
                run_dir.mkdir(parents=True, exist_ok=True)
                run_paths[run_name] = run_dir

                config = {
                    "run_name": run_name,
                    "phase": "01C_expanded_search",
                    "generated_at_utc": utc_now_iso(),
                    "model_family": family,
                    "horizon_bars": horizon,
                    "band": band,
                    "dataset_path": str(labeled_path.relative_to(ROOT_DIR)),
                    "selection_source": str(selected_models_path.relative_to(ROOT_DIR)),
                    "split_counts": {
                        "train": int(len(train_df)),
                        "valid": int(len(valid_df)),
                        "test": int(len(test_df)),
                    },
                    "class_counts": {
                        "train": class_counts(train_df["label"]),
                        "valid": class_counts(valid_df["label"]),
                        "test": class_counts(test_df["label"]),
                    },
                    "selection_metric": "valid_macro_f1",
                }
                write_json(run_dir / "config.json", config)

                metric = fit_fn(
                    train_df=train_df,
                    valid_df=valid_df,
                    run_dir=run_dir,
                    random_state=args.random_state,
                )
                metric.test_rows = int(len(test_df))
                metric_payload = asdict(metric)
                metric_payload["horizon_bars"] = horizon
                metric_payload["band"] = band
                write_json(run_dir / "metrics.json", metric_payload)
                results_payloads.append(metric_payload)

    results_df = pd.DataFrame(results_payloads).sort_values(
        by=["valid_macro_f1", "valid_balanced_accuracy", "valid_accuracy", "valid_log_loss"],
        ascending=[False, False, False, True],
    )
    results_df.to_csv(review_dir / "01C_expanded_search_results.csv", index=False)

    best = results_df.iloc[0].to_dict()
    runner_up = results_df.iloc[1].to_dict()
    keep_name = best["run_name"]
    archived_runs: list[str] = []
    for run_name, run_dir in run_paths.items():
        if run_name == keep_name:
            continue
        target = archived_dir / run_name
        if target.exists():
            if target.is_dir():
                for child in target.iterdir():
                    if child.is_file():
                        child.unlink()
                target.rmdir()
        run_dir.rename(target)
        archived_runs.append(run_name)

    lines = [
        "# 01C Expanded Search Review",
        "",
        f"Generated at: `{utc_now_iso()}`",
        "",
        "## Search Scope",
        "",
        f"- horizons: `{', '.join(str(item) for item in horizons)}`",
        f"- bands: `{', '.join(f'{item:.5f}' for item in bands)}`",
        f"- models: `{', '.join(families)}`",
        "- selection metric: `valid_macro_f1`",
        "",
        "## Top Results",
        "",
    ]
    for row in results_df.head(10).itertuples(index=False):
        lines.append(
            f"- `{row.run_name}` ({row.model_family}, h={row.horizon_bars}, band={row.band:.5f}): "
            f"macro_f1={row.valid_macro_f1:.4f}, balanced_acc={row.valid_balanced_accuracy:.4f}, "
            f"accuracy={row.valid_accuracy:.4f}, log_loss={row.valid_log_loss:.4f}"
        )
    lines.extend(
        [
            "",
            "## Selection",
            "",
            f"- selected final candidate for `01D`: `{best['run_name']}`",
            f"- runner-up reference: `{runner_up['run_name']}`",
            f"- archived 01C runs: `{len(archived_runs)}`",
        ]
    )
    write_text(review_dir / "01C_expanded_search_review.md", "\n".join(lines) + "\n")

    selected_payload = {
        "generated_at_utc": utc_now_iso(),
        "phase": "01C_expanded_search",
        "selection_metric": "valid_macro_f1",
        "selected_final_candidate": best,
        "runner_up": runner_up,
        "candidate_models_used": families,
        "candidate_horizons": horizons,
        "candidate_bands": bands,
        "archived_runs": archived_runs,
        "next_phase": "01D_final_confirmation",
    }
    write_json(selected_dir / "01C_selected_final_candidate.json", selected_payload)
    write_text(
        selected_dir / "01C_selected_final_candidate.md",
        "\n".join(
            [
                "# 01C Selected Final Candidate",
                "",
                f"- selected run: `{best['run_name']}`",
                f"- model: `{best['model_family']}`",
                f"- horizon: `{int(best['horizon_bars'])}` bars",
                f"- band: `{float(best['band']):.5f}`",
                f"- valid macro_f1: `{float(best['valid_macro_f1']):.4f}`",
                f"- valid balanced_accuracy: `{float(best['valid_balanced_accuracy']):.4f}`",
                f"- next phase: `01D_final_confirmation`",
            ]
        )
        + "\n",
    )

    print(json.dumps(selected_payload, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
