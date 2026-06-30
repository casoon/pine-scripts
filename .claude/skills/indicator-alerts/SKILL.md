---
name: indicator-alerts
description: >-
  Best-Practice-Regelwerk für Alerts in TradingView/Pine-Indikatoren dieses Repos.
  Benutzen, sobald an einem Indikator Alerts hinzugefügt, geändert, vereinheitlicht oder
  geprüft werden — auch wenn nur "Benachrichtigung", "alert", "alertcondition", "Signal soll
  feuern", "Webhook" oder "Create Alert" genannt wird. Triggert bei: neuen alertcondition()/
  alert()-Definitionen, Repaint-/Bar-Close-Fragen bei Alerts, Alert-Message-Texten, Emoji-/
  Präfix-Konvention, "welche Alerts soll der Indikator haben", Alert-Inputgruppe/Toggle,
  Watch-vs-Entry-vs-Exit-Alert-Trennung, Regime-/Kontext-Alerts, und der Frage ob ein Indikator
  überhaupt Alerts braucht. Baut auf den Signaltypen aus indicator-design (§7) auf — dort wohnt
  das Rollen-/Signalmodell; dieser Skill regelt nur deren Ausspielung als Alert.
---

# Indicator Alerts — Best-Practice-Regelwerk

Alerts sind die **Ausspielung der Signaltypen**, nicht eine eigene Taxonomie. Das
Signal-/Rollenmodell wohnt in `indicator-design` (§1 Rollen, §7 `Watch → Setup → Trigger →
Confirmation → Invalidation`). Dieser Skill regelt nur, *wie* diese Typen als TradingView-Alert
herauskommen — einheitlich, repaint-frei, attributierbar.

Grundsatz wie überall im Repo: ein Alert muss beantworten *welches Event, auf welchem Symbol/TF*.
Ein Alert, der nur „Bullish Divergence detected" sagt, ist auf mehreren parallelen Charts wertlos.

## 0. Repo-Konventionen (verbindlich entschieden)

- **Default-Mechanismus: `alertcondition()`.** User wählt granular im „Create Alert"-Dialog.
- **Message-Tiefe: leicht.** Pflichtformat `Kürzel · Event · {{ticker}} {{interval}}`. Mehr
  (Preis, Score, Regime) nur, wo es echten Mehrwert hat — nicht als Pflicht.

Diese zwei Punkte sind gesetzt; der Rest dieses Skills setzt sie um.

## 1. Mechanismus-Wahl — eine Regel pro Event

| Mechanismus | Default? | Wann | Nie |
|---|---|---|---|
| `alertcondition()` | **ja** | Diskrete, einzeln wählbare Events | im lokalen Scope (`if`-Block) — verboten in Pine |
| `alert()` runtime | nur Ausnahme | Reicher dynamischer Kontext nötig **oder** eine konsolidierte „Any alert() call"-Regel für Webhooks | als *stille* zweite Kopie eines Events neben einer `alertcondition()` |

**Keine *stille* Doppel-Definition.** Wer beide Mechanismen für dasselbe Event hat, ohne es zu
kennzeichnen, riskiert Doppel-Feuern (beobachtet in `regime_detector`).

**Legitime Ausnahme — das dokumentierte Either/Or** (Referenz: `mtf_wavetrend_confluence`,
`oscillator_divergence_zones`): granulare named `alertcondition()` (User wählt *eine*) **und
höchstens eine** konsolidierte `alert()`-Regel, die alle Events abdeckt und reicheren Kontext
trägt (Score/Grade/Regime — was `alertcondition`-Messages nicht können). Zulässig **nur**, wenn
ein Code-Kommentar unmissverständlich sagt: *entweder* die named Alerts *oder* die kombinierte
`alert()`-Regel einrichten, nicht beide. Ohne diesen Hinweis ist es das Anti-Pattern.

`alertcondition()` **muss im globalen Scope** stehen. Gating erfolgt durch `and`-Verknüpfung
des Boolean, **nicht** durch ein umschließendes `if` (das ist ein Compile-Fehler).

## 2. Repaint-Regel — der wichtigste Korrektheitspunkt

Ein Alert darf nicht auf der **formenden** Kerze feuern und dann flippen.

### Für `alertcondition()` — Confirmation-Gate (Referenzmuster aus `smc_structure_expectation`)

```pine
bool alertsOnBarClose = input.bool(true, "Alerts only on bar close (confirmed)", group=g_alert)
bool alertOk          = not alertsOnBarClose or barstate.isconfirmed

alertcondition(alertOk and longTrigger,  title="…", message="…")
alertcondition(alertOk and shortTrigger, title="…", message="…")
```

- Default-Toggle **an** (`true`). Der User kann zusätzlich im TV-Dialog „Once Per Bar Close"
  wählen, aber der Indikator darf sich nicht darauf verlassen — das Gate gehört in den Code.
- Wenn das Signal ohnehin schon ein bestätigter Zustand ist (z. B. `… and barstate.isconfirmed`
  in der Signal-Definition), ist das Gate redundant — dann nicht doppeln.
- **Zusammengesetzte Bedingungen immer klammern:** `alertcondition(alertOk and (a or b), …)`.
  Ohne Klammer bindet `and` stärker → `(alertOk and a) or b` feuert trotz ausgeschaltetem Gate.

### Für `alert()` — `freq` explizit

```pine
if longTrigger
    alert("XYZ · LONG · " + syminfo.ticker + " " + timeframe.period, alert.freq_once_per_bar_close)
```

- **Default `alert.freq_once_per_bar_close`.** `alert.freq_once_per_bar` nur mit Begründung im
  Code-Kommentar (z. B. echtes Intrabar-Event, das bewusst früh feuern soll). `alert.freq_all`
  praktisch nie.
- `alert()` **immer in `if cond` kapseln** — ungeguarded feuert es jede Kerze.

## 3. Alert-Arten = Signaltypen (Mapping zu indicator-design §7)

Jede Art bekommt einen klaren, stabilen Titel. Nicht alle Indikatoren brauchen alle Arten — aber
keine Art doppelt erfinden.

| Alert-Art | Signaltyp | Titel-Beispiel | Hinweis |
|---|---|---|---|
| **Entry/Trigger** | Trigger/Confirmation | `XYZ Long`, `XYZ Short` | das aktionierbare Kern-Signal |
| **Exit** | Invalidation/Exit | `XYZ Exit Long` | nur wo der Indikator Exits hat |
| **Watch/Setup** | Watch/Setup | `XYZ Watch Long` | Frühwarnung, **getrennt** vom Entry — nie zusammenwerfen |
| **Regime/Kontext** | Quality/Veto | `XYZ Regime Change` | **kein** Trade-Signal — im Titel/Message als Kontext kennzeichnen |
| **Quality/Confluence** | Quality | `XYZ High-Quality Setup` | optionale Güte-Meldung |
| **Invalidation/Warning** | Invalidation | `XYZ Bull Weakness` | Reversal-Risiko / Trap |

Watch und Entry **immer als zwei Alerts** (siehe `jma_struct`, `cpm_v4`) — der Trader entscheidet
selbst über Vorlauf. Sie in einen Alert zu pressen macht das Timing unattributierbar (§7).

## 4. Message-Standard (leicht)

Pflichtformat:

```
<Kürzel> · <Event> · {{ticker}} {{interval}}
```

- **Kürzel** — kurzes, **über Versionen stabiles** Indikator-Kürzel (z. B. `RDP`, `CPM3`, `TWR`).
  Aus der Registry `indicators/ALERT_KUERZEL.md` nehmen; neuen Indikator dort eintragen,
  bestehende nie umbenennen.
- **Event** — sprechend und eindeutig (`LONG`, `EXIT LONG`, `WATCH LONG`, `REGIME CHANGE`).
- `{{ticker}} {{interval}}` — Pflicht, damit der Alert auf parallelen Charts identifizierbar ist.

Optionaler State **nur wo nützlich** (B-Entscheidung: nicht verpflichtend):
- Preis: `@ {{close}}`
- Live-Plotwert: `{{plot("Consensus Score")}}` (nur in `alertcondition`)

```pine
// alertcondition — Placeholder werden von TradingView ersetzt:
alertcondition(alertOk and longTrigger, title="CPM Long",
     message="CPM · LONG · {{ticker}} {{interval}}")

// Webhook-Variante (key=value, maschinenlesbar) — nur wenn ausdrücklich gewünscht:
alertcondition(alertOk and longTrigger, title="CPM Long (webhook)",
     message='{"ind":"CPM","ev":"LONG","sym":"{{ticker}}","tf":"{{interval}}","px":{{close}}}')
```

**Wichtig — Placeholder gelten nur für `alertcondition()`.** In `alert()` gibt es keine
`{{…}}`-Ersetzung; dort baut man den String selbst:
`syminfo.ticker + " " + timeframe.period` (und `str.tostring(close, format.mintick)` statt
`{{close}}`).

### Emoji-/Präfix-Konvention (optional, aber einheitlich)

Wenn Emoji verwendet werden (Multi-Monitor-Scan), dann nur dieses Minimal-Set, konsistent:

| Emoji | Bedeutung |
|---|---|
| `✅` | Entry / finales Trigger |
| `⚠️` | Watch / Frühwarnung / Risiko |
| `🔒` | Invalidation / Konflikt |

Kein Emoji ist auch ok — aber nicht mischen (mal mit, mal ohne) innerhalb eines Indikators.

## 5. Input-Konvention

- Eine eigene Alert-Inputgruppe: `g_alert = "Alerts"` (Konstante oben definieren).
- Mindestens das `alertsOnBarClose`-Toggle aus §2.
- Optional ein `Enable Alerts`-Master-Toggle, wenn der Indikator viele Alerts hat — dann **alle**
  alertconditions konsistent damit gaten (`alertOk and enableAlerts and …`), nicht nur einige.
- **Anti-Pattern:** im selben File manche Alerts gegated, andere nicht (beobachtet in
  `regime_detector`). Entweder alle oder keiner.

## 6. Braucht der Indikator überhaupt Alerts?

- **Ja**, wenn er einen Signaltyp aus §3 produziert (Trigger/Exit/Watch/Regime/Warning).
- **Nein** für reine Visual-/Mapping-Overlays ohne Event (z. B. `vwap_cross_visuals`,
  `zigzag_fibo_pullback_map`) — Alerts ohne klares Event sind Lärm.
- Wenn ein Indikator benannte Signale hat (`longSignal`, `crossUp`, …) aber **keinen** Alert,
  ist das eine Lücke — Alert ergänzen oder bewusst begründen, warum nicht.

## Checkliste (vor dem Commit)

1. **Mechanismus:** `alertcondition()` Default; `alert()` nur mit Grund; nie beide für 1 Event.
2. **Scope:** jede `alertcondition()` im globalen Scope, Gating per `and`-Bool.
3. **Repaint:** `alertOk = not alertsOnBarClose or barstate.isconfirmed` vorgeschaltet
   (bzw. `freq_once_per_bar_close` bei `alert()`).
4. **`alert()` geguarded** in `if cond`.
5. **Message:** `Kürzel · Event · {{ticker}} {{interval}}`; Kürzel versionsstabil.
6. **Arten getrennt:** Watch ≠ Entry; Regime/Kontext klar als Nicht-Trade markiert.
7. **Inputgruppe `Alerts`**, Gating konsistent über *alle* Alerts.
8. **Emoji** nur aus dem Minimal-Set, einheitlich oder gar nicht.

## Anti-Patterns (im Repo beobachtet, nicht wiederholen)

- `alert.freq_once_per_bar` ohne Begründung / `alert()` ohne `freq` → Intrabar-Repaint.
- Message ohne `{{ticker}} {{interval}}` → auf parallelen Charts nicht zuordenbar.
- Gating mal an, mal aus im selben File.
- *Stille* Doppel-Definition (beide Mechanismen für ein Event ohne Either/Or-Kommentar) → Doppel-Feuern. Das dokumentierte Either/Or (§1) ist erlaubt.
- Watch und Entry in einem Alert → Timing nicht mehr attributierbar.
- Wechselnde Kürzel je Version → Alert-Regeln des Users brechen beim Update.
