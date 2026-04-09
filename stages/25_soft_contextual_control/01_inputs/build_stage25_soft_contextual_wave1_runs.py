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
    / "24_gated_specialist_overlay"
    / "02_runs"
    / "active"
    / "24A_23a_base_gate_ref_0001"
)
ACTIVE_RUNS_DIR = Path(__file__).resolve().parents[1] / "02_runs" / "active"
UTC = timezone.utc


def utc_now_iso() -> str:
    return datetime.now(tz=UTC).isoformat()


def build_status_history() -> list[StatusEvent]:
    now = utc_now_iso()
    return [
        StatusEvent(status="draft", changed_at_utc=now, reason="bundle_initialized_from_24A_regular_reference"),
        StatusEvent(status="ready", changed_at_utc=now, reason="stage25_soft_contextual_wave1_prepared"),
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
        "folder_name": "25A_24a_base_softctx_ref_0001",
        "experiment_id": "exp_25a_24a_base_softctx_ref_v1",
        "stage_id": "25A",
        "label": "regular inherited baseline",
        "context_rules": [],
        "extra_overrides": {},
    },
    {
        "folder_name": "25B_24a_monshort_t050_m050_0001",
        "experiment_id": "exp_25b_24a_monshort_t050_m050_v1",
        "stage_id": "25B",
        "label": "Monday short soft suppressor",
        "context_rules": [
            make_contextual_soft_suppressor_rule(
                "filters_02",
                context="monday",
                direction="short",
                threshold_add=0.05,
                min_margin_add=0.05,
            )
        ],
        "extra_overrides": {
            "soft_context_label": "monday_short_soft_suppressor",
        },
    },
    {
        "folder_name": "25C_24a_postshort_t050_m030_0001",
        "experiment_id": "exp_25c_24a_postshort_t050_m030_v1",
        "stage_id": "25C",
        "label": "NY postcash short soft suppressor",
        "context_rules": [
            make_contextual_soft_suppressor_rule(
                "filters_02",
                context="ny_postcash",
                direction="short",
                threshold_add=0.05,
                min_margin_add=0.03,
            )
        ],
        "extra_overrides": {
            "soft_context_label": "ny_postcash_short_soft_suppressor",
        },
    },
    {
        "folder_name": "25D_24a_monpost_t050_m030_psh2_0001",
        "experiment_id": "exp_25d_24a_monpost_t050_m030_psh2_v1",
        "stage_id": "25D",
        "label": "combined short suppressor plus postcash short hold cut",
        "context_rules": [
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
        ],
        "extra_overrides": {
            "ny_postcash_short_hold_cap_bars": 2,
            "soft_context_label": "combined_short_soft_suppressor_with_postcash_short_hold_cut",
        },
    },
]


def filter_base_artifacts(bundle: ExperimentBundle):
    return [artifact for artifact in bundle.artifacts if not artifact.role.startswith("mt5_")]


def upsert_capabilities(bundle: ExperimentBundle, *, has_context_rules: bool, has_direction_hold_cap: bool) -> None:
    filtered = [
        capability
        for capability in bundle.compatibility.required_ea_capabilities
        if capability.name not in {"contextual_soft_suppressor", "direction_hold_cap"}
    ]
    if has_context_rules:
        filtered.append(CapabilityRequirement(name="contextual_soft_suppressor", min_version="1.0"))
    if has_direction_hold_cap:
        filtered.append(CapabilityRequirement(name="direction_hold_cap", min_version="1.0"))
    bundle.compatibility.required_ea_capabilities = filtered


def main() -> int:
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
        bundle.identity.stage_name = "soft_contextual_thresholds_hold_control"
        bundle.identity.created_at_utc = utc_now_iso()
        bundle.identity.bundle_status = "ready"
        bundle.status_history = build_status_history()
        bundle.results = ResultsBlock()
        bundle.run_attempts = []
        bundle.artifacts = filter_base_artifacts(bundle)

        bundle.rule_stack.filters = deepcopy(base_bundle.rule_stack.filters) + deepcopy(run["context_rules"])
        bundle.runtime_snapshot.extra = deepcopy(base_bundle.runtime_snapshot.extra)
        bundle.runtime_snapshot.extra.update(run["extra_overrides"])

        upsert_capabilities(
            bundle,
            has_context_rules=bool(run["context_rules"]),
            has_direction_hold_cap=("ny_postcash_short_hold_cap_bars" in run["extra_overrides"]),
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
