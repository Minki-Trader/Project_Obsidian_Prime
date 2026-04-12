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
    / "23_state_conditioned_exit"
    / "02_runs"
    / "active"
    / "23C_22q_margin004_h2_risk2_0001"
)
ACTIVE_RUNS_DIR = Path(__file__).resolve().parents[1] / "02_runs" / "active"
UTC = timezone.utc


def utc_now_iso() -> str:
    return datetime.now(tz=UTC).isoformat()


def build_status_history() -> list[StatusEvent]:
    now = utc_now_iso()
    return [
        StatusEvent(status="draft", changed_at_utc=now, reason="bundle_initialized_from_23C_shadow_anchor"),
        StatusEvent(status="ready", changed_at_utc=now, reason="stage23_state_exit_wave2_prepared"),
    ]


def make_time_exit_rule() -> RuleDefinition:
    return RuleDefinition(
        rule_id="exit_01",
        type="time_exit",
        enabled=True,
        params={"max_hold_bars": 5},
    )


def make_state_exit_rule(
    rule_id: str,
    *,
    min_hold_bars: int,
    direction: str | None = None,
    min_flat_probability: float | None = None,
    max_direction_margin: float | None = None,
    max_signal_entropy: float | None = None,
    close_fraction: float | None = None,
) -> RuleDefinition:
    params: dict[str, float | int | str] = {"min_hold_bars": min_hold_bars}
    if direction and direction not in {"", "both"}:
        params["direction"] = direction
    if min_flat_probability is not None:
        params["min_flat_probability"] = min_flat_probability
    if max_direction_margin is not None:
        params["max_direction_margin"] = max_direction_margin
    if max_signal_entropy is not None:
        params["max_signal_entropy"] = max_signal_entropy
    if close_fraction is not None:
        params["close_fraction"] = close_fraction
    return RuleDefinition(
        rule_id=rule_id,
        type="state_exit_guard",
        enabled=True,
        params=params,
    )


RUNS = [
    {
        "folder_name": "23E_23c_margin003_h2_0001",
        "experiment_id": "exp_23e_23c_margin003_h2_v1",
        "stage_id": "23E",
        "label": "narrower state margin 0.03 with h2 anchor",
        "exit_rules": [
            make_time_exit_rule(),
            make_state_exit_rule("exit_02", min_hold_bars=2, max_direction_margin=0.03),
        ],
        "extra_overrides": {
            "state_exit_wave2_label": "local_margin_003_anchor_h2",
        },
    },
    {
        "folder_name": "23F_23c_margin005_h2_0001",
        "experiment_id": "exp_23f_23c_margin005_h2_v1",
        "stage_id": "23F",
        "label": "looser state margin 0.05 with h2 anchor",
        "exit_rules": [
            make_time_exit_rule(),
            make_state_exit_rule("exit_02", min_hold_bars=2, max_direction_margin=0.05),
        ],
        "extra_overrides": {
            "state_exit_wave2_label": "local_margin_005_anchor_h2",
        },
    },
    {
        "folder_name": "23G_23c_margin004_h1_0001",
        "experiment_id": "exp_23g_23c_margin004_h1_v1",
        "stage_id": "23G",
        "label": "faster state exit with min hold 1",
        "exit_rules": [
            make_time_exit_rule(),
            make_state_exit_rule("exit_02", min_hold_bars=1, max_direction_margin=0.04),
        ],
        "extra_overrides": {
            "state_exit_wave2_label": "local_hold_1_margin_004",
        },
    },
    {
        "folder_name": "23H_23c_margin004_h3_0001",
        "experiment_id": "exp_23h_23c_margin004_h3_v1",
        "stage_id": "23H",
        "label": "slower state exit with min hold 3",
        "exit_rules": [
            make_time_exit_rule(),
            make_state_exit_rule("exit_02", min_hold_bars=3, max_direction_margin=0.04),
        ],
        "extra_overrides": {
            "state_exit_wave2_label": "local_hold_3_margin_004",
        },
    },
    {
        "folder_name": "23I_23c_margin004_h2_p25_0001",
        "experiment_id": "exp_23i_23c_margin004_h2_p25_v1",
        "stage_id": "23I",
        "label": "state exit partial reduce 25%",
        "exit_rules": [
            make_time_exit_rule(),
            make_state_exit_rule("exit_02", min_hold_bars=2, max_direction_margin=0.04, close_fraction=0.25),
        ],
        "extra_overrides": {
            "state_exit_wave2_label": "local_partial_reduce_25",
        },
    },
    {
        "folder_name": "23J_23c_margin004_h2_p50_0001",
        "experiment_id": "exp_23j_23c_margin004_h2_p50_v1",
        "stage_id": "23J",
        "label": "state exit partial reduce 50%",
        "exit_rules": [
            make_time_exit_rule(),
            make_state_exit_rule("exit_02", min_hold_bars=2, max_direction_margin=0.04, close_fraction=0.50),
        ],
        "extra_overrides": {
            "state_exit_wave2_label": "local_partial_reduce_50",
        },
    },
    {
        "folder_name": "23K_23c_margin004_h2_lock1_0001",
        "experiment_id": "exp_23k_23c_margin004_h2_lock1_v1",
        "stage_id": "23K",
        "label": "state exit with one-bar reentry lock",
        "exit_rules": [
            make_time_exit_rule(),
            make_state_exit_rule("exit_02", min_hold_bars=2, max_direction_margin=0.04),
        ],
        "extra_overrides": {
            "state_exit_reentry_lock_bars": 1,
            "state_exit_wave2_label": "local_reentry_lock_1",
        },
    },
    {
        "folder_name": "23L_23c_margin004_h2_lock2_0001",
        "experiment_id": "exp_23l_23c_margin004_h2_lock2_v1",
        "stage_id": "23L",
        "label": "state exit with two-bar reentry lock",
        "exit_rules": [
            make_time_exit_rule(),
            make_state_exit_rule("exit_02", min_hold_bars=2, max_direction_margin=0.04),
        ],
        "extra_overrides": {
            "state_exit_reentry_lock_bars": 2,
            "state_exit_wave2_label": "local_reentry_lock_2",
        },
    },
    {
        "folder_name": "23M_23c_ladderw050p25s030_0001",
        "experiment_id": "exp_23m_23c_ladderw050p25s030_v1",
        "stage_id": "23M",
        "label": "ladder exit weak partial 25% then strong full",
        "exit_rules": [
            make_time_exit_rule(),
            make_state_exit_rule("exit_02", min_hold_bars=2, max_direction_margin=0.05, close_fraction=0.25),
            make_state_exit_rule("exit_03", min_hold_bars=2, max_direction_margin=0.03),
        ],
        "extra_overrides": {
            "state_exit_wave2_label": "expansion_ladder_partial25_then_full",
        },
    },
    {
        "folder_name": "23N_23c_ladderw050p50s030_0001",
        "experiment_id": "exp_23n_23c_ladderw050p50s030_v1",
        "stage_id": "23N",
        "label": "ladder exit weak partial 50% then strong full",
        "exit_rules": [
            make_time_exit_rule(),
            make_state_exit_rule("exit_02", min_hold_bars=2, max_direction_margin=0.05, close_fraction=0.50),
            make_state_exit_rule("exit_03", min_hold_bars=2, max_direction_margin=0.03),
        ],
        "extra_overrides": {
            "state_exit_wave2_label": "expansion_ladder_partial50_then_full",
        },
    },
    {
        "folder_name": "23O_23c_dirsplit_l050_s030_0001",
        "experiment_id": "exp_23o_23c_dirsplit_l050_s030_v1",
        "stage_id": "23O",
        "label": "direction-specific state exit with looser long and tighter short",
        "exit_rules": [
            make_time_exit_rule(),
            make_state_exit_rule("exit_02", min_hold_bars=2, direction="long", max_direction_margin=0.05),
            make_state_exit_rule("exit_03", min_hold_bars=2, direction="short", max_direction_margin=0.03),
        ],
        "extra_overrides": {
            "state_exit_wave2_label": "expansion_direction_split_long_loose_short_tight",
        },
    },
    {
        "folder_name": "23P_23c_dirsplit_l030_s050_0001",
        "experiment_id": "exp_23p_23c_dirsplit_l030_s050_v1",
        "stage_id": "23P",
        "label": "direction-specific state exit with tighter long and looser short",
        "exit_rules": [
            make_time_exit_rule(),
            make_state_exit_rule("exit_02", min_hold_bars=2, direction="long", max_direction_margin=0.03),
            make_state_exit_rule("exit_03", min_hold_bars=2, direction="short", max_direction_margin=0.05),
        ],
        "extra_overrides": {
            "state_exit_wave2_label": "expansion_direction_split_long_tight_short_loose",
        },
    },
]


def filter_base_artifacts(bundle: ExperimentBundle):
    return [artifact for artifact in bundle.artifacts if not artifact.role.startswith("mt5_")]


def upsert_capabilities(bundle: ExperimentBundle, exit_rules: list[RuleDefinition], extra_overrides: dict[str, int | float | str]) -> None:
    filtered = [
        capability
        for capability in bundle.compatibility.required_ea_capabilities
        if capability.name
        not in {
            "state_exit_guard",
            "state_exit_guard_partial_reduce",
            "state_exit_guard_directional",
            "state_exit_reentry_lock",
        }
    ]
    if any(rule.type == "state_exit_guard" for rule in exit_rules):
        filtered.append(CapabilityRequirement(name="state_exit_guard", min_version="1.1"))
    if any(
        rule.type == "state_exit_guard" and 0.0 < float(rule.params.get("close_fraction", 0.0)) < 1.0
        for rule in exit_rules
    ):
        filtered.append(CapabilityRequirement(name="state_exit_guard_partial_reduce", min_version="1.0"))
    if any(rule.type == "state_exit_guard" and "direction" in rule.params for rule in exit_rules):
        filtered.append(CapabilityRequirement(name="state_exit_guard_directional", min_version="1.0"))
    if int(extra_overrides.get("state_exit_reentry_lock_bars", 0)) > 0:
        filtered.append(CapabilityRequirement(name="state_exit_reentry_lock", min_version="1.0"))
    bundle.compatibility.required_ea_capabilities = filtered


def main() -> int:
    base_bundle = ExperimentBundle.from_json((BASE_RUN_DIR / "experiment_bundle.json").read_text(encoding="utf-8-sig"))
    base_filters = deepcopy(base_bundle.rule_stack.filters)
    base_extra = deepcopy(base_bundle.runtime_snapshot.extra)

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
        bundle.rule_stack.filters = deepcopy(base_filters)
        bundle.rule_stack.exit = deepcopy(run["exit_rules"])
        bundle.runtime_snapshot.extra = deepcopy(base_extra)
        bundle.runtime_snapshot.extra.update(run["extra_overrides"])
        bundle.results = ResultsBlock()
        bundle.run_attempts = []
        bundle.artifacts = filter_base_artifacts(bundle)
        upsert_capabilities(bundle, run["exit_rules"], run["extra_overrides"])

        (run_dir / "rule_stack.json").write_text(
            bundle.rule_stack.model_dump_json(indent=2, exclude_none=False),
            encoding="utf-8",
        )
        (run_dir / "experiment_bundle.json").write_text(bundle.to_json(indent=2), encoding="utf-8")
        print(f"[done] created={run_dir}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
