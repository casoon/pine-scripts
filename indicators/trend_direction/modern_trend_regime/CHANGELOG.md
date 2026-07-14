## v1.3.1 — 2026-07-14
- Trend-confirmation marker restyled again — from the flag-style `BULL`/`BEAR` text label to a small hollow triangle (`label.style_triangleup`/`triangledown`, `size.tiny`) carrying the same information as a hover tooltip instead of inline text

## v1.3.0 — 2026-07-14
- Trend classification changed from a hard 5-condition AND-chain (ADX, efficiency ratio, DI, line stack, price) to a factor score (`requiredTrendScore`, 4 of 5; 5 of 5 for Range Trading) — on volatile instruments (e.g. NatGas) efficiency ratio rarely clears 0.42 even in a clear trend, which previously kept Trend from ever re-confirming after the first one, leaving almost no BULL/BEAR markers on the whole rest of the chart
- Threshold is set so direction alone (DI + stack + price, max 3 of 5) can never satisfy the default 4-of-5 requirement — ADX or efficiency ratio must always contribute, so a flat/ranging market with incidentally aligned lines still can't be scored as "Trend"

## v1.2.1 — 2026-07-14
- Strukturvorschau now defaults to on

## v1.2.0 — 2026-07-14
- Trend confirmation now fires on the regime transition itself (`isBullTrend`/`isBearTrend` turning true) instead of the raw Fast Trend / Trend Basis crossover — the crossover fired on every wiggle inside chop that hadn't earned a confirmed Range yet, producing misleading arrows; removed the now-redundant "Kursbestätigung verlangen" toggle since price confirmation is already part of the regime classification itself
- Restyled the trend-confirmation marker from a plain triangle+letter to a flag-style label (`BULL` / `BEAR`), matching the existing breakout marker style

## v1.1.0 — 2026-07-14
- Fixed base-line slope calculation — was comparing a 20-bar move against 1 ATR instead of normalizing per bar, which made Range detection almost unreachable; now correctly ATR-per-bar scaled, with adjusted preset thresholds
- Regime state machine now drops to Transition immediately when the current Trend/Range conditions stop holding, instead of holding the stale regime for several bars; only entering a new Trend/Range still needs confirmation bars
- Range detection changed from a hard 4-condition AND-chain to a 4-factor score (`requiredRangeScore`), so one borderline factor no longer blocks the whole read
- Trend candidates now also require DI in trend direction and close beyond the Trend Basis
- Trend Flips now require the base line to be moving with the cross (structure improving) and are gated by "not Range and not Range-candidate" instead of blocking Transition; removed the "Flips im Übergang erlauben" toggle since it's no longer applicable
- Range corridor is now a real structure — boundaries are frozen from the swing high/low at Range entry instead of an ATR band around the Trend Basis that trailed price
- Range breakouts are now armed once per Range and fire at most once, replacing the fixed 3-bar breakout window
- Range reactions are now edge-detected (first touching bar only) instead of re-firing on every bar that tests the boundary
- Removed the now-unused Range-Korridor-Breite input (superseded by the frozen swing-based boundaries)
- Renamed "Zukunftsprojektion" to "Strukturvorschau" with a tooltip clarifying it's a visual offset, not a price forecast

## v1.0.0 — 2026-07-14
- Initial release: Trend / Range / Transition market-mode classification with confirmation filter
- Regime-gated trend flips with optional price confirmation
- ATR range corridor with edge reactions and separate breakout signals
- Six tuned presets (Standard, Schnell, Ruhig, Trendfolge, Range Trading, Ausbruch) plus Benutzerdefiniert
- Trendband, Range-Korridor, Regime-Leiste, Minimal and Alles visualization modes
- Optional future structure projection, bar coloring and transition background
