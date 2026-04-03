#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import subprocess
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from foundation.pipelines.compile_mt5_bundle_runtime import DEFAULT_COMMON_PROJECT_ROOT
from foundation.pipelines.experiment_bundle_models import (
    ArtifactRef,
    ExecutionMetrics,
    ExperimentBundle,
    ReportReference,
    RunAttempt,
    SplitResults,
    StatusEvent,
)
from foundation.pipelines.show_experiment_leaderboard import write_markdown_report


UTC = timezone.utc
DEFAULT_TERMINAL_PATH = Path(r"C:\Program Files\MetaTrader 5\terminal64.exe")
CONTRACT_SKIP_PREFIXES = ("SESSION_", "EXTERNAL_TIMESTAMP_MISMATCH_")
STARTUP_SKIP_MARKERS = ("NOT_READY", "WARMUP", "MODEL_NOT_READY")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run an MT5 Strategy Tester attempt from experiment_bundle.json.")
    parser.add_argument("--bundle-json", required=True, help="Path to experiment_bundle.json")
    parser.add_argument(
        "--from-date",
        help="Tester start date YYYY.MM.DD. Defaults to the bundle split start when omitted.",
    )
    parser.add_argument(
        "--to-date",
        help="Tester end date YYYY.MM.DD. Defaults to the bundle split end-exclusive date when omitted.",
    )
    parser.add_argument("--split-name", default="validation", help="Logical split name for results.by_split")
    parser.add_argument("--runtime-id", help="Optional MT5 runtime package id. Defaults to experiment_id")
    parser.add_argument("--feature-mode", type=int, default=1, help="EA feature mode (default: 1 = PRICE_CORE_PARTIAL)")
    parser.add_argument("--enable-trading", action="store_true", help="Enable market orders in the EA")
    parser.add_argument("--warmup-bars", type=int, default=300, help="InpWarmupBars override")
    parser.add_argument("--magic-number", type=int, default=26032901, help="EA magic number")
    parser.add_argument("--trade-deviation-points", type=int, default=100, help="EA trade deviation in points")
    parser.add_argument(
        "--terminal-path",
        default=str(DEFAULT_TERMINAL_PATH),
        help="Path to MetaTrader terminal64.exe",
    )
    parser.add_argument(
        "--common-project-root",
        default=str(DEFAULT_COMMON_PROJECT_ROOT),
        help="Common Files Project_Obsidian_Prime root",
    )
    parser.add_argument(
        "--tester-report-format",
        default="xml",
        choices=["xml", "html"],
        help="Desired tester report extension",
    )
    parser.add_argument(
        "--skip-leaderboard-refresh",
        action="store_true",
        help="Skip the shared markdown leaderboard refresh after the attempt.",
    )
    return parser


def utc_now_iso() -> str:
    return datetime.now(tz=UTC).isoformat()


def compute_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def next_attempt_id(bundle: ExperimentBundle) -> str:
    return f"att_{len(bundle.run_attempts) + 1:04d}"


def parse_utc_iso(value: str) -> datetime:
    normalized = value.strip().replace("Z", "+00:00")
    parsed = datetime.fromisoformat(normalized)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=UTC)
    return parsed.astimezone(UTC)


def derive_split_dates(bundle: ExperimentBundle, split_name: str) -> tuple[str, str]:
    boundaries = bundle.data_snapshot.split_boundaries
    normalized = split_name.strip().lower()
    if normalized == "train":
        start_utc = parse_utc_iso(boundaries.train_start_utc)
        end_utc = parse_utc_iso(boundaries.train_end_utc_exclusive)
    elif normalized in {"validation", "valid"}:
        start_utc = parse_utc_iso(boundaries.train_end_utc_exclusive)
        end_utc = parse_utc_iso(boundaries.validation_end_utc_exclusive)
    elif normalized == "test":
        start_utc = parse_utc_iso(boundaries.validation_end_utc_exclusive)
        end_utc = parse_utc_iso(boundaries.test_end_utc_exclusive)
    else:
        raise ValueError(
            f"cannot derive tester dates for split_name={split_name!r}; provide --from-date and --to-date explicitly"
        )

    # MT5 tester date windows behave like an exclusive upper boundary in practice,
    # so we pass the bundle's end-exclusive UTC date through unchanged.
    return start_utc.strftime("%Y.%m.%d"), end_utc.strftime("%Y.%m.%d")


def resolve_tester_dates(bundle: ExperimentBundle, args: argparse.Namespace) -> tuple[str, str, bool]:
    if args.from_date and args.to_date:
        return args.from_date, args.to_date, False
    if args.from_date or args.to_date:
        raise ValueError("provide both --from-date and --to-date, or omit both to derive dates from the bundle split")
    from_date, to_date = derive_split_dates(bundle, args.split_name)
    return from_date, to_date, True


def classify_skip_reasons(skip_reasons: Counter[str]) -> dict[str, object]:
    contract_skip_breakdown: Counter[str] = Counter()
    startup_skip_breakdown: Counter[str] = Counter()
    unexpected_skip_breakdown: Counter[str] = Counter()

    for reason, count in skip_reasons.items():
        if any(reason.startswith(prefix) for prefix in CONTRACT_SKIP_PREFIXES):
            contract_skip_breakdown[reason] = count
        elif any(marker in reason for marker in STARTUP_SKIP_MARKERS):
            startup_skip_breakdown[reason] = count
        else:
            unexpected_skip_breakdown[reason] = count

    return {
        "contract_skip_breakdown": dict(contract_skip_breakdown),
        "contract_skip_count": sum(contract_skip_breakdown.values()),
        "startup_skip_breakdown": dict(startup_skip_breakdown),
        "startup_skip_count": sum(startup_skip_breakdown.values()),
        "unexpected_skip_breakdown": dict(unexpected_skip_breakdown),
        "unexpected_skip_count": sum(unexpected_skip_breakdown.values()),
    }


def expected_ready_row_count(bundle: ExperimentBundle, split_name: str) -> int | None:
    split_key_map = {
        "train": "train",
        "validation": "valid",
        "valid": "valid",
        "test": "test",
    }
    split_key = split_key_map.get(split_name.strip().lower())
    if split_key is None:
        return None
    return bundle.data_snapshot.split_counts.get(split_key)


def upsert_artifact(bundle: ExperimentBundle, artifact: ArtifactRef) -> None:
    for index, existing in enumerate(bundle.artifacts):
        if existing.artifact_id == artifact.artifact_id:
            bundle.artifacts[index] = artifact
            return
    bundle.artifacts.append(artifact)


def append_status(bundle: ExperimentBundle, status: str, reason: str) -> None:
    bundle.identity.bundle_status = status
    bundle.status_history.append(StatusEvent(status=status, changed_at_utc=utc_now_iso(), reason=reason))


def ensure_split_results(bundle: ExperimentBundle, split_name: str) -> SplitResults:
    if split_name not in bundle.results.by_split:
        bundle.results.by_split[split_name] = SplitResults()
    return bundle.results.by_split[split_name]


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def refresh_leaderboard_markdown() -> Path:
    return write_markdown_report(root=ROOT_DIR / "stages", split="validation", sort_by="return_pct")


def build_tester_ini_text(
    bundle: ExperimentBundle,
    *,
    runtime_id: str,
    from_date: str,
    to_date: str,
    feature_mode: int,
    enable_trading: bool,
    warmup_bars: int,
    magic_number: int,
    trade_deviation_points: int,
    report_path: Path,
    csv_log_relative_path: str,
    trade_ledger_relative_path: str,
) -> str:
    runtime_config_relative = f"Project_Obsidian_Prime\\runtime\\{runtime_id}\\mt5_runtime_config.txt"
    tester_model_value = 4 if bundle.runtime_snapshot.tester_model == "real_ticks" else 1
    lines = [
        "[Tester]",
        r"Expert=Project_Obsidian_Prime\foundation\mt5\ObsidianPrime_Stage1_ShadowEA.ex5",
        f"Symbol={bundle.runtime_snapshot.symbol}",
        f"Period={bundle.runtime_snapshot.timeframe}",
        "Optimization=0",
        f"Model={tester_model_value}",
        "Dates=1",
        f"FromDate={from_date}",
        f"ToDate={to_date}",
        "ForwardMode=0",
        f"Deposit={int(bundle.runtime_snapshot.deposit) if bundle.runtime_snapshot.deposit.is_integer() else bundle.runtime_snapshot.deposit}",
        f"Currency={bundle.runtime_snapshot.currency or 'USD'}",
        "ProfitInPips=0",
        f"Leverage={bundle.runtime_snapshot.leverage}",
        "ExecutionMode=0",
        "OptimizationCriterion=0",
        "Visual=0",
        f"Report={report_path}",
        "ReplaceReport=1",
        "ShutdownTerminal=1",
        "",
        "[TesterInputs]",
        r"InpOnnxModelPath=Project_Obsidian_Prime\obsidian_prime_stage01d_probonly.onnx",
        "InpOnnxUseCommonFiles=false",
        "InpUseRuntimeConfig=true",
        f"InpRuntimeConfigPath={runtime_config_relative}",
        "InpRuntimeConfigUseCommonFiles=true",
        "InpUseCpuOnly=true",
        "InpDumpModelIo=false",
        "InpRunSmokeOnInit=true",
        f"InpFeatureMode={feature_mode}",
        f"InpWarmupBars={warmup_bars}",
        "InpShortThreshold=0.333333",
        "InpLongThreshold=0.333333",
        "InpMinMargin=0.0",
        f"InpFixedLot={bundle.runtime_snapshot.fixed_lot}",
        f"InpEnableTrading={'true' if enable_trading else 'false'}",
        f"InpMagicNumber={magic_number}",
        f"InpTradeDeviationPoints={trade_deviation_points}",
        "InpAllowPartialInference=false",
        "InpWriteCsvLog=true",
        "InpLogUseCommonFiles=true",
        f"InpCsvLogPath={csv_log_relative_path}",
        f"InpWriteTradeLedger={'true' if enable_trading else 'false'}",
        "InpTradeLedgerUseCommonFiles=true",
        f"InpTradeLedgerPath={trade_ledger_relative_path}",
        "InpVerboseLog=true",
        "",
    ]
    return "\n".join(lines)


def run_compile_runtime(bundle_path: Path, runtime_id: str, common_project_root: Path) -> None:
    cmd = [
        sys.executable,
        str(ROOT_DIR / "foundation" / "pipelines" / "compile_mt5_bundle_runtime.py"),
        "--bundle-json",
        str(bundle_path),
        "--runtime-id",
        runtime_id,
        "--common-project-root",
        str(common_project_root),
    ]
    subprocess.run(cmd, cwd=ROOT_DIR, check=True)


def parse_shadow_csv(csv_path: Path) -> dict[str, object]:
    if not csv_path.exists():
        raise FileNotFoundError(f"missing tester CSV log: {csv_path}")

    with csv_path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)

    if not rows:
        raise ValueError(f"tester CSV log is empty: {csv_path}")

    total_rows = len(rows)
    ready_rows = [row for row in rows if row.get("row_ready", "").lower() == "true"]
    skipped_rows = [row for row in rows if row.get("row_ready", "").lower() != "true"]
    decisions = Counter(row.get("decision", "") for row in ready_rows)
    skip_reasons = Counter(row.get("skip_reason", "") for row in skipped_rows if row.get("skip_reason", ""))

    external_mismatch_count = sum(
        count for reason, count in skip_reasons.items() if reason.startswith("EXTERNAL_TIMESTAMP_MISMATCH")
    )
    data_readiness_failures = sum(
        count
        for reason, count in skip_reasons.items()
        if "NOT_READY" in reason or "WARMUP" in reason or "MODEL_NOT_READY" in reason
    )
    feature_ready_max = max(int(row.get("feature_ready_count", "0") or 0) for row in rows)
    ready_rate = (len(ready_rows) / total_rows) if total_rows else 0.0
    no_trade_rate = (decisions.get("NO_TRADE", 0) / len(ready_rows)) if ready_rows else 1.0
    classified = classify_skip_reasons(skip_reasons)

    return {
        "row_count": total_rows,
        "ready_row_count": len(ready_rows),
        "skip_row_count": len(skipped_rows),
        "ready_rate": ready_rate,
        "long_signal_count": decisions.get("LONG", 0),
        "short_signal_count": decisions.get("SHORT", 0),
        "no_trade_count": decisions.get("NO_TRADE", 0),
        "no_trade_rate": no_trade_rate,
        "skip_reason_breakdown": dict(skip_reasons),
        "external_mismatch_count": external_mismatch_count,
        "data_readiness_failures": data_readiness_failures,
        "feature_ready_max": feature_ready_max,
        "latest_bar_time_server": rows[-1].get("bar_time_server"),
        **classified,
        "rows": rows,
    }


def parse_float(value: object) -> float | None:
    if value is None:
        return None
    text = str(value).strip()
    if not text:
        return None
    try:
        return float(text)
    except ValueError:
        return None


def parse_int(value: object) -> int | None:
    parsed = parse_float(value)
    if parsed is None:
        return None
    return int(round(parsed))


def parse_mt5_time(value: object) -> datetime | None:
    if value is None:
        return None
    text = str(value).strip()
    if not text:
        return None
    try:
        return datetime.strptime(text, "%Y.%m.%d %H:%M:%S")
    except ValueError:
        return None


def percentile(values: list[float], quantile: float) -> float | None:
    if not values:
        return None
    if len(values) == 1:
        return float(values[0])
    ordered = sorted(values)
    position = (len(ordered) - 1) * quantile
    lower = int(math.floor(position))
    upper = int(math.ceil(position))
    if lower == upper:
        return float(ordered[lower])
    weight = position - lower
    return float(ordered[lower] * (1.0 - weight) + ordered[upper] * weight)


def compute_drawdown_metrics(points: list[tuple[datetime, float]]) -> dict[str, float | None]:
    if not points:
        return {
            "max_dd_amount": None,
            "max_dd_pct": None,
            "time_under_water": None,
            "longest_recovery_duration": None,
            "ulcer_index": None,
        }

    peak = points[0][1]
    max_dd_amount = 0.0
    max_dd_pct = 0.0
    drawdown_pcts: list[float] = []
    underwater_start: datetime | None = None
    time_under_water = 0.0
    longest_recovery = 0.0
    previous_time = points[0][0]
    previous_underwater = False

    for current_time, value in points:
        if previous_underwater:
            time_under_water += max(0.0, (current_time - previous_time).total_seconds())

        if value >= peak:
            peak = value
            if underwater_start is not None:
                longest_recovery = max(longest_recovery, (current_time - underwater_start).total_seconds())
                underwater_start = None
            drawdown_pct = 0.0
        else:
            dd_amount = peak - value
            drawdown_pct = (dd_amount / peak * 100.0) if peak > 0.0 else 0.0
            max_dd_amount = max(max_dd_amount, dd_amount)
            max_dd_pct = max(max_dd_pct, dd_amount / peak * 100.0 if peak > 0.0 else 0.0)
            if underwater_start is None:
                underwater_start = current_time

        drawdown_pcts.append(drawdown_pct)
        previous_time = current_time
        previous_underwater = drawdown_pct > 0.0

    if underwater_start is not None:
        longest_recovery = max(longest_recovery, (points[-1][0] - underwater_start).total_seconds())

    ulcer_index = math.sqrt(sum(value * value for value in drawdown_pcts) / len(drawdown_pcts)) if drawdown_pcts else None
    return {
        "max_dd_amount": float(max_dd_amount),
        "max_dd_pct": float(max_dd_pct),
        "time_under_water": float(time_under_water),
        "longest_recovery_duration": float(longest_recovery),
        "ulcer_index": float(ulcer_index) if ulcer_index is not None else None,
    }


def parse_trade_ledger(csv_path: Path) -> list[dict[str, object]]:
    if not csv_path.exists():
        return []

    with csv_path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        trades: list[dict[str, object]] = []
        for row in reader:
            net_profit = parse_float(row.get("net_profit")) or 0.0
            max_floating_profit = parse_float(row.get("max_floating_profit")) or 0.0
            min_floating_profit = parse_float(row.get("min_floating_profit")) or 0.0
            trades.append(
                {
                    "direction": (row.get("direction") or "").strip().upper(),
                    "entry_time": parse_mt5_time(row.get("entry_time_server")),
                    "exit_time": parse_mt5_time(row.get("exit_time_server")),
                    "entry_bar_time": parse_mt5_time(row.get("entry_bar_time_server")),
                    "exit_bar_time": parse_mt5_time(row.get("exit_bar_time_server")),
                    "entry_price": parse_float(row.get("entry_price")),
                    "exit_price": parse_float(row.get("exit_price")),
                    "hold_bars": parse_int(row.get("hold_bars")) or 0,
                    "close_reason": row.get("close_reason") or "",
                    "decision_at_entry": row.get("decision_at_entry") or "",
                    "gross_profit": parse_float(row.get("gross_profit")) or 0.0,
                    "swap": parse_float(row.get("swap")) or 0.0,
                    "commission": parse_float(row.get("commission")) or 0.0,
                    "fee": parse_float(row.get("fee")) or 0.0,
                    "net_profit": net_profit,
                    "max_floating_profit": max_floating_profit,
                    "min_floating_profit": min_floating_profit,
                    "mfe_mag": max(0.0, max_floating_profit),
                    "mae_mag": max(0.0, -min_floating_profit),
                }
            )
    return trades


def summarize_financial_metrics(
    *,
    bundle: ExperimentBundle,
    shadow_rows: list[dict[str, str]],
    trades: list[dict[str, object]],
    parsed_shadow: dict[str, object],
) -> dict[str, object]:
    balance_points: list[tuple[datetime, float]] = []
    equity_points: list[tuple[datetime, float]] = []
    free_margin_values: list[float] = []
    spread_values: list[float] = []
    reject_count = 0
    broker_constraint_events = 0
    fill_distance_points: list[float] = []
    decision_reason_counts: Counter[str] = Counter()

    for row in shadow_rows:
        bar_time = parse_mt5_time(row.get("bar_time_server"))
        if bar_time is None:
            continue

        balance = parse_float(row.get("balance"))
        equity = parse_float(row.get("equity"))
        free_margin = parse_float(row.get("free_margin"))
        spread_points = parse_float(row.get("spread_points"))
        trade_action_reason = (row.get("trade_action_reason") or "").strip()
        decision_reason = (row.get("decision_reason") or "").strip()

        if balance is not None:
            balance_points.append((bar_time, balance))
        if equity is not None:
            equity_points.append((bar_time, equity))
        if free_margin is not None:
            free_margin_values.append(free_margin)
        if spread_points is not None:
            spread_values.append(spread_points)
        if decision_reason:
            decision_reason_counts[decision_reason] += 1
        if trade_action_reason.startswith("ENTRY_ORDER_FAIL"):
            reject_count += 1
            broker_constraint_events += 1

        if trade_action_reason in {"ENTRY_BUY_OK", "ENTRY_SELL_OK"}:
            fill_price = parse_float(row.get("trade_fill_price"))
            bid = parse_float(row.get("bid"))
            ask = parse_float(row.get("ask"))
            spread = parse_float(row.get("spread_points"))
            point = None
            if bid is not None and ask is not None and spread is not None and spread > 0.0:
                point = (ask - bid) / spread
            if fill_price is not None and point and point > 0.0:
                reference_price = ask if trade_action_reason == "ENTRY_BUY_OK" else bid
                if reference_price is not None:
                    fill_distance_points.append(abs(fill_price - reference_price) / point)

    balance_stats = compute_drawdown_metrics(balance_points)
    equity_stats = compute_drawdown_metrics(equity_points)

    trade_count = len(trades)
    net_profit = sum(float(trade["net_profit"]) for trade in trades)
    deposit = bundle.runtime_snapshot.deposit
    return_pct = (net_profit / deposit * 100.0) if deposit else None
    wins = [float(trade["net_profit"]) for trade in trades if float(trade["net_profit"]) > 0.0]
    losses = [float(trade["net_profit"]) for trade in trades if float(trade["net_profit"]) < 0.0]
    long_trades = [trade for trade in trades if trade["direction"] == "LONG"]
    short_trades = [trade for trade in trades if trade["direction"] == "SHORT"]
    mfe_values = [float(trade["mfe_mag"]) for trade in trades]
    mae_values = [float(trade["mae_mag"]) for trade in trades]
    hold_values = [float(trade["hold_bars"]) for trade in trades]

    daily_net: Counter[str] = Counter()
    weekly_net: Counter[str] = Counter()
    consecutive_losses = 0
    worst_streak = 0
    for trade in trades:
        trade_profit = float(trade["net_profit"])
        exit_time = trade["exit_time"]
        if isinstance(exit_time, datetime):
            daily_net[exit_time.strftime("%Y-%m-%d")] += trade_profit
            iso_year, iso_week, _ = exit_time.isocalendar()
            weekly_net[f"{iso_year}-W{iso_week:02d}"] += trade_profit
        if trade_profit < 0.0:
            consecutive_losses += 1
            worst_streak = max(worst_streak, consecutive_losses)
        else:
            consecutive_losses = 0

    avg_win = (sum(wins) / len(wins)) if wins else None
    avg_loss = (sum(losses) / len(losses)) if losses else None
    profit_factor = (sum(wins) / abs(sum(losses))) if losses else None
    expectancy = (net_profit / trade_count) if trade_count else None
    payoff_ratio = ((avg_win or 0.0) / abs(avg_loss)) if (avg_win is not None and avg_loss not in (None, 0.0)) else None
    equity_dd_amount = equity_stats["max_dd_amount"]
    recovery_factor = (net_profit / equity_dd_amount) if (equity_dd_amount not in (None, 0.0)) else None
    win_rate = (len(wins) / trade_count) if trade_count else None
    long_expectancy = (
        sum(float(trade["net_profit"]) for trade in long_trades) / len(long_trades) if long_trades else None
    )
    short_expectancy = (
        sum(float(trade["net_profit"]) for trade in short_trades) / len(short_trades) if short_trades else None
    )
    realized_over_mfe_values = [
        (float(trade["net_profit"]) / float(trade["mfe_mag"]))
        for trade in trades
        if float(trade["mfe_mag"]) > 0.0
    ]
    win_trade_mae_values = [float(trade["mae_mag"]) for trade in trades if float(trade["net_profit"]) > 0.0]
    loss_trade_mfe_values = [float(trade["mfe_mag"]) for trade in trades if float(trade["net_profit"]) < 0.0]

    order_attempts = sum(
        1
        for row in shadow_rows
        if (row.get("trade_action_reason") or "").strip() in {"ENTRY_BUY_OK", "ENTRY_SELL_OK"} or
        (row.get("trade_action_reason") or "").strip().startswith("ENTRY_ORDER_FAIL")
    )
    successful_entries = sum(
        1 for row in shadow_rows if (row.get("trade_action_reason") or "").strip() in {"ENTRY_BUY_OK", "ENTRY_SELL_OK"}
    )
    fill_rate = (successful_entries / order_attempts) if order_attempts else None
    runtime_warning_counts = {
        **dict(parsed_shadow["startup_skip_breakdown"]),
        **dict(parsed_shadow["unexpected_skip_breakdown"]),
    }

    return {
        "headline": {
            "net_profit": net_profit,
            "return_pct": return_pct,
            "trade_count": trade_count,
            "win_rate": win_rate,
            "profit_factor": profit_factor,
            "expectancy_per_trade": expectancy,
            "max_dd_pct": equity_stats["max_dd_pct"],
            "recovery_factor": recovery_factor,
            "extra": {
                "final_balance": balance_points[-1][1] if balance_points else None,
                "initial_deposit": deposit,
            },
        },
        "risk": {
            "max_dd_pct": balance_stats["max_dd_pct"],
            "max_dd_amount": balance_stats["max_dd_amount"],
            "equity_dd_pct": equity_stats["max_dd_pct"],
            "equity_dd_amount": equity_stats["max_dd_amount"],
            "time_under_water": equity_stats["time_under_water"],
            "longest_recovery_duration": equity_stats["longest_recovery_duration"],
            "worst_day": min(daily_net.values()) if daily_net else None,
            "worst_week": min(weekly_net.values()) if weekly_net else None,
            "min_free_margin": min(free_margin_values) if free_margin_values else None,
            "margin_call_proximity": None,
            "ulcer_index": equity_stats["ulcer_index"],
            "consecutive_losses": worst_streak if trade_count else None,
            "extra": {
                "min_balance": min((value for _, value in balance_points), default=None),
                "min_equity": min((value for _, value in equity_points), default=None),
            },
        },
        "diagnostics": {
            "avg_win": avg_win,
            "avg_loss": avg_loss,
            "payoff_ratio": payoff_ratio,
            "avg_hold": (sum(hold_values) / len(hold_values)) if hold_values else None,
            "hold_distribution": {
                "p50": percentile(hold_values, 0.50),
                "p90": percentile(hold_values, 0.90),
            },
            "long_count": len(long_trades),
            "short_count": len(short_trades),
            "long_expectancy": long_expectancy,
            "short_expectancy": short_expectancy,
            "mfe_mean": (sum(mfe_values) / len(mfe_values)) if mfe_values else None,
            "mfe_median": percentile(mfe_values, 0.50),
            "mfe_p90": percentile(mfe_values, 0.90),
            "mae_mean": (sum(mae_values) / len(mae_values)) if mae_values else None,
            "mae_median": percentile(mae_values, 0.50),
            "mae_p90": percentile(mae_values, 0.90),
            "realized_over_mfe": (
                sum(realized_over_mfe_values) / len(realized_over_mfe_values) if realized_over_mfe_values else None
            ),
            "win_trade_mae": (sum(win_trade_mae_values) / len(win_trade_mae_values)) if win_trade_mae_values else None,
            "loss_trade_mfe": (sum(loss_trade_mfe_values) / len(loss_trade_mfe_values)) if loss_trade_mfe_values else None,
            "rule_pass_rates": {
                "long_signal_rate": (
                    float(parsed_shadow["long_signal_count"]) / float(parsed_shadow["ready_row_count"])
                    if parsed_shadow["ready_row_count"]
                    else None
                ),
                "short_signal_rate": (
                    float(parsed_shadow["short_signal_count"]) / float(parsed_shadow["ready_row_count"])
                    if parsed_shadow["ready_row_count"]
                    else None
                ),
            },
            "no_trade_rate": float(parsed_shadow["no_trade_rate"]),
            "extra": {
                "decision_reason_breakdown": dict(decision_reason_counts),
                "trade_close_reason_breakdown": dict(Counter(str(trade["close_reason"]) for trade in trades)),
                "no_trade_count": int(parsed_shadow["no_trade_count"]),
                "mfe_mae_unit": "account_currency",
            },
        },
        "execution": {
            "reject_count": reject_count,
            "avg_spread": (sum(spread_values) / len(spread_values)) if spread_values else None,
            "avg_slippage": (sum(fill_distance_points) / len(fill_distance_points)) if fill_distance_points else None,
            "fill_rate": fill_rate,
            "next_tick_fill_distance": {
                "mean_points": (sum(fill_distance_points) / len(fill_distance_points)) if fill_distance_points else None,
                "p90_points": percentile(fill_distance_points, 0.90),
            },
            "runtime_warning_counts": runtime_warning_counts,
            "contract_skip_count": int(parsed_shadow["contract_skip_count"]),
            "contract_skip_breakdown": dict(parsed_shadow["contract_skip_breakdown"]),
            "broker_constraint_events": broker_constraint_events,
        },
    }


def main() -> int:
    args = build_parser().parse_args()
    bundle_path = Path(args.bundle_json).resolve()
    bundle = ExperimentBundle.from_json(bundle_path.read_text(encoding="utf-8-sig"))
    common_project_root = Path(args.common_project_root).resolve()
    runtime_id = args.runtime_id or bundle.identity.experiment_id
    terminal_path = Path(args.terminal_path).resolve()
    from_date, to_date, dates_derived_from_bundle = resolve_tester_dates(bundle, args)
    if not terminal_path.exists():
        raise FileNotFoundError(f"terminal executable not found: {terminal_path}")

    attempt_id = next_attempt_id(bundle)
    attempt_dir = bundle_path.parent / "mt5_attempts" / attempt_id
    attempt_dir.mkdir(parents=True, exist_ok=True)
    report_path = (attempt_dir / f"tester_report.{args.tester_report_format}").resolve()
    ini_path = (attempt_dir / "tester_run.ini").resolve()
    summary_path = (attempt_dir / "tester_attempt_summary.json").resolve()

    csv_log_relative_path = (
        Path("Project_Obsidian_Prime")
        / "runtime"
        / runtime_id
        / "logs"
        / f"{attempt_id}_shadow.csv"
    ).as_posix().replace("/", "\\")
    trade_ledger_relative_path = (
        Path("Project_Obsidian_Prime")
        / "runtime"
        / runtime_id
        / "logs"
        / f"{attempt_id}_trades.csv"
    ).as_posix().replace("/", "\\")
    csv_log_path = (common_project_root / "runtime" / runtime_id / "logs" / f"{attempt_id}_shadow.csv").resolve()
    trade_ledger_path = (common_project_root / "runtime" / runtime_id / "logs" / f"{attempt_id}_trades.csv").resolve()
    csv_log_path.parent.mkdir(parents=True, exist_ok=True)
    if csv_log_path.exists():
        csv_log_path.unlink()
    if trade_ledger_path.exists():
        trade_ledger_path.unlink()

    ini_text = build_tester_ini_text(
        bundle,
        runtime_id=runtime_id,
        from_date=from_date,
        to_date=to_date,
        feature_mode=args.feature_mode,
        enable_trading=args.enable_trading,
        warmup_bars=args.warmup_bars,
        magic_number=args.magic_number,
        trade_deviation_points=args.trade_deviation_points,
        report_path=report_path,
        csv_log_relative_path=csv_log_relative_path,
        trade_ledger_relative_path=trade_ledger_relative_path,
    )
    write_text(ini_path, ini_text)

    attempt_started_at = utc_now_iso()
    append_status(bundle, "running", f"tester_attempt_started:{attempt_id}")
    bundle_path.write_text(bundle.to_json(indent=2), encoding="utf-8")

    try:
        run_compile_runtime(bundle_path, runtime_id, common_project_root)

        subprocess.run(
            [str(terminal_path), f"/config:{ini_path}"],
            cwd=ROOT_DIR,
            check=True,
            timeout=60 * 15,
        )

        parsed = parse_shadow_csv(csv_log_path)
        shadow_rows = parsed.pop("rows", [])
        expected_ready_rows = expected_ready_row_count(bundle, args.split_name)
        ready_row_gap = (
            int(parsed["ready_row_count"]) - int(expected_ready_rows)
            if expected_ready_rows is not None
            else None
        )
        coverage_check = {
            "expected_ready_row_count": expected_ready_rows,
            "actual_ready_row_count": int(parsed["ready_row_count"]),
            "ready_row_gap": ready_row_gap,
            "matches_offline_split_count": (ready_row_gap == 0) if ready_row_gap is not None else None,
        }
        trades = parse_trade_ledger(trade_ledger_path)
        financial_metrics = summarize_financial_metrics(
            bundle=bundle,
            shadow_rows=shadow_rows,
            trades=trades,
            parsed_shadow=parsed,
        )
        summary_payload = {
            "status": "completed",
            "generated_at_utc": utc_now_iso(),
            "attempt_id": attempt_id,
            "runtime_id": runtime_id,
            "bundle_json": str(bundle_path),
            "tester_ini_path": str(ini_path),
            "tester_report_path": str(report_path),
            "csv_log_path": str(csv_log_path),
            "trade_ledger_path": str(trade_ledger_path),
            "split_name": args.split_name,
            "enable_trading": args.enable_trading,
            "date_window": {
                "from_date": from_date,
                "to_date": to_date,
                "derived_from_bundle": dates_derived_from_bundle,
            },
            "coverage_check": coverage_check,
            "metrics": parsed,
            "financial_metrics": financial_metrics,
        }
        summary_path.write_text(json.dumps(summary_payload, indent=2, ensure_ascii=False), encoding="utf-8")

        ini_artifact_id = f"art_{attempt_id}_tester_ini"
        csv_artifact_id = f"art_{attempt_id}_shadow_csv"
        trade_ledger_artifact_id = f"art_{attempt_id}_trade_ledger"
        summary_artifact_id = f"art_{attempt_id}_attempt_summary"
        upsert_artifact(
            bundle,
            ArtifactRef(
                artifact_id=ini_artifact_id,
                role="mt5_tester_ini",
                path=str(ini_path),
                format="ini",
                sha256=compute_sha256(ini_path),
                required=False,
            ),
        )
        upsert_artifact(
            bundle,
            ArtifactRef(
                artifact_id=csv_artifact_id,
                role="mt5_shadow_csv",
                path=str(csv_log_path),
                format="csv",
                sha256=compute_sha256(csv_log_path),
                required=False,
            ),
        )
        if trade_ledger_path.exists():
            upsert_artifact(
                bundle,
                ArtifactRef(
                    artifact_id=trade_ledger_artifact_id,
                    role="mt5_trade_ledger",
                    path=str(trade_ledger_path),
                    format="csv",
                    sha256=compute_sha256(trade_ledger_path),
                    required=False,
                ),
            )
        upsert_artifact(
            bundle,
            ArtifactRef(
                artifact_id=summary_artifact_id,
                role="mt5_attempt_summary",
                path=str(summary_path),
                format="json",
                sha256=compute_sha256(summary_path),
                required=False,
            ),
        )

        split_results = ensure_split_results(bundle, args.split_name)
        split_results.execution = ExecutionMetrics(
            skip_rate=1.0 - float(parsed["ready_rate"]),
            reject_count=int(financial_metrics["execution"]["reject_count"]) if financial_metrics["execution"]["reject_count"] is not None else None,
            avg_spread=float(financial_metrics["execution"]["avg_spread"]) if financial_metrics["execution"]["avg_spread"] is not None else None,
            avg_slippage=float(financial_metrics["execution"]["avg_slippage"]) if financial_metrics["execution"]["avg_slippage"] is not None else None,
            skip_reason_breakdown=dict(parsed["skip_reason_breakdown"]),
            external_mismatch_count=int(parsed["external_mismatch_count"]),
            fill_rate=float(financial_metrics["execution"]["fill_rate"]) if financial_metrics["execution"]["fill_rate"] is not None else None,
            next_tick_fill_distance=dict(financial_metrics["execution"]["next_tick_fill_distance"]),
            runtime_warning_counts={
                **dict(parsed["startup_skip_breakdown"]),
                **dict(parsed["unexpected_skip_breakdown"]),
            },
            data_readiness_failures=int(parsed["data_readiness_failures"]),
            broker_constraint_events=int(financial_metrics["execution"]["broker_constraint_events"]) if financial_metrics["execution"]["broker_constraint_events"] is not None else None,
            extra={
                "ready_row_count": int(parsed["ready_row_count"]),
                "row_count": int(parsed["row_count"]),
                "feature_ready_max": int(parsed["feature_ready_max"]),
                "latest_bar_time_server": parsed["latest_bar_time_server"],
                "expected_ready_row_count": expected_ready_rows,
                "ready_row_gap": ready_row_gap,
                "matches_offline_split_count": (ready_row_gap == 0) if ready_row_gap is not None else None,
                "contract_skip_count": int(parsed["contract_skip_count"]),
                "contract_skip_breakdown": dict(parsed["contract_skip_breakdown"]),
                "startup_skip_count": int(parsed["startup_skip_count"]),
                "startup_skip_breakdown": dict(parsed["startup_skip_breakdown"]),
                "unexpected_skip_count": int(parsed["unexpected_skip_count"]),
                "unexpected_skip_breakdown": dict(parsed["unexpected_skip_breakdown"]),
                "tester_from_date": from_date,
                "tester_to_date": to_date,
                "tester_dates_derived_from_bundle": dates_derived_from_bundle,
                "attempt_id": attempt_id,
                "csv_log_path": str(csv_log_path),
                "trade_ledger_path": str(trade_ledger_path),
            },
        )
        split_results.headline.net_profit = financial_metrics["headline"]["net_profit"]
        split_results.headline.return_pct = financial_metrics["headline"]["return_pct"]
        split_results.headline.trade_count = financial_metrics["headline"]["trade_count"]
        split_results.headline.win_rate = financial_metrics["headline"]["win_rate"]
        split_results.headline.profit_factor = financial_metrics["headline"]["profit_factor"]
        split_results.headline.expectancy_per_trade = financial_metrics["headline"]["expectancy_per_trade"]
        split_results.headline.max_dd_pct = financial_metrics["headline"]["max_dd_pct"]
        split_results.headline.recovery_factor = financial_metrics["headline"]["recovery_factor"]
        split_results.headline.extra = dict(financial_metrics["headline"]["extra"])

        split_results.risk.max_dd_pct = financial_metrics["risk"]["max_dd_pct"]
        split_results.risk.max_dd_amount = financial_metrics["risk"]["max_dd_amount"]
        split_results.risk.equity_dd_pct = financial_metrics["risk"]["equity_dd_pct"]
        split_results.risk.equity_dd_amount = financial_metrics["risk"]["equity_dd_amount"]
        split_results.risk.time_under_water = financial_metrics["risk"]["time_under_water"]
        split_results.risk.longest_recovery_duration = financial_metrics["risk"]["longest_recovery_duration"]
        split_results.risk.worst_day = financial_metrics["risk"]["worst_day"]
        split_results.risk.worst_week = financial_metrics["risk"]["worst_week"]
        split_results.risk.min_free_margin = financial_metrics["risk"]["min_free_margin"]
        split_results.risk.margin_call_proximity = financial_metrics["risk"]["margin_call_proximity"]
        split_results.risk.ulcer_index = financial_metrics["risk"]["ulcer_index"]
        split_results.risk.consecutive_losses = financial_metrics["risk"]["consecutive_losses"]
        split_results.risk.extra = dict(financial_metrics["risk"]["extra"])

        split_results.diagnostics.avg_win = financial_metrics["diagnostics"]["avg_win"]
        split_results.diagnostics.avg_loss = financial_metrics["diagnostics"]["avg_loss"]
        split_results.diagnostics.payoff_ratio = financial_metrics["diagnostics"]["payoff_ratio"]
        split_results.diagnostics.avg_hold = financial_metrics["diagnostics"]["avg_hold"]
        split_results.diagnostics.hold_distribution = dict(financial_metrics["diagnostics"]["hold_distribution"])
        split_results.diagnostics.long_count = financial_metrics["diagnostics"]["long_count"]
        split_results.diagnostics.short_count = financial_metrics["diagnostics"]["short_count"]
        split_results.diagnostics.long_expectancy = financial_metrics["diagnostics"]["long_expectancy"]
        split_results.diagnostics.short_expectancy = financial_metrics["diagnostics"]["short_expectancy"]
        split_results.diagnostics.mfe_mean = financial_metrics["diagnostics"]["mfe_mean"]
        split_results.diagnostics.mfe_median = financial_metrics["diagnostics"]["mfe_median"]
        split_results.diagnostics.mfe_p90 = financial_metrics["diagnostics"]["mfe_p90"]
        split_results.diagnostics.mae_mean = financial_metrics["diagnostics"]["mae_mean"]
        split_results.diagnostics.mae_median = financial_metrics["diagnostics"]["mae_median"]
        split_results.diagnostics.mae_p90 = financial_metrics["diagnostics"]["mae_p90"]
        split_results.diagnostics.realized_over_mfe = financial_metrics["diagnostics"]["realized_over_mfe"]
        split_results.diagnostics.win_trade_mae = financial_metrics["diagnostics"]["win_trade_mae"]
        split_results.diagnostics.loss_trade_mfe = financial_metrics["diagnostics"]["loss_trade_mfe"]
        split_results.diagnostics.rule_pass_rates = dict(financial_metrics["diagnostics"]["rule_pass_rates"])
        split_results.diagnostics.no_trade_rate = float(financial_metrics["diagnostics"]["no_trade_rate"])
        split_results.diagnostics.extra = dict(financial_metrics["diagnostics"]["extra"])
        split_results.diagnostics.extra["attempt_id"] = attempt_id

        bundle.results.report_refs = [
            ref
            for ref in bundle.results.report_refs
            if not (ref.split == args.split_name and ref.role in {"mt5_shadow_csv", "mt5_trade_ledger", "mt5_attempt_summary"})
        ]
        new_report_refs = [
            ReportReference(
                role="mt5_shadow_csv",
                split=args.split_name,
                artifact_id=csv_artifact_id,
                description=f"MT5 shadow/trade CSV log for {attempt_id}",
            ),
            ReportReference(
                role="mt5_attempt_summary",
                split=args.split_name,
                artifact_id=summary_artifact_id,
                description=f"MT5 attempt summary for {attempt_id}",
            ),
        ]
        if trade_ledger_path.exists():
            new_report_refs.append(
                ReportReference(
                    role="mt5_trade_ledger",
                    split=args.split_name,
                    artifact_id=trade_ledger_artifact_id,
                    description=f"MT5 closed trade ledger for {attempt_id}",
                )
            )
        bundle.results.report_refs.extend(new_report_refs)
        bundle.run_attempts.append(
            RunAttempt(
                attempt_id=attempt_id,
                status="completed",
                started_at_utc=attempt_started_at,
                ended_at_utc=utc_now_iso(),
                summary_metrics={
                    "split_name": args.split_name,
                    "row_count": parsed["row_count"],
                    "ready_row_count": parsed["ready_row_count"],
                    "ready_rate": parsed["ready_rate"],
                    "expected_ready_row_count": expected_ready_rows,
                    "ready_row_gap": ready_row_gap,
                    "long_signal_count": parsed["long_signal_count"],
                    "short_signal_count": parsed["short_signal_count"],
                    "no_trade_count": parsed["no_trade_count"],
                    "trade_count": financial_metrics["headline"]["trade_count"],
                    "net_profit": financial_metrics["headline"]["net_profit"],
                    "return_pct": financial_metrics["headline"]["return_pct"],
                    "max_dd_pct": financial_metrics["risk"]["equity_dd_pct"],
                },
                report_artifact_ids=[
                    artifact_id
                    for artifact_id in [csv_artifact_id, trade_ledger_artifact_id if trade_ledger_path.exists() else None, summary_artifact_id, ini_artifact_id]
                    if artifact_id is not None
                ],
            )
        )
        append_status(bundle, "completed", f"tester_attempt_completed:{attempt_id}")
        bundle_path.write_text(bundle.to_json(indent=2), encoding="utf-8")
        leaderboard_path: Path | None = None
        if not args.skip_leaderboard_refresh:
            try:
                leaderboard_path = refresh_leaderboard_markdown()
            except Exception as leaderboard_exc:
                print(f"[warn] leaderboard refresh failed: {leaderboard_exc}")

        print(f"[done] attempt_id={attempt_id}")
        print(f"[done] csv_log={csv_log_path}")
        print(f"[done] summary={summary_path}")
        if leaderboard_path is not None:
            print(f"[done] leaderboard={leaderboard_path}")
        return 0
    except Exception as exc:
        failure_payload = {
            "status": "failed",
            "generated_at_utc": utc_now_iso(),
            "attempt_id": attempt_id,
            "runtime_id": runtime_id,
            "bundle_json": str(bundle_path),
            "tester_ini_path": str(ini_path),
            "csv_log_path": str(csv_log_path),
            "error_type": exc.__class__.__name__,
            "error": str(exc),
        }
        summary_path.write_text(json.dumps(failure_payload, indent=2, ensure_ascii=False), encoding="utf-8")
        summary_artifact_id = f"art_{attempt_id}_attempt_failure"
        upsert_artifact(
            bundle,
            ArtifactRef(
                artifact_id=summary_artifact_id,
                role="mt5_attempt_failure",
                path=str(summary_path),
                format="json",
                sha256=compute_sha256(summary_path),
                required=False,
            ),
        )
        bundle.run_attempts.append(
            RunAttempt(
                attempt_id=attempt_id,
                status="failed",
                started_at_utc=attempt_started_at,
                ended_at_utc=utc_now_iso(),
                failure_summary=failure_payload,
                report_artifact_ids=[summary_artifact_id],
            )
        )
        append_status(bundle, "failed", f"tester_attempt_failed:{attempt_id}")
        bundle_path.write_text(bundle.to_json(indent=2), encoding="utf-8")
        if not args.skip_leaderboard_refresh:
            try:
                leaderboard_path = refresh_leaderboard_markdown()
                print(f"[done] leaderboard={leaderboard_path}")
            except Exception as leaderboard_exc:
                print(f"[warn] leaderboard refresh failed: {leaderboard_exc}")
        raise


if __name__ == "__main__":
    raise SystemExit(main())
