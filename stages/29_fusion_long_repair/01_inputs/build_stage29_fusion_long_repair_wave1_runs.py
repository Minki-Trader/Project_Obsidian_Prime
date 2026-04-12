#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import shutil
import sys
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[3]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from foundation.pipelines.experiment_bundle_models import (  # noqa: E402
    ArtifactRef,
    CapabilityRequirement,
    ExperimentBundle,
    ResultsBlock,
    RuleDefinition,
    StatusEvent,
)

BASE_RUN_DIR = (
    ROOT_DIR
    / "stages"
    / "25_soft_contextual_control"
    / "02_runs"
    / "active"
    / "25O_25d_ctx_exit_holdfusion_0001"
)
SHORT_GATE_AUX_ONNX_SOURCE = (
    ROOT_DIR
    / "stages"
    / "17_09c_directional_core_fork"
    / "02_runs"
    / "active"
    / "17C_2501_short_specialist_0001"
    / "artifacts"
    / "model_probonly.onnx"
)
ACTIVE_RUNS_DIR = Path(__file__).resolve().parents[1] / "02_runs" / "active"
UTC = timezone.utc


def utc_now_iso() -> str:
    return datetime.now(tz=UTC).isoformat()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build_status_history() -> list[StatusEvent]:
    now = utc_now_iso()
    return [
        StatusEvent(status="draft", changed_at_utc=now, reason="bundle_initialized_from_25O_wave2_winner"),
        StatusEvent(status="ready", changed_at_utc=now, reason="stage29_fusion_long_repair_wave1_prepared"),
    ]


def make_contextual_soft_suppressor_rule(
    rule_id: str,
    *,
    context: str,
    direction: str,
    threshold_add: float,
    min_margin_add: float,
) -> RuleDefinition:
    return RuleDefinition(
        rule_id=rule_id,
        type="contextual_soft_suppressor",
        enabled=True,
        params={
            "context": context,
            "direction": direction,
            "threshold_add": threshold_add,
            "min_margin_add": min_margin_add,
        },
    )


def make_specialist_short_gate_rule(
    rule_id: str,
    *,
    min_aux_short_probability: float,
    context: str,
) -> RuleDefinition:
    return RuleDefinition(
        rule_id=rule_id,
        type="specialist_short_gate",
        enabled=True,
        params={
            "min_aux_short_probability": min_aux_short_probability,
            "context": context,
        },
    )


def make_state_exit_rule(
    rule_id: str,
    *,
    min_hold_bars: int,
    max_direction_margin: float,
) -> RuleDefinition:
    return RuleDefinition(
        rule_id=rule_id,
        type="state_exit_guard",
        enabled=True,
        params={
            "min_hold_bars": min_hold_bars,
            "max_direction_margin": max_direction_margin,
        },
    )


def base_context_rules() -> list[RuleDefinition]:
    return [
        make_contextual_soft_suppressor_rule(
            "filters_02",
            context="monday",
            direction="short",
            threshold_add=0.05,
            min_margin_add=0.05,
        ),
        make_contextual_soft_suppressor_rule(
            "filters_03",
            context="ny_postcash",
            direction="short",
            threshold_add=0.05,
            min_margin_add=0.03,
        ),
        make_contextual_soft_suppressor_rule(
            "filters_04",
            context="late_session",
            direction="long",
            threshold_add=0.02,
            min_margin_add=0.01,
        ),
    ]


def long_repair_light_rules() -> list[RuleDefinition]:
    return [
        make_contextual_soft_suppressor_rule(
            "filters_02",
            context="monday",
            direction="short",
            threshold_add=0.05,
            min_margin_add=0.05,
        ),
        make_contextual_soft_suppressor_rule(
            "filters_03",
            context="ny_postcash",
            direction="short",
            threshold_add=0.05,
            min_margin_add=0.03,
        ),
        make_contextual_soft_suppressor_rule(
            "filters_04",
            context="late_session",
            direction="long",
            threshold_add=0.03,
            min_margin_add=0.02,
        ),
    ]


def long_repair_medium_rules() -> list[RuleDefinition]:
    return [
        make_contextual_soft_suppressor_rule(
            "filters_02",
            context="monday",
            direction="short",
            threshold_add=0.05,
            min_margin_add=0.05,
        ),
        make_contextual_soft_suppressor_rule(
            "filters_03",
            context="ny_postcash",
            direction="short",
            threshold_add=0.05,
            min_margin_add=0.03,
        ),
        make_contextual_soft_suppressor_rule(
            "filters_04",
            context="monday",
            direction="long",
            threshold_add=0.02,
            min_margin_add=0.01,
        ),
        make_contextual_soft_suppressor_rule(
            "filters_05",
            context="late_session",
            direction="long",
            threshold_add=0.04,
            min_margin_add=0.03,
        ),
    ]


RUNS = [
    {
        "folder_name": "29A_25o_refcarry_0001",
        "experiment_id": "exp_29a_25o_refcarry_v1",
        "stage_id": "29A",
        "label": "plain 25O carry reference inside stage29",
        "context_rules": base_context_rules(),
        "extra_overrides": {
            "soft_context_label": "stage29_refcarry_25o",
            "stage29_wave1_label": "refcarry_25o",
        },
        "state_exit": None,
        "specialist_gate": None,
    },
    {
        "folder_name": "29B_25o_sx23g_0001",
        "experiment_id": "exp_29b_25o_sx23g_v1",
        "stage_id": "29B",
        "label": "25O plus stable 23G state exit",
        "context_rules": base_context_rules(),
        "extra_overrides": {
            "soft_context_label": "stage29_25o_plus_state_exit",
            "stage29_wave1_label": "state_exit_addon_23g",
        },
        "state_exit": make_state_exit_rule("exit_02", min_hold_bars=1, max_direction_margin=0.04),
        "specialist_gate": None,
    },
    {
        "folder_name": "29C_25o_gate24j_0001",
        "experiment_id": "exp_29c_25o_gate24j_v1",
        "stage_id": "29C",
        "label": "25O plus Monday or postcash specialist short gate",
        "context_rules": base_context_rules(),
        "extra_overrides": {
            "short_gate_source_label": "17C_2501_short_specialist_0001",
            "soft_context_label": "stage29_25o_plus_specialist_gate",
            "stage29_wave1_label": "specialist_gate_addon_24j",
        },
        "state_exit": None,
        "specialist_gate": make_specialist_short_gate_rule(
            "filters_90",
            min_aux_short_probability=0.4,
            context="monday_or_postcash",
        ),
    },
    {
        "folder_name": "29D_25o_gburst26m_0001",
        "experiment_id": "exp_29d_25o_gburst26m_v1",
        "stage_id": "29D",
        "label": "25O plus governance burst overlay",
        "context_rules": base_context_rules(),
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
            "soft_context_label": "stage29_25o_plus_gburst26m",
            "stage29_wave1_label": "governance_burst_addon_26m",
        },
        "state_exit": None,
        "specialist_gate": None,
    },
    {
        "folder_name": "29E_25o_gweak26o_0001",
        "experiment_id": "exp_29e_25o_gweak26o_v1",
        "stage_id": "29E",
        "label": "25O plus weak-pocket governance fusion",
        "context_rules": base_context_rules(),
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
            "soft_context_label": "stage29_25o_plus_gweak26o",
            "stage29_wave1_label": "governance_weak_pocket_addon_26o",
        },
        "state_exit": None,
        "specialist_gate": None,
    },
    {
        "folder_name": "29F_25o_vpost27m_0001",
        "experiment_id": "exp_29f_25o_vpost27m_v1",
        "stage_id": "29F",
        "label": "25O plus postcash high-vol short overlay",
        "context_rules": base_context_rules(),
        "extra_overrides": {
            "vol_overlay_label": "postcash_high_vol_short_092",
            "vol_risk_high_mult": 0.92,
            "vol_risk_high_threshold": 1.1,
            "vol_risk_mid_mult": 1.0,
            "vol_risk_low_mult": 1.0,
            "vol_risk_low_threshold": 0.9,
            "vol_overlay_context": "ny_postcash",
            "vol_overlay_direction": "short",
            "soft_context_label": "stage29_25o_plus_vpost27m",
            "stage29_wave1_label": "vol_postcash_short_addon_27m",
        },
        "state_exit": None,
        "specialist_gate": None,
    },
    {
        "folder_name": "29G_25o_lrepair1_0001",
        "experiment_id": "exp_29g_25o_lrepair1_v1",
        "stage_id": "29G",
        "label": "25O plus light long repair",
        "context_rules": long_repair_light_rules(),
        "extra_overrides": {
            "monday_long_hold_cap_bars": 3,
            "soft_context_label": "stage29_long_repair_light",
            "stage29_wave1_label": "long_repair_light",
        },
        "state_exit": None,
        "specialist_gate": None,
    },
    {
        "folder_name": "29H_25o_lrepair2_0001",
        "experiment_id": "exp_29h_25o_lrepair2_v1",
        "stage_id": "29H",
        "label": "25O plus medium long repair",
        "context_rules": long_repair_medium_rules(),
        "extra_overrides": {
            "monday_long_hold_cap_bars": 2,
            "soft_context_label": "stage29_long_repair_medium",
            "stage29_wave1_label": "long_repair_medium",
        },
        "state_exit": None,
        "specialist_gate": None,
    },
    {
        "folder_name": "29I_25o_sx23g_gburst_0001",
        "experiment_id": "exp_29i_25o_sx23g_gburst_v1",
        "stage_id": "29I",
        "label": "25O plus 23G state exit plus governance burst",
        "context_rules": base_context_rules(),
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
            "soft_context_label": "stage29_25o_state_exit_gburst",
            "stage29_wave1_label": "state_exit_plus_gburst",
        },
        "state_exit": make_state_exit_rule("exit_02", min_hold_bars=1, max_direction_margin=0.04),
        "specialist_gate": None,
    },
    {
        "folder_name": "29J_25o_sx23g_gweak_0001",
        "experiment_id": "exp_29j_25o_sx23g_gweak_v1",
        "stage_id": "29J",
        "label": "25O plus 23G state exit plus weak-pocket governance",
        "context_rules": base_context_rules(),
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
            "soft_context_label": "stage29_25o_state_exit_gweak",
            "stage29_wave1_label": "state_exit_plus_gweak",
        },
        "state_exit": make_state_exit_rule("exit_02", min_hold_bars=1, max_direction_margin=0.04),
        "specialist_gate": None,
    },
    {
        "folder_name": "29K_25o_sx23g_lrepair2_0001",
        "experiment_id": "exp_29k_25o_sx23g_lrepair2_v1",
        "stage_id": "29K",
        "label": "25O plus 23G state exit plus medium long repair",
        "context_rules": long_repair_medium_rules(),
        "extra_overrides": {
            "monday_long_hold_cap_bars": 2,
            "soft_context_label": "stage29_state_exit_long_repair_medium",
            "stage29_wave1_label": "state_exit_plus_long_repair_medium",
        },
        "state_exit": make_state_exit_rule("exit_02", min_hold_bars=1, max_direction_margin=0.04),
        "specialist_gate": None,
    },
    {
        "folder_name": "29L_25o_sx23g_gburst_l2_0001",
        "experiment_id": "exp_29l_25o_sx23g_gburst_l2_v1",
        "stage_id": "29L",
        "label": "25O plus 23G state exit plus governance burst plus medium long repair",
        "context_rules": long_repair_medium_rules(),
        "extra_overrides": {
            "monday_long_hold_cap_bars": 2,
            "governance_overlay_label": "burst_combo_mix_d3",
            "governance_signal_taper_max_argmax_share": 0.82,
            "governance_signal_taper_min_entropy": 0.90,
            "governance_signal_taper_mult": 0.90,
            "governance_signal_taper_mode": "either",
            "governance_signal_taper_duration_bars": 3,
            "governance_external_taper_max_skip_rate": 0.34,
            "governance_external_taper_mult": 0.90,
            "governance_external_taper_duration_bars": 3,
            "soft_context_label": "stage29_state_exit_gburst_long_repair_medium",
            "stage29_wave1_label": "state_exit_plus_gburst_plus_long_repair_medium",
        },
        "state_exit": make_state_exit_rule("exit_02", min_hold_bars=1, max_direction_margin=0.04),
        "specialist_gate": None,
    },
    {
        "folder_name": "29M_25o_sx23g_vpost_l2_0001",
        "experiment_id": "exp_29m_25o_sx23g_vpost_l2_v1",
        "stage_id": "29M",
        "label": "25O plus 23G state exit plus postcash high-vol short overlay plus medium long repair",
        "context_rules": long_repair_medium_rules(),
        "extra_overrides": {
            "monday_long_hold_cap_bars": 2,
            "vol_overlay_label": "postcash_high_vol_short_092",
            "vol_risk_high_mult": 0.92,
            "vol_risk_high_threshold": 1.1,
            "vol_risk_mid_mult": 1.0,
            "vol_risk_low_mult": 1.0,
            "vol_risk_low_threshold": 0.9,
            "vol_overlay_context": "ny_postcash",
            "vol_overlay_direction": "short",
            "soft_context_label": "stage29_state_exit_vpost_long_repair_medium",
            "stage29_wave1_label": "state_exit_plus_vol_postcash_plus_long_repair_medium",
        },
        "state_exit": make_state_exit_rule("exit_02", min_hold_bars=1, max_direction_margin=0.04),
        "specialist_gate": None,
    },
]


def filter_base_artifacts(bundle: ExperimentBundle):
    return [
        artifact
        for artifact in bundle.artifacts
        if not artifact.role.startswith("mt5_") and artifact.role != "short_gate_onnx_model"
    ]


def derive_core_filters(bundle: ExperimentBundle) -> list[RuleDefinition]:
    return [
        deepcopy(rule)
        for rule in bundle.rule_stack.filters
        if rule.type not in {"contextual_soft_suppressor", "specialist_short_gate"}
    ]


def derive_base_exit(bundle: ExperimentBundle) -> list[RuleDefinition]:
    return [deepcopy(rule) for rule in bundle.rule_stack.exit if rule.type != "state_exit_guard"]


def derive_base_extra(bundle: ExperimentBundle) -> dict[str, int | float | str]:
    extra = deepcopy(bundle.runtime_snapshot.extra)
    extra.pop("soft_context_label", None)
    for key in list(extra.keys()):
        if key.startswith("stage25_") or key.startswith("stage29_"):
            extra.pop(key, None)
    return extra


def upsert_capabilities(
    bundle: ExperimentBundle,
    *,
    context_rules: list[RuleDefinition],
    state_exit: RuleDefinition | None,
    specialist_gate: RuleDefinition | None,
    runtime_extra: dict[str, int | float | str],
) -> None:
    filtered = [
        capability
        for capability in bundle.compatibility.required_ea_capabilities
        if capability.name
        not in {
            "contextual_soft_suppressor",
            "late_session_context",
            "direction_hold_cap",
            "state_exit_guard",
            "specialist_short_gate",
            "specialist_short_gate_context",
            "governance_adaptive_overlay",
            "governance_adaptive_overlay_duration",
            "governance_adaptive_overlay_context_direction",
            "governance_signal_mode_switch",
            "volatility_risk_overlay",
            "volatility_overlay_context_direction",
            "volatility_hold_cap",
        }
    ]
    if context_rules:
        filtered.append(CapabilityRequirement(name="contextual_soft_suppressor", min_version="1.1"))
    if any(rule.params.get("context") == "late_session" for rule in context_rules):
        filtered.append(CapabilityRequirement(name="late_session_context", min_version="1.0"))
    if any(
        key in runtime_extra
        for key in {
            "ny_postcash_short_hold_cap_bars",
            "ny_postcash_long_hold_cap_bars",
            "monday_short_hold_cap_bars",
            "monday_long_hold_cap_bars",
        }
    ):
        filtered.append(CapabilityRequirement(name="direction_hold_cap", min_version="1.1"))
    if state_exit is not None:
        filtered.append(CapabilityRequirement(name="state_exit_guard", min_version="1.0"))
    if specialist_gate is not None:
        filtered.append(CapabilityRequirement(name="specialist_short_gate", min_version="1.0"))
        if specialist_gate.params.get("context") not in {None, "", "any"}:
            filtered.append(CapabilityRequirement(name="specialist_short_gate_context", min_version="1.0"))
    if any(key.startswith("governance_") for key in runtime_extra):
        filtered.append(CapabilityRequirement(name="governance_adaptive_overlay", min_version="1.1"))
        if (
            int(runtime_extra.get("governance_signal_taper_duration_bars", 1)) > 1
            or int(runtime_extra.get("governance_external_taper_duration_bars", 1)) > 1
        ):
            filtered.append(CapabilityRequirement(name="governance_adaptive_overlay_duration", min_version="1.0"))
        if "governance_overlay_context" in runtime_extra or "governance_overlay_direction" in runtime_extra:
            filtered.append(CapabilityRequirement(name="governance_adaptive_overlay_context_direction", min_version="1.0"))
        if "governance_signal_taper_mode" in runtime_extra:
            filtered.append(CapabilityRequirement(name="governance_signal_mode_switch", min_version="1.0"))
    if any(key.startswith("vol_") for key in runtime_extra):
        filtered.append(CapabilityRequirement(name="volatility_risk_overlay", min_version="1.0"))
        if "vol_overlay_context" in runtime_extra or "vol_overlay_direction" in runtime_extra:
            filtered.append(CapabilityRequirement(name="volatility_overlay_context_direction", min_version="1.0"))
        if any(key in runtime_extra for key in {"vol_high_hold_cap_bars", "vol_high_short_hold_cap_bars", "vol_high_long_hold_cap_bars"}):
            filtered.append(CapabilityRequirement(name="volatility_hold_cap", min_version="1.0"))
    bundle.compatibility.required_ea_capabilities = filtered


def main() -> int:
    if not SHORT_GATE_AUX_ONNX_SOURCE.exists():
        raise FileNotFoundError(f"missing short gate aux ONNX source: {SHORT_GATE_AUX_ONNX_SOURCE}")

    base_bundle = ExperimentBundle.from_json((BASE_RUN_DIR / "experiment_bundle.json").read_text(encoding="utf-8-sig"))
    core_filters = derive_core_filters(base_bundle)
    base_exit = derive_base_exit(base_bundle)
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
        bundle.identity.stage_name = "fusion_long_repair"
        bundle.identity.created_at_utc = utc_now_iso()
        bundle.identity.bundle_status = "ready"
        bundle.status_history = build_status_history()
        bundle.results = ResultsBlock()
        bundle.run_attempts = []
        bundle.artifacts = filter_base_artifacts(bundle)

        if run["specialist_gate"] is not None:
            aux_target_path = run_dir / "artifacts" / "short_gate_aux_17c.onnx"
            shutil.copy2(SHORT_GATE_AUX_ONNX_SOURCE, aux_target_path)
            bundle.artifacts.append(
                ArtifactRef(
                    artifact_id="art_short_gate_onnx",
                    role="short_gate_onnx_model",
                    path="artifacts/short_gate_aux_17c.onnx",
                    format="onnx",
                    sha256=sha256(aux_target_path),
                    required=True,
                )
            )

        bundle.rule_stack.filters = deepcopy(core_filters) + deepcopy(run["context_rules"])
        if run["specialist_gate"] is not None:
            bundle.rule_stack.filters.append(deepcopy(run["specialist_gate"]))
        bundle.rule_stack.exit = deepcopy(base_exit)
        if run["state_exit"] is not None:
            bundle.rule_stack.exit.append(deepcopy(run["state_exit"]))

        bundle.runtime_snapshot.extra = deepcopy(base_extra)
        bundle.runtime_snapshot.extra.update(run["extra_overrides"])

        upsert_capabilities(
            bundle,
            context_rules=run["context_rules"],
            state_exit=run["state_exit"],
            specialist_gate=run["specialist_gate"],
            runtime_extra=bundle.runtime_snapshot.extra,
        )

        (run_dir / "rule_stack.json").write_text(
            bundle.rule_stack.model_dump_json(indent=2, exclude_none=False),
            encoding="utf-8",
        )
        (run_dir / "experiment_bundle.json").write_text(bundle.to_json(indent=2), encoding="utf-8")
        print(f"[done] created={run_dir}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
