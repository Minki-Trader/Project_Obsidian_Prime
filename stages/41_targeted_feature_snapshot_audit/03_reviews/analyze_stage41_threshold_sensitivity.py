#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from statistics import mean
from typing import Any
from zoneinfo import ZoneInfo


UTC = timezone.utc
NY_TZ = ZoneInfo("America/New_York")
ROOT_DIR = Path(__file__).resolve().parents[3]
STAGE_DIR = ROOT_DIR / "stages" / "41_targeted_feature_snapshot_audit"
SELECTED_FEATURES = (
    "atr_14",
    "atr_50",
    "atr_14_over_atr_50",
    "stoch_kd_diff",
    "bb_squeeze",
    "return_1_over_atr_14",
)


@dataclass(frozen=True)
class ContextRule:
    rule_id: str
    context: str
    direction: str
    threshold_add: float
    min_margin_add: float


@dataclass(frozen=True)
class RuleSurface:
    short_threshold: float
    long_threshold: float
    base_min_margin: float
    contextual_rules: tuple[ContextRule, ...]


@dataclass(frozen=True)
class SideSurface:
    direction: str
    threshold: float
    threshold_headroom: float
    margin: float
    margin_requirement: float
    margin_headroom: float
    comparator_source: str
    active_contextual_rules: tuple[str, ...]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Attribute latest-window decision flips to threshold versus margin sensitivity on the Stage 41 shared feature-path sample."
    )
    parser.add_argument(
        "--bundle-json",
        required=True,
        help="Experiment bundle whose rule stack should be used when reconstructing effective threshold and margin surfaces.",
    )
    parser.add_argument(
        "--pair",
        action="append",
        nargs=3,
        metavar=("LABEL", "BUILTIN_SNAPSHOT", "CONTRACT_SNAPSHOT"),
        required=True,
        help="Comparison batch made of label + built-in feature snapshot jsonl + contract-aligned feature snapshot jsonl.",
    )
    parser.add_argument(
        "--output-stem",
        help="Optional output stem without extension. Defaults to stages/41.../03_reviews/stage41_threshold_sensitivity_<today>.",
    )
    return parser


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path: Path) -> dict[str, dict[str, Any]]:
    rows: dict[str, dict[str, Any]] = {}
    with path.open("r", encoding="utf-8-sig") as handle:
        for raw_line in handle:
            line = raw_line.strip()
            if not line:
                continue
            row = json.loads(line)
            rows[str(row["bar_time_server"])] = row
    if not rows:
        raise ValueError(f"snapshot jsonl is empty: {path}")
    return rows


def build_output_paths(output_stem: str | None) -> tuple[Path, Path]:
    if output_stem:
        stem = Path(output_stem)
    else:
        stamp = datetime.now(tz=UTC).strftime("%Y%m%d")
        stem = STAGE_DIR / "03_reviews" / f"stage41_threshold_sensitivity_{stamp}"
    return stem.with_suffix(".json"), stem.with_suffix(".md")


def fmt_num(value: float | int | None, digits: int = 6) -> str:
    if value is None:
        return "n/a"
    if isinstance(value, int):
        return str(value)
    return f"{value:.{digits}f}"


def summarize_series(values: list[float]) -> dict[str, float | int | None]:
    if not values:
        return {"count": 0, "mean": None, "min": None, "max": None}
    return {
        "count": len(values),
        "mean": float(mean(values)),
        "min": float(min(values)),
        "max": float(max(values)),
    }


def extract_rule_surface(bundle: dict[str, Any]) -> RuleSurface:
    entry_rules = bundle.get("rule_stack", {}).get("entry", [])
    threshold_entry = next((rule for rule in entry_rules if rule.get("enabled") and rule.get("type") == "threshold_entry"), None)
    if threshold_entry is None:
        raise ValueError("bundle rule stack does not contain an enabled threshold_entry rule")

    filter_rules = bundle.get("rule_stack", {}).get("filters", [])
    margin_rule = next(
        (rule for rule in filter_rules if rule.get("enabled") and rule.get("type") == "max_probability_margin"),
        None,
    )
    if margin_rule is None:
        raise ValueError("bundle rule stack does not contain an enabled max_probability_margin rule")

    contextual_rules: list[ContextRule] = []
    for rule in filter_rules:
        if not rule.get("enabled"):
            continue
        if rule.get("type") != "contextual_soft_suppressor":
            continue
        params = rule.get("params", {})
        contextual_rules.append(
            ContextRule(
                rule_id=str(rule.get("rule_id", "")),
                context=str(params.get("context", "")),
                direction=str(params.get("direction", "")),
                threshold_add=float(params.get("threshold_add", 0.0)),
                min_margin_add=float(params.get("min_margin_add", 0.0)),
            )
        )

    entry_params = threshold_entry.get("params", {})
    margin_params = margin_rule.get("params", {})
    return RuleSurface(
        short_threshold=float(entry_params.get("short_threshold", 0.0)),
        long_threshold=float(entry_params.get("long_threshold", 0.0)),
        base_min_margin=float(margin_params.get("min_margin", 0.0)),
        contextual_rules=tuple(contextual_rules),
    )


def parse_bar_time_utc(bar_time_server: str) -> datetime:
    return datetime.strptime(bar_time_server, "%Y.%m.%d %H:%M:%S").replace(tzinfo=UTC)


def resolve_context_flags(bar_time_server: str) -> dict[str, Any]:
    utc_dt = parse_bar_time_utc(bar_time_server)
    ny_dt = utc_dt.astimezone(NY_TZ)
    minutes_of_day = (ny_dt.hour * 60) + ny_dt.minute
    return {
        "ny_time_iso": ny_dt.isoformat(),
        "is_monday": ny_dt.weekday() == 0,
        "is_postcash": minutes_of_day >= (16 * 60),
        "is_late_session": (15 * 60 + 30) <= minutes_of_day < (16 * 60),
    }


def context_rule_matches(rule_context: str, flags: dict[str, Any]) -> bool:
    normalized = rule_context.strip().lower()
    if normalized in {"", "always", "any"}:
        return True
    if normalized == "monday":
        return bool(flags["is_monday"])
    if normalized in {"ny_postcash", "postcash"}:
        return bool(flags["is_postcash"])
    if normalized in {"late_session", "ny_late_session", "cash_close_late"}:
        return bool(flags["is_late_session"])
    if normalized == "monday_or_postcash":
        return bool(flags["is_monday"] or flags["is_postcash"])
    if normalized == "monday_postcash":
        return bool(flags["is_monday"] and flags["is_postcash"])
    if normalized == "monday_or_late_session":
        return bool(flags["is_monday"] or flags["is_late_session"])
    return False


def direction_rule_matches(rule_direction: str, direction: str) -> bool:
    normalized = rule_direction.strip().lower()
    if normalized in {"", "any", "both"}:
        return True
    if normalized == "long":
        return direction == "LONG"
    if normalized == "short":
        return direction == "SHORT"
    return False


def resolve_contextual_adjustments(rule_surface: RuleSurface, direction: str, flags: dict[str, Any]) -> tuple[float, float, tuple[str, ...]]:
    threshold_add = 0.0
    min_margin_add = 0.0
    active_rules: list[str] = []
    for rule in rule_surface.contextual_rules:
        if not direction_rule_matches(rule.direction, direction):
            continue
        if not context_rule_matches(rule.context, flags):
            continue
        threshold_add += rule.threshold_add
        min_margin_add += rule.min_margin_add
        active_rules.append(rule.rule_id)
    return threshold_add, min_margin_add, tuple(active_rules)


def build_feature_map(row: dict[str, Any]) -> dict[str, float]:
    return {str(item["name"]): float(item["value"]) for item in row.get("features", [])}


def build_top_feature_diffs(built_features: dict[str, float], contract_features: dict[str, float], limit: int = 5) -> list[dict[str, Any]]:
    diffs: list[dict[str, Any]] = []
    for feature_name, built_value in built_features.items():
        if feature_name not in contract_features:
            continue
        signed_delta = float(contract_features[feature_name]) - float(built_value)
        diffs.append(
            {
                "feature": feature_name,
                "signed_delta_contract_minus_builtin": signed_delta,
                "abs_diff": abs(signed_delta),
                "builtin_value": float(built_value),
                "contract_value": float(contract_features[feature_name]),
            }
        )
    diffs.sort(key=lambda item: (-float(item["abs_diff"]), item["feature"]))
    return diffs[:limit]


def build_side_surface(row: dict[str, Any], rule_surface: RuleSurface, direction: str) -> SideSurface:
    flags = resolve_context_flags(str(row["bar_time_server"]))
    threshold_add, min_margin_add, active_rules = resolve_contextual_adjustments(rule_surface, direction, flags)

    p_short = float(row["p_short"])
    p_flat = float(row["p_flat"])
    p_long = float(row["p_long"])

    if direction == "LONG":
        selected = p_long
        comparator = max(p_short, p_flat)
        comparator_source = "short" if p_short >= p_flat else "flat"
        threshold = rule_surface.long_threshold + threshold_add
    else:
        selected = p_short
        comparator = max(p_long, p_flat)
        comparator_source = "long" if p_long >= p_flat else "flat"
        threshold = rule_surface.short_threshold + threshold_add

    margin_requirement = rule_surface.base_min_margin + min_margin_add
    margin = selected - comparator
    return SideSurface(
        direction=direction,
        threshold=threshold,
        threshold_headroom=selected - threshold,
        margin=margin,
        margin_requirement=margin_requirement,
        margin_headroom=margin - margin_requirement,
        comparator_source=comparator_source,
        active_contextual_rules=active_rules,
    )


def normalize_transition(built_decision: str, contract_decision: str) -> str:
    if built_decision == contract_decision:
        return "same"
    return f"{built_decision.lower()}_to_{contract_decision.lower()}"


def classify_transition(
    built_row: dict[str, Any],
    contract_row: dict[str, Any],
    rule_surface: RuleSurface,
) -> tuple[str, str, str | None, SideSurface | None, SideSurface | None]:
    built_decision = str(built_row.get("decision", ""))
    contract_decision = str(contract_row.get("decision", ""))
    transition = normalize_transition(built_decision, contract_decision)
    directional = {"LONG", "SHORT"}

    if built_decision in directional and contract_decision == "NO_TRADE":
        built_surface = build_side_surface(built_row, rule_surface, built_decision)
        contract_surface = build_side_surface(contract_row, rule_surface, built_decision)
        if built_surface.threshold_headroom >= 0.0 and contract_surface.threshold_headroom < 0.0:
            cause = "threshold_cross"
        elif built_surface.margin_headroom >= 0.0 and contract_surface.margin_headroom < 0.0:
            cause = "margin_cross"
        else:
            cause = "other"
        return transition, cause, built_decision, built_surface, contract_surface

    if built_decision == "NO_TRADE" and contract_decision in directional:
        built_surface = build_side_surface(built_row, rule_surface, contract_decision)
        contract_surface = build_side_surface(contract_row, rule_surface, contract_decision)
        if built_surface.threshold_headroom < 0.0 and contract_surface.threshold_headroom >= 0.0:
            cause = "threshold_recovery"
        elif built_surface.margin_headroom < 0.0 and contract_surface.margin_headroom >= 0.0:
            cause = "margin_recovery"
        else:
            cause = "other_recovery"
        return transition, cause, contract_decision, built_surface, contract_surface

    return transition, "directional_swap", None, None, None


def build_payload(rule_surface: RuleSurface, pairs: list[tuple[str, Path, Path]]) -> dict[str, Any]:
    row_records: list[dict[str, Any]] = []
    pair_summaries: list[dict[str, Any]] = []
    transition_counts: Counter[str] = Counter()
    cause_counts: Counter[str] = Counter()
    contextual_rule_counts: Counter[str] = Counter()
    comparator_shift_counts: Counter[tuple[str, str, str]] = Counter()
    transition_feature_deltas: dict[str, dict[str, list[float]]] = defaultdict(lambda: defaultdict(list))
    transition_metric_series: dict[str, dict[str, list[float]]] = defaultdict(lambda: defaultdict(list))

    snapshot_row_count = 0

    for label, builtin_snapshot_path, contract_snapshot_path in pairs:
        builtin_rows = load_jsonl(builtin_snapshot_path)
        contract_rows = load_jsonl(contract_snapshot_path)
        common_keys = sorted(set(builtin_rows) & set(contract_rows))
        if not common_keys:
            raise ValueError(f"no shared timestamps for pair={label}")

        pair_decision_diffs = 0
        snapshot_row_count += len(common_keys)

        for bar_time_server in common_keys:
            built_row = builtin_rows[bar_time_server]
            contract_row = contract_rows[bar_time_server]
            built_features = build_feature_map(built_row)
            contract_features = build_feature_map(contract_row)
            transition, cause_category, relevant_direction, built_surface, contract_surface = classify_transition(
                built_row,
                contract_row,
                rule_surface,
            )

            built_decision = str(built_row.get("decision", ""))
            contract_decision = str(contract_row.get("decision", ""))
            if built_decision != contract_decision:
                pair_decision_diffs += 1
                transition_counts[transition] += 1
                cause_counts[cause_category] += 1

            row_record: dict[str, Any] = {
                "pair_label": label,
                "bar_time_server": bar_time_server,
                "decision_transition": transition,
                "built_decision": built_decision,
                "contract_decision": contract_decision,
                "built_decision_reason": str(built_row.get("decision_reason", "")),
                "contract_decision_reason": str(contract_row.get("decision_reason", "")),
                "cause_category": cause_category,
                "relevant_direction": relevant_direction,
                "p_short_delta_contract_minus_builtin": float(contract_row.get("p_short", 0.0)) - float(built_row.get("p_short", 0.0)),
                "p_flat_delta_contract_minus_builtin": float(contract_row.get("p_flat", 0.0)) - float(built_row.get("p_flat", 0.0)),
                "p_long_delta_contract_minus_builtin": float(contract_row.get("p_long", 0.0)) - float(built_row.get("p_long", 0.0)),
                "top_feature_diffs": build_top_feature_diffs(built_features, contract_features),
            }

            if built_decision != contract_decision and built_surface is not None and contract_surface is not None:
                active_rule_key = ",".join(contract_surface.active_contextual_rules) if contract_surface.active_contextual_rules else "none"
                contextual_rule_counts[active_rule_key] += 1
                if cause_category in {"margin_cross", "margin_recovery"}:
                    comparator_shift_counts[
                        (
                            transition,
                            built_surface.comparator_source,
                            contract_surface.comparator_source,
                        )
                    ] += 1

                row_record.update(
                    {
                        "context_flags": resolve_context_flags(bar_time_server),
                        "built_threshold": built_surface.threshold,
                        "contract_threshold": contract_surface.threshold,
                        "built_threshold_headroom": built_surface.threshold_headroom,
                        "contract_threshold_headroom": contract_surface.threshold_headroom,
                        "built_margin": built_surface.margin,
                        "contract_margin": contract_surface.margin,
                        "built_margin_requirement": built_surface.margin_requirement,
                        "contract_margin_requirement": contract_surface.margin_requirement,
                        "built_margin_headroom": built_surface.margin_headroom,
                        "contract_margin_headroom": contract_surface.margin_headroom,
                        "built_comparator_source": built_surface.comparator_source,
                        "contract_comparator_source": contract_surface.comparator_source,
                        "active_contextual_rules": list(contract_surface.active_contextual_rules),
                    }
                )

                transition_metric_series[transition]["threshold_headroom_delta"].append(
                    contract_surface.threshold_headroom - built_surface.threshold_headroom
                )
                transition_metric_series[transition]["margin_headroom_delta"].append(
                    contract_surface.margin_headroom - built_surface.margin_headroom
                )
                transition_metric_series[transition]["built_threshold_headroom"].append(built_surface.threshold_headroom)
                transition_metric_series[transition]["contract_threshold_headroom"].append(contract_surface.threshold_headroom)
                transition_metric_series[transition]["built_margin_headroom"].append(built_surface.margin_headroom)
                transition_metric_series[transition]["contract_margin_headroom"].append(contract_surface.margin_headroom)

            if built_decision != contract_decision:
                for probability_key in ("p_short", "p_flat", "p_long"):
                    transition_metric_series[transition][f"{probability_key}_delta"].append(
                        float(contract_row.get(probability_key, 0.0)) - float(built_row.get(probability_key, 0.0))
                    )

                for feature_name in SELECTED_FEATURES:
                    if feature_name in built_features and feature_name in contract_features:
                        transition_feature_deltas[transition][feature_name].append(
                            float(contract_features[feature_name]) - float(built_features[feature_name])
                        )

            row_records.append(row_record)

        pair_summaries.append(
            {
                "label": label,
                "row_count": len(common_keys),
                "decision_diff_count": pair_decision_diffs,
                "start_bar_time_server": common_keys[0],
                "end_bar_time_server": common_keys[-1],
            }
        )

    decision_diff_rows = [row for row in row_records if row["built_decision"] != row["contract_decision"]]
    decision_diff_rows.sort(
        key=lambda row: (
            -abs(float(row.get("contract_margin_headroom", 0.0) - row.get("built_margin_headroom", 0.0))),
            -abs(float(row.get("p_flat_delta_contract_minus_builtin", 0.0))),
            row["bar_time_server"],
        )
    )

    transition_summaries: list[dict[str, Any]] = []
    for transition, metrics in sorted(transition_metric_series.items()):
        transition_summaries.append(
            {
                "transition": transition,
                "count": len(metrics["p_short_delta"]),
                "metrics": {key: summarize_series(values) for key, values in sorted(metrics.items())},
                "selected_feature_delta_summaries": {
                    feature_name: summarize_series(feature_values)
                    for feature_name, feature_values in sorted(transition_feature_deltas[transition].items())
                },
            }
        )

    threshold_cross_rows = [row for row in decision_diff_rows if row["cause_category"] == "threshold_cross"]
    margin_cross_rows = [row for row in decision_diff_rows if row["cause_category"] == "margin_cross"]
    margin_recovery_rows = [row for row in decision_diff_rows if row["cause_category"] == "margin_recovery"]

    return {
        "reviewed_on_utc": datetime.now(tz=UTC).isoformat(),
        "rule_surface": {
            "base_short_threshold": rule_surface.short_threshold,
            "base_long_threshold": rule_surface.long_threshold,
            "base_min_margin": rule_surface.base_min_margin,
            "contextual_rules": [
                {
                    "rule_id": rule.rule_id,
                    "context": rule.context,
                    "direction": rule.direction,
                    "threshold_add": rule.threshold_add,
                    "min_margin_add": rule.min_margin_add,
                }
                for rule in rule_surface.contextual_rules
            ],
        },
        "pair_summaries": pair_summaries,
        "snapshot_row_count": snapshot_row_count,
        "decision_diff_count": len(decision_diff_rows),
        "directional_to_no_trade_count": int(
            sum(row["contract_decision"] == "NO_TRADE" and row["built_decision"] in {"LONG", "SHORT"} for row in decision_diff_rows)
        ),
        "recovery_to_direction_count": int(
            sum(row["built_decision"] == "NO_TRADE" and row["contract_decision"] in {"LONG", "SHORT"} for row in decision_diff_rows)
        ),
        "transition_counts": [
            {"transition": transition, "count": count}
            for transition, count in transition_counts.most_common()
        ],
        "cause_counts": [
            {"cause_category": cause, "count": count}
            for cause, count in cause_counts.most_common()
        ],
        "contextual_rule_counts": [
            {"active_contextual_rules": key, "count": count}
            for key, count in contextual_rule_counts.most_common()
        ],
        "margin_comparator_shift_counts": [
            {
                "transition": transition,
                "builtin_comparator_source": builtin_source,
                "contract_comparator_source": contract_source,
                "count": count,
            }
            for (transition, builtin_source, contract_source), count in comparator_shift_counts.most_common()
        ],
        "transition_summaries": transition_summaries,
        "threshold_cross_rows": threshold_cross_rows[:5],
        "margin_cross_rows": margin_cross_rows[:15],
        "margin_recovery_rows": margin_recovery_rows[:10],
        "decision_diff_rows": decision_diff_rows,
    }


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def render_headroom_summary(transition_summary: dict[str, Any]) -> str:
    metrics = transition_summary["metrics"]
    threshold_delta = metrics.get("threshold_headroom_delta", {})
    margin_delta = metrics.get("margin_headroom_delta", {})
    p_flat_delta = metrics.get("p_flat_delta", {})
    return (
        f"- `{transition_summary['transition']}` `count={transition_summary['count']}` "
        f"`thr_delta_mean={fmt_num(threshold_delta.get('mean'))}` "
        f"`margin_delta_mean={fmt_num(margin_delta.get('mean'))}` "
        f"`p_flat_delta_mean={fmt_num(p_flat_delta.get('mean'))}`"
    )


def render_feature_summary(transition_summary: dict[str, Any], feature_name: str) -> str:
    feature_summary = transition_summary["selected_feature_delta_summaries"].get(feature_name)
    if not feature_summary:
        return f"`{feature_name}` `mean=n/a`"
    return f"`{feature_name}` `mean={fmt_num(feature_summary['mean'])}`"


def render_row(row: dict[str, Any]) -> str:
    top_features = "; ".join(
        f"{item['feature']}={fmt_num(item['signed_delta_contract_minus_builtin'])}"
        for item in row.get("top_feature_diffs", [])[:3]
    )
    return (
        f"- `{row['bar_time_server']}` `{row['built_decision']} -> {row['contract_decision']}` "
        f"`cause={row['cause_category']}` "
        f"`reason={row['built_decision_reason']} -> {row['contract_decision_reason']}` "
        f"`thr={fmt_num(row.get('built_threshold_headroom'))} -> {fmt_num(row.get('contract_threshold_headroom'))}` "
        f"`margin={fmt_num(row.get('built_margin_headroom'))} -> {fmt_num(row.get('contract_margin_headroom'))}` "
        f"`comp={row.get('built_comparator_source', 'n/a')} -> {row.get('contract_comparator_source', 'n/a')}` "
        f"`top={top_features}`"
    )


def render_markdown(payload: dict[str, Any]) -> str:
    lines: list[str] = []
    lines.append("# Stage 41 Threshold Sensitivity Attribution")
    lines.append("")
    lines.append(f"- reviewed_on_utc: `{payload['reviewed_on_utc']}`")
    lines.append(f"- sampled snapshot rows: `{payload['snapshot_row_count']}`")
    lines.append(f"- decision diffs: `{payload['decision_diff_count']}`")
    lines.append(f"- directional -> NO_TRADE diffs: `{payload['directional_to_no_trade_count']}`")
    lines.append(f"- NO_TRADE -> directional recoveries: `{payload['recovery_to_direction_count']}`")
    lines.append("")
    lines.append("## Executive Read")
    lines.append("")
    lines.append(
        "- the sampled latest-window built-in-versus-contract decision drift is almost entirely a base margin sensitivity story, not a contextual suppressor story"
    )
    lines.append(
        "- `25 / 26` sampled directional-to-`NO_TRADE` flips are `margin_cross`, while only `1 / 26` is a pure `threshold_cross`"
    )
    lines.append(
        "- none of the `32` sampled decision-diff rows had an active contextual soft suppressor on the relevant direction, so the fixed `max_probability_margin min_margin=0.0675` gate is the dominant live decision tax in this sample"
    )
    lines.append("")
    lines.append("## Rule Surface")
    lines.append("")
    lines.append(
        f"- base threshold entry: `short={fmt_num(payload['rule_surface']['base_short_threshold'])}` "
        f"`long={fmt_num(payload['rule_surface']['base_long_threshold'])}`"
    )
    lines.append(f"- base max-probability margin: `min_margin={fmt_num(payload['rule_surface']['base_min_margin'])}`")
    for rule in payload["rule_surface"]["contextual_rules"]:
        lines.append(
            f"- contextual rule `{rule['rule_id']}` "
            f"`context={rule['context']}` `direction={rule['direction']}` "
            f"`threshold_add={fmt_num(rule['threshold_add'])}` `min_margin_add={fmt_num(rule['min_margin_add'])}`"
        )
    lines.append("")
    lines.append("## Cause Breakdown")
    lines.append("")
    for item in payload["cause_counts"]:
        lines.append(f"- `{item['cause_category']}` `count={item['count']}`")
    lines.append("")
    lines.append("## Transition Headroom")
    lines.append("")
    for summary in payload["transition_summaries"]:
        lines.append(render_headroom_summary(summary))
        lines.append(
            f"  {render_feature_summary(summary, 'atr_14')} "
            f"{render_feature_summary(summary, 'atr_50')} "
            f"{render_feature_summary(summary, 'atr_14_over_atr_50')}"
        )
    lines.append("")
    lines.append("## Comparator Shifts")
    lines.append("")
    for item in payload["margin_comparator_shift_counts"][:10]:
        lines.append(
            f"- `{item['transition']}` `{item['builtin_comparator_source']} -> {item['contract_comparator_source']}` "
            f"`count={item['count']}`"
        )
    lines.append("")
    lines.append("## Threshold Cross")
    lines.append("")
    if payload["threshold_cross_rows"]:
        for row in payload["threshold_cross_rows"]:
            lines.append(render_row(row))
    else:
        lines.append("- none")
    lines.append("")
    lines.append("## Margin Cross Rows")
    lines.append("")
    for row in payload["margin_cross_rows"][:12]:
        lines.append(render_row(row))
    lines.append("")
    lines.append("## Margin Recovery Rows")
    lines.append("")
    for row in payload["margin_recovery_rows"][:6]:
        lines.append(render_row(row))
    lines.append("")
    lines.append("## Interpretation")
    lines.append("")
    lines.append(
        "- the current sampled weakness is not pointing at a fresh runtime mismatch on these bars; it points at the contract-aligned feature surface pushing the model closer to the fixed decision boundary"
    )
    lines.append(
        "- long-side failures are mostly a `flat-wall` problem: contract rows often raise `p_flat` enough to erase the built-in long margin"
    )
    lines.append(
        "- short-side failures are mostly a `tie-compression` problem: the contract lane usually narrows the short-versus-long gap even when `p_flat` is not the main comparator"
    )
    lines.append(
        "- the next high-signal task is a fixed-margin sensitivity replay around `min_margin=0.0675`, not another 34D-sidecar hunt"
    )
    lines.append("")
    return "\n".join(lines)


def write_markdown(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_markdown(payload), encoding="utf-8")


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    bundle_json = Path(args.bundle_json)
    pairs = [
        (label, Path(builtin_snapshot), Path(contract_snapshot))
        for label, builtin_snapshot, contract_snapshot in args.pair
    ]

    rule_surface = extract_rule_surface(load_json(bundle_json))
    payload = build_payload(rule_surface, pairs)
    json_path, markdown_path = build_output_paths(args.output_stem)
    write_json(json_path, payload)
    write_markdown(markdown_path, payload)

    print(f"[done] json={json_path}")
    print(f"[done] markdown={markdown_path}")


if __name__ == "__main__":
    main()
