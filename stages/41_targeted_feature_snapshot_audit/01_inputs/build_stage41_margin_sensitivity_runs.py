#!/usr/bin/env python3
from __future__ import annotations

import shutil
import sys
import argparse
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[3]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from foundation.pipelines.experiment_bundle_models import ExperimentBundle, ResultsBlock, StatusEvent  # noqa: E402


UTC = timezone.utc
STAGE_DIR = ROOT_DIR / "stages" / "41_targeted_feature_snapshot_audit"
ACTIVE_RUNS_DIR = STAGE_DIR / "02_runs" / "active"
ARCHIVED_RUNS_DIR = STAGE_DIR / "02_runs" / "archived"
BASE_RUN_DIRS = {
    "34b": ROOT_DIR / "stages" / "39_window_extension_mt5_validation" / "02_runs" / "active" / "39B_34b_bridge_ext_0001",
    "34d": ROOT_DIR / "stages" / "39_window_extension_mt5_validation" / "02_runs" / "active" / "39A_34d_bridge_ext_0001",
}


RUN_SPECS = [
    {
        "stage_id": "41A",
        "folder_name": "41A_34b_margin0600_0001",
        "experiment_id": "exp_41a_34b_margin0600_v1",
        "min_margin": 0.0600,
        "label": "34b_contract_margin0600_latest",
    },
    {
        "stage_id": "41B",
        "folder_name": "41B_34b_margin0625_0001",
        "experiment_id": "exp_41b_34b_margin0625_v1",
        "min_margin": 0.0625,
        "label": "34b_contract_margin0625_latest",
    },
    {
        "stage_id": "41C",
        "folder_name": "41C_34b_margin0650_0001",
        "experiment_id": "exp_41c_34b_margin0650_v1",
        "min_margin": 0.0650,
        "label": "34b_contract_margin0650_latest",
    },
    {
        "stage_id": "41D",
        "folder_name": "41D_34b_margin0675_0001",
        "experiment_id": "exp_41d_34b_margin0675_v1",
        "min_margin": 0.0675,
        "label": "34b_contract_margin0675_latest",
    },
    {
        "stage_id": "41E",
        "folder_name": "41E_34b_margin0700_0001",
        "experiment_id": "exp_41e_34b_margin0700_v1",
        "min_margin": 0.0700,
        "label": "34b_contract_margin0700_latest",
        "base_key": "34b",
    },
    {
        "stage_id": "41F",
        "folder_name": "41F_34d_margin0600_0001",
        "experiment_id": "exp_41f_34d_margin0600_v1",
        "min_margin": 0.0600,
        "label": "34d_contract_margin0600_latest",
        "base_key": "34d",
    },
]


def utc_now_iso() -> str:
    return datetime.now(tz=UTC).isoformat()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Create Stage 41 fixed-margin replay run directories.")
    parser.add_argument(
        "--only-stage-ids",
        help="Optional comma-separated subset such as 41F. When omitted, all specs are considered.",
    )
    parser.add_argument(
        "--skip-existing",
        action="store_true",
        help="Skip run directories that already exist instead of failing.",
    )
    return parser


def build_status_history() -> list[StatusEvent]:
    now = utc_now_iso()
    return [
        StatusEvent(status="draft", changed_at_utc=now, reason="bundle_initialized_from_stage39_margin_sensitivity_source"),
        StatusEvent(status="ready", changed_at_utc=now, reason="stage41_margin_sensitivity_replay_prepared"),
    ]


def filter_base_artifacts(bundle: ExperimentBundle):
    return [artifact for artifact in bundle.artifacts if not artifact.role.startswith("mt5_")]


def update_margin_rule(bundle: ExperimentBundle, min_margin: float) -> None:
    margin_rule = next(
        (rule for rule in bundle.rule_stack.filters if rule.enabled and rule.type == "max_probability_margin"),
        None,
    )
    if margin_rule is None:
        raise ValueError("base bundle has no enabled max_probability_margin rule")
    margin_rule.params["min_margin"] = float(min_margin)


def main() -> int:
    args = build_parser().parse_args()
    ACTIVE_RUNS_DIR.mkdir(parents=True, exist_ok=True)
    ARCHIVED_RUNS_DIR.mkdir(parents=True, exist_ok=True)

    selected_stage_ids = None
    if args.only_stage_ids:
        selected_stage_ids = {item.strip().upper() for item in args.only_stage_ids.split(",") if item.strip()}

    base_bundles = {
        key: ExperimentBundle.from_json((path / "experiment_bundle.json").read_text(encoding="utf-8-sig"))
        for key, path in BASE_RUN_DIRS.items()
    }

    for spec in RUN_SPECS:
        if selected_stage_ids is not None and str(spec["stage_id"]).upper() not in selected_stage_ids:
            continue

        run_dir = ACTIVE_RUNS_DIR / spec["folder_name"]
        if run_dir.exists():
            if args.skip_existing:
                print(f"[skip] exists={run_dir}")
                continue
            raise FileExistsError(f"target run directory already exists: {run_dir}")

        run_dir.mkdir(parents=True, exist_ok=False)
        base_key = str(spec.get("base_key", "34b"))
        base_run_dir = BASE_RUN_DIRS[base_key]
        shutil.copytree(base_run_dir / "artifacts", run_dir / "artifacts")

        bundle = deepcopy(base_bundles[base_key])
        bundle.identity.experiment_id = spec["experiment_id"]
        bundle.identity.stage_id = spec["stage_id"]
        bundle.identity.stage_name = "targeted_feature_snapshot_audit"
        bundle.identity.created_at_utc = utc_now_iso()
        bundle.identity.bundle_status = "ready"
        bundle.status_history = build_status_history()
        bundle.results = ResultsBlock()
        bundle.run_attempts = []
        bundle.artifacts = filter_base_artifacts(bundle)

        update_margin_rule(bundle, float(spec["min_margin"]))
        bundle.runtime_snapshot.extra["stage41_margin_sensitivity_label"] = spec["label"]
        bundle.runtime_snapshot.extra["stage41_margin_sensitivity_mode"] = "latest_window_contract_margin_replay"
        bundle.runtime_snapshot.extra["stage41_margin_sensitivity_min_margin"] = float(spec["min_margin"])

        (run_dir / "rule_stack.json").write_text(
            bundle.rule_stack.model_dump_json(indent=2, exclude_none=False),
            encoding="utf-8",
        )
        (run_dir / "experiment_bundle.json").write_text(bundle.to_json(indent=2), encoding="utf-8")
        print(f"[done] created={run_dir} min_margin={spec['min_margin']:.4f}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
