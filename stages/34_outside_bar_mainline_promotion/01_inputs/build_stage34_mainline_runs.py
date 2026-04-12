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

BASE_RUNS = {
    "29N": ROOT_DIR / "stages" / "29_fusion_long_repair" / "02_runs" / "active" / "29N_25o_sxh2_0001",
    "29S": ROOT_DIR / "stages" / "29_fusion_long_repair" / "02_runs" / "active" / "29S_25o_sxh2_gweak_0001",
}
ACTIVE_RUNS_DIR = Path(__file__).resolve().parents[1] / "02_runs" / "active"
UTC = timezone.utc


def utc_now_iso() -> str:
    return datetime.now(tz=UTC).isoformat()


def build_status_history() -> list[StatusEvent]:
    now = utc_now_iso()
    return [
        StatusEvent(status="draft", changed_at_utc=now, reason="bundle_initialized_from_stage29_reference"),
        StatusEvent(status="ready", changed_at_utc=now, reason="stage34_outside_bar_mainline_wave1_prepared"),
    ]


def make_extra(
    label: str,
    *,
    enable_outside_bar: bool,
) -> dict[str, int | float | str | bool]:
    extra: dict[str, int | float | str | bool] = {
        "stage34_mainline_label": label,
    }
    if enable_outside_bar:
        extra.update(
            {
                "state_exit_outside_bar_suppress_enabled": True,
                "state_exit_outside_bar_direction": "long",
                "state_exit_outside_bar_min_range_atr14": 0.0,
                "state_exit_outside_bar_trigger_scope": "margin_only",
            }
        )
    return extra


RUNS = [
    {
        "folder_name": "34A_29n_refcarry_0001",
        "experiment_id": "exp_34a_29n_refcarry_v1",
        "stage_id": "34A",
        "base_key": "29N",
        "label": "29N carry rerun inside regular stage",
        "extra_overrides": make_extra("29n_refcarry", enable_outside_bar=False),
    },
    {
        "folder_name": "34B_29s_refcarry_0001",
        "experiment_id": "exp_34b_29s_refcarry_v1",
        "stage_id": "34B",
        "base_key": "29S",
        "label": "29S carry rerun inside regular stage",
        "extra_overrides": make_extra("29s_refcarry", enable_outside_bar=False),
    },
    {
        "folder_name": "34C_29n_outbarlong_0001",
        "experiment_id": "exp_34c_29n_outbarlong_v1",
        "stage_id": "34C",
        "base_key": "29N",
        "label": "29N plus long-only outside adverse bar suppressor",
        "extra_overrides": make_extra("29n_outbar_long", enable_outside_bar=True),
    },
    {
        "folder_name": "34D_29s_outbarlong_0001",
        "experiment_id": "exp_34d_29s_outbarlong_v1",
        "stage_id": "34D",
        "base_key": "29S",
        "label": "29S plus long-only outside adverse bar suppressor",
        "extra_overrides": make_extra("29s_outbar_long", enable_outside_bar=True),
    },
]


def filter_base_artifacts(bundle: ExperimentBundle):
    return [artifact for artifact in bundle.artifacts if not artifact.role.startswith("mt5_")]


def derive_base_extra(bundle: ExperimentBundle) -> dict[str, int | float | str | bool]:
    extra = deepcopy(bundle.runtime_snapshot.extra)
    for key in list(extra.keys()):
        if key.startswith("stage33_") or key.startswith("stage34_"):
            extra.pop(key, None)
    extra.pop("state_exit_outside_bar_suppress_enabled", None)
    extra.pop("state_exit_outside_bar_direction", None)
    extra.pop("state_exit_outside_bar_min_range_atr14", None)
    extra.pop("state_exit_outside_bar_trigger_scope", None)
    return extra


def upsert_capabilities(bundle: ExperimentBundle, runtime_extra: dict[str, int | float | str | bool]) -> None:
    filtered = [
        capability
        for capability in bundle.compatibility.required_ea_capabilities
        if capability.name
        not in {
            "state_exit_outside_bar_suppressor",
            "state_exit_outside_bar_suppressor_range_filter",
        }
    ]
    if bool(runtime_extra.get("state_exit_outside_bar_suppress_enabled", False)):
        filtered.append(CapabilityRequirement(name="state_exit_outside_bar_suppressor", min_version="1.0"))
        if float(runtime_extra.get("state_exit_outside_bar_min_range_atr14", 0.0) or 0.0) > 0.0:
            filtered.append(CapabilityRequirement(name="state_exit_outside_bar_suppressor_range_filter", min_version="1.0"))
    bundle.compatibility.required_ea_capabilities = filtered


def main() -> int:
    base_bundles = {
        key: ExperimentBundle.from_json((path / "experiment_bundle.json").read_text(encoding="utf-8-sig"))
        for key, path in BASE_RUNS.items()
    }

    for run in RUNS:
        run_dir = ACTIVE_RUNS_DIR / run["folder_name"]
        if run_dir.exists():
            raise FileExistsError(f"target run directory already exists: {run_dir}")

        base_dir = BASE_RUNS[run["base_key"]]
        base_bundle = base_bundles[run["base_key"]]
        base_extra = derive_base_extra(base_bundle)

        run_dir.mkdir(parents=True, exist_ok=False)
        shutil.copytree(base_dir / "artifacts", run_dir / "artifacts")

        bundle = deepcopy(base_bundle)
        bundle.identity.experiment_id = run["experiment_id"]
        bundle.identity.stage_id = run["stage_id"]
        bundle.identity.stage_name = "outside_bar_mainline_promotion"
        bundle.identity.created_at_utc = utc_now_iso()
        bundle.identity.bundle_status = "ready"
        bundle.status_history = build_status_history()
        bundle.results = ResultsBlock()
        bundle.run_attempts = []
        bundle.artifacts = filter_base_artifacts(bundle)

        bundle.runtime_snapshot.extra = deepcopy(base_extra)
        bundle.runtime_snapshot.extra.update(run["extra_overrides"])

        upsert_capabilities(bundle, runtime_extra=bundle.runtime_snapshot.extra)

        (run_dir / "rule_stack.json").write_text(
            bundle.rule_stack.model_dump_json(indent=2, exclude_none=False),
            encoding="utf-8",
        )
        (run_dir / "experiment_bundle.json").write_text(bundle.to_json(indent=2), encoding="utf-8")
        print(f"[done] created={run_dir}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
