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
- Features use `✓` prefix (not `-` or `*`)
- `Build:` date is kept from the original; only update it when the script is actually modified
- No `@description`, `@author`, `@version` JSDoc-style tags — use the structured fields above

## When adding a new indicator

1. Create a subdirectory under `indicators/<name>/`
2. Place the `.pine` file there
3. Write `README.md` following the structure above
4. Write `DESCRIPTION_TV.bbcode` if the script is intended for TradingView publication
5. Add an entry to the root `README.md` under the appropriate section with a one-line description
