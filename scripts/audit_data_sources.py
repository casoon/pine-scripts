#!/usr/bin/env python3
"""Audit aller .pine-Dateien gegen DATA_VALIDITY.md.

Mechanischer Scan: findet Datenquellen-Nutzung (Volumen, volumenabgeleitete TA,
Pseudo-Orderflow, Cross-Symbol-Requests, OI) und bewertet, ob ein echter
Validitäts-Guard vorhanden ist.

    python3 scripts/audit_data_sources.py [--root .] [--out DATA_VALIDITY_AUDIT.md]

Der Scanner urteilt nicht — er priorisiert für die Einzelfallprüfung.
"""

import argparse
import re
from collections import Counter
from pathlib import Path

# ---------------------------------------------------------------- Muster

VOLUME_TA = {
    "ta.vwap": "VWAP",
    "ta.obv": "OBV",
    "ta.mfi": "MFI",
    "ta.vwma": "VWMA",
    "ta.cmf": "CMF",
    "ta.accdist": "A/D",
    "ta.pvt": "PVT",
    "ta.nvi": "NVI",
    "ta.pvi": "PVI",
    "ta.wad": "WAD",
    "ta.iii": "III",
    "ta.wvad": "WVAD",
}

# Bezeichner, die echten Orderflow behaupten
ORDERFLOW_NAMES = re.compile(
    r"\b(cvd|delta|buy_?vol\w*|sell_?vol\w*|buy(ing)?_?press\w*|sell(ing)?_?press\w*|"
    r"bid_?vol\w*|ask_?vol\w*|absorption|aggressor)\b",
    re.IGNORECASE,
)

# konstruiertes Vorzeichen-Volumen: Volumen wird mit einer Richtungsgröße
# vorzeichenbehaftet gemacht und damit implizit als Orderflow interpretiert.
SIGNED_VOLUME = re.compile(
    # Ternär ±volume  ->  close > open ? volume : -volume
    r"\?[^\n:]{0,70}\bn?z?\(?\s*volume\b[^\n]{0,70}:[^\n]{0,50}-\s*n?z?\(?\s*volume\b"
    # volume * Close-Location / Richtungsfaktor
    r"|\bvolume\s*\*\s*\(?\s*(clv|closeloc\w*|closepos\w*|close\s*-|open\s*-)"
    r"|\b(clv|closeloc\w*|closepos\w*)\s*\*\s*n?z?\(?\s*volume\b"
    r"|\(\s*close\s*-[^\n]{0,40}\)\s*\*\s*n?z?\(?\s*volume\b"
    # (2 * clv - 1) * volume
    r"|\(\s*2(\.\d+)?\s*\*[^\n]{0,50}-\s*1(\.\d+)?\s*\)\s*\*\s*n?z?\(?\s*volume\b",
    re.IGNORECASE,
)

VOLUME_TOKEN = re.compile(r"(?<![\w.])volume(?![\w])")
GUARD_REAL = re.compile(r"syminfo\.volumetype")
GUARD_WEAK = re.compile(r"n[az]\(\s*volume\s*\)")
OI_TOKEN = re.compile(r"_OI[\"']|request\.footprint")
DATA_CONTRACT = re.compile(r"^//\s*Data Contract:", re.MULTILINE)

# Rahmenbedingungen (DATA_VALIDITY.md §9)
REQUEST_CALL = re.compile(r"request\.[a-z_]+\s*\(")
IS_STRATEGY = re.compile(r"^\s*strategy\s*\(", re.MULTILINE)
CHART_TYPE_GUARD = re.compile(r"chart\.is_[a-z]+")
CALC_EVERY_TICK = re.compile(r"calc_on_every_tick\s*=\s*true")
REQUEST_BUDGET_WARN = 25

# request.security(<symbol>, ...) — erstes Argument einsammeln
SECURITY_CALL = re.compile(r"request\.security(?:_lower_tf)?\s*\(\s*([^,\n)]+)")
OWN_SYMBOL = re.compile(r"syminfo\.(tickerid|ticker|main_tickerid)")

# Bedingungs-/Gate-Kontext: Volumen entscheidet über einen Bool
GATE_CONTEXT = re.compile(
    r"(?<![\w.])volume(?![\w])[^\n]{0,80}(>=|<=|>|<)"
    r"|(>=|<=|>|<)[^\n]{0,40}(?<![\w.])volume(?![\w])"
)


def strip_comments(text: str) -> str:
    """Entfernt //-Kommentare, respektiert String-Literale. Zeilenanzahl bleibt gleich."""
    out = []
    for line in text.split("\n"):
        res, i, quote = [], 0, None
        while i < len(line):
            ch = line[i]
            if quote:
                if ch == "\\":
                    res.append(line[i : i + 2])
                    i += 2
                    continue
                if ch == quote:
                    quote = None
                res.append(ch)
            elif ch in "\"'":
                quote = ch
                res.append(ch)
            elif ch == "/" and i + 1 < len(line) and line[i + 1] == "/":
                break
            else:
                res.append(ch)
            i += 1
        out.append("".join(res))
    return "\n".join(out)


def strip_strings(code: str) -> str:
    """Ersetzt String-Inhalte durch Leerzeichen — Tooltips/Titel sind kein Code."""
    out, i, quote = [], 0, None
    while i < len(code):
        ch = code[i]
        if quote:
            if ch == "\\":
                out.append("  ")
                i += 2
                continue
            if ch == quote:
                quote = None
                out.append(ch)
            else:
                out.append("\n" if ch == "\n" else " ")
        elif ch in "\"'":
            quote = ch
            out.append(ch)
        else:
            out.append(ch)
        i += 1
    return "".join(out)


def lines_matching(code: str, pattern) -> list:
    hits = []
    for n, line in enumerate(code.split("\n"), 1):
        if pattern.search(line):
            hits.append((n, line.strip()[:110]))
    return hits


# ---------------------------------------------------------------- Analyse


def analyse(path: Path, root: Path) -> dict:
    raw = path.read_text(encoding="utf-8", errors="replace")
    code = strip_comments(raw)

    vol_hits = lines_matching(code, VOLUME_TOKEN)
    ta_hits = {}
    for fn, label in VOLUME_TA.items():
        h = lines_matching(code, re.compile(re.escape(fn) + r"\s*\("))
        if h:
            ta_hits[label] = h

    bare = strip_strings(code)
    signed = lines_matching(bare, SIGNED_VOLUME)
    of_names = [
        (n, t) for n, t in lines_matching(bare, ORDERFLOW_NAMES) if VOLUME_TOKEN.search(t)
    ]

    cross = []
    for m in SECURITY_CALL.finditer(code):
        arg = m.group(1).strip()
        if OWN_SYMBOL.search(arg):
            continue
        if arg in ('""', "''"):  # leeres Symbol = Chart-Symbol
            continue
        line = code[: m.start()].count("\n") + 1
        cross.append((line, arg[:70]))

    guard_real = bool(GUARD_REAL.search(code))
    guard_weak = bool(GUARD_WEAK.search(code))
    gate_ctx = bool(GATE_CONTEXT.search(bare)) if vol_hits else False
    contract = bool(DATA_CONTRACT.search(raw))
    oi = lines_matching(code, OI_TOKEN)

    findings = []
    priority = 4

    if ta_hits and not guard_real:
        names = ", ".join(sorted(ta_hits))
        findings.append(
            f"volumenabgeleitete TA ohne `volumetype`-Guard: {names}"
        )
        priority = min(priority, 1)

    if signed:
        findings.append(
            "konstruiertes Vorzeichen-Volumen (Pseudo-Orderflow) — "
            f"{len(signed)} Stelle(n), z.B. Zeile {signed[0][0]}"
        )
        priority = min(priority, 1)

    if of_names:
        findings.append(
            "Bezeichner behauptet Orderflow (delta/cvd/buyVol/pressure) — "
            f"Zeile {of_names[0][0]}"
        )
        priority = min(priority, 1)

    if vol_hits and not guard_real:
        if gate_ctx:
            findings.append(
                f"`volume` in Bedingung/Gate ohne `volumetype`-Guard ({len(vol_hits)} Referenzen)"
            )
            priority = min(priority, 2)
        else:
            findings.append(
                f"`volume` verwendet ohne `volumetype`-Guard ({len(vol_hits)} Referenzen)"
            )
            priority = min(priority, 3)

    if guard_weak and not guard_real:
        findings.append("`nz(volume)`/`na(volume)` als vermeintlicher Guard — stellt keine Validität her")
        priority = min(priority, 2 if gate_ctx else 3)

    if cross:
        findings.append(
            f"Cross-Symbol-`request.security` ({len(cross)}x) — Referenzmarkt-Regeln prüfen: "
            + ", ".join(a for _, a in cross[:3])
        )
        priority = min(priority, 3)

    if oi:
        findings.append(f"OI-/Footprint-Zugriff ({len(oi)}x) — Instrumentbindung prüfen")
        priority = min(priority, 3)

    n_requests = len(REQUEST_CALL.findall(code))
    if n_requests >= REQUEST_BUDGET_WARN:
        findings.append(
            f"`request.*`-Budget: {n_requests} Aufrufe (Limit 40, Ultimate 64) — "
            "kein Spielraum für zusätzliche Referenzmarkt-Requests"
        )
        priority = min(priority, 3)

    if IS_STRATEGY.search(code):
        if not CHART_TYPE_GUARD.search(code):
            findings.append(
                "Strategie ohne Charttyp-Guard — auf Heikin Ashi/Renko sind die "
                "Backtest-Ergebnisse laut Pine-Doku ungültig"
            )
            priority = min(priority, 3)
        if CALC_EVERY_TICK.search(code):
            findings.append("`calc_on_every_tick=true` — Backtest nicht reproduzierbar")
            priority = min(priority, 2)

    if not contract:
        findings.append("kein `Data Contract`-Block im Header")

    if not findings:
        return {}

    if not vol_hits and not cross and not oi and not contract:
        priority = 4

    return {
        "path": str(path.relative_to(root)),
        "priority": priority,
        "vol_refs": len(vol_hits),
        "guard": "volumetype" if guard_real else ("nz/na" if guard_weak else "keiner"),
        "contract": contract,
        "gate": gate_ctx,
        "ta": sorted(ta_hits),
        "findings": findings,
    }


PRIO_LABEL = {
    1: "P1 — Überarbeiten/Umwidmen prüfen (Volumen tragend oder falsch benannt)",
    2: "P2 — Kennzeichnen (Volumen entscheidet Bedingungen, Guard fehlt/schwach)",
    3: "P3 — Prüfen (Volumen/Fremdsymbol vorhanden, Wirkung unklar)",
    4: "P4 — Nur Data Contract fehlt",
}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--out", default="DATA_VALIDITY_AUDIT.md")
    ap.add_argument("--include-archive", action="store_true")
    args = ap.parse_args()

    root = Path(args.root).resolve()
    files = sorted(root.rglob("*.pine"))
    if not args.include_archive:
        files = [f for f in files if "archive" not in f.parts and "temp" not in f.parts]

    results = [r for r in (analyse(f, root) for f in files) if r]
    results.sort(key=lambda r: (r["priority"], -r["vol_refs"], r["path"]))

    counts = Counter(r["priority"] for r in results)
    clean = len(files) - len(results)

    out = []
    out.append("# Data Validity Audit\n")
    out.append(
        f"Scan über {len(files)} `.pine`-Dateien gegen [`DATA_VALIDITY.md`](DATA_VALIDITY.md). "
        "Mechanischer Vorfilter — die Entscheidung (OK / Kennzeichnen / Überarbeiten / "
        "Umwidmen) trifft die Einzelfallprüfung nach Skill `instrument-data-validity`.\n"
    )
    out.append("| Priorität | Dateien |\n|---|---|")
    for p in (1, 2, 3, 4):
        out.append(f"| {PRIO_LABEL[p]} | {counts.get(p, 0)} |")
    out.append(f"| ohne Befund | {clean} |\n")

    for p in (1, 2, 3, 4):
        block = [r for r in results if r["priority"] == p]
        if not block:
            continue
        out.append(f"\n## {PRIO_LABEL[p]}\n")
        out.append("| Datei | vol-Refs | Guard | Contract | Befunde |")
        out.append("|---|---|---|---|---|")
        for r in block:
            fs = "<br>".join(r["findings"])
            out.append(
                f"| `{r['path']}` | {r['vol_refs']} | {r['guard']} | "
                f"{'ja' if r['contract'] else '—'} | {fs} |"
            )

    Path(args.out).write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"{len(results)} Dateien mit Befund von {len(files)} → {args.out}")
    for p in (1, 2, 3, 4):
        print(f"  P{p}: {counts.get(p, 0)}")


if __name__ == "__main__":
    main()
