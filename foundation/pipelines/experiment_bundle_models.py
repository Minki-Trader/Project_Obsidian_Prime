#!/usr/bin/env python3
from __future__ import annotations

import json
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, ValidationError, field_validator, model_validator


JsonValue = Any
TesterModel = Literal["real_ticks"]

BundleStatus = Literal["draft", "ready", "running", "completed", "failed"]
SchemaType = Literal["probs3"]
AlignmentRule = Literal["exact_closed_bar_match"]
MismatchPolicy = Literal["fail_fast"]

EXPECTED_PROBS3_ORDER = ["p_short", "p_flat", "p_long"]


class BundleBaseModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class BundleIdentity(BundleBaseModel):
    experiment_id: str
    stage_id: str
    stage_name: str
    bundle_version: str
    created_at_utc: str
    created_by: str
    bundle_status: BundleStatus


class StatusEvent(BundleBaseModel):
    status: BundleStatus
    changed_at_utc: str
    reason: str


class ArtifactRef(BundleBaseModel):
    artifact_id: str
    role: str
    path: str
    format: str
    sha256: str
    required: bool


class FeatureSchemaSnapshot(BundleBaseModel):
    feature_count: int
    order_version: str
    feature_schema_artifact_id: str
    feature_fingerprint: str


class OutputSchema(BundleBaseModel):
    schema_type: SchemaType
    output_order: list[str]

    @field_validator("output_order")
    @classmethod
    def validate_output_order(cls, value: list[str]) -> list[str]:
        if value != EXPECTED_PROBS3_ORDER:
            raise ValueError(f"output_order must equal {EXPECTED_PROBS3_ORDER}")
        return value


class ExternalInputRequirement(BundleBaseModel):
    input_id: str
    symbol: str
    timeframe: str
    required: bool
    alignment_rule: AlignmentRule
    role: str | None = None
    group: str | None = None


class SplitBoundaries(BundleBaseModel):
    train_start_utc: str
    train_end_utc_exclusive: str
    validation_end_utc_exclusive: str
    test_end_utc_exclusive: str


class LabelConfig(BundleBaseModel):
    label_type: str
    horizon_bars: int
    band: float


class DataSnapshot(BundleBaseModel):
    dataset_id: str
    source_artifact_ids: list[str]
    split_boundaries: SplitBoundaries
    label_config: LabelConfig
    split_counts: dict[str, int] = Field(default_factory=dict)
    extra: dict[str, JsonValue] = Field(default_factory=dict)


class RuntimeSnapshot(BundleBaseModel):
    symbol: str
    timeframe: str
    tester_model: TesterModel
    deposit: float
    leverage: int
    sizing_mode: str
    fixed_lot: float
    risk_pct: float | None = None
    capital_base: str | None = None
    stop_model: str | None = None
    stop_execution_mode: str | None = None
    stop_policy: str | None = None
    stop_atr_period: int | None = None
    stop_atr_mult: float | None = None
    stop_long_atr_mult: float | None = None
    stop_short_atr_mult: float | None = None
    stop_low_vol_threshold: float | None = None
    stop_high_vol_threshold: float | None = None
    stop_low_atr_mult: float | None = None
    stop_mid_atr_mult: float | None = None
    stop_high_atr_mult: float | None = None
    entry_timing: str
    max_concurrent_positions: int
    cost_behavior: str
    currency: str | None = None
    extra: dict[str, JsonValue] = Field(default_factory=dict)


class RuleDefinition(BundleBaseModel):
    rule_id: str
    type: str
    enabled: bool
    params: dict[str, JsonValue] = Field(default_factory=dict)


class RuleStack(BundleBaseModel):
    entry: list[RuleDefinition] = Field(default_factory=list)
    filters: list[RuleDefinition] = Field(default_factory=list)
    position: list[RuleDefinition] = Field(default_factory=list)
    exit: list[RuleDefinition] = Field(default_factory=list)


class HeadlineMetrics(BundleBaseModel):
    net_profit: float | None = None
    return_pct: float | None = None
    trade_count: int | None = None
    win_rate: float | None = None
    profit_factor: float | None = None
    expectancy_per_trade: float | None = None
    max_dd_pct: float | None = None
    recovery_factor: float | None = None
    extra: dict[str, JsonValue] = Field(default_factory=dict)


class RiskMetrics(BundleBaseModel):
    max_dd_pct: float | None = None
    max_dd_amount: float | None = None
    equity_dd_pct: float | None = None
    equity_dd_amount: float | None = None
    time_under_water: float | None = None
    longest_recovery_duration: float | None = None
    worst_day: float | None = None
    worst_week: float | None = None
    min_free_margin: float | None = None
    margin_call_proximity: float | None = None
    ulcer_index: float | None = None
    consecutive_losses: int | None = None
    extra: dict[str, JsonValue] = Field(default_factory=dict)


class DiagnosticsMetrics(BundleBaseModel):
    avg_win: float | None = None
    avg_loss: float | None = None
    payoff_ratio: float | None = None
    avg_hold: float | None = None
    hold_distribution: dict[str, JsonValue] = Field(default_factory=dict)
    long_count: int | None = None
    short_count: int | None = None
    long_expectancy: float | None = None
    short_expectancy: float | None = None
    mfe_mean: float | None = None
    mfe_median: float | None = None
    mfe_p90: float | None = None
    mae_mean: float | None = None
    mae_median: float | None = None
    mae_p90: float | None = None
    realized_over_mfe: float | None = None
    win_trade_mae: float | None = None
    loss_trade_mfe: float | None = None
    rule_pass_rates: dict[str, JsonValue] = Field(default_factory=dict)
    no_trade_rate: float | None = None
    extra: dict[str, JsonValue] = Field(default_factory=dict)


class ExecutionMetrics(BundleBaseModel):
    skip_rate: float | None = None
    reject_count: int | None = None
    avg_spread: float | None = None
    avg_slippage: float | None = None
    skip_reason_breakdown: dict[str, JsonValue] = Field(default_factory=dict)
    external_mismatch_count: int | None = None
    fill_rate: float | None = None
    entry_delay_stats: dict[str, JsonValue] = Field(default_factory=dict)
    next_tick_fill_distance: dict[str, JsonValue] = Field(default_factory=dict)
    spread_regime_breakdown: dict[str, JsonValue] = Field(default_factory=dict)
    slippage_regime_breakdown: dict[str, JsonValue] = Field(default_factory=dict)
    sessionwise_execution_quality: dict[str, JsonValue] = Field(default_factory=dict)
    runtime_warning_counts: dict[str, JsonValue] = Field(default_factory=dict)
    data_readiness_failures: int | None = None
    broker_constraint_events: int | None = None
    extra: dict[str, JsonValue] = Field(default_factory=dict)


class SplitResults(BundleBaseModel):
    headline: HeadlineMetrics = Field(default_factory=HeadlineMetrics)
    risk: RiskMetrics = Field(default_factory=RiskMetrics)
    diagnostics: DiagnosticsMetrics = Field(default_factory=DiagnosticsMetrics)
    execution: ExecutionMetrics = Field(default_factory=ExecutionMetrics)


class StabilityMetrics(BundleBaseModel):
    validation_test_gap_metrics: dict[str, JsonValue] = Field(default_factory=dict)
    profit_factor_gap: float | None = None
    expectancy_gap: float | None = None
    win_rate_gap: float | None = None
    long_short_mix_shift: float | None = None
    parameter_neighborhood_robustness: float | None = None
    subperiod_consistency: float | None = None
    regime_slice_consistency: float | None = None
    rank_consistency: float | None = None
    parameter_surface_smoothness: float | None = None
    extra: dict[str, JsonValue] = Field(default_factory=dict)


class CrossSplitResults(BundleBaseModel):
    stability: StabilityMetrics = Field(default_factory=StabilityMetrics)


class ReportReference(BundleBaseModel):
    role: str
    split: str
    artifact_id: str
    description: str


class ResultsBlock(BundleBaseModel):
    by_split: dict[str, SplitResults] = Field(default_factory=dict)
    cross_split: CrossSplitResults = Field(default_factory=CrossSplitResults)
    report_refs: list[ReportReference] = Field(default_factory=list)


class CapabilityRequirement(BundleBaseModel):
    name: str
    min_version: str
    params: dict[str, JsonValue] = Field(default_factory=dict)


class ArtifactHashRequirement(BundleBaseModel):
    artifact_id: str
    sha256: str


class CompatibilityBlock(BundleBaseModel):
    schema_version: str
    min_ea_bundle_support_version: str
    required_output_schema: OutputSchema
    required_feature_fingerprint: str
    required_artifact_hashes: list[ArtifactHashRequirement] = Field(default_factory=list)
    required_ea_capabilities: list[CapabilityRequirement] = Field(default_factory=list)
    bundle_integrity_hash: str = ""
    mismatch_policy: MismatchPolicy = "fail_fast"


class RunAttempt(BundleBaseModel):
    attempt_id: str
    status: BundleStatus
    started_at_utc: str
    ended_at_utc: str | None = None
    runtime_snapshot_override: dict[str, JsonValue] = Field(default_factory=dict)
    summary_metrics: dict[str, JsonValue] = Field(default_factory=dict)
    failure_summary: dict[str, JsonValue] | None = None
    report_artifact_ids: list[str] = Field(default_factory=list)


class ExperimentBundle(BundleBaseModel):
    identity: BundleIdentity
    status_history: list[StatusEvent]
    artifacts: list[ArtifactRef]
    feature_schema: FeatureSchemaSnapshot
    output_schema: OutputSchema
    external_inputs: list[ExternalInputRequirement]
    data_snapshot: DataSnapshot
    runtime_snapshot: RuntimeSnapshot
    rule_stack: RuleStack
    results: ResultsBlock
    compatibility: CompatibilityBlock
    run_attempts: list[RunAttempt] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_internal_references(self) -> "ExperimentBundle":
        artifact_ids = [artifact.artifact_id for artifact in self.artifacts]
        duplicate_artifact_ids = {artifact_id for artifact_id in artifact_ids if artifact_ids.count(artifact_id) > 1}
        if duplicate_artifact_ids:
            raise ValueError(f"duplicate artifact_id values found: {sorted(duplicate_artifact_ids)}")

        artifact_id_set = set(artifact_ids)

        if self.feature_schema.feature_schema_artifact_id not in artifact_id_set:
            raise ValueError(
                f"feature_schema_artifact_id '{self.feature_schema.feature_schema_artifact_id}' is missing from artifacts"
            )

        missing_source_artifacts = sorted(set(self.data_snapshot.source_artifact_ids) - artifact_id_set)
        if missing_source_artifacts:
            raise ValueError(f"data_snapshot.source_artifact_ids missing from artifacts: {missing_source_artifacts}")

        missing_required_hash_artifacts = sorted(
            {
                requirement.artifact_id
                for requirement in self.compatibility.required_artifact_hashes
                if requirement.artifact_id not in artifact_id_set
            }
        )
        if missing_required_hash_artifacts:
            raise ValueError(
                f"compatibility.required_artifact_hashes reference missing artifacts: {missing_required_hash_artifacts}"
            )

        missing_report_ref_artifacts = sorted(
            {ref.artifact_id for ref in self.results.report_refs if ref.artifact_id not in artifact_id_set}
        )
        if missing_report_ref_artifacts:
            raise ValueError(f"results.report_refs reference missing artifacts: {missing_report_ref_artifacts}")

        missing_attempt_report_artifacts = sorted(
            {
                artifact_id
                for attempt in self.run_attempts
                for artifact_id in attempt.report_artifact_ids
                if artifact_id not in artifact_id_set
            }
        )
        if missing_attempt_report_artifacts:
            raise ValueError(
                f"run_attempts.report_artifact_ids reference missing artifacts: {missing_attempt_report_artifacts}"
            )

        if self.output_schema != self.compatibility.required_output_schema:
            raise ValueError("compatibility.required_output_schema must match output_schema")

        if self.feature_schema.feature_fingerprint != self.compatibility.required_feature_fingerprint:
            raise ValueError("compatibility.required_feature_fingerprint must match feature_schema.feature_fingerprint")

        return self

    def to_dict(self) -> dict[str, JsonValue]:
        return self.model_dump(mode="json", exclude_none=False)

    def to_json(self, *, indent: int = 2) -> str:
        return self.model_dump_json(indent=indent, exclude_none=False)

    @classmethod
    def from_dict(cls, payload: dict[str, JsonValue]) -> "ExperimentBundle":
        return cls.model_validate(payload)

    @classmethod
    def from_json(cls, payload: str | bytes) -> "ExperimentBundle":
        return cls.model_validate_json(payload)

    def core_dict_for_integrity(self) -> dict[str, JsonValue]:
        data = self.to_dict()
        data.pop("results", None)
        data.pop("run_attempts", None)

        compatibility = dict(data.get("compatibility", {}))
        compatibility.pop("bundle_integrity_hash", None)
        data["compatibility"] = compatibility
        return data

    def canonical_core_json(self) -> str:
        return json.dumps(
            self.core_dict_for_integrity(),
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
        )


__all__ = [
    "AlignmentRule",
    "ArtifactHashRequirement",
    "ArtifactRef",
    "BundleIdentity",
    "BundleStatus",
    "CapabilityRequirement",
    "CompatibilityBlock",
    "CrossSplitResults",
    "DataSnapshot",
    "DiagnosticsMetrics",
    "ExecutionMetrics",
    "ExperimentBundle",
    "ExternalInputRequirement",
    "FeatureSchemaSnapshot",
    "HeadlineMetrics",
    "JsonValue",
    "LabelConfig",
    "MismatchPolicy",
    "OutputSchema",
    "ReportReference",
    "ResultsBlock",
    "RiskMetrics",
    "RuleDefinition",
    "RuleStack",
    "RunAttempt",
    "SchemaType",
    "SplitBoundaries",
    "SplitResults",
    "StabilityMetrics",
    "StatusEvent",
    "RuntimeSnapshot",
    "ValidationError",
]
