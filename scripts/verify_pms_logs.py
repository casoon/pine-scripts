#!/usr/bin/env python3
"""Verify Pine-log CSV exports from pivot_momentum_structure.pine (PMS PIVOT lines).

Usage: python3 verify_pms_logs.py <dir-or-glob-of-csv-files>

Checks (per row, using only fields present in that row's log format):
  1. Mutual exclusivity of directional flags.
  2. hasAnchor=false implies every anchor-dependent flag is false.
  3. Regular/hidden divergence and confirmation flags imply their exact boolean
     building blocks (direction-aware: regular/hidden divergence directions are
     mirrored between High and Low pivots, confirmation is symmetric).
  4. Divergence and confirmation are mutually exclusive; both directions of each
     are mutually exclusive.
  5. anchorDist arithmetic is correct and the anchor is always in the past.
  6. Directional flags match the actual current-vs-anchor price/oscillator comparison.
  7. The anchor actually exists in this run's own same-type pivot history, with
     matching stored price/oscillator values.
  8. (v2 fields only) priceStruct/oscStruct match an independent recomputation
     from prevPrice/prevOsc/priceTolerance.
  9. (v2 fields only) the anchor actually chosen is the one with the highest
     f_anchorScore (recency 40% / oscillator rate-of-change 30% / extreme-zone
     context 20% / price distinctness 10%) over the logged history window
     (catches anchor-selection regressions, not just internal consistency of a
     single row). Also cross-checks the logged anchorScore against the
     recomputed one.
"""
import csv
import glob
import re
import sys

HIGH_KEYS = ["type","idx","osc","mode","price","priceStruct","oscVal","oscIdx","oscStruct",
             "hasAnchor","anchorIdx","anchorDist","anchorPrice","anchorOsc","anchorScore","oscStDev",
             "priceMadeHigherHigh","priceMadeLowerHigh","priceMadeEqualHigh",
             "oscMadeHigherHigh","oscMadeLowerHigh","highExtremeValid","trendContextBearishOk",
             "regularBearishDiv","hiddenBearishDiv","bullConfirm","bearConfirm",
             "priceTolerance","prevPrice","prevOsc","allowEqual","minOscDiff",
             "minPivotDist","maxPivotDist","histIdx","histPrice","histOsc"]
LOW_KEYS = ["type","idx","osc","mode","price","priceStruct","oscVal","oscIdx","oscStruct",
            "hasAnchor","anchorIdx","anchorDist","anchorPrice","anchorOsc","anchorScore","oscStDev",
            "priceMadeHigherLow","priceMadeLowerLow","priceMadeEqualLow",
            "oscMadeHigherLow","oscMadeLowerLow","lowExtremeValid","trendContextBullishOk",
            "regularBullishDiv","hiddenBullishDiv","bullConfirm","bearConfirm",
            "priceTolerance","prevPrice","prevOsc","allowEqual","minOscDiff",
            "minPivotDist","maxPivotDist","histIdx","histPrice","histOsc"]

# Mirrors the `upperExtreme`/`lowerExtreme` switch in pivot_momentum_structure.pine
# (OSCILLATOR SCALE section) — constant per run, keyed by the logged `osc=` field.
UPPER_EXTREME = {
    "RSI": 70.0, "WaveTrend": 60.0, "Stochastic RSI": 80.0, "CCI": 100.0,
    "Fisher": 1.5, "TSI": 25.0, "Williams %R": -20.0, "CMO": 50.0,
}
LOWER_EXTREME = {
    "RSI": 30.0, "WaveTrend": -60.0, "Stochastic RSI": 20.0, "CCI": -100.0,
    "Fisher": -1.5, "TSI": -25.0, "Williams %R": -80.0, "CMO": -50.0,
}

def parse_row(msg):
    if not msg.startswith("PMS PIVOT"):
        return None
    body = msg[len("PMS PIVOT "):]
    m = re.match(r"type=(High|Low)", body)
    if not m:
        return None
    keys = HIGH_KEYS if m.group(1) == "High" else LOW_KEYS
    positions = []
    for k in keys:
        pat = re.compile(r"(?<![A-Za-z])" + re.escape(k) + "=")
        mo = pat.search(body)
        if mo is not None:
            positions.append((k, mo.start(), mo.end()))
    positions.sort(key=lambda x: x[1])
    result = {}
    for i, (k, s, e) in enumerate(positions):
        val_start = e
        val_end = positions[i+1][1] if i+1 < len(positions) else len(body)
        result[k] = body[val_start:val_end].strip()
    return result

def to_bool(s):
    return s == "true"

def to_float(s):
    if s in ("NaN", "", None):
        return None
    try:
        return float(s)
    except ValueError:
        return None

def to_int(s):
    if s in ("NaN", "", None):
        return None
    try:
        return int(float(s))
    except ValueError:
        return None

def parse_hist(idxStr, priceStr, oscStr):
    if not idxStr:
        return []
    idxs = [to_int(x) for x in idxStr.split("|")]
    prices = [to_float(x) for x in priceStr.split("|")] if priceStr else []
    oscs = [to_float(x) for x in oscStr.split("|")] if oscStr else []
    return list(zip(idxs, prices, oscs))

def anchor_score(current_price, cand_price, price_tolerance, current_osc, cand_osc,
                  current_idx, cand_idx, is_high, osc_stdev, upper_extreme, lower_extreme,
                  min_dist, max_dist):
    """Mirrors f_anchorScore in pivot_momentum_structure.pine exactly."""
    distance = current_idx - cand_idx
    distance_range = max_dist - min_dist
    recency_score = 50.0
    if distance_range > 0:
        recency_score = 100.0 - max(0.0, min(100.0, (distance - min_dist) / distance_range * 100.0))
    osc_diff = abs(current_osc - cand_osc)
    osc_rate = osc_diff / distance if distance > 0 else osc_diff
    rate_score = 50.0
    if osc_stdev is not None and osc_stdev > 0:
        rate_score = max(0.0, min(100.0, osc_rate / (osc_stdev * 0.5) * 100.0))
    in_extreme = (cand_osc >= upper_extreme) if is_high else (cand_osc <= lower_extreme)
    extreme_score = 100.0 if in_extreme else 0.0
    price_diff = abs(current_price - cand_price)
    price_score = 50.0
    if price_tolerance is not None and price_tolerance > 0:
        price_score = max(0.0, min(100.0, price_diff / (price_tolerance * 3.0) * 100.0))
    return recency_score * 0.40 + rate_score * 0.30 + extreme_score * 0.20 + price_score * 0.10

def find_best_anchor(hist, current_idx, current_price, current_osc,
                      price_tolerance, allow_equal, min_osc_diff, min_dist, max_dist,
                      is_high, osc_stdev, upper_extreme, lower_extreme):
    """Mirrors f_findBestAnchor in pivot_momentum_structure.pine exactly — scans the
    full window (most-recent-first, matching the Pine loop order) and picks the
    highest-scoring qualifying candidate, not just the first (nearest) one."""
    best_idx = None
    best_score = -1.0
    for idx, price, osc in reversed(hist):
        if idx is None or price is None or osc is None:
            continue
        dist = current_idx - idx
        if not (min_dist <= dist <= max_dist):
            continue
        price_diff = abs(current_price - price)
        price_ok = price_diff >= price_tolerance or (allow_equal and price_diff <= price_tolerance)
        if not price_ok:
            continue
        osc_diff = abs(current_osc - osc)
        if osc_diff < min_osc_diff:
            continue
        score = anchor_score(current_price, price, price_tolerance, current_osc, osc,
                              current_idx, idx, is_high, osc_stdev, upper_extreme, lower_extreme,
                              min_dist, max_dist)
        if score > best_score:
            best_score = score
            best_idx = idx
    return best_idx, best_score

def classify(current, previous, tolerance, higher_label, lower_label, equal_label, first_label):
    if previous is None:
        return first_label
    if current > previous + tolerance:
        return higher_label
    elif current < previous - tolerance:
        return lower_label
    return equal_label

def validate_file(path):
    issues = []
    n_rows = 0
    n_high = 0
    n_low = 0
    n_hasanchor = 0
    n_regdiv = 0
    n_hiddendiv = 0
    n_confirm = 0
    max_anchor_dist = 0
    has_v2_fields = False
    high_history = []  # (idx, price, oscVal) — mirrors the Pine array (max 8, oldest-first)
    low_history = []
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader, None)
        for lineno, row in enumerate(reader, start=2):
            if len(row) < 2:
                continue
            msg = row[1]
            r = parse_row(msg)
            if r is None:
                continue
            n_rows += 1
            typ = r["type"]
            idx = to_int(r["idx"])
            price = to_float(r["price"])
            oscVal = to_float(r["oscVal"])
            hasAnchor = to_bool(r["hasAnchor"])
            anchorIdx = to_int(r["anchorIdx"])
            anchorDist = to_int(r["anchorDist"])
            anchorPrice = to_float(r["anchorPrice"])
            anchorOsc = to_float(r["anchorOsc"])
            priceStruct = r.get("priceStruct")

            if typ == "High":
                n_high += 1
                pmhh = to_bool(r["priceMadeHigherHigh"])
                pmlh = to_bool(r["priceMadeLowerHigh"])
                pmeh = to_bool(r["priceMadeEqualHigh"])
                omhh = to_bool(r["oscMadeHigherHigh"])
                omlh = to_bool(r["oscMadeLowerHigh"])
                extremeOk = to_bool(r["highExtremeValid"])
                trendOk = to_bool(r["trendContextBearishOk"])
                regDiv = to_bool(r["regularBearishDiv"])
                hidDiv = to_bool(r["hiddenBearishDiv"])
                bullC = to_bool(r["bullConfirm"])
                bearC = to_bool(r["bearConfirm"])
                history = high_history
            else:
                n_low += 1
                pmhh = to_bool(r["priceMadeHigherLow"])
                pmlh = to_bool(r["priceMadeLowerLow"])
                pmeh = to_bool(r["priceMadeEqualLow"])
                omhh = to_bool(r["oscMadeHigherLow"])
                omlh = to_bool(r["oscMadeLowerLow"])
                extremeOk = to_bool(r["lowExtremeValid"])
                trendOk = to_bool(r["trendContextBullishOk"])
                regDiv = to_bool(r["regularBullishDiv"])
                hidDiv = to_bool(r["hiddenBullishDiv"])
                bullC = to_bool(r["bullConfirm"])
                bearC = to_bool(r["bearConfirm"])
                history = low_history

            tag = f"{path.split('/')[-1]}:{lineno} idx={idx} type={typ}"

            # Rule 1
            if pmhh and pmlh:
                issues.append(f"{tag}: priceMadeHigher AND priceMadeLower both true")
            if omhh and omlh:
                issues.append(f"{tag}: oscMadeHigher AND oscMadeLower both true")

            # Rule 2 / 5
            if not hasAnchor:
                if any([pmhh, pmlh, pmeh, omhh, omlh, regDiv, hidDiv, bullC, bearC]):
                    issues.append(f"{tag}: hasAnchor=false but a dependent flag is true "
                                  f"(pmhh={pmhh} pmlh={pmlh} pmeh={pmeh} omhh={omhh} omlh={omlh} "
                                  f"regDiv={regDiv} hidDiv={hidDiv} bullC={bullC} bearC={bearC})")
            else:
                n_hasanchor += 1
                if anchorDist is not None:
                    max_anchor_dist = max(max_anchor_dist, anchorDist)
                if idx is not None and anchorIdx is not None and anchorDist != (idx - anchorIdx):
                    issues.append(f"{tag}: anchorDist={anchorDist} != idx-anchorIdx={idx-anchorIdx}")
                if anchorDist is not None and anchorDist <= 0:
                    issues.append(f"{tag}: anchorDist={anchorDist} <= 0 (anchor not in the past)")

            # Rule 3 (direction-aware)
            priceDirOk = (pmhh or pmeh) if typ == "High" else (pmlh or pmeh)
            oscDirOk = omlh if typ == "High" else omhh
            if regDiv:
                n_regdiv += 1
                if not hasAnchor:
                    issues.append(f"{tag}: regularDiv=true but hasAnchor=false")
                if not priceDirOk:
                    issues.append(f"{tag}: regularDiv=true but price direction condition false (pmhh={pmhh} pmlh={pmlh} pmeh={pmeh})")
                if not oscDirOk:
                    issues.append(f"{tag}: regularDiv=true but osc direction condition false (omhh={omhh} omlh={omlh})")
                if not extremeOk:
                    issues.append(f"{tag}: regularDiv=true but extremeValid=false")

            # Rule 4 (direction-aware, + trend context gate)
            hidPriceDirOk = pmlh if typ == "High" else pmhh
            hidOscDirOk = omhh if typ == "High" else omlh
            if hidDiv:
                n_hiddendiv += 1
                if not hasAnchor:
                    issues.append(f"{tag}: hiddenDiv=true but hasAnchor=false")
                if not trendOk:
                    issues.append(f"{tag}: hiddenDiv=true but trendContextOk=false")
                if not hidPriceDirOk:
                    issues.append(f"{tag}: hiddenDiv=true but price direction condition false (pmhh={pmhh} pmlh={pmlh})")
                if not hidOscDirOk:
                    issues.append(f"{tag}: hiddenDiv=true but osc direction condition false (omhh={omhh} omlh={omlh})")

            # Rule 5: confirmation implications (symmetric across type)
            if bullC:
                n_confirm += 1
                if not (pmhh and omhh):
                    issues.append(f"{tag}: bullConfirm=true but not (priceMadeHigher and oscMadeHigher)")
            if bearC:
                n_confirm += 1
                if not (pmlh and omlh):
                    issues.append(f"{tag}: bearConfirm=true but not (priceMadeLower and oscMadeLower)")
            if bullC and bearC:
                issues.append(f"{tag}: bullConfirm AND bearConfirm both true in same row")
            if regDiv and hidDiv:
                issues.append(f"{tag}: regularDiv AND hiddenDiv both true in same row")

            # Rule 6: directional flags vs actual comparison
            if hasAnchor and price is not None and anchorPrice is not None:
                if pmhh and price <= anchorPrice:
                    issues.append(f"{tag}: priceMadeHigher=true but price({price}) <= anchorPrice({anchorPrice})")
                if pmlh and price >= anchorPrice:
                    issues.append(f"{tag}: priceMadeLower=true but price({price}) >= anchorPrice({anchorPrice})")
            if hasAnchor and oscVal is not None and anchorOsc is not None:
                if omhh and oscVal <= anchorOsc:
                    issues.append(f"{tag}: oscMadeHigher=true but oscVal({oscVal}) <= anchorOsc({anchorOsc})")
                if omlh and oscVal >= anchorOsc:
                    issues.append(f"{tag}: oscMadeLower=true but oscVal({oscVal}) >= anchorOsc({anchorOsc})")

            # Rule 7: anchor must reference a real prior same-type pivot
            if hasAnchor:
                match = [h for h in history if h[0] == anchorIdx]
                if not match:
                    issues.append(f"{tag}: anchorIdx={anchorIdx} not found in prior {typ}-type history "
                                  f"(history idxs so far: {[h[0] for h in history[-10:]]})")
                else:
                    hp, ho = match[0][1], match[0][2]
                    if anchorPrice is not None and hp is not None and abs(hp - anchorPrice) > 1e-6:
                        issues.append(f"{tag}: anchorPrice({anchorPrice}) != stored history price({hp}) for idx={anchorIdx}")
                    if anchorOsc is not None and ho is not None and abs(ho - anchorOsc) > 1e-4:
                        issues.append(f"{tag}: anchorOsc({anchorOsc}) != stored history oscVal({ho}) for idx={anchorIdx}")

            # --- v2 fields (only present after the 2.6.1 logging expansion) ---
            if "priceTolerance" in r and r["priceTolerance"]:
                has_v2_fields = True
                priceTolerance = to_float(r["priceTolerance"])
                prevPrice = to_float(r["prevPrice"])
                allowEqual = to_bool(r["allowEqual"])
                minOscDiff = to_float(r["minOscDiff"])
                minPivotDist = to_int(r["minPivotDist"])
                maxPivotDist = to_int(r["maxPivotDist"])
                logHist = parse_hist(r.get("histIdx",""), r.get("histPrice",""), r.get("histOsc",""))

                # Rule 8: priceStruct re-derivation (skip if tolerance is NaN — ATR warmup on early bars)
                if price is not None and (prevPrice is None or priceTolerance is not None):
                    if typ == "High":
                        expected = classify(price, prevPrice, priceTolerance, "HH", "LH", "EH", "H")
                    else:
                        expected = classify(price, prevPrice, priceTolerance, "HL", "LL", "EL", "L")
                    if priceStruct is not None and expected != priceStruct:
                        issues.append(f"{tag}: priceStruct={priceStruct} but recomputed from prevPrice/tolerance = {expected} "
                                      f"(price={price} prevPrice={prevPrice} tol={priceTolerance})")

                # Rule 9: highest-scoring anchor re-derivation using the logged history window
                if price is not None and oscVal is not None and priceTolerance is not None \
                   and minOscDiff is not None and minPivotDist is not None and maxPivotDist is not None:
                    oscType = r.get("osc")
                    upperExtremeVal = UPPER_EXTREME.get(oscType, 70.0)
                    lowerExtremeVal = LOWER_EXTREME.get(oscType, 30.0)
                    oscStDev = to_float(r.get("oscStDev", ""))
                    isHigh = typ == "High"
                    expectedAnchor, expectedScore = find_best_anchor(
                        logHist, idx, price, oscVal,
                        priceTolerance, allowEqual, minOscDiff,
                        minPivotDist, maxPivotDist,
                        isHigh, oscStDev, upperExtremeVal, lowerExtremeVal
                    )
                    loggedAnchor = anchorIdx if hasAnchor else None
                    if expectedAnchor != loggedAnchor:
                        issues.append(f"{tag}: anchor search mismatch — logged anchorIdx={loggedAnchor}, "
                                      f"recomputed highest-scoring={expectedAnchor} "
                                      f"(history={logHist})")
                    elif hasAnchor:
                        loggedScore = to_float(r.get("anchorScore"))
                        if loggedScore is not None and expectedScore is not None \
                           and abs(loggedScore - expectedScore) > 0.5:
                            issues.append(f"{tag}: anchorScore mismatch — logged={loggedScore}, "
                                          f"recomputed={expectedScore:.2f}")

            history.append((idx, price, oscVal))
            if len(history) > 8:
                history.pop(0)

    return {
        "file": path.split("/")[-1],
        "rows": n_rows, "high": n_high, "low": n_low,
        "hasAnchor": n_hasanchor, "regDiv": n_regdiv, "hiddenDiv": n_hiddendiv,
        "confirm": n_confirm, "max_anchor_dist": max_anchor_dist,
        "has_v2_fields": has_v2_fields,
        "issues": issues,
    }

def main():
    pattern = sys.argv[1] if len(sys.argv) > 1 else "pine-logs-PMS_*.csv"
    files = sorted(glob.glob(pattern))
    if not files:
        print(f"No files matched: {pattern}")
        sys.exit(1)
    total_issues = 0
    for path in files:
        res = validate_file(path)
        total_issues += len(res["issues"])
        print(f"=== {res['file']} (v2 fields: {res['has_v2_fields']}) ===")
        print(f"  rows={res['rows']} high={res['high']} low={res['low']} hasAnchor={res['hasAnchor']} "
              f"regDiv={res['regDiv']} hiddenDiv={res['hiddenDiv']} confirm={res['confirm']} "
              f"maxAnchorDist={res['max_anchor_dist']}")
        if res["issues"]:
            print(f"  ISSUES ({len(res['issues'])}):")
            for iss in res["issues"][:20]:
                print(f"    - {iss}")
            if len(res["issues"]) > 20:
                print(f"    ... and {len(res['issues'])-20} more")
        else:
            print("  no issues found")
        print()
    print(f"TOTAL ISSUES ACROSS ALL FILES: {total_issues}")

if __name__ == "__main__":
    main()
