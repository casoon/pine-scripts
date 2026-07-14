# Modern Trend Regime

Simplified trend/range regime system without Ichimoku terminology. A three-line structure (Fast Trend, Trend Basis, Long-Term Structure) drives a confirmed market-mode classification — Trend / Range / Transition — that gates trend flips, range reactions and range breakouts so each signal only fires in the regime it belongs to.

## Features

- **Market mode classification** — Uptrend / Downtrend / Range / Transition from ADX, efficiency ratio, DI direction, line stack, price position, base-line slope and structure compression; both Trend and Range use a factor score (not a hard AND-chain) so one weak factor doesn't kill the whole read
- **Immediate-transition state machine** — losing a confirmed Trend or Range drops straight to Transition on the next bar; only *entering* a new Trend or Range needs the confirmation-bar count
- **Regime-driven trend confirmation** — a small triangle marker (hover for details) fires on the regime transition itself (`isBullTrend`/`isBearTrend` turning true), not on the raw Fast Trend / Trend Basis crossover — a crossover in a still-unconfirmed chop no longer produces a signal
- **Real range structure** — corridor boundaries are frozen from the swing high/low at Range entry (not a moving ATR band), so reactions and breakouts are measured against an actual range, not a channel that trails price
- **One-shot breakout arming** — a breakout can fire at most once per Range, and reactions are edge-detected so a multi-bar boundary test doesn't repeat the signal
- **Six tuned presets** — Standard, Schnell, Ruhig, Trendfolge, Range Trading, Ausbruch, plus Benutzerdefiniert for full manual control
- **Multiple visualization modes** — Trendband, Range-Korridor, Regime-Leiste, Minimal, or Alles, plus an optional structure preview (visual offset only, not a forecast), bar coloring and transition background

## Market modes

| Mode | Condition |
|---|---|
| Trend (up/down) | At least `requiredTrendScore` of 5 factors true: ADX above trend threshold, efficiency ratio above trend threshold, DI in trend direction, the three lines stacked in trend direction, close beyond the Trend Basis. All presets need 4 of 5 (so ADX or efficiency ratio must always contribute — direction alone can't reach 4), Range Trading needs 5 of 5 |
| Range | At least `requiredRangeScore` of 4 factors true: ADX below range threshold, efficiency ratio below range threshold, base-line slope (per bar, ATR-normalized) below the slope threshold, structure width below the compression threshold. Range Trading needs 3 of 4, all other presets need all 4 |
| Transition | Neither Trend nor Range is confirmed |

A candidate **Trend or Range** must persist for **Bestätigungskerzen** consecutive bars before it becomes the active `marketRegime`. Losing an active Trend/Range, however, drops to Transition on the very next bar — the old regime is never held past the point where its own conditions stop being true.

## Presets

| Preset | Character |
|---|---|
| Standard | Original default parameters (fast=9 / base=26 / slow=52) |
| Schnell | Shorter lengths and lower thresholds — reacts earlier, more regime changes |
| Ruhig | Longer lengths and higher confirmation — fewer, more stable regime changes |
| Trendfolge | Higher trend-efficiency requirement, longer base length — favors persistent trend detection over range detection |
| Range Trading | Wider range-efficiency/compression tolerance, only 3-of-4 required range score, and a stricter 5-of-5 required trend score — biases every tie toward Range over Trend |
| Ausbruch | Balanced regime detection with a larger breakout buffer — tuned for the range-breakout signals |
| Benutzerdefiniert | Uses the manual values from the "– Benutzerdefiniert" input groups |

Switching away from **Benutzerdefiniert** overrides the corresponding manual inputs; the manual groups remain visible so values can be prepared before switching to Benutzerdefiniert.

## Signals

- **Trend Confirmed** (small triangle, hover for text) — `marketRegime` just switched to Uptrend/Downtrend; already passed the score-based Trend check, DI direction, price confirmation and the confirmation-bar count, so it fires once per genuine regime change instead of on every Fast/Base wiggle
- **Range Reaction** (`R`) — price touches and rejects the frozen range boundary while in Range mode (first touching bar only)
- **Range Breakout** (`BREAK`) — price closes beyond the frozen range boundary plus buffer after leaving Range mode; fires at most once until the next Range

Trading off against the old crossover-based flip: this version fires later (only after `Bestätigungskerzen` bars of confirmation) but no longer produces a signal on chop that hasn't earned a regime change.
