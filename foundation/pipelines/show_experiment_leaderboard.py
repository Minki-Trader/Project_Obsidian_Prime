#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from foundation.pipelines.experiment_bundle_models import ExperimentBundle, RuleDefinition


UTC = timezone.utc
DEFAULT_LEADERBOARD_OUTPUT_PATH = (
    ROOT_DIR / "stages" / "05_optimization" / "03_reviews" / "mt5_validation_leaderboard.md"
)


@dataclass
class AttemptView:
    attempt_id: str
    status: str
    ended_at_utc: str | None
    return_pct: float | None
    trade_count: int | None
    ready_row_count: int | None
    expected_ready_row_count: int | None
    ready_row_gap: int | None


@dataclass
class BundleView:
    bundle_path: Path
    stage_folder: str
    run_bucket: str
    run_name: str
    experiment_id: str
    bundle_status: str
    split_name: str
    latest_attempt_id: str | None
    latest_attempt_status: str | None
    latest_attempt_ended_at_utc: str | None
    headline: dict[str, Any]
    risk: dict[str, Any]
    diagnostics: dict[str, Any]
    execution: dict[str, Any]
    rule_summary: str
    attempt_views: list[AttemptView]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Show a terminal leaderboard from experiment_bundle.json files.")
    parser.add_argument(
        "--root",
        default="stages",
        help="Directory to scan for experiment_bundle.json files. Defaults to stages.",
    )
    parser.add_argument(
        "--split",
        default="validation",
        help="Split name to read from results.by_split. Defaults to validation.",
    )
    parser.add_argument(
        "--sort-by",
        default="return_pct",
        choices=[
            "return_pct",
            "profit_factor",
            "recovery_factor",
            "trade_count",
            "win_rate",
            "expectancy_per_trade",
            "max_dd_pct",
            "ready_rate",
            "ulcer_index",
        ],
        help="Metric used to rank bundles.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        help="Optional maximum number of bundles to print after sorting.",
    )
    parser.add_argument(
        "--summary-only",
        action="store_true",
        help="Print only the leaderboard table without per-run detail sections.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit machine-readable JSON instead of formatted text.",
    )
    parser.add_argument(
        "--write-markdown",
        nargs="?",
        const=str(DEFAULT_LEADERBOARD_OUTPUT_PATH),
        help="Write the leaderboard markdown to the given path. Defaults to the Stage 05 review file.",
    )
    return parser


def parse_utc_text(value: str | None) -> datetime | None:
    if not value:
        return None
    normalized = value.strip().replace("Z", "+00:00")
    parsed = datetime.fromisoformat(normalized)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=UTC)
    return parsed.astimezone(UTC)


def fmt_float(value: float | None, digits: int = 3) -> str:
    if value is None:
        return "-"
    return f"{value:.{digits}f}"


def fmt_pct(value: float | None, digits: int = 2) -> str:
    if value is None:
        return "-"
    return f"{value:.{digits}f}"


def fmt_int(value: int | None) -> str:
    if value is None:
        return "-"
    return str(value)


def fmt_timestamp(value: str | None) -> str:
    parsed = parse_utc_text(value)
    if parsed is None:
        return "-"
    return parsed.strftime("%Y-%m-%d %H:%M:%S UTC")


def safe_sort_value(value: float | int | None, *, reverse_metric: bool) -> tuple[int, float]:
    if value is None:
        return (1, 0.0)
    numeric = float(value)
    if reverse_metric:
        numeric *= -1.0
    return (0, numeric)


def render_table(headers: list[str], rows: list[list[str]]) -> str:
    widths = [len(header) for header in headers]
    for row in rows:
        for index, cell in enumerate(row):
            widths[index] = max(widths[index], len(cell))

    def render_row(row: list[str]) -> str:
        return " | ".join(cell.ljust(widths[index]) for index, cell in enumerate(row))

    sep = "-+-".join("-" * width for width in widths)
    lines = [render_row(headers), sep]
    lines.extend(render_row(row) for row in rows)
    return "\n".join(lines)


def iter_bundle_paths(root: Path) -> list[Path]:
    return sorted(root.rglob("experiment_bundle.json"))


def summarize_rule(rule: RuleDefinition) -> str:
    if not rule.enabled:
        return ""
    if not rule.params:
        return rule.type
    params = ", ".join(f"{key}={value}" for key, value in rule.params.items())
    return f"{rule.type}({params})"


def build_rule_summary(bundle: ExperimentBundle) -> str:
    parts: list[str] = []
    for category in ("entry", "filters", "position", "exit"):
        rules = getattr(bundle.rule_stack, category)
        rendered = [summarize_rule(rule) for rule in rules]
        rendered = [item for item in rendered if item]
        if rendered:
            parts.append(f"{category}: " + " -> ".join(rendered))
    return " | ".join(parts) if parts else "-"


def derive_stage_context(bundle_path: Path) -> tuple[str, str, str]:
    parts = bundle_path.parts
    if "stages" in parts:
        idx = parts.index("stages")
        if len(parts) > idx + 4:
            return parts[idx + 1], parts[idx + 3], parts[idx + 4]
    return ("unknown_stage", "unknown_bucket", bundle_path.parent.name)


def build_attempt_views(bundle: ExperimentBundle) -> list[AttemptView]:
    attempts: list[AttemptView] = []
    for attempt in bundle.run_attempts:
        summary = dict(attempt.summary_metrics)
        attempts.append(
            AttemptView(
                attempt_id=attempt.attempt_id,
                status=attempt.status,
                ended_at_utc=attempt.ended_at_utc,
                return_pct=summary.get("return_pct"),
                trade_count=summary.get("trade_count"),
                ready_row_count=summary.get("ready_row_count"),
                expected_ready_row_count=summary.get("expected_ready_row_count"),
                ready_row_gap=summary.get("ready_row_gap"),
            )
        )
    attempts.sort(key=lambda item: parse_utc_text(item.ended_at_utc) or datetime.min.replace(tzinfo=UTC), reverse=True)
    return attempts


def build_bundle_view(bundle_path: Path, bundle: ExperimentBundle, split_name: str) -> BundleView | None:
    split = bundle.results.by_split.get(split_name)
    if split is None:
        return None

    stage_folder, run_bucket, run_name = derive_stage_context(bundle_path)
    attempt_views = build_attempt_views(bundle)
    latest_attempt = attempt_views[0] if attempt_views else None

    return BundleView(
        bundle_path=bundle_path,
        stage_folder=stage_folder,
        run_bucket=run_bucket,
        run_name=run_name,
        experiment_id=bundle.identity.experiment_id,
        bundle_status=bundle.identity.bundle_status,
        split_name=split_name,
        latest_attempt_id=latest_attempt.attempt_id if latest_attempt else None,
        latest_attempt_status=latest_attempt.status if latest_attempt else None,
        latest_attempt_ended_at_utc=latest_attempt.ended_at_utc if latest_attempt else None,
        headline=split.headline.model_dump(mode="json", exclude_none=False),
        risk=split.risk.model_dump(mode="json", exclude_none=False),
        diagnostics=split.diagnostics.model_dump(mode="json", exclude_none=False),
        execution=split.execution.model_dump(mode="json", exclude_none=False),
        rule_summary=build_rule_summary(bundle),
        attempt_views=attempt_views,
    )


def load_bundle_views(root: Path, split_name: str) -> list[BundleView]:
    bundle_views: list[BundleView] = []
    for bundle_path in iter_bundle_paths(root):
        bundle = ExperimentBundle.from_json(bundle_path.read_text(encoding="utf-8-sig"))
        view = build_bundle_view(bundle_path, bundle, split_name)
        if view is not None:
            bundle_views.append(view)
    return bundle_views


def sort_bundle_views(bundle_views: list[BundleView], sort_by: str) -> list[BundleView]:
    descending = sort_by != "max_dd_pct"

    def metric_value(view: BundleView) -> float | int | None:
        if sort_by == "ulcer_index":
            return view.risk.get("ulcer_index")
        if sort_by == "ready_rate":
            extra = view.execution.get("extra") or {}
            ready = extra.get("ready_row_count")
            rows = extra.get("row_count")
            if ready is None or rows in (None, 0):
                return None
            return float(ready) / float(rows)
        return view.headline.get(sort_by)

    return sorted(
        bundle_views,
        key=lambda view: (
            safe_sort_value(metric_value(view), reverse_metric=descending),
            view.stage_folder,
            view.run_name,
        ),
    )


def bundle_view_to_dict(view: BundleView) -> dict[str, Any]:
    return {
        "bundle_path": str(view.bundle_path),
        "stage_folder": view.stage_folder,
        "run_bucket": view.run_bucket,
        "run_name": view.run_name,
        "experiment_id": view.experiment_id,
        "bundle_status": view.bundle_status,
        "split_name": view.split_name,
        "latest_attempt_id": view.latest_attempt_id,
        "latest_attempt_status": view.latest_attempt_status,
        "latest_attempt_ended_at_utc": view.latest_attempt_ended_at_utc,
        "rule_summary": view.rule_summary,
        "headline": view.headline,
        "risk": view.risk,
        "diagnostics": view.diagnostics,
        "execution": view.execution,
        "attempts": [
            {
                "attempt_id": attempt.attempt_id,
                "status": attempt.status,
                "ended_at_utc": attempt.ended_at_utc,
                "return_pct": attempt.return_pct,
                "trade_count": attempt.trade_count,
                "ready_row_count": attempt.ready_row_count,
                "expected_ready_row_count": attempt.expected_ready_row_count,
                "ready_row_gap": attempt.ready_row_gap,
            }
            for attempt in view.attempt_views
        ],
    }


def render_summary_table(bundle_views: list[BundleView]) -> str:
    rows: list[list[str]] = []
    for rank, view in enumerate(bundle_views, start=1):
        extra = view.execution.get("extra") or {}
        ready = extra.get("ready_row_count")
        rows_total = extra.get("row_count")
        ready_rate = None
        if ready is not None and rows_total not in (None, 0):
            ready_rate = float(ready) / float(rows_total) * 100.0
        rows.append(
            [
                str(rank),
                view.stage_folder,
                view.run_name,
                view.latest_attempt_id or "-",
                view.latest_attempt_status or "-",
                fmt_pct(view.headline.get("return_pct")),
                fmt_float(view.headline.get("profit_factor")),
                fmt_pct(view.headline.get("max_dd_pct")),
                fmt_int(view.headline.get("trade_count")),
                fmt_pct(ready_rate),
                fmt_int(extra.get("ready_row_gap")),
                fmt_int(extra.get("unexpected_skip_count")),
            ]
        )
    headers = [
        "Rank",
        "Stage",
        "Run",
        "LatestAttempt",
        "AttemptStatus",
        "Return%",
        "PF",
        "MaxDD%",
        "Trades",
        "Ready%",
        "ReadyGap",
        "UnexpectedSkips",
    ]
    return render_table(headers, rows)


def render_attempt_table(attempts: list[AttemptView]) -> str:
    rows = [
        [
            attempt.attempt_id,
            attempt.status,
            fmt_timestamp(attempt.ended_at_utc),
            fmt_pct(attempt.return_pct),
            fmt_int(attempt.trade_count),
            fmt_int(attempt.ready_row_count),
            fmt_int(attempt.expected_ready_row_count),
            fmt_int(attempt.ready_row_gap),
        ]
        for attempt in attempts
    ]
    return render_table(
        ["Attempt", "Status", "EndedUTC", "Return%", "Trades", "Ready", "ExpectedReady", "ReadyGap"],
        rows,
    )


def render_metric_markdown_table(metrics: dict[str, Any], preferred_keys: list[str]) -> str:
    lines = ["| Metric | Value |", "|---|---|"]
    rendered_keys: set[str] = set()
    for key in preferred_keys:
        if key in metrics:
            lines.append(f"| `{key}` | `{metrics.get(key)}` |")
            rendered_keys.add(key)

    for key in sorted(metrics.keys()):
        if key in rendered_keys:
            continue
        if key == "extra":
            continue
        value = metrics[key]
        if value in ({}, [], None):
            continue
        lines.append(f"| `{key}` | `{value}` |")
    return "\n".join(lines)


def build_markdown_report(bundle_views: list[BundleView], *, root: Path, split: str, sort_by: str) -> str:
    lines: list[str] = [
        "# MT5 Validation Leaderboard",
        "",
        f"- generated_at_utc: `{datetime.now(tz=UTC).isoformat()}`",
        f"- scan_root: `{root}`",
        f"- split: `{split}`",
        f"- sort_by: `{sort_by}`",
        f"- bundle_count: `{len(bundle_views)}`",
        "",
        "## Summary",
        "",
        "```text",
        render_summary_table(bundle_views) if bundle_views else "(no bundles found)",
        "```",
    ]

    if not bundle_views:
        return "\n".join(lines) + "\n"

    lines.extend(["", "## Runs"])
    for rank, view in enumerate(bundle_views, start=1):
        extra = view.execution.get("extra") or {}
        lines.extend(
            [
                "",
                f"### {rank}. `{view.stage_folder}` / `{view.run_name}`",
                "",
                f"- run_bucket: `{view.run_bucket}`",
                f"- bundle_path: `{view.bundle_path}`",
                f"- experiment_id: `{view.experiment_id}`",
                f"- bundle_status: `{view.bundle_status}`",
                f"- latest_attempt: `{view.latest_attempt_id or '-'}`",
                f"- latest_attempt_status: `{view.latest_attempt_status or '-'}`",
                f"- latest_attempt_ended_at_utc: `{view.latest_attempt_ended_at_utc or '-'}`",
                f"- rule_summary: `{view.rule_summary}`",
                f"- ready_rows: `{extra.get('ready_row_count', '-')}` / `{extra.get('row_count', '-')}`",
                f"- expected_ready_rows: `{extra.get('expected_ready_row_count', '-')}`",
                f"- ready_row_gap: `{extra.get('ready_row_gap', '-')}`",
                f"- contract_skip_count: `{extra.get('contract_skip_count', '-')}`",
                f"- startup_skip_count: `{extra.get('startup_skip_count', '-')}`",
                f"- unexpected_skip_count: `{extra.get('unexpected_skip_count', '-')}`",
                "",
                "#### Headline",
                "",
                render_metric_markdown_table(
                    view.headline,
                    [
                        "return_pct",
                        "profit_factor",
                        "trade_count",
                        "win_rate",
                        "expectancy_per_trade",
                        "max_dd_pct",
                        "recovery_factor",
                        "net_profit",
                    ],
                ),
                "",
                "#### Risk",
                "",
                render_metric_markdown_table(
                    view.risk,
                    [
                        "equity_dd_pct",
                        "equity_dd_amount",
                        "max_dd_pct",
                        "max_dd_amount",
                        "ulcer_index",
                        "worst_day",
                        "worst_week",
                        "min_free_margin",
                        "consecutive_losses",
                        "time_under_water",
                        "longest_recovery_duration",
                    ],
                ),
                "",
                "#### Diagnostics",
                "",
                render_metric_markdown_table(
                    view.diagnostics,
                    [
                        "avg_hold",
                        "payoff_ratio",
                        "avg_win",
                        "avg_loss",
                        "long_count",
                        "short_count",
                        "long_expectancy",
                        "short_expectancy",
                        "mfe_mean",
                        "mfe_median",
                        "mfe_p90",
                        "mae_mean",
                        "mae_median",
                        "mae_p90",
                        "no_trade_rate",
                    ],
                ),
                "",
                "#### Execution",
                "",
                render_metric_markdown_table(
                    view.execution,
                    [
                        "skip_rate",
                        "external_mismatch_count",
                        "fill_rate",
                        "avg_spread",
                        "avg_slippage",
                        "reject_count",
                        "data_readiness_failures",
                        "broker_constraint_events",
                    ],
                ),
                "",
                "#### Attempts",
                "",
                "```text",
                render_attempt_table(view.attempt_views) if view.attempt_views else "(none)",
                "```",
            ]
        )
    return "\n".join(lines) + "\n"


def write_markdown_report(
    *,
    root: Path | None = None,
    split: str = "validation",
    sort_by: str = "return_pct",
    limit: int | None = None,
    output_path: Path | None = None,
) -> Path:
    resolved_root = (root or (ROOT_DIR / "stages")).resolve()
    resolved_output = (output_path or DEFAULT_LEADERBOARD_OUTPUT_PATH).resolve()
    bundle_views = load_bundle_views(resolved_root, split)
    bundle_views = sort_bundle_views(bundle_views, sort_by)
    if limit is not None:
        bundle_views = bundle_views[:limit]
    markdown = build_markdown_report(bundle_views, root=resolved_root, split=split, sort_by=sort_by)
    resolved_output.parent.mkdir(parents=True, exist_ok=True)
    resolved_output.write_text(markdown, encoding="utf-8-sig")
    return resolved_output


def render_detail_sections(bundle_views: list[BundleView]) -> str:
    sections: list[str] = []
    for rank, view in enumerate(bundle_views, start=1):
        extra = view.execution.get("extra") or {}
        headline = view.headline
        risk = view.risk
        diagnostics = view.diagnostics
        execution = view.execution
        section_lines = [
            f"[{rank}] {view.stage_folder} / {view.run_name} ({view.run_bucket})",
            f"bundle: {view.bundle_path}",
            f"experiment_id: {view.experiment_id}",
            f"latest_attempt: {view.latest_attempt_id or '-'} ({view.latest_attempt_status or '-'}) ended {fmt_timestamp(view.latest_attempt_ended_at_utc)}",
            f"rules: {view.rule_summary}",
            (
                "headline: "
                f"return_pct={fmt_pct(headline.get('return_pct'))}, "
                f"profit_factor={fmt_float(headline.get('profit_factor'))}, "
                f"trades={fmt_int(headline.get('trade_count'))}, "
                f"win_rate={fmt_pct((headline.get('win_rate') or 0.0) * 100.0) if headline.get('win_rate') is not None else '-'}, "
                f"max_dd_pct={fmt_pct(headline.get('max_dd_pct'))}, "
                f"recovery_factor={fmt_float(headline.get('recovery_factor'))}"
            ),
            (
                "risk: "
                f"equity_dd_amount={fmt_float(risk.get('equity_dd_amount'), 2)}, "
                f"ulcer_index={fmt_float(risk.get('ulcer_index'))}, "
                f"worst_day={fmt_float(risk.get('worst_day'), 2)}, "
                f"worst_week={fmt_float(risk.get('worst_week'), 2)}, "
                f"min_free_margin={fmt_float(risk.get('min_free_margin'), 2)}, "
                f"consecutive_losses={fmt_int(risk.get('consecutive_losses'))}"
            ),
            (
                "diagnostics: "
                f"avg_hold={fmt_float(diagnostics.get('avg_hold'), 2)}, "
                f"payoff_ratio={fmt_float(diagnostics.get('payoff_ratio'))}, "
                f"no_trade_rate={fmt_pct((diagnostics.get('no_trade_rate') or 0.0) * 100.0) if diagnostics.get('no_trade_rate') is not None else '-'}, "
                f"long_count={fmt_int(diagnostics.get('long_count'))}, "
                f"short_count={fmt_int(diagnostics.get('short_count'))}, "
                f"long_expectancy={fmt_float(diagnostics.get('long_expectancy'))}, "
                f"short_expectancy={fmt_float(diagnostics.get('short_expectancy'))}"
            ),
            (
                "execution: "
                f"ready={fmt_int(extra.get('ready_row_count'))}/{fmt_int(extra.get('row_count'))}, "
                f"contract_skips={fmt_int(extra.get('contract_skip_count'))}, "
                f"startup_skips={fmt_int(extra.get('startup_skip_count'))}, "
                f"unexpected_skips={fmt_int(extra.get('unexpected_skip_count'))}, "
                f"external_mismatch_count={fmt_int(execution.get('external_mismatch_count'))}, "
                f"fill_rate={fmt_float(execution.get('fill_rate'))}"
            ),
            "attempts:",
            render_attempt_table(view.attempt_views) if view.attempt_views else "  (none)",
        ]
        sections.append("\n".join(section_lines))
    return "\n\n".join(sections)


def main() -> int:
    args = build_parser().parse_args()
    root = (ROOT_DIR / args.root).resolve()
    if not root.exists():
        raise FileNotFoundError(f"scan root does not exist: {root}")

    bundle_views = load_bundle_views(root, args.split)
    bundle_views = sort_bundle_views(bundle_views, args.sort_by)
    if args.limit is not None:
        bundle_views = bundle_views[: args.limit]

    if args.json:
        payload = {
            "scan_root": str(root),
            "split": args.split,
            "sort_by": args.sort_by,
            "bundle_count": len(bundle_views),
            "items": [bundle_view_to_dict(view) for view in bundle_views],
        }
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return 0

    if args.write_markdown:
        output_path = write_markdown_report(
            root=root,
            split=args.split,
            sort_by=args.sort_by,
            limit=args.limit,
            output_path=Path(args.write_markdown),
        )
        print(f"[done] markdown={output_path}")
        return 0

    print(f"Experiment Leaderboard | root={root} | split={args.split} | sort_by={args.sort_by}")
    if not bundle_views:
        print("(no bundles found)")
        return 0

    print()
    print(render_summary_table(bundle_views))
    if args.summary_only:
        return 0

    print()
    print(render_detail_sections(bundle_views))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
