# Project Instructions

## Indicator directory structure

Each indicator (or suite of related indicators) lives in its own subdirectory under a category folder inside `indicators/`. The category folders are: `momentum`, `money_flow`, `trend_strength`, `trend_direction`, `market_structure`, `volatility`, `mean_reversion`, `relative_strength`, `composite`. The `indicators/composite/commodity_pulse_matrix/` directory is the reference for how an indicator directory should be structured.

Every indicator directory contains:

### `README.md`
Technical documentation for developers and users reading the code. Structure:
- Title as `# Heading`
- TradingView publication link directly below the title if the script is published: `**TradingView:** <url>`
- One-paragraph description of what the indicator does
- `## Features` — bullet list of capabilities
- Additional sections as needed (e.g. `## Scoring`, `## Modes`) explaining the logic and UI

### `CHANGELOG.md`
Incremental version history for TradingView update posts. One entry per published version. Use this as the source for TV update notes — copy the relevant section rather than rewriting the full description.

Format:
```markdown
## vX.Y.Z — YYYY-MM-DD
- What changed (user-visible, one bullet per meaningful change)
```

### `screenshots/` (optional)
Visual documentation for README and TradingView update posts.

Naming convention: `<indicatorname>_<context>_<optional-version>.png`

Examples:
- `wyckoff_schematics_overview.png` — main chart view
- `wyckoff_schematics_spring_example.png` — specific setup
- `wyckoff_schematics_v4.3_update.png` — screenshot for a TV update post

### `DESCRIPTION_TV.bbcode`
The publication description for TradingView, written in BBCode. Structure:
- Opening bold title line
- `[b]What it does[/b]` — plain-language explanation of the purpose
- Key sections as `[b]Section[/b]` headings with `[list][*]...[/list]` for feature lists
- Closing standard trading disclaimer in `[i]...[/i]`:

  > This script is provided for educational and informational purposes only. It does not constitute financial advice. Trading commodities and other financial instruments involves substantial risk of loss and is not suitable for all investors. Past performance of any indicator or system is not indicative of future results. Always conduct your own research, apply proper risk management, and consider consulting a qualified financial advisor before making trading decisions.

### TradingView BBCode — supported tags

TradingView supports only a subset of BBCode. Use only these tags:

| Tag | Purpose |
|---|---|
| `[b]...[/b]` | Bold |
| `[i]...[/i]` | Italic |
| `[u]...[/u]` | Underline |
| `[s]...[/s]` | Strikethrough |
| `[url=...]...[/url]` | Hyperlink |
| `[img]...[/img]` | Image |
| `[list][*]...[/list]` | Unordered list |
| `[list=1][*]...[/list]` | Ordered list |
| `[code]...[/code]` | Code block |
| `[quote]...[/quote]` | Quote block |

**Not supported:** `[hr]`, `[h1]`/`[h2]` headings, `[table]`, `[center]`, `[color]`, `[size]`.

### The `.pine` file(s)
The script itself. No additional wrapper or build files.

The header of `indicators/composite/commodity_pulse_matrix/commodity_pulse_matrix_v3.pine` is the reference for how every `.pine` file should start. The exact structure:

```pine
//@version=6
// ============================================================================
// Script Name [WavesUnchained]
// Version: X.Y
// Author: WavesUnchained
// Build: YYYY-MM-DD HH:MM:SS
// ============================================================================
// One-line description of what the script does.
//
// Features:
//   ✓ Feature one
//   ✓ Feature two
//
// ============================================================================

indicator(...)
```

Rules:
- `//@version=6` is always the first line
- The comment block always comes **before** the `indicator()` call
- Separator lines are exactly `// ` followed by 76 `=` characters (79 characters total) — used once above and once below the Version/Author/Build block, and once more after Features, right before the blank line and `indicator(...)`
- Script name in the comment block always ends with `[WavesUnchained]`
- The `indicator()` title string also always ends with `[WavesUnchained]`
- Never prefix the script/indicator name with "Waves" — the `[WavesUnchained]` suffix already attributes it; the name itself starts directly with the indicator's own name (e.g. `ZigZag Core`, not `Waves ZigZag Core`)
- `Version:`, `Author: WavesUnchained`, `Build:` — always present, in that exact order, directly below the title line
- `Build:` date is `YYYY-MM-DD` or `YYYY-MM-DD HH:MM:SS`; kept from the original, only update it when the script is actually modified
- The description is prose (one sentence to a short paragraph), directly below the header separator, no blank line before it
- The `// Features:` heading is always the literal word "Features:" — don't replace it with a custom lead-in sentence
- One blank `//` line before `Features:` and one blank `//` line after the last bullet, before the closing separator
- Features use `✓` prefix (not `-`, `*`, or `•`)
- No `@description`, `@author`, `@version` JSDoc-style tags — use the structured fields above

## Dashboard table style

All indicator dashboards use the same light-theme table style. The reference implementation is `indicators/trend_direction/vein/vein_trend.pine`.

### Table init

```pine
var table t = table.new(position, columns, rows,
     bgcolor=color.new(color.white, 5),
     border_color=color.new(color.gray, 60),
     border_width=1,
     frame_color=color.new(color.gray, 40),
     frame_width=1)
```

### Color constants

```pine
color tc = color.new(color.gray, 20)   // standard text color (dark gray)
color hd = color.new(color.gray, 90)   // header row background (very light gray)
```

### Cell rules

- **Header row**: `text_color=tc`, `bgcolor=hd`, `text_size=size.small`
- **Data labels** (left column): `text_color=tc`, no explicit bgcolor, `text_size=size.small`
- **Data values**: `text_color=tc` (or accent color like `#00c853`, `#d50000`), no explicit bgcolor, `text_size=size.small`
- **Status cells with state**: dynamic `bgcolor` (colored when active, `color.new(color.gray, 80)` when inactive), `text_color=color.white` when colored, `tc` when inactive
- **Separator rows**: `bgcolor=color.new(color.gray, 80)`, empty text, one cell per column (no merge)
- **Accent colors**: bullish `#00c853`, bearish `#d50000`, warning `#ff6f00`, alert `#ffd600`
- No `merge_cells` for separator rows — set each cell individually
- No dark-theme backgrounds (`#131722` etc.) — the light table works on both TradingView themes
- Never use `size.tiny` for persistent dashboard or table text. It is not sufficiently readable on MacBook Pro Retina displays; `size.small` is the minimum unless the user explicitly requests otherwise.

## No performance claims in user-facing text

Backtest numbers are a **calibration tool**, not a selling point. They exist to improve
quality, and they belong only where their context (instrument, timeframe, sample size,
dataset) travels with them.

**Never** put performance figures or quality claims into user-facing surfaces:

- input `tooltip=` strings
- the `indicator()` / `strategy()` title and description
- `README.md`, `DESCRIPTION_TV.bbcode`, `CHANGELOG.md`
- chart labels, dashboard cells, alert messages

That means no win rates, no profit factors, no drawdown or R figures, and no quality
superlatives derived from them — "highest-quality signal", "the actual edge source",
"best in repo", "empirically validated", "data-driven default".

A tooltip explains **what a setting does and why it exists** ("filters persists that fire
without a real wave-reversal origin"). It never argues the setting is profitable.

**Allowed** — real statistics, in the internal calibration record:

- `strategies/<name>_strategy_assessment.md`, `APPROACH.md`, `todo.md`
- `testdata/`, analysis scripts and their reports
- `CATALOG.md` / root `README.md` status columns (status tracking, not promotion)
- `.claude/` working context

There, every figure carries instrument, timeframe, sample size, and the dataset it came
from (`test92`). Code comments may point at that record (`calibrated on test1`) but must
not repeat the numbers as proof of quality.

Unpublished research strategies under `strategies/` count as part of that record — their
tooltips may carry test-run figures while they are being tuned. The moment a script is
published, those figures come out.

Two hard limits that apply **everywhere**, including internal notes:

- Never state a "100% win rate" — it is a statement about the sample, not the signal.
- Never generalise from a small sample (n < 30) into a claim about a signal, a filter, or
  an instrument. Report `n` next to the figure or drop the figure.

## When adding a new indicator

1. Create a subdirectory under `indicators/<category>/<name>/`
2. Place the `.pine` file there
3. Write `README.md` following the structure above
4. Create `CHANGELOG.md` with the initial version entry
5. Write `DESCRIPTION_TV.bbcode` if the script is intended for TradingView publication
6. Add an entry to the root `README.md` under the appropriate section with a one-line description
7. Add an entry to `CATALOG.md` with status and quality ratings

`CATALOG.md` at the root is the operational status overview. Keep it up to date when indicator status or quality changes.

## Strategy infrastructure

Strategy files live in `strategies/`. They fall into two categories:

- **Generated** — produced by `build_strategies.py` from an indicator with a `@strategy-config` block. Regenerating overwrites any manual changes.
- **Standalone** — manually written and maintained (e.g. `wavetrend_v4_strategy.pine`, `reversal_engine_score_v1_strategy.pine`). These must **never** be regenerated or overwritten without explicit confirmation from the user.

**Rule: before running `build_strategies.py` in any form (including `# rebuild all`), identify which output files would be overwritten and ask for confirmation for any standalone strategy.**

To check whether a strategy is standalone: if the corresponding indicator has no `@strategy-config` block, the strategy is standalone.

### Generator

```bash
python3 scripts/build_strategies.py                        # rebuild all
python3 scripts/build_strategies.py indicators/momentum/foo/  # rebuild one
```

### @strategy-config annotation

To make an indicator eligible for strategy generation, add a config block at the end of the `.pine` file (after all code). TradingView ignores these comment lines.

```pine
// @strategy-config
// long:       longSignal
// short:      shortSignal
// sl_type:    trailing          // trailing | fixed | pivot_atr
// sl_long:    longStop          // for sl_type: trailing
// sl_short:   shortStop         // for sl_type: trailing
// sl:         SL                // for sl_type: fixed
// tp1:        TP1_lvl           // optional, for sl_type: fixed with TP levels
// tp2:        TP2_lvl
// tp3:        TP3_lvl
// tp_default: TP1               // default TP level shown in strategy inputs
// pivot_low:  low[pivRight]     // for sl_type: pivot_atr
// pivot_high: high[pivRight]    // for sl_type: pivot_atr
// @end-strategy-config
```

Multiple signals per direction: comma-separated (`long: sig1, sig2` → `sig1 or sig2`).

### Generated strategy features (always included)

Every generated strategy adds these inputs to the Strategy group:
- **Trade Direction** — Both / Long Only / Short Only
- **Entries on Confirmed Bar Only** (default: true) — prevents repainting
- **Cooldown Bars After Exit** (default: 0) — whipsaw protection
- **Break-Even Stop** (default: off) + **Break-Even Trigger (ATR×)**

Commission default: 0.02% (realistic for CFD/futures).

### Assessment files

Each strategy has a `strategies/<name>_strategy_assessment.md` documenting backtest runs and verdict. The schema is defined in `strategies/ASSESSMENT_SCHEMA.md`.

Ratings: **Not ready** (PF < 1.15 or Return/DD < 1.5) · **Promising** (PF ≥ 1.15, not yet out-of-sample validated) · **Ready** (PF ≥ 1.3, validated on ≥ 2 instruments)
