# strategy-helper

Rust CLI for analyzing TradingView Pine logs emitted by `wavetrend_v3_strategy.pine`.

## Log Format Contract

The canonical event marker is:

```text
WT3 REAL EXIT | key=value | key=value | ...
```

Rules:

- Fields are separated by ` | `.
- Keys are case-sensitive and stable.
- Decimal separator is `.`.
- Missing optional numeric values are logged as `NaN`.
- Booleans are `true` or `false`.
- `entryStruct` is a comma-separated nested `key=value` list.
- New fields may be appended, but existing keys must not be renamed.

Required top-level fields:

- `tf`, `chartSec`, `profile`, `executionMode`
- `dir`, `family`, `exit`
- `trade`, `barsHeld`, `pnl`, `R`, `entry`, `exitPx`
- `MFE`, `MAE`, `capturePct`
- `targetRoomR`, `targetRoomATR`, `targetHit`, `barsToTarget`
- `targetPx`
- `favPivotR`, `barsToFavPivot`, `advPivotR`, `barsToAdvPivot`
- `favPivotPx`, `advPivotPx`
- `entryScore`, `entryStruct`

Required `entryStruct` fields:

- `hh`, `hl`, `lh`, `ll`
- `longStruct`, `shortStruct`
- `rangePos`, `target`, `stop`

Machine-readable schema:

```bash
cargo run -- schema
```

Validate logs before comparing results:

```bash
cargo run -- validate ../testdata/test60
```

## Usage

```bash
cargo run -- analyze ../testdata/test59 \
  --out ../testdata/test59/strategy_helper_report.md \
  --trades-csv ../testdata/test59/strategy_helper_trades.csv
```

From the repo root:

```bash
cargo run --manifest-path strategy-helper/Cargo.toml -- analyze testdata/test59
```

Older logs without `tf` are still parsed, but grouped as `unknown`.
