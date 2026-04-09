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
    / "23_state_conditioned_exit"
    / "02_runs"
    / "active"
    / "23A_22q_base_stateexit_ref_0001"
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
        StatusEvent(status="draft", changed_at_utc=now, reason="bundle_initialized_from_23A_regular_reference"),
        StatusEvent(status="ready", changed_at_utc=now, reason="stage24_gated_specialist_wave1_prepared"),
    ]


def make_specialist_short_gate_rule(rule_id: str, min_aux_short_probability: float) -> RuleDefinition:
    return RuleDefinition(
        rule_id=rule_id,
        type="specialist_short_gate",
        enabled=True,
        params={
            "min_aux_short_probability": min_aux_short_probability,
        },
    )


RUNS = [
    {
        "folder_name": "24A_23a_base_gate_ref_0001",
        "experiment_id": "exp_24a_23a_base_gate_ref_v1",
        "stage_id": "24A",
        "gate_threshold": None,
    },
    {
        "folder_name": "24B_23a_17csg040_gate_0001",
        "experiment_id": "exp_24b_23a_17csg040_gate_v1",
        "stage_id": "24B",
        "gate_threshold": 0.40,
    },
    {
        "folder_name": "24C_23a_17csg045_gate_0001",
        "experiment_id": "exp_24c_23a_17csg045_gate_v1",
        "stage_id": "24C",
        "gate_threshold": 0.45,
    },
    {
        "folder_name": "24D_23a_17csg050_gate_0001",
        "experiment_id": "exp_24d_23a_17csg050_gate_v1",
        "stage_id": "24D",
        "gate_threshold": 0.50,
    },
]


def filter_base_artifacts(bundle: ExperimentBundle) -> list[ArtifactRef]:
    return [artifact for artifact in bundle.artifacts if not artifact.role.startswith("mt5_") and artifact.role != "short_gate_onnx_model"]


def upsert_short_gate_capability(bundle: ExperimentBundle, gate_enabled: bool) -> None:
    bundle.compatibility.required_ea_capabilities = [
        capability
        for capability in bundle.compatibility.required_ea_capabilities
        if capability.name != "specialist_short_gate"
    ]
    if gate_enabled:
        bundle.compatibility.required_ea_capabilities.append(
            CapabilityRequirement(name="specialist_short_gate", min_version="1.0")
        )


def main() -> int:
    if not AUX_ONNX_SOURCE.exists():
        raise FileNotFoundError(f"missing aux ONNX source: {AUX_ONNX_SOURCE}")

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
        bundle.identity.stage_name = "gated_specialist_overlay"
        bundle.identity.created_at_utc = utc_now_iso()
        bundle.identity.bundle_status = "ready"
        bundle.status_history = build_status_history()
        bundle.results = ResultsBlock()
        bundle.run_attempts = []
        bundle.artifacts = filter_base_artifacts(bundle)

        gate_threshold = run["gate_threshold"]
        base_filters = deepcopy(base_bundle.rule_stack.filters)
        if gate_threshold is None:
            bundle.rule_stack.filters = base_filters
            bundle.runtime_snapshot.extra.pop("short_gate_source_label", None)
            bundle.runtime_snapshot.extra.pop("short_gate_min_aux_short_probability", None)
        else:
            bundle.rule_stack.filters = base_filters + [
                make_specialist_short_gate_rule("filters_02", gate_threshold)
            ]
            bundle.runtime_snapshot.extra["short_gate_source_label"] = "17C_2501_short_specialist_0001"
            bundle.runtime_snapshot.extra["short_gate_min_aux_short_probability"] = gate_threshold
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

        upsert_short_gate_capability(bundle, gate_threshold is not None)

        (run_dir / "rule_stack.json").write_text(
            bundle.rule_stack.model_dump_json(indent=2, exclude_none=False),
            encoding="utf-8",
        )
        (run_dir / "experiment_bundle.json").write_text(bundle.to_json(indent=2), encoding="utf-8")
        print(f"[done] created={run_dir}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
