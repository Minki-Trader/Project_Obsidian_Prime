from __future__ import annotations

import csv
import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[3]
STAGE_DIR = PROJECT_ROOT / "stages" / "22_point_exit_management"
REVIEW_DIR = STAGE_DIR / "03_reviews"

SPLITS = {
    "hist_2024": {
        "label": "2024 historical",
        "baseline": Path(
            r"C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\Common\Files\Project_Obsidian_Prime\runtime\exp_22a_05dp_base_hist_2024_v1\logs\att_0001_trades.csv"
        ),
    },
    "val_2501": {
        "label": "2025 validation Jan-Sep",
        "baseline": Path(
            r"C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\Common\Files\Project_Obsidian_Prime\runtime\exp_22a_05dp_base_val_2501_v1\logs\att_0002_trades.csv"
        ),
    },
    "oos_2501": {
        "label": "2501 OOS",
        "baseline": Path(
            r"C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\Common\Files\Project_Obsidian_Prime\runtime\exp_22a_05dp_base_oos_2501_v1\logs\att_0003_trades.csv"
        ),
    },
}

VARIANT_PATHS = {
    "22B": {
        "label": "break_even",
        "event_reason": "BREAK_EVEN_STOP",
        "paths": {
            "hist_2024": Path(
                r"C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\Common\Files\Project_Obsidian_Prime\runtime\exp_22b_05dp_be50_lock10_v1_hist_2024\logs\att_0001_trades.csv"
            ),
            "val_2501": Path(
                r"C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\Common\Files\Project_Obsidian_Prime\runtime\exp_22b_05dp_be50_lock10_v1_val_2501\logs\att_0002_trades.csv"
            ),
            "oos_2501": Path(
                r"C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\Common\Files\Project_Obsidian_Prime\runtime\exp_22b_05dp_be50_lock10_v1_oos_2501\logs\att_0003_trades.csv"
            ),
        },
    },
    "22C": {
        "label": "trailing_stop",
        "event_reason": "TRAIL_STOP",
        "paths": {
            "hist_2024": Path(
                r"C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\Common\Files\Project_Obsidian_Prime\runtime\exp_22c_05dp_trail60_dist35_v1_hist_2024\logs\att_0001_trades.csv"
            ),
            "val_2501": Path(
                r"C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\Common\Files\Project_Obsidian_Prime\runtime\exp_22c_05dp_trail60_dist35_v1_val_2501\logs\att_0002_trades.csv"
            ),
            "oos_2501": Path(
                r"C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\Common\Files\Project_Obsidian_Prime\runtime\exp_22c_05dp_trail60_dist35_v1_oos_2501\logs\att_0003_trades.csv"
            ),
        },
    },
    "22D": {
        "label": "partial_stop_loss",
        "event_reason": "PARTIAL_STOP_LOSS",
        "paths": {
            "hist_2024": Path(
                r"C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\Common\Files\Project_Obsidian_Prime\runtime\exp_22d_05dp_psl45_half_v1_hist_2024\logs\att_0001_trades.csv"
            ),
            "val_2501": Path(
                r"C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\Common\Files\Project_Obsidian_Prime\runtime\exp_22d_05dp_psl45_half_v1_val_2501\logs\att_0002_trades.csv"
            ),
            "oos_2501": Path(
                r"C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\Common\Files\Project_Obsidian_Prime\runtime\exp_22d_05dp_psl45_half_v1_oos_2501\logs\att_0003_trades.csv"
            ),
        },
    },
    "22E": {
        "label": "partial_take_profit",
        "event_reason": "PARTIAL_TAKE_PROFIT",
        "paths": {
            "hist_2024": Path(
                r"C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\Common\Files\Project_Obsidian_Prime\runtime\exp_22e_05dp_ptp60_half_v1_hist_2024\logs\att_0001_trades.csv"
            ),
            "val_2501": Path(
                r"C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\Common\Files\Project_Obsidian_Prime\runtime\exp_22e_05dp_ptp60_half_v1_val_2501\logs\att_0002_trades.csv"
            ),
            "oos_2501": Path(
                r"C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\Common\Files\Project_Obsidian_Prime\runtime\exp_22e_05dp_ptp60_half_v1_oos_2501\logs\att_0003_trades.csv"
            ),
        },
    },
}

PROFIT_THRESHOLDS = [4.0, 4.5, 5.0, 5.5, 6.0, 7.0, 8.0]
LOSS_THRESHOLDS = [4.0, 4.5, 5.0, 5.5, 6.0, 7.0, 8.0]


def parse_float(value: str) -> float:
    return float(value) if value not in ("", None) else 0.0


def round_or_none(value: float | None, digits: int = 4) -> float | None:
    if value is None:
        return None
    return round(value, digits)


def load_position_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def load_grouped_positions(path: Path) -> dict[str, dict[str, Any]]:
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in load_position_rows(path):
        grouped[row["position_identifier"]].append(row)

    positions: dict[str, dict[str, Any]] = {}
    for position_id, rows in grouped.items():
        rows.sort(key=lambda row: (row["exit_time_server"], row["event_timestamp_gmt"], row["close_reason"]))
        first = rows[0]
        positions[first["entry_bar_time_server"] + "|" + first["direction"]] = {
            "position_id": position_id,
            "direction": first["direction"],
            "entry_bar_time_server": first["entry_bar_time_server"],
            "net_profit": round(sum(parse_float(row["net_profit"]) for row in rows), 4),
            "max_floating_profit": max(parse_float(row["max_floating_profit"]) for row in rows),
            "min_floating_profit": min(parse_float(row["min_floating_profit"]) for row in rows),
            "event_rows": rows,
        }
    return positions


def hit_rate(values: list[float], threshold: float, mode: str) -> float | None:
    if not values:
        return None
    if mode == "profit":
        hits = sum(1 for value in values if value >= threshold)
    else:
        hits = sum(1 for value in values if abs(value) >= threshold)
    return hits / len(values)


def build_analysis() -> dict[str, Any]:
    baseline_positions = {
        split_name: load_grouped_positions(split_info["baseline"])
        for split_name, split_info in SPLITS.items()
    }

    analysis: dict[str, Any] = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "threshold_unit_note": "trade ledger floating profit/loss is in account currency at fixed 0.1 lot; for these runs, about 10 points ~= 1.0 currency unit",
        "baseline_trigger_zones": {},
        "variant_event_timing": {},
        "recommendations": {},
    }

    for split_name, positions in baseline_positions.items():
        wins = [position for position in positions.values() if position["net_profit"] > 0.0]
        losses = [position for position in positions.values() if position["net_profit"] < 0.0]
        win_max = [position["max_floating_profit"] for position in wins]
        loss_max = [position["max_floating_profit"] for position in losses]
        win_min = [position["min_floating_profit"] for position in wins]
        loss_min = [position["min_floating_profit"] for position in losses]

        analysis["baseline_trigger_zones"][split_name] = {
            "label": SPLITS[split_name]["label"],
            "position_count": len(positions),
            "winner_count": len(wins),
            "loser_count": len(losses),
            "profit_thresholds": [
                {
                    "threshold_currency": threshold,
                    "threshold_points_approx": round(threshold * 10.0, 1),
                    "winner_hit_rate": round_or_none(hit_rate(win_max, threshold, "profit")),
                    "loser_hit_rate": round_or_none(hit_rate(loss_max, threshold, "profit")),
                    "separation_gap": round_or_none(
                        (hit_rate(win_max, threshold, "profit") or 0.0)
                        - (hit_rate(loss_max, threshold, "profit") or 0.0)
                    ),
                }
                for threshold in PROFIT_THRESHOLDS
            ],
            "loss_thresholds": [
                {
                    "threshold_currency": threshold,
                    "threshold_points_approx": round(threshold * 10.0, 1),
                    "winner_hit_rate": round_or_none(hit_rate(win_min, threshold, "loss")),
                    "loser_hit_rate": round_or_none(hit_rate(loss_min, threshold, "loss")),
                    "separation_gap": round_or_none(
                        (hit_rate(loss_min, threshold, "loss") or 0.0)
                        - (hit_rate(win_min, threshold, "loss") or 0.0)
                    ),
                }
                for threshold in LOSS_THRESHOLDS
            ],
        }

    for variant_code, variant_info in VARIANT_PATHS.items():
        split_payload: dict[str, Any] = {}
        for split_name, path in variant_info["paths"].items():
            base = baseline_positions[split_name]
            variant = load_grouped_positions(path)
            hold_bar_counts = Counter()
            class_counts = Counter()
            for match_key, position in variant.items():
                if match_key not in base:
                    continue
                baseline_class = "winner" if base[match_key]["net_profit"] > 0.0 else "loser"
                for row in position["event_rows"]:
                    if row["close_reason"] != variant_info["event_reason"]:
                        continue
                    hold_bars = int(row["hold_bars"])
                    hold_bar_counts[hold_bars] += 1
                    class_counts[(hold_bars, baseline_class)] += 1

            split_payload[split_name] = {
                "label": SPLITS[split_name]["label"],
                "event_reason": variant_info["event_reason"],
                "hold_bar_counts": dict(sorted(hold_bar_counts.items())),
                "hold_bar_class_counts": {
                    f"bar_{hold_bar}_{baseline_class}": count
                    for (hold_bar, baseline_class), count in sorted(class_counts.items())
                },
            }
        analysis["variant_event_timing"][variant_code] = {
            "label": variant_info["label"],
            "splits": split_payload,
        }

    analysis["recommendations"] = {
        "22F": {
            "title": "partial_stop_loss_late_small",
            "why": [
                "partial_stop_loss is the only variant that consistently helps baseline losers more than winners",
                "most partial stop loss events happen on bars 1-2, and bar 1 carries the heaviest winner contamination",
                "the 45-50 point adverse zone already separates losers from winners well enough; the bigger problem is firing too early and cutting too much size",
            ],
            "design": {
                "core_rule": "partial_stop_loss",
                "change_type": "add hold-bar gate and reduce fraction rather than moving the trigger blindly",
                "candidate_logic": {
                    "trigger_points_anchor": 45,
                    "min_hold_bars": 2,
                    "close_fraction": 0.25,
                },
                "success_criteria": [
                    "retain most deep-loser mitigation from 22D",
                    "reduce winner_clip_rate versus 22D",
                    "keep position_count identical to 22A",
                ],
            },
        },
        "22G": {
            "title": "trailing_stop_extreme_runner_only",
            "why": [
                "trailing_stop fires overwhelmingly on baseline winners, especially from bars 2-5",
                "the 60-point trigger is not selective enough inside a hold5 system",
                "profit separation improves materially only in the 80-point zone, where loser hit rates drop much lower",
            ],
            "design": {
                "core_rule": "trailing_stop",
                "change_type": "move from generic point trail to late extreme-runner protection",
                "candidate_logic": {
                    "activate_points_anchor": 80,
                    "min_hold_bars": 4,
                    "distance_points_anchor": 45,
                },
                "success_criteria": [
                    "event_position_share falls well below 22C",
                    "big_winner_clip_rate falls materially below 22C",
                    "net delta versus 22A improves even if trade count stays similar",
                ],
            },
        },
        "22H": {
            "title": "partial_stop_loss_late_small_plus_extreme_runner_trail",
            "why": [
                "22D gives the best containment signal",
                "22C as a broad trail is too destructive, but a very late trail may still help only on rare extended runners",
                "the combination only makes sense if partial stop loss is narrowed first",
            ],
            "design": {
                "core_rule": "composite",
                "change_type": "combine containment-first partial SL with extreme-runner trailing only on late bars",
                "candidate_logic": {
                    "partial_stop_loss": {
                        "trigger_points_anchor": 45,
                        "min_hold_bars": 2,
                        "close_fraction": 0.25,
                    },
                    "trailing_stop": {
                        "activate_points_anchor": 80,
                        "min_hold_bars": 4,
                        "distance_points_anchor": 45,
                    },
                },
                "success_criteria": [
                    "improve worst drawdown versus 22A without repeating 22D-size net profit drag",
                    "keep big winner clipping much lower than 22C and 22E",
                    "treat this as a containment challenger, not an automatic alpha upgrade",
                ],
            },
        },
        "deprioritized": [
            {
                "variant": "break_even",
                "reason": "event timing and class mix show too much winner-side interaction to justify another standalone rerun first",
            },
            {
                "variant": "partial_take_profit",
                "reason": "profit-taking events repeatedly align with winner clipping and offer weak loser relief",
            },
        ],
    }
    return analysis


def render_markdown(analysis: dict[str, Any]) -> str:
    lines: list[str] = []
    lines.append("# Stage 22 Trigger Zone Review")
    lines.append("")
    lines.append(f"Generated at: `{analysis['generated_at_utc']}`")
    lines.append("")
    lines.append(f"- note: `{analysis['threshold_unit_note']}`")
    lines.append("")
    lines.append("## Baseline Trigger Zones")
    lines.append("")
    for split_name in ("hist_2024", "val_2501", "oos_2501"):
        payload = analysis["baseline_trigger_zones"][split_name]
        lines.append(f"### {payload['label']}")
        lines.append("")
        lines.append(
            "- baseline positions: `{}` winners, `{}` losers".format(
                payload["winner_count"], payload["loser_count"]
            )
        )
        lines.append("")
        lines.append("| profit trigger approx points | winner hit rate | loser hit rate | gap |")
        lines.append("|---|---:|---:|---:|")
        for row in payload["profit_thresholds"]:
            lines.append(
                "| {points:.0f} | {winner:.3f} | {loser:.3f} | {gap:.3f} |".format(
                    points=row["threshold_points_approx"],
                    winner=row["winner_hit_rate"] or 0.0,
                    loser=row["loser_hit_rate"] or 0.0,
                    gap=row["separation_gap"] or 0.0,
                )
            )
        lines.append("")
        lines.append("| adverse trigger approx points | winner hit rate | loser hit rate | loser-minus-winner gap |")
        lines.append("|---|---:|---:|---:|")
        for row in payload["loss_thresholds"]:
            lines.append(
                "| {points:.0f} | {winner:.3f} | {loser:.3f} | {gap:.3f} |".format(
                    points=row["threshold_points_approx"],
                    winner=row["winner_hit_rate"] or 0.0,
                    loser=row["loser_hit_rate"] or 0.0,
                    gap=row["separation_gap"] or 0.0,
                )
            )
        lines.append("")

    lines.append("## Event Timing By Variant")
    lines.append("")
    for variant_code in ("22B", "22C", "22D", "22E"):
        variant = analysis["variant_event_timing"][variant_code]
        lines.append(f"### {variant_code} `{variant['label']}`")
        lines.append("")
        for split_name in ("hist_2024", "val_2501", "oos_2501"):
            payload = variant["splits"][split_name]
            lines.append(
                "- {} `{}` hold bars: `{}`".format(
                    payload["label"],
                    payload["event_reason"],
                    payload["hold_bar_counts"],
                )
            )
            lines.append(
                "  baseline class mix: `{}`".format(payload["hold_bar_class_counts"])
            )
        lines.append("")

    lines.append("## Recommended Next Experiments")
    lines.append("")
    for exp_code in ("22F", "22G", "22H"):
        payload = analysis["recommendations"][exp_code]
        lines.append(f"### {exp_code} `{payload['title']}`")
        lines.append("")
        for reason in payload["why"]:
            lines.append(f"- {reason}")
        lines.append("- candidate logic: `{}`".format(payload["design"]["candidate_logic"]))
        for criterion in payload["design"]["success_criteria"]:
            lines.append(f"- success test: {criterion}")
        lines.append("")

    lines.append("## Deprioritized")
    lines.append("")
    for item in analysis["recommendations"]["deprioritized"]:
        lines.append(f"- `{item['variant']}`: {item['reason']}")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    REVIEW_DIR.mkdir(parents=True, exist_ok=True)
    analysis = build_analysis()
    json_path = REVIEW_DIR / "stage22_trigger_zone_review_20260408.json"
    md_path = REVIEW_DIR / "stage22_trigger_zone_review_20260408.md"
    json_path.write_text(json.dumps(analysis, ensure_ascii=False, indent=2), encoding="utf-8")
    md_path.write_text(render_markdown(analysis), encoding="utf-8-sig")
    print(json_path)
    print(md_path)


if __name__ == "__main__":
    main()
