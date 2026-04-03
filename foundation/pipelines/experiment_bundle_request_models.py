#!/usr/bin/env python3
from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from foundation.pipelines.experiment_bundle_models import (
    CapabilityRequirement,
    DataSnapshot,
    ExternalInputRequirement,
    OutputSchema,
    RuleStack,
    RuntimeSnapshot,
)


EXPECTED_PROBS3_ORDER = ["p_short", "p_flat", "p_long"]


class RequestBaseModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class IdentityRequest(RequestBaseModel):
    experiment_id: str
    stage_id: str
    stage_name: str
    bundle_version: str = "1.0.0"
    created_by: str = "python_orchestrator"
    created_at_utc: str | None = None


class ArtifactRequest(RequestBaseModel):
    artifact_id: str
    role: str
    path: str
    format: str
    required: bool


class FeatureSchemaRequest(RequestBaseModel):
    feature_count: int | None = None
    order_version: str
    feature_schema_artifact_id: str
    feature_fingerprint: str | None = None


class CompatibilityRequest(RequestBaseModel):
    schema_version: str = "1.0.0"
    min_ea_bundle_support_version: str = "1.0.0"
    required_ea_capabilities: list[CapabilityRequirement] = Field(default_factory=list)
    required_hash_artifact_ids: list[str] | None = None
    mismatch_policy: Literal["fail_fast"] = "fail_fast"


class SmokeArraySpec(RequestBaseModel):
    path: str
    format: Literal["json", "npy"]
    key: str | None = None


class SmokeTestRequest(RequestBaseModel):
    onnx_artifact_id: str
    input: SmokeArraySpec
    expected_output: SmokeArraySpec
    atol: float = 1e-6
    rtol: float = 1e-5


class BundleBuildRequest(RequestBaseModel):
    identity: IdentityRequest
    artifacts: list[ArtifactRequest]
    feature_schema: FeatureSchemaRequest
    output_schema: OutputSchema = Field(
        default_factory=lambda: OutputSchema(schema_type="probs3", output_order=EXPECTED_PROBS3_ORDER)
    )
    external_inputs: list[ExternalInputRequirement] = Field(default_factory=list)
    data_snapshot: DataSnapshot
    runtime_snapshot: RuntimeSnapshot
    rule_stack: RuleStack
    compatibility: CompatibilityRequest = Field(default_factory=CompatibilityRequest)
    smoke_test: SmokeTestRequest


__all__ = [
    "ArtifactRequest",
    "BundleBuildRequest",
    "CompatibilityRequest",
    "EXPECTED_PROBS3_ORDER",
    "FeatureSchemaRequest",
    "IdentityRequest",
    "RequestBaseModel",
    "SmokeArraySpec",
    "SmokeTestRequest",
]
