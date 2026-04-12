#!/usr/bin/env python3
from __future__ import annotations

import shutil
import sys
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[3]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from foundation.pipelines.experiment_bundle_models import (  # noqa: E402
    ExperimentBundle,
    ResultsBlock,
    StatusEvent,
)


BASE_RUN_DIR = ROOT_DIR / "stages" / "22_point_exit_management" / "02_runs" / "active" / "22A_05dp_base_hold5_0001"
UTC = timezone.utc


def utc_now_iso() -> str:
    return datetime.now(tz=UTC).isoformat()


def build_status_history() -> list[StatusEvent]:
    now = utc_now_iso()
    return [
        StatusEvent(status="draft", changed_at_utc=now, reason="bundle_initialized_from_22A_baseline"),
        StatusEvent(status="ready", changed_at_utc=now, reason="alignment_ablation_bundle_prepared"),
    ]


RUN_SPECS = [
    {
        "folder_name": "22I_05dp_breadth_stale1_0001",
        "experiment_id": "exp_22i_05dp_breadth_stale1_v1",
        "stage_id": "22I",
        "runtime_extra": {
            "external_alignment_mode": "stale_closed_bar",
            "external_relaxed_scope": "breadth_only",
            "external_max_stale_bars": 1,
        },
    },
    {
        "folder_name": "22J_05dp_macro_stale1_0001",
        "experiment_id": "exp_22j_05dp_macro_stale1_v1",
        "stage_id": "22J",
        "runtime_extra": {
            "external_alignment_mode": "stale_closed_bar",
            "external_relaxed_scope": "macro_only",
            "external_max_stale_bars": 1,
        },
    },
    {
        "folder_name": "22K_05dp_all_stale1_0001",
        "experiment_id": "exp_22k_05dp_all_stale1_v1",
        "stage_id": "22K",
        "runtime_extra": {
            "external_alignment_mode": "stale_closed_bar",
            "external_relaxed_scope": "all",
            "external_max_stale_bars": 1,
        },
    },
]


def filter_base_artifacts(bundle: ExperimentBundle):
    return [artifact for artifact in bundle.artifacts if not artifact.role.startswith("mt5_")]


def main() -> int:
    base_bundle = ExperimentBundle.from_json((BASE_RUN_DIR / "experiment_bundle.json").read_text(encoding="utf-8-sig"))
    active_runs_dir = BASE_RUN_DIR.parent

    for spec in RUN_SPECS:
        run_dir = active_runs_dir / spec["folder_name"]
        if run_dir.exists():
            raise FileExistsError(f"target run directory already exists: {run_dir}")

        run_dir.mkdir(parents=True, exist_ok=False)
        shutil.copytree(BASE_RUN_DIR / "artifacts", run_dir / "artifacts")

        bundle = deepcopy(base_bundle)
        bundle.identity.experiment_id = spec["experiment_id"]
        bundle.identity.stage_id = spec["stage_id"]
        bundle.identity.created_at_utc = utc_now_iso()
        bundle.identity.bundle_status = "ready"
        bundle.status_history = build_status_history()
        bundle.results = ResultsBlock()
        bundle.run_attempts = []
        bundle.artifacts = filter_base_artifacts(bundle)
        bundle.runtime_snapshot.extra = dict(spec["runtime_extra"])

        (run_dir / "rule_stack.json").write_text(
            bundle.rule_stack.model_dump_json(indent=2, exclude_none=False),
            encoding="utf-8",
        )
        (run_dir / "experiment_bundle.json").write_text(bundle.to_json(indent=2), encoding="utf-8")

        print(f"[done] created={run_dir}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
