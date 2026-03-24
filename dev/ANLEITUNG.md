# NG Reversal System — Visuelle Anleitung

## Übersicht

Das System besteht aus 4 Indikatoren, die zusammen auf einem NatGas 4H Chart laufen.

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

## 2. NG Feature Exporter (separates Panel)

Zeigt Indikatorwerte als Oszillator-Panel unterhalb des Charts.

**Plot-Gruppe wählbar über Input "Plot Group":**

| Gruppe | Was zu sehen ist |
|--------|-----------------|
| Momentum | RSI (gelb), Stoch RSI K (cyan), Stoch RSI D (orange) |
| Volume | MFI (teal), Relative Volume (lila) |
| Volatility | BB Width (orange), Candle/ATR (grün), BB Distance (cyan) |
| Trend | Price→EMA20 (gelb), EMA20→EMA50 (orange), Slope-Richtung (Punkte) |
| Candle | Body/Range % (gelb), Upper Wick % (rot), Lower Wick % (grün) |

**Research-Modus:** Zeigt eine Tabelle mit den aktuellen Feature-Werten der letzten Bar.

**Zweck:** Visuell prüfen, welche Indikatoren bei den gelabelten Reversals (▲/▼) auffällige Werte zeigen.

---

## 3. NG Structure Events (Overlay)

Markiert strukturelle Ereignisse direkt im Chart. Labels sind nach Wichtigkeit gestuft und nach Qualität abgestuft.

### Micro vs Major

Alle Swing- und BOS-Events werden auf zwei Ebenen erkannt:
- **Micro** (Pivot 3/3) — lokale Struktur, kürzere Swings
- **Major** (Pivot 7/7) — signifikante Struktur, längere Swings

Major-Events sind visuell größer und prominenter als Micro-Events.

### Tier 1 — Wichtigste Events (groß, auffällig)

| Label | Bedeutung |
|-------|-----------|
| ★ SPRING | Major Spring — Fake Breakdown unter signifikantem Swing Low, Close zurück darüber |
| spring | Micro Spring — Fake Breakdown unter lokalem Swing Low |
| ★ UPTHRUST | Major Upthrust — Fake Breakout über signifikantem Swing High |
| upthrust | Micro Upthrust — Fake Breakout über lokalem Swing High |
| ★ BOS ↑↑ / ★ BOS ↓↓ | Major Break of Structure — bricht signifikanten Swing |
| bos ↑ / bos ↓ | Micro Break of Structure — bricht lokalen Swing |

### Event-Qualität

Jedes Event bekommt eine Qualitätsstufe basierend auf 4 Faktoren:
- Wick-Größe (≥ 55% = stark)
- Candle Range (≥ 0.8× ATR = stark)
- Volumen (≥ 1.3× Durchschnitt = stark)
- Sweep-Tiefe (≥ 0.15× ATR = stark)

| Prefix | Qualität | Farbe | Kriterium |
|--------|----------|-------|-----------|
| ★ | **Strong** | kräftig, voll | 3–4 Faktoren über Schwelle |
| (kein) | Normal | mittel | 1–2 Faktoren |
| ~ | Weak | blass | Gerade so qualifiziert |

### Tier 2 — Climax Sequenz

Der Climax wird nicht mehr einzeln betrachtet, sondern als Sequenz:

| Label | Farbe | Bedeutung |
|-------|-------|-----------|
| Selling CLX / Buying CLX | fuchsia | Climax-Kerze erkannt, Sequenz gestartet |
| TST ↑ / TST ↓ | lila | Test validiert — kleinere Range + weniger Volumen in Climax-Zone |
| **CLX→TST→BOS ↑ / ↓** | **grün/rot, groß** | **Volle Sequenz bestätigt — stärkstes Signal im System** |

Die Sequenz durchläuft intern 5 Stufen:
1. CLX detected → 2. Reacting → 3. Test Pending → 4. Test Valid → 5. Confirmed (nach BOS)

Timeout: Sequenz verfällt wenn zu viele Bars ohne Fortschritt vergehen.

### Tier 2 — Fake Breaks

| Label | Farbe | Bedeutung |
|-------|-------|-----------|
| FB | orange | Fake Break — Ausbruch über/unter Swing Level, aber Close zurück |

### Tier 3 — Dezente Events

| Label | Bedeutung |
|-------|-----------|
| ★rej / rej / ~rej | Rejection (mit Qualität) — starker Wick + kleiner Body |

### Tier 4 — Minimal

| Label | Bedeutung |
|-------|-----------|
| · (Punkt oben) | Swing High erkannt |
| · (Punkt unten) | Swing Low erkannt |

**Tooltips:** Hover über jedes Label zeigt Details: Qualitätsstufe, Sweep-Tiefe, Wick%, Volumen-Multiple.

**Debug-Modus:** Zeigt Steplines — dünne Linien für Micro Swings, dicke Linien für Major Swings.

---

## 4. NG Reversal Score (separates Panel)

Zwei-Ebenen-Scoring mit Regime-Filter, Level-Kontext und Konflikterkennung.

### Kernprinzip

Oszillatoren allein reichen nicht. NatGas kann extrem lange überdehnt bleiben. Erst wenn eine Strukturbestätigung dazukommt, wird ein Setup ernst genommen. Dabei werden Regime und Level-Kontext berücksichtigt.

### Zwei Ebenen

**Ebene A — Setup Score (Balken):**
Misst ob Momentum, Überdehnung, Candle, Volumen und Level-Kontext auf ein Reversal hindeuten.

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
Misst ob die Struktur das Setup bestätigt. Qualität der Events fließt ein.

| Baustein | Micro weak | Micro strong | Major weak | Major strong |
|----------|-----------|-------------|-----------|-------------|
| Spring/Upthrust | +1.5 | +3.0 | +3.0 | +4.5 |
| BOS | +0.5 | +2.0 | +2.0 | +3.5 |
| Fake Break | +0.5 | — | +1.0 | — |
| Climax Sequenz (progressiv): | | | | |
| — CLX detected | +1.0 | | | |
| — Test validated | +1.5 | | | |
| — CLX→TST→BOS confirmed | +2.5 | | | |

### Momentum-Varianten (umschaltbar)

| Variante | Aktive Bausteine | Zweck |
|----------|-----------------|-------|
| **A: RSI+MFI+MACD** (Default) | RSI, MFI, MACD Hist | Sauberer, ohne nervösen Stoch RSI |
| B: RSI+MFI+StochRSI | RSI, MFI, Stoch RSI | Schnelleres Timing |
| C: All | Alles | Zum Vergleich |

### Regime-Filter

Das Regime beeinflusst die Score-Gewichtung automatisch:

| Regime | Erkennung | Setup-Score | Confirmation-Score |
|--------|-----------|------------|-------------------|
| RANGE | Efficiency Ratio ≤ 0.35 | ×1.2 (Oszillatoren wertvoller) | ×1.0 |
| TREND ↑/↓ | EMA-Alignment + ER > 0.35 | ×0.8 (Oszillatoren weniger zuverlässig) | ×1.3 (BOS zählt mehr) |
| HIGH VOL | BB Width > 1.3× Durchschnitt | — | ×1.2 Bonus |
| LOW VOL | BB Width < 0.7× Durchschnitt | — | ×0.8 |

### Level-Kontext

Reversals an sinnvollen Stellen bekommen Bonus, Reversals im Niemandsland Abzug:
- **Nahe Major Swing Low** (< 0.5 ATR) oder am **20-Bar Range-Tief** → Bull Setup +1
- **Nahe Major Swing High** oder am **Range-Hoch** → Bear Setup +1
- **Weit weg von allem** → -0.5

### Status-Logik

| Status | Icon | Bedeutung |
|--------|------|-----------|
| — | · | Nichts los |
| WATCH | ○ | Setup baut sich auf (≥ 3), keine Confirmation |
| SETUP | ◈ | Setup stark (≥ 5), keine Confirmation |
| ALERT | ⚡ | Struktur-Event, aber Setup zu schwach |
| **CANDIDATE** | **◉** | **Setup + Confirmation bestätigt — ernst nehmen** |
| **CONFLICTED** | **⊘** | **Signal widersprüchlich — nicht handeln** |

### Konflikterkennung

| Konflikt-Typ | Erkennung | Effekt |
|-------------|-----------|--------|
| Setup-Konflikt | Bull + Bear Setup beide aktiv | Markt unentschlossen |
| Conf-Konflikt | Beide Seiten confirmed | Widersprüchliche Struktur |
| Trend-Konflikt | Setup gegen starken Trend (ER > 0.45) | Signal gegen die Strömung |
| Opposed Candidate | Candidate + Gegenrichtung confirmed | Stärkstes Warnsignal |

**CONFLICTED** ersetzt CANDIDATE wenn ein Trend- oder Opposing-Konflikt vorliegt.

**Severity in Debug-Tabelle:**
- ✓ CLEAR (grün) — kein Konflikt
- ⊘ LOW (grau) — 1 Typ aktiv
- ⊘ MODERATE (amber) — 2 Typen
- ⊘ HIGH (orange) — 3+ Typen

### Hintergrundfarbe

| Farbe | Bedeutung |
|-------|-----------|
| Grün | Bull CANDIDATE |
| Rot | Bear CANDIDATE |
| **Grau-blau** | **CONFLICTED — nicht handeln** |
| Amber | Beide Seiten confirmed |
| Blasses Grau | Gemischte Setups |

### Darstellung im Panel

| Element | Bedeutung |
|---------|-----------|
| Grüne Balken (nach oben) | Bull Setup Score |
| Rote Balken (nach unten) | Bear Setup Score |
| Grüne Kreise | Bull Confirmation (Setup + Struktur addiert) |
| Rote Kreise | Bear Confirmation |

**Optional: Component Lines** (Input "Show Component Lines"):
4 Steplines für Setup/Conf getrennt — zeigt ob der Score von Überdehnung oder Struktur getrieben wird.

### Status-Leiste (unten links, immer sichtbar)

Zeigt auf einen Blick:
- Aktuelles Regime (TREND ↑/↓ / RANGE) + Volatilität
- Aktive Multiplier
- Bull Status + Setup/Conf Werte
- Bear Status + Setup/Conf Werte

---

## Display-Modi

Jedes Skript hat drei Modi (Input "Display Mode"):

| Modus | Was es zeigt |
|-------|-------------|
| Light | Nur das Wesentliche — Marker, Score, Kernplots |
| Debug | Zusätzliche Werte, Swing-Lines (Micro + Major), Statusinfos |
| Research | Alles — Tabellen, Statistiken, Timing-Auswertung, Export-Daten |

**Empfehlung:** Für den täglichen Blick "Light". Zum Analysieren "Research".
