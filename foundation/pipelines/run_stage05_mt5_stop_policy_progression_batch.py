#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from foundation.pipelines.show_experiment_leaderboard import load_bundle_views


UTC = timezone.utc
PROBE_SCRIPT = ROOT_DIR / "foundation" / "pipelines" / "run_stage05_mt5_05dp_risk_pct_probe.py"


def utc_now_iso() -> str:
    return datetime.now(tz=UTC).isoformat()


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_json(path: Path, payload: dict[str, Any]) -> None:
    write_text(path, json.dumps(payload, indent=2, ensure_ascii=False) + "\n")


def format_metric(value: Any, digits: int = 4) -> str:
    if value is None:
        return "n/a"
    return f"{float(value):.{digits}f}"


def update_review_index(review_dir: Path, review_filename: str) -> None:
    review_index_path = review_dir / "review_index.md"
    lines = review_index_path.read_text(encoding="utf-8").splitlines() if review_index_path.exists() else []
    stage_tag = review_filename.split("_", 1)[0]
    entry = f"- `{stage_tag}`: see `{review_filename}`"
    if entry not in lines:
        insert_at = 4 if len(lines) >= 4 else len(lines)
        lines.insert(insert_at, entry)
    write_text(review_index_path, "\n".join(lines).rstrip() + "\n")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run sequential stop-policy progression probes on top of the 05DP broker-native risk% path.")
    parser.add_argument("--stage-root", default="stages/05_optimization", help="Stage 05 root directory.")
    parser.add_argument("--risk-pct", type=float, default=3.0, help="Risk percent used across all progression runs.")
    parser.add_argument("--rebuild-bundle", action="store_true", help="Force bundle rebuilds for every progression run.")
    return parser


def build_specs(risk_pct: float) -> list[dict[str, Any]]:
    return [
        {
            "family": "fixed",
            "stage_id": "05GC",
            "run_name": "05GC_05dp_fixed_stop10_riskpct300_brokersl_0001",
            "experiment_id": "exp_05gc_05dp_fixed_stop10_riskpct300_brokersl_v1",
            "review_basename": "05GC_mt5_fixed_stop10_riskpct300_brokersl_probe_review",
            "args": ["--stop-policy", "fixed", "--stop-atr-mult", "1.0"],
        },
        {
            "family": "fixed",
            "stage_id": "05GD",
            "run_name": "05GD_05dp_fixed_stop15_riskpct300_brokersl_0001",
            "experiment_id": "exp_05gd_05dp_fixed_stop15_riskpct300_brokersl_v1",
            "review_basename": "05GD_mt5_fixed_stop15_riskpct300_brokersl_probe_review",
            "args": ["--stop-policy", "fixed", "--stop-atr-mult", "1.5"],
        },
        {
            "family": "fixed",
            "stage_id": "05GE",
            "run_name": "05GE_05dp_fixed_stop20_riskpct300_brokersl_0001",
            "experiment_id": "exp_05ge_05dp_fixed_stop20_riskpct300_brokersl_v1",
            "review_basename": "05GE_mt5_fixed_stop20_riskpct300_brokersl_probe_review",
            "args": ["--stop-policy", "fixed", "--stop-atr-mult", "2.0"],
        },
        {
            "family": "regime_bucket",
            "stage_id": "05GF",
            "run_name": "05GF_05dp_regime085_115_100_150_200_riskpct300_0001",
            "experiment_id": "exp_05gf_05dp_regime085_115_100_150_200_riskpct300_v1",
            "review_basename": "05GF_mt5_regime_bucket_riskpct300_probe_review",
            "args": [
                "--stop-policy", "regime_bucket",
                "--stop-low-vol-threshold", "0.85",
                "--stop-high-vol-threshold", "1.15",
                "--stop-low-atr-mult", "1.0",
                "--stop-mid-atr-mult", "1.5",
                "--stop-high-atr-mult", "2.0",
            ],
        },
        {
            "family": "regime_bucket",
            "stage_id": "05GG",
            "run_name": "05GG_05dp_regime090_110_090_140_180_riskpct300_0001",
            "experiment_id": "exp_05gg_05dp_regime090_110_090_140_180_riskpct300_v1",
            "review_basename": "05GG_mt5_regime_bucket_riskpct300_probe_review",
            "args": [
                "--stop-policy", "regime_bucket",
                "--stop-low-vol-threshold", "0.90",
                "--stop-high-vol-threshold", "1.10",
                "--stop-low-atr-mult", "0.9",
                "--stop-mid-atr-mult", "1.4",
                "--stop-high-atr-mult", "1.8",
            ],
        },
        {
            "family": "regime_bucket",
            "stage_id": "05GH",
            "run_name": "05GH_05dp_regime085_120_110_150_220_riskpct300_0001",
            "experiment_id": "exp_05gh_05dp_regime085_120_110_150_220_riskpct300_v1",
            "review_basename": "05GH_mt5_regime_bucket_riskpct300_probe_review",
            "args": [
                "--stop-policy", "regime_bucket",
                "--stop-low-vol-threshold", "0.85",
                "--stop-high-vol-threshold", "1.20",
                "--stop-low-atr-mult", "1.1",
                "--stop-mid-atr-mult", "1.5",
                "--stop-high-atr-mult", "2.2",
            ],
        },
        {
            "family": "direction_split",
            "stage_id": "05GI",
            "run_name": "05GI_05dp_dirsplit_l13_s17_riskpct300_0001",
            "experiment_id": "exp_05gi_05dp_dirsplit_l13_s17_riskpct300_v1",
            "review_basename": "05GI_mt5_direction_split_riskpct300_probe_review",
            "args": [
                "--stop-policy", "direction_split",
                "--stop-long-atr-mult", "1.3",
                "--stop-short-atr-mult", "1.7",
            ],
        },
        {
            "family": "direction_split",
            "stage_id": "05GJ",
            "run_name": "05GJ_05dp_dirsplit_l12_s18_riskpct300_0001",
            "experiment_id": "exp_05gj_05dp_dirsplit_l12_s18_riskpct300_v1",
            "review_basename": "05GJ_mt5_direction_split_riskpct300_probe_review",
            "args": [
                "--stop-policy", "direction_split",
                "--stop-long-atr-mult", "1.2",
                "--stop-short-atr-mult", "1.8",
            ],
        },
        {
            "family": "direction_split",
            "stage_id": "05GK",
            "run_name": "05GK_05dp_dirsplit_l14_s20_riskpct300_0001",
            "experiment_id": "exp_05gk_05dp_dirsplit_l14_s20_riskpct300_v1",
            "review_basename": "05GK_mt5_direction_split_riskpct300_probe_review",
            "args": [
                "--stop-policy", "direction_split",
                "--stop-long-atr-mult", "1.4",
                "--stop-short-atr-mult", "2.0",
            ],
        },
    ]


def run_spec(spec: dict[str, Any], args: argparse.Namespace) -> None:
    cmd = [
        sys.executable,
        str(PROBE_SCRIPT),
        "--run-name", spec["run_name"],
        "--experiment-id", spec["experiment_id"],
        "--stage-id", spec["stage_id"],
        "--review-basename", spec["review_basename"],
        "--risk-pct", str(args.risk_pct),
        "--stop-execution-mode", "broker_native",
    ]
    if args.rebuild_bundle:
        cmd.append("--rebuild-bundle")
    cmd.extend(spec["args"])
    subprocess.run(cmd, cwd=ROOT_DIR, check=True)


def load_view_map(run_names: list[str]) -> dict[str, Any]:
    views = load_bundle_views(ROOT_DIR / "stages", "validation")
    out: dict[str, Any] = {}
    for view in views:
        if view.run_name in run_names:
            out[view.run_name] = view
    missing = [name for name in run_names if name not in out]
    if missing:
        raise FileNotFoundError(f"missing validation bundle view(s): {missing}")
    return out


def build_payload(specs: list[dict[str, Any]], view_map: dict[str, Any], risk_pct: float) -> dict[str, Any]:
    family_rows: dict[str, list[dict[str, Any]]] = {}
    for spec in specs:
        view = view_map[spec["run_name"]]
        row = {
            "family": spec["family"],
            "stage_id": spec["stage_id"],
            "run_name": spec["run_name"],
            "params": spec["args"],
            "return_pct": view.headline.get("return_pct"),
            "profit_factor": view.headline.get("profit_factor"),
            "trade_count": view.headline.get("trade_count"),
            "max_dd_pct": view.headline.get("max_dd_pct"),
            "ulcer_index": view.risk.get("ulcer_index"),
            "avg_hold": view.diagnostics.get("avg_hold"),
            "no_trade_rate": view.diagnostics.get("no_trade_rate"),
        }
        family_rows.setdefault(spec["family"], []).append(row)

    family_leaders: dict[str, dict[str, Any]] = {}
    for family, rows in family_rows.items():
        family_leaders[family] = max(rows, key=lambda row: float(row["return_pct"] or float("-inf")))

    overall_leader = max(
        [row for rows in family_rows.values() for row in rows],
        key=lambda row: float(row["return_pct"] or float("-inf")),
    )

    return {
        "generated_at_utc": utc_now_iso(),
        "phase": "05GL_mt5_stop_policy_progression_batch",
        "risk_pct": risk_pct,
        "stop_execution_mode": "broker_native",
        "families": family_rows,
        "family_leaders": family_leaders,
        "overall_leader": overall_leader,
    }


def build_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# 05GL Stage 05 Stop Policy Progression Review",
        "",
        f"Generated at: `{payload['generated_at_utc']}`",
        "",
        "## Scope",
        "",
        f"- risk_pct: `{payload['risk_pct']:.4f}`",
        f"- stop_execution_mode: `{payload['stop_execution_mode']}`",
        "- progression: `fixed -> regime_bucket -> direction_split`",
        "",
    ]

    for family in ["fixed", "regime_bucket", "direction_split"]:
        lines.extend([f"## {family}", ""])
        for row in payload["families"].get(family, []):
            lines.append(
                f"- `{row['stage_id']}` `{row['run_name']}`: "
                f"return_pct `{format_metric(row['return_pct'], 3)}`, "
                f"PF `{format_metric(row['profit_factor'], 4)}`, "
                f"trades `{row['trade_count']}`, "
                f"max_dd_pct `{format_metric(row['max_dd_pct'], 4)}`, "
                f"ulcer `{format_metric(row['ulcer_index'], 4)}`, "
                f"avg_hold `{format_metric(row['avg_hold'], 4)}`, "
                f"no_trade_rate `{format_metric(row['no_trade_rate'], 4)}`"
            )
        leader = payload["family_leaders"].get(family)
        if leader:
            lines.extend([
                "",
                f"- leader: `{leader['stage_id']}` `{leader['run_name']}` with return_pct `{format_metric(leader['return_pct'], 3)}` and PF `{format_metric(leader['profit_factor'], 4)}`",
            ])
        lines.append("")

    overall = payload["overall_leader"]
    lines.extend([
        "## Overall",
        "",
        f"- leader: `{overall['stage_id']}` `{overall['run_name']}`",
        f"- return_pct: `{format_metric(overall['return_pct'], 3)}`",
        f"- profit_factor: `{format_metric(overall['profit_factor'], 4)}`",
        f"- max_dd_pct: `{format_metric(overall['max_dd_pct'], 4)}`",
        "",
    ])
    return "\n".join(lines)


def main() -> int:
    args = build_parser().parse_args()
    specs = build_specs(args.risk_pct)

    for spec in specs:
        print(f"[run] {spec['stage_id']} {spec['run_name']}")
        run_spec(spec, args)

    run_names = [spec["run_name"] for spec in specs]
    view_map = load_view_map(run_names)
    payload = build_payload(specs, view_map, args.risk_pct)

    review_dir = ROOT_DIR / args.stage_root / "03_reviews"
    review_md_path = review_dir / "05GL_mt5_stop_policy_progression_review.md"
    review_json_path = review_dir / "05GL_mt5_stop_policy_progression_review.json"
    write_json(review_json_path, payload)
    write_text(review_md_path, build_markdown(payload))
    update_review_index(review_dir, review_md_path.name)

    print(f"[done] review_md={review_md_path}")
    print(f"[done] review_json={review_json_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
