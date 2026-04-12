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
    / "25_soft_contextual_control"
    / "02_runs"
    / "active"
    / "25D_24a_monpost_t050_m030_psh2_0001"
)
ACTIVE_RUNS_DIR = Path(__file__).resolve().parents[1] / "02_runs" / "active"
UTC = timezone.utc


def utc_now_iso() -> str:
    return datetime.now(tz=UTC).isoformat()


def build_status_history() -> list[StatusEvent]:
    now = utc_now_iso()
    return [
        StatusEvent(status="draft", changed_at_utc=now, reason="bundle_initialized_from_25D_regular_reference"),
        StatusEvent(status="ready", changed_at_utc=now, reason="stage26_gov_adaptive_wave1_prepared"),
    ]


RUNS = [
    {
        "folder_name": "26A_25d_govref_0001",
        "experiment_id": "exp_26a_25d_govref_v1",
        "stage_id": "26A",
        "label": "governance observe-only inherited baseline",
        "extra_overrides": {
            "governance_overlay_label": "observe_only_reference",
        },
        "needs_governance_capability": False,
    },
    {
        "folder_name": "26B_25d_gsig080_0001",
        "experiment_id": "exp_26b_25d_gsig080_v1",
        "stage_id": "26B",
        "label": "signal drift taper",
        "extra_overrides": {
            "governance_overlay_label": "signal_drift_taper",
            "governance_signal_taper_max_argmax_share": 0.82,
            "governance_signal_taper_min_entropy": 0.90,
            "governance_signal_taper_mult": 0.80,
        },
        "needs_governance_capability": True,
    },
    {
        "folder_name": "26C_25d_gext085_0001",
        "experiment_id": "exp_26c_25d_gext085_v1",
        "stage_id": "26C",
        "label": "external skip burst taper",
        "extra_overrides": {
            "governance_overlay_label": "external_skip_taper",
            "governance_external_taper_max_skip_rate": 0.34,
            "governance_external_taper_mult": 0.85,
        },
        "needs_governance_capability": True,
    },
    {
        "folder_name": "26D_25d_gmix090_0001",
        "experiment_id": "exp_26d_25d_gmix090_v1",
        "stage_id": "26D",
        "label": "combined mild governance taper",
        "extra_overrides": {
            "governance_overlay_label": "combined_signal_external_taper",
            "governance_signal_taper_max_argmax_share": 0.82,
            "governance_signal_taper_min_entropy": 0.90,
            "governance_signal_taper_mult": 0.90,
            "governance_external_taper_max_skip_rate": 0.34,
            "governance_external_taper_mult": 0.92,
        },
        "needs_governance_capability": True,
    },
]


def filter_base_artifacts(bundle: ExperimentBundle):
    return [artifact for artifact in bundle.artifacts if not artifact.role.startswith("mt5_")]


def upsert_capabilities(bundle: ExperimentBundle, *, needs_governance_capability: bool) -> None:
    filtered = [
        capability
        for capability in bundle.compatibility.required_ea_capabilities
        if capability.name != "governance_adaptive_overlay"
    ]
    if needs_governance_capability:
        filtered.append(CapabilityRequirement(name="governance_adaptive_overlay", min_version="1.0"))
    bundle.compatibility.required_ea_capabilities = filtered


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
        bundle.identity.stage_name = "governance_led_adaptive_overlays"
        bundle.identity.created_at_utc = utc_now_iso()
        bundle.identity.bundle_status = "ready"
        bundle.status_history = build_status_history()
        bundle.results = ResultsBlock()
        bundle.run_attempts = []
        bundle.artifacts = filter_base_artifacts(bundle)

        bundle.runtime_snapshot.extra = deepcopy(base_bundle.runtime_snapshot.extra)
        bundle.runtime_snapshot.extra.update(run["extra_overrides"])

        upsert_capabilities(bundle, needs_governance_capability=run["needs_governance_capability"])

        (run_dir / "rule_stack.json").write_text(
            bundle.rule_stack.model_dump_json(indent=2, exclude_none=False),
            encoding="utf-8",
        )
        (run_dir / "experiment_bundle.json").write_text(bundle.to_json(indent=2), encoding="utf-8")
        print(f"[done] created={run_dir}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
