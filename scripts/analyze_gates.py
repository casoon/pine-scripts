#!/usr/bin/env python3
"""
Gate effectiveness analyzer for WaveTrend v4 strategy logs.

Usage:
    python3 scripts/analyze_gates.py testdata/testXX [--out report.md]

Reads WT4 PIVOT_OPP, WT4 BLOCKED, WT4 ENTRY, WT4 REAL EXIT from CSV logs
and produces a structured gate effectiveness report.

Key questions answered:
  1. Signal coverage  — what % of pivot opportunities had a WT signal?
  2. Gate cost        — what % of WT signals does each gate block?
  3. Blocked quality  — were the blocked signals good? (cross-matched vs pivot proximity)
  4. Entry quality    — WR / avgR of actual entries, broken down by TF and direction
"""

import sys
import csv
import re
import os
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path

GATES = ["srsi", "cooldown", "session", "dateRange", "tf", "atrRank",
         "bbExpansion", "chop", "pivotBars", "pivotDist", "sweep",
         "gateA", "gateB", "gateB2", "gateC", "gateD", "gateG", "gateH", "gateI"]

NEAR_PIV_THRESHOLD = 10  # bars — signals within this distance count as "near pivot"
PIV_LEN = 5              # default pivot confirmation lookback (bars)
TF_SECONDS = {"15": 900, "60": 3600, "240": 14400, "1D": 86400}
SL_MULT = 1.5            # must match strategy SL multiplier


def parse_kv(msg: str) -> dict:
    # Strip thousand separators from numbers before parsing
    msg = re.sub(r'(\w+=)(\d{1,3}(?:,\d{3})+)', lambda m: m.group(1) + m.group(2).replace(",", ""), msg)
    return dict(re.findall(r'(\w+)=([^|\s]+)', msg))


def load_logs(testdir: str) -> dict:
    """Load all log events from CSV files in testdir, keyed by event type."""
    events = defaultdict(list)
    for fname in sorted(os.listdir(testdir)):
        if not fname.endswith(".csv"):
            continue
        with open(f"{testdir}/{fname}") as f:
            for row in csv.DictReader(f):
                msg = row.get("Nachricht", "")
                ts = row.get("Datum", "")
                # "WT4 ENTRY FILL" must be checked before "WT4 ENTRY" (substring match)
                for marker in ("WT4 PIVOT", "WT4 BLOCKED", "WT4 ENTRY FILL", "WT4 ENTRY", "WT4 REAL EXIT", "WT4 STRUCT_WT"):
                    if marker in msg:
                        kv = parse_kv(msg)
                        kv["_ts"] = ts
                        events[marker].append(kv)
                        break
    return events


def pct(n, total):
    return f"{100*n/total:.0f}%" if total else "—"


def fmt_r(rs):
    if not rs:
        return "—"
    avg = sum(rs) / len(rs)
    wr = sum(1 for r in rs if r > 0) / len(rs)
    return f"WR={100*wr:.0f}% avgR={avg:+.2f} n={len(rs)}"


def parse_ts(s: str):
    if not s:
        return None
    s = re.sub(r'\.\d+', '', s)  # strip milliseconds
    try:
        return datetime.fromisoformat(s)
    except Exception:
        return None


def pivot_to_pivot_baseline(pivots: list, entries: list, exits: list, tfs: list) -> list[str]:
    """
    Pair consecutive opposite-direction confirmed pivots per TF.
    Each Low→High pair = theoretical long, High→Low = theoretical short.
    R = price_move / (SL_MULT × atr_at_entry_pivot).
    Cross-reference with actual entries to measure capture rate.
    """
    out = []
    out.append("## 0. Pivot-to-Pivot Baseline (theoretical vs. actual)\n")
    out.append("Each consecutive Low↔High pivot pair = one theoretical trade.")
    out.append(f"R = move / ({SL_MULT}×ATR at entry pivot).  Capture = strategy entry within window.\n")
    out.append(f"{'TF':<6} {'Dir':<7} {'Opps':>6} {'AvgR':>7} {'SumR':>8} {'Caught':>7} {'CaptR%':>8} {'Caught avgR':>12}")
    out.append("-" * 75)

    total_opps = total_r = total_caught = total_caught_r = 0

    for tf in tfs:
        bar_sec = TF_SECONDS.get(tf, 3600)
        confirm_delay = timedelta(seconds=PIV_LEN * bar_sec)

        tf_pivots = sorted(
            [p for p in pivots if p.get("tf") == tf],
            key=lambda p: p.get("_ts", "")
        )
        tf_entries = [e for e in entries if e.get("tf") == tf]
        entry_ts_by_dir = defaultdict(list)
        for e in tf_entries:
            t = parse_ts(e.get("_ts", ""))
            if t:
                entry_ts_by_dir[e.get("dir", "")].append(t)
        for d in entry_ts_by_dir:
            entry_ts_by_dir[d].sort()

        theoretical = []
        for i in range(len(tf_pivots) - 1):
            p1, p2 = tf_pivots[i], tf_pivots[i + 1]
            d1, d2 = p1.get("dir"), p2.get("dir")
            if d1 == d2:
                continue
            try:
                atr = float(p1.get("pivAtr", "nan"))
                if atr != atr or atr <= 0:  # nan or zero
                    continue
                if d1 == "long" and d2 == "short":
                    move = float(p2["pivHigh"]) - float(p1["pivLow"])
                    trade_dir = "long"
                else:
                    move = float(p1["pivHigh"]) - float(p2["pivLow"])
                    trade_dir = "short"
                if move <= 0:
                    continue
                r = move / (SL_MULT * atr)
                # Entry window: pivot bar = confirm_ts - confirm_delay; window ends at p2 confirm
                t1 = parse_ts(p1["_ts"])
                t2 = parse_ts(p2["_ts"])
                if t1 is None or t2 is None:
                    continue
                window_start = t1 - confirm_delay
                theoretical.append((trade_dir, r, window_start, t2))
            except (KeyError, ValueError):
                continue

        for dir_ in ("long", "short"):
            opps = [(r, ws, we) for d, r, ws, we in theoretical if d == dir_]
            if not opps:
                continue
            rs = [r for r, _, _ in opps]
            avg_r = sum(rs) / len(rs)
            sum_r = sum(rs)

            e_times = entry_ts_by_dir.get(dir_, [])
            caught_rs = []
            for r, ws, we in opps:
                hit = any(ws <= t <= we for t in e_times)
                if hit:
                    caught_rs.append(r)

            c_avg = sum(caught_rs) / len(caught_rs) if caught_rs else 0
            out.append(
                f"{tf:<6} {dir_:<7} {len(opps):>6} {avg_r:>7.2f} {sum_r:>8.1f}"
                f" {len(caught_rs):>7} {pct(len(caught_rs), len(opps)):>8}"
                f"  {c_avg:>+.2f}"
            )
            total_opps   += len(opps)
            total_r      += sum_r
            total_caught += len(caught_rs)
            total_caught_r += sum(caught_rs)

    out.append("-" * 75)
    c_avg_total = total_caught_r / total_caught if total_caught else 0
    total_avg_r = total_r / total_opps if total_opps else 0
    out.append(
        f"{'ALL':<6} {'':7} {total_opps:>6} {total_avg_r:>7.2f} {total_r:>8.1f}"
        f" {total_caught:>7} {pct(total_caught, total_opps):>8}"
        f"  {c_avg_total:>+.2f}"
    )
    out.append("")
    return out


def analyze(testdir: str) -> str:
    events = load_logs(testdir)
    pivots      = events["WT4 PIVOT"]
    blocked     = events["WT4 BLOCKED"]
    entries     = events["WT4 ENTRY"]
    entry_fills = events["WT4 ENTRY FILL"]
    exits       = events["WT4 REAL EXIT"]

    all_events = pivots + blocked + entries + exits
    tfs = sorted({e.get("tf", "?") for e in all_events if e.get("tf")})
    out = []

    out.append(f"# Gate Analysis — {Path(testdir).name}\n")
    out.append(f"Events: {len(pivots)} pivot_ref | {len(blocked)} blocked | {len(entries)} entry_signals | {len(entry_fills)} entry_fills | {len(exits)} exits\n")

    out.extend(pivot_to_pivot_baseline(pivots, entries, exits, tfs))

    # Pre-build block_events_by_gate early — used in sections 2, 4, 5
    block_events_by_gate = defaultdict(list)
    for b in blocked:
        block_events_by_gate[b.get("reason", "?")].append(b)

    # Total WT crosses = blocked + entries (both are downstream of a raw WT cross)
    total_fired = len(blocked) + len(entries)
    passed = len(entries)

    # ── 1. Signal coverage per TF ─────────────────────────────────────────────
    out.append("## 1. Signal Coverage (WT cross → passed all gates?)\n")
    out.append(f"{'TF':<6} {'Fired':>7} {'Blocked':>9} {'Passed':>8} {'Pass%':>7} {'Dir long':>10} {'Dir short':>11}")
    out.append("-" * 65)
    for tf in tfs:
        bl_tf  = [b for b in blocked if b.get("tf") == tf]
        en_tf  = [e for e in entries if e.get("tf") == tf]
        fired_tf = len(bl_tf) + len(en_tf)
        long_  = sum(1 for e in en_tf if e.get("dir") == "long")
        short_ = sum(1 for e in en_tf if e.get("dir") == "short")
        out.append(f"{tf:<6} {fired_tf:>7} {len(bl_tf):>9} {len(en_tf):>8} {pct(len(en_tf), fired_tf):>7} {long_:>10} {short_:>11}")
    out.append("")

    # ── 2. Gate cost (blocked per gate, using WT4 BLOCKED log) ───────────────
    out.append("## 2. Gate Cost (first-blocking gate per WT4 BLOCKED event)\n")
    out.append(f"Total WT crosses (blocked + entries): {total_fired}\n")
    out.append(f"{'Gate':<14} {'Blocked':>8} {'% of fired':>12} {'TF breakdown'}")
    out.append("-" * 60)
    for gate in GATES:
        bs = block_events_by_gate.get(gate, [])
        if not bs:
            continue
        tf_counts = ", ".join(f"{tf}:{sum(1 for b in bs if b.get('tf')==tf)}" for tf in tfs if any(b.get('tf')==tf for b in bs))
        out.append(f"{gate:<14} {len(bs):>8} {pct(len(bs), total_fired):>12}   [{tf_counts}]")
    out.append(f"{'(passed)':<14} {passed:>8} {pct(passed, total_fired):>12}")
    out.append("")

    # ── 3. Entry quality (actual trades) ─────────────────────────────────────
    out.append("## 3. Entry Quality (actual trades)\n")
    out.append(f"{'TF':<6} {'Dir':<7} {'Trades':>7} {'Result'}")
    out.append("-" * 55)
    exit_rs = defaultdict(list)
    for e in exits:
        try:
            exit_rs[(e.get("tf"), e.get("dir"))].append(float(e["R"]))
        except (KeyError, ValueError):
            pass
    exits_by_entry = {k: (sum(v)/len(v), len(v)) for k, v in exit_rs.items()}  # reuse for summary
    for tf in tfs:
        for dir_ in ("long", "short"):
            rs = exit_rs.get((tf, dir_), [])
            if rs:
                out.append(f"{tf:<6} {dir_:<7} {len(rs):>7}   {fmt_r(rs)}")
    out.append("")

    # ── 4. Blocked quality per gate (BLOCKED log cross-check) ────────────────
    out.append("## 4. Blocked signal quality (WT4 BLOCKED log)\n")
    out.append(f"{'Gate':<14} {'Count':>6} {'TF':>5} {'Dir':>6}   {'Detail'}")
    out.append("-" * 65)
    for gate in GATES:
        bs = block_events_by_gate.get(gate, [])
        if not bs:
            continue
        for tf in tfs:
            for dir_ in ("long", "short"):
                sub = [b for b in bs if b.get("tf") == tf and b.get("dir") == dir_]
                if sub:
                    # Summarize context: avg atrRank, chop, bbWidthRank at block time
                    try:
                        avg_atr = sum(float(b["atrRank"]) for b in sub if "atrRank" in b) / len(sub)
                        avg_chop = sum(float(b["chop"]) for b in sub if "chop" in b) / len(sub)
                        ctx = f"atrRank={avg_atr:.0f} chop={avg_chop:.0f}"
                    except Exception:
                        ctx = ""
                    out.append(f"{gate:<14} {len(sub):>6} {tf:>5} {dir_:>6}   {ctx}")
    out.append("")

    # ── 5. Pivot proximity quality per gate ──────────────────────────────────
    out.append("## 5. Gate Quality — Near-Pivot vs Far-from-Pivot Blocks\n")
    out.append(f"'Near pivot' = barsSinceLowPiv or barsSinceHighPiv ≤ {NEAR_PIV_THRESHOLD} bars at block time.\n")
    out.append(f"{'Gate':<14} {'Total':>6} {'Near':>6} {'%Near':>7} {'Far':>6} {'%Far':>7}   {'interpretation'}")
    out.append("-" * 75)

    def piv_bars_for(ev: dict) -> int | None:
        """Return the direction-appropriate pivot-bars field, or None if absent."""
        dir_ = ev.get("dir", "")
        key = "lowPivBars" if dir_ == "long" else "highPivBars"
        # Also accept barsSinceLowPiv / barsSinceHighPiv
        for candidate in (key, "barsSinceLowPiv" if dir_ == "long" else "barsSinceHighPiv"):
            if candidate in ev:
                try:
                    return int(float(ev[candidate]))
                except ValueError:
                    pass
        return None

    for gate in GATES:
        bs = block_events_by_gate.get(gate, [])
        if not bs:
            continue
        with_data = [b for b in bs if piv_bars_for(b) is not None]
        if not with_data:
            out.append(f"{gate:<14} {len(bs):>6}   (no pivot-bar data in logs)")
            continue
        near = sum(1 for b in with_data if piv_bars_for(b) <= NEAR_PIV_THRESHOLD)
        far  = len(with_data) - near
        interp = "blocks mostly QUALITY setups ⚠" if near / len(with_data) > 0.5 else "blocks mostly NOISE ✓"
        out.append(f"{gate:<14} {len(with_data):>6} {near:>6} {pct(near, len(with_data)):>7} {far:>6} {pct(far, len(with_data)):>7}   {interp}")
    out.append("")

    # ── 6. Summary table ──────────────────────────────────────────────────────
    out.append("## 6. Summary\n")
    out.append(f"- Pivot reference events logged: {len(pivots)}")
    out.append(f"- Total WT crosses (blocked + entries): {total_fired}")
    out.append(f"- Signals that passed all gates: {pct(passed, total_fired)} ({passed}/{total_fired})")
    out.append(f"- Entry signals (order submission): {len(entries)}")
    fills_long  = sum(1 for f in entry_fills if f.get("dir") == "long")
    fills_short = sum(1 for f in entry_fills if f.get("dir") == "short")
    delta = len(entry_fills) - len(exits)
    out.append(f"- Entry fills:   {len(entry_fills)} (long={fills_long} short={fills_short})")
    out.append(f"- Real exits:    {len(exits)}")
    out.append(f"- Fill/Exit delta: {delta:+d}  {'✓ 1:1' if abs(delta) <= 3 else '⚠ mismatch — open trades or double fills'}")
    fill_ids  = {int(float(f["tradeId"])) for f in entry_fills if "tradeId" in f}
    exit_ids  = {int(float(e["tradeId"])) for e in exits       if "tradeId" in e}
    fills_only = sorted(fill_ids - exit_ids)
    exits_only = sorted(exit_ids - fill_ids)
    if fills_only:
        out.append(f"- Fills with no exit:  {len(fills_only)} — first 10: {fills_only[:10]}")
    if exits_only:
        out.append(f"- Exits with no fill:  {len(exits_only)} — first 10: {exits_only[:10]}")
    all_rs = [r for rs in exit_rs.values() for r in rs]
    out.append(f"- Entry quality (all TF): {fmt_r(all_rs)}")
    out.append("")
    out.append("### Gate impact ranking (by blocked signals)\n")
    gate_rank = sorted(block_events_by_gate.items(), key=lambda x: -len(x[1]))
    for gate, bs in gate_rank:
        out.append(f"  {gate:<14} blocks {len(bs):>4} signals ({pct(len(bs), total_fired)})")

    # ── 7. WT-cross exit probe ────────────────────────────────────────────────
    struct_wt = events.get("WT4 STRUCT_WT", [])
    if struct_wt:
        out.append("\n## 7. WT-Cross Exit Probe (diagnostic)\n")
        out.append("Signal: wt1 crosses wt2 in OB/OS zone (candidate for WT-based struct exit).")
        out.append("'Aligned' = signal direction matches open trade direction.\n")
        out.append(f"{'TF':<6} {'Dir':<12} {'Total':>7} {'InTrade':>8} {'Aligned':>8}  R distribution (aligned)")
        out.append("-" * 78)
        buckets = [(-999, 0, "<0R"), (0, 1, "0–1R"), (1, 2, "1–2R"), (2, 3, "2–3R"), (3, 999, "3R+")]
        for tf in ["15", "60", "240", "1D"]:
            for d in ["long_exit", "short_exit"]:
                evs = [e for e in struct_wt if e.get("tf") == tf and e.get("dir") == d]
                if not evs:
                    continue
                in_trade = [e for e in evs if e.get("inTrade") == "1"]
                trade_dir = "long" if d == "long_exit" else "short"
                aligned   = [e for e in in_trade if e.get("tradeDir") == trade_dir]
                rs = []
                for e in aligned:
                    try:
                        rs.append(float(e["currentR"]))
                    except (KeyError, ValueError):
                        pass
                dist = ""
                if rs:
                    parts = []
                    for lo, hi, label in buckets:
                        n = sum(1 for r in rs if lo <= r < hi)
                        if n:
                            parts.append(f"{label}:{n}")
                    dist = "  " + " | ".join(parts)
                out.append(f"{tf:<6} {d:<12} {len(evs):>7} {len(in_trade):>8} {len(aligned):>8}{dist}")
        out.append("")

    return "\n".join(out)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 scripts/analyze_gates.py testdata/testXX [--out report.md]")
        sys.exit(1)

    testdir = sys.argv[1]
    out_path = None
    if "--out" in sys.argv:
        idx = sys.argv.index("--out")
        out_path = sys.argv[idx + 1]

    report = analyze(testdir)

    if out_path:
        with open(out_path, "w") as f:
            f.write(report)
        print(f"Report written to {out_path}")
    else:
        print(report)
