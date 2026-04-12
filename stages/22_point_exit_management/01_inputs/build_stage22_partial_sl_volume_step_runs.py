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
    RuleDefinition,
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
        StatusEvent(status="ready", changed_at_utc=now, reason="stage22_partial_sl_volume_step_probe_prepared"),
    ]


def make_time_exit_rule() -> RuleDefinition:
    return RuleDefinition(
        rule_id="exit_01",
        type="time_exit",
        enabled=True,
        params={"max_hold_bars": 5},
    )


def make_partial_stop_rule(rule_id: str, close_fraction: float, min_hold_bars: int) -> RuleDefinition:
    return RuleDefinition(
        rule_id=rule_id,
        type="partial_stop_loss",
        enabled=True,
        params={
            "trigger_points": 45.0,
            "close_fraction": close_fraction,
            "min_hold_bars": min_hold_bars,
        },
    )


RUNS = [
    {
        "folder_name": "22O_05dp_psl45_p10_minhold3_0001",
        "experiment_id": "exp_22o_05dp_psl45_p10_h3_v1",
        "stage_id": "22O",
        "exit_rules": [
            make_time_exit_rule(),
            make_partial_stop_rule("exit_02", 0.10, 3),
        ],
    },
    {
        "folder_name": "22P_05dp_psl45_p30_minhold3_0001",
        "experiment_id": "exp_22p_05dp_psl45_p30_h3_v1",
        "stage_id": "22P",
        "exit_rules": [
            make_time_exit_rule(),
            make_partial_stop_rule("exit_02", 0.30, 3),
        ],
    },
]


def filter_base_artifacts(bundle: ExperimentBundle):
    return [artifact for artifact in bundle.artifacts if not artifact.role.startswith("mt5_")]


def main() -> int:
    base_bundle = ExperimentBundle.from_json((BASE_RUN_DIR / "experiment_bundle.json").read_text(encoding="utf-8-sig"))
    active_runs_dir = BASE_RUN_DIR.parent

    for run in RUNS:
        run_dir = active_runs_dir / run["folder_name"]
        if run_dir.exists():
            raise FileExistsError(f"target run directory already exists: {run_dir}")

        run_dir.mkdir(parents=True, exist_ok=False)
        shutil.copytree(BASE_RUN_DIR / "artifacts", run_dir / "artifacts")

        bundle = deepcopy(base_bundle)
        bundle.identity.experiment_id = run["experiment_id"]
        bundle.identity.stage_id = run["stage_id"]
        bundle.identity.created_at_utc = utc_now_iso()
        bundle.identity.bundle_status = "ready"
        bundle.status_history = build_status_history()
        bundle.rule_stack.exit = run["exit_rules"]
        bundle.results = ResultsBlock()
        bundle.run_attempts = []
        bundle.artifacts = filter_base_artifacts(bundle)

        (run_dir / "rule_stack.json").write_text(
            bundle.rule_stack.model_dump_json(indent=2, exclude_none=False),
            encoding="utf-8",
        )
        (run_dir / "experiment_bundle.json").write_text(bundle.to_json(indent=2), encoding="utf-8")

        print(f"[done] created={run_dir}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
