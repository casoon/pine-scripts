# Kestrel Swing Structure

Statistical swing structure: swing pivots that strictly alternate between highs and lows, the legs between them measured in ATRs, and from them the median correction over the median impulse, the trend quality of the newest corrections and where the current bar stands in its correction. Highs and lows are treated alike, so a price series reflected about a level gives the same readings. The rules and defaults are those of `kestrel_swing_structure` (alias `swing_structure`) in kestrel-chartkit.

## Features

- Strict pivots (`left` bars before, `right` bars after, ties disqualify), looked for only on bars with an ATR
- Strict alternation: a pivot of the same kind as the newest one extends that swing (the more extreme stays; on equal prices the existing one)
- Outside bars (pivot high and low at once) ordered by the alternation; with no earlier pivot by the bar's own direction, and none for a bar that closed at its open
- Trend from higher highs and higher lows or lower highs and lower lows, otherwise the direction of the newest leg — no bias towards either side
- Trend quality from the newest three corrections: strengthening, stable or weakening
- Retracement, remaining potential, required stop, reward-to-risk and impulse velocity in ATRs
- Zigzag of the confirmed pivots, dashboard, optional correction-zone dots, every engine reading in the data window

## Readings

| Data window | Meaning |
|---|---|
| `value (correction_impulse_ratio)` | median correction / median impulse (0 for a median impulse of 0) |
| `trend_quality` | 1 strengthening, 0 stable, −1 weakening: the newest of the last three corrections against the oldest of them |
| `median_impulse_atr`, `median_correction_atr` | medians of the legs along and against the trend, over the newest `Legs for the medians` legs |
| `current_retracement_atr` | \|close − last pivot\| / ATR |
| `entry_zone_reached` | 1 when the retracement reaches 0.8 × median correction |
| `remaining_potential_atr` | max(median impulse − retracement, 0) |
| `required_stop_atr` | max(median correction, 0.1) |
| `potential_crv` | remaining potential / required stop |
| `last_impulse_velocity_atr` | size / span in bars of the newest impulse leg |
| `recent_correction_atr_1..3` | newest corrections, newest first |

All legs are divided by the ATR of the current bar. A reading needs four pivots and at least two impulse and two correction legs; before that the values are empty.

## Purpose, use and guardrails

- **Why it exists.** A binary "trend up / down" hides how the trend is built. Leg sizes in ATRs show it: shrinking corrections against steady impulses read differently from growing ones.
- **What it is for.** Describing the swing a market is in — how deep corrections usually run, how far the current one has come, and how much of a typical impulse would still be left. Useful as context next to a chart, and for exporting the readings.
- **What it is not.** A direction signal. The correction zone and the reward-to-risk figures describe the swing measured so far; they are not orders and not forecasts.
- **Delay.** Every pivot is known `right` bars after its own bar; the zigzag and the readings move only then.
- **Series it was computed on.** Readings depend on the bar series (session cut, roll, price adjustment, range of the bars); compare them only on the same kind of series.

## Kestrel parity

- Engine: kestrel-chartkit, catalog `kestrel_swing_structure`, `src/indicator/swing_structure.rs` (`SwingStructureIndicator`), mirror-exact state of commit `e7d117a`; defaults `left 5`, `right 5`, `max_swings 50`, `atr_len 14` (Wilder).
- Ties at the threshold of `entry_zone_reached` and between corrections in `trend_quality` use the engine's relative tolerance of `1e-11`, which keeps both readings the same on a reflected series.
- Checked by a line-by-line transliteration of this script against the independent reference implementation of kestrel-chartkit, on synthetic and tick-grid series with outside bars and their reflections: identical values; the only differences are exact ties at the `entry_zone_reached` threshold, where this script follows the engine's tolerance.
