# Project Instructions

## Indicator directory structure

Each indicator (or suite of related indicators) lives in its own subdirectory under `indicators/`. The `indicators/commodity_pulse_matrix/` directory is the reference for how a directory should be structured.

Every indicator directory contains:

### `README.md`
Technical documentation for developers and users reading the code. Structure:
- Title as `# Heading`
- TradingView publication link directly below the title if the script is published: `**TradingView:** <url>`
- One-paragraph description of what the indicator does
- `## Features` — bullet list of capabilities
- Additional sections as needed (e.g. `## Scoring`, `## Modes`) explaining the logic and UI

### `DESCRIPTION_TV.bbcode`
The publication description for TradingView, written in BBCode. Structure:
- Opening bold title line
- `[b]What it does[/b]` — plain-language explanation of the purpose
- Key sections as `[b]Section[/b]` headings with `[list][*]...[/list]` for feature lists
- Closing `[hr]` followed by the standard trading disclaimer in `[i]...[/i]`:

  > This script is provided for educational and informational purposes only. It does not constitute financial advice. Trading commodities and other financial instruments involves substantial risk of loss and is not suitable for all investors. Past performance of any indicator or system is not indicative of future results. Always conduct your own research, apply proper risk management, and consider consulting a qualified financial advisor before making trading decisions.

### The `.pine` file(s)
The script itself. No additional wrapper or build files.

The header of `indicators/commodity_pulse_matrix/commodity_pulse_matrix_v3.pine` is the reference for how every `.pine` file should start. The exact structure:

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
- Script name in the comment block always ends with `[WavesUnchained]`
- The `indicator()` title string also always ends with `[WavesUnchained]`
- Features use `✓` prefix (not `-` or `*`)
- `Build:` date is kept from the original; only update it when the script is actually modified
- No `@description`, `@author`, `@version` JSDoc-style tags — use the structured fields above

## Dashboard table style

All indicator dashboards use the same light-theme table style. The reference implementation is `indicators/vein/vein_trend.pine`.

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
- **Data labels** (left column): `text_color=tc`, no explicit bgcolor, `text_size=size.small` or `size.tiny`
- **Data values**: `text_color=tc` (or accent color like `#00c853`, `#d50000`), no explicit bgcolor
- **Status cells with state**: dynamic `bgcolor` (colored when active, `color.new(color.gray, 80)` when inactive), `text_color=color.white` when colored, `tc` when inactive
- **Separator rows**: `bgcolor=color.new(color.gray, 80)`, empty text, one cell per column (no merge)
- **Accent colors**: bullish `#00c853`, bearish `#d50000`, warning `#ff6f00`, alert `#ffd600`
- No `merge_cells` for separator rows — set each cell individually
- No dark-theme backgrounds (`#131722` etc.) — the light table works on both TradingView themes

## When adding a new indicator

1. Create a subdirectory under `indicators/<name>/`
2. Place the `.pine` file there
3. Write `README.md` following the structure above
4. Write `DESCRIPTION_TV.bbcode` if the script is intended for TradingView publication
5. Add an entry to the root `README.md` under the appropriate section with a one-line description

## Strategy infrastructure

Generated strategy files live in `strategies/`. Never edit them by hand — they are always regenerated from the indicator source.

### Generator

```bash
python3 scripts/build_strategies.py                        # rebuild all
python3 scripts/build_strategies.py indicators/foo/        # rebuild one
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
