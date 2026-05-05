#!/usr/bin/env python3
"""
Pivot-Window-basierte Gate-Auswertung.

Idee: Der ideale Trade geht von einem bestätigten Pivot zum nächsten gegenläufigen
Pivot. Innerhalb dieses Windows sollte unser tatsächlicher Trade liegen und 70–80%
des verfügbaren Wegs abdecken. Pro Window klassifizieren wir:

- IDEAL:     Trade existiert, coverage ≥ threshold, kein SL
- CUT_SHORT: Trade existiert, aber coverage < threshold ODER SL
- LOST:      kein Trade, aber Signals wurden geblockt
- NO_SIGNAL: keine Signals (kein Schuldiger)

Pro Gate berechnen wir die Disturbance-Rate:
    disturbance = blocks_in_(LOST or CUT_SHORT) / total_blocks
- < 10% → BEHALTEN
- 10–30% → JUSTIEREN
- > 30% → ENTFERNEN

Aufruf: python3 scripts/evaluate_pivot_coverage.py <testdir>
"""

import csv
import os
import sys
from collections import defaultdict, Counter

COVERAGE_THRESHOLD = 0.70    # ideal trade muss ≥ 70% der Pivot-Strecke abdecken
MIN_THEORETICAL_R  = 1.5     # nur Windows mit theoretischem R ≥ 1.5 zählen als "Opportunity"
ACTION_KEEP = 0.20
ACTION_TUNE = 0.40
SL_MULT     = 1.5            # muss zu strategy.slMult passen (für theoretical R)


def to_f(v):
    try:
        f = float(v)
        return None if f != f else f
    except Exception:
        return None


def to_i(v):
    try:
        return int(float(v))
    except Exception:
        return None


def load_events(testdir: str):
    events = defaultdict(list)
    for fname in sorted(os.listdir(testdir)):
        if not fname.startswith('pine-logs'):
            continue
        with open(os.path.join(testdir, fname)) as f:
            for row in csv.DictReader(f):
                msg = row.get('Nachricht', '')
                ts = row.get('Datum', '')
                # FILL must be checked before ENTRY (substring)
                for marker in (
                    'WT4 ENTRY FILL', 'WT4 ENTRY',
                    'WT4 REAL EXIT', 'WT4 BLOCKED', 'WT4 PIVOT',
                ):
                    if marker in msg:
                        kv = {}
                        for s in msg.split(' | '):
                            if '=' in s:
                                k, v = s.split('=', 1)
                                kv[k.strip()] = v.strip().replace(',', '')
                        kv['_ts'] = ts
                        events[marker].append(kv)
                        break
    return events


def build_pivot_windows(pivots: list, tf: str):
    """
    Build pivot-to-pivot windows per direction. Each window includes theoretical R
    (= span / (slMult * pivAtr)) so we can filter out tiny windows that aren't
    real opportunities.
    """
    tf_pivs = sorted(
        [p for p in pivots if p.get('tf') == tf and to_i(p.get('pivBar')) is not None],
        key=lambda p: to_i(p.get('pivBar')),
    )
    windows = []
    for i in range(len(tf_pivs) - 1):
        p1, p2 = tf_pivs[i], tf_pivs[i + 1]
        if p1.get('dir') == p2.get('dir'):
            continue
        if p1.get('dir') == 'long':
            d = 'long'
            price1 = to_f(p1.get('pivLow'))
            price2 = to_f(p2.get('pivHigh'))
        else:
            d = 'short'
            price1 = to_f(p1.get('pivHigh'))
            price2 = to_f(p2.get('pivLow'))
        b1 = to_i(p1.get('pivBar'))
        b2 = to_i(p2.get('pivBar'))
        pivAtr = to_f(p1.get('pivAtr'))
        if None in (price1, price2, b1, b2):
            continue
        span_price = abs(price2 - price1)
        theoretical_R = (span_price / (SL_MULT * pivAtr)) if pivAtr and pivAtr > 0 else None
        windows.append({
            'tf': tf, 'dir': d,
            'b1': b1, 'b2': b2,
            'p1': price1, 'p2': price2,
            'span_bars': b2 - b1,
            'span_price': span_price,
            'pivAtr': pivAtr,
            'theoretical_R': theoretical_R,
        })
    return windows


def classify_windows(windows: list, fills: list, exits: list, signals: list, blocks: list):
    """
    For each window, find related events and classify.
    Events are filtered by tf, dir, and bar range.
    """
    # index events by tf, dir for fast lookup
    fills_by = defaultdict(list)
    for f in fills:
        eb = to_i(f.get('bar'))
        if eb is not None:
            fills_by[(f.get('tf'), f.get('dir'))].append((eb, f))
    exits_by_id = {to_i(x.get('tradeId')): x for x in exits if to_i(x.get('tradeId')) is not None}

    sigs_by = defaultdict(list)
    for s in signals:
        eb = to_i(s.get('bar'))
        if eb is not None:
            sigs_by[(s.get('tf'), s.get('dir'))].append((eb, s))

    blks_by = defaultdict(list)
    for b in blocks:
        eb = to_i(b.get('bar'))
        if eb is not None:
            blks_by[(b.get('tf'), b.get('dir'))].append((eb, b))

    classified = []
    for w in windows:
        tf, d = w['tf'], w['dir']
        b1, b2 = w['b1'], w['b2']

        # Fills in window (entry bar between b1 and b2)
        wfills = [(eb, f) for eb, f in fills_by[(tf, d)] if b1 <= eb <= b2]
        # Signals (only in this window)
        wsigs = [(eb, s) for eb, s in sigs_by[(tf, d)] if b1 <= eb <= b2]
        # Blocks in window
        wblks = [(eb, b) for eb, b in blks_by[(tf, d)] if b1 <= eb <= b2]

        # Find exit for the (first) fill if exists
        cls = 'NO_SIGNAL'
        coverage = None
        sl_hit = False
        actual_R = None
        actual_exitReason = None
        used_fill = None
        if wfills:
            used_fill = wfills[0][1]
            tid = to_i(used_fill.get('tradeId'))
            xrec = exits_by_id.get(tid)
            if xrec is not None:
                ep = to_f(xrec.get('entry'))
                xp = to_f(xrec.get('exitPx'))
                actual_exitReason = xrec.get('exitReason')
                actual_R = to_f(xrec.get('R'))
                sl_hit = (actual_exitReason == 'sl')
                if ep is not None and xp is not None and w['span_price'] > 0:
                    raw_move = (xp - ep) if d == 'long' else (ep - xp)
                    coverage = raw_move / w['span_price']
            if coverage is not None and coverage >= COVERAGE_THRESHOLD and not sl_hit:
                cls = 'IDEAL'
            else:
                cls = 'CUT_SHORT'
        else:
            if wblks:
                cls = 'LOST'
            elif wsigs:
                cls = 'CUT_SHORT'  # signal but no fill (cancelled order, edge case)
            else:
                cls = 'NO_SIGNAL'

        classified.append({**w,
            'cls': cls,
            'coverage': coverage,
            'sl_hit': sl_hit,
            'actual_R': actual_R,
            'actual_exitReason': actual_exitReason,
            'wblks': wblks,
            'wsigs': wsigs,
            'wfills': wfills,
        })
    return classified


def evaluate(testdir: str):
    events = load_events(testdir)
    pivots = events['WT4 PIVOT']
    fills = events['WT4 ENTRY FILL']
    exits = events['WT4 REAL EXIT']
    signals = events['WT4 ENTRY']
    blocks = events['WT4 BLOCKED']

    tfs = sorted(set(p.get('tf') for p in pivots if p.get('tf')))
    out = [
        f'# Pivot-Window Coverage — {os.path.basename(testdir.rstrip("/"))}',
        '',
        f'Coverage threshold: {int(COVERAGE_THRESHOLD*100)}% of pivot-to-pivot move',
        '',
    ]

    all_classified = []
    for tf in tfs:
        windows = build_pivot_windows(pivots, tf)
        classified = classify_windows(windows, fills, exits, signals, blocks)
        all_classified.extend(classified)

    # Filter to "opportunity" windows (theoretical R ≥ MIN_THEORETICAL_R)
    opps = [c for c in all_classified if c.get('theoretical_R') is not None and c['theoretical_R'] >= MIN_THEORETICAL_R]
    out.append(f'Opportunity filter: theoretical_R ≥ {MIN_THEORETICAL_R} (= span ≥ {SL_MULT * MIN_THEORETICAL_R} × ATR_at_pivot)')
    out.append(f'  Opportunity windows: {len(opps)} / {len(all_classified)} total\n')

    # Per TF/dir summary (opportunities only)
    out.append('## 1. Opportunity Windows Klassifikation pro TF/dir\n')
    out.append(f'{"TF/dir":<10} {"Opps":>5} {"IDEAL":>6} {"CUT":>6} {"LOST":>6} {"NO_SIG":>7} {"avgR_ideal":>11}')
    out.append('-' * 65)
    for tfd in sorted(set((c['tf'], c['dir']) for c in opps)):
        sub = [c for c in opps if (c['tf'], c['dir']) == tfd]
        n = len(sub)
        idea = sum(1 for c in sub if c['cls'] == 'IDEAL')
        cut = sum(1 for c in sub if c['cls'] == 'CUT_SHORT')
        lost = sum(1 for c in sub if c['cls'] == 'LOST')
        nosig = sum(1 for c in sub if c['cls'] == 'NO_SIGNAL')
        ideal_R = [c['actual_R'] for c in sub if c['cls'] == 'IDEAL' and c['actual_R'] is not None]
        avgR_str = f'{sum(ideal_R)/len(ideal_R):+.2f}' if ideal_R else '—'
        out.append(f'{tfd[0]:<3}/{tfd[1]:<5} {n:>5} {idea:>6} {cut:>6} {lost:>6} {nosig:>7} {avgR_str:>11}')

    # Index windows for fast lookup
    win_by_tfd = defaultdict(list)
    for c in all_classified:
        win_by_tfd[(c['tf'], c['dir'])].append(c)
    for k in win_by_tfd:
        win_by_tfd[k].sort(key=lambda c: c['b1'])

    def find_window(tf, d, bar):
        for c in win_by_tfd.get((tf, d), []):
            if c['b1'] <= bar <= c['b2']:
                return c
        return None

    # Per gate: track UNIQUE opportunity windows the gate disturbed (LOST/CUT_SHORT) vs total
    out.append('\n## 2. Gate Disturbance Rate (auf Opportunity-Windows beschränkt)\n')
    out.append('Disturbance = unique_opp_windows_disturbed_by_gate / total_unique_opp_windows_blocked_by_gate')
    out.append('A window is "disturbed" if it ended up LOST or CUT_SHORT and this gate blocked at least once in it.')
    out.append('')

    gate_window_blocked = defaultdict(set)         # gate → set of (tf,dir,b1) of opp windows it blocked in
    gate_window_disturbed = defaultdict(set)       # gate → subset that ended LOST/CUT_SHORT
    gate_window_ideal = defaultdict(set)           # gate → subset that ended IDEAL
    gate_total_blocks = Counter()
    gate_outside_blocks = Counter()                # blocks not in any opp window
    gate_nosig_blocks = Counter()                  # blocks in NO_SIGNAL opp windows

    for b in blocks:
        gate = b.get('reason', 'unknown')
        gate_total_blocks[gate] += 1
        tf = b.get('tf'); d = b.get('dir')
        bar = to_i(b.get('bar'))
        if bar is None:
            gate_outside_blocks[gate] += 1
            continue
        w = find_window(tf, d, bar)
        # Only consider opportunity windows
        if w is None or w.get('theoretical_R') is None or w['theoretical_R'] < MIN_THEORETICAL_R:
            gate_outside_blocks[gate] += 1
            continue
        wid = (tf, d, w['b1'])
        gate_window_blocked[gate].add(wid)
        if w['cls'] in ('LOST', 'CUT_SHORT'):
            gate_window_disturbed[gate].add(wid)
        elif w['cls'] == 'IDEAL':
            gate_window_ideal[gate].add(wid)
        else:
            gate_nosig_blocks[gate] += 1

    out.append(f'{"Gate":<14} {"Blocks":>7} {"OppWins":>7} {"Disturbed":>10} {"InIdeal":>8} {"OutsideOpp":>11} {"Disturb%":>9} {"Verdict":>14}')
    out.append('-' * 95)
    for gate in sorted(gate_total_blocks.keys(), key=lambda g: -gate_total_blocks[g]):
        total = gate_total_blocks[gate]
        opp_blocked = len(gate_window_blocked.get(gate, set()))
        disturbed = len(gate_window_disturbed.get(gate, set()))
        ideal = len(gate_window_ideal.get(gate, set()))
        outside = gate_outside_blocks.get(gate, 0)
        rate = disturbed / opp_blocked if opp_blocked else 0
        if not gate.startswith('gate'):
            verdict = '(non-gate)'
        elif rate < ACTION_KEEP:
            verdict = '✓ BEHALTEN'
        elif rate < ACTION_TUNE:
            verdict = '~ JUSTIEREN'
        else:
            verdict = '✗ ENTFERNEN'
        out.append(f'{gate:<14} {total:>7} {opp_blocked:>7} {disturbed:>10} {ideal:>8} {outside:>11} {100*rate:>8.0f}% {verdict:>14}')

    # Section 4: Block POSITION in opp windows — wo blockt jedes Gate?
    # Position = (block_bar - b1) / (b2 - b1)
    # 0.0 = am Start des Windows (= ideale Entry-Zone für Long)
    # 1.0 = am Ende des Windows (= zu spät, der Move ist fast durch)
    out.append('\n## 4. Block-Position im Opp-Window (0=Start/idealer Entry, 1=Ende/zu spät)\n')
    out.append('Wenn Gate hauptsächlich am START blockt → blockt evtl. echte Setups.')
    out.append('Wenn Gate Richtung ENDE blockt → blockt zu spät kommende Trades (gut so).')
    out.append('')
    out.append(f'{"Gate":<10} {"OppWins":>8} {"BlocksPos_avg":>15} {"BlocksPos_med":>15}')
    out.append('-' * 55)

    gate_block_positions = defaultdict(list)
    for b in blocks:
        gate = b.get('reason', '')
        if not gate.startswith('gate'):
            continue
        tf = b.get('tf'); d = b.get('dir')
        bar = to_i(b.get('bar'))
        if bar is None: continue
        w = find_window(tf, d, bar)
        if w is None or w.get('theoretical_R') is None or w['theoretical_R'] < MIN_THEORETICAL_R:
            continue
        if w['b2'] == w['b1']: continue
        pos = (bar - w['b1']) / (w['b2'] - w['b1'])
        gate_block_positions[gate].append(pos)

    # Also: position of actual fills (baseline)
    fill_positions_all = []
    for f in fills:
        tf = f.get('tf'); d = f.get('dir')
        eb = to_i(f.get('bar'))
        if eb is None: continue
        w = find_window(tf, d, eb)
        if w is None or w.get('theoretical_R') is None or w['theoretical_R'] < MIN_THEORETICAL_R:
            continue
        if w['b2'] == w['b1']: continue
        pos = (eb - w['b1']) / (w['b2'] - w['b1'])
        fill_positions_all.append(pos)

    if fill_positions_all:
        fp_sorted = sorted(fill_positions_all)
        fp_med = fp_sorted[len(fp_sorted)//2]
        out.append(f'{"FILLS (baseline)":<10} {len(fill_positions_all):>8} {sum(fill_positions_all)/len(fill_positions_all):>15.2f} {fp_med:>15.2f}')

    for gate in sorted(gate_block_positions.keys()):
        ps = gate_block_positions[gate]
        if not ps: continue
        avg_pos = sum(ps) / len(ps)
        ps_sorted = sorted(ps)
        med_pos = ps_sorted[len(ps_sorted)//2]
        out.append(f'{gate:<10} {len(ps):>8} {avg_pos:>15.2f} {med_pos:>15.2f}')

    # Per gate per TF/dir disturbance breakdown
    out.append('\n## 5. Gate Disturbance pro TF/dir (Opportunity-Windows only)\n')
    out.append(f'{"Gate":<10} {"TF/dir":<10} {"OppWins":>8} {"Disturbed":>10} {"InIdeal":>8} {"Disturb%":>9}')
    out.append('-' * 65)

    gate_tfd_blocked = defaultdict(lambda: defaultdict(set))
    gate_tfd_disturbed = defaultdict(lambda: defaultdict(set))
    gate_tfd_ideal = defaultdict(lambda: defaultdict(set))
    for b in blocks:
        gate = b.get('reason', '')
        if not gate.startswith('gate'):
            continue
        tf = b.get('tf'); d = b.get('dir')
        bar = to_i(b.get('bar'))
        if bar is None:
            continue
        w = find_window(tf, d, bar)
        if w is None or w.get('theoretical_R') is None or w['theoretical_R'] < MIN_THEORETICAL_R:
            continue
        wid = (tf, d, w['b1'])
        gate_tfd_blocked[gate][(tf, d)].add(wid)
        if w['cls'] in ('LOST', 'CUT_SHORT'):
            gate_tfd_disturbed[gate][(tf, d)].add(wid)
        elif w['cls'] == 'IDEAL':
            gate_tfd_ideal[gate][(tf, d)].add(wid)

    for gate in sorted(gate_tfd_blocked.keys()):
        for tfd in sorted(gate_tfd_blocked[gate].keys()):
            t = len(gate_tfd_blocked[gate][tfd])
            p = len(gate_tfd_disturbed[gate][tfd])
            i = len(gate_tfd_ideal[gate][tfd])
            rate = p / t if t else 0
            out.append(f'{gate:<10} {tfd[0]:<3}/{tfd[1]:<5} {t:>8} {p:>10} {i:>8} {100*rate:>8.0f}%')

    # Section 6: Gate-flag simulation
    # If BLOCKED log contains `gates=A=T|B=T|C=F|...` we can simulate "what if Gate X were OFF?"
    # A signal would have passed if all OTHER gates are T (i.e., every flag != target gate is T).
    out.append('\n## 6. Simulation: was wäre passiert wenn Gate X aus gewesen wäre?\n')
    out.append('Pro Gate: wie viele LOST/CUT_SHORT Opp-Windows hätten ein Signal gehabt, wenn Gate X aus gewesen wäre?')
    out.append('(D.h. das Signal wurde NUR durch Gate X geblockt — alle anderen waren T.)')
    out.append('Wenn ein Gate viele Windows freischaltet → es ist der primäre Disturber dort.')
    out.append('')

    GATE_LETTERS = ['A','B','C','D','G','H','I']

    # Parse gate flags from blocks
    def parse_flags(s):
        """Parse 'A=T|B=T|C=F|D=T|G=T|H=T|I=T' into dict."""
        result = {}
        if not s: return result
        for part in s.split('|'):
            if '=' in part:
                k, v = part.split('=', 1)
                result[k.strip()] = v.strip() == 'T'
        return result

    # For each LOST/CUT_SHORT opp window, check if signal would have passed without gate X
    # We need to look at BLOCKED events with gate flags. If all flags != X are T, removing X unblocks.
    gate_unblock_count = defaultdict(set)  # gate_letter → set of (tf,dir,b1) of opp windows it would unblock
    flag_blocks = 0
    no_flag_blocks = 0
    for b in blocks:
        flags_str = b.get('gates', '')
        if not flags_str:
            no_flag_blocks += 1
            continue
        flag_blocks += 1
        flags = parse_flags(flags_str)
        tf = b.get('tf'); d = b.get('dir')
        bar = to_i(b.get('bar'))
        if bar is None: continue
        w = find_window(tf, d, bar)
        if w is None or w.get('theoretical_R') is None or w['theoretical_R'] < MIN_THEORETICAL_R: continue
        if w['cls'] not in ('LOST', 'CUT_SHORT'): continue
        wid = (tf, d, w['b1'])
        # For each gate: would removing it unblock this signal?
        for letter in GATE_LETTERS:
            if not flags.get(letter, True):
                # This gate failed. Would removing it unblock? Only if all OTHER letters are T.
                others_pass = all(flags.get(other, True) for other in GATE_LETTERS if other != letter)
                if others_pass:
                    gate_unblock_count[letter].add(wid)

    if no_flag_blocks > 0:
        out.append(f'⚠ {no_flag_blocks} blocks ohne `gates=` field (alte Strategy-Version oder cooldown). Skipped.')
        out.append('')

    if flag_blocks > 0:
        out.append(f'{"Gate":<10} {"WouldUnblock":>14} {"Comment":>40}')
        out.append('-' * 70)
        for letter in GATE_LETTERS:
            count = len(gate_unblock_count.get(letter, set()))
            if count == 0:
                comment = 'kein einzigartiger Disturber'
            elif count < 20:
                comment = 'kleiner unique impact'
            elif count < 100:
                comment = 'moderater unique impact'
            else:
                comment = 'großer unique impact — primärer Disturber'
            out.append(f'gate{letter:<6} {count:>14}    {comment}')
        out.append('')
        out.append('„WouldUnblock" = Anzahl LOST/CUT_SHORT Opp-Windows, in denen ein Signal nur an diesem Gate scheiterte.')
        out.append('Hohe Werte = Gate ist allein verantwortlich für viele verlorene Opps. Tiefe Werte = Gate hat Schnittmengen mit anderen.')

    print('\n'.join(out))


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: evaluate_pivot_coverage.py <testdir>')
        sys.exit(1)
    evaluate(sys.argv[1])
