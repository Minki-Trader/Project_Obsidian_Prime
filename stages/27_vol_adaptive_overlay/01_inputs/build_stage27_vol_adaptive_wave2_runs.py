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
    / "27_vol_adaptive_overlay"
    / "02_runs"
    / "active"
    / "27A_26a_volref_0001"
)
ACTIVE_RUNS_DIR = Path(__file__).resolve().parents[1] / "02_runs" / "active"
UTC = timezone.utc


def utc_now_iso() -> str:
    return datetime.now(tz=UTC).isoformat()


def build_status_history() -> list[StatusEvent]:
    now = utc_now_iso()
    return [
        StatusEvent(status="draft", changed_at_utc=now, reason="bundle_initialized_from_27A_reference"),
        StatusEvent(status="ready", changed_at_utc=now, reason="stage27_vol_adaptive_wave2_prepared"),
    ]


RUNS = [
    {
        "folder_name": "27E_27a_vh090_0001",
        "experiment_id": "exp_27e_27a_vh090_v1",
        "stage_id": "27E",
        "label": "high-vol-only taper 0.90",
        "extra_overrides": {
            "vol_overlay_label": "high_vol_only_090",
            "vol_risk_low_threshold": 0.90,
            "vol_risk_high_threshold": 1.10,
            "vol_risk_low_mult": 1.00,
            "vol_risk_mid_mult": 1.00,
            "vol_risk_high_mult": 0.90,
            "stage27_wave2_label": "local_high_vol_090",
        },
    },
    {
        "folder_name": "27F_27a_vh092_0001",
        "experiment_id": "exp_27f_27a_vh092_v1",
        "stage_id": "27F",
        "label": "high-vol-only taper 0.92",
        "extra_overrides": {
            "vol_overlay_label": "high_vol_only_092",
            "vol_risk_low_threshold": 0.90,
            "vol_risk_high_threshold": 1.10,
            "vol_risk_low_mult": 1.00,
            "vol_risk_mid_mult": 1.00,
            "vol_risk_high_mult": 0.92,
            "stage27_wave2_label": "local_high_vol_092",
        },
    },
    {
        "folder_name": "27G_27a_vh095_0001",
        "experiment_id": "exp_27g_27a_vh095_v1",
        "stage_id": "27G",
        "label": "high-vol-only taper 0.95",
        "extra_overrides": {
            "vol_overlay_label": "high_vol_only_095",
            "vol_risk_low_threshold": 0.90,
            "vol_risk_high_threshold": 1.10,
            "vol_risk_low_mult": 1.00,
            "vol_risk_mid_mult": 1.00,
            "vol_risk_high_mult": 0.95,
            "stage27_wave2_label": "local_high_vol_095",
        },
    },
    {
        "folder_name": "27H_27a_vthr105_0001",
        "experiment_id": "exp_27h_27a_vthr105_v1",
        "stage_id": "27H",
        "label": "denser high-vol boundary 1.05",
        "extra_overrides": {
            "vol_overlay_label": "high_vol_thr_105",
            "vol_risk_low_threshold": 0.90,
            "vol_risk_high_threshold": 1.05,
            "vol_risk_low_mult": 1.00,
            "vol_risk_mid_mult": 1.00,
            "vol_risk_high_mult": 0.92,
            "stage27_wave2_label": "local_boundary_105",
        },
    },
    {
        "folder_name": "27I_27a_vthr115_0001",
        "experiment_id": "exp_27i_27a_vthr115_v1",
        "stage_id": "27I",
        "label": "denser high-vol boundary 1.15",
        "extra_overrides": {
            "vol_overlay_label": "high_vol_thr_115",
            "vol_risk_low_threshold": 0.90,
            "vol_risk_high_threshold": 1.15,
            "vol_risk_low_mult": 1.00,
            "vol_risk_mid_mult": 1.00,
            "vol_risk_high_mult": 0.92,
            "stage27_wave2_label": "local_boundary_115",
        },
    },
    {
        "folder_name": "27J_27a_holdonly_hv2_0001",
        "experiment_id": "exp_27j_27a_holdonly_hv2_v1",
        "stage_id": "27J",
        "label": "high-vol hold-cap cut without risk taper",
        "extra_overrides": {
            "vol_overlay_label": "high_vol_hold_only_h2",
            "vol_risk_low_threshold": 0.90,
            "vol_risk_high_threshold": 1.10,
            "vol_risk_low_mult": 1.00,
            "vol_risk_mid_mult": 1.00,
            "vol_risk_high_mult": 1.00,
            "vol_high_short_hold_cap_bars": 2,
            "stage27_wave2_label": "local_hold_only_high_vol",
        },
    },
    {
        "folder_name": "27K_27a_vh092_shortonly_0001",
        "experiment_id": "exp_27k_27a_vh092_shortonly_v1",
        "stage_id": "27K",
        "label": "high-vol short-only taper",
        "extra_overrides": {
            "vol_overlay_label": "high_vol_short_only_092",
            "vol_risk_low_threshold": 0.90,
            "vol_risk_high_threshold": 1.10,
            "vol_risk_low_mult": 1.00,
            "vol_risk_mid_mult": 1.00,
            "vol_risk_high_mult": 0.92,
            "vol_overlay_direction": "short",
            "stage27_wave2_label": "expansion_direction_split_short",
        },
    },
    {
        "folder_name": "27L_27a_vh092_longonly_0001",
        "experiment_id": "exp_27l_27a_vh092_longonly_v1",
        "stage_id": "27L",
        "label": "high-vol long-only taper",
        "extra_overrides": {
            "vol_overlay_label": "high_vol_long_only_092",
            "vol_risk_low_threshold": 0.90,
            "vol_risk_high_threshold": 1.10,
            "vol_risk_low_mult": 1.00,
            "vol_risk_mid_mult": 1.00,
            "vol_risk_high_mult": 0.92,
            "vol_overlay_direction": "long",
            "stage27_wave2_label": "expansion_direction_split_long",
        },
    },
    {
        "folder_name": "27M_27a_vh092_postshort_0001",
        "experiment_id": "exp_27m_27a_vh092_postshort_v1",
        "stage_id": "27M",
        "label": "postcash high-vol short taper",
        "extra_overrides": {
            "vol_overlay_label": "postcash_high_vol_short_092",
            "vol_risk_low_threshold": 0.90,
            "vol_risk_high_threshold": 1.10,
            "vol_risk_low_mult": 1.00,
            "vol_risk_mid_mult": 1.00,
            "vol_risk_high_mult": 0.92,
            "vol_overlay_context": "ny_postcash",
            "vol_overlay_direction": "short",
            "stage27_wave2_label": "expansion_postcash_short_overlay",
        },
    },
    {
        "folder_name": "27N_27a_vh092_short_h2_0001",
        "experiment_id": "exp_27n_27a_vh092_short_h2_v1",
        "stage_id": "27N",
        "label": "high-vol short taper with hold-cap fusion",
        "extra_overrides": {
            "vol_overlay_label": "high_vol_short_092_hold2",
            "vol_risk_low_threshold": 0.90,
            "vol_risk_high_threshold": 1.10,
            "vol_risk_low_mult": 1.00,
            "vol_risk_mid_mult": 1.00,
            "vol_risk_high_mult": 0.92,
            "vol_overlay_direction": "short",
            "vol_high_short_hold_cap_bars": 2,
            "stage27_wave2_label": "expansion_vol_hold_fusion",
        },
    },
]


def filter_base_artifacts(bundle: ExperimentBundle):
    return [artifact for artifact in bundle.artifacts if not artifact.role.startswith("mt5_")]


def derive_base_extra(bundle: ExperimentBundle) -> dict[str, int | float | str]:
    extra = deepcopy(bundle.runtime_snapshot.extra)
    for key in list(extra.keys()):
        if key.startswith("vol_"):
            extra.pop(key, None)
    return extra


def upsert_capabilities(bundle: ExperimentBundle, extra_overrides: dict[str, int | float | str]) -> None:
    filtered = [
        capability
        for capability in bundle.compatibility.required_ea_capabilities
        if capability.name not in {"volatility_risk_overlay", "volatility_overlay_context_direction", "volatility_hold_cap"}
    ]
    filtered.append(CapabilityRequirement(name="volatility_risk_overlay", min_version="1.1"))
    if "vol_overlay_context" in extra_overrides or "vol_overlay_direction" in extra_overrides:
        filtered.append(CapabilityRequirement(name="volatility_overlay_context_direction", min_version="1.0"))
    if any(key in extra_overrides for key in {"vol_high_hold_cap_bars", "vol_high_long_hold_cap_bars", "vol_high_short_hold_cap_bars"}):
        filtered.append(CapabilityRequirement(name="volatility_hold_cap", min_version="1.0"))
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
        bundle.identity.stage_name = "volatility_adaptive_overlay"
        bundle.identity.created_at_utc = utc_now_iso()
        bundle.identity.bundle_status = "ready"
        bundle.status_history = build_status_history()
        bundle.results = ResultsBlock()
        bundle.run_attempts = []
        bundle.artifacts = filter_base_artifacts(bundle)

        bundle.runtime_snapshot.extra = deepcopy(base_extra)
        bundle.runtime_snapshot.extra.update(run["extra_overrides"])
        upsert_capabilities(bundle, run["extra_overrides"])

        (run_dir / "rule_stack.json").write_text(
            bundle.rule_stack.model_dump_json(indent=2, exclude_none=False),
            encoding="utf-8",
        )
        (run_dir / "experiment_bundle.json").write_text(bundle.to_json(indent=2), encoding="utf-8")
        print(f"[done] created={run_dir}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
