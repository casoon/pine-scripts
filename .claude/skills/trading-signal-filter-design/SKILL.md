---
name: trading-signal-filter-design
description: Methodik zum Entwerfen und Validieren von Filtern/Gates in regelbasierten Trading-Strategien (jeder Markt, jedes Tool — nicht Pine-spezifisch) — wann ein Filter wirkt vs. wertlos ist, wie man das vor der Implementierung abschätzt, und in welcher Reihenfolge man an einer Strategie arbeitet. Destilliert aus mehreren verworfenen Gate-Hypothesen in echten Backtests (Aggregat-Trugschluss, zu kleines Blockvolumen, Capture-Rate vs. avgR) sowie dem Mehrfachvergleichs-/Overfitting-Risiko beim iterativen Testen mehrerer Gate-Varianten gegen denselben Datensatz. Nutzen beim Design neuer Entry-/Exit-Filter, bei der Analyse von Backtest-Ergebnissen nach Gate-/Filter-Wirkung, wenn eine Filter-Idee aus aggregierten Statistiken abgeleitet wurde, oder wenn ein Gate/Filter nach mehreren Testläufen auf demselben Datenfenster in die Standard-Konfiguration übernommen werden soll ("ist das Ergebnis schon Out-of-Sample bestätigt", "wie viele Varianten wurden schon gegen diese Daten getestet"). Nicht für die Implementierung selbst (Pine-Syntax siehe pine-script-v6-language) und nicht für allgemeines Code-Debugging (siehe systematic-debugging).
---

# Trading Signal Filter Design

## Gotchas — warum Gates in der Praxis scheitern

- **Aggregat verbirgt TF-/Richtungs-Muster.** Ein Befund über alle Timeframes/Richtungen hinweg (z. B. "Setup A performt besser als Setup B") kann für eine einzelne TF/Richtungs-Kombination exakt umgekehrt sein. Eine Gate-Hypothese muss aus einer Auswertung stammen, die pro Timeframe UND pro Richtung getrennt aufgeschlüsselt ist — nicht aus dem Gesamtdurchschnitt.
- **Erwartetes Blockvolumen vor Implementierung schätzen — als Heuristik, nicht als Beweis.** Ein Filter, der unter ~5 % der Signale blockiert, braucht eine sehr große Effektgröße in der blockierten Teilmenge, um überhaupt sichtbar zu werden (Beispielfall aus einem konkreten Backtest: 18 von 1500+ Signalen blockiert, avgR/WR unverändert — die blockierte Teilmenge war dort nicht extrem genug). Das ist kein mathematisches Gesetz: ein seltener Filter, der gezielt wenige extreme Tail-Verluste abfängt, kann avgR trotzdem deutlich verschieben. Vor der Implementierung sowohl das erwartete Blockvolumen **als auch** die avgR/Verteilung der voraussichtlich blockierten Teilmenge schätzen — ein niedriges Blockvolumen ist ein Grund für genaueres Hinsehen, kein automatisches Verwerfungskriterium.
- **avgR-Verbesserung allein reicht nicht — Capture-Rate als unabhängige zweite Prüfung.** Steigt avgR nach einem Filter, aber die Capture-Rate (getroffene vs. verfügbare Trades) fällt stärker als avgR steigt, ist das ein eigenständiges Warnsignal für Selektionsneutralität (der Filter entfernt gute und schlechte Trades im ähnlichen Verhältnis und sieht wegen der kleineren, verzerrten Stichprobe nur besser aus) — unabhängig vom Blockvolumen-Check oben, nicht als dessen zwingende Folge.
- **"Regime X = schlecht" ist keine Universalregel.** Ein Zustand (z. B. niedrige Volatilität, ein bestimmter Chop-Wert) kann je nach Instrument/TF/Richtung unterdurchschnittlich ODER überdurchschnittlich performen. Ein Regime-Filter ohne Selektion *innerhalb* des Regimes blockiert ganze Cluster undifferenziert — inklusive der besten Setups darin.
- **Bestätigungs-Lag von Referenzpunkten (Pivots o. ä.) ≠ "Signal ist zu spät".** Ein Referenzpunkt, der erst nach N Bars bestätigt wird, lässt sich nicht direkt in eine "wie weit ist die Bewegung schon gelaufen"-Schwelle übersetzen — das Verhältnis kippt je nach Timeframe, weil Bewegungen auf höheren TFs strukturell länger laufen.
- **Pivots/Referenzpunkte sind Kontext, kein Trigger.** Starker Default, keine Naturkonstante: die Regel stammt aus einem konkreten Fall, in dem ein Pivot mit fester Bestätigungsverzögerung (N Bars, bevor der Pivot als bestätigt gilt) als Trigger-/Gate-Abhängigkeit verwendet wurde und dadurch dessen Lag unbemerkt in die Signal-Logik vererbt hat. Jeder Referenzpunkt mit einer vergleichbaren Bestätigungsverzögerung ist gefährdet — ein Pivot- oder Struktur-Overlay dient der Einordnung, nicht als Abhängigkeit für Signal-Auslösung, -Bewertung oder Deduplizierung. Ist der Mechanismus (Lag der Bestätigung) im Einzelfall nicht gegeben, prüfen statt die Regel blind zu übernehmen.
- **Mehrere Hypothesen gegen denselben Datensatz sind ein Mehrfachvergleichs-Problem.** Wird Hypothese 1 verworfen, Hypothese 2 aus denselben Daten abgeleitet, Hypothese 3 usw. (eine laufende Testreihe auf demselben Backtest-Fenster), steigt mit jeder weiteren getesteten Variante die Wahrscheinlichkeit, zufällig einen Filter zu finden, der nur zum Zufallsrauschen dieses einen Fensters passt, nicht zu einem realen Muster. Ein "besser als die letzte Version"-Ergebnis aus derselben Iterationsreihe ist noch kein Fund.

## Out-of-Sample-Bestätigung vor Promotion

Ein Gate, das iterativ gegen denselben Datensatz optimiert wurde, hat sich mit steigender
Iterationszahl zunehmend an dessen Rauschen angepasst statt an ein reales Muster. Vor der
Übernahme in die Standard-/Live-Konfiguration:

1. **Iterationszähler mitführen.** Wie viele Gate-Varianten wurden bereits gegen dasselbe
   Datenfenster getestet? Mit jeder weiteren Variante sinkt die Aussagekraft eines einzelnen
   "besser als vorher"-Ergebnisses.
2. **Bestätigung auf einem unabhängigen Fenster verlangen**, bevor ein Gate übernommen wird —
   anderer Zeitraum oder anderes Instrument als das Fenster, aus dem die Hypothese stammt.
3. **Keine Rückwärts-Erklärung als Bestätigung akzeptieren.** "Es performt auf den neuen Daten
   besser, und wir können auch erklären warum" ist keine Out-of-Sample-Bestätigung, solange die
   Erklärung erst nach Kenntnis des Ergebnisses gebaut wurde — genau das ist der Mechanismus
   hinter dem Mehrfachvergleichs-Risiko.
4. **Verworfene Hypothesen dokumentieren, nicht nur die gewählte.** Ein Log verworfener Gates
   (Hypothese, Datenbasis, tatsächliche Wirkung, Diagnose) macht sichtbar, wie viele Versuche in
   ein Ergebnis eingeflossen sind — ohne das Log wirkt jeder einzelne Fund isolierter und
   überzeugender, als er in der Gesamtreihe tatsächlich ist.

## Reihenfolge: Fundament vor Feintuning

1. **Strategische Hebel zuerst** (große Wirkung, wenige Freiheitsgrade): Exit-Logik (Trailing-/Structural-Exit statt fixed-R), Signal-Qualität (Divergenzen, struktureller Kontext), Higher-Timeframe-Confluence.
2. **Erst danach Feintuning** (kleine Wirkung, viele Freiheitsgrade): per-TF-Schwellwerte, per-TF/Richtung-Bänder, Mikro-Cluster-Optimierung.

Feintuning auf einer Strategie mit struktureller Exit-Schwäche optimiert auf das falsche Ziel — eine Mikro-Verbesserung aus Richtungs-/TF-Tuning (z. B. +0.05R) wird vom strukturellen Defizit (z. B. fehlender Trailing-Stop, der +0.30R kosten würde) überlagert, bevor sie überhaupt sichtbar wird.

**Anti-Pattern:** feinere Bänder pro TF/Richtung anlegen, während die Haupt-Exit-Strategie das dominante Verlustmuster im Ergebnis ist.

## Symmetrie-Prinzip

Regeln müssen für long/short (bzw. beide Richtungen eines Systems) symmetrisch sein — kein hartcodiertes "long braucht X, short braucht Y". Asymmetrisches Verhalten muss aus der **Situation** kommen (Regime, Marktphase, Kontext), nicht aus der Richtung selbst. Ein Regelwerk, das pro Richtung unterschiedliche Schwellen fest verdrahtet, hat mit hoher Wahrscheinlichkeit ein Regime-Problem, das als Richtungs-Problem getarnt ist.

## Checkliste vor jedem neuen Gate

- [ ] Hypothese auf TF-/Richtungs-Ebene konsistent geprüft, nicht nur im Aggregat
- [ ] Erwartetes Blockvolumen **und** avgR/Verteilung der voraussichtlich blockierten Teilmenge aus echten Daten geschätzt (< 5 % Blockvolumen ohne belegte hohe Effektgröße dort ist ein Warnsignal, kein automatisches Aus)
- [ ] Effekt sowohl auf avgR als auch auf Capture-Rate geprüft
- [ ] Keine Richtungs-Hardcodierung — Asymmetrie kommt aus Regime/Kontext, nicht aus long/short
- [ ] Referenz-/Kontextwerte (z. B. Pivots) nicht als Trigger- oder Gate-Abhängigkeit verwendet — nur als Overlay
- [ ] Bei Ableitung aus einer laufenden Testreihe auf demselben Datensatz: Out-of-Sample-Bestätigung auf unabhängigem Fenster/Instrument vor Übernahme in die Standard-Konfiguration

## Bei negativem Befund: weiterarbeiten, nicht abbrechen

Wenn jemand einen konkreten Defekt am aktuellen Ergebnis benennt, ist das Ergebnis nicht "optimal" — am genannten Problem weiterarbeiten, statt das Ergebnis zu verteidigen oder die Analyse für abgeschlossen zu erklären.
