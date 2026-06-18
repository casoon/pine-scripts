# Vein: Reversal Zones

**TradingView:** https://de.tradingview.com/script/WtyCfLGZ/

S/R zones derived from forward-validated reversal bars, combined with a live multi-trigger signal engine. Zones mark price levels where ATR-confirmed, quality-graded reversals occurred historically. Signals fire when a trigger coincides with one of those levels.

## How it works

The indicator replicates the Vein Reversal Labeler logic internally. When a reversal is confirmed (after the forward evaluation window), a zone is drawn at the reversal candle's key range:

- **Support zone** — `[low, close]` of the bull reversal bar: the area price dipped into and recovered from
- **Resistance zone** — `[close, high]` of the bear reversal bar: the area price pushed into and rejected from

Zones are filtered, merged, and scored in real-time. Only the nearest N zones within ATR range are displayed.

## Zone Filtering

| Setting | Default | Description |
|---|---|---|
| Visible Zone Range | 8 ATR | Zones farther than this are hidden (not deleted) |
| Max Visible Supports | 2 | Only the 2 nearest support zones are shown |
| Max Visible Resistances | 2 | Only the 2 nearest resistance zones are shown |
| Merge Nearby Zones | 0.5 ATR | Zones within this distance are merged into one |
| Delete When Broken | on | Zone is removed when price closes fully through it |

## Signal Triggers

Five triggers are available, each independently toggleable:

| Trigger | Long | Short |
|---|---|---|
| WaveTrend Cross | WT crossover in OS zone | WT crossunder in OB zone |
| RSI Reclaim | RSI crosses back above OS level | RSI crosses back below OB level |
| Supertrend Flip | Direction flips bullish | Direction flips bearish |
| Candle Sweep | Low violates swing low, close recovers | High violates swing high, close recovers |
| MA / Momentum | Close crosses above MA + MACD hist rising | Close crosses below MA + MACD hist falling |

MA type for the reclaim line is configurable (EMA / RMA / SMA / WMA / HMA / JMA, default RMA). JMA Phase and Power are exposed when JMA is selected.

## Signal Modes

- **Known Zones** *(default)* — signal only fires when price is near an existing reversal zone
- **Candidates** — signal fires on trigger alone, regardless of zone
- **Both** — fires in both cases; solid arrow (`▲/▼`) = zone-confluent, outline (`△/▽`) = candidate only

## Touch Counter

Each time price re-enters a zone, the touch counter increments (`★★ ×3`). Repeatedly tested zones are visually distinguishable from fresh ones.

## Inputs

**Labeling Parameters** — ATR length, forward/extended bar windows, weak/strong ATR targets, max adverse move (mirror of Vein Reversal Labeler)

**Quality Criteria** — fast reversal threshold, MAE threshold for strong grade

**Cluster Filter** — minimum bars between labels of the same direction

**Zones** — grade visibility toggles, max stored zones, visibility range, merge distance, deletion on break, right extension

**Signals** — signal mode, trigger requirement (Any / 2+), zone proximity threshold, cooldown bars

**Trigger groups** — per-trigger settings (WT levels, RSI levels, ST factor, sweep lookback, MA type/length/MACD lengths)

**Display** — colors per grade, touch count visibility, grade label toggle
