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
ACTIVE_RUNS_DIR = BASE_RUN_DIR.parent

UTC = timezone.utc

RISK_OVERLAY = {
    "sizing_mode": "risk_pct",
    "fixed_lot": 0.1,
    "risk_pct": 2.0,
    "capital_base": "balance",
    "stop_model": "atr",
    "stop_execution_mode": "broker_native",
    "stop_policy": "direction_split",
    "stop_atr_period": 14,
    "stop_atr_mult": 1.0,
    "stop_long_atr_mult": 1.4,
    "stop_short_atr_mult": 2.0,
    "extra": {
        "monday_risk_pct_mult": 0.75,
        "ny_postcash_risk_pct_mult": 0.7,
        "ny_postcash_hold_cap_bars": 3,
        "session_overlay_label": "postcash_hold_cut",
        "risk_overlay_reference": "18E_19A_reference",
    },
}


def utc_now_iso() -> str:
    return datetime.now(tz=UTC).isoformat()


def build_status_history() -> list[StatusEvent]:
    now = utc_now_iso()
    return [
        StatusEvent(status="draft", changed_at_utc=now, reason="bundle_initialized_from_22A_baseline"),
        StatusEvent(status="ready", changed_at_utc=now, reason="stage22_risk_overlay_probe_prepared"),
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
        "folder_name": "22Q_05dp_base_risk2_dirsplit_postcash_0001",
        "experiment_id": "exp_22q_05dp_base_risk2_dirsplit_postcash_v1",
        "stage_id": "22Q",
        "exit_rules": [
            make_time_exit_rule(),
        ],
    },
    {
        "folder_name": "22R_05dp_psl45_qtr_h3_risk2_0001",
        "experiment_id": "exp_22r_05dp_psl45_qtr_h3_risk2_v1",
        "stage_id": "22R",
        "exit_rules": [
            make_time_exit_rule(),
            make_partial_stop_rule("exit_02", 0.25, 3),
        ],
    },
    {
        "folder_name": "22S_05dp_psl45_p10_h3_risk2_0001",
        "experiment_id": "exp_22s_05dp_psl45_p10_h3_risk2_v1",
        "stage_id": "22S",
        "exit_rules": [
            make_time_exit_rule(),
            make_partial_stop_rule("exit_02", 0.10, 3),
        ],
    },
    {
        "folder_name": "22T_05dp_psl45_p30_h3_risk2_0001",
        "experiment_id": "exp_22t_05dp_psl45_p30_h3_risk2_v1",
        "stage_id": "22T",
        "exit_rules": [
            make_time_exit_rule(),
            make_partial_stop_rule("exit_02", 0.30, 3),
        ],
    },
]


def filter_base_artifacts(bundle: ExperimentBundle):
    return [artifact for artifact in bundle.artifacts if not artifact.role.startswith("mt5_")]


def apply_risk_overlay(bundle: ExperimentBundle) -> None:
    bundle.runtime_snapshot.sizing_mode = RISK_OVERLAY["sizing_mode"]
    bundle.runtime_snapshot.fixed_lot = RISK_OVERLAY["fixed_lot"]
    bundle.runtime_snapshot.risk_pct = RISK_OVERLAY["risk_pct"]
    bundle.runtime_snapshot.capital_base = RISK_OVERLAY["capital_base"]
    bundle.runtime_snapshot.stop_model = RISK_OVERLAY["stop_model"]
    bundle.runtime_snapshot.stop_execution_mode = RISK_OVERLAY["stop_execution_mode"]
    bundle.runtime_snapshot.stop_policy = RISK_OVERLAY["stop_policy"]
    bundle.runtime_snapshot.stop_atr_period = RISK_OVERLAY["stop_atr_period"]
    bundle.runtime_snapshot.stop_atr_mult = RISK_OVERLAY["stop_atr_mult"]
    bundle.runtime_snapshot.stop_long_atr_mult = RISK_OVERLAY["stop_long_atr_mult"]
    bundle.runtime_snapshot.stop_short_atr_mult = RISK_OVERLAY["stop_short_atr_mult"]
    bundle.runtime_snapshot.extra = dict(RISK_OVERLAY["extra"])


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
        bundle.identity.created_at_utc = utc_now_iso()
        bundle.identity.bundle_status = "ready"
        bundle.status_history = build_status_history()
        bundle.rule_stack.exit = run["exit_rules"]
        apply_risk_overlay(bundle)
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
