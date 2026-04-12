#!/usr/bin/env python3
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

import numpy as np
import onnxruntime as ort
import pandas as pd


ROOT_DIR = Path(__file__).resolve().parents[3]
STAGE_DIR = ROOT_DIR / "stages" / "38_prelive_evidence_pack"
OUTPUT_JSON = STAGE_DIR / "03_reviews" / "stage38_prelive_evidence_20260413.json"
OUTPUT_MD = STAGE_DIR / "03_reviews" / "stage38_prelive_evidence_20260413.md"

STAGE34_JSON = ROOT_DIR / "stages" / "34_outside_bar_mainline_promotion" / "03_reviews" / "stage34_mainline_20260412.json"
STAGE35_JSON = ROOT_DIR / "stages" / "35_candle_sidecar_simplification_check" / "03_reviews" / "stage35_simplification_20260412.json"
STAGE36_JSON = ROOT_DIR / "stages" / "36_outside_bar_localization_diagnostic" / "03_reviews" / "stage36_outside_bar_localization_20260412.json"
STAGE37_JSON = ROOT_DIR / "stages" / "37_long_horizon_bridge_read" / "03_reviews" / "stage37_bridge_20260412.json"
RUNTIME_HANDOFF_MD = ROOT_DIR / "stages" / "34_outside_bar_mainline_promotion" / "04_selected" / "runtime_handoff_status.md"

FEATURE_MATRIX_PATH = ROOT_DIR / "data" / "processed" / "fpmarkets_v2" / "features" / "extended_window" / "feature_matrix.parquet"
FEATURE_SCHEMA_PATH = ROOT_DIR / "stages" / "34_outside_bar_mainline_promotion" / "02_runs" / "active" / "34D_29s_outbarlong_0001" / "artifacts" / "feature_schema.json"
MODEL_PATH = ROOT_DIR / "stages" / "34_outside_bar_mainline_promotion" / "02_runs" / "active" / "34D_29s_outbarlong_0001" / "artifacts" / "model_probonly.onnx"
HANDOFF_TEST_SHADOW_PATH = Path(
    r"C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\Common\Files\Project_Obsidian_Prime\runtime\exp_34d_29s_outbarlong_v1_handoff\logs\att_0005_shadow.csv"
)

FEATURE_CONTEXT_COLUMNS = [
    "atr_14",
    "atr_50",
    "atr_14_over_atr_50",
    "return_1_over_atr_14",
    "rsi_14",
    "rsi_50",
    "bb_position_20",
    "historical_vol_20",
    "is_us_cash_open",
    "minutes_from_cash_open",
    "is_first_30m_after_open",
    "is_last_30m_before_cash_close",
    "vix_change_1",
    "vix_zscore_20",
    "us10yr_change_1",
    "us10yr_zscore_20",
    "usdx_change_1",
    "usdx_zscore_20",
]
EXTERNAL_SYMBOLS = ["VIX", "US10YR", "USDX"]
PROXY_PARITY_SAMPLE_SIZE = 100
FNV_PRIME = 16777619
FNV_MASK = (1 << 64) - 1


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def fmt_num(value: float | int | None, digits: int = 3) -> str:
    if value is None:
        return "n/a"
    if isinstance(value, int):
        return str(value)
    return f"{value:.{digits}f}"


def parse_server_ts(text: str) -> pd.Timestamp:
    return pd.Timestamp(text.replace(".", "-").replace(" ", "T") + "Z")


def month_path(symbol: str, ts: pd.Timestamp) -> Path:
    year = ts.strftime("%Y")
    month = ts.strftime("%Y-%m")
    return ROOT_DIR / "data" / "raw" / "mt5_bars" / "m5" / symbol / year / f"{symbol}_m5_{month}.parquet"


def load_symbol_windows(symbol: str, timestamps: list[pd.Timestamp]) -> pd.DataFrame:
    months: set[tuple[int, int]] = set()
    for ts in timestamps:
        for offset in range(0, 6):
            shifted = ts - pd.Timedelta(minutes=5 * offset)
            months.add((shifted.year, shifted.month))
    frames: list[pd.DataFrame] = []
    for year, month in sorted(months):
        month_ts = pd.Timestamp(year=year, month=month, day=1, tz="UTC")
        path = month_path(symbol, month_ts)
        if path.exists():
            frame = pd.read_parquet(path)
            frame["time_utc"] = pd.to_datetime(frame["time_utc"], utc=True)
            frame = frame.sort_values("time_utc").set_index("time_utc")
            frames.append(frame)
    if not frames:
        return pd.DataFrame()
    return pd.concat(frames).sort_index()


def classify_atr_bucket(value: float | None) -> str:
    if value is None or pd.isna(value):
        return "unknown"
    if value < 0.9:
        return "low"
    if value <= 1.1:
        return "mid"
    return "high"


def candle_record(ts: pd.Timestamp, row: pd.Series, prev_row: pd.Series | None) -> dict[str, object]:
    high = float(row["high"])
    low = float(row["low"])
    open_ = float(row["open"])
    close = float(row["close"])
    range_points = high - low
    body_points = abs(close - open_)
    upper_wick_points = high - max(open_, close)
    lower_wick_points = min(open_, close) - low
    outside_prev = None
    inside_prev = None
    if prev_row is not None:
        outside_prev = bool(high > float(prev_row["high"]) and low < float(prev_row["low"]))
        inside_prev = bool(high <= float(prev_row["high"]) and low >= float(prev_row["low"]))
    direction = "doji"
    if close > open_:
        direction = "bull"
    elif close < open_:
        direction = "bear"
    return {
        "timestamp": ts.isoformat(),
        "open": open_,
        "high": high,
        "low": low,
        "close": close,
        "range_points": range_points,
        "body_points": body_points,
        "upper_wick_points": upper_wick_points,
        "lower_wick_points": lower_wick_points,
        "body_to_range": None if range_points == 0 else body_points / range_points,
        "direction": direction,
        "outside_prev": outside_prev,
        "inside_prev": inside_prev,
    }


def feature_checksum(values: list[float]) -> int:
    h = 2166136261
    for value in values:
        token = f"{float(value):.8f}|"
        for ch in token:
            h ^= ord(ch)
            h = (h * FNV_PRIME) & FNV_MASK
    return h


def build_direct_event_pack(
    stage36: dict,
    feature_df: pd.DataFrame,
) -> dict[str, object]:
    raw_timestamps: list[pd.Timestamp] = []
    direct_events: list[dict[str, object]] = []
    split_order = ["validation", "test", "hist_2024"]
    for split_name in split_order:
        events = stage36["split_summaries"][split_name]["direct_events"]
        direct_events.extend(events)
        for event in events:
            raw_timestamps.append(parse_server_ts(event["suppressed_bar_time_server"]))

    us100_df = load_symbol_windows("US100", raw_timestamps)
    external_dfs = {symbol: load_symbol_windows(symbol, raw_timestamps) for symbol in EXTERNAL_SYMBOLS}

    enriched_events: list[dict[str, object]] = []
    atr_bucket_counter: Counter[str] = Counter()
    external_exact_counter: Counter[str] = Counter()

    for event in sorted(direct_events, key=lambda item: abs(float(item["net_profit_delta_35a_minus_35b"])), reverse=True):
        suppressed_ts = parse_server_ts(event["suppressed_bar_time_server"])
        trigger_ts = suppressed_ts - pd.Timedelta(minutes=5)
        feature_row = feature_df.loc[trigger_ts]
        feature_context = {
            column: (None if pd.isna(feature_row[column]) else float(feature_row[column]))
            for column in FEATURE_CONTEXT_COLUMNS
        }
        atr_bucket = classify_atr_bucket(feature_context["atr_14_over_atr_50"])
        atr_bucket_counter[atr_bucket] += 1

        window_rows: list[dict[str, object]] = []
        for offset in range(4, -1, -1):
            bar_ts = trigger_ts - pd.Timedelta(minutes=5 * offset)
            current_row = us100_df.loc[bar_ts]
            prev_row = us100_df.loc[bar_ts - pd.Timedelta(minutes=5)] if (bar_ts - pd.Timedelta(minutes=5)) in us100_df.index else None
            record = candle_record(bar_ts, current_row, prev_row)
            record["offset_from_trigger_bars"] = -offset
            window_rows.append(record)

        trigger_bar = next(item for item in window_rows if item["offset_from_trigger_bars"] == 0)

        external_exact = {}
        external_window5 = {}
        for symbol, df in external_dfs.items():
            exact = bool(trigger_ts in df.index)
            external_exact[symbol] = exact
            external_exact_counter[f"{symbol}:{exact}"] += 1
            count = 0
            for offset in range(0, 5):
                bar_ts = trigger_ts - pd.Timedelta(minutes=5 * offset)
                if bar_ts in df.index:
                    count += 1
            external_window5[symbol] = count

        enriched_events.append(
            {
                "split": event["split"],
                "direction": event["direction"],
                "entry_bar_time_server": event["entry_bar_time_server"],
                "suppressed_bar_time_server": event["suppressed_bar_time_server"],
                "trigger_bar_time_server": trigger_ts.strftime("%Y.%m.%d %H:%M:%S"),
                "suppressed_bar_time_ny": event["suppressed_bar_time_ny"],
                "weekday_ny": event["weekday_ny"],
                "session_bucket_ny": event["session_bucket_ny"],
                "decision_reason": event["decision_reason"],
                "argmax_class": event["argmax_class"],
                "argmax_margin": event["argmax_margin"],
                "floating_profit_at_suppression": event["floating_profit_at_suppression"],
                "net_profit_35a": event["net_profit_35a"],
                "net_profit_35b": event["net_profit_35b"],
                "net_profit_delta_35a_minus_35b": event["net_profit_delta_35a_minus_35b"],
                "later_exit_delay_bars": event["later_exit_delay_bars"],
                "feature_context_at_trigger_bar": feature_context,
                "atr_bucket": atr_bucket,
                "trigger_bar_shape": trigger_bar,
                "pre_trigger_window": window_rows,
                "external_exact_match_at_trigger_bar": external_exact,
                "external_exact_match_count_last5": external_window5,
            }
        )

    split_headline_total = sum(
        float(stage36["split_summaries"][split_name]["headline_delta_35a_minus_35b"]["net_profit"])
        for split_name in split_order
    )
    direct_total = sum(
        float(stage36["split_summaries"][split_name]["decomposition"]["direct_suppression_net_profit_delta_35a_minus_35b"])
        for split_name in split_order
    )

    return {
        "direct_event_count": len(enriched_events),
        "direct_net_profit_delta_total": direct_total,
        "headline_net_profit_delta_total": split_headline_total,
        "direct_share_of_headline_net_delta_total": None if split_headline_total == 0 else direct_total / split_headline_total,
        "atr_bucket_breakdown": dict(atr_bucket_counter),
        "external_exact_match_breakdown": dict(external_exact_counter),
        "events": enriched_events,
    }


def build_stage34_decomposition(stage34: dict) -> dict[str, object]:
    reference = stage34["reference"]
    candidates = {record["run_name"]: record for record in stage34["candidates"]}
    run34b = candidates["34B_29s_refcarry_0001"]
    run34c = candidates["34C_29n_outbarlong_0001"]
    run34d = candidates["34D_29s_outbarlong_0001"]

    by_split: dict[str, dict[str, float]] = {}
    for split_name in ["validation", "test", "hist_2024"]:
        ref = reference["splits"][split_name]
        b = run34b["splits"][split_name]
        c = run34c["splits"][split_name]
        d = run34d["splits"][split_name]
        by_split[split_name] = {
            "governance_only_return_delta_34b_minus_29n": float(b["return_pct"]) - float(ref["return_pct"]),
            "outbar_only_return_delta_34c_minus_29n": float(c["return_pct"]) - float(ref["return_pct"]),
            "combined_return_delta_34d_minus_29n": float(d["return_pct"]) - float(ref["return_pct"]),
            "incremental_outbar_on_governance_34d_minus_34b": float(d["return_pct"]) - float(b["return_pct"]),
            "incremental_pf_34d_minus_34b": float(d["profit_factor"]) - float(b["profit_factor"]),
            "incremental_dd_pct_34d_minus_34b": float(d["max_dd_pct"]) - float(b["max_dd_pct"]),
        }
    return {
        "reference_run": reference["run_name"],
        "governance_shadow_run": run34b["run_name"],
        "outbar_only_run": run34c["run_name"],
        "combined_run": run34d["run_name"],
        "by_split": by_split,
    }


def build_stage35_attribution(stage35: dict, stage36: dict) -> dict[str, object]:
    by_split: dict[str, dict[str, object]] = {}
    for split_name in ["validation", "test", "hist_2024"]:
        reference = stage35["reference"]["splits"][split_name]
        candidate = stage35["candidate"]["splits"][split_name]
        decomposition = stage36["split_summaries"][split_name]["decomposition"]
        by_split[split_name] = {
            "34d_return_pct": reference["return_pct"],
            "34b_return_pct": candidate["return_pct"],
            "return_pct_delta_34d_minus_34b": float(reference["return_pct"]) - float(candidate["return_pct"]),
            "profit_factor_delta_34d_minus_34b": float(reference["profit_factor"]) - float(candidate["profit_factor"]),
            "max_dd_pct_delta_34d_minus_34b": float(reference["max_dd_pct"]) - float(candidate["max_dd_pct"]),
            "trade_count_delta": int(reference["trade_count"]) - int(candidate["trade_count"]),
            "long_expectancy_delta_34d_minus_34b": float(reference["long_expectancy"]) - float(candidate["long_expectancy"]),
            "short_expectancy_delta_34d_minus_34b": float(reference["short_expectancy"]) - float(candidate["short_expectancy"]),
            "direct_suppression_event_count": decomposition["direct_suppression_event_count"],
            "direct_suppression_net_profit_delta_34d_minus_34b": decomposition["direct_suppression_net_profit_delta_35a_minus_35b"],
            "shifted_entry_net_profit_delta_34d_minus_34b": decomposition["shifted_entry_net_profit_delta_35a_minus_35b"],
            "carry_drift_net_profit_delta_34d_minus_34b": decomposition["carry_drift_net_profit_delta_35a_minus_35b"],
            "direct_share_of_headline_net_delta": decomposition["direct_share_of_headline_net_delta"],
        }
    return {
        "reference_run": stage35["reference"]["run_name"],
        "base_run": stage35["candidate"]["run_name"],
        "by_split": by_split,
    }


def build_stage37_continuity(stage37: dict) -> dict[str, object]:
    return {
        "bridge_window": stage37["bridge_window"],
        "reference_run": stage37["reference"]["run_name"],
        "base_run": stage37["candidate"]["run_name"],
        "bridge_delta": {
            "net_profit_delta_34d_minus_34b": stage37["delta"]["net_profit_delta"],
            "return_pct_delta_34d_minus_34b": stage37["delta"]["return_pct_delta"],
            "profit_factor_delta_34d_minus_34b": stage37["delta"]["profit_factor_delta"],
            "max_dd_pct_delta_34d_minus_34b": stage37["delta"]["max_dd_pct_delta"],
            "ulcer_index_delta_34d_minus_34b": stage37["delta"]["ulcer_index_delta"],
            "long_expectancy_delta_34d_minus_34b": stage37["delta"]["long_expectancy_delta"],
            "short_expectancy_delta_34d_minus_34b": stage37["delta"]["short_expectancy_delta"],
        },
        "year_buckets": stage37["delta"]["year_buckets"],
        "reference_bridge": stage37["reference"]["bridge"],
        "base_bridge": stage37["candidate"]["bridge"],
    }


def build_proxy_parity(feature_df: pd.DataFrame, feature_names: list[str]) -> dict[str, object]:
    shadow_df = pd.read_csv(HANDOFF_TEST_SHADOW_PATH)
    ready_rows = shadow_df[shadow_df["row_ready"].astype(str).str.lower() == "true"].tail(PROXY_PARITY_SAMPLE_SIZE).copy()

    session = ort.InferenceSession(str(MODEL_PATH), providers=["CPUExecutionProvider"])
    input_name = session.get_inputs()[0].name

    exact_diffs: list[float] = []
    best_neighbor_diffs: list[float] = []
    exact_checksum_matches = 0
    best_neighbor_checksum_matches = 0

    for _, row in ready_rows.iterrows():
        base_ts = parse_server_ts(str(row["bar_time_server"]))
        mt5_probs = np.array([row["p_short"], row["p_flat"], row["p_long"]], dtype=np.float32)
        neighbor_diffs: list[float] = []
        checksum_hit = False
        exact_hit = False
        exact_diff = None

        for minute_shift in [0, -5, 5]:
            ts = base_ts + pd.Timedelta(minutes=minute_shift)
            if ts not in feature_df.index:
                continue
            values = feature_df.loc[ts, feature_names].tolist()
            if any(pd.isna(values)):
                continue
            feature_array = np.asarray(values, dtype=np.float32).reshape(1, -1)
            py_probs = session.run(None, {input_name: feature_array})[0][0]
            diff = float(np.max(np.abs(py_probs - mt5_probs)))
            neighbor_diffs.append(diff)

            checksum_value = feature_checksum(values)
            if minute_shift == 0:
                exact_diff = diff
                if checksum_value == int(row["feature_checksum"]):
                    exact_hit = True
            if checksum_value == int(row["feature_checksum"]):
                checksum_hit = True

        if exact_diff is not None:
            exact_diffs.append(exact_diff)
        if neighbor_diffs:
            best_neighbor_diffs.append(min(neighbor_diffs))
        if exact_hit:
            exact_checksum_matches += 1
        if checksum_hit:
            best_neighbor_checksum_matches += 1

    def summarize(values: list[float]) -> dict[str, float | int | None]:
        if not values:
            return {"count": 0, "mean": None, "median": None, "p90": None, "max": None}
        arr = np.asarray(values, dtype=float)
        return {
            "count": int(arr.size),
            "mean": float(arr.mean()),
            "median": float(np.median(arr)),
            "p90": float(np.quantile(arr, 0.9)),
            "max": float(arr.max()),
        }

    return {
        "sample_source": str(HANDOFF_TEST_SHADOW_PATH),
        "sample_size_requested": PROXY_PARITY_SAMPLE_SIZE,
        "exact_timestamp_prob_diff": summarize(exact_diffs),
        "best_neighbor_prob_diff": summarize(best_neighbor_diffs),
        "exact_timestamp_checksum_match_count": exact_checksum_matches,
        "best_neighbor_checksum_match_count": best_neighbor_checksum_matches,
        "interpretation": (
            "processed feature_matrix is a useful proxy surface, but it is not yet a drop-in parity audit surface "
            "for the live MT5 runtime because neither exact checksum parity nor exact probability parity was recovered"
        ),
    }


def build_markdown(payload: dict) -> str:
    event_pack = payload["event_evidence"]
    attribution = payload["value_attribution"]
    parity = payload["proxy_parity"]

    lines = [
        "# Stage 38 Pre-Live Evidence Pack",
        "",
        f"- reviewed_on: `{payload['reviewed_on']}`",
        "- stage: `38_prelive_evidence_pack`",
        "- operating_reference: `34D_29s_outbarlong_0001`",
        "- base_shadow: `34B_29s_refcarry_0001`",
        "",
        "## Executive Read",
        "",
        "- this stage keeps the follow-up package broader than a single narrow rerun, but it still centers the work on the one place where the current live edge is actually being earned",
        f"- Stage 36 direct events remain the core evidence: `count={event_pack['direct_event_count']}` `direct_net={fmt_num(event_pack['direct_net_profit_delta_total'])}` `headline_net={fmt_num(event_pack['headline_net_profit_delta_total'])}` `share={fmt_num(event_pack['direct_share_of_headline_net_delta_total'], 4)}`",
        "- the broad next package is now easier to define as three linked workstreams:",
        "  - event evidence hardening",
        "  - base-versus-incumbent value attribution",
        "  - dedicated fresh runtime parity audit",
        "",
        "## Event Evidence",
        "",
        f"- direct-event count: `{event_pack['direct_event_count']}`",
        f"- atr bucket breakdown: `{event_pack['atr_bucket_breakdown']}`",
        f"- external exact-match breakdown at trigger bars: `{event_pack['external_exact_match_breakdown']}`",
        "",
        "### Critical Protection Events",
        "",
    ]

    for event in event_pack["events"]:
        feature_context = event["feature_context_at_trigger_bar"]
        trigger_bar = event["trigger_bar_shape"]
        lines.append(
            f"- `{event['split']}` `{event['suppressed_bar_time_server']}` "
            f"`delta={fmt_num(event['net_profit_delta_35a_minus_35b'])}` "
            f"`reason={event['decision_reason']}` "
            f"`session={event['session_bucket_ny']}` "
            f"`atr_ratio={fmt_num(feature_context['atr_14_over_atr_50'], 4)}` "
            f"`vix_change_1={fmt_num(feature_context['vix_change_1'], 4)}` "
            f"`us10yr_change_1={fmt_num(feature_context['us10yr_change_1'], 4)}`"
        )
        lines.append(
            f"- trigger bar `{event['trigger_bar_time_server']}` "
            f"`outside_prev={trigger_bar['outside_prev']}` "
            f"`direction={trigger_bar['direction']}` "
            f"`range={fmt_num(trigger_bar['range_points'], 2)}` "
            f"`body={fmt_num(trigger_bar['body_points'], 2)}` "
            f"`float_at_suppression={fmt_num(event['floating_profit_at_suppression'])}`"
        )
        lines.append(
            f"- externals: `VIX={event['external_exact_match_at_trigger_bar']['VIX']}` "
            f"`US10YR={event['external_exact_match_at_trigger_bar']['US10YR']}` "
            f"`USDX={event['external_exact_match_at_trigger_bar']['USDX']}`"
        )
        lines.append("")

    lines.extend(
        [
            "## Value Attribution",
            "",
            "### Stage 34 Decomposition",
            "",
        ]
    )

    for split_name, values in attribution["stage34_decomposition"]["by_split"].items():
        lines.append(
            f"- `{split_name}` "
            f"`34B-29N={fmt_num(values['governance_only_return_delta_34b_minus_29n'])}` "
            f"`34C-29N={fmt_num(values['outbar_only_return_delta_34c_minus_29n'])}` "
            f"`34D-29N={fmt_num(values['combined_return_delta_34d_minus_29n'])}` "
            f"`34D-34B={fmt_num(values['incremental_outbar_on_governance_34d_minus_34b'])}`"
        )

    lines.extend(["", "### Stage 35 / Stage 36 Split-Reset Attribution", ""])
    for split_name, values in attribution["stage35_and_36"]["by_split"].items():
        lines.append(
            f"- `{split_name}` "
            f"`return_delta={fmt_num(values['return_pct_delta_34d_minus_34b'])}` "
            f"`pf_delta={fmt_num(values['profit_factor_delta_34d_minus_34b'], 4)}` "
            f"`dd_delta={fmt_num(values['max_dd_pct_delta_34d_minus_34b'], 4)}` "
            f"`direct_events={values['direct_suppression_event_count']}` "
            f"`direct_net={fmt_num(values['direct_suppression_net_profit_delta_34d_minus_34b'])}`"
        )

    bridge = attribution["stage37_continuity"]
    lines.extend(["", "### Stage 37 Continuous Bridge", ""])
    lines.append(
        f"- bridge delta `net={fmt_num(bridge['bridge_delta']['net_profit_delta_34d_minus_34b'])}` "
        f"`return_pct={fmt_num(bridge['bridge_delta']['return_pct_delta_34d_minus_34b'])}` "
        f"`pf={fmt_num(bridge['bridge_delta']['profit_factor_delta_34d_minus_34b'], 4)}` "
        f"`dd_pct={fmt_num(bridge['bridge_delta']['max_dd_pct_delta_34d_minus_34b'], 4)}` "
        f"`ulcer={fmt_num(bridge['bridge_delta']['ulcer_index_delta_34d_minus_34b'], 4)}`"
    )
    for bucket_name, bucket in bridge["year_buckets"].items():
        lines.append(
            f"- `{bucket_name}` `net_delta={fmt_num(bucket['net_profit_delta'])}` `trade_delta={bucket['trade_count_delta']}`"
        )

    lines.extend(["", "## Proxy Parity Read", ""])
    exact = parity["exact_timestamp_prob_diff"]
    best = parity["best_neighbor_prob_diff"]
    lines.append(
        f"- exact timestamp proxy: `count={exact['count']}` `mean_max_abs={fmt_num(exact['mean'], 4)}` "
        f"`p90={fmt_num(exact['p90'], 4)}` `max={fmt_num(exact['max'], 4)}`"
    )
    lines.append(
        f"- best-neighbor proxy: `count={best['count']}` `mean_max_abs={fmt_num(best['mean'], 4)}` "
        f"`p90={fmt_num(best['p90'], 4)}` `max={fmt_num(best['max'], 4)}`"
    )
    lines.append(
        f"- checksum matches: `exact={parity['exact_timestamp_checksum_match_count']}` "
        f"`best_neighbor={parity['best_neighbor_checksum_match_count']}`"
    )
    lines.append(f"- interpretation: {parity['interpretation']}")

    lines.extend(
        [
            "",
            "## Follow-Up Bias",
            "",
            "- keep the next work package broader than a single narrow rerun, but still centered on the direct-event evidence that actually explains the live edge",
            "- build the human-facing base-versus-incumbent story around `34B -> 34D`, then use `34C` only as the decomposition side note",
            "- do not jump from this stage straight into broad retraining or blanket simplification",
            "- before live attachment, prioritize a fresh runtime snapshot parity audit over any new alpha-search branch",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    stage34 = load_json(STAGE34_JSON)
    stage35 = load_json(STAGE35_JSON)
    stage36 = load_json(STAGE36_JSON)
    stage37 = load_json(STAGE37_JSON)
    feature_names = load_json(FEATURE_SCHEMA_PATH)["feature_names"]

    feature_df = pd.read_parquet(FEATURE_MATRIX_PATH)
    feature_df["timestamp"] = pd.to_datetime(feature_df["timestamp"], utc=True)
    feature_df = feature_df[feature_df["symbol"] == "US100"].set_index("timestamp").sort_index()

    payload = {
        "reviewed_on": "2026-04-13",
        "event_evidence": build_direct_event_pack(stage36, feature_df),
        "value_attribution": {
            "stage34_decomposition": build_stage34_decomposition(stage34),
            "stage35_and_36": build_stage35_attribution(stage35, stage36),
            "stage37_continuity": build_stage37_continuity(stage37),
        },
        "proxy_parity": build_proxy_parity(feature_df, feature_names),
        "report_inputs": {
            "stage34_json": str(STAGE34_JSON),
            "stage35_json": str(STAGE35_JSON),
            "stage36_json": str(STAGE36_JSON),
            "stage37_json": str(STAGE37_JSON),
            "feature_matrix": str(FEATURE_MATRIX_PATH),
            "feature_schema": str(FEATURE_SCHEMA_PATH),
            "model_path": str(MODEL_PATH),
            "runtime_handoff_note": str(RUNTIME_HANDOFF_MD),
        },
    }
    write_json(OUTPUT_JSON, payload)
    write_text(OUTPUT_MD, build_markdown(payload))
    print(f"[done] wrote={OUTPUT_JSON}")
    print(f"[done] wrote={OUTPUT_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
