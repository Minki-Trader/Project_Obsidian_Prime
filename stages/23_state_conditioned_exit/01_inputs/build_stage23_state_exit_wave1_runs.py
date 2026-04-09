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
    CapabilityRequirement,
    ExperimentBundle,
    ResultsBlock,
    RuleDefinition,
    StatusEvent,
)

BASE_RUN_DIR = (
    ROOT_DIR
    / "stages"
    / "22_point_exit_management"
    / "02_runs"
    / "active"
    / "22Q_05dp_base_risk2_dirsplit_postcash_0001"
)
ACTIVE_RUNS_DIR = Path(__file__).resolve().parents[1] / "02_runs" / "active"
UTC = timezone.utc


def utc_now_iso() -> str:
    return datetime.now(tz=UTC).isoformat()


def build_status_history() -> list[StatusEvent]:
    now = utc_now_iso()
    return [
        StatusEvent(status="draft", changed_at_utc=now, reason="bundle_initialized_from_22Q_regular_reference"),
        StatusEvent(status="ready", changed_at_utc=now, reason="stage23_state_exit_wave1_prepared"),
    ]


def make_time_exit_rule() -> RuleDefinition:
    return RuleDefinition(
        rule_id="exit_01",
        type="time_exit",
        enabled=True,
        params={"max_hold_bars": 5},
    )


def make_flat_exit_rule(rule_id: str, min_flat_probability: float, min_hold_bars: int) -> RuleDefinition:
    return RuleDefinition(
        rule_id=rule_id,
        type="flat_exit_guard",
        enabled=True,
        params={
            "min_flat_probability": min_flat_probability,
            "min_hold_bars": min_hold_bars,
        },
    )


def make_state_exit_rule(
    rule_id: str,
    *,
    min_hold_bars: int,
    min_flat_probability: float | None = None,
    max_direction_margin: float | None = None,
) -> RuleDefinition:
    params: dict[str, float | int] = {"min_hold_bars": min_hold_bars}
    if min_flat_probability is not None:
        params["min_flat_probability"] = min_flat_probability
    if max_direction_margin is not None:
        params["max_direction_margin"] = max_direction_margin
    return RuleDefinition(
        rule_id=rule_id,
        type="state_exit_guard",
        enabled=True,
        params=params,
    )


RUNS = [
    {
        "folder_name": "23A_22q_base_stateexit_ref_0001",
        "experiment_id": "exp_23a_22q_base_stateexit_ref_v1",
        "stage_id": "23A",
        "exit_rules": [
            make_time_exit_rule(),
        ],
    },
    {
        "folder_name": "23B_22q_flat035_h3_risk2_0001",
        "experiment_id": "exp_23b_22q_flat035_h3_risk2_v1",
        "stage_id": "23B",
        "exit_rules": [
            make_time_exit_rule(),
            make_flat_exit_rule("exit_02", 0.35, 3),
        ],
    },
    {
        "folder_name": "23C_22q_margin004_h2_risk2_0001",
        "experiment_id": "exp_23c_22q_margin004_h2_risk2_v1",
        "stage_id": "23C",
        "exit_rules": [
            make_time_exit_rule(),
            make_state_exit_rule("exit_02", min_hold_bars=2, max_direction_margin=0.04),
        ],
    },
    {
        "folder_name": "23D_22q_flat035_margin004_h2_risk2_0001",
        "experiment_id": "exp_23d_22q_flat035_margin004_h2_risk2_v1",
        "stage_id": "23D",
        "exit_rules": [
            make_time_exit_rule(),
            make_state_exit_rule(
                "exit_02",
                min_hold_bars=2,
                min_flat_probability=0.35,
                max_direction_margin=0.04,
            ),
        ],
    },
]


def filter_base_artifacts(bundle: ExperimentBundle):
    return [artifact for artifact in bundle.artifacts if not artifact.role.startswith("mt5_")]


def upsert_state_exit_capability(bundle: ExperimentBundle, exit_rules: list[RuleDefinition]) -> None:
    bundle.compatibility.required_ea_capabilities = [
        capability
        for capability in bundle.compatibility.required_ea_capabilities
        if capability.name != "state_exit_guard"
    ]
    if any(rule.type == "state_exit_guard" for rule in exit_rules):
        bundle.compatibility.required_ea_capabilities.append(
            CapabilityRequirement(name="state_exit_guard", min_version="1.0")
        )


def main() -> int:
    base_bundle = ExperimentBundle.from_json((BASE_RUN_DIR / "experiment_bundle.json").read_text(encoding="utf-8-sig"))

    for run in RUNS:
        run_dir = ACTIVE_RUNS_DIR / run["folder_name"]
        if run_dir.exists():
            raise FileExistsError(f"target run directory already exists: {run_dir}")

        run_dir.mkdir(parents=True, exist_ok=False)
        shutil.copytree(BASE_RUN_DIR / "artifacts", run_dir / "artifacts")

        bundle = deepcopy(base_bundle)
        bundle.identity.experiment_id = run["experiment_id"]
        bundle.identity.stage_id = run["stage_id"]
        bundle.identity.stage_name = "state_conditioned_exit"
        bundle.identity.created_at_utc = utc_now_iso()
        bundle.identity.bundle_status = "ready"
        bundle.status_history = build_status_history()
        bundle.rule_stack.exit = run["exit_rules"]
        bundle.results = ResultsBlock()
        bundle.run_attempts = []
        bundle.artifacts = filter_base_artifacts(bundle)
        upsert_state_exit_capability(bundle, run["exit_rules"])

        (run_dir / "rule_stack.json").write_text(
            bundle.rule_stack.model_dump_json(indent=2, exclude_none=False),
            encoding="utf-8",
        )
        (run_dir / "experiment_bundle.json").write_text(bundle.to_json(indent=2), encoding="utf-8")
        print(f"[done] created={run_dir}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
