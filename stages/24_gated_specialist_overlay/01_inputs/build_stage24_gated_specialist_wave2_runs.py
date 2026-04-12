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
    / "24_gated_specialist_overlay"
    / "02_runs"
    / "active"
    / "24A_23a_base_gate_ref_0001"
)
AUX_ONNX_SOURCE = (
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
        StatusEvent(status="draft", changed_at_utc=now, reason="bundle_initialized_from_24A_regular_reference"),
        StatusEvent(status="ready", changed_at_utc=now, reason="stage24_gated_specialist_wave2_prepared"),
    ]


def make_specialist_short_gate_rule(
    rule_id: str,
    *,
    min_aux_short_probability: float | None = None,
    min_aux_short_margin: float | None = None,
    context: str | None = None,
) -> RuleDefinition:
    params: dict[str, float | str] = {}
    if min_aux_short_probability is not None:
        params["min_aux_short_probability"] = min_aux_short_probability
    if min_aux_short_margin is not None:
        params["min_aux_short_margin"] = min_aux_short_margin
    if context:
        params["context"] = context
    return RuleDefinition(
        rule_id=rule_id,
        type="specialist_short_gate",
        enabled=True,
        params=params,
    )


RUNS = [
    {
        "folder_name": "24E_24a_17csg038_gate_0001",
        "experiment_id": "exp_24e_24a_17csg038_gate_v1",
        "stage_id": "24E",
        "label": "denser aux short threshold 0.38 hard gate",
        "gate_rule": make_specialist_short_gate_rule("filters_02", min_aux_short_probability=0.38),
        "extra_overrides": {
            "short_gate_source_label": "17C_2501_short_specialist_0001",
            "stage24_wave2_label": "local_threshold_038",
        },
    },
    {
        "folder_name": "24F_24a_17csg042_gate_0001",
        "experiment_id": "exp_24f_24a_17csg042_gate_v1",
        "stage_id": "24F",
        "label": "denser aux short threshold 0.42 hard gate",
        "gate_rule": make_specialist_short_gate_rule("filters_02", min_aux_short_probability=0.42),
        "extra_overrides": {
            "short_gate_source_label": "17C_2501_short_specialist_0001",
            "stage24_wave2_label": "local_threshold_042",
        },
    },
    {
        "folder_name": "24G_24a_17csg040_lowmargin_0001",
        "experiment_id": "exp_24g_24a_17csg040_lowmargin_v1",
        "stage_id": "24G",
        "label": "gate only on low-margin shorts",
        "gate_rule": make_specialist_short_gate_rule("filters_02", min_aux_short_probability=0.40),
        "extra_overrides": {
            "short_gate_source_label": "17C_2501_short_specialist_0001",
            "specialist_short_gate_max_primary_direction_margin_to_apply": 0.05,
            "stage24_wave2_label": "local_low_margin_only_gate",
        },
    },
    {
        "folder_name": "24H_24a_17csg040_softt030_0001",
        "experiment_id": "exp_24h_24a_17csg040_softt030_v1",
        "stage_id": "24H",
        "label": "soft gate penalty via threshold add",
        "gate_rule": make_specialist_short_gate_rule("filters_02", min_aux_short_probability=0.40),
        "extra_overrides": {
            "short_gate_source_label": "17C_2501_short_specialist_0001",
            "specialist_short_gate_fail_mode": "soft_penalty",
            "specialist_short_gate_soft_threshold_add": 0.03,
            "stage24_wave2_label": "local_soft_threshold_penalty",
        },
    },
    {
        "folder_name": "24I_24a_17csg040_monshort_0001",
        "experiment_id": "exp_24i_24a_17csg040_monshort_v1",
        "stage_id": "24I",
        "label": "Monday short-only hard gate",
        "gate_rule": make_specialist_short_gate_rule(
            "filters_02",
            min_aux_short_probability=0.40,
            context="monday",
        ),
        "extra_overrides": {
            "short_gate_source_label": "17C_2501_short_specialist_0001",
            "stage24_wave2_label": "local_monday_short_gate",
        },
    },
    {
        "folder_name": "24J_24a_17csg040_monpost_0001",
        "experiment_id": "exp_24j_24a_17csg040_monpost_v1",
        "stage_id": "24J",
        "label": "weak-pocket contextual gate for Monday or postcash shorts",
        "gate_rule": make_specialist_short_gate_rule(
            "filters_02",
            min_aux_short_probability=0.40,
            context="monday_or_postcash",
        ),
        "extra_overrides": {
            "short_gate_source_label": "17C_2501_short_specialist_0001",
            "stage24_wave2_label": "expansion_contextual_weak_pocket_gate",
        },
    },
    {
        "folder_name": "24K_24a_17cbnd38_44_madd03_0001",
        "experiment_id": "exp_24k_24a_17cbnd38_44_madd03_v1",
        "stage_id": "24K",
        "label": "confidence band gate reject-low penalty-mid pass-high",
        "gate_rule": make_specialist_short_gate_rule("filters_02"),
        "extra_overrides": {
            "short_gate_source_label": "17C_2501_short_specialist_0001",
            "specialist_short_gate_soft_min_margin_add": 0.03,
            "specialist_short_gate_confidence_reject_below": 0.38,
            "specialist_short_gate_confidence_penalty_below": 0.44,
            "stage24_wave2_label": "expansion_confidence_band_gate",
        },
    },
    {
        "folder_name": "24L_24a_17csg040_jointpm05_0001",
        "experiment_id": "exp_24l_24a_17csg040_jointpm05_v1",
        "stage_id": "24L",
        "label": "joint gate with primary short margin floor",
        "gate_rule": make_specialist_short_gate_rule("filters_02", min_aux_short_probability=0.40),
        "extra_overrides": {
            "short_gate_source_label": "17C_2501_short_specialist_0001",
            "specialist_short_gate_min_primary_direction_margin": 0.05,
            "stage24_wave2_label": "expansion_joint_primary_margin_gate",
        },
    },
    {
        "folder_name": "24M_24a_17csg040_monpost_soft_0001",
        "experiment_id": "exp_24m_24a_17csg040_monpost_soft_v1",
        "stage_id": "24M",
        "label": "contextual low-margin soft gate on weak short pockets",
        "gate_rule": make_specialist_short_gate_rule(
            "filters_02",
            min_aux_short_probability=0.40,
            context="monday_or_postcash",
        ),
        "extra_overrides": {
            "short_gate_source_label": "17C_2501_short_specialist_0001",
            "specialist_short_gate_fail_mode": "soft_penalty",
            "specialist_short_gate_soft_threshold_add": 0.02,
            "specialist_short_gate_max_primary_direction_margin_to_apply": 0.05,
            "stage24_wave2_label": "expansion_contextual_low_margin_soft_gate",
        },
    },
]


def filter_base_artifacts(bundle: ExperimentBundle) -> list[ArtifactRef]:
    return [artifact for artifact in bundle.artifacts if not artifact.role.startswith("mt5_") and artifact.role != "short_gate_onnx_model"]


def upsert_short_gate_capabilities(
    bundle: ExperimentBundle,
    gate_rule: RuleDefinition,
    extra_overrides: dict[str, int | float | str],
) -> None:
    filtered = [
        capability
        for capability in bundle.compatibility.required_ea_capabilities
        if capability.name
        not in {
            "specialist_short_gate",
            "specialist_short_gate_context",
            "specialist_short_gate_soft_penalty",
            "specialist_short_gate_confidence_band",
            "specialist_short_gate_joint_primary_margin",
        }
    ]
    filtered.append(CapabilityRequirement(name="specialist_short_gate", min_version="1.1"))
    if "specialist_short_gate_fail_mode" in extra_overrides:
        filtered.append(CapabilityRequirement(name="specialist_short_gate_soft_penalty", min_version="1.0"))
    if "specialist_short_gate_confidence_penalty_below" in extra_overrides:
        filtered.append(CapabilityRequirement(name="specialist_short_gate_confidence_band", min_version="1.0"))
    if "specialist_short_gate_min_primary_direction_margin" in extra_overrides:
        filtered.append(CapabilityRequirement(name="specialist_short_gate_joint_primary_margin", min_version="1.0"))
    if gate_rule.params.get("context") is not None or "specialist_short_gate_max_primary_direction_margin_to_apply" in extra_overrides:
        filtered.append(CapabilityRequirement(name="specialist_short_gate_context", min_version="1.0"))
    bundle.compatibility.required_ea_capabilities = filtered


def main() -> int:
    if not AUX_ONNX_SOURCE.exists():
        raise FileNotFoundError(f"missing aux ONNX source: {AUX_ONNX_SOURCE}")

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
        bundle.identity.stage_name = "gated_specialist_overlay"
        bundle.identity.created_at_utc = utc_now_iso()
        bundle.identity.bundle_status = "ready"
        bundle.status_history = build_status_history()
        bundle.results = ResultsBlock()
        bundle.run_attempts = []
        bundle.artifacts = filter_base_artifacts(bundle)

        aux_target_path = run_dir / "artifacts" / "short_gate_aux_17c.onnx"
        shutil.copy2(AUX_ONNX_SOURCE, aux_target_path)
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

        bundle.rule_stack.filters = deepcopy(base_filters) + [deepcopy(run["gate_rule"])]
        bundle.runtime_snapshot.extra = deepcopy(base_extra)
        bundle.runtime_snapshot.extra.update(run["extra_overrides"])
        upsert_short_gate_capabilities(bundle, run["gate_rule"], run["extra_overrides"])

        (run_dir / "rule_stack.json").write_text(
            bundle.rule_stack.model_dump_json(indent=2, exclude_none=False),
            encoding="utf-8",
        )
        (run_dir / "experiment_bundle.json").write_text(bundle.to_json(indent=2), encoding="utf-8")
        print(f"[done] created={run_dir}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
