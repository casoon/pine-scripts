# Kestrel FVG Zones

Fair value gaps followed as zones until a later bar trades back into them, and what price does at that return. A rejection closes back beyond the zone within a short window, a break closes through the far side, and otherwise the window simply runs out. The zones and fills are those of `fvg_fill` in kestrel-chartkit; the reaction rule is the same for both directions.

## Features

- Bullish gap: the low of bar t above the high of bar t−2 (zone from that high to that low); bearish gap: the high of bar t below the low of bar t−2
- Both directions in one list; only the newest `Open zones kept` open zones are followed
- Fill on the first later bar that trades back into the zone (bullish: low at or below the upper edge; bearish: high at or above the lower edge) — the bar that forms a gap never fills it
- Reaction tracking after the fill: rejection, break through the far side, or expiry of the window
- Open zones extend to the right; filled zones stay as muted boxes up to a set number
- Engine counts and reaction events in the data window

## Reaction rule

For a bullish zone (bearish mirrored):

- **Rejection:** a bar from the fill bar up to `Reaction window` bars after it that trades into the zone and closes above its upper edge. The fill bar itself can be the rejection.
- **Break:** a close below the zone's lower edge first — the reaction ends as a break.
- **Expiry:** neither within the window.

The check order on each bar is break, then rejection, then expiry.

## Data window

| Name | Meaning |
|---|---|
| `value (open zones)`, `created`, `filled`, `open_bullish`, `open_bearish` | the `fvg_fill` engine outputs |
| `rejection_bullish`, `rejection_bearish` | rejections on this bar |
| `break_bullish`, `break_bearish` | breaks on this bar |
| `expired_bullish`, `expired_bearish` | reactions that ran out on this bar |

## Purpose, use and guardrails

- **Why it exists.** A gap left by a fast move marks a price range the market skipped. When price returns to it, the touch alone says little; how price behaves on the return is what this script shows.
- **What it is for.** Seeing the open gaps and the reaction at each return: waiting for the reaction instead of a resting limit order inside the zone. A limit in the zone is filled exactly when price runs through it, so it collects the fills a reaction rule would leave out.
- **What it is not.** An entry rule on its own. The rejection sorts the returns into those that turned and those that did not; it does not by itself make the turned ones worth trading.
- **Counting.** Several zones can be filled or rejected on the same bar; the data window counts them, the markers show only whether there was at least one.

## Kestrel parity

- Engine: kestrel-chartkit, catalog `fvg_fill`, `src/indicator/smart_money_structure.rs` (`FvgFillEngine`, zones from `LiquidityFvgEngine`); default `max_zones 20`.
- The reaction rule is a research definition from the Kestrel lab, not part of the engine; window `3` is its fixed setting.
- Checked by a line-by-line transliteration of this script against the kestrel-chartkit reference implementation of `fvg_fill` (zone counts) and against the lab's own reaction code (rejections and non-confirmations), for zone counts 16, 20 and 24: identical on synthetic series.
