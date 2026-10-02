# Project Instructions

## Indicator directory structure

Each indicator (or suite of related indicators) lives in its own subdirectory under a category folder inside `indicators/`. The `indicators/composite/commodity_pulse_matrix/` directory is the reference for how an indicator directory should be structured.

Every indicator directory contains `README.md`, `CHANGELOG.md`, `DESCRIPTION_TV.bbcode` (if published), optional `screenshots/`, and the `.pine` file(s). Format rules live in `.claude/rules/` (`indicator-docs.md`, `pine-script-header.md`, `dashboard-table-style.md`) and load when matching files are read.

## Data source validity

Before any indicator uses `volume`, VWAP, Volume Profile, Open Interest, term structure or a
cross-symbol `request.security()`, check [`DATA_VALIDITY.md`](DATA_VALIDITY.md) — the matrix of
which data class carries a real signal on which instrument type. Skill: `instrument-data-validity`.

Core rule: volume validity comes from `syminfo.volumetype` (`base`/`quote` = real, `tick`/`n/a` =
not), never from the existence of a `volume` series. `nz(volume)` is not a guard.

Every `.pine` file carries a Data Contract block in its header — format in `.claude/rules/pine-script-header.md`.

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
3. Write `README.md` following `.claude/rules/indicator-docs.md`
4. Create `CHANGELOG.md` with the initial version entry
5. Write `DESCRIPTION_TV.bbcode` if the script is intended for TradingView publication
6. Add an entry to `INDICATORS.md` under the appropriate section with a one-line description
7. Add an entry to `CATALOG.md` with status and quality ratings

`CATALOG.md` at the root is the operational status overview. Keep it up to date when indicator status or quality changes.

## Strategy infrastructure

Strategy files live in `strategies/<name>/`. **All of them are standalone and hand-maintained.**
There is no generator — `scripts/build_strategies.py` was removed on 2026-09-08; its knowledge
now lives in the Claude Code skill `strategy-from-indicator`.

Use that skill whenever a strategy is built from an indicator or pulled back in line with a
changed indicator. It carries the standard input groups, the exit patterns, the
`indicator()` → `strategy()` transformation and the chart-type guard.

`@strategy-config` block, standard strategy features and assessment files: `.claude/rules/strategy-config-annotation.md`, `.claude/rules/strategies.md`.
