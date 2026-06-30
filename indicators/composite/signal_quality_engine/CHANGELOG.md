# Changelog

## v3.2.2 — 2026-06-30
- Alerts: added a "Alerts only on bar close (confirmed)" toggle (default on); all alert conditions now respect it, preventing intrabar repaint of the named alerts

## v3.2.1 — 2026-06-29
- Alerts: messages standardized to `SQE · EVENT · {{ticker}} {{interval}}` so they identify symbol/timeframe on multi-chart setups (titles unchanged)

## v3.2 — 2026-06-28
- **Market profiles now actually differentiate asset classes.** Instead of nudging only two near-identical band constants, each profile sets four levers with a meaningful spread: band width (`bbMult` 1.9–2.5), edge proximity, and — the lever that really separates assets for a fade tool — regime tolerance (`adxMax` 20–28, `slopeMax` 0.35–0.55). Commodities (esp. Natural Gas) mean-revert through choppy trends, so they fade readily and use wider bands; Stocks/Indices trend persistently, so they get a stricter range filter and tighter bands.
- **Trigger re-checks structure** — a fade now also requires price still in the lower/upper third of the range (`rangePos < 0.35` / `> 0.65`), so a stale armed extreme can't fire once price has left the edge.
- **Consistent Watch state** — `longWatch`/`shortWatch` are now gated by the regime, so the internal state matches the chart/alerts instead of being only visually hidden in trends.
- **Safer arming** — `barssince()` is explicitly `na`-guarded before the confirmation-window comparison.
- **Clamped Bollinger-Z** (`±4`) so a very small stdev can't briefly distort the exhaustion score.
- **Leaner default chart** — the pivot reference and the dashboard table are now off by default (toggle them on in Visuals when needed). Trigger labels, Setup/Watch markers, mean & bands, and ATR risk levels stay on.
- **Range regime gate** — the tool now verifies the market is actually ranging before it fades an edge (`ADX < 24` and `|EMA50 slope| < 0.45 ATR/bar`). Previously it would fade pullbacks in strong trends; in a trend it now stands down (dashboard status `Trending — fade off`, no chart markers, no alerts).
- **Sharper edge detection** — "near high/low" now also requires price in the outer fifth of the 80-bar range (`rangePos > 0.80` / `< 0.20`), not just proximity to a trending extreme.
- **Sweep-and-reclaim rejection** — the candle trigger now requires a liquidity sweep of the prior bar's extreme with a close back inside (or a stronger 0.40 wick), replacing the looser `close < low[1]` breakdown that could mark trend continuation.
- **Risk levels persist** — SL/TP1/TP2 stay plotted for 20 bars after a trigger instead of only on the signal candle.
- **Grade coupled to strictness** — A+/A/B/C are now relative to the active score threshold, so a triggerable setup always reads at least B regardless of preset.
- **TF hint** softened — intraday < 1H reads `Low TF noisy`, 4H `4H OK`, otherwise `Check context`.

## v3.1 — 2026-06-28
- **More signals: removed the separate momentum gate.** v3.0 stacked an extra momentum-turn requirement (Watch) on top of the exhaustion score *and* the candle rejection, which starved the triggers (many yellow/gray markers, almost no labels — and almost no longs). Momentum is already a component of the exhaustion score, so the gate was redundant. Now the trigger mirrors the Exhaustion Scanner: score-extreme + candle rejection, nothing else.
- **Confirmation window** — a candle rejection within `Confirmation Window` bars (default 3) after an exhaustion extreme still triggers, so the rejection need not be exactly on the extreme bar.
- **Lower Balanced threshold** (42 → 38; Strict 50 → 48; Very Strict 58 → 56) for more setups, especially on the bottom-fade (long) side.
- **Removed** the `Momentum Sensor` and `Momentum Window` inputs (the momentum machinery they drove is gone); added `Confirmation Window`. Watch now means "extreme reached, rejection pending".

## v3.0 — 2026-06-28
- **Switched the one model to a range fader.** v2.0's trend-pullback logic was the wrong tool for a ranging instrument (it stays quiet when there's no trend), so it produced no tradeable signals on a range-bound NatGas 4H. 3.0 keeps the "one clean thing" principle but makes that thing a **range fader**: long the exhausted lows, short the exhausted highs.
- **Exhaustion score (0–100)** adapted from the validated Exhaustion Scanner top/bottom logic, trimmed to three components: **Distance** (stretch past the mean, EMA-ATR + Bollinger-Z), **Structure** (recent high/low proximity + wick rejection + close beyond the band), **Momentum** (RSI/StochRSI/WT overbought-oversold). Weighted 40/30/30.
- **Same three tiers, one logic** — Edge (which side is exhausted) → Setup (exhaustion building) → Watch (momentum turns back off the edge, windowed) → Trigger (candle rejects + score clears threshold + cooldown).
- **Candle-rejection confirmation** (closes back off the edge) and the momentum window carried over from 2.0.
- **Thresholds lowered** to match exhaustion-score magnitudes (Balanced 42 / Strict 50 / Very Strict 58; grades A+ 75 / A 62 / B 50 / C 38). Profiles now tune band width and high/low proximity. Risk levels are mean-reversion oriented (SL beyond the edge, TP1 = mean, TP2 = opposite band).
- **Trade-off (by design):** built for ranges. In a strong trend it is intentionally quiet — use a trend tool there. Still no `request.security`, no MTF, no divergence, no pivot signals.

## v2.0 — 2026-06-28
- **Refocus on one model done well: a 4H trend-pullback engine.** v1.1–1.4 had drifted into a do-everything tool (auto-regime, mean-reversion, MTF divergence, range-fade) where it was no longer clear *why* a signal fired. 2.0 strips back to a single, legible logic: trend direction → pullback into the trend → momentum turns back in → candle confirms → score → Trigger.
- **Removed:** auto-regime / dual model, mean-reversion / range-fade, MTF bonus/malus and the LTF "divergence" proxy (it was only a 5-bar compare over a compressed `request.security` state — not a real pivot divergence), the regime discount, and the range-band inputs. No `request.security` at all now — fully chart-TF, no repaint.
- **Stable directional Bias** — the bias holds its last clear trend state (`var biasDir`) and only flips on a clear opposite trend, instead of "which score is higher", which could flip on score noise.
- **Momentum window** — a momentum turn now stays valid for `Momentum Window` bars (default 3), so a one-bar timing miss no longer voids the setup (the old `momTurn`-on-the-exact-bar requirement was too punctual).
- **One coherent score** — trend quality (slope strength), market quality, pullback depth, momentum and candle confirmation. Bias/Setup/Watch/Trigger all live inside this single logic.

## v1.4 — 2026-06-27
- **Horizon-correct regime detection** — `trendiness` is now a long-horizon (40-bar) Kaufman efficiency ratio instead of the 10-bar slow-HMA slope. The old slope read "Trend" on every individual swing of a large range, so the mean-reversion model never engaged at the turning points and the range edges were left untraded. The long ER stays low across a range (low net displacement vs. total path) even when its legs are fast, so MR now activates throughout a range and fades the actual edges. Regime classification only — not a signal gate.
- Thresholds unchanged in spirit: `trendiness ≥ 0.6` = Trend, `≤ 0.3` = Range; ER mapped 0.25 → 0.55.

## v1.3 — 2026-06-27
- **Regime-adaptive signal model** — the engine now switches logic by regime instead of only discounting trend signals in a range. In a **trend** it takes trend pullbacks; in a **range** it takes mean-reversion fades at the range edges (buy the lower band, sell the upper band as momentum turns back in). This fixes the v1.2 problem of too few, badly located signals: trend-following in a range was entering at the wrong end (shorting near the range low). The `Signal Model` input is now `Auto (Adaptive)` (default), `Trend Pullback`, or `Mean Reversion` (force one).
- **Range-relative location** — mean-reversion zones are the lower/upper `Range Band (fraction)` of the recent 20-bar range (default 0.30), so they adapt to range width. Pivot-free. Replaces the fixed ATR-stretch.
- **Model-aware tradability** — a range has low efficiency by nature, so the ER-based market-quality gate no longer blocks mean-reversion. Trend signals still require efficiency (`marketQuality ≥ 45`); range signals only require enough amplitude (`range ≥ 2.5 ATR`). Resolves the contradiction where a range was flagged "too weak" exactly when mean-reversion wanted to trade it.
- **Regime row** now also shows the active model (`Range · MR`, `Trend · Trend`, `Transition · Both`); Market row shows model-aware OK/Weak with quality and range-amplitude readouts.
- **Removed** the old weakness-gated reversal path and the counter-trend penalty (superseded by the adaptive model).

## v1.2 — 2026-06-27
- **Range/Trend regime** — trend conviction is now discounted by `trendFactor` (0.45× in a range … 1.0× in a trend), derived from the slow-HMA slope over 10 bars in ATR units. In a sideways market a "trend pullback" is really a range swing, so its score drops and it surfaces as Watch instead of a Trigger — directly cutting the whipsaw cluster of opposing signals seen inside ranges. Situation-driven and symmetric; no hard gate.
- **Regime dashboard row** — Trend / Transition / Range, colored.
- **Compact signal labels** — `L 82` / `S 79` (tiny) so neighbouring signals no longer overlap; full score on hover.
- **Tighter Setup/Watch bands** — setup `scoreMin − 15` (was −20), watch `scoreMin − 7` (was −10), reducing gray-circle clutter.

## v1.1 — 2026-06-27
- **Three-tier read (Bias → Setup → Trigger)** — the indicator is no longer trigger-only. Bias (preferred direction + both side scores) is always shown, so the chart is never empty
- **Setup / Watch markers** — gray circle = setup forming (location of interest, market tradable, no trigger yet), yellow circle = watch (momentum leaning in, trigger near). Only the dominant-bias side is surfaced; triggers still print as labels
- **Soft market quality (0–100)** — replaced the hard `er > erMin and atrRatio > atrMin` block with a graded blend (`marketQuality >= 45`). A forming range/compression no longer reads "Weak / Choppy" just because one value dips
- **Optional MTF bonus / malus (`Use MTF Bonus / Malus`, off by default)** — a higher-TF trend bias (default Daily, non-repainting) and a lower-TF regular divergence (default 1H) add a soft score bonus when aligned / a malus when the HTF opposes. Never a gate, never a kill-switch
- **Dashboard "why no trigger"** — new Bias / Status / Action rows: Status spells out the current tier (No setup / Market too weak / Setup building / Watch — trigger pending / Trigger active); Market row shows the numeric quality
- **Watch alert** — `SQE Watch` fires when a setup matures, so a maturing idea can be caught before the trigger

## v1.0 — 2026-06-27
- Initial release
- 4H-first signal overlay with composite 0–100 setup-quality score and A+/A/B/C grades
- Six market profiles (Natural Gas, Oil, Gold/Silver, Broad Commodities, Stocks/Indices, Generic Futures) tuning ER floor, ATR-expansion floor and pullback depth
- Two signal models: Trend Pullback, and Auto (Trend + weakness-gated Reversal)
- Pluggable momentum sensor (Stoch RSI / WaveTrend)
- Strictness presets (Very Strict / Strict / Balanced) driving score threshold + cooldown
- ATR risk levels (SL / TP1 / TP2)
- Pivot reference markers as a pure control overlay; reversal location judged by pivot-free ATR-stretch from the slow HMA
- Light-theme dashboard and long/short/any alerts
