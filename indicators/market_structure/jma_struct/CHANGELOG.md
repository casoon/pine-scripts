# Changelog

## v2.5.0 — 2026-10-02
- Fix: the Wyckoff context penalty (`Check Wyckoff Context`) never fired — it compared the phase label against "BULLISH"/"BEARISH", which the phase text never contains. It now checks the persistent Wyckoff bias (last SC/Spring or BC/UT event until it expires); the Spring/Upthrust exceptions are unchanged
- Changed: `Min score jump` is now set in JMA steps (one step = one JMA crossing = 100 / active JMAs) instead of score points, so it means the same with any number of active JMAs. Default 2 steps (provisional); the old point default of 10 equalled one step with 10 JMAs and never filtered anything
- Changed: order blocks no longer get a +25 score for BOS — BOS is a creation requirement, so every OB carried the same constant. The OB score now tops out at 75; the box border thresholds were rescaled to match (>56.25 / >37.5, previously >75 / >50)
- Fix: order block displacement only looked at the single bar after the OB candle. OB evaluation is now deferred until 3 bars (the displacement window) after the OB candle, so displacement is measured over the full window; FVG overlap and relative volume are still read at the displacement candle, and returns into the zone during the window already count as mitigation
- Fix: absorption could add to the data-driven quality score up to three times (STRUCTURE class, ABSORPTION bonus and pattern bonus). The pattern bonus now only applies to a Wyckoff spring/upthrust entry without absorption; input renamed to "Boost Wyckoff Patterns"
- Fix: long exhaustion was not the mirror of short exhaustion — it required a score of at least 60 (cluster still bullish) and a bullish candle, and failed-to-continue long required a score of at least 60. Long exhaustion now requires a score at or below 35 with the score above its 5-bar low (divergence), and failed-to-continue long a score at or below 30, mirroring the short rules. The 5-bar score low is computed on every bar
- Input tooltips no longer cite backtest figures or quality claims; they describe what each setting does and why. Selling/Buying Climax label tooltips now state the actual rule (down close / up close on the swing bar)
- Removed the remaining backtest figures from user-facing text: the header no longer advertises "data-driven" scoring, and the quality-model switch is now "Use Bonus/Penalty Quality Scoring" (renamed input — re-enable it if you had it on). Code comments point at the internal calibration record instead of repeating numbers
- Fix: the order-block score gave volume points on tick volume. Without real trade volume the volume component is skipped and the score is rescaled onto the same 0–75 range

## v2.4.0 — 2026-10-02
- Fix: Selling/Buying Climax read the wrong bar. The swing is confirmed `Lookback` bars back, but candle direction, relative volume, swing size and the Trading Range boundary were taken from the confirming (current) bar. All of them now come from the swing bar; the SC/BC chart labels are placed on that bar too
- Fix: Wyckoff Upthrust entry pattern required relative volume above 1.3 even when the feed has no real trade volume — it now passes through like the Spring pattern does
- Fix: order blocks were checked for mitigation on their own creation bar, where the displacement candle almost always trades back into the OB candle's range — practically every OB was "mitigated" at birth. Mitigation is now checked from the next bar on, and the OB score is refreshed so the fresh bonus drops once an OB is mitigated
- Fix: "Max Alert Window for Bonus" had no effect — the alert-window bonus used a fixed upper bound of 100 bars. It now uses the input (default 100, so default behaviour is unchanged)
- Fix: three `ta.highest`/`ta.lowest` calls in the exhaustion / failed-to-continue conditions sat inside short-circuited conditions and did not run on every bar; they are now computed unconditionally
- "Min score jump" tooltip now explains that a value at or below one JMA step (100 / active JMAs) never filters a cluster flip

## v2.3.5 — 2026-09-06
- Volume validity is now decided by `syminfo.volumetype`. Every Wyckoff entry pattern required `relVolume` above 1.3–1.5; on feeds without real trade volume those comparisons could never be true, so Spring, Upthrust and the Wyckoff spring entry silently stopped firing
- Confirming thresholds (entry patterns, secondary tests, SOS/SOW breakouts) now pass through when trade volume is unavailable
- Climax and absorption events are withheld in that case rather than approximated
- Shock-bar detection is explicitly tied to volume availability (behaviour unchanged, intent now stated)
- Added a chart note and the Data Contract header block

## v2.3.3 — 2026-06-30
- Alerts: added a "Alerts only on bar close (confirmed)" toggle (default on); all alert conditions now respect it, preventing intrabar repaint of the named alerts

## v2.3.2 — 2026-06-29
- Alerts: messages standardized to `JMAS · EVENT · {{ticker}} {{interval}}` so they identify symbol/timeframe on multi-chart setups (titles unchanged)

## v2.3.1 — 2026-06-11
- Fixed: 3-bar timeout for armed pattern signals (Spring, Upthrust, Wyckoff Spring/UT, Exhaustion) never fired — armed signals persisted until a confirmation eventually triggered, producing late entries. Signals now reset 3 bars after the pattern bar as documented.
- Fixed: bullish Break-of-Structure check guarded with the wrong swing variables (no functional crash, but inconsistent na-handling).
- Performance: removed duplicate standard-deviation calculation for the reversion zone.

## v2.3.0
- Initial release
