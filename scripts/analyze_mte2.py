#!/usr/bin/env python3
"""Analyze Market Tradability Engine v2 Pine-log CSV exports.

The analyzer reads ``MTE2 CAL`` rows, reports state coverage and classification
blockers, and derives forward price outcomes from the logged OHLC/ATR values.
Optionally, it can attach MTE2 states to a CSV of realized strategy signals and
compare allowed versus blocked trades.

Usage:
    python3 scripts/analyze_mte2.py <log-file-or-directory>
    python3 scripts/analyze_mte2.py testdata/mte2 --out report.md
    python3 scripts/analyze_mte2.py testdata/mte2 \
        --signals-csv signals.csv --allowed-states READY,BREAKOUT,TREND
    python3 scripts/analyze_mte2.py testdata/mte2 \
        --tps-csv matching-tps-transition-log.csv

Signal CSV columns:
    Join key: ``bar`` (preferred), or ``timestamp``/``Datum``/``Time``.
    Optional disambiguation: ``symbol`` and ``tf``.
    Outcome: ``R``/``outcomeR``; optional ``MFE`` and ``MAE``.
"""

from __future__ import annotations

import argparse
import csv
import math
import re
import statistics
import sys
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Iterable


MARKER = "MTE2 CAL"
DEFAULT_HORIZONS = (5, 10, 20)
STATE_ORDER = (
    "NO_TRADE",
    "BALANCE",
    "COMPRESSION",
    "READY",
    "BREAKOUT",
    "TREND",
    "AFTERMATH",
    "EXHAUSTION",
)
GATE_FIELDS = (
    "dataReady",
    "hasFramework",
    "rangeFramework",
    "balanceAllowed",
    "balance",
    "compression",
    "ready",
    "breakout",
    "trend",
    "aftermath",
    "exhaustion",
    "energyBuilding",
    "bullPressure",
    "bearPressure",
    "rawBullBreak",
    "rawBearBreak",
    "volumeConfirmed",
    "compressionArmed",
    "breakoutArmed",
)


def canonical_state(value: str | None) -> str:
    return (value or "UNKNOWN").strip().upper().replace(" ", "_")


def parse_kv(message: str) -> dict[str, str]:
    """Parse pipe-delimited key/value fields without truncating spaced values."""
    marker_at = message.find(MARKER)
    if marker_at < 0:
        return {}
    payload = message[marker_at:]
    parsed: dict[str, str] = {}
    for field in payload.split("|")[1:]:
        key, separator, value = field.strip().partition("=")
        if separator:
            parsed[key.strip()] = value.strip()
    return parsed


def csv_files(path: Path) -> Iterable[Path]:
    if path.is_file():
        if path.suffix.lower() == ".csv":
            yield path
        return
    yield from sorted(candidate for candidate in path.rglob("*.csv") if candidate.is_file())


def load_rows(path: str) -> list[dict[str, str]]:
    source = Path(path)
    if not source.exists():
        sys.exit(f"Input not found: {source}")

    files = list(csv_files(source))
    if not files:
        sys.exit(f"No CSV files in {source}")

    rows: list[dict[str, str]] = []
    for file_path in files:
        with file_path.open(encoding="utf-8-sig", newline="") as handle:
            for csv_row in csv.DictReader(handle):
                message = csv_row.get("Nachricht") or csv_row.get("Message") or ""
                if MARKER not in message:
                    continue
                parsed = parse_kv(message)
                if not parsed:
                    continue
                parsed["state"] = canonical_state(parsed.get("state"))
                parsed["candidate"] = canonical_state(parsed.get("candidate"))
                parsed["_ts"] = (
                    csv_row.get("Datum")
                    or csv_row.get("Time")
                    or csv_row.get("Timestamp")
                    or parsed.get("time")
                    or ""
                )
                parsed["_source"] = str(file_path)
                rows.append(parsed)
    if not rows:
        sys.exit(f"No {MARKER} rows in {source}")
    return rows


def numeric(value: str | int | float | None) -> float | None:
    if value is None or value == "":
        return None
    try:
        parsed = float(str(value).replace(",", ""))
        return parsed if math.isfinite(parsed) else None
    except ValueError:
        return None


def integer(value: str | int | None) -> int | None:
    number = numeric(value)
    return int(number) if number is not None else None


def boolean(value: str | None) -> bool | None:
    if value is None:
        return None
    lowered = value.lower()
    if lowered == "true":
        return True
    if lowered == "false":
        return False
    return None


def mean(values: Iterable[float]) -> float:
    materialized = [value for value in values if math.isfinite(value)]
    return statistics.fmean(materialized) if materialized else math.nan


def median(values: Iterable[float]) -> float:
    materialized = [value for value in values if math.isfinite(value)]
    return statistics.median(materialized) if materialized else math.nan


def fmt(value: float, digits: int = 2) -> str:
    if math.isnan(value):
        return "—"
    return f"{value:.{digits}f}"


def pct(numerator: int, denominator: int) -> str:
    return "—" if denominator == 0 else f"{100.0 * numerator / denominator:.1f}%"


def grouped_runs(rows: list[dict[str, str]]) -> list[list[dict[str, str]]]:
    grouped: dict[tuple[str, str, str], list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        key = (row.get("_source", ""), row.get("symbol", "?"), row.get("tf", "?"))
        grouped[key].append(row)

    runs: list[list[dict[str, str]]] = []
    for run_rows in grouped.values():
        by_bar: dict[int, dict[str, str]] = {}
        without_bar: list[dict[str, str]] = []
        for row in run_rows:
            bar = integer(row.get("bar"))
            if bar is None:
                without_bar.append(row)
            else:
                by_bar[bar] = row
        ordered = [by_bar[bar] for bar in sorted(by_bar)]
        ordered.extend(without_bar)
        runs.append(ordered)
    return runs


def state_durations(runs: list[list[dict[str, str]]]) -> dict[str, list[int]]:
    durations: dict[str, list[int]] = defaultdict(list)
    for rows in runs:
        active_state: str | None = None
        active_bars = 0
        previous_bar: int | None = None
        for row in rows:
            state = row["state"]
            bar = integer(row.get("bar"))
            contiguous = previous_bar is None or bar is None or bar == previous_bar + 1
            if state != active_state or not contiguous:
                if active_state is not None:
                    durations[active_state].append(active_bars)
                active_state = state
                active_bars = 1
            else:
                active_bars += 1
            previous_bar = bar
        if active_state is not None:
            durations[active_state].append(active_bars)
    return durations


def forward_outcomes(
    runs: list[list[dict[str, str]]], horizons: tuple[int, ...]
) -> dict[int, list[dict[str, float | str | bool | None]]]:
    outcomes: dict[int, list[dict[str, float | str | bool | None]]] = defaultdict(list)
    for rows in runs:
        for index, row in enumerate(rows):
            origin_bar = integer(row.get("bar"))
            close = numeric(row.get("close"))
            atr = numeric(row.get("atr"))
            acceptance = numeric(row.get("acceptance"))
            if origin_bar is None or close is None or atr is None or atr <= 0.0:
                continue

            for horizon in horizons:
                end_index = index + horizon
                if end_index >= len(rows):
                    continue
                end_bar = integer(rows[end_index].get("bar"))
                if end_bar != origin_bar + horizon:
                    continue
                future = rows[index + 1 : end_index + 1]
                highs = [numeric(item.get("high")) for item in future]
                lows = [numeric(item.get("low")) for item in future]
                closes = [numeric(item.get("close")) for item in future]
                if any(value is None for value in highs + lows + closes):
                    continue

                typed_highs = [float(value) for value in highs if value is not None]
                typed_lows = [float(value) for value in lows if value is not None]
                typed_closes = [float(value) for value in closes if value is not None]
                final_close = typed_closes[-1]
                long_mfe = max(0.0, (max(typed_highs) - close) / atr)
                long_mae = max(0.0, (close - min(typed_lows)) / atr)
                short_mfe = long_mae
                short_mae = long_mfe
                direction = 1 if (acceptance or 0.0) > 0.0 else -1 if (acceptance or 0.0) < 0.0 else 0
                aligned_return = direction * (final_close - close) / atr if direction else math.nan
                aligned_mfe = long_mfe if direction > 0 else short_mfe if direction < 0 else math.nan
                aligned_mae = long_mae if direction > 0 else short_mae if direction < 0 else math.nan

                path = [close, *typed_closes]
                travel = sum(abs(path[i] - path[i - 1]) for i in range(1, len(path)))
                path_efficiency = abs(final_close - close) / travel if travel > 0.0 else 0.0

                first_touch: bool | None = None
                if direction:
                    for high, low in zip(typed_highs, typed_lows):
                        favorable = (high - close) / atr if direction > 0 else (close - low) / atr
                        adverse = (close - low) / atr if direction > 0 else (high - close) / atr
                        if favorable >= 1.0 or adverse >= 1.0:
                            first_touch = favorable >= 1.0 and adverse < 1.0
                            break

                outcomes[horizon].append(
                    {
                        "state": row["state"],
                        "return": (final_close - close) / atr,
                        "abs_return": abs(final_close - close) / atr,
                        "oracle_mfe": max(long_mfe, short_mfe),
                        "aligned_return": aligned_return,
                        "aligned_mfe": aligned_mfe,
                        "aligned_mae": aligned_mae,
                        "path_efficiency": path_efficiency,
                        "first_touch": first_touch,
                    }
                )
    return outcomes


def get_alias(row: dict[str, str], aliases: tuple[str, ...]) -> str | None:
    for alias in aliases:
        if alias in row and row[alias] != "":
            return row[alias]
    lowered = {key.lower(): value for key, value in row.items()}
    for alias in aliases:
        value = lowered.get(alias.lower())
        if value not in (None, ""):
            return value
    return None


def load_signals(path: str) -> list[dict[str, str]]:
    with open(path, encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def load_tps_transitions(path: str) -> list[tuple[datetime, str]]:
    pattern = re.compile(r"TPS STATE (.*?) -> (.*?) \|")
    transitions: list[tuple[datetime, str]] = []
    with open(path, encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            message = row.get("Nachricht") or row.get("Message") or ""
            timestamp = row.get("Datum") or row.get("Time") or row.get("Timestamp") or ""
            match = pattern.search(message)
            if not match or not timestamp:
                continue
            transitions.append((datetime.fromisoformat(timestamp), match.group(2)))
    return sorted(transitions)


def join_tps_states(
    bars: list[dict[str, str]], transitions: list[tuple[datetime, str]]
) -> list[tuple[str, str]]:
    if not transitions:
        return []
    ordered_bars = sorted(
        (row for row in bars if row.get("_ts")),
        key=lambda row: datetime.fromisoformat(row["_ts"]),
    )
    joined: list[tuple[str, str]] = []
    transition_index = 0
    tps_state: str | None = None
    for row in ordered_bars:
        timestamp = datetime.fromisoformat(row["_ts"])
        while (
            transition_index < len(transitions)
            and transitions[transition_index][0] <= timestamp
        ):
            tps_state = transitions[transition_index][1]
            transition_index += 1
        if tps_state is not None:
            joined.append((row["state"], tps_state))
    return joined


def attach_signals(
    signals: list[dict[str, str]], bars: list[dict[str, str]]
) -> tuple[list[dict[str, str | float]], int]:
    exact_bar: dict[tuple[str, str, int], list[dict[str, str]]] = defaultdict(list)
    loose_bar: dict[int, list[dict[str, str]]] = defaultdict(list)
    timestamps: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in bars:
        bar = integer(row.get("bar"))
        if bar is not None:
            exact_bar[(row.get("symbol", ""), row.get("tf", ""), bar)].append(row)
            loose_bar[bar].append(row)
        if row.get("_ts"):
            timestamps[row["_ts"]].append(row)

    attached: list[dict[str, str | float]] = []
    eligible = 0
    for signal in signals:
        outcome_r = numeric(get_alias(signal, ("R", "outcomeR", "outcome_r")))
        if outcome_r is None:
            continue
        eligible += 1
        bar = integer(get_alias(signal, ("bar", "entryBar", "entry_bar")))
        symbol = get_alias(signal, ("symbol", "ticker")) or ""
        timeframe = get_alias(signal, ("tf", "timeframe")) or ""
        matched: dict[str, str] | None = None
        if bar is not None:
            exact_matches = exact_bar.get((symbol, timeframe, bar), [])
            if len(exact_matches) == 1:
                matched = exact_matches[0]
            if matched is None and len(loose_bar.get(bar, [])) == 1:
                matched = loose_bar[bar][0]
        if matched is None:
            timestamp = get_alias(signal, ("timestamp", "Datum", "Time", "date")) or ""
            if len(timestamps.get(timestamp, [])) == 1:
                matched = timestamps[timestamp][0]
        if matched is None:
            continue
        mfe = numeric(get_alias(signal, ("MFE", "mfe")))
        mae = numeric(get_alias(signal, ("MAE", "mae")))
        attached.append(
            {
                "state": matched["state"],
                "R": outcome_r,
                "MFE": mfe if mfe is not None else math.nan,
                "MAE": mae if mae is not None else math.nan,
            }
        )
    return attached, eligible


def trade_stats(rows: list[dict[str, str | float]]) -> tuple[int, float, float, float]:
    returns = [float(row["R"]) for row in rows]
    if not returns:
        return 0, math.nan, math.nan, math.nan
    winners = [value for value in returns if value > 0.0]
    losers = [value for value in returns if value < 0.0]
    profit_factor = sum(winners) / abs(sum(losers)) if losers else math.inf
    return len(returns), mean(returns), 100.0 * len(winners) / len(returns) if returns else math.nan, profit_factor


def render_report(
    rows: list[dict[str, str]],
    horizons: tuple[int, ...],
    signal_rows: list[dict[str, str | float]] | None,
    signal_total: int,
    allowed_states: set[str],
    tps_rows: list[tuple[str, str]] | None,
) -> str:
    runs = grouped_runs(rows)
    outcomes = forward_outcomes(runs, horizons)
    state_counts = Counter(row["state"] for row in rows)
    candidate_counts = Counter(row["candidate"] for row in rows)
    reasons = Counter(
        row.get("noTradeReason", "UNKNOWN")
        for row in rows
        if row["candidate"] == "NO_TRADE"
    )
    mismatch = sum(row["state"] != row["candidate"] for row in rows)
    durations = state_durations(runs)

    lines: list[str] = ["# Market Tradability Engine v2 — Log Analysis", ""]
    lines.append(
        f"Rows: {len(rows)} · Runs: {len(runs)} · "
        f"State/candidate mismatch: {mismatch} ({pct(mismatch, len(rows))})"
    )
    lines.append("")

    lines.extend(("## 1 · State coverage", "", "| State | Confirmed bars | Share | Candidate bars | Median duration |", "|---|---:|---:|---:|---:|"))
    for state in STATE_ORDER:
        count = state_counts.get(state, 0)
        state_runs = durations.get(state, [])
        lines.append(
            f"| {state} | {count} | {pct(count, len(rows))} | "
            f"{candidate_counts.get(state, 0)} | {fmt(median(state_runs), 1)} |"
        )
    unknown_states = sorted(set(state_counts) - set(STATE_ORDER))
    for state in unknown_states:
        count = state_counts[state]
        lines.append(f"| {state} | {count} | {pct(count, len(rows))} | {candidate_counts.get(state, 0)} | — |")
    lines.append("")

    lines.extend(("## 2 · NO_TRADE blockers", "", "| Reason | Bars | Share of NO_TRADE candidates |", "|---|---:|---:|"))
    reason_total = sum(reasons.values())
    for reason, count in reasons.most_common():
        lines.append(f"| {reason} | {count} | {pct(count, reason_total)} |")
    lines.append("")

    available_gates = [gate for gate in GATE_FIELDS if any(gate in row for row in rows)]
    if available_gates:
        lines.extend(("## 3 · Gate activation", "", "| Gate | true | evaluated | Rate |", "|---|---:|---:|---:|"))
        for gate in available_gates:
            values = [boolean(row.get(gate)) for row in rows]
            evaluated = [value for value in values if value is not None]
            true_count = sum(value is True for value in evaluated)
            lines.append(f"| {gate} | {true_count} | {len(evaluated)} | {pct(true_count, len(evaluated))} |")
        lines.append("")

    section = 4
    if tps_rows is not None:
        tps_order = (
            "Trend Strong",
            "Trend Healthy",
            "Transition",
            "Weak / Range",
            "Trend Dead",
        )
        lines.extend(
            (
                f"## {section} · TPS state cross-check",
                "",
                "TPS transitions are carried forward to MTE bar timestamps. This is valid only when both exports use the same symbol, timeframe and settings.",
                "",
                "| TPS state | Joined bars | MTE NO_TRADE | MTE TREND | MTE EXHAUSTION |",
                "|---|---:|---:|---:|---:|",
            )
        )
        for tps_state in tps_order:
            samples = [mte_state for mte_state, state in tps_rows if state == tps_state]
            counts = Counter(samples)
            lines.append(
                f"| {tps_state} | {len(samples)} | "
                f"{pct(counts['NO_TRADE'], len(samples))} | "
                f"{pct(counts['TREND'], len(samples))} | "
                f"{pct(counts['EXHAUSTION'], len(samples))} |"
            )
        healthy = {"Trend Strong", "Trend Healthy"}
        baseline_healthy = sum(state in healthy for _, state in tps_rows)
        mte_trend = [state for mte_state, state in tps_rows if mte_state == "TREND"]
        mte_no_trade = [state for mte_state, state in tps_rows if mte_state == "NO_TRADE"]
        lines.append("")
        lines.append(
            f"TPS Healthy/Strong baseline: **{pct(baseline_healthy, len(tps_rows))}** · "
            f"inside MTE TREND: **{pct(sum(state in healthy for state in mte_trend), len(mte_trend))}** · "
            f"inside MTE NO_TRADE: **{pct(sum(state in healthy for state in mte_no_trade), len(mte_no_trade))}**"
        )
        lines.append("")
        section += 1

    for horizon in horizons:
        horizon_rows = outcomes.get(horizon, [])
        lines.extend(
            (
                f"## {section} · Forward outcomes — {horizon} bars",
                "",
                "ATR-normalized. `Aligned` follows the sign of Acceptance; `1R first` means +1 ATR before −1 ATR.",
                "",
                "| State | N | Mean abs return | Mean oracle MFE | Mean path efficiency | Mean aligned return | Mean aligned MFE | Mean aligned MAE | 1R first |",
                "|---|---:|---:|---:|---:|---:|---:|---:|---:|",
            )
        )
        for state in STATE_ORDER:
            samples = [item for item in horizon_rows if item["state"] == state]
            if not samples:
                continue
            touches = [item["first_touch"] for item in samples if item["first_touch"] is not None]
            touch_wins = sum(value is True for value in touches)
            lines.append(
                f"| {state} | {len(samples)} | "
                f"{fmt(mean(float(item['abs_return']) for item in samples))} | "
                f"{fmt(mean(float(item['oracle_mfe']) for item in samples))} | "
                f"{fmt(mean(float(item['path_efficiency']) for item in samples))} | "
                f"{fmt(mean(float(item['aligned_return']) for item in samples))} | "
                f"{fmt(mean(float(item['aligned_mfe']) for item in samples))} | "
                f"{fmt(mean(float(item['aligned_mae']) for item in samples))} | "
                f"{pct(touch_wins, len(touches))} |"
            )
        lines.append("")
        section += 1

    if signal_rows is not None:
        allowed = [row for row in signal_rows if row["state"] in allowed_states]
        blocked = [row for row in signal_rows if row["state"] not in allowed_states]
        lines.extend(
            (
                f"## {section} · Strategy filter lift",
                "",
                f"Allowed states: {', '.join(sorted(allowed_states))}. "
                f"Matched signals: {len(signal_rows)} of {signal_total} rows with R.",
                "",
                "| Segment | Trades | Mean R | Win rate | Profit factor |",
                "|---|---:|---:|---:|---:|",
            )
        )
        for label, samples in (("All", signal_rows), ("Allowed", allowed), ("Blocked", blocked)):
            count, average_r, win_rate, profit_factor = trade_stats(samples)
            pf_text = "∞" if math.isinf(profit_factor) else fmt(profit_factor)
            lines.append(f"| {label} | {count} | {fmt(average_r)} | {fmt(win_rate, 1)}% | {pf_text} |")
        lines.append("")
        all_winners = [row for row in signal_rows if float(row["R"]) > 0.0]
        all_losers = [row for row in signal_rows if float(row["R"]) < 0.0]
        blocked_winners = [row for row in blocked if float(row["R"]) > 0.0]
        blocked_losers = [row for row in blocked if float(row["R"]) < 0.0]
        all_mean = mean(float(row["R"]) for row in signal_rows)
        allowed_mean = mean(float(row["R"]) for row in allowed)
        expectancy_lift = allowed_mean - all_mean
        lines.append(
            f"Coverage: **{pct(len(allowed), len(signal_rows))}** · "
            f"Loss avoidance: **{pct(len(blocked_losers), len(all_losers))}** · "
            f"Missed winners: **{pct(len(blocked_winners), len(all_winners))}** · "
            f"Expectancy lift: **{fmt(expectancy_lift)}R/trade** · "
            f"Blocked net result: **{fmt(sum(float(row['R']) for row in blocked))}R**"
        )
        lines.append("")

    lines.append(
        "> Forward outcomes are descriptive market labels, not a profitability test. "
        "The strategy filter section is the decisive test: validate its expectancy lift "
        "chronologically and out of sample across multiple instruments/timeframes."
    )
    lines.append("")
    return "\n".join(lines)


def parse_horizons(raw: str) -> tuple[int, ...]:
    try:
        horizons = tuple(sorted({int(value) for value in raw.split(",") if int(value) > 0}))
    except ValueError as error:
        raise argparse.ArgumentTypeError("horizons must be positive comma-separated integers") from error
    if not horizons:
        raise argparse.ArgumentTypeError("at least one horizon is required")
    return horizons


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", help="TradingView Pine-log CSV file or directory")
    parser.add_argument("--out", help="Write Markdown report to this path")
    parser.add_argument("--horizons", type=parse_horizons, default=DEFAULT_HORIZONS)
    parser.add_argument("--signals-csv", help="Optional realized strategy-signal CSV")
    parser.add_argument(
        "--tps-csv",
        help="Optional matching TPS transition-log CSV for state cross-check",
    )
    parser.add_argument(
        "--allowed-states",
        default="READY,BREAKOUT,TREND",
        help="Comma-separated states treated as allowed for strategy-filter comparison",
    )
    args = parser.parse_args()

    rows = load_rows(args.input)
    signal_rows = None
    signal_total = 0
    if args.signals_csv:
        signal_rows, signal_total = attach_signals(load_signals(args.signals_csv), rows)
    tps_rows = None
    if args.tps_csv:
        tps_rows = join_tps_states(rows, load_tps_transitions(args.tps_csv))
    allowed_states = {canonical_state(value) for value in args.allowed_states.split(",") if value}
    report = render_report(
        rows,
        args.horizons,
        signal_rows,
        signal_total,
        allowed_states,
        tps_rows,
    )

    if args.out:
        Path(args.out).write_text(report, encoding="utf-8")
        print(f"Wrote {args.out}")
    else:
        print(report)


if __name__ == "__main__":
    main()
