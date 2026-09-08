# Klinger Volume Force Map

Volume-force analysis based on Stephen J. Klinger's original 1997 concept. It accumulates volume force while the H+L+C trend direction persists (resetting on each trend flip), takes the spread between a fast and a slow EMA of that force against its own EMA-based signal line, and normalizes the result so it stays comparable across instruments. On top of the raw oscillator it runs a hysteretic Bull/Neutral/Bear regime engine, confirmed-pivot divergence detection, and continuation/structure-break event detection.

## Features

- Original 1997 Volume Force formula as default, with alternative formula variants (TradingView documentation formula, simplified signed-volume baseline) for research/comparison
- Raw KVO remains the source of all zero/signal-cross logic regardless of display normalization
- Zero-preserving normalization (`KVO / EMA(abs(KVO), N)` by default, or StdDev scale, or raw) for readable cross-market visualization
- Momentum histogram (KVO − Signal) with acceleration/deceleration coloring
- Hysteretic Bull / Neutral / Bear regime engine, with Strong Bull / Strong Bear expansion states
- Confirmed regular + hidden divergence detection on confirmed PRICE pivots
- Divergence quality filter using ATR displacement, KVO displacement, and pivot separation
- Bull/Bear Flow Rejection continuation events
- Flow-confirmed structural breakouts
- Clean / Analysis / Research visual modes
- Optional price-chart divergence and event overlays
- Compact current-state dashboard plus research diagnostics (formula correlation/disagreement)

## Instrumente

- **Gültig:** jedes Symbol, dessen `syminfo.volumetype` `"base"` oder `"quote"` meldet — in der Regel Futures, börsennotierte Aktien und Krypto-Börsen, dazu Broker-Feeds, die echte gehandelte Menge durchreichen.
- **Näherung:** ist dieses Volumen der Anteil eines einzelnen Brokers (ein CFD-Feed, der `"base"` meldet), beschreibt der Oszillator dessen Fluss, nicht den der Börse — brauchbar als Näherung, nicht als Börsenvolumen.
- **Ungültig:** jedes Symbol mit `"tick"` (Zahl der Preis-Updates) oder `"n/a"` — dort gibt es nichts zu gewichten.
- Der Indikator prüft das zur Laufzeit über einen `volumetype`-Guard. Ist kein echtes Volumen vorhanden, bleiben Oszillator, Signal-Linie, Histogramm, Regime-Engine und Divergenzerkennung leer (kein Plot, keine Fehlinterpretation) und ein einmaliges Warn-Label ("benötigt echtes Handelsvolumen — aktuell: …") erscheint im Panel.
- **Referenzmarkt-Variante (z.B. `NYMEX:NG1!`) — bewusst nicht implementiert:** Die Klinger Volume Force ist ein reiner Oszillator ohne absoluten Preislevel, ein Cross-Symbol-Wert würde also anders als bei VWAP keine Preisniveaus mischen. Das ändert aber nichts daran, dass ein `request.security()`-Aufruf auf ein Fremdsymbol laut `DATA_VALIDITY.md` §4.1 die Ausnahme bleibt, nicht der Standard: Latenz, Settlement-Unklarheit, Session-Versatz, Request-Budget, Repaint-Risiko und Symbol-Mapping sind sechs zusätzliche Fehlerquellen, die ein Einzelindikator nicht tragen sollte. Diese Abwägung ist hier dokumentiert, aber nicht umgesetzt — der Indikator degradiert stattdessen hart auf `Exchange-only`.

## Notes

- Divergences use confirmed price pivots — a divergence is only emitted after `Pivot right bars` have elapsed. This avoids repainting a still-forming pivot at the cost of confirmation delay.
- The default normalization divides KVO, Signal, and the histogram by the same denominator (`EMA(abs(KVO), N)`), which preserves zero crossings and KVO/Signal crossings while making the pane comparable across instruments.
- "StdDev scale" intentionally uses `KVO / stdev(KVO)`, not a mean-subtracted Z-score, so the semantic KVO zero line doesn't move.
- Requires real trade volume (`syminfo.volumetype` `base`/`quote`). On CFDs, Forex, and most indices the indicator produces no output — see Instrumente above.
