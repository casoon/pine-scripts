# Changelog

## v1.4.2 — 2026-10-02
- Fixed: the broken-level check (Broken Level Penalty and Hold Rate) scanned from each reaction's own bar up to now, so the remaining A→B leg — and the reaction itself — counted as breaking the level, marking almost every reaction as broken. Breaks are now checked only over the current pullback, from B up to now

## v1.4.1 — 2026-10-02
- Fixed: reaction size now measures only the bars after the micro pivot. The pivot bar's own range was included, so a single wide pivot candle could pass the minimum-reaction filter on its own and inflated reaction strength

## v1.4 — 2026-08-11
- Added per-level Hold Rate: % of historical reactions near a level that were never subsequently broken, shown next to the score in the label (`Show Hold Rate` toggle, on by default); reuses the v1.3 broken-level check, no new scan pass

## v1.3 — 2026-08-11
- Added a broken-level penalty: historical reactions whose level was later broken (checked against the current leg's fixed A/B range using each bar's own raw high/low, from the reaction's bar up to now) now count for less than reactions whose level was never subsequently broken (`Broken Level Penalty` input, default `0.5`, `0` = old behavior)

## v1.2 — 2026-08-11
- Added level consumption: reactions are now scanned oldest-first and each additional test of the same Fib level counts for less than the first (`Level Consumption` input, `1 / (1 + decay × testsSoFar)`); default `0.35`, `0` reproduces the old unweighted behavior

## v1.1 — 2026-08-11
- Replaced the stateless AHEAD/TESTING/PASSED/REJECTED classification with a real per-level state machine (APPROACHING/TESTING/REJECTED/ACCEPTED/RECLAIMED), derived from current retracement vs. the deepest retracement reached during the pullback; removed the now-redundant `fibTouched` array

## v1.0 — 2026-08-10
- Initial release: confirmed A→B reference leg, ATR-weighted micro-pivot reaction memory normalized onto standard Fib levels, 0–100 saturating Memory Score per level, AHEAD/TESTING/PASSED/REJECTED state, score-based NEXT level highlight, no table — all context attached directly to the Fib lines/labels
