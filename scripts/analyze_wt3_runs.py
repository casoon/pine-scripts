#!/usr/bin/env python3
"""Analyze WaveTrend v3 TradingView exports and Pine logs.

Usage:
    python3 scripts/analyze_wt3_runs.py testdata/test16

The script pairs Pine DECISION log rows with TradingView closed trades by count,
then summarizes which setup/filter components admitted winners or losers and
which components most often blocked triggers.
"""

from __future__ import annotations

import argparse
import csv
import math
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pandas as pd


KEY_RE = re.compile(r"([A-Za-z][A-Za-z0-9_]*)=([^ |]+)")


@dataclass
class LogRun:
    path: Path
    rows: list[dict[str, Any]]
    decisions: list[dict[str, Any]]
    blocked: list[dict[str, Any]]


@dataclass
class TradeRun:
    path: Path
    exits: pd.DataFrame


def parse_bool(value: Any) -> Any:
    if value == "true":
        return True
    if value == "false":
        return False
    return value


def parse_number(value: Any) -> Any:
    if not isinstance(value, str):
        return value
    if "/" in value:
        return value
    try:
        return float(value)
    except ValueError:
        return value


def parse_ctx(value: Any) -> tuple[float | None, float | None]:
    if not isinstance(value, str) or "/" not in value:
        return None, None
    left, right = value.split("/", 1)
    try:
        return float(left), float(right)
    except ValueError:
        return None, None


def parse_message(date: str, msg: str, source: Path) -> dict[str, Any]:
    direction = "LONG" if " LONG " in f" {msg} " else "SHORT" if " SHORT " in f" {msg} " else ""
    status = "DECISION" if " DECISION " in f" {msg} " else "BLOCKED" if " BLOCKED " in f" {msg} " else ""
    parsed: dict[str, Any] = {
        "date": date,
        "direction": direction,
        "status": status,
        "source_log": source.name,
        "message": msg,
    }
    for key, raw in KEY_RE.findall(msg):
        parsed[key] = parse_number(parse_bool(raw))
    score, max_score = parse_ctx(parsed.get("ctxScore"))
    parsed["ctxScoreValue"] = score
    parsed["ctxScoreMax"] = max_score
    return parsed


def read_log(path: Path) -> LogRun:
    rows: list[dict[str, Any]] = []
    with path.open(newline="", encoding="utf-8-sig") as fh:
        for row in csv.DictReader(fh):
            msg = row.get("Nachricht") or row.get("Message") or ""
            if "WT3 " not in msg:
                continue
            parsed = parse_message(row.get("Datum") or row.get("Date") or "", msg, path)
            if parsed["status"]:
                rows.append(parsed)
    decisions = [r for r in rows if r["status"] == "DECISION"]
    blocked = [r for r in rows if r["status"] == "BLOCKED"]
    return LogRun(path=path, rows=rows, decisions=decisions, blocked=blocked)


def read_trades(path: Path) -> TradeRun | None:
    try:
        df = pd.read_excel(path, sheet_name="Liste der Trades")
    except Exception:
        return None
    if "Typ" not in df.columns or "G&V netto USD" not in df.columns:
        return None
    exits = df[df["Typ"].astype(str).str.contains("Ausstieg", na=False)].copy()
    exits = exits.reset_index(drop=True)
    return TradeRun(path=path, exits=exits)


def profit_factor(pnls: pd.Series) -> float:
    wins = pnls[pnls > 0].sum()
    losses = -pnls[pnls < 0].sum()
    if losses == 0:
        return math.inf if wins > 0 else 0.0
    return float(wins / losses)


def summarize_group(df: pd.DataFrame, group_cols: list[str]) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame()
    rows: list[dict[str, Any]] = []
    grouped = df.groupby(group_cols, dropna=False)
    for keys, g in grouped:
        if not isinstance(keys, tuple):
            keys = (keys,)
        pnls = g["pnl"].astype(float)
        row = {col: key for col, key in zip(group_cols, keys)}
        row.update(
            {
                "trades": int(len(g)),
                "net": round(float(pnls.sum()), 2),
                "win_rate": round(float((pnls > 0).mean() * 100), 1),
                "avg": round(float(pnls.mean()), 2),
                "pf": "inf" if math.isinf(profit_factor(pnls)) else round(profit_factor(pnls), 3),
            }
        )
        rows.append(row)
    return pd.DataFrame(rows).sort_values(["net", "trades"], ascending=[False, False])


def pair_runs(logs: list[LogRun], trades: list[TradeRun]) -> list[tuple[LogRun, TradeRun | None]]:
    by_count: dict[int, list[TradeRun]] = {}
    for tr in trades:
        by_count.setdefault(len(tr.exits), []).append(tr)
    used: set[Path] = set()
    pairs: list[tuple[LogRun, TradeRun | None]] = []
    for log in logs:
        candidates = [tr for tr in by_count.get(len(log.decisions), []) if tr.path not in used]
        if len(candidates) == 1:
            used.add(candidates[0].path)
            pairs.append((log, candidates[0]))
        else:
            pairs.append((log, None))
    return pairs


def attach_pnl(log: LogRun, trades: TradeRun | None) -> pd.DataFrame:
    df = pd.DataFrame(log.decisions)
    if df.empty:
        return df
    if trades is None or len(trades.exits) != len(df):
        df["pnl"] = float("nan")
        df["trade_export"] = ""
        return df
    df["pnl"] = trades.exits["G&V netto USD"].astype(float).to_list()
    df["trade_export"] = trades.path.name
    return df


def blocker_columns(df: pd.DataFrame) -> list[str]:
    candidates = [
        "mtfOk",
        "STRUCT",
        "POC",
        "VOL",
        "ok",
        "loc",
        "rangeLoc",
        "swingLoc",
        "roomOk",
        "volOk",
        "pbOk",
        "pbTrend",
        "pbLoc",
    ]
    return [c for c in candidates if c in df.columns]


def print_table(title: str, df: pd.DataFrame, limit: int = 20) -> None:
    print(f"\n## {title}")
    if df.empty:
        print("(no rows)")
        return
    print(df.head(limit).to_string(index=False))


def analyze(path: Path) -> None:
    logs = [read_log(p) for p in sorted(path.glob("*.csv"))]
    logs = [l for l in logs if l.rows]
    trades = [t for t in (read_trades(p) for p in sorted(path.glob("*.xlsx"))) if t is not None]

    print(f"# WT3 run analysis: {path}")
    print(f"logs={len(logs)} trade_exports={len(trades)}")

    all_decisions: list[pd.DataFrame] = []
    for log, trade in pair_runs(logs, trades):
        dec = attach_pnl(log, trade)
        all_decisions.append(dec)
        print(f"\n# Run: {log.path.name}")
        print(f"decisions={len(log.decisions)} blocked={len(log.blocked)} paired_export={trade.path.name if trade else 'UNPAIRED'}")
        if not dec.empty and "pnl" in dec and dec["pnl"].notna().any():
            pnls = dec["pnl"].astype(float)
            print(
                "net={:.2f} win_rate={:.1f}% pf={}".format(
                    pnls.sum(),
                    (pnls > 0).mean() * 100,
                    "inf" if math.isinf(profit_factor(pnls)) else round(profit_factor(pnls), 3),
                )
            )
            for cols in (["direction"], ["type"], ["direction", "type"], ["volOk"], ["pbOk"], ["rangeLoc"], ["swingLoc"]):
                if all(c in dec.columns for c in cols):
                    print_table("accepted by " + "/".join(cols), summarize_group(dec, cols), 12)

        blocked = pd.DataFrame(log.blocked)
        if not blocked.empty:
            cols = blocker_columns(blocked)
            rows = []
            for col in cols:
                false_count = int((blocked[col] == False).sum())  # noqa: E712
                if false_count:
                    rows.append({"blocked_component_false": col, "count": false_count, "share": round(false_count / len(blocked) * 100, 1)})
            print_table("blocked marginal reasons", pd.DataFrame(rows).sort_values("count", ascending=False) if rows else pd.DataFrame(), 20)
            combo_cols = [c for c in ["mtfOk", "ok", "loc", "roomOk", "volOk", "pbOk", "STRUCT", "POC", "VOL"] if c in blocked.columns]
            if combo_cols:
                combo = blocked.groupby(combo_cols, dropna=False).size().reset_index(name="count").sort_values("count", ascending=False)
                print_table("top blocked combinations", combo, 12)

    combined = pd.concat([d for d in all_decisions if not d.empty], ignore_index=True) if all_decisions else pd.DataFrame()
    if not combined.empty and "pnl" in combined and combined["pnl"].notna().any():
        print("\n# Combined accepted-decision diagnostics")
        for col in ["type", "direction", "volOk", "pbOk", "pbTrend", "pbLoc", "rangeLoc", "swingLoc", "STRUCT", "POC", "VOL", "mtfOk"]:
            if col in combined.columns:
                print_table(f"combined by {col}", summarize_group(combined, [col]), 12)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=Path)
    args = parser.parse_args()
    analyze(args.path)


if __name__ == "__main__":
    main()
