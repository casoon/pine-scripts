# NG Reversal System — Visuelle Anleitung

## Übersicht

Das System besteht aus 4 Indikatoren, die zusammen auf einem NatGas 4H Chart laufen.

| Skript | Typ | Datei |
|--------|-----|-------|
| NG Reversal Labeler | Overlay | `ng_reversal_labeler_4h.pine` |
| NG Structure & Zones | Overlay | `ng_structure_zones_4h.pine` |
| NG Feature Exporter | Panel | `ng_feature_exporter_core_4h.pine` |
| NG Reversal Score | Panel | `ng_reversal_score_4h.pine` |

---

## 1. NG Reversal Labeler (Overlay)

Markiert historische Wendepunkte direkt im Chart — mit Qualitäts- und Timing-Unterscheidung.

### Labels

| Element | Bedeutung |
|---------|-----------|
| ▲▲ grün (groß, kräftig) | **Strong Bull** — großer Move, schnell erreicht, geringe Gegenbewegung |
| ▲ grün (klein, blass) | Weak Bull — Reversal vorhanden, aber schwächer oder langsamer |
| ▼▼ rot (groß, kräftig) | **Strong Bear** — großer Move, schnell erreicht, geringe Gegenbewegung |
| ▼ rot (klein, blass) | Weak Bear — Reversal vorhanden, aber schwächer oder langsamer |

### Timing-Suffixe

| Suffix | Bedeutung | Kriterium |
|--------|-----------|-----------|
| ⚡ | **Fast** — Signal war früh und brauchbar | Ziel in ≤ 4 Bars erreicht |
| (kein) | Normal — solides Timing | Ziel in ≤ 8 Bars |
| ~ | Slow — Signal war spät / noisy | Ziel in > 8 Bars |

Beispiel: `▲▲ ⚡` = Strong Bull, fast — bester Fall. `▼ ~` = Weak Bear, slow — schlechtester Fall.

### Qualitätskriterien

Ein Reversal gilt als **strong**, wenn:
- der Kurs das große Ziel erreicht (2.5× ATR in 16 Bars), ODER
- das kleine Ziel (1.5× ATR) schnell erreicht wird (≤ 4 Bars) bei geringer Gegenbewegung (≤ 0.3× ATR)

Alles andere ist **weak**.

### Tooltips

Hover über jedes Label zeigt:
- **Move** — erreichter Move in ATR
- **MAE** — Max Adverse Excursion (größte Gegenbewegung in ATR)
- **Bars** — wie viele Bars bis zum Ziel
- **Timing** — Fast / Normal / Slow

### Tabelle (Research-Modus, oben rechts)

Zwei Sektionen:
- **Qualität:** Bull Strong / Bull Weak / Bear Strong / Bear Weak — Count + Prozent
- **Timing:** Fast / Normal / Slow — Count + Prozent aller Signale

**Wichtig:** Die Labels schauen in die Zukunft. Sie zeigen, wo rückblickend ein Reversal begonnen hat. Das ist kein Live-Signal, sondern Forschungsdaten.

---

## 2. NG Structure & Zones (Overlay)

Kombiniertes Skript für strukturelle Events UND automatische S/R-Zonen in einem einzigen Overlay.

### Event-Labels

#### Micro vs Major

Alle Swing- und BOS-Events werden auf zwei Ebenen erkannt:
- **Micro** (Pivot 3/3) — lokale Struktur, kürzere Swings
- **Major** (Pivot 7/7) — signifikante Struktur, längere Swings

#### Tier 1 — Wichtigste Events (groß, auffällig)

| Label | Bedeutung |
|-------|-----------|
| ★ SPRING | Major Spring — Fake Breakdown unter signifikantem Swing Low |
| spring | Micro Spring — Fake Breakdown unter lokalem Swing Low |
| ★ UPTHRUST | Major Upthrust — Fake Breakout über signifikantem Swing High |
| upthrust | Micro Upthrust — Fake Breakout über lokalem Swing High |
| ★ BOS ↑↑ / ★ BOS ↓↓ | Major Break of Structure |
| bos ↑ / bos ↓ | Micro Break of Structure |

#### Event-Qualität

Jedes Event bekommt eine Qualitätsstufe basierend auf 4 Faktoren:
- Wick-Größe (≥ 55% = stark)
- Candle Range (≥ 0.8× ATR = stark)
- Volumen (≥ 1.3× Durchschnitt = stark)
- Sweep-Tiefe (≥ 0.15× ATR = stark)

| Prefix | Qualität | Farbe | Kriterium |
|--------|----------|-------|-----------|
| ★ | **Strong** | kräftig | 3–4 Faktoren über Schwelle |
| (kein) | Normal | mittel | 1–2 Faktoren |
| ~ | Weak | blass | Gerade so qualifiziert |

#### Climax-Sequenz

| Label | Farbe | Bedeutung |
|-------|-------|-----------|
| Selling CLX / Buying CLX | fuchsia | Climax erkannt, Sequenz gestartet |
| TST ↑ / TST ↓ | lila | Test validiert |
| **CLX→TST→BOS ↑ / ↓** | **grün/rot, groß** | **Volle Sequenz — stärkstes Signal** |

Intern 5 Stufen: CLX → Reacting → Test Pending → Test Valid → Confirmed (nach BOS).

#### Weitere Events

| Label | Bedeutung |
|-------|-----------|
| FB | Fake Break — Ausbruch über/unter Swing Level, Close zurück |
| ★rej / rej / ~rej | Rejection (mit Qualität) |
| · | Swing High/Low (minimal) |

### Automatische Zonen

Aus den Events werden automatisch horizontale S/R-Zonen als farbige Boxen erzeugt.

#### Zonenquellen

| Typ | Quelle | Richtung |
|-----|--------|----------|
| Swing Zone | Major Swing High/Low | S/R |
| Spring Zone | Sweep Low → altes Swing Low | Support |
| Upthrust Zone | Altes Swing High → Sweep High | Resistance |
| BOS Flip | Gebrochenes Major Swing Level | S↔R |
| Climax Zone | High/Low der Climax-Kerze | Nach Richtung |

#### Zonenstatus (Lebenszyklus)

| Status | Bedeutung |
|--------|-----------|
| Fresh | Neu erzeugt, noch nicht getestet |
| Tested | Preis hat die Zone berührt |
| Confirmed | Preis hat in der Zone reagiert |
| Broken | Zone durchbrochen |
| Flipped | Gebrochene Zone, Rolle gewechselt |

#### Zonendarstellung

- **Grüne Boxen** = Support
- **Rote Boxen** = Resistance
- **Amber Boxen** = Flip-Zonen
- Nur die besten N Zonen werden angezeigt (Default: 8), priorisiert nach Typ, Qualität, Status, Touches und Alter

#### Kernnutzen

**"Hier ist eine Zone, an der das Reversal-System ernst genommen werden sollte."**

**Tooltips:** Hover über jede Zone zeigt Typ, Status, Score, Touches, Qualität.

**Debug-Modus:** Steplines für Micro (dünn) und Major Swings (dick). Zonen-Labels mit Score-Werten.

**Research-Tabelle (oben rechts):** Event-Statistiken + Zonen-Übersicht (Total, Support, Resistance, Visible).

---

## 3. NG Feature Exporter (separates Panel)

Zeigt Indikatorwerte als Oszillator-Panel unterhalb des Charts.

**Plot-Gruppe wählbar über Input "Plot Group":**

| Gruppe | Was zu sehen ist |
|--------|-----------------|
| Momentum | RSI (gelb), Stoch RSI K (cyan), Stoch RSI D (orange) |
| Volume | MFI (teal), Relative Volume (lila) |
| Volatility | BB Width (orange), Candle/ATR (grün), BB Distance (cyan) |
| Trend | Price→EMA20 (gelb), EMA20→EMA50 (orange), Slope-Richtung (Punkte) |
| Candle | Body/Range % (gelb), Upper Wick % (rot), Lower Wick % (grün) |

**Research-Modus:** Tabelle mit aktuellen Feature-Werten.

---

## 4. NG Reversal Score (separates Panel)

Zwei-Ebenen-Scoring mit Regime-Filter, Level-Kontext, Follow-through und Konflikterkennung.

### Kernprinzip

Oszillatoren allein reichen nicht. Erst Setup + Strukturbestätigung + Follow-through = ernst nehmen.

### Zwei Ebenen

**Ebene A — Setup Score (Balken):**

| Baustein | Punkte |
|----------|--------|
| RSI in Extremzone | +1 |
| RSI dreht | +0.5 |
| MFI in Extremzone | +1 |
| MFI dreht | +0.5 |
| Stoch RSI / MACD (je nach Variante) | +0.5 bis +1 |
| Kurs weit von EMA20 | +1 bis +1.5 |
| Bollinger-Band berührt | +1 |
| Starker Wick | +1 |
| **An sinnvollem Level** | **+1** |
| Trend gegen Setup | -1 |
| Kein Volumen | -0.5 |
| Weit weg von jedem Level | -0.5 |

**Ebene B — Confirmation Score (Kreise):**

| Baustein | Micro weak | Micro strong | Major weak | Major strong |
|----------|-----------|-------------|-----------|-------------|
| Spring/Upthrust | +1.5 | +3.0 | +3.0 | +4.5 |
| BOS | +0.5 | +2.0 | +2.0 | +3.5 |
| Fake Break | +0.5 | — | +1.0 | — |
| CLX detected | +1.0 | | | |
| Test validated | +1.5 | | | |
| CLX→TST→BOS | +2.5 | | | |

### Event Decay

Confirmation verliert nach dem Event automatisch an Gewicht:

| Bars nach Event | Wirkung |
|----------------|---------|
| 0–3 | 100% |
| 4–6 | Linear abnehmend → 20% |
| >6 | 0% (abgelaufen) |

### Follow-Through

Nach einem Event wird geprüft (innerhalb 2–4 Bars):
- Gibt es ein höheres/tieferes Close?
- Hält der Preis über/unter dem Trigger-Level?
- Kommt kein Gegen-BOS?

### Status-Logik

| Status | Icon | Bedeutung |
|--------|------|-----------|
| — | · | Nichts los |
| WATCH | ○ | Setup baut sich auf |
| SETUP | ◈ | Setup stark, wartet auf Confirmation |
| ALERT | ⚡ | Struktur-Event, aber Setup zu schwach |
| PENDING | ◎ | Setup + Conf, Follow-through ausstehend |
| **CANDIDATE** | **◉** | **Setup + Conf + Follow-through — ernst nehmen** |
| **CONFLICTED** | **⊘** | **Widersprüchlich — nicht handeln** |
| EXPIRED | ◌ | Event zu alt |
| **FAILED** | **✗** | **Kein Follow-through oder Trigger verloren** |

### Konflikterkennung

| Konflikt-Typ | Erkennung |
|-------------|-----------|
| Setup-Konflikt | Bull + Bear Setup beide aktiv |
| Conf-Konflikt | Beide Seiten confirmed |
| Trend-Konflikt | Setup gegen starken Trend (ER > 0.45) |
| Opposed Candidate | Candidate + Gegenrichtung confirmed |

### Drei Alert-Typen

| Alert | Bedingung | Zweck |
|-------|-----------|-------|
| **REVIEW** | Setup ≥ 4, Conf ≥ 1.5, kein starker Konflikt | "Schau drauf" |
| **ACTION** | Setup ≥ 5, Conf ≥ 3, Follow-through ✓, kein Konflikt | "Ernsthaft prüfen" |
| **INVALIDATION** | Vorher Candidate, jetzt Failed | "Signal ist tot" |

Plus: **Trap Hint** wenn gescheitertes Reversal die Gegenrichtung signalisiert.

### Regime-Filter

| Regime | Setup-Score | Confirmation-Score |
|--------|------------|-------------------|
| RANGE | ×1.2 | ×1.0 |
| TREND | ×0.8 | ×1.3 |
| HIGH VOL | — | ×1.2 |
| LOW VOL | — | ×0.8 |

### Momentum-Varianten (umschaltbar)

| Variante | Bausteine |
|----------|----------|
| **A: RSI+MFI+MACD** (Default) | Sauberer |
| B: RSI+MFI+StochRSI | Schneller |
| C: All | Zum Vergleich |

### Hintergrundfarbe

| Farbe | Bedeutung |
|-------|-----------|
| Grün | CANDIDATE |
| Rot | Bear CANDIDATE |
| Grau-blau | CONFLICTED |
| Orange | FAILED |
| Amber | Beide confirmed |
| Blass grün/rot | PENDING |

### Status-Leiste (unten links)

Regime + Volatilität + Multiplier + Bull/Bear Status mit Setup/Conf Werten.

### Debug-Tabelle (oben rechts)

Setup-Komponenten mit ✓/·, Confirmation-Events, CLX-Sequenz-Status, Follow-through, Conflict Severity.

**Optional: Component Lines** — 4 Steplines für Setup/Conf getrennt.

---

## Display-Modi

Jedes Skript hat drei Modi (Input "Display Mode"):

| Modus | Was es zeigt |
|-------|-------------|
| Light | Nur das Wesentliche — Marker, Score, Zonen, Kernplots |
| Debug | Zusätzliche Werte, Swing-Lines, Zone-Scores, Statusinfos |
| Research | Alles — Tabellen, Statistiken, Timing, Export-Daten |

**Empfehlung:** Für den täglichen Blick "Light". Zum Analysieren "Research".
