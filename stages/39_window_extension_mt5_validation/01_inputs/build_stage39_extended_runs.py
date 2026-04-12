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

from foundation.pipelines.experiment_bundle_models import ExperimentBundle, ResultsBlock, StatusEvent  # noqa: E402

BASE_RUNS = {
    "35A": ROOT_DIR / "stages" / "35_candle_sidecar_simplification_check" / "02_runs" / "active" / "35A_34d_refcarry_0001",
    "35B": ROOT_DIR / "stages" / "35_candle_sidecar_simplification_check" / "02_runs" / "active" / "35B_34b_simpleref_0001",
}
ACTIVE_RUNS_DIR = Path(__file__).resolve().parents[1] / "02_runs" / "active"
UTC = timezone.utc


def utc_now_iso() -> str:
    return datetime.now(tz=UTC).isoformat()


def build_status_history() -> list[StatusEvent]:
    now = utc_now_iso()
    return [
        StatusEvent(status="draft", changed_at_utc=now, reason="bundle_initialized_from_stage35_extension_reference"),
        StatusEvent(status="ready", changed_at_utc=now, reason="stage39_window_extension_wave1_prepared"),
    ]


RUNS = [
    {
        "folder_name": "39A_34d_bridge_ext_0001",
        "experiment_id": "exp_39a_34d_bridge_ext_v1",
        "stage_id": "39A",
        "base_key": "35A",
        "extra_overrides": {
            "stage39_extension_label": "34d_continuous_bridge_latest",
            "stage39_extension_mode": "operating_reference_continuity_latest",
        },
    },
    {
        "folder_name": "39B_34b_bridge_ext_0001",
        "experiment_id": "exp_39b_34b_bridge_ext_v1",
        "stage_id": "39B",
        "base_key": "35B",
        "extra_overrides": {
            "stage39_extension_label": "34b_governance_only_bridge_latest",
            "stage39_extension_mode": "simplification_shadow_continuity_latest",
        },
    },
]


def filter_base_artifacts(bundle: ExperimentBundle):
    return [artifact for artifact in bundle.artifacts if not artifact.role.startswith("mt5_")]


def derive_base_extra(bundle: ExperimentBundle) -> dict[str, int | float | str | bool]:
    extra = deepcopy(bundle.runtime_snapshot.extra)
    extra.pop("stage37_bridge_label", None)
    extra.pop("stage37_bridge_mode", None)
    extra.pop("stage39_extension_label", None)
    extra.pop("stage39_extension_mode", None)
    return extra


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
        bundle.identity.stage_name = "window_extension_mt5_validation"
        bundle.identity.created_at_utc = utc_now_iso()
        bundle.identity.bundle_status = "ready"
        bundle.status_history = build_status_history()
        bundle.results = ResultsBlock()
        bundle.run_attempts = []
        bundle.artifacts = filter_base_artifacts(bundle)

        bundle.runtime_snapshot.extra = deepcopy(base_extra)
        bundle.runtime_snapshot.extra.update(run["extra_overrides"])

        (run_dir / "rule_stack.json").write_text(
            bundle.rule_stack.model_dump_json(indent=2, exclude_none=False),
            encoding="utf-8",
        )
        (run_dir / "experiment_bundle.json").write_text(bundle.to_json(indent=2), encoding="utf-8")
        print(f"[done] created={run_dir}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
