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
        StatusEvent(status="draft", changed_at_utc=now, reason="bundle_initialized_from_26A_reference"),
        StatusEvent(status="ready", changed_at_utc=now, reason="stage26_gov_adaptive_wave2_prepared"),
    ]


RUNS = [
    {
        "folder_name": "26E_26a_gext030_m090_d1_0001",
        "experiment_id": "exp_26e_26a_gext030_m090_d1_v1",
        "stage_id": "26E",
        "label": "external skip trigger 0.30 mild taper",
        "extra_overrides": {
            "governance_overlay_label": "external_skip_030_m090_d1",
            "governance_external_taper_max_skip_rate": 0.30,
            "governance_external_taper_mult": 0.90,
            "governance_external_taper_duration_bars": 1,
            "stage26_wave2_label": "local_external_skip_030",
        },
    },
    {
        "folder_name": "26F_26a_gext038_m090_d1_0001",
        "experiment_id": "exp_26f_26a_gext038_m090_d1_v1",
        "stage_id": "26F",
        "label": "external skip trigger 0.38 mild taper",
        "extra_overrides": {
            "governance_overlay_label": "external_skip_038_m090_d1",
            "governance_external_taper_max_skip_rate": 0.38,
            "governance_external_taper_mult": 0.90,
            "governance_external_taper_duration_bars": 1,
            "stage26_wave2_label": "local_external_skip_038",
        },
    },
    {
        "folder_name": "26G_26a_gsig_argmax_m090_0001",
        "experiment_id": "exp_26g_26a_gsig_argmax_m090_v1",
        "stage_id": "26G",
        "label": "argmax-only governance trigger",
        "extra_overrides": {
            "governance_overlay_label": "signal_argmax_only_m090",
            "governance_signal_taper_max_argmax_share": 0.82,
            "governance_signal_taper_mult": 0.90,
            "governance_signal_taper_mode": "argmax_only",
            "governance_signal_taper_duration_bars": 1,
            "stage26_wave2_label": "local_signal_argmax_only",
        },
    },
    {
        "folder_name": "26H_26a_gsig_entropy_m090_0001",
        "experiment_id": "exp_26h_26a_gsig_entropy_m090_v1",
        "stage_id": "26H",
        "label": "entropy-only governance trigger",
        "extra_overrides": {
            "governance_overlay_label": "signal_entropy_only_m090",
            "governance_signal_taper_min_entropy": 0.90,
            "governance_signal_taper_mult": 0.90,
            "governance_signal_taper_mode": "entropy_only",
            "governance_signal_taper_duration_bars": 1,
            "stage26_wave2_label": "local_signal_entropy_only",
        },
    },
    {
        "folder_name": "26I_26a_gsig_both_m090_0001",
        "experiment_id": "exp_26i_26a_gsig_both_m090_v1",
        "stage_id": "26I",
        "label": "combined signal trigger requiring both conditions",
        "extra_overrides": {
            "governance_overlay_label": "signal_both_m090",
            "governance_signal_taper_max_argmax_share": 0.82,
            "governance_signal_taper_min_entropy": 0.90,
            "governance_signal_taper_mult": 0.90,
            "governance_signal_taper_mode": "both",
            "governance_signal_taper_duration_bars": 1,
            "stage26_wave2_label": "local_signal_both",
        },
    },
    {
        "folder_name": "26J_26a_gext034_m095_d1_0001",
        "experiment_id": "exp_26j_26a_gext034_m095_d1_v1",
        "stage_id": "26J",
        "label": "external skip taper strength 0.95",
        "extra_overrides": {
            "governance_overlay_label": "external_skip_034_m095_d1",
            "governance_external_taper_max_skip_rate": 0.34,
            "governance_external_taper_mult": 0.95,
            "governance_external_taper_duration_bars": 1,
            "stage26_wave2_label": "local_taper_strength_095",
        },
    },
    {
        "folder_name": "26K_26a_gext034_m090_d3_0001",
        "experiment_id": "exp_26k_26a_gext034_m090_d3_v1",
        "stage_id": "26K",
        "label": "external skip taper duration 3",
        "extra_overrides": {
            "governance_overlay_label": "external_skip_034_m090_d3",
            "governance_external_taper_max_skip_rate": 0.34,
            "governance_external_taper_mult": 0.90,
            "governance_external_taper_duration_bars": 3,
            "stage26_wave2_label": "local_duration_3",
        },
    },
    {
        "folder_name": "26L_26a_gext034_m090_d5_0001",
        "experiment_id": "exp_26l_26a_gext034_m090_d5_v1",
        "stage_id": "26L",
        "label": "external skip taper duration 5",
        "extra_overrides": {
            "governance_overlay_label": "external_skip_034_m090_d5",
            "governance_external_taper_max_skip_rate": 0.34,
            "governance_external_taper_mult": 0.90,
            "governance_external_taper_duration_bars": 5,
            "stage26_wave2_label": "local_duration_5",
        },
    },
    {
        "folder_name": "26M_26a_gburst_mix_d3_0001",
        "experiment_id": "exp_26m_26a_gburst_mix_d3_v1",
        "stage_id": "26M",
        "label": "burst-style combined signal and external overlay",
        "extra_overrides": {
            "governance_overlay_label": "burst_combo_mix_d3",
            "governance_signal_taper_max_argmax_share": 0.82,
            "governance_signal_taper_min_entropy": 0.90,
            "governance_signal_taper_mult": 0.90,
            "governance_signal_taper_mode": "either",
            "governance_signal_taper_duration_bars": 3,
            "governance_external_taper_max_skip_rate": 0.34,
            "governance_external_taper_mult": 0.90,
            "governance_external_taper_duration_bars": 3,
            "stage26_wave2_label": "expansion_burst_combo_overlay",
        },
    },
    {
        "folder_name": "26N_26a_gpost_short_d3_0001",
        "experiment_id": "exp_26n_26a_gpost_short_d3_v1",
        "stage_id": "26N",
        "label": "postcash short-only governance overlay",
        "extra_overrides": {
            "governance_overlay_label": "postcash_short_external_d3",
            "governance_external_taper_max_skip_rate": 0.34,
            "governance_external_taper_mult": 0.90,
            "governance_external_taper_duration_bars": 3,
            "governance_overlay_context": "ny_postcash",
            "governance_overlay_direction": "short",
            "stage26_wave2_label": "expansion_postcash_short_governance",
        },
    },
    {
        "folder_name": "26O_26a_gweakpocket_short_d3_0001",
        "experiment_id": "exp_26o_26a_gweakpocket_short_d3_v1",
        "stage_id": "26O",
        "label": "weak-pocket governance-context fusion",
        "extra_overrides": {
            "governance_overlay_label": "weak_pocket_short_fusion_d3",
            "governance_signal_taper_max_argmax_share": 0.82,
            "governance_signal_taper_min_entropy": 0.90,
            "governance_signal_taper_mult": 0.90,
            "governance_signal_taper_mode": "either",
            "governance_signal_taper_duration_bars": 3,
            "governance_external_taper_max_skip_rate": 0.34,
            "governance_external_taper_mult": 0.90,
            "governance_external_taper_duration_bars": 3,
            "governance_overlay_context": "monday_or_postcash",
            "governance_overlay_direction": "short",
            "stage26_wave2_label": "expansion_weak_pocket_context_fusion",
        },
    },
]


def filter_base_artifacts(bundle: ExperimentBundle):
    return [artifact for artifact in bundle.artifacts if not artifact.role.startswith("mt5_")]


def derive_base_extra(bundle: ExperimentBundle) -> dict[str, int | float | str]:
    extra = deepcopy(bundle.runtime_snapshot.extra)
    for key in list(extra.keys()):
        if key.startswith("governance_"):
            extra.pop(key, None)
    return extra


def upsert_capabilities(bundle: ExperimentBundle, extra_overrides: dict[str, int | float | str]) -> None:
    filtered = [
        capability
        for capability in bundle.compatibility.required_ea_capabilities
        if capability.name
        not in {
            "governance_adaptive_overlay",
            "governance_adaptive_overlay_duration",
            "governance_adaptive_overlay_context_direction",
            "governance_signal_mode_switch",
        }
    ]
    filtered.append(CapabilityRequirement(name="governance_adaptive_overlay", min_version="1.1"))
    if (
        int(extra_overrides.get("governance_signal_taper_duration_bars", 1)) > 1
        or int(extra_overrides.get("governance_external_taper_duration_bars", 1)) > 1
    ):
        filtered.append(CapabilityRequirement(name="governance_adaptive_overlay_duration", min_version="1.0"))
    if "governance_overlay_context" in extra_overrides or "governance_overlay_direction" in extra_overrides:
        filtered.append(CapabilityRequirement(name="governance_adaptive_overlay_context_direction", min_version="1.0"))
    if "governance_signal_taper_mode" in extra_overrides:
        filtered.append(CapabilityRequirement(name="governance_signal_mode_switch", min_version="1.0"))
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
        bundle.identity.stage_name = "governance_led_adaptive_overlays"
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
