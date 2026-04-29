#!/usr/bin/env python3
"""
build_strategies.py — WavesUnchained strategy generator

Scans indicators/ for @strategy-config annotation blocks, then generates
a ready-to-use TradingView strategy .pine file in strategies/ for each
annotated indicator.

Usage:
    python scripts/build_strategies.py                     # rebuild all
    python scripts/build_strategies.py indicators/smooth_trend_radar/
    python scripts/build_strategies.py indicators/smooth_trend_radar/smooth_trend_radar.pine
"""

import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).parent.parent
INDICATORS_DIR = ROOT / "indicators"
OUTPUT_DIR = ROOT / "strategies"

# ─── Pine fragments injected by the generator ─────────────────────────────────

_STRATEGY_HEADER = """\
// ─── Strategy inputs (generated) ─────────────────────────────────────────────
g_strat       = "Strategy"
tradeDirInput = input.string("Both", "Trade Direction",
     options=["Both", "Long Only", "Short Only"], group=g_strat,
     tooltip="Filter entries by direction. Useful for asymmetric instruments.")
confirmClose  = input.bool(true,  "Entries on Confirmed Bar Only", group=g_strat,
     tooltip="Only trigger entries on closed bars. Prevents repainting in live trading.")
cooldownBars  = input.int(0,     "Cooldown Bars After Exit", minval=0, group=g_strat,
     tooltip="Block new entries for N bars after a position closes. Set 0 to disable.")
enableBE      = input.bool(false, "Break-Even Stop", group=g_strat,
     tooltip="Move SL to entry price once the trade is N×ATR in profit.")
beATRInput    = input.float(1.0,  "Break-Even Trigger (ATR×)", minval=0.1, step=0.1, group=g_strat,
     tooltip="ATR distance from entry that triggers the break-even move.")

var int _lastExitBar = na
_justClosed = strategy.closedtrades > 0 and strategy.closedtrades.exit_bar_index(0) == bar_index
if _justClosed
    _lastExitBar := bar_index
_inCooldown = cooldownBars > 0 and not na(_lastExitBar) and (bar_index - _lastExitBar) < cooldownBars
_canEntry   = not _inCooldown and (not confirmClose or barstate.isconfirmed)
"""

_TP_LEVEL_INPUT = """\
exitLvlInput  = input.string("{default_tp}", "Exit at TP",
     options=["TP1", "TP2", "TP3", "None (next signal)"], group=g_strat,
     tooltip="TP level for the exit limit order. 'None' holds until the next opposing signal.")
"""

_PIVOT_ATR_INPUTS = """\
slBufInput = input.float(0.5, "SL ATR Buffer (×)", minval=0.1, step=0.1, group=g_strat,
     tooltip="ATR distance beyond the divergence pivot for the stop loss.")
tpRRInput  = input.float(2.0, "TP R:R Ratio",      minval=0.5, step=0.5, group=g_strat,
     tooltip="Take profit at this R:R multiple of the SL distance from entry.")
"""

# sl_type: trailing — separate long/short trailing stops
_EXEC_TRAILING = """\

// ─── Strategy execution (generated) ──────────────────────────────────────────
_canLong  = tradeDirInput != "Short Only"
_canShort = tradeDirInput != "Long Only"

if ({long}) and _canLong and _canEntry
    strategy.entry("Long", strategy.long)
if ({short}) and _canShort and _canEntry
    strategy.entry("Short", strategy.short)

if strategy.position_size > 0
    strategy.exit("Long Exit", "Long", stop={sl_long})
if strategy.position_size < 0
    strategy.exit("Short Exit", "Short", stop={sl_short})
"""

# sl_type: fixed, no pre-computed TP
_EXEC_FIXED = """\

// ─── Strategy execution (generated) ──────────────────────────────────────────
_canLong  = tradeDirInput != "Short Only"
_canShort = tradeDirInput != "Long Only"

if ({long}) and _canLong and _canEntry
    strategy.entry("Long", strategy.long)
if ({short}) and _canShort and _canEntry
    strategy.entry("Short", strategy.short)

if strategy.position_size > 0
    strategy.exit("Long Exit", "Long", stop={sl})
if strategy.position_size < 0
    strategy.exit("Short Exit", "Short", stop={sl})
"""

# sl_type: fixed, pre-computed TP1/TP2/TP3
_EXEC_FIXED_TP = """\

// ─── Strategy execution (generated) ──────────────────────────────────────────
_canLong  = tradeDirInput != "Short Only"
_canShort = tradeDirInput != "Long Only"

var float _exitTP = na

_doLong  = ({long})  and _canLong  and _canEntry
_doShort = ({short}) and _canShort and _canEntry

if _doLong
    _exitTP := exitLvlInput == "TP1" ? {tp1} :
               exitLvlInput == "TP2" ? {tp2} :
               exitLvlInput == "TP3" ? {tp3} : na
    strategy.entry("Long", strategy.long)

if _doShort
    _exitTP := exitLvlInput == "TP1" ? {tp1} :
               exitLvlInput == "TP2" ? {tp2} :
               exitLvlInput == "TP3" ? {tp3} : na
    strategy.entry("Short", strategy.short)

if strategy.position_size > 0
    strategy.exit("Long Exit", "Long", stop={sl}, limit=_exitTP)
if strategy.position_size < 0
    strategy.exit("Short Exit", "Short", stop={sl}, limit=_exitTP)
"""

# sl_type: pivot_atr — SL computed from divergence pivot + ATR buffer
_EXEC_PIVOT_ATR = """\

// ─── Strategy execution (generated) ──────────────────────────────────────────
_canLong  = tradeDirInput != "Short Only"
_canShort = tradeDirInput != "Long Only"

var float _sl = na
var float _tp = na

if ({long}) and _canLong and _canEntry
    _atr    = ta.atr(14)
    _sl    := {pivot_low} - _atr * slBufInput
    _slDist = math.max(close - _sl, syminfo.mintick)
    _tp    := close + _slDist * tpRRInput
    strategy.entry("Long", strategy.long)

if ({short}) and _canShort and _canEntry
    _atr    = ta.atr(14)
    _sl    := {pivot_high} + _atr * slBufInput
    _slDist = math.max(_sl - close, syminfo.mintick)
    _tp    := close - _slDist * tpRRInput
    strategy.entry("Short", strategy.short)

if strategy.position_size > 0
    strategy.exit("Long Exit", "Long", stop=_sl, limit=_tp)
if strategy.position_size < 0
    strategy.exit("Short Exit", "Short", stop=_sl, limit=_tp)
"""

_EXEC_RISK_MANAGEMENT = """\

// ─── Break-even management (generated) ────────────────────────────────────────
if enableBE
    _beAtr = ta.atr(14) * beATRInput
    if strategy.position_size > 0 and close >= strategy.position_avg_price + _beAtr
        strategy.exit("Long BE", "Long", stop=strategy.position_avg_price)
    if strategy.position_size < 0 and close <= strategy.position_avg_price - _beAtr
        strategy.exit("Short BE", "Short", stop=strategy.position_avg_price)
"""


# ─── Parsing helpers ──────────────────────────────────────────────────────────

def parse_strategy_config(source: str) -> dict | None:
    """
    Extract key:value pairs from the @strategy-config block.
    Returns None when no block is found.
    """
    m = re.search(
        r"//\s*@strategy-config\s*\n(.*?)//\s*@end-strategy-config",
        source,
        re.DOTALL,
    )
    if not m:
        return None
    cfg: dict[str, str] = {}
    for line in m.group(1).splitlines():
        pair = re.match(r"//\s*(\w+)\s*:\s*(.+)", line)
        if pair:
            cfg[pair.group(1).strip()] = pair.group(2).strip()
    return cfg


def extract_indicator_call(source: str) -> tuple[str, dict]:
    """
    Find the indicator(...) call (handles multi-line).
    Returns (full_call_string, {title, overlay, extra_params}).
    """
    pos = source.find("indicator(")
    if pos == -1:
        return "", {}

    depth, end = 0, pos
    for i in range(pos, len(source)):
        if source[i] == "(":
            depth += 1
        elif source[i] == ")":
            depth -= 1
            if depth == 0:
                end = i + 1
                break

    call = source[pos:end]
    params: dict[str, str] = {}

    m = re.search(r'indicator\s*\(\s*["\']([^"\']+)["\']', call)
    if m:
        params["title"] = m.group(1)

    m = re.search(r"overlay\s*=\s*(true|false)", call)
    params["overlay"] = m.group(1) if m else "false"

    # Collect remaining key=value params to forward to strategy()
    extras = []
    for key in ("format", "precision", "max_lines_count",
                "max_labels_count", "max_boxes_count", "max_bars_back"):
        m = re.search(rf"{key}\s*=\s*([^\s,)]+)", call)
        if m:
            extras.append(f"{key}={m.group(1)}")
    params["extras"] = extras

    return call, params


def build_strategy_call(ind: dict) -> str:
    title   = ind.get("title", "Indicator [WavesUnchained]")
    overlay = ind.get("overlay", "false")
    extras  = ind.get("extras", [])

    strat_title = title if "— Strategy" in title else title + " — Strategy"

    parts = [f'strategy("{strat_title}", overlay={overlay}']
    parts += [f"     {e}" for e in extras]
    parts += [
        "     default_qty_type=strategy.percent_of_equity, default_qty_value=10",
        "     commission_type=strategy.commission.percent, commission_value=0.02",
        "     slippage=1, max_bars_back=500)",
    ]
    return ",\n".join(parts)


def signals_expr(raw: str) -> str:
    """'sig1, sig2' → 'sig1 or sig2',  'sig1' → 'sig1'"""
    parts = [s.strip() for s in raw.split(",") if s.strip()]
    return " or ".join(parts)


def remove_alertconditions(source: str) -> str:
    """
    Remove alertcondition() calls — they are not valid in strategy scripts
    and cause a compile error.
    """
    return re.sub(
        r"alertcondition\s*\((?:[^)(]|\((?:[^)(]|\([^)(]*\))*\))*\)\s*\n?",
        "",
        source,
    )


def update_header(source: str, stem: str) -> str:
    """Append '— Strategy (generated)' to the script name line in the header."""
    return re.sub(
        r"(//\s*" + re.escape(stem.replace("_", " ").title()) + r".*?\[WavesUnchained\])",
        r"\1 — Strategy (generated)",
        source,
        count=1,
        flags=re.IGNORECASE,
    )


# ─── Main transform ───────────────────────────────────────────────────────────

def generate(pine_path: Path) -> tuple[str, str] | None:
    """
    Build a strategy file from a Pine indicator file.
    Returns (output_filename, content) or None.
    """
    source = pine_path.read_text(encoding="utf-8")

    cfg = parse_strategy_config(source)
    if cfg is None:
        return None

    call, ind = extract_indicator_call(source)
    if not call:
        print(f"  WARN  no indicator() call in {pine_path.name}")
        return None

    sl_type    = cfg.get("sl_type", "fixed")
    long_expr  = signals_expr(cfg.get("long",  "longSignal"))
    short_expr = signals_expr(cfg.get("short", "shortSignal"))

    # ── Transform source ──────────────────────────────────────────────────────
    out = source

    # 1. Replace indicator() with strategy()
    out = out.replace(call, build_strategy_call(ind), 1)

    # 2. Remove alertcondition() calls
    out = remove_alertconditions(out)

    # 3. Strip the @strategy-config block itself from the output
    out = re.sub(
        r"\n?// @strategy-config.*?// @end-strategy-config\n?",
        "",
        out,
        flags=re.DOTALL,
    )

    # 4. Update header name line
    out = update_header(out, pine_path.stem)

    # ── Build extra inputs + execution block ──────────────────────────────────
    extra_inputs = ""
    exec_block   = ""

    if sl_type == "trailing":
        sl_long  = cfg.get("sl_long",  "longStop")
        sl_short = cfg.get("sl_short", "shortStop")
        exec_block = _EXEC_TRAILING.format(
            long=long_expr, short=short_expr,
            sl_long=sl_long, sl_short=sl_short,
        )

    elif sl_type == "fixed":
        sl_var   = cfg.get("sl", "SL")
        has_tp   = any(k in cfg for k in ("tp1", "tp2", "tp3"))
        if has_tp:
            default_tp = cfg.get("tp_default", "TP2").upper()
            extra_inputs = _TP_LEVEL_INPUT.format(default_tp=default_tp)
            exec_block   = _EXEC_FIXED_TP.format(
                long=long_expr, short=short_expr,
                sl=sl_var,
                tp1=cfg.get("tp1", "na"),
                tp2=cfg.get("tp2", "na"),
                tp3=cfg.get("tp3", "na"),
            )
        else:
            exec_block = _EXEC_FIXED.format(
                long=long_expr, short=short_expr, sl=sl_var,
            )

    elif sl_type == "pivot_atr":
        pivot_low  = cfg.get("pivot_low",  "low[pivRight]")
        pivot_high = cfg.get("pivot_high", "high[pivRight]")
        extra_inputs = _PIVOT_ATR_INPUTS
        exec_block   = _EXEC_PIVOT_ATR.format(
            long=long_expr, short=short_expr,
            pivot_low=pivot_low, pivot_high=pivot_high,
        )

    else:
        print(f"  WARN  unknown sl_type '{sl_type}' in {pine_path.name}")
        return None

    out = out.rstrip("\n") + "\n"
    out += _STRATEGY_HEADER
    out += extra_inputs
    out += exec_block
    out += _EXEC_RISK_MANAGEMENT

    out_name = pine_path.stem + "_strategy.pine"
    return out_name, out


# ─── Entry point ──────────────────────────────────────────────────────────────

def main() -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)

    targets = sys.argv[1:] if len(sys.argv) > 1 else [str(INDICATORS_DIR)]
    pine_files: list[Path] = []
    for t in targets:
        p = Path(t).resolve()
        if p.is_file() and p.suffix == ".pine":
            pine_files.append(p)
        else:
            pine_files.extend(sorted(p.rglob("*.pine")))

    # Never process files already in strategies/
    pine_files = [f for f in pine_files if OUTPUT_DIR not in f.resolve().parents]

    generated = 0
    for pine_path in pine_files:
        result = generate(pine_path)
        if result is None:
            continue
        name, content = result
        out_path = OUTPUT_DIR / name
        out_path.write_text(content, encoding="utf-8")
        rel = pine_path.relative_to(ROOT)
        print(f"  ✓  {rel}  →  strategies/{name}")
        generated += 1

    if generated == 0:
        print("Nothing generated — add @strategy-config blocks to indicator files.")
    else:
        print(f"\n{generated} strategy file(s) written to strategies/")


if __name__ == "__main__":
    main()
