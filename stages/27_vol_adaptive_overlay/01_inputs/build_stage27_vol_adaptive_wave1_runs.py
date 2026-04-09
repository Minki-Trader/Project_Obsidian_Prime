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
    / "26_gov_adaptive_overlay"
    / "02_runs"
    / "active"
    / "26A_25d_govref_0001"
)
ACTIVE_RUNS_DIR = Path(__file__).resolve().parents[1] / "02_runs" / "active"
UTC = timezone.utc


def utc_now_iso() -> str:
    return datetime.now(tz=UTC).isoformat()


def build_status_history() -> list[StatusEvent]:
    now = utc_now_iso()
    return [
        StatusEvent(status="draft", changed_at_utc=now, reason="bundle_initialized_from_26A_regular_reference"),
        StatusEvent(status="ready", changed_at_utc=now, reason="stage27_vol_adaptive_wave1_prepared"),
    ]


RUNS = [
    {
        "folder_name": "27A_26a_volref_0001",
        "experiment_id": "exp_27a_26a_volref_v1",
        "stage_id": "27A",
        "label": "volatility observe-only inherited baseline",
        "extra_overrides": {
            "vol_overlay_label": "observe_only_reference",
        },
        "needs_capability": False,
    },
    {
        "folder_name": "27B_26a_vh080_0001",
        "experiment_id": "exp_27b_26a_vh080_v1",
        "stage_id": "27B",
        "label": "high-volatility taper only",
        "extra_overrides": {
            "vol_overlay_label": "high_vol_taper_only",
            "vol_risk_low_threshold": 0.90,
            "vol_risk_high_threshold": 1.10,
            "vol_risk_low_mult": 1.00,
            "vol_risk_mid_mult": 1.00,
            "vol_risk_high_mult": 0.80,
        },
        "needs_capability": True,
    },
    {
        "folder_name": "27C_26a_vl105h080_0001",
        "experiment_id": "exp_27c_26a_vl105h080_v1",
        "stage_id": "27C",
        "label": "two-sided mild volatility bucket overlay",
        "extra_overrides": {
            "vol_overlay_label": "two_sided_mild_bucket",
            "vol_risk_low_threshold": 0.90,
            "vol_risk_high_threshold": 1.10,
            "vol_risk_low_mult": 1.05,
            "vol_risk_mid_mult": 1.00,
            "vol_risk_high_mult": 0.80,
        },
        "needs_capability": True,
    },
    {
        "folder_name": "27D_26a_vl110h085_0001",
        "experiment_id": "exp_27d_26a_vl110h085_v1",
        "stage_id": "27D",
        "label": "two-sided stronger volatility bucket overlay",
        "extra_overrides": {
            "vol_overlay_label": "two_sided_stronger_bucket",
            "vol_risk_low_threshold": 0.90,
            "vol_risk_high_threshold": 1.10,
            "vol_risk_low_mult": 1.10,
            "vol_risk_mid_mult": 1.00,
            "vol_risk_high_mult": 0.85,
        },
        "needs_capability": True,
    },
]


def filter_base_artifacts(bundle: ExperimentBundle):
    return [artifact for artifact in bundle.artifacts if not artifact.role.startswith("mt5_")]


def upsert_capabilities(bundle: ExperimentBundle, *, needs_capability: bool) -> None:
    filtered = [
        capability
        for capability in bundle.compatibility.required_ea_capabilities
        if capability.name != "volatility_risk_overlay"
    ]
    if needs_capability:
        filtered.append(CapabilityRequirement(name="volatility_risk_overlay", min_version="1.0"))
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
        bundle.identity.stage_name = "volatility_adaptive_overlay"
        bundle.identity.created_at_utc = utc_now_iso()
        bundle.identity.bundle_status = "ready"
        bundle.status_history = build_status_history()
        bundle.results = ResultsBlock()
        bundle.run_attempts = []
        bundle.artifacts = filter_base_artifacts(bundle)

        bundle.runtime_snapshot.extra = deepcopy(base_bundle.runtime_snapshot.extra)
        bundle.runtime_snapshot.extra.update(run["extra_overrides"])

        upsert_capabilities(bundle, needs_capability=run["needs_capability"])

        (run_dir / "rule_stack.json").write_text(
            bundle.rule_stack.model_dump_json(indent=2, exclude_none=False),
            encoding="utf-8",
        )
        (run_dir / "experiment_bundle.json").write_text(bundle.to_json(indent=2), encoding="utf-8")
        print(f"[done] created={run_dir}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
