# Changelog

## v1.10.1 — 2026-10-12
- Volume check fixed: only `tick` volume is rejected; `n/a` counts when the feed actually delivers volume. Most non-crypto feeds report `n/a` — the old `base`/`quote` check also blocked futures and stocks with real volume (e.g. EUREX:FDAX1!)
- Without real trade volume a short "not available" notice now sits in the bottom-right corner instead of a long warning label on the last candle; the requirement is stated in the Data Contract header

## v1.10.0 — 2026-10-02
- Fixed: Profile Shape almost always showed "B (Double)" because it counted HVN rows instead of HVN nodes — any single smooth peak spans several rows above the threshold. Shape now counts separate HVN nodes (contiguous runs of HVN rows); B requires at least two, so D / P / b are reachable again
## v1.9.4 — 2026-09-05
- Hard Exchange-only gate: the entire profile (computation + all drawing) now only runs when `syminfo.volumetype` is `base`/`quote` and `volume` is not `na`; on tick/n/a volume it draws nothing but a "needs real trade volume" warning label instead
- Added Data Contract header block (Verdict: Exchange-only)

## v1.9.3 — 2026-07-09
- Fix: `npoc_already_touched` now guards against `na` prev POC explicitly
- Naked POC: added "Naked POC Min Distance (ATR)" input — filters out noise-driven POC shifts before tracking a new naked POC (default 0.1 ATR)

## v1.9.2 — 2026-06-30
- Alerts: added a "Alerts only on bar close (confirmed)" toggle (default on); all alert conditions now respect it, preventing intrabar repaint of the named alerts

## v1.9.1 — 2026-06-29
- Alerts: messages standardized to `VST · EVENT · {{ticker}} {{interval}}` so they identify symbol/timeframe on multi-chart setups (titles unchanged)

## v1.9
- Initial release
