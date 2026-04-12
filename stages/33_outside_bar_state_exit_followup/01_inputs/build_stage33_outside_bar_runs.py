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
    StatusEvent,
)

BASE_RUN_DIR = (
    ROOT_DIR
    / "stages"
    / "29_fusion_long_repair"
    / "02_runs"
    / "active"
    / "29N_25o_sxh2_0001"
)
ACTIVE_RUNS_DIR = Path(__file__).resolve().parents[1] / "02_runs" / "active"
UTC = timezone.utc


def utc_now_iso() -> str:
    return datetime.now(tz=UTC).isoformat()


def build_status_history() -> list[StatusEvent]:
    now = utc_now_iso()
    return [
        StatusEvent(status="draft", changed_at_utc=now, reason="bundle_initialized_from_29N_regular_reference"),
        StatusEvent(status="ready", changed_at_utc=now, reason="stage33_outside_bar_followup_prepared"),
    ]


def make_extra(
    label: str,
    *,
    enabled: bool,
    direction: str = "both",
    min_range_atr14: float = 0.0,
) -> dict[str, int | float | str | bool]:
    extra: dict[str, int | float | str | bool] = {
        "stage33_outside_bar_label": label,
        "state_exit_outside_bar_trigger_scope": "margin_only",
    }
    if enabled:
        extra.update(
            {
                "state_exit_outside_bar_suppress_enabled": True,
                "state_exit_outside_bar_direction": direction,
                "state_exit_outside_bar_min_range_atr14": min_range_atr14,
            }
        )
    return extra


RUNS = [
    {
        "folder_name": "33A_29n_refcarry_0001",
        "experiment_id": "exp_33a_29n_refcarry_v1",
        "stage_id": "33A",
        "label": "29N carry rerun under updated EA",
        "extra_overrides": make_extra("refcarry", enabled=False),
    },
    {
        "folder_name": "33B_29n_outbar_both_0001",
        "experiment_id": "exp_33b_29n_outbar_both_v1",
        "stage_id": "33B",
        "label": "29N plus outside adverse bar suppressor both directions",
        "extra_overrides": make_extra("outside_bar_both", enabled=True, direction="both", min_range_atr14=0.0),
    },
    {
        "folder_name": "33C_29n_outbar_long_0001",
        "experiment_id": "exp_33c_29n_outbar_long_v1",
        "stage_id": "33C",
        "label": "29N plus outside adverse bar suppressor long only",
        "extra_overrides": make_extra("outside_bar_long_only", enabled=True, direction="long", min_range_atr14=0.0),
    },
    {
        "folder_name": "33D_29n_outbar_short_0001",
        "experiment_id": "exp_33d_29n_outbar_short_v1",
        "stage_id": "33D",
        "label": "29N plus outside adverse bar suppressor short only",
        "extra_overrides": make_extra("outside_bar_short_only", enabled=True, direction="short", min_range_atr14=0.0),
    },
    {
        "folder_name": "33E_29n_outbar_both_a125_0001",
        "experiment_id": "exp_33e_29n_outbar_both_a125_v1",
        "stage_id": "33E",
        "label": "29N plus outside adverse bar suppressor both directions with ATR floor 1.25",
        "extra_overrides": make_extra("outside_bar_both_atr125", enabled=True, direction="both", min_range_atr14=1.25),
    },
    {
        "folder_name": "33F_29n_outbar_long_a125_0001",
        "experiment_id": "exp_33f_29n_outbar_long_a125_v1",
        "stage_id": "33F",
        "label": "29N plus outside adverse bar suppressor long only with ATR floor 1.25",
        "extra_overrides": make_extra("outside_bar_long_atr125", enabled=True, direction="long", min_range_atr14=1.25),
    },
]


def filter_base_artifacts(bundle: ExperimentBundle):
    return [artifact for artifact in bundle.artifacts if not artifact.role.startswith("mt5_")]


def derive_base_extra(bundle: ExperimentBundle) -> dict[str, int | float | str | bool]:
    extra = deepcopy(bundle.runtime_snapshot.extra)
    for key in list(extra.keys()):
        if key.startswith("stage29_") or key.startswith("stage32_") or key.startswith("stage33_"):
            extra.pop(key, None)
    extra.pop("state_exit_outside_bar_suppress_enabled", None)
    extra.pop("state_exit_outside_bar_direction", None)
    extra.pop("state_exit_outside_bar_min_range_atr14", None)
    extra.pop("state_exit_outside_bar_trigger_scope", None)
    return extra


def upsert_capabilities(
    bundle: ExperimentBundle,
    *,
    runtime_extra: dict[str, int | float | str | bool],
) -> None:
    filtered = [
        capability
        for capability in bundle.compatibility.required_ea_capabilities
        if capability.name
        not in {
            "state_exit_outside_bar_suppressor",
            "state_exit_outside_bar_suppressor_range_filter",
        }
    ]
    if bool(runtime_extra.get("state_exit_outside_bar_suppress_enabled", False)):
        filtered.append(CapabilityRequirement(name="state_exit_outside_bar_suppressor", min_version="1.0"))
        if float(runtime_extra.get("state_exit_outside_bar_min_range_atr14", 0.0) or 0.0) > 0.0:
            filtered.append(CapabilityRequirement(name="state_exit_outside_bar_suppressor_range_filter", min_version="1.0"))
    bundle.compatibility.required_ea_capabilities = filtered


def main() -> int:
    base_bundle = ExperimentBundle.from_json((BASE_RUN_DIR / "experiment_bundle.json").read_text(encoding="utf-8-sig"))
    base_extra = derive_base_extra(base_bundle)

    for run in RUNS:
        run_dir = ACTIVE_RUNS_DIR / run["folder_name"]
        if run_dir.exists():
            raise FileExistsError(f"target run directory already exists: {run_dir}")

        run_dir.mkdir(parents=True, exist_ok=False)
        shutil.copytree(BASE_RUN_DIR / "artifacts", run_dir / "artifacts")

        bundle = deepcopy(base_bundle)
        bundle.identity.experiment_id = run["experiment_id"]
        bundle.identity.stage_id = run["stage_id"]
        bundle.identity.stage_name = "outside_bar_state_exit_followup"
        bundle.identity.created_at_utc = utc_now_iso()
        bundle.identity.bundle_status = "ready"
        bundle.status_history = build_status_history()
        bundle.results = ResultsBlock()
        bundle.run_attempts = []
        bundle.artifacts = filter_base_artifacts(bundle)

        bundle.runtime_snapshot.extra = deepcopy(base_extra)
        bundle.runtime_snapshot.extra.update(run["extra_overrides"])

        upsert_capabilities(bundle, runtime_extra=bundle.runtime_snapshot.extra)

        (run_dir / "rule_stack.json").write_text(
            bundle.rule_stack.model_dump_json(indent=2, exclude_none=False),
            encoding="utf-8",
        )
        (run_dir / "experiment_bundle.json").write_text(bundle.to_json(indent=2), encoding="utf-8")
        print(f"[done] created={run_dir}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
