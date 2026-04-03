#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import traceback
from datetime import datetime, timezone
from pathlib import Path
from typing import Literal

import numpy as np
import onnxruntime as ort
from pydantic import ValidationError

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from foundation.pipelines.experiment_bundle_models import (
    ArtifactHashRequirement,
    ArtifactRef,
    BundleIdentity,
    CapabilityRequirement,
    CompatibilityBlock,
    DataSnapshot,
    ExperimentBundle,
    ExternalInputRequirement,
    FeatureSchemaSnapshot,
    OutputSchema,
    ResultsBlock,
    RuleStack,
    RuntimeSnapshot,
    StatusEvent,
)
from foundation.pipelines.experiment_bundle_request_models import (
    BundleBuildRequest,
    EXPECTED_PROBS3_ORDER,
    SmokeArraySpec,
)

UTC = timezone.utc


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Build validated experiment_bundle.json from request metadata.")
    parser.add_argument("--request-json", required=True, help="Bundle build request JSON path")
    parser.add_argument(
        "--output-dir",
        help="Output directory for experiment_bundle.json and reports. Defaults to request JSON parent.",
    )
    return parser


def utc_now_iso() -> str:
    return datetime.now(tz=UTC).isoformat()


def read_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def resolve_path(value: str, base_dir: Path) -> Path:
    path = Path(value)
    if not path.is_absolute():
        path = (base_dir / path).resolve()
    return path


def extract_sequence_from_json(payload: object, *, key: str | None, purpose: str) -> object:
    if key is not None:
        if not isinstance(payload, dict):
            raise ValueError(f"{purpose}: JSON key '{key}' requested but file does not contain an object")
        if key not in payload:
            raise ValueError(f"{purpose}: missing JSON key '{key}'")
        return payload[key]

    if isinstance(payload, list):
        return payload

    if isinstance(payload, dict):
        if all(label in payload for label in EXPECTED_PROBS3_ORDER):
            return [payload[label] for label in EXPECTED_PROBS3_ORDER]
        for candidate in ("features", "feature_names", "feature_order", "probabilities", "input", "vector"):
            if candidate in payload:
                return payload[candidate]
        if len(payload) == 1:
            return next(iter(payload.values()))

    raise ValueError(f"{purpose}: could not infer array payload from JSON")


def load_numpy_array(spec: SmokeArraySpec, *, request_dir: Path, purpose: str) -> np.ndarray:
    path = resolve_path(spec.path, request_dir)
    if not path.exists():
        raise FileNotFoundError(f"{purpose}: missing file {path}")

    if spec.format == "npy":
        array = np.load(path)
    else:
        payload = read_json(path)
        array = np.asarray(extract_sequence_from_json(payload, key=spec.key, purpose=purpose), dtype=np.float32)

    array = np.asarray(array, dtype=np.float32)
    if array.size == 0:
        raise ValueError(f"{purpose}: loaded empty array from {path}")
    return array


def extract_feature_names(feature_schema_path: Path) -> list[str]:
    payload = read_json(feature_schema_path)

    if isinstance(payload, list):
        if all(isinstance(item, str) for item in payload):
            return payload
        if all(isinstance(item, dict) and "name" in item for item in payload):
            return [str(item["name"]) for item in payload]

    if isinstance(payload, dict):
        for key in ("feature_names", "feature_order"):
            value = payload.get(key)
            if isinstance(value, list) and all(isinstance(item, str) for item in value):
                return value

        features = payload.get("features")
        if isinstance(features, list):
            if all(isinstance(item, str) for item in features):
                return features
            if all(isinstance(item, dict) and "name" in item for item in features):
                return [str(item["name"]) for item in features]

    raise ValueError(
        f"could not extract feature names from schema artifact {feature_schema_path}; "
        "supported shapes are list[str], {'feature_names': [...]}, {'feature_order': [...]}, or {'features': [...]}"
    )


def resolve_feature_schema_snapshot(
    request: BundleBuildRequest,
    *,
    artifact_paths: dict[str, Path],
) -> FeatureSchemaSnapshot:
    artifact_id = request.feature_schema.feature_schema_artifact_id
    if artifact_id not in artifact_paths:
        raise ValueError(f"feature_schema_artifact_id '{artifact_id}' is missing from artifacts")

    feature_names = extract_feature_names(artifact_paths[artifact_id])
    feature_count = request.feature_schema.feature_count or len(feature_names)
    if feature_count != len(feature_names):
        raise ValueError(
            f"feature_count mismatch: request={feature_count}, derived_from_schema={len(feature_names)}"
        )

    derived_fingerprint = sha256_text(",".join(feature_names))
    feature_fingerprint = request.feature_schema.feature_fingerprint or derived_fingerprint
    if feature_fingerprint != derived_fingerprint:
        raise ValueError(
            "feature_fingerprint mismatch: request value does not match the feature schema artifact contents"
        )

    return FeatureSchemaSnapshot(
        feature_count=feature_count,
        order_version=request.feature_schema.order_version,
        feature_schema_artifact_id=artifact_id,
        feature_fingerprint=feature_fingerprint,
    )


def build_artifacts(
    request: BundleBuildRequest,
    *,
    request_dir: Path,
) -> tuple[list[ArtifactRef], dict[str, Path]]:
    artifacts: list[ArtifactRef] = []
    artifact_paths: dict[str, Path] = {}

    for artifact in request.artifacts:
        resolved_path = resolve_path(artifact.path, request_dir)
        if not resolved_path.exists():
            raise FileNotFoundError(f"artifact '{artifact.artifact_id}' is missing: {resolved_path}")

        artifact_paths[artifact.artifact_id] = resolved_path
        artifacts.append(
            ArtifactRef(
                artifact_id=artifact.artifact_id,
                role=artifact.role,
                path=artifact.path,
                format=artifact.format,
                sha256=sha256_file(resolved_path),
                required=artifact.required,
            )
        )

    return artifacts, artifact_paths


def run_smoke_test(
    request: BundleBuildRequest,
    *,
    request_dir: Path,
    artifact_paths: dict[str, Path],
    feature_schema: FeatureSchemaSnapshot,
) -> dict[str, object]:
    if request.smoke_test.onnx_artifact_id not in artifact_paths:
        raise ValueError(
            f"smoke_test.onnx_artifact_id '{request.smoke_test.onnx_artifact_id}' is missing from artifacts"
        )

    onnx_path = artifact_paths[request.smoke_test.onnx_artifact_id]
    input_array = load_numpy_array(request.smoke_test.input, request_dir=request_dir, purpose="smoke_test.input")
    expected_output = load_numpy_array(
        request.smoke_test.expected_output,
        request_dir=request_dir,
        purpose="smoke_test.expected_output",
    )

    if input_array.ndim == 1:
        input_array = input_array.reshape(1, -1)
    if input_array.ndim != 2:
        raise ValueError(f"smoke_test.input must resolve to a 1D or 2D array, got shape {input_array.shape}")
    if input_array.shape[1] != feature_schema.feature_count:
        raise ValueError(
            f"smoke_test.input feature width mismatch: expected {feature_schema.feature_count}, got {input_array.shape[1]}"
        )

    expected_output = expected_output.reshape(-1)
    if expected_output.size != len(EXPECTED_PROBS3_ORDER):
        raise ValueError(
            f"smoke_test.expected_output must have {len(EXPECTED_PROBS3_ORDER)} values, got {expected_output.size}"
        )

    session = ort.InferenceSession(str(onnx_path), providers=["CPUExecutionProvider"])
    session_inputs = session.get_inputs()
    session_outputs = session.get_outputs()

    if len(session_inputs) != 1:
        raise ValueError(f"expected exactly 1 ONNX input, found {len(session_inputs)}")
    if len(session_outputs) != 1:
        raise ValueError(f"expected exactly 1 ONNX output, found {len(session_outputs)}")

    actual_output = np.asarray(
        session.run(None, {session_inputs[0].name: input_array.astype(np.float32)})[0],
        dtype=np.float32,
    )
    actual_output = actual_output.reshape(-1)
    if actual_output.size != len(EXPECTED_PROBS3_ORDER):
        raise ValueError(
            f"ONNX output width mismatch: expected {len(EXPECTED_PROBS3_ORDER)}, got {actual_output.size}"
        )

    if not np.allclose(
        actual_output,
        expected_output,
        rtol=request.smoke_test.rtol,
        atol=request.smoke_test.atol,
    ):
        diff = np.abs(actual_output - expected_output)
        raise ValueError(
            "smoke test output mismatch against expected output; "
            f"max_abs_diff={float(diff.max()):.8f}"
        )

    return {
        "onnx_input_name": session_inputs[0].name,
        "onnx_output_name": session_outputs[0].name,
        "input_shape": list(input_array.shape),
        "output_shape": list(actual_output.shape),
        "providers": session.get_providers(),
        "max_abs_diff": float(np.abs(actual_output - expected_output).max()),
    }


def build_required_artifact_hashes(
    request: BundleBuildRequest,
    artifacts: list[ArtifactRef],
) -> list[ArtifactHashRequirement]:
    artifact_map = {artifact.artifact_id: artifact for artifact in artifacts}
    target_ids = request.compatibility.required_hash_artifact_ids
    if target_ids is None:
        target_ids = [artifact.artifact_id for artifact in artifacts if artifact.required]

    missing_ids = sorted(set(target_ids) - set(artifact_map))
    if missing_ids:
        raise ValueError(f"compatibility.required_hash_artifact_ids missing from artifacts: {missing_ids}")

    return [
        ArtifactHashRequirement(artifact_id=artifact_id, sha256=artifact_map[artifact_id].sha256)
        for artifact_id in target_ids
    ]


def build_identity(identity_request: IdentityRequest, *, created_at_utc: str) -> BundleIdentity:
    return BundleIdentity(
        experiment_id=identity_request.experiment_id,
        stage_id=identity_request.stage_id,
        stage_name=identity_request.stage_name,
        bundle_version=identity_request.bundle_version,
        created_at_utc=created_at_utc,
        created_by=identity_request.created_by,
        bundle_status="ready",
    )


def build_status_history(*, created_at_utc: str, ready_at_utc: str) -> list[StatusEvent]:
    return [
        StatusEvent(status="draft", changed_at_utc=created_at_utc, reason="bundle_initialized"),
        StatusEvent(status="ready", changed_at_utc=ready_at_utc, reason="preflight_passed"),
    ]


def assemble_bundle(
    request: BundleBuildRequest,
    *,
    request_dir: Path,
) -> tuple[ExperimentBundle, dict[str, object]]:
    artifacts, artifact_paths = build_artifacts(request, request_dir=request_dir)
    feature_schema = resolve_feature_schema_snapshot(request, artifact_paths=artifact_paths)
    smoke_summary = run_smoke_test(
        request,
        request_dir=request_dir,
        artifact_paths=artifact_paths,
        feature_schema=feature_schema,
    )

    created_at_utc = request.identity.created_at_utc or utc_now_iso()
    ready_at_utc = utc_now_iso()
    required_artifact_hashes = build_required_artifact_hashes(request, artifacts)

    compatibility = CompatibilityBlock(
        schema_version=request.compatibility.schema_version,
        min_ea_bundle_support_version=request.compatibility.min_ea_bundle_support_version,
        required_output_schema=request.output_schema,
        required_feature_fingerprint=feature_schema.feature_fingerprint,
        required_artifact_hashes=required_artifact_hashes,
        required_ea_capabilities=request.compatibility.required_ea_capabilities,
        mismatch_policy=request.compatibility.mismatch_policy,
    )

    bundle = ExperimentBundle(
        identity=build_identity(request.identity, created_at_utc=created_at_utc),
        status_history=build_status_history(created_at_utc=created_at_utc, ready_at_utc=ready_at_utc),
        artifacts=artifacts,
        feature_schema=feature_schema,
        output_schema=request.output_schema,
        external_inputs=request.external_inputs,
        data_snapshot=request.data_snapshot,
        runtime_snapshot=request.runtime_snapshot,
        rule_stack=request.rule_stack,
        results=ResultsBlock(),
        compatibility=compatibility,
        run_attempts=[],
    )

    bundle.compatibility.bundle_integrity_hash = sha256_text(bundle.canonical_core_json())
    bundle = ExperimentBundle.from_dict(bundle.to_dict())
    return bundle, smoke_summary


def build_success_summary(
    bundle: ExperimentBundle,
    *,
    bundle_path: Path,
    summary_path: Path,
    smoke_summary: dict[str, object],
) -> dict[str, object]:
    return {
        "status": "success",
        "generated_at_utc": utc_now_iso(),
        "experiment_id": bundle.identity.experiment_id,
        "bundle_path": str(bundle_path.as_posix()),
        "summary_path": str(summary_path.as_posix()),
        "artifact_count": len(bundle.artifacts),
        "required_artifact_count": int(sum(artifact.required for artifact in bundle.artifacts)),
        "feature_count": bundle.feature_schema.feature_count,
        "bundle_integrity_hash": bundle.compatibility.bundle_integrity_hash,
        "smoke_test": smoke_summary,
    }


def build_failure_report(
    *,
    request_json: Path,
    output_dir: Path,
    error: Exception,
) -> dict[str, object]:
    report: dict[str, object] = {
        "status": "failed_preflight",
        "generated_at_utc": utc_now_iso(),
        "request_json": str(request_json.as_posix()),
        "output_dir": str(output_dir.as_posix()),
        "error_type": type(error).__name__,
        "error_message": str(error),
    }
    if isinstance(error, ValidationError):
        report["validation_errors"] = error.errors(include_url=False)
    else:
        report["traceback"] = traceback.format_exc()
    return report


def main() -> int:
    args = build_parser().parse_args()
    request_json_path = Path(args.request_json).resolve()
    output_dir = Path(args.output_dir).resolve() if args.output_dir else request_json_path.parent.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    bundle_path = output_dir / "experiment_bundle.json"
    summary_path = output_dir / "bundle_build_summary.json"
    failure_path = output_dir / "bundle_build_failure_report.json"

    try:
        request_payload = read_json(request_json_path)
        request = BundleBuildRequest.model_validate(request_payload)
        bundle, smoke_summary = assemble_bundle(request, request_dir=request_json_path.parent)

        if failure_path.exists():
            failure_path.unlink()

        bundle_path.write_text(bundle.to_json(indent=2), encoding="utf-8")
        success_summary = build_success_summary(
            bundle,
            bundle_path=bundle_path,
            summary_path=summary_path,
            smoke_summary=smoke_summary,
        )
        write_json(summary_path, success_summary)

        print(f"[done] bundle={bundle_path}")
        print(f"[done] summary={summary_path}")
        print(f"[done] bundle_integrity_hash={bundle.compatibility.bundle_integrity_hash}")
        return 0
    except Exception as error:  # noqa: BLE001
        for stale_path in (bundle_path, summary_path):
            if stale_path.exists():
                stale_path.unlink()
        failure_report = build_failure_report(
            request_json=request_json_path,
            output_dir=output_dir,
            error=error,
        )
        write_json(failure_path, failure_report)
        print(f"[error] failure_report={failure_path}", file=sys.stderr)
        print(f"[error] {type(error).__name__}: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
