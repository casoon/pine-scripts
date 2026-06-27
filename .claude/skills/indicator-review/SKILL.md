---
name: indicator-review
description: >-
  Diagnose-Regelwerk zum Prüfen bestehender TradingView/Pine-Indikatoren und zum Analysieren
  verpasster oder falscher Signale. Benutzen, wann immer ein Indikator bewertet, auditiert oder
  fehlersuchend untersucht wird — auch ohne das Wort "Review". Triggert bei: "warum hat der
  Indikator diesen Pivot/diese Bewegung verpasst", "warum kam (k)ein Signal hier", Backtest-/
  Capture-Rate-Analyse, Pivot-to-Pivot-Auswertung, Gate-Cost-/Block-Analyse, Fehlerklassifikation,
  "ist dieser Filter sein Geld wert", Verdacht auf Overfitting/Aggregat-Trugschluss, und der
  Beurteilung ob ein Indikator architektonisch sauber gebaut ist. Für das *Bauen/Umbauen* eines
  Indikators stattdessen indicator-design verwenden (dort wohnt das Rollen-Modell).
---

# Indicator Review — Diagnose & Fehleranalyse

Dieses Regelwerk strukturiert das *Prüfen*: Es trennt echte Defekte von Fehlerwartungen und
verhindert die in diesem Repo wiederholt teuer bezahlten Trugschlüsse (Aggregat-maskierte
Patterns, wirkungslose Gates, Pivot-als-Ziel — siehe `.claude/CLAUDE.md`, verworfene Gates A/B/C).
Das Rollen-Vokabular (Trend/Location/Momentum/Trigger/Quality) stammt aus `indicator-design`.

## 1. Pivot-Regel — Pivots zur Diagnose, nicht als exaktes Ziel

Pivots sind ein hervorragendes *Prüfraster* für Signal-Timing, aber **nicht** der Maßstab
„Signal muss exakt auf der Pivot-Kerze kommen". Das wäre unfair gegen ein Modul, das den
*Bereich* korrekt erkannt hat.

Pro verpasstem/getroffenem Pivot klassifizieren:

| Lage | Bedeutung |
|---|---|
| Signal 0–N Kerzen **vor** Pivot | früh — Bereich erkannt, ggf. zu eilig |
| Signal **am** Pivot | Punktgenau |
| Signal 0–N Kerzen **nach** Pivot | spät — Bereich erkannt, Timing-Lag (oft Pivot-Confirmation-Lag) |
| **kein** Signal im Fenster | Bereich verfehlt → Rollenfrage (siehe §2) |

Die eigentliche Frage ist „Bereich erkannt vs. Punkt verfehlt", nicht „Kerze exakt getroffen".
Pivots bleiben dabei reines Control-Overlay — sie dürfen den Signalpfad nie speisen
(Memory `feedback_pivot_is_control_not_signal`).

## 2. Fehleranalyse-Regel — war die Rolle überhaupt zuständig?

Bei jedem verpassten Pivot **nicht** sofort fragen „war der Indikator schlecht?", sondern:
**war diese Rolle überhaupt zuständig?**

Beispiel: Zeigt StochRSI am Pivot nichts, ist das kein automatischer Momentum-Fehler — der
Pivot war vielleicht *strukturell* (Location/Market-Structure-getrieben), nicht
momentumgetrieben. Dann hätte die Location-Rolle anschlagen müssen, nicht Momentum. Du hast die
falsche Aussage vom falschen Modul erwartet.

## 3. Fehlerklassen

Jeden Befund einer Klasse zuordnen — das verhindert, dass „Indikator schlecht" als
Sammelbegriff für unterschiedliche Ursachen herhält:

1. **Codefehler** — Logik/Pine-Bug (siehe Memory `reference_pine_v6_pitfalls`)
2. **Berechnungsfehler** — Formel/Serie falsch
3. **Visualisierungsfehler** — Logik richtig, Anzeige falsch
4. **Schwellenwertfehler** — Rolle richtig, Schwelle daneben
5. **Rollenfehler** — falsches Modul für die Aufgabe zuständig gemacht (§2)
6. **Gewichtungsfehler** — Rolle richtig erkannt, aber falsch gewichtet
7. **Regimefehler** — Trendfolge-Logik in Range angewandt (oder umgekehrt)
8. **Timeframefehler** — Gewichtung der TF nicht angepasst
9. **Marktprofilfehler** — falsches Profil (Rohstoff-Intuition auf Aktien etc.)
10. **Erwartungsfehler** — kein Defekt; falsche Aussage vom falschen Modul erwartet

**Kernsatz: Nicht jeder verpasste Pivot ist ein Fehler.** Erst Klasse 5/10 ausschließen,
bevor an Code oder Schwellen geschraubt wird.

## 4. Backtest-Regel — Rollen-Scores an jedem Pivot speichern

Für systematische Diagnose an *jedem* bestätigten Pivot rückwirkend loggen:

```text
Trend Score · Location Score · Momentum Score · Trigger Score · Quality Score · Final Score
```

Dann auswerten:

- Welche **guten** Pivots wurden verpasst — und welcher Rollen-Score fehlte dort?
- Welche **schlechten** Pivots wurden erkannt — welche Rolle war zu laut?
- Welche Rolle war **falsch gewichtet**? Welche war **blind** (immer ~0)?

In diesem Repo existiert das als `WT4 PIVOT` / `WT4 BLOCKED` / `WT4 ENTRY` / `WT4 REAL EXIT`
log-Events, ausgewertet über `scripts/analyze_gates.py` (Pivot-to-Pivot-Baseline, Signal
Coverage, Gate Cost, Entry/Blocked/Gate Quality).

## 5. Gate-/Filter-Prüfung — verhindert die wiederholten Repo-Fehler

Bevor ein Gate als „sinnvoll" gilt, gegen die hart erkauften Lektionen aus `.claude/CLAUDE.md`
prüfen:

- **Block-Volumen schätzen** *vor* Implementierung. Gates die < ~5 % blocken sind selbst bei
  perfekter Treffsicherheit irrelevant (verworfenes Gate C: nur 1 % geblockt).
- **Capture-Rate** *neben* avgR betrachten. Fällt Capture stärker als avgR steigt, ist das Gate
  selektionsneutral (verkappt wertlos) — es entfernt gute *und* schlechte Setups gleich oft.
- **Niemals aus Aggregat-Daten schließen.** Aggregierte Befunde über alle TF/Dir maskieren
  TF-/Dir-spezifische Patterns: Gate B blockte `atrRank<30` global, obwohl 1D-Long dort den
  *besten* Bucket (avgR +0.58) hatte. Hypothesen müssen auf TF/Dir-Ebene konsistent sein.
- **Veto-Check:** Blockt das Gate den eigentlichen Reversal-Trigger? Das ist das wiederkehrende
  Versagensmuster (Memory `feedback_er_gates_blocking_reversals`).

## 6. Architektur-Audit eines bestehenden Indikators

Checkliste gegen das Rollen-Modell (`indicator-design`):

- [ ] Macht das Modul **eine** Hauptaufgabe — oder ist es eine eierlegende Wollmilchsau, bei der
      man nicht mehr sagen kann *warum* ein Signal feuert? (Memory `feedback_one_thing_done_well`)
- [ ] Hat jeder Sensor genau **eine** Rolle, oder erfüllt einer eine fremde (RSI als Trend,
      Pivot als Trigger, Volumen-Spike als Long/Short)?
- [ ] Gibt es eine harte **AND-Kette**, die gute Setups killt — statt Evidenz-Scoring?
- [ ] Vetoen zu **viele** Sensoren? Darf ein einzelner schwacher Wert ein Setup töten?
- [ ] Ist die **Gewichtung** auf Rollen-Ebene (nicht je Indikator) und TF-/Markt-/Regime-abhängig?
- [ ] Sind **Regime** (Trend vs. Reversal) getrennt, oder laufen beide Modelle mehrdeutig parallel?
- [ ] Speist ein **Pivot** den Signalpfad (Trigger/Grade/Dedup)? → Defekt, auf Control-Overlay
      zurückbauen.
- [ ] Gibt es **Debug-Ausgaben**, die „warum (k)ein Signal" beantworten?
- [ ] Beantwortet er die **sechs Fragen** (Wo / Richtung / frisch-erschöpft / Timing / Sicherheit /
      Warum kein Signal)?

## 7. Arbeitsprinzip — Fundament vor Feintuning

Vor jeder Mikro-Optimierung prüfen, ob das *strukturelle* Fundament steht. Per-TF/Dir-Bänder
gewinnen ~0.05 R; ein besserer Exit oder eine reparierte Rollen-Zuständigkeit gewinnt ~0.30 R.
Feintuning auf schlechtem Fundament optimiert auf das falsche Ziel — erst Fundament (Exit-Logik,
Signal-Quality, Rollen-Zuständigkeit, HTF-Confluence), dann polieren (Memory-Prinzip aus
`.claude/CLAUDE.md`, „Fundament vor Feintuning").
