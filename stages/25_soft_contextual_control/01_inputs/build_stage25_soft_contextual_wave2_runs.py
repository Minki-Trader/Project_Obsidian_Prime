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
        StatusEvent(status="draft", changed_at_utc=now, reason="bundle_initialized_from_25D_incumbent"),
        StatusEvent(status="ready", changed_at_utc=now, reason="stage25_soft_contextual_wave2_prepared"),
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


RUNS = [
    {
        "folder_name": "25E_25d_thronly_monpost_0001",
        "experiment_id": "exp_25e_25d_thronly_monpost_v1",
        "stage_id": "25E",
        "label": "threshold-add ablation for Monday and postcash shorts",
        "context_rules": [
            make_contextual_soft_suppressor_rule("filters_02", context="monday", direction="short", threshold_add=0.05, min_margin_add=0.0),
            make_contextual_soft_suppressor_rule("filters_03", context="ny_postcash", direction="short", threshold_add=0.05, min_margin_add=0.0),
        ],
        "extra_overrides": {
            "soft_context_label": "threshold_only_monpost_short",
            "stage25_wave2_label": "local_threshold_add_ablation",
        },
    },
    {
        "folder_name": "25F_25d_marginonly_monpost_0001",
        "experiment_id": "exp_25f_25d_marginonly_monpost_v1",
        "stage_id": "25F",
        "label": "min-margin-add ablation for Monday and postcash shorts",
        "context_rules": [
            make_contextual_soft_suppressor_rule("filters_02", context="monday", direction="short", threshold_add=0.0, min_margin_add=0.05),
            make_contextual_soft_suppressor_rule("filters_03", context="ny_postcash", direction="short", threshold_add=0.0, min_margin_add=0.03),
        ],
        "extra_overrides": {
            "soft_context_label": "margin_only_monpost_short",
            "stage25_wave2_label": "local_min_margin_add_ablation",
        },
    },
    {
        "folder_name": "25G_25d_holdonly_posth2_0001",
        "experiment_id": "exp_25g_25d_holdonly_posth2_v1",
        "stage_id": "25G",
        "label": "hold-cap-only ablation with postcash short cap 2",
        "context_rules": [],
        "extra_overrides": {
            "ny_postcash_short_hold_cap_bars": 2,
            "soft_context_label": "hold_only_postcash_short_h2",
            "stage25_wave2_label": "local_hold_only_ablation_h2",
        },
    },
    {
        "folder_name": "25H_25d_holdonly_posth1_0001",
        "experiment_id": "exp_25h_25d_holdonly_posth1_v1",
        "stage_id": "25H",
        "label": "postcash short hold cap 1",
        "context_rules": [],
        "extra_overrides": {
            "ny_postcash_short_hold_cap_bars": 1,
            "soft_context_label": "hold_only_postcash_short_h1",
            "stage25_wave2_label": "local_postcash_hold_cap_1",
        },
    },
    {
        "folder_name": "25I_25d_holdonly_posth3_0001",
        "experiment_id": "exp_25i_25d_holdonly_posth3_v1",
        "stage_id": "25I",
        "label": "postcash short hold cap 3",
        "context_rules": [],
        "extra_overrides": {
            "ny_postcash_short_hold_cap_bars": 3,
            "soft_context_label": "hold_only_postcash_short_h3",
            "stage25_wave2_label": "local_postcash_hold_cap_3",
        },
    },
    {
        "folder_name": "25J_25d_monlight_0001",
        "experiment_id": "exp_25j_25d_monlight_v1",
        "stage_id": "25J",
        "label": "Monday short suppressor light",
        "context_rules": [
            make_contextual_soft_suppressor_rule("filters_02", context="monday", direction="short", threshold_add=0.03, min_margin_add=0.02),
        ],
        "extra_overrides": {
            "soft_context_label": "monday_short_light",
            "stage25_wave2_label": "local_monday_light",
        },
    },
    {
        "folder_name": "25K_25d_monmedium_0001",
        "experiment_id": "exp_25k_25d_monmedium_v1",
        "stage_id": "25K",
        "label": "Monday short suppressor medium",
        "context_rules": [
            make_contextual_soft_suppressor_rule("filters_02", context="monday", direction="short", threshold_add=0.05, min_margin_add=0.05),
        ],
        "extra_overrides": {
            "soft_context_label": "monday_short_medium",
            "stage25_wave2_label": "local_monday_medium",
        },
    },
    {
        "folder_name": "25L_25d_monstrong_0001",
        "experiment_id": "exp_25l_25d_monstrong_v1",
        "stage_id": "25L",
        "label": "Monday short suppressor strong",
        "context_rules": [
            make_contextual_soft_suppressor_rule("filters_02", context="monday", direction="short", threshold_add=0.07, min_margin_add=0.07),
        ],
        "extra_overrides": {
            "soft_context_label": "monday_short_strong",
            "stage25_wave2_label": "local_monday_strong",
        },
    },
    {
        "folder_name": "25M_25d_asym_latelong_0001",
        "experiment_id": "exp_25m_25d_asym_latelong_v1",
        "stage_id": "25M",
        "label": "direction-asymmetric extension with late-session long penalty",
        "context_rules": [
            make_contextual_soft_suppressor_rule("filters_02", context="monday", direction="short", threshold_add=0.05, min_margin_add=0.05),
            make_contextual_soft_suppressor_rule("filters_03", context="ny_postcash", direction="short", threshold_add=0.05, min_margin_add=0.03),
            make_contextual_soft_suppressor_rule("filters_04", context="late_session", direction="long", threshold_add=0.02, min_margin_add=0.01),
        ],
        "extra_overrides": {
            "ny_postcash_short_hold_cap_bars": 2,
            "soft_context_label": "asym_short_plus_late_long",
            "stage25_wave2_label": "expansion_direction_asymmetric_long_probe",
        },
    },
    {
        "folder_name": "25N_25d_pocketmap_latelong_0001",
        "experiment_id": "exp_25n_25d_pocketmap_latelong_v1",
        "stage_id": "25N",
        "label": "session-direction pocket map with late-session long pocket",
        "context_rules": [
            make_contextual_soft_suppressor_rule("filters_02", context="monday", direction="short", threshold_add=0.05, min_margin_add=0.05),
            make_contextual_soft_suppressor_rule("filters_03", context="ny_postcash", direction="short", threshold_add=0.05, min_margin_add=0.03),
            make_contextual_soft_suppressor_rule("filters_04", context="late_session", direction="long", threshold_add=0.03, min_margin_add=0.02),
        ],
        "extra_overrides": {
            "ny_postcash_short_hold_cap_bars": 2,
            "soft_context_label": "pocket_map_mon_post_late_long",
            "stage25_wave2_label": "expansion_session_direction_pocket_map",
        },
    },
    {
        "folder_name": "25O_25d_ctx_exit_holdfusion_0001",
        "experiment_id": "exp_25o_25d_ctx_exit_holdfusion_v1",
        "stage_id": "25O",
        "label": "soft contextual exit fusion with pocket-specific hold cuts",
        "context_rules": [
            make_contextual_soft_suppressor_rule("filters_02", context="monday", direction="short", threshold_add=0.05, min_margin_add=0.05),
            make_contextual_soft_suppressor_rule("filters_03", context="ny_postcash", direction="short", threshold_add=0.05, min_margin_add=0.03),
            make_contextual_soft_suppressor_rule("filters_04", context="late_session", direction="long", threshold_add=0.02, min_margin_add=0.01),
        ],
        "extra_overrides": {
            "monday_short_hold_cap_bars": 2,
            "ny_postcash_short_hold_cap_bars": 2,
            "soft_context_label": "contextual_entry_exit_hold_fusion",
            "stage25_wave2_label": "expansion_contextual_exit_hold_caps",
        },
    },
]


def filter_base_artifacts(bundle: ExperimentBundle):
    return [artifact for artifact in bundle.artifacts if not artifact.role.startswith("mt5_")]


def derive_base_filters(bundle: ExperimentBundle) -> list[RuleDefinition]:
    return [deepcopy(rule) for rule in bundle.rule_stack.filters if rule.type != "contextual_soft_suppressor"]


def derive_base_extra(bundle: ExperimentBundle) -> dict[str, int | float | str]:
    extra = deepcopy(bundle.runtime_snapshot.extra)
    extra.pop("soft_context_label", None)
    extra.pop("ny_postcash_short_hold_cap_bars", None)
    extra.pop("monday_short_hold_cap_bars", None)
    extra.pop("monday_long_hold_cap_bars", None)
    return extra


def upsert_capabilities(
    bundle: ExperimentBundle,
    *,
    context_rules: list[RuleDefinition],
    extra_overrides: dict[str, int | float | str],
) -> None:
    filtered = [
        capability
        for capability in bundle.compatibility.required_ea_capabilities
        if capability.name not in {"contextual_soft_suppressor", "direction_hold_cap", "late_session_context"}
    ]
    if context_rules:
        filtered.append(CapabilityRequirement(name="contextual_soft_suppressor", min_version="1.1"))
    if any(rule.params.get("context") == "late_session" for rule in context_rules):
        filtered.append(CapabilityRequirement(name="late_session_context", min_version="1.0"))
    if any(
        key in extra_overrides
        for key in {
            "ny_postcash_short_hold_cap_bars",
            "ny_postcash_long_hold_cap_bars",
            "monday_short_hold_cap_bars",
            "monday_long_hold_cap_bars",
        }
    ):
        filtered.append(CapabilityRequirement(name="direction_hold_cap", min_version="1.1"))
    bundle.compatibility.required_ea_capabilities = filtered


def main() -> int:
    base_bundle = ExperimentBundle.from_json((BASE_RUN_DIR / "experiment_bundle.json").read_text(encoding="utf-8-sig"))
    base_filters = derive_base_filters(base_bundle)
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
        bundle.identity.stage_name = "soft_contextual_thresholds_hold_control"
        bundle.identity.created_at_utc = utc_now_iso()
        bundle.identity.bundle_status = "ready"
        bundle.status_history = build_status_history()
        bundle.results = ResultsBlock()
        bundle.run_attempts = []
        bundle.artifacts = filter_base_artifacts(bundle)

        bundle.rule_stack.filters = deepcopy(base_filters) + deepcopy(run["context_rules"])
        bundle.runtime_snapshot.extra = deepcopy(base_extra)
        bundle.runtime_snapshot.extra.update(run["extra_overrides"])
        upsert_capabilities(bundle, context_rules=run["context_rules"], extra_overrides=run["extra_overrides"])

        (run_dir / "rule_stack.json").write_text(
            bundle.rule_stack.model_dump_json(indent=2, exclude_none=False),
            encoding="utf-8",
        )
        (run_dir / "experiment_bundle.json").write_text(bundle.to_json(indent=2), encoding="utf-8")
        print(f"[done] created={run_dir}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
