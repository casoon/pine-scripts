# Kestrel Opportunity Lens

Ein Pine-v6-Indikator für den Preis-Chart: Er kennzeichnet Überdehnungen nach unten (Long) und nach oben (Short) und beobachtet anschließend innerhalb eines begrenzten Zeitfensters, ob sich Williams und Preis vom Extrem dieses Fensters lösen. Optional bestätigt ein drehender WaveTrend die Regel. Das ist ein eigenständiger, unkalibrierter Regelprototyp zur visuellen Untersuchung der Ideen aus Kestrel Lab V034, **keine Portierung der trainierten Modelle**.

## Features

- Long und Short als zwei unabhängige Zustandsmaschinen mit einem gespiegelten, gemeinsamen Regelsatz; Auswahl `Both` / `Long` / `Short`.
- Erholung wird vom Extrem des jeweiligen Fensters gemessen, nicht über einen rollierenden Rückblick.
- Zonenstart, aktives Beobachtungsfenster, Setup, Verfall und Review als schlichte Chart-Symbole mit Hover-Tooltip.
- Trendkontext (mit dem Trend / gegen den Trend / gemischt) wird an jedem Ereignis erfasst, filtert aber nichts.
- Dashboard mit Long- und Short-Spalte für die letzte geschlossene Kerze; Rohwerte, Kontext und Ereignisse im Datenfenster.
- Acht getrennte Alerts (je Richtung Start, Setup, Verfall, Review).
- Nur OHLC des Chart-Symbols; kein Volumen, Fremdsymbol oder Zukunftspivot.

## Verwendung

1. `kestrel_opportunity_lens.pine` vollständig in TradingViews Pine Editor kopieren und dem Chart hinzufügen.
2. Als Ausgangspunkt den zuvor untersuchten Capital.com-NATURALGAS-Chart mit normalen 4h-Kerzen verwenden. Andere Instrumente/Zeitebenen sind technisch möglich, aber nicht dadurch geprüft.
3. Oranger Punkt `●` unter der Kerze (Long) bzw. über der Kerze (Short) bedeutet Gelegenheit, nicht Einstieg. Orange Hintergrund bedeutet, dass mindestens ein Fenster aktiv ist, einschließlich der Bar, auf der es mit Setup oder Verfall endet. Grünes Dreieck `▲` bzw. rotes Dreieck `▼` bedeutet, dass alle eingeschalteten Regeln am Kerzenschluss erfüllt waren. Graues Kreuz `×` bedeutet Verfall ohne Setup.
4. Beim Überfahren mit der Maus zeigt jeder Marker die Werte, aus denen er entstanden ist: Williams, Abstand vom Fensterextrem in Punkten und ATR, WaveTrend, Bar im Fenster und Trendkontext. Beim Verfall zeigen ✓/✗, welche Bedingung auf der letzten Fensterbar fehlte.
5. Blaue Raute `◆` erscheint zwölf Bars nach einem Setup (einstellbar) auf derselben Seite wie das Setup. Bis dahin werden neue Gelegenheiten derselben Richtung standardmäßig unterdrückt; mit „Suppress new windows until review“ = aus wird jede gültige Gelegenheit erfasst, jedes Setup behält dabei seine eigene Review-Erinnerung. Der Tooltip nennt Setup-Schluss, aktuellen Schluss und den Trendkontext damals und jetzt. Das simuliert weder eine Position noch Stop, Fill oder Gewinn.
6. In „Alarm erstellen“ die gewünschte KOL-Bedingung und „Einmal pro Kerzenschluss“ wählen. Nach Einstellungsänderungen einen bestehenden Alarm neu erstellen, damit dessen gespeicherte Konfiguration aktualisiert wird.

## Regeldefinition

Williams-Rohwert = `100 * (close - lowest(low,14)) / (highest(high,14) - lowest(low,14))`; 0 liegt am Tief, 100 am Hoch, flache Spannen ergeben 50.

Beide Richtungen nutzen denselben Regelsatz, gespiegelt an der Mitte. Long arbeitet mit Williams, Schluss und Tief; Short mit 100 − Williams, negiertem Schluss und Hoch. Es gibt bewusst keine richtungsgetrennten Parameter: Unterschiede zwischen Long und Short sollen aus der Marktsituation sichtbar werden (Trendkontext), nicht aus einer festen Richtungsregel.

Ein Zonenstart entsteht bei Williams ≤ 20 (Long) bzw. ≥ 80 (Short), sofern seit der letzten Zonenbar dieser Richtung mehr als drei Bars vergangen sind. Akzeptierte Starts einer Richtung müssen außerdem mindestens den Episodenabstand auseinanderliegen (Default 12 Bars). Während eines aktiven Fensters (und, falls eingeschaltet, der Review-Sperre) werden keine weiteren Starts derselben Richtung angenommen; die Frist wird nicht verlängert. Long- und Short-Fenster können sich überschneiden; überlappende Ereignisse sind keine unabhängigen Beobachtungen.

Default: sechs Bars ab dem Start, einschließlich Startbar, dürfen ein Setup liefern; ohne Setup verfällt das Fenster auf seiner letzten Bar. Beim Start werden Williams-Extrem und Preis-Extrem (tiefstes Tief bzw. höchstes Hoch) festgehalten und im Fenster nur weiter fortgeschrieben, wenn ein neues Extrem entsteht. Alle folgenden Bedingungen müssen erfüllt sein (Long; Short gespiegelt):

- Williams liegt mindestens fünf Punkte über seinem Minimum seit Fensterstart und steigt gegenüber der Vorbar.
- Der Schluss liegt mindestens 0,25 ATR über dem tiefsten Tief seit Fensterstart und über dem vorherigen Schluss.
- Falls aktiviert: WaveTrend steigt gegenüber der Vorbar; kein Cross erforderlich.

Weil die Startbar das Extrem definiert, kann sie selbst kein Setup liefern, solange die Williams-Schwelle über null liegt.

Die drei Bedingungen messen alle dieselbe Preisbewegung aus etwas anderem Blickwinkel. Drei erfüllte Bedingungen sind deshalb keine drei unabhängigen Hinweise; WaveTrend ist eine Glättung derselben Preise, keine eigene Informationsquelle.

ATR ist hier der einfache 20-Bar-Mittelwert der True Range. WaveTrend nutzt HLC3, EMA10 für Mittelwert und absolute Abweichung, Faktor 0,015 und EMA21 für die Hauptlinie.

## Trendkontext

Trend aufwärts, wenn der Schluss über der EMA20 liegt und die EMA20 höher als vor fünf Bars steht; abwärts spiegelbildlich; sonst gemischt. Relativ zur Signalrichtung ergibt das „with the trend“, „counter-trend“ oder „mixed“. „mixed“ heißt nur, dass Schlusslage und EMA-Steigung nicht übereinstimmen – nicht zwingend ein Seitwärtsmarkt. Der Kontext steht in Tooltips, Dashboard und Datenfenster und ist **kein Filter**: Er soll zeigen, in welcher Lage ein Setup entstand, damit sich Pullbacks im Trend von Gegenbewegungen in einem laufenden Trend unterscheiden lassen.

## Datenfenster

Neben Williams, WaveTrend und Trendkontext (+1 / −1 / 0) stehen dort die Erholung je Richtung (während eines aktiven Fensters einschließlich der Setup- bzw. Verfallsbar, die es schließt) und je Richtung die Ereignisse Start, Setup, Verfall und Review als 1/0-Reihen. Für eine vollständige Stichprobe die Review-Sperre ausschalten; Ereignisse mit überlappenden Fenstern bleiben voneinander abhängig. Über „Chart-Daten exportieren“ lassen sie sich für eigene Auswertungen außerhalb von TradingView mitnehmen. Der Indikator selbst berechnet keine Ergebnisse nach dem Signal. Die Messung je Setup über mehrere Horizonte samt Baseline-Vergleich übernimmt die Evaluationsstrategie [`strategies/kestrel_opportunity_lens/`](../../../strategies/kestrel_opportunity_lens/).

## Zeit- und Datenvertrag

Zustandsänderungen, Marker und Alerts nur auf bestätigten Bars; mindestens 260 Bars Anlauf. Keine rückversetzten Markierungen, keine `request.security()`-Aufrufe. Datenfenster und EMA können auf der laufenden Kerze schwanken; das Dashboard zeigt bestätigte Bedingungen. Das Signal markiert eine Entscheidung am Schluss, keinen bereits erzielten Einstiegspreis. Nichtstandard-Charts sperren Signale. Brokerdaten, Sessiongrenzen und Historienlänge können Ergebnisse verändern.

Die Erholungsschwellen sind **neu gewählte illustrative Regeln**, keine aus Lab-Ergebnissen gelernten Werte. Der zuletzt stärkere Lab-Ansatz nutzte gelernte Koeffizienten einschließlich zusätzlicher Zustandsmerkmale. Diese fehlen hier bewusst; Lab-Kontoergebnisse lassen sich deshalb nicht auf dieses Skript übertragen. WaveTrend ist standardmäßig ausgeschaltet, weil sein Zusatznutzen im Lab von der jeweiligen Konfiguration abhing.

## Prüfstand

Header, Datenvertrag, Indexeinträge und Signal-Logik lokal statisch geprüft. Noch nicht mit TradingViews Pine-Compiler oder Bar Replay geprüft; keine wirtschaftliche Validierung der Regeln, weder für Long noch für Short. Das Skript ist ein Draft und nicht veröffentlicht.

Technische Referenzen: [Bar states](https://www.tradingview.com/pine-script-docs/concepts/bar-states/), [Alerts](https://www.tradingview.com/pine-script-docs/concepts/alerts/).
