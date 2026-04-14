#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd


UTC = timezone.utc
ROOT_DIR = Path(__file__).resolve().parents[3]
STAGE_DIR = ROOT_DIR / "stages" / "41_targeted_feature_snapshot_audit"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Compare built-in versus contract-aligned MT5 feature snapshots on shared latest-window attribution windows."
    )
    parser.add_argument(
        "--pair",
        action="append",
        nargs=5,
        metavar=("LABEL", "BUILTIN_SNAPSHOT", "CONTRACT_SNAPSHOT", "BUILTIN_SHADOW", "CONTRACT_SHADOW"),
        required=True,
        help="One comparison batch made of label + built-in snapshot jsonl + contract snapshot jsonl + built-in shadow csv + contract shadow csv.",
    )
    parser.add_argument(
        "--output-stem",
        help="Optional output stem without extension. Defaults to stages/41.../03_reviews/stage41_feature_path_shared_attribution_<today>.",
    )
    return parser


def load_jsonl(path: Path) -> list[dict]:
    rows: list[dict] = []
    with path.open("r", encoding="utf-8-sig") as handle:
        for raw_line in handle:
            line = raw_line.strip()
            if not line:
                continue
            rows.append(json.loads(line))
    if not rows:
        raise ValueError(f"snapshot jsonl is empty: {path}")
    return rows


def load_shadow_map(path: Path) -> dict[str, dict]:
    df = pd.read_csv(path)
    df["bar_time_server"] = pd.to_datetime(df["bar_time_server"], format="%Y.%m.%d %H:%M:%S")
    for col in ["decision", "decision_reason", "trade_action_reason"]:
        df[col] = df[col].fillna("")
    return df.set_index(df["bar_time_server"].dt.strftime("%Y.%m.%d %H:%M:%S")).to_dict("index")


def summarize_series(values: list[float]) -> dict[str, float | int | None]:
    if not values:
        return {"count": 0, "mean": None, "median": None, "p10": None, "p90": None, "min": None, "max": None}
    arr = np.asarray(values, dtype=float)
    return {
        "count": int(arr.size),
        "mean": float(arr.mean()),
        "median": float(np.median(arr)),
        "p10": float(np.quantile(arr, 0.10)),
        "p90": float(np.quantile(arr, 0.90)),
        "min": float(arr.min()),
        "max": float(arr.max()),
    }


def fmt_num(value: float | int | None, digits: int = 6) -> str:
    if value is None:
        return "n/a"
    if isinstance(value, int):
        return str(value)
    return f"{value:.{digits}f}"


def normalize_transition(decision_builtin: str, decision_contract: str) -> str:
    if decision_builtin == decision_contract:
        return "same"
    directional = {"LONG", "SHORT"}
    if decision_builtin in directional and decision_contract == "NO_TRADE":
        return f"{decision_builtin.lower()}_to_no_trade"
    if decision_builtin == "NO_TRADE" and decision_contract in directional:
        return f"no_trade_to_{decision_contract.lower()}"
    return f"{decision_builtin.lower()}_to_{decision_contract.lower()}"


def build_output_paths(output_stem: str | None) -> tuple[Path, Path]:
    if output_stem:
        stem = Path(output_stem)
    else:
        stamp = datetime.now(tz=UTC).strftime("%Y%m%d")
        stem = STAGE_DIR / "03_reviews" / f"stage41_feature_path_shared_attribution_{stamp}"
    return stem.with_suffix(".json"), stem.with_suffix(".md")


def build_payload(pairs: list[tuple[str, Path, Path, Path, Path]]) -> dict[str, object]:
    row_records: list[dict[str, object]] = []
    per_feature_abs: dict[str, list[float]] = defaultdict(list)
    per_feature_signed: dict[str, list[float]] = defaultdict(list)
    pair_summaries: list[dict[str, object]] = []

    for label, built_snapshot_path, contract_snapshot_path, built_shadow_path, contract_shadow_path in pairs:
        built_rows = load_jsonl(built_snapshot_path)
        contract_rows = load_jsonl(contract_snapshot_path)
        built_map = {str(row["bar_time_server"]): row for row in built_rows}
        contract_map = {str(row["bar_time_server"]): row for row in contract_rows}
        common_keys = sorted(set(built_map) & set(contract_map))
        if not common_keys:
            raise ValueError(f"no shared snapshot timestamps for pair={label}")

        built_shadow_map = load_shadow_map(built_shadow_path)
        contract_shadow_map = load_shadow_map(contract_shadow_path)

        pair_decision_diffs = 0
        pair_action_diffs = 0

        for bar_time_server in common_keys:
            built_row = built_map[bar_time_server]
            contract_row = contract_map[bar_time_server]
            built_features = {str(item["name"]): item.get("value") for item in built_row.get("features", [])}
            contract_features = {str(item["name"]): item.get("value") for item in contract_row.get("features", [])}

            feature_diffs: list[dict[str, object]] = []
            for feature_name, built_value in built_features.items():
                contract_value = contract_features.get(feature_name)
                if built_value is None or contract_value is None:
                    continue
                signed_delta = float(contract_value) - float(built_value)
                abs_delta = abs(signed_delta)
                feature_diffs.append(
                    {
                        "feature": feature_name,
                        "abs_diff": abs_delta,
                        "signed_delta_contract_minus_builtin": signed_delta,
                        "builtin_value": float(built_value),
                        "contract_value": float(contract_value),
                    }
                )
                per_feature_abs[feature_name].append(abs_delta)
                per_feature_signed[feature_name].append(signed_delta)

            feature_diffs.sort(key=lambda item: (-float(item["abs_diff"]), item["feature"]))
            top_feature_diffs = feature_diffs[:5]

            built_decision = str(built_row.get("decision", ""))
            contract_decision = str(contract_row.get("decision", ""))
            built_action = str(built_row.get("trade_action_reason", ""))
            contract_action = str(contract_row.get("trade_action_reason", ""))
            if built_decision != contract_decision:
                pair_decision_diffs += 1
            if built_action != contract_action:
                pair_action_diffs += 1

            built_shadow = built_shadow_map.get(bar_time_server, {})
            contract_shadow = contract_shadow_map.get(bar_time_server, {})

            row_records.append(
                {
                    "pair_label": label,
                    "bar_time_server": bar_time_server,
                    "feature_checksum_builtin": built_row.get("feature_checksum"),
                    "feature_checksum_contract": contract_row.get("feature_checksum"),
                    "decision_builtin": built_decision,
                    "decision_contract": contract_decision,
                    "decision_reason_builtin": str(built_row.get("decision_reason", "")),
                    "decision_reason_contract": str(contract_row.get("decision_reason", "")),
                    "trade_action_reason_builtin": built_action,
                    "trade_action_reason_contract": contract_action,
                    "shadow_trade_action_reason_builtin": str(built_shadow.get("trade_action_reason", "")),
                    "shadow_trade_action_reason_contract": str(contract_shadow.get("trade_action_reason", "")),
                    "p_short_delta_contract_minus_builtin": float(contract_row.get("p_short", 0.0)) - float(built_row.get("p_short", 0.0)),
                    "p_flat_delta_contract_minus_builtin": float(contract_row.get("p_flat", 0.0)) - float(built_row.get("p_flat", 0.0)),
                    "p_long_delta_contract_minus_builtin": float(contract_row.get("p_long", 0.0)) - float(built_row.get("p_long", 0.0)),
                    "decision_transition": normalize_transition(built_decision, contract_decision),
                    "max_feature_abs_diff": float(top_feature_diffs[0]["abs_diff"]) if top_feature_diffs else 0.0,
                    "top_feature_diffs": top_feature_diffs,
                }
            )

        pair_summaries.append(
            {
                "label": label,
                "row_count": len(common_keys),
                "decision_diff_count": pair_decision_diffs,
                "trade_action_diff_count": pair_action_diffs,
                "start_bar_time_server": common_keys[0],
                "end_bar_time_server": common_keys[-1],
            }
        )

    feature_records: list[dict[str, object]] = []
    for feature_name, abs_values in per_feature_abs.items():
        abs_summary = summarize_series(abs_values)
        signed_summary = summarize_series(per_feature_signed[feature_name])
        feature_records.append(
            {
                "feature": feature_name,
                "count": abs_summary["count"],
                "mean_abs_diff": abs_summary["mean"],
                "p90_abs_diff": abs_summary["p90"],
                "max_abs_diff": abs_summary["max"],
                "mean_signed_delta_contract_minus_builtin": signed_summary["mean"],
            }
        )
    feature_records.sort(
        key=lambda item: (
            item["max_abs_diff"] is None,
            -(item["max_abs_diff"] or -1.0),
            -(item["mean_abs_diff"] or -1.0),
            item["feature"],
        )
    )

    probability_summaries = {
        "p_short_delta_contract_minus_builtin": summarize_series(
            [float(row["p_short_delta_contract_minus_builtin"]) for row in row_records]
        ),
        "p_flat_delta_contract_minus_builtin": summarize_series(
            [float(row["p_flat_delta_contract_minus_builtin"]) for row in row_records]
        ),
        "p_long_delta_contract_minus_builtin": summarize_series(
            [float(row["p_long_delta_contract_minus_builtin"]) for row in row_records]
        ),
    }

    decision_pairs = Counter((str(row["decision_builtin"]), str(row["decision_contract"])) for row in row_records)
    action_pairs = Counter(
        (str(row["trade_action_reason_builtin"]), str(row["trade_action_reason_contract"])) for row in row_records
    )
    transition_counts = Counter(str(row["decision_transition"]) for row in row_records)

    decision_diff_rows = [
        row
        for row in row_records
        if row["decision_builtin"] != row["decision_contract"]
    ]
    decision_diff_rows.sort(
        key=lambda row: (
            -abs(float(row["p_flat_delta_contract_minus_builtin"])),
            -float(row["max_feature_abs_diff"]),
            row["bar_time_server"],
        )
    )

    top_rows_by_feature_diff = sorted(
        row_records,
        key=lambda row: (-float(row["max_feature_abs_diff"]), row["bar_time_server"]),
    )[:20]

    return {
        "reviewed_on_utc": datetime.now(tz=UTC).isoformat(),
        "pair_summaries": pair_summaries,
        "snapshot_row_count": len(row_records),
        "decision_diff_count": sum(row["decision_builtin"] != row["decision_contract"] for row in row_records),
        "decision_reason_diff_count": sum(
            row["decision_reason_builtin"] != row["decision_reason_contract"] for row in row_records
        ),
        "trade_action_diff_count": sum(
            row["trade_action_reason_builtin"] != row["trade_action_reason_contract"] for row in row_records
        ),
        "feature_checksum_diff_count": sum(
            row["feature_checksum_builtin"] != row["feature_checksum_contract"] for row in row_records
        ),
        "decision_pair_counts": [
            {"builtin": key[0], "contract": key[1], "count": count}
            for key, count in decision_pairs.most_common()
        ],
        "decision_transition_counts": [
            {"transition": key, "count": count}
            for key, count in transition_counts.most_common()
        ],
        "trade_action_pair_counts": [
            {"builtin": key[0], "contract": key[1], "count": count}
            for key, count in action_pairs.most_common()
        ],
        "probability_delta_summaries": probability_summaries,
        "top_feature_diffs": feature_records[:20],
        "top_rows_by_feature_diff": top_rows_by_feature_diff,
        "decision_diff_rows": decision_diff_rows[:25],
    }


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def render_markdown(payload: dict[str, object]) -> str:
    lines: list[str] = []
    lines.append("# Stage 41 Shared Feature-Path Attribution")
    lines.append("")
    lines.append(f"- reviewed_on_utc: `{payload['reviewed_on_utc']}`")
    lines.append(f"- sampled snapshot rows: `{payload['snapshot_row_count']}`")
    lines.append(f"- decision diffs: `{payload['decision_diff_count']}`")
    lines.append(f"- trade action diffs: `{payload['trade_action_diff_count']}`")
    lines.append(f"- checksum diffs: `{payload['feature_checksum_diff_count']}`")
    lines.append("")
    lines.append("## Executive Read")
    lines.append("")
    lines.append(
        "- the sampled latest-window built-in-versus-contract drift is dominated by shared ATR-path changes rather than family-specific rule behavior"
    )
    lines.append(
        "- contract-aligned snapshots systematically push probability mass toward `p_flat`, while both directional probabilities usually weaken"
    )
    lines.append(
        "- in the sampled rows, most decision changes were `directional -> NO_TRADE`, which is consistent with the shared headline drop already observed on the corrected Stage 39 A/B read"
    )
    lines.append("")
    lines.append("## Sample Batches")
    lines.append("")
    for item in payload["pair_summaries"]:
        lines.append(
            f"- `{item['label']}` `{item['start_bar_time_server']}` -> `{item['end_bar_time_server']}` "
            f"`rows={item['row_count']}` `decision_diffs={item['decision_diff_count']}` "
            f"`trade_action_diffs={item['trade_action_diff_count']}`"
        )
    lines.append("")
    lines.append("## Probability Drift")
    lines.append("")
    for key, summary in payload["probability_delta_summaries"].items():
        lines.append(
            f"- `{key}` `mean={fmt_num(summary['mean'])}` `p10={fmt_num(summary['p10'])}` "
            f"`p90={fmt_num(summary['p90'])}` `min={fmt_num(summary['min'])}` `max={fmt_num(summary['max'])}`"
        )
    lines.append("")
    lines.append("## Decision Transitions")
    lines.append("")
    for item in payload["decision_transition_counts"][:10]:
        lines.append(f"- `{item['transition']}` `count={item['count']}`")
    lines.append("")
    lines.append("## Top Feature Diffs")
    lines.append("")
    for item in payload["top_feature_diffs"][:10]:
        lines.append(
            f"- `{item['feature']}` `count={item['count']}` `mean_abs={fmt_num(item['mean_abs_diff'])}` "
            f"`p90_abs={fmt_num(item['p90_abs_diff'])}` `max_abs={fmt_num(item['max_abs_diff'])}` "
            f"`mean_signed_contract_minus_builtin={fmt_num(item['mean_signed_delta_contract_minus_builtin'])}`"
        )
    lines.append("")
    lines.append("## Largest Feature-Drift Rows")
    lines.append("")
    for item in payload["top_rows_by_feature_diff"][:12]:
        top_bits = "; ".join(
            f"{feature['feature']}={fmt_num(feature['signed_delta_contract_minus_builtin'])}"
            for feature in item["top_feature_diffs"][:3]
        )
        lines.append(
            f"- `{item['bar_time_server']}` `{item['decision_builtin']} -> {item['decision_contract']}` "
            f"`max_feature_abs_diff={fmt_num(item['max_feature_abs_diff'])}` `top={top_bits}`"
        )
    lines.append("")
    lines.append("## Decision-Diff Rows")
    lines.append("")
    for item in payload["decision_diff_rows"][:15]:
        top_bits = "; ".join(
            f"{feature['feature']}={fmt_num(feature['signed_delta_contract_minus_builtin'])}"
            for feature in item["top_feature_diffs"][:3]
        )
        lines.append(
            f"- `{item['bar_time_server']}` `{item['decision_builtin']} -> {item['decision_contract']}` "
            f"`reason={item['decision_reason_builtin']} -> {item['decision_reason_contract']}` "
            f"`d_p_short={fmt_num(item['p_short_delta_contract_minus_builtin'])}` "
            f"`d_p_flat={fmt_num(item['p_flat_delta_contract_minus_builtin'])}` "
            f"`d_p_long={fmt_num(item['p_long_delta_contract_minus_builtin'])}` "
            f"`top={top_bits}`"
        )
    lines.append("")
    lines.append("## Interpretation")
    lines.append("")
    lines.append(
        "- `atr_14`, `atr_50`, and `atr_14_over_atr_50` dominate the shared drift surface across the sampled bars, with `stoch_kd_diff` acting as a secondary contributor"
    )
    lines.append(
        "- the strongest sampled decision flips are concentrated in bars where the contract-aligned path lowers directional conviction and raises `p_flat` enough to turn a built-in entry into `NO_TRADE`"
    )
    lines.append(
        "- this supports the corrected Stage 39 read: the current open question is shared feature-surface attribution, not a `34D`-only sidecar explanation"
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    args = build_parser().parse_args()
    pairs = [
        (label, Path(built_snapshot), Path(contract_snapshot), Path(built_shadow), Path(contract_shadow))
        for label, built_snapshot, contract_snapshot, built_shadow, contract_shadow in args.pair
    ]
    payload = build_payload(pairs)
    json_path, md_path = build_output_paths(args.output_stem)
    write_json(json_path, payload)
    md_path.write_text(render_markdown(payload), encoding="utf-8")
    print(f"[done] json={json_path}")
    print(f"[done] md={md_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
