#!/usr/bin/env python3
"""
Compression Fractal Release — log analyzer.

Parses TradingView Pine-log CSV exports (column "Nachricht"/"Datum") containing
CFR BREAK and CFR BAR rows, and derives data-driven regime thresholds so the
base/correction/clean classification is calibrated to the actual symbol/TF
distribution instead of fixed defaults.

Usage:
    python3 scripts/analyze_cfr.py <logdir> [--out report.md]

Emit the rows by enabling "Log Breaks" and "Log Every Bar (distribution)" in the
indicator's Debug group, then export the Pine logs to CSV into <logdir>.

Row formats:
    CFR BAR   cmp= eff= fd= chop= coil= dyn= htf= regime=
    CFR BREAK dir= type= htf= score= coil= dyn= cmp= eff= fd= chop= regime= wasBase= reason=
"""
import argparse
import csv
import os
import re
import sys
from collections import Counter, defaultdict

MARKERS = ("CFR BREAK", "CFR BAR")


def parse_kv(msg: str) -> dict:
    msg = re.sub(r'(\w+=)(\d{1,3}(?:,\d{3})+)', lambda m: m.group(1) + m.group(2).replace(",", ""), msg)
    return dict(re.findall(r'(\w+)=([^|\s]+)', msg))


def load_rows(logdir: str) -> dict:
    events = defaultdict(list)
    found_csv = False
    for fname in sorted(os.listdir(logdir)):
        if not fname.endswith(".csv"):
            continue
        found_csv = True
        with open(os.path.join(logdir, fname)) as f:
            for row in csv.DictReader(f):
                msg = row.get("Nachricht") or row.get("Message") or ""
                for marker in MARKERS:
                    if marker in msg:
                        kv = parse_kv(msg)
                        kv["_ts"] = row.get("Datum") or row.get("Time") or ""
                        events[marker].append(kv)
                        break
    if not found_csv:
        sys.exit(f"No CSV files in {logdir}")
    return events


def fnum(rows, key):
    out = []
    for r in rows:
        v = r.get(key)
        if v is None:
            continue
        try:
            out.append(float(v))
        except ValueError:
            pass
    return out


def pct(vals, q):
    if not vals:
        return float("nan")
    s = sorted(vals)
    i = (len(s) - 1) * q
    lo, hi = int(i), min(int(i) + 1, len(s) - 1)
    return s[lo] + (s[hi] - s[lo]) * (i - lo)


def dist_line(name, vals):
    if not vals:
        return f"| {name} | — | — | — | — | — | — |"
    return (f"| {name} | {min(vals):.2f} | {pct(vals,0.25):.2f} | {pct(vals,0.50):.2f} | "
            f"{pct(vals,0.75):.2f} | {pct(vals,0.90):.2f} | {max(vals):.2f} |")


def report(events) -> str:
    bars = events.get("CFR BAR", [])
    breaks = events.get("CFR BREAK", [])
    src = bars if bars else breaks
    src_label = "CFR BAR (per-bar)" if bars else "CFR BREAK only (enable 'Log Every Bar' for full distribution)"

    L = []
    L.append("# Compression Fractal Release — Log Analysis\n")
    L.append(f"Bars: {len(bars)} · Breaks: {len(breaks)} · Distribution source: {src_label}\n")

    # 1 · Metric distribution
    L.append("## 1 · Metric distribution\n")
    L.append("| Metric | min | p25 | p50 | p75 | p90 | max |")
    L.append("|---|---|---|---|---|---|---|")
    for key, label in [("cmp", "Compression"), ("eff", "Efficiency"), ("fd", "Fractal Dim"),
                       ("chop", "Choppiness"), ("coil", "Coil"), ("dyn", "Release Dyn")]:
        L.append(dist_line(label, fnum(src, key)))
    L.append("")

    # 2 · Regime occupancy
    if src and any("regime" in r for r in src):
        reg = Counter(r.get("regime", "?") for r in src)
        tot = sum(reg.values())
        L.append("## 2 · Regime occupancy\n")
        L.append("| Regime | bars | share |")
        L.append("|---|---|---|")
        for name in ("clean", "corr", "base", "mixed"):
            n = reg.get(name, 0)
            L.append(f"| {name} | {n} | {100*n/tot:.0f}% |")
        L.append("")
        if 100 * reg.get("base", 0) / tot > 50:
            L.append("> ⚠ `base` occupies >50% of bars — the regime thresholds are mis-calibrated "
                     "for this symbol; the background and the Base-Break precondition carry little information.\n")

    # 3 · Break reasons
    if breaks:
        L.append("## 3 · Break outcomes\n")
        by_reason = Counter(r.get("reason", "?") for r in breaks)
        L.append("| reason | count | share |")
        L.append("|---|---|---|")
        for reason, n in by_reason.most_common():
            L.append(f"| {reason} | {n} | {100*n/len(breaks):.0f}% |")
        L.append("")
        # ok breaks by type/direction
        ok = [r for r in breaks if r.get("reason") == "ok"]
        if ok:
            by_td = Counter((r.get("type", "?"), r.get("dir", "?")) for r in ok)
            L.append("Fired (reason=ok) by type/direction: " +
                     ", ".join(f"{t}/{d}={n}" for (t, d), n in by_td.most_common()) + "\n")

    # 4 · Suggested data-driven thresholds (terciles → balanced clean/corr/base)
    cmp_v, eff_v = fnum(src, "cmp"), fnum(src, "eff")
    if cmp_v and eff_v:
        L.append("## 4 · Suggested regime thresholds (terciles)\n")
        L.append("Set so clean/correction/base are roughly balanced on this symbol/TF:\n")
        L.append(f"- High Complexity Threshold ≈ **{pct(cmp_v,0.66):.0f}** (current default 62)")
        L.append(f"- Low Complexity Threshold  ≈ **{pct(cmp_v,0.33):.0f}** (current default 48)")
        L.append(f"- High Efficiency Threshold ≈ **{pct(eff_v,0.66):.0f}** (current default 42)")
        L.append(f"- Low Efficiency Threshold  ≈ **{pct(eff_v,0.33):.0f}** (current default 25)")
        L.append("")
        L.append("> These calibrate the *background regime + Base-Break precondition* only. "
                 "Signal quality (whether the fired releases are profitable) needs an R-outcome "
                 "backtest — the log cannot measure forward returns.\n")

    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("logdir")
    ap.add_argument("--out")
    args = ap.parse_args()
    out = report(load_rows(args.logdir))
    if args.out:
        with open(args.out, "w") as f:
            f.write(out)
        print(f"Wrote {args.out}")
    else:
        print(out)


if __name__ == "__main__":
    main()
