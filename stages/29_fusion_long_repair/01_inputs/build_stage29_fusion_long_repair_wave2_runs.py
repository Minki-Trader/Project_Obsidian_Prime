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
    / "25O_25d_ctx_exit_holdfusion_0001"
)
ACTIVE_RUNS_DIR = Path(__file__).resolve().parents[1] / "02_runs" / "active"
UTC = timezone.utc


def utc_now_iso() -> str:
    return datetime.now(tz=UTC).isoformat()


def build_status_history() -> list[StatusEvent]:
    now = utc_now_iso()
    return [
        StatusEvent(status="draft", changed_at_utc=now, reason="bundle_initialized_from_25O_carry_incumbent"),
        StatusEvent(status="ready", changed_at_utc=now, reason="stage29_fusion_long_repair_wave2_prepared"),
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


def make_state_exit_rule(
    rule_id: str,
    *,
    min_hold_bars: int,
    max_direction_margin: float,
    direction: str | None = None,
) -> RuleDefinition:
    params: dict[str, float | int | str] = {
        "min_hold_bars": min_hold_bars,
        "max_direction_margin": max_direction_margin,
    }
    if direction and direction not in {"", "both"}:
        params["direction"] = direction
    return RuleDefinition(
        rule_id=rule_id,
        type="state_exit_guard",
        enabled=True,
        params=params,
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


def make_gweak_extra(label: str) -> dict[str, int | float | str]:
    return {
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
        "soft_context_label": f"stage29_wave2_{label}",
        "stage29_wave2_label": label,
    }


def make_plain_extra(label: str) -> dict[str, int | float | str]:
    return {
        "soft_context_label": f"stage29_wave2_{label}",
        "stage29_wave2_label": label,
    }


RUNS = [
    {
        "folder_name": "29N_25o_sxh2_0001",
        "experiment_id": "exp_29n_25o_sxh2_v1",
        "stage_id": "29N",
        "label": "25O plus slower state exit h2 margin 0.04",
        "context_rules": base_context_rules(),
        "state_exit_rules": [
            make_state_exit_rule("exit_02", min_hold_bars=2, max_direction_margin=0.04),
        ],
        "extra_overrides": make_plain_extra("state_exit_h2_margin004"),
    },
    {
        "folder_name": "29O_25o_sxloose_0001",
        "experiment_id": "exp_29o_25o_sxloose_v1",
        "stage_id": "29O",
        "label": "25O plus looser state exit h1 margin 0.05",
        "context_rules": base_context_rules(),
        "state_exit_rules": [
            make_state_exit_rule("exit_02", min_hold_bars=1, max_direction_margin=0.05),
        ],
        "extra_overrides": make_plain_extra("state_exit_h1_margin005"),
    },
    {
        "folder_name": "29P_25o_sxlock1_0001",
        "experiment_id": "exp_29p_25o_sxlock1_v1",
        "stage_id": "29P",
        "label": "25O plus state exit h1 margin 0.04 with one-bar lock",
        "context_rules": base_context_rules(),
        "state_exit_rules": [
            make_state_exit_rule("exit_02", min_hold_bars=1, max_direction_margin=0.04),
        ],
        "extra_overrides": {
            **make_plain_extra("state_exit_h1_margin004_lock1"),
            "state_exit_reentry_lock_bars": 1,
        },
    },
    {
        "folder_name": "29Q_25o_sxshort_0001",
        "experiment_id": "exp_29q_25o_sxshort_v1",
        "stage_id": "29Q",
        "label": "25O plus short-only state exit h1 margin 0.04",
        "context_rules": base_context_rules(),
        "state_exit_rules": [
            make_state_exit_rule("exit_02", min_hold_bars=1, max_direction_margin=0.04, direction="short"),
        ],
        "extra_overrides": make_plain_extra("state_exit_short_only_h1_margin004"),
    },
    {
        "folder_name": "29R_25o_sxdirls_0001",
        "experiment_id": "exp_29r_25o_sxdirls_v1",
        "stage_id": "29R",
        "label": "25O plus long-loose short-tight directional state exit",
        "context_rules": base_context_rules(),
        "state_exit_rules": [
            make_state_exit_rule("exit_02", min_hold_bars=1, max_direction_margin=0.05, direction="long"),
            make_state_exit_rule("exit_03", min_hold_bars=1, max_direction_margin=0.03, direction="short"),
        ],
        "extra_overrides": make_plain_extra("state_exit_dirsplit_long005_short003"),
    },
    {
        "folder_name": "29S_25o_sxh2_gweak_0001",
        "experiment_id": "exp_29s_25o_sxh2_gweak_v1",
        "stage_id": "29S",
        "label": "25O plus slower state exit h2 margin 0.04 plus weak-pocket governance",
        "context_rules": base_context_rules(),
        "state_exit_rules": [
            make_state_exit_rule("exit_02", min_hold_bars=2, max_direction_margin=0.04),
        ],
        "extra_overrides": make_gweak_extra("state_exit_h2_margin004_gweak"),
    },
    {
        "folder_name": "29T_25o_sxloose_gweak_0001",
        "experiment_id": "exp_29t_25o_sxloose_gweak_v1",
        "stage_id": "29T",
        "label": "25O plus looser state exit h1 margin 0.05 plus weak-pocket governance",
        "context_rules": base_context_rules(),
        "state_exit_rules": [
            make_state_exit_rule("exit_02", min_hold_bars=1, max_direction_margin=0.05),
        ],
        "extra_overrides": make_gweak_extra("state_exit_h1_margin005_gweak"),
    },
    {
        "folder_name": "29U_25o_sxlock1_gweak_0001",
        "experiment_id": "exp_29u_25o_sxlock1_gweak_v1",
        "stage_id": "29U",
        "label": "25O plus state exit h1 margin 0.04 with one-bar lock plus weak-pocket governance",
        "context_rules": base_context_rules(),
        "state_exit_rules": [
            make_state_exit_rule("exit_02", min_hold_bars=1, max_direction_margin=0.04),
        ],
        "extra_overrides": {
            **make_gweak_extra("state_exit_h1_margin004_lock1_gweak"),
            "state_exit_reentry_lock_bars": 1,
        },
    },
    {
        "folder_name": "29V_25o_sxshort_gweak_0001",
        "experiment_id": "exp_29v_25o_sxshort_gweak_v1",
        "stage_id": "29V",
        "label": "25O plus short-only state exit h1 margin 0.04 plus weak-pocket governance",
        "context_rules": base_context_rules(),
        "state_exit_rules": [
            make_state_exit_rule("exit_02", min_hold_bars=1, max_direction_margin=0.04, direction="short"),
        ],
        "extra_overrides": make_gweak_extra("state_exit_short_only_h1_margin004_gweak"),
    },
    {
        "folder_name": "29W_25o_sxdirls_gweak_0001",
        "experiment_id": "exp_29w_25o_sxdirls_gweak_v1",
        "stage_id": "29W",
        "label": "25O plus long-loose short-tight directional state exit plus weak-pocket governance",
        "context_rules": base_context_rules(),
        "state_exit_rules": [
            make_state_exit_rule("exit_02", min_hold_bars=1, max_direction_margin=0.05, direction="long"),
            make_state_exit_rule("exit_03", min_hold_bars=1, max_direction_margin=0.03, direction="short"),
        ],
        "extra_overrides": make_gweak_extra("state_exit_dirsplit_long005_short003_gweak"),
    },
]


def filter_base_artifacts(bundle: ExperimentBundle):
    return [artifact for artifact in bundle.artifacts if not artifact.role.startswith("mt5_")]


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
    state_exit_rules: list[RuleDefinition],
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
            "state_exit_guard_directional",
            "state_exit_reentry_lock",
            "governance_adaptive_overlay",
            "governance_adaptive_overlay_duration",
            "governance_adaptive_overlay_context_direction",
            "governance_signal_mode_switch",
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
    if state_exit_rules:
        filtered.append(CapabilityRequirement(name="state_exit_guard", min_version="1.1"))
    if any("direction" in rule.params for rule in state_exit_rules):
        filtered.append(CapabilityRequirement(name="state_exit_guard_directional", min_version="1.0"))
    if int(runtime_extra.get("state_exit_reentry_lock_bars", 0)) > 0:
        filtered.append(CapabilityRequirement(name="state_exit_reentry_lock", min_version="1.0"))
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
    bundle.compatibility.required_ea_capabilities = filtered


def main() -> int:
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

        bundle.rule_stack.filters = deepcopy(core_filters) + deepcopy(run["context_rules"])
        bundle.rule_stack.exit = deepcopy(base_exit) + deepcopy(run["state_exit_rules"])

        bundle.runtime_snapshot.extra = deepcopy(base_extra)
        bundle.runtime_snapshot.extra.update(run["extra_overrides"])

        upsert_capabilities(
            bundle,
            context_rules=run["context_rules"],
            state_exit_rules=run["state_exit_rules"],
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
