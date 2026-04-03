#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from foundation.pipelines.experiment_bundle_models import ExperimentBundle


UTC = timezone.utc
DEFAULT_COMMON_PROJECT_ROOT = Path.home() / "AppData" / "Roaming" / "MetaQuotes" / "Terminal" / "Common" / "Files" / "Project_Obsidian_Prime"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Compile experiment_bundle.json into an EA-friendly MT5 runtime package.")
    parser.add_argument("--bundle-json", required=True, help="Path to experiment_bundle.json")
    parser.add_argument("--runtime-id", help="Optional runtime package id. Defaults to bundle experiment_id")
    parser.add_argument(
        "--common-project-root",
        default=str(DEFAULT_COMMON_PROJECT_ROOT),
        help="Target Project_Obsidian_Prime Common Files root",
    )
    parser.add_argument("--copy-bundle", action="store_true", help="Copy the source experiment_bundle.json into the runtime package")
    return parser


def utc_now_iso() -> str:
    return datetime.now(tz=UTC).isoformat()


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(__import__("json").dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def resolve_bundle_artifact_path(bundle_path: Path, artifact_path: str) -> Path:
    path = Path(artifact_path)
    if path.is_absolute():
        return path
    return (bundle_path.parent / path).resolve()


def find_artifact_id_by_role(bundle: ExperimentBundle, role: str) -> str:
    matches = [artifact.artifact_id for artifact in bundle.artifacts if artifact.role == role]
    if not matches:
        raise ValueError(f"bundle is missing required artifact role '{role}'")
    if len(matches) > 1:
        raise ValueError(f"bundle has multiple artifacts for role '{role}': {matches}")
    return matches[0]


def get_artifact(bundle: ExperimentBundle, artifact_id: str):
    for artifact in bundle.artifacts:
        if artifact.artifact_id == artifact_id:
            return artifact
    raise ValueError(f"artifact_id '{artifact_id}' not found in bundle")


def detect_logic_family(bundle: ExperimentBundle) -> str:
    filter_types = [rule.type for rule in bundle.rule_stack.filters if rule.enabled]
    if not filter_types:
        return "threshold_only"
    if filter_types == ["max_probability_margin"]:
        return "margin_only"
    if filter_types == ["probability_difference"]:
        return "prob_diff_only"
    return "custom"


def bool_text(value: bool) -> str:
    return "true" if value else "false"


def flatten_rule_stack(bundle: ExperimentBundle) -> list[str]:
    lines: list[str] = []
    categories = [
        ("entry", bundle.rule_stack.entry),
        ("filters", bundle.rule_stack.filters),
        ("position", bundle.rule_stack.position),
        ("exit", bundle.rule_stack.exit),
    ]
    for category_name, rules in categories:
        lines.append(f"{category_name}_count={len(rules)}")
        for index, rule in enumerate(rules):
            prefix = f"{category_name}_{index}"
            lines.append(f"{prefix}_rule_id={rule.rule_id}")
            lines.append(f"{prefix}_type={rule.type}")
            lines.append(f"{prefix}_enabled={bool_text(rule.enabled)}")
            for key, value in sorted(rule.params.items()):
                lines.append(f"{prefix}_{key}={value}")
    return lines


def build_runtime_config_lines(
    bundle: ExperimentBundle,
    *,
    runtime_id: str,
    onnx_relative_path: str,
    feature_schema_relative_path: str,
    feature_names: list[str],
) -> list[str]:
    lines = [
        "# Project Obsidian Prime MT5 runtime config",
        f"generated_at_utc={utc_now_iso()}",
        f"runtime_id={runtime_id}",
        f"experiment_id={bundle.identity.experiment_id}",
        f"bundle_version={bundle.identity.bundle_version}",
        f"bundle_integrity_hash={bundle.compatibility.bundle_integrity_hash}",
        f"logic_family={detect_logic_family(bundle)}",
        f"onnx_model_path={onnx_relative_path}",
        "onnx_use_common_files=true",
        f"feature_schema_path={feature_schema_relative_path}",
        "feature_schema_use_common_files=true",
        f"feature_count={bundle.feature_schema.feature_count}",
        f"feature_fingerprint={bundle.feature_schema.feature_fingerprint}",
        f"output_schema_type={bundle.output_schema.schema_type}",
        f"output_order={','.join(bundle.output_schema.output_order)}",
        f"symbol={bundle.runtime_snapshot.symbol}",
        f"timeframe={bundle.runtime_snapshot.timeframe}",
        f"tester_model={bundle.runtime_snapshot.tester_model}",
        f"deposit={bundle.runtime_snapshot.deposit}",
        f"leverage={bundle.runtime_snapshot.leverage}",
        f"sizing_mode={bundle.runtime_snapshot.sizing_mode}",
        f"fixed_lot={bundle.runtime_snapshot.fixed_lot}",
        f"entry_timing={bundle.runtime_snapshot.entry_timing}",
        f"max_concurrent_positions={bundle.runtime_snapshot.max_concurrent_positions}",
        f"cost_behavior={bundle.runtime_snapshot.cost_behavior}",
    ]
    if bundle.runtime_snapshot.risk_pct is not None:
        lines.append(f"risk_pct={bundle.runtime_snapshot.risk_pct}")
    if bundle.runtime_snapshot.capital_base is not None:
        lines.append(f"capital_base={bundle.runtime_snapshot.capital_base}")
    if bundle.runtime_snapshot.stop_model is not None:
        lines.append(f"stop_model={bundle.runtime_snapshot.stop_model}")
    if bundle.runtime_snapshot.stop_execution_mode is not None:
        lines.append(f"stop_execution_mode={bundle.runtime_snapshot.stop_execution_mode}")
    if bundle.runtime_snapshot.stop_policy is not None:
        lines.append(f"stop_policy={bundle.runtime_snapshot.stop_policy}")
    if bundle.runtime_snapshot.stop_atr_period is not None:
        lines.append(f"stop_atr_period={bundle.runtime_snapshot.stop_atr_period}")
    if bundle.runtime_snapshot.stop_atr_mult is not None:
        lines.append(f"stop_atr_mult={bundle.runtime_snapshot.stop_atr_mult}")
    if bundle.runtime_snapshot.stop_long_atr_mult is not None:
        lines.append(f"stop_long_atr_mult={bundle.runtime_snapshot.stop_long_atr_mult}")
    if bundle.runtime_snapshot.stop_short_atr_mult is not None:
        lines.append(f"stop_short_atr_mult={bundle.runtime_snapshot.stop_short_atr_mult}")
    if bundle.runtime_snapshot.stop_low_vol_threshold is not None:
        lines.append(f"stop_low_vol_threshold={bundle.runtime_snapshot.stop_low_vol_threshold}")
    if bundle.runtime_snapshot.stop_high_vol_threshold is not None:
        lines.append(f"stop_high_vol_threshold={bundle.runtime_snapshot.stop_high_vol_threshold}")
    if bundle.runtime_snapshot.stop_low_atr_mult is not None:
        lines.append(f"stop_low_atr_mult={bundle.runtime_snapshot.stop_low_atr_mult}")
    if bundle.runtime_snapshot.stop_mid_atr_mult is not None:
        lines.append(f"stop_mid_atr_mult={bundle.runtime_snapshot.stop_mid_atr_mult}")
    if bundle.runtime_snapshot.stop_high_atr_mult is not None:
        lines.append(f"stop_high_atr_mult={bundle.runtime_snapshot.stop_high_atr_mult}")
    for key, value in sorted(bundle.runtime_snapshot.extra.items()):
        if isinstance(value, bool):
            lines.append(f"{key}={'true' if value else 'false'}")
        elif isinstance(value, (int, float, str)):
            lines.append(f"{key}={value}")
    for index, feature_name in enumerate(feature_names):
        lines.append(f"feature_{index}_name={feature_name}")
    lines.extend(flatten_rule_stack(bundle))
    return lines


def main() -> int:
    args = build_parser().parse_args()
    bundle_path = Path(args.bundle_json).resolve()
    bundle = ExperimentBundle.from_json(bundle_path.read_text(encoding="utf-8-sig"))

    runtime_id = args.runtime_id or bundle.identity.experiment_id
    common_project_root = Path(args.common_project_root).resolve()
    runtime_dir = common_project_root / "runtime" / runtime_id
    runtime_dir.mkdir(parents=True, exist_ok=True)

    onnx_artifact = get_artifact(bundle, find_artifact_id_by_role(bundle, "onnx_model"))
    feature_schema_artifact = get_artifact(bundle, bundle.feature_schema.feature_schema_artifact_id)

    onnx_source_path = resolve_bundle_artifact_path(bundle_path, onnx_artifact.path)
    feature_schema_source_path = resolve_bundle_artifact_path(bundle_path, feature_schema_artifact.path)
    if not onnx_source_path.exists():
        raise FileNotFoundError(f"missing ONNX artifact source: {onnx_source_path}")
    if not feature_schema_source_path.exists():
        raise FileNotFoundError(f"missing feature schema artifact source: {feature_schema_source_path}")

    feature_schema_payload = json.loads(feature_schema_source_path.read_text(encoding="utf-8-sig"))
    feature_names = feature_schema_payload.get("feature_names")
    if not isinstance(feature_names, list) or not feature_names:
        raise ValueError("feature schema must contain a non-empty feature_names list")
    if len(feature_names) != bundle.feature_schema.feature_count:
        raise ValueError(
            "feature schema count mismatch: "
            f"bundle={bundle.feature_schema.feature_count} schema={len(feature_names)}"
        )

    onnx_target_path = runtime_dir / "model.onnx"
    feature_schema_target_path = runtime_dir / "feature_schema.json"
    runtime_config_path = runtime_dir / "mt5_runtime_config.txt"
    summary_path = runtime_dir / "mt5_runtime_compile_summary.json"

    shutil.copy2(onnx_source_path, onnx_target_path)
    shutil.copy2(feature_schema_source_path, feature_schema_target_path)

    if args.copy_bundle:
        shutil.copy2(bundle_path, runtime_dir / "experiment_bundle.json")

    common_relative_root = Path("Project_Obsidian_Prime") / "runtime" / runtime_id
    runtime_config_lines = build_runtime_config_lines(
        bundle,
        runtime_id=runtime_id,
        onnx_relative_path=(common_relative_root / "model.onnx").as_posix().replace("/", "\\"),
        feature_schema_relative_path=(common_relative_root / "feature_schema.json").as_posix().replace("/", "\\"),
        feature_names=feature_names,
    )
    write_text(runtime_config_path, "\n".join(runtime_config_lines) + "\n")

    summary = {
        "status": "success",
        "generated_at_utc": utc_now_iso(),
        "runtime_id": runtime_id,
        "source_bundle_path": str(bundle_path.as_posix()),
        "runtime_dir": str(runtime_dir.as_posix()),
        "runtime_config_path": str(runtime_config_path.as_posix()),
        "onnx_target_path": str(onnx_target_path.as_posix()),
        "feature_schema_target_path": str(feature_schema_target_path.as_posix()),
        "logic_family": detect_logic_family(bundle),
        "feature_count": bundle.feature_schema.feature_count,
        "bundle_integrity_hash": bundle.compatibility.bundle_integrity_hash,
    }
    write_json(summary_path, summary)

    print(f"[done] runtime_config={runtime_config_path}")
    print(f"[done] summary={summary_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
