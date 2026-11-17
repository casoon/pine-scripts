# Changelog

## v1.3.0 — 2026-11-17
- The weighted signal quality score (volatility 0.5, volume 0.3, trend 0.2, confluence halving) is removed. RDP entries and the SSA gate now use one explicit filter condition: enough volatility, plus a volume confirmation or a trend slope (`volOk and (volGate or trendScore > 0.2)`); the volume part passes when the volume filter is off or the symbol has no real trade volume. With the default Confluence Filter settings this is the same decision as before. Users who had changed Confluence Filter / Confluence Threshold can see different entries; the SSA gate previously used its own 0.60 minimum, which at default settings made the same decision
- Removed inputs: Confluence Filter, Confluence Threshold, SSA Min Signal Quality, SSA Show pending marker (the pending markers could never appear)
- SSA status table: Quality row removed. Alert builder: condition "Quality OK" is now "Filter OK". Pine-log export: `quality=` field replaced by `filter=true/false`

## v1.2.0 — 2026-11-17
- RDP entry tiers A/B removed: an entry now fires on the regime start itself (confirmation bars, filter and HTF gate, one entry per regime). Entries that were previously held back below the Tier B thresholds now fire, so entries can come more often; the `LOWQ` labels, the A/B quality label next to the bar and the A/B status text are gone
- Removed inputs: Tier A/B Min Confidence / HTF Agreement / Signal Quality, Alert Confidence Min, Confidence Meters, Signal Strength, Strength Dot Position / Offset / Color, Playbook Line; SSA: Strong Min Confidence / HTF / Quality, Enable Super tier and its three requirements, SSA entries require RDP Tier B+, SSA Entry Tier Gate, SSA Signal Display, Strong shows plus markers
- SSA Strong/Super tiers removed; the SSA long/short event stays. SSA Entry Source is now "SSA Engine" or "RDP Entries"; without the tier gate SSA events can come more often (mainly in Scalping mode)
- Removed alerts: RDP Any High Confidence, SSA Strong Long/Short, SSA Super Long/Short. The alert builder drops the conditions SSA Strong Long/Short and RDP Tier A/B+ (new defaults: SSA Long, RDP Bull Regime); the webhook message drops the `Q=` field
- Info panel: Tier, Signal Quality and Action (playbook) rows removed; SSA table: Tier row removed
- Fix: the SSA table in compact mode no longer writes one row past its end when every row is filled

## v1.1.8 — 2026-11-17
- HTF agreement now reads the last closed higher-timeframe bar (no repaint); the HTF gate, tiers, SSA and MA zones no longer change while the HTF bar is still forming
- RDP entries: after a band exit, a new entry in the same direction needs a new regime start; the same ongoing regime no longer re-enters after the cooldown
- SSA events fire on the rising edge of the gate condition only; the cooldown now filters events instead of creating a new one every time it expires
- Info panel: Win Rate and Profit Factor rows removed

## v1.1.7 — 2026-10-12
- Volume check fixed: only `tick` volume is rejected; `n/a` counts when the feed actually delivers volume. Most non-crypto feeds report `n/a`, so the old `base`/`quote` check treated futures and stocks with real volume (e.g. EUREX:FDAX1!) as volume-less — volume-based parts are active there again, which can change scores, gates and signals on those markets

## v1.1.6 — 2026-10-02
- Fix: no regime could ever form with default inputs. Regime confidence was the normalized efficiency ratio multiplied by Regime Sensitivity, which capped it at the sensitivity value (0.60 at default) — below Min Regime Confidence (0.65), so the regime stayed FLAT and every Bull/Bear-dependent part (bands, heatmap, playbook, AGING, MA zones, entries, tiers) was dead. Confidence is now the normalized efficiency ratio itself; entering a regime still requires a strong ER (≥ ~0.72 over the ER length at the default thresholds), so regimes remain selective
- Regime Sensitivity now only drives the momentum gate (minimum normalized slope strength). Its tooltip said "higher = more sensitive", which was inverted for that gate — corrected: higher = stricter

## v1.1.5 — 2026-06-30
- Alerts: added a "Alerts only on bar close (confirmed)" toggle (default on); all alert conditions now respect it, preventing intrabar repaint of the named alerts

## v1.1.4 — 2026-06-29
- Alerts: the three context alerts (Regime Weakening, Volatility Compression, Volatility Expansion) are now gated by the "Smart Alerts" toggle, consistent with the other alerts — previously they fired even when Smart Alerts was off

## v1.1.3 — 2026-06-29
- Alerts: messages standardized to `RDP · EVENT · {{ticker}} {{interval}}` so they identify symbol/timeframe on multi-chart setups (titles unchanged)

## v1.1.2 — 2026-06-29
- Docs: clarified that the named `alertcondition()` alerts and the combined `alert()` webhook rule are an either/or — enable one, not both, or each event fires twice. No behaviour change.

## v1.1.1 — 2026-06-27
- **Trade engine isolated behind a toggle**: new "Show Trade Engine (entries/exits/TP/SL + performance)" input (Signal Management group, default OFF). When off, RDP behaves as a pure regime classifier/visual — only regime bands, heatmap, candle tint, context labels and warnings render. When on, it re-enables the RDP entry/exit markers, tier/quality labels, MA-zone entry/SL engine, trade-entry/exit alerts and the performance statistics rows.

## v1.1.0 — 2026-06-11
- **Volatility dimension**: a second axis (Quiet / Normal / Volatile) from ATR percentile + Bollinger-width percentile, turning "Bull" into "Quiet Bull" / "Volatile Bull" etc. New "Regime Context" input group (lookback, quiet/volatile thresholds).
- **Regime maturity + transition warning**: tracks bars-in-regime and peak strength, then classifies Fresh / Mature / Mature-strong / Aging-weakening (slope turning against the regime, efficiency below exit threshold, or fade below 50% of peak).
- **Plain-language playbook**: a panel line translating the combined regime into an action hint (e.g. "Healthy uptrend — buy pullbacks", "Compression — await breakout", "Trend aging — tighten stops").
- **Optional RS vs. benchmark (equities)**: relative strength vs. SPY/QQQ as a regime modifier — appends "RS leading ✓ / lagging ✗" to the playbook and a dedicated RS panel line.
- New alerts: Regime Weakening, Volatility Compression, Volatility Expansion.
- Fix: in Compact Mode the panel row count omitted the Performance (2 rows) and Auto-Tune rows although their cells are always written — could trigger a "cannot create table cell" runtime error when both were enabled. Row count now matches the cells in both modes.
- **Visual refresh**: new Visual Theme selector (Modern / Soft / Classic), soft gradient ATR bands (vertical fade), a softer volatility-aware regime heatmap, and a default-on Regime Candle Tint (direction × volatility intensity) so the chart reads at a glance instead of "a band with a few labels". Candle tint auto-suppresses when SSA candle coloring is active. All implemented within the existing plot/fill objects to stay under TradingView's 64-output limit.
- Info panel now defaults to Bottom Left so it sits clear of both the SSA status table (Top Right) and the broker's symbol/price overlay (Top Left).
- Context event labels on the chart (default on): COMPRESS (volatility contracted → breakout setup), EXPAND (volatility spiked → climax/whipsaw risk), AGING (trend regime weakening). Implemented with label.new, so they do not count toward the plot budget.
- Both tables (Info Panel and SSA Status Table) now default to off for a cleaner chart — enable either in its settings group when needed.

## v1.0.1 — 2026-06-11
- Fix: SSA pending limit-style entries never activated — tuple destructuring into the pending-state variable names created shadowing locals, so the pending state was silently discarded. Pending state is now assigned explicitly.
- Fix: win rate in the info panel / auto-tuning was computed with integer division and always showed 0 (or 1).
- Fix: logged signal quality (`Log label metrics`) always reported the current value for historical bars — now uses a real series.
- Fix: multi-line ternary for zone strength normalization rewritten as if/else (Pine v6 compile error CE10156).
- Fix: `ta.atr(14)` was called inside conditionally executed functions (SL source, trail candidate) — hoisted to global scope to keep history consistent.
- Fix: info panel showed hardcoded "v2.0" although the script version is 1.0.x.
- Info panel and SSA status table restyled to the light-theme dashboard convention (was dark background with white text).

## v1.0.0
- Initial release
