use calamine::{Data, Reader, open_workbook_auto};
use std::collections::BTreeMap;
use std::env;
use std::fs;
use std::io;
use std::path::{Path, PathBuf};

const REAL_EXIT_MARKER: &str = "WT3 REAL EXIT";
const RAW_WT_MARKER: &str = "RAW_WT:";
const REQUIRED_FIELDS: &[(&str, FieldKind)] = &[
    ("dir", FieldKind::Enum(&["LONG", "SHORT"])),
    ("family", FieldKind::Enum(&["rr", "pb", "er"])),
    ("exit", FieldKind::Text),
    ("profile", FieldKind::Text),
    ("tf", FieldKind::Text),
    ("chartSec", FieldKind::Integer),
    ("executionMode", FieldKind::Text),
    ("trade", FieldKind::Integer),
    ("barsHeld", FieldKind::Number),
    ("pnl", FieldKind::Number),
    ("R", FieldKind::Number),
    ("entry", FieldKind::Number),
    ("exitPx", FieldKind::Number),
    ("MFE", FieldKind::Number),
    ("MAE", FieldKind::Number),
    ("capturePct", FieldKind::OptionalNumber),
    ("targetPx", FieldKind::Number),
    ("targetRoomR", FieldKind::Number),
    ("targetRoomATR", FieldKind::Number),
    ("targetHit", FieldKind::Bool),
    ("barsToTarget", FieldKind::OptionalNumber),
    ("favPivotPx", FieldKind::OptionalNumber),
    ("favPivotR", FieldKind::OptionalNumber),
    ("barsToFavPivot", FieldKind::OptionalNumber),
    ("advPivotPx", FieldKind::OptionalNumber),
    ("advPivotR", FieldKind::OptionalNumber),
    ("barsToAdvPivot", FieldKind::OptionalNumber),
    ("entryScore", FieldKind::Number),
    ("entryStruct", FieldKind::EntryStruct),
];

const ENTRY_STRUCT_FIELDS: &[(&str, FieldKind)] = &[
    ("hh", FieldKind::Bool),
    ("hl", FieldKind::Bool),
    ("lh", FieldKind::Bool),
    ("ll", FieldKind::Bool),
    ("longStruct", FieldKind::Bool),
    ("shortStruct", FieldKind::Bool),
    ("rangePos", FieldKind::Number),
    ("target", FieldKind::Number),
    ("stop", FieldKind::Number),
];

#[derive(Debug, Clone, Copy)]
enum FieldKind {
    Text,
    Number,
    OptionalNumber,
    Integer,
    Bool,
    EntryStruct,
    Enum(&'static [&'static str]),
}

#[derive(Debug, Clone)]
struct Trade {
    source: String,
    dir: String,
    family: String,
    exit: String,
    profile: String,
    tf: String,
    chart_sec: Option<i64>,
    execution_mode: String,
    bars_held: Option<f64>,
    pnl: Option<f64>,
    r: Option<f64>,
    mfe: Option<f64>,
    mae: Option<f64>,
    capture_pct: Option<f64>,
    target_room_r: Option<f64>,
    target_room_atr: Option<f64>,
    target_hit: bool,
    bars_to_target: Option<f64>,
    fav_pivot_r: Option<f64>,
    bars_to_fav_pivot: Option<f64>,
    adv_pivot_r: Option<f64>,
    bars_to_adv_pivot: Option<f64>,
    entry_score: Option<f64>,
    hh: Option<bool>,
    hl: Option<bool>,
    lh: Option<bool>,
    ll: Option<bool>,
    long_struct: Option<bool>,
    short_struct: Option<bool>,
    structure_phase: String,
    playbook: String,
    wt_bull_div: Option<bool>,
    wt_bear_div: Option<bool>,
    high_confirm_bars: Option<f64>,
    low_confirm_bars: Option<f64>,
    high_actual_bars: Option<f64>,
    low_actual_bars: Option<f64>,
    range_pos: Option<f64>,
}

#[derive(Debug, Clone)]
struct RawWtEvent {
    source: String,
    dir: String,
    profile: String,
    playbook_active: String,
    structure_phase: String,
    pivot_confirm_bars: Option<f64>,
    pivot_actual_bars: Option<f64>,
    piv_len: Option<f64>,
}

#[derive(Debug, Clone, Default)]
struct Stats {
    n: usize,
    wins: usize,
    target_hits: usize,
    pnl_sum: f64,
    r_sum: f64,
    r_n: usize,
    mfe_sum: f64,
    mfe_n: usize,
    mae_sum: f64,
    mae_n: usize,
    capture_sum: f64,
    capture_n: usize,
    target_room_r_sum: f64,
    target_room_r_n: usize,
    bars_sum: f64,
    bars_n: usize,
    bars_to_target_sum: f64,
    bars_to_target_n: usize,
    fav_pivot_r_sum: f64,
    fav_pivot_r_n: usize,
    adv_pivot_r_sum: f64,
    adv_pivot_r_n: usize,
}

#[derive(Debug, Clone, Default)]
struct StrategyRun {
    source: String,
    tf: String,
    profile: String,
    execution_mode: String,
    net_profit: Option<f64>,
    gross_profit: Option<f64>,
    gross_loss: Option<f64>,
    commission: Option<f64>,
    max_drawdown: Option<f64>,
    trades: Option<f64>,
    winners: Option<f64>,
    win_rate: Option<f64>,
    avg_trade: Option<f64>,
    win_loss_ratio: Option<f64>,
    profit_factor: Option<f64>,
    sharpe: Option<f64>,
    exits: BTreeMap<String, ExitSummary>,
}

#[derive(Debug, Clone, Default)]
struct ExitSummary {
    n: usize,
    pnl: f64,
}

impl Stats {
    fn add(&mut self, t: &Trade) {
        self.n += 1;
        if t.pnl.unwrap_or(0.0) > 0.0 {
            self.wins += 1;
        }
        if t.target_hit {
            self.target_hits += 1;
        }
        self.pnl_sum += t.pnl.unwrap_or(0.0);
        add_opt(t.r, &mut self.r_sum, &mut self.r_n);
        add_opt(t.mfe, &mut self.mfe_sum, &mut self.mfe_n);
        add_opt(t.mae, &mut self.mae_sum, &mut self.mae_n);
        add_opt(t.capture_pct, &mut self.capture_sum, &mut self.capture_n);
        add_opt(
            t.target_room_r,
            &mut self.target_room_r_sum,
            &mut self.target_room_r_n,
        );
        add_opt(t.bars_held, &mut self.bars_sum, &mut self.bars_n);
        add_opt(
            t.bars_to_target,
            &mut self.bars_to_target_sum,
            &mut self.bars_to_target_n,
        );
        add_opt(
            t.fav_pivot_r,
            &mut self.fav_pivot_r_sum,
            &mut self.fav_pivot_r_n,
        );
        add_opt(
            t.adv_pivot_r,
            &mut self.adv_pivot_r_sum,
            &mut self.adv_pivot_r_n,
        );
    }

    fn win_rate(&self) -> f64 {
        pct(self.wins, self.n)
    }

    fn target_rate(&self) -> f64 {
        pct(self.target_hits, self.n)
    }
}

fn main() {
    if let Err(err) = run() {
        eprintln!("error: {err}");
        std::process::exit(1);
    }
}

fn run() -> Result<(), Box<dyn std::error::Error>> {
    let args: Vec<String> = env::args().collect();
    if args.len() < 2 {
        print_usage(&args[0]);
        return Ok(());
    }

    match args[1].as_str() {
        "analyze" => analyze_command(&args),
        "schema" => {
            println!("{}", render_schema_markdown());
            Ok(())
        }
        "validate" => validate_command(&args),
        "--help" | "-h" => {
            print_usage(&args[0]);
            Ok(())
        }
        other => Err(format!("unknown command: {other}").into()),
    }
}

fn analyze_command(args: &[String]) -> Result<(), Box<dyn std::error::Error>> {
    if args.len() < 3 {
        print_usage(&args[0]);
        return Ok(());
    }

    let input = PathBuf::from(&args[2]);
    let mut out_md: Option<PathBuf> = None;
    let mut out_csv: Option<PathBuf> = None;
    let mut i = 3;
    while i < args.len() {
        match args[i].as_str() {
            "--out" if i + 1 < args.len() => {
                out_md = Some(PathBuf::from(&args[i + 1]));
                i += 2;
            }
            "--trades-csv" if i + 1 < args.len() => {
                out_csv = Some(PathBuf::from(&args[i + 1]));
                i += 2;
            }
            "--help" | "-h" => {
                print_usage(&args[0]);
                return Ok(());
            }
            other => return Err(format!("unknown argument: {other}").into()),
        }
    }

    let trades = load_trades(&input)?;
    if trades.is_empty() {
        return Err(format!("no {REAL_EXIT_MARKER} rows found under {}", input.display()).into());
    }
    let strategy_runs = load_strategy_runs(&input)?;
    let raw_wt_events = load_raw_wt_events(&input)?;

    let report = render_markdown_report(&input, &trades, &strategy_runs, &raw_wt_events);
    if let Some(path) = out_md {
        write_parented(&path, report.as_bytes())?;
    } else {
        println!("{report}");
    }

    if let Some(path) = out_csv {
        write_parented(&path, render_trades_csv(&trades).as_bytes())?;
    }

    Ok(())
}

fn validate_command(args: &[String]) -> Result<(), Box<dyn std::error::Error>> {
    if args.len() != 3 {
        print_usage(&args[0]);
        return Ok(());
    }

    let input = PathBuf::from(&args[2]);
    let diagnostics = validate_logs(&input)?;
    if diagnostics.is_empty() {
        println!("ok: log format valid");
        Ok(())
    } else {
        for diagnostic in &diagnostics {
            eprintln!(
                "{}:{}: {}",
                diagnostic.source.display(),
                diagnostic.line,
                diagnostic.message
            );
        }
        Err(format!("{} log format issue(s)", diagnostics.len()).into())
    }
}

fn print_usage(bin: &str) {
    eprintln!(
        "usage:\n  {bin} analyze <file-or-dir> [--out report.md] [--trades-csv trades.csv]\n  {bin} validate <file-or-dir>\n  {bin} schema\n\n\
         Parses TradingView CSV logs containing `WT3 REAL EXIT | key=value | ...` rows."
    );
}

fn load_trades(input: &Path) -> io::Result<Vec<Trade>> {
    let files = collect_files(input)?;
    let mut trades = Vec::new();
    for file in files {
        let content = fs::read_to_string(&file)?;
        for line in content.lines() {
            if !line.contains(REAL_EXIT_MARKER) {
                continue;
            }
            let message = csv_last_field(line);
            if let Some(trade) = parse_trade(&message, &file) {
                trades.push(trade);
            }
        }
    }
    Ok(trades)
}

fn load_raw_wt_events(input: &Path) -> io::Result<Vec<RawWtEvent>> {
    let files = collect_files(input)?;
    let mut dedup = BTreeMap::new();
    for file in files {
        let content = fs::read_to_string(&file)?;
        for line in content.lines() {
            if !line.contains(RAW_WT_MARKER) {
                continue;
            }
            let message = csv_last_field(line);
            for event in parse_raw_wt_events(&message, &file) {
                let key = format!(
                    "{}|{}|{}|{}|{}",
                    event.source,
                    parse_pipe_fields(&message)
                        .get("bar")
                        .cloned()
                        .unwrap_or_default(),
                    event.profile,
                    event.dir,
                    event.playbook_active
                );
                dedup.entry(key).or_insert(event);
            }
        }
    }
    Ok(dedup.into_values().collect())
}

fn load_strategy_runs(input: &Path) -> Result<Vec<StrategyRun>, Box<dyn std::error::Error>> {
    let files = collect_xlsx_files(input)?;
    let mut runs = Vec::new();
    for file in files {
        match parse_strategy_run(&file) {
            Ok(run) => runs.push(run),
            Err(err) => eprintln!("warning: failed to read {}: {err}", file.display()),
        }
    }
    Ok(runs)
}

fn collect_xlsx_files(input: &Path) -> io::Result<Vec<PathBuf>> {
    if input.is_file() {
        return Ok(
            if input.extension().and_then(|ext| ext.to_str()) == Some("xlsx") {
                vec![input.to_path_buf()]
            } else {
                Vec::new()
            },
        );
    }

    let mut files = Vec::new();
    collect_xlsx_files_recursive(input, &mut files)?;
    files.sort();
    Ok(files)
}

fn collect_xlsx_files_recursive(dir: &Path, files: &mut Vec<PathBuf>) -> io::Result<()> {
    for entry in fs::read_dir(dir)? {
        let path = entry?.path();
        if path.is_dir() {
            collect_xlsx_files_recursive(&path, files)?;
        } else if path.extension().and_then(|ext| ext.to_str()) == Some("xlsx") {
            files.push(path);
        }
    }
    Ok(())
}

fn parse_strategy_run(path: &Path) -> Result<StrategyRun, Box<dyn std::error::Error>> {
    let mut workbook = open_workbook_auto(path)?;
    let properties = read_key_value_sheet(&mut workbook, "Eigenschaften");
    let performance = read_key_value_sheet(&mut workbook, "Performance");
    let trade_analysis = read_key_value_sheet(&mut workbook, "Analyse der Trades");
    let risk = read_key_value_sheet(&mut workbook, "Risikogewichtete Performance");
    let exits = read_exit_summary(&mut workbook);

    Ok(StrategyRun {
        source: path.display().to_string(),
        tf: normalize_tv_tf(
            properties
                .get("Zeitrahmen")
                .map(String::as_str)
                .unwrap_or(""),
        ),
        profile: properties
            .get("Strategy Profile")
            .cloned()
            .unwrap_or_else(|| "unknown".to_string()),
        execution_mode: properties
            .get("1H Execution Mode")
            .cloned()
            .unwrap_or_else(|| "unknown".to_string()),
        net_profit: number_from_map(&performance, "Nettogewinn"),
        gross_profit: number_from_map(&performance, "Bruttogewinn"),
        gross_loss: number_from_map(&performance, "Bruttoverlust"),
        commission: number_from_map(&performance, "Gezahlte Provision"),
        max_drawdown: number_from_map(&performance, "Max. Drawdown (innerhalb Balken)"),
        trades: number_from_map(&trade_analysis, "Trades insgesamt"),
        winners: number_from_map(&trade_analysis, "Gewinnbringende Trades"),
        win_rate: percent_from_trade_analysis(&trade_analysis),
        avg_trade: number_from_map(&trade_analysis, "Durchschn. G&V"),
        win_loss_ratio: number_from_map(
            &trade_analysis,
            "Verhältnis von durchschn. Gewinn / durchschn. Verlust",
        ),
        profit_factor: number_from_map(&risk, "Profitfaktor"),
        sharpe: number_from_map(&risk, "Sharpe-Ratio"),
        exits,
    })
}

fn read_key_value_sheet<R, RS>(workbook: &mut R, sheet: &str) -> BTreeMap<String, String>
where
    R: Reader<RS>,
    RS: std::io::Read + std::io::Seek,
{
    let mut out = BTreeMap::new();
    if let Ok(range) = workbook.worksheet_range(sheet) {
        for row in range.rows() {
            if row.len() < 2 {
                continue;
            }
            let key = cell_string(&row[0]);
            if key.is_empty() {
                continue;
            }
            out.insert(key, cell_string(&row[1]));
        }
    }
    out
}

fn read_exit_summary<R, RS>(workbook: &mut R) -> BTreeMap<String, ExitSummary>
where
    R: Reader<RS>,
    RS: std::io::Read + std::io::Seek,
{
    let mut exits = BTreeMap::new();
    if let Ok(range) = workbook.worksheet_range("Liste der Trades") {
        for row in range.rows().skip(1) {
            if row.len() < 8 {
                continue;
            }
            let kind = cell_string(&row[1]);
            if !kind.contains("Ausstieg") {
                continue;
            }
            let signal = cell_string(&row[3]);
            if signal.is_empty() {
                continue;
            }
            let pnl = cell_f64(&row[7]).unwrap_or(0.0);
            let summary = exits.entry(signal).or_insert_with(ExitSummary::default);
            summary.n += 1;
            summary.pnl += pnl;
        }
    }
    exits
}

fn cell_string(cell: &Data) -> String {
    match cell {
        Data::Empty => String::new(),
        Data::String(value) => value.trim().to_string(),
        Data::Float(value) => trim_float(*value),
        Data::Int(value) => value.to_string(),
        Data::Bool(value) => {
            if *value {
                "true".to_string()
            } else {
                "false".to_string()
            }
        }
        other => other.to_string().trim().to_string(),
    }
}

fn cell_f64(cell: &Data) -> Option<f64> {
    match cell {
        Data::Float(value) => Some(*value),
        Data::Int(value) => Some(*value as f64),
        Data::String(value) => parse_number(value),
        _ => None,
    }
}

fn number_from_map(map: &BTreeMap<String, String>, key: &str) -> Option<f64> {
    map.get(key).and_then(|value| parse_number(value))
}

fn percent_from_trade_analysis(map: &BTreeMap<String, String>) -> Option<f64> {
    map.get("Prozentsatz gewinnbringend")
        .and_then(|value| parse_number(value))
        .or_else(|| {
            let wins = number_from_map(map, "Gewinnbringende Trades")?;
            let trades = number_from_map(map, "Trades insgesamt")?;
            if trades > 0.0 {
                Some(wins / trades * 100.0)
            } else {
                None
            }
        })
}

fn parse_number(value: &str) -> Option<f64> {
    let normalized = value.trim().replace('%', "").replace(',', ".");
    if normalized.is_empty()
        || normalized.eq_ignore_ascii_case("nan")
        || normalized.eq_ignore_ascii_case("na")
    {
        return None;
    }
    normalized.parse::<f64>().ok().filter(|v| v.is_finite())
}

fn trim_float(value: f64) -> String {
    if value.fract() == 0.0 {
        format!("{value:.0}")
    } else {
        value.to_string()
    }
}

fn normalize_tv_tf(raw: &str) -> String {
    match raw {
        "5 Minuten" => "5m".to_string(),
        "15 Minuten" => "15m".to_string(),
        "1 Stunde" => "1H".to_string(),
        "4 Stunden" => "4H".to_string(),
        "1 Tag" => "1D".to_string(),
        "" => "unknown".to_string(),
        other => other.to_string(),
    }
}

#[derive(Debug, Clone)]
struct Diagnostic {
    source: PathBuf,
    line: usize,
    message: String,
}

fn validate_logs(input: &Path) -> io::Result<Vec<Diagnostic>> {
    let files = collect_files(input)?;
    let mut diagnostics = Vec::new();
    for file in files {
        let content = fs::read_to_string(&file)?;
        for (idx, line) in content.lines().enumerate() {
            if !line.contains(REAL_EXIT_MARKER) {
                continue;
            }
            let message = csv_last_field(line);
            diagnostics.extend(validate_message(&message, &file, idx + 1));
        }
    }
    Ok(diagnostics)
}

fn validate_message(message: &str, source: &Path, line: usize) -> Vec<Diagnostic> {
    let mut diagnostics = Vec::new();
    if !message.contains(REAL_EXIT_MARKER) {
        diagnostics.push(Diagnostic {
            source: source.to_path_buf(),
            line,
            message: format!("missing marker `{REAL_EXIT_MARKER}`"),
        });
        return diagnostics;
    }

    let fields = parse_pipe_fields(message);
    for (key, kind) in REQUIRED_FIELDS {
        match fields.get(*key) {
            Some(value) => {
                if let Some(reason) = validate_field_value(value, *kind) {
                    diagnostics.push(Diagnostic {
                        source: source.to_path_buf(),
                        line,
                        message: format!("invalid `{key}`: {reason}"),
                    });
                }
            }
            None => diagnostics.push(Diagnostic {
                source: source.to_path_buf(),
                line,
                message: format!("missing required field `{key}`"),
            }),
        }
    }

    if let Some(entry_struct) = fields.get("entryStruct") {
        let nested = parse_entry_struct(entry_struct);
        for (key, kind) in ENTRY_STRUCT_FIELDS {
            match nested.get(*key) {
                Some(value) => {
                    if let Some(reason) = validate_field_value(value, *kind) {
                        diagnostics.push(Diagnostic {
                            source: source.to_path_buf(),
                            line,
                            message: format!("invalid `entryStruct.{key}`: {reason}"),
                        });
                    }
                }
                None => diagnostics.push(Diagnostic {
                    source: source.to_path_buf(),
                    line,
                    message: format!("missing required field `entryStruct.{key}`"),
                }),
            }
        }
    }

    diagnostics
}

fn collect_files(input: &Path) -> io::Result<Vec<PathBuf>> {
    if input.is_file() {
        return Ok(vec![input.to_path_buf()]);
    }

    let mut files = Vec::new();
    collect_files_recursive(input, &mut files)?;
    files.sort();
    Ok(files)
}

fn collect_files_recursive(dir: &Path, files: &mut Vec<PathBuf>) -> io::Result<()> {
    for entry in fs::read_dir(dir)? {
        let path = entry?.path();
        if path.is_dir() {
            collect_files_recursive(&path, files)?;
        } else if path
            .file_name()
            .and_then(|name| name.to_str())
            .is_some_and(|name| name.ends_with(".csv") && name.contains("pine-logs"))
        {
            files.push(path);
        }
    }
    Ok(())
}

fn csv_last_field(line: &str) -> String {
    let mut fields = Vec::new();
    let mut field = String::new();
    let mut in_quotes = false;
    let mut chars = line.chars().peekable();

    while let Some(ch) = chars.next() {
        match ch {
            '"' if in_quotes && chars.peek() == Some(&'"') => {
                field.push('"');
                chars.next();
            }
            '"' => in_quotes = !in_quotes,
            ',' if !in_quotes => {
                fields.push(field);
                field = String::new();
            }
            _ => field.push(ch),
        }
    }
    fields.push(field);
    fields.pop().unwrap_or_default()
}

fn parse_trade(message: &str, source: &Path) -> Option<Trade> {
    if !message.contains(REAL_EXIT_MARKER) {
        return None;
    }

    let fields = parse_pipe_fields(message);
    let entry_struct = fields
        .get("entryStruct")
        .map_or_else(BTreeMap::new, |v| parse_entry_struct(v));

    let chart_sec = parse_i64(fields.get("chartSec"));
    let tf = normalize_tf(&text_default(&fields, "tf", "unknown"), chart_sec);

    Some(Trade {
        source: source.display().to_string(),
        dir: text(&fields, "dir"),
        family: text(&fields, "family"),
        exit: text(&fields, "exit"),
        profile: text(&fields, "profile"),
        tf,
        chart_sec,
        execution_mode: text_default(&fields, "executionMode", "unknown"),
        bars_held: parse_f64(fields.get("barsHeld")),
        pnl: parse_f64(fields.get("pnl")),
        r: parse_f64(fields.get("R")),
        mfe: parse_f64(fields.get("MFE")),
        mae: parse_f64(fields.get("MAE")),
        capture_pct: parse_f64(fields.get("capturePct")),
        target_room_r: parse_f64(fields.get("targetRoomR")),
        target_room_atr: parse_f64(fields.get("targetRoomATR")),
        target_hit: parse_bool(fields.get("targetHit")).unwrap_or(false),
        bars_to_target: parse_f64(fields.get("barsToTarget")),
        fav_pivot_r: parse_f64(fields.get("favPivotR")),
        bars_to_fav_pivot: parse_f64(fields.get("barsToFavPivot")),
        adv_pivot_r: parse_f64(fields.get("advPivotR")),
        bars_to_adv_pivot: parse_f64(fields.get("barsToAdvPivot")),
        entry_score: parse_f64(fields.get("entryScore")),
        hh: parse_bool(entry_struct.get("hh")),
        hl: parse_bool(entry_struct.get("hl")),
        lh: parse_bool(entry_struct.get("lh")),
        ll: parse_bool(entry_struct.get("ll")),
        long_struct: parse_bool(entry_struct.get("longStruct")),
        short_struct: parse_bool(entry_struct.get("shortStruct")),
        structure_phase: text_default(&entry_struct, "structurePhase", "unknown"),
        playbook: text_default(&entry_struct, "playbook", "unknown"),
        wt_bull_div: parse_bool(entry_struct.get("wtBullDiv")),
        wt_bear_div: parse_bool(entry_struct.get("wtBearDiv")),
        high_confirm_bars: parse_f64(entry_struct.get("highConfirmBars")),
        low_confirm_bars: parse_f64(entry_struct.get("lowConfirmBars")),
        high_actual_bars: parse_f64(entry_struct.get("highActualBars")),
        low_actual_bars: parse_f64(entry_struct.get("lowActualBars")),
        range_pos: parse_f64(entry_struct.get("rangePos")),
    })
}

fn parse_raw_wt_events(message: &str, source: &Path) -> Vec<RawWtEvent> {
    if !message.contains(RAW_WT_MARKER) {
        return Vec::new();
    }

    let fields = parse_pipe_fields(message);
    let raw = parse_named_segment(message, RAW_WT_MARKER);
    let playbook = parse_named_segment(message, "PLAYBOOK:");
    let strong_bull = parse_bool(raw.get("strongBull")).unwrap_or(false);
    let strong_bear = parse_bool(raw.get("strongBear")).unwrap_or(false);
    let profile = text_default(&fields, "profile", "unknown");
    let playbook_active = text_default(&playbook, "active", "unknown");
    let structure_phase = text_default(&playbook, "structure", "unknown");

    let mut events = Vec::new();
    if strong_bull {
        events.push(RawWtEvent {
            source: source.display().to_string(),
            dir: "BULL".to_string(),
            profile: profile.clone(),
            playbook_active: playbook_active.clone(),
            structure_phase: structure_phase.clone(),
            pivot_confirm_bars: parse_f64(raw.get("lowConfirmBars")),
            pivot_actual_bars: parse_f64(raw.get("lowActualBars")),
            piv_len: parse_f64(raw.get("pivLen")),
        });
    }
    if strong_bear {
        events.push(RawWtEvent {
            source: source.display().to_string(),
            dir: "BEAR".to_string(),
            profile,
            playbook_active,
            structure_phase,
            pivot_confirm_bars: parse_f64(raw.get("highConfirmBars")),
            pivot_actual_bars: parse_f64(raw.get("highActualBars")),
            piv_len: parse_f64(raw.get("pivLen")),
        });
    }
    events
}

fn parse_pipe_fields(message: &str) -> BTreeMap<String, String> {
    let mut out = BTreeMap::new();
    for part in message.split('|').skip(1) {
        if let Some((key, value)) = part.trim().split_once('=') {
            out.insert(key.trim().to_string(), value.trim().to_string());
        }
    }
    out
}

fn parse_named_segment(message: &str, marker: &str) -> BTreeMap<String, String> {
    let Some((_, tail)) = message.split_once(marker) else {
        return BTreeMap::new();
    };
    let segment = tail.split('|').next().unwrap_or_default();
    let mut out = BTreeMap::new();
    for part in segment.split_whitespace() {
        if let Some((key, value)) = part.split_once('=') {
            out.insert(key.trim().to_string(), value.trim().to_string());
        }
    }
    out
}

fn parse_entry_struct(value: &str) -> BTreeMap<String, String> {
    let mut out = BTreeMap::new();
    for part in value.split(',') {
        if let Some((key, value)) = part.trim().split_once('=') {
            out.insert(key.trim().to_string(), value.trim().to_string());
        }
    }
    out
}

fn render_markdown_report(
    input: &Path,
    trades: &[Trade],
    strategy_runs: &[StrategyRun],
    raw_wt_events: &[RawWtEvent],
) -> String {
    let mut out = String::new();
    out.push_str("# Strategy Helper Report\n\n");
    out.push_str(&format!("- Input: `{}`\n", input.display()));
    out.push_str(&format!("- Trades: `{}`\n\n", trades.len()));

    if !strategy_runs.is_empty() {
        out.push_str("## Strategy Tester Exports\n\n");
        out.push_str(&render_strategy_runs_table(strategy_runs));
        out.push_str("\n## Strategy Tester Exits\n\n");
        out.push_str(&render_strategy_exits_table(strategy_runs));
        out.push('\n');
    }

    out.push_str("## Overall\n\n");
    out.push_str(&render_table(vec![(
        "all".to_string(),
        summarize(trades.iter()),
    )]));

    out.push_str("\n## By Timeframe / Profile / Family\n\n");
    out.push_str(&render_grouped_table(trades, |t| {
        format!("{} / {} / {}", t.tf, t.profile, t.family)
    }));

    out.push_str("\n## By Timeframe / Family / Exit\n\n");
    out.push_str(&render_grouped_table(trades, |t| {
        format!("{} / {} / {}", t.tf, t.family, t.exit)
    }));

    out.push_str("\n## By Timeframe / Family / Target\n\n");
    out.push_str(&render_grouped_table(trades, |t| {
        format!(
            "{} / {} / {}",
            t.tf,
            t.family,
            if t.target_hit {
                "target hit"
            } else {
                "target miss"
            }
        )
    }));

    out.push_str("\n## By Timeframe / Family / Structure\n\n");
    out.push_str(&render_grouped_table(trades, |t| {
        format!("{} / {} / {}", t.tf, t.family, structure_label(t))
    }));

    if trades.iter().any(|t| t.playbook != "unknown") {
        out.push_str("\n## By Timeframe / Playbook / Family\n\n");
        out.push_str(&render_grouped_table(trades, |t| {
            format!("{} / {} / {}", t.tf, t.playbook, t.family)
        }));
    }

    if trades
        .iter()
        .any(|t| t.wt_bull_div.is_some() || t.wt_bear_div.is_some())
    {
        out.push_str("\n## By Timeframe / Playbook / WT Divergence\n\n");
        out.push_str(&render_grouped_table(trades, |t| {
            format!("{} / {} / {}", t.tf, t.playbook, wt_divergence_label(t))
        }));
    }

    if !raw_wt_events.is_empty() {
        out.push_str("\n## Raw Strong WT Cross / Pivot Timing\n\n");
        out.push_str(&render_raw_wt_table(raw_wt_events));
    }

    out.push_str("\n## Error Classes\n\n");
    out.push_str(&render_grouped_table(trades, |t| {
        format!("{} / {} / {}", t.tf, t.family, error_class(t))
    }));

    out
}

fn render_strategy_runs_table(runs: &[StrategyRun]) -> String {
    let mut out = String::new();
    out.push_str("| Source | TF | Profile | Execution | Trades | Winners | Net | Gross Profit | Gross Loss | PF | WR | Avg | W/L | Sharpe | Commission | Max DD |\n");
    out.push_str("|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|\n");
    for run in runs {
        out.push_str(&format!(
            "| {} | {} | {} | {} | {} | {} | {} | {} | {} | {} | {} | {} | {} | {} | {} | {} |\n",
            escape_md(short_file_name(&run.source)),
            escape_md(&run.tf),
            escape_md(&run.profile),
            escape_md(&run.execution_mode),
            opt(run.trades),
            opt(run.winners),
            opt(run.net_profit),
            opt(run.gross_profit),
            opt(run.gross_loss),
            opt(run.profit_factor),
            opt(run.win_rate),
            opt(run.avg_trade),
            opt(run.win_loss_ratio),
            opt(run.sharpe),
            opt(run.commission),
            opt(run.max_drawdown),
        ));
    }
    out
}

fn render_strategy_exits_table(runs: &[StrategyRun]) -> String {
    let mut out = String::new();
    out.push_str("| Run | TF | Profile | Exit | Trades | Net |\n");
    out.push_str("|---|---|---|---|---:|---:|\n");
    for run in runs {
        for (exit, summary) in &run.exits {
            out.push_str(&format!(
                "| {} | {} | {} | {} | {} | {} |\n",
                escape_md(short_file_name(&run.source)),
                escape_md(&run.tf),
                escape_md(&run.profile),
                escape_md(exit),
                summary.n,
                f(summary.pnl),
            ));
        }
    }
    out
}

fn render_raw_wt_table(events: &[RawWtEvent]) -> String {
    let mut groups: BTreeMap<String, Vec<&RawWtEvent>> = BTreeMap::new();
    for event in events {
        let key = format!(
            "{} / {} / active={} / {}",
            event.profile, event.dir, event.playbook_active, event.structure_phase
        );
        groups.entry(key).or_default().push(event);
    }

    let mut rows: Vec<_> = groups.into_iter().collect();
    rows.sort_by(|a, b| b.1.len().cmp(&a.1.len()).then_with(|| a.0.cmp(&b.0)));

    let has_pivot_timing = events
        .iter()
        .any(|event| event.pivot_confirm_bars.is_some() || event.pivot_actual_bars.is_some());

    let mut out = String::new();
    if !has_pivot_timing {
        out.push_str("Current logs contain raw strong WT crosses, but not pivot-distance fields yet. Re-export after the Pine update to get coincidence rates.\n\n");
    }

    out.push_str("| Group | Crosses | Confirm <=0 | Confirm <=2 | Actual <=PivLen+2 | Avg Confirm Bars | Avg Actual Bars |\n");
    out.push_str("|---|---:|---:|---:|---:|---:|---:|\n");
    for (key, group) in rows {
        let n = group.len();
        let confirm_now = group
            .iter()
            .filter(|event| event.pivot_confirm_bars.is_some_and(|bars| bars <= 0.0))
            .count();
        let confirm_near = group
            .iter()
            .filter(|event| event.pivot_confirm_bars.is_some_and(|bars| bars <= 2.0))
            .count();
        let actual_near = group
            .iter()
            .filter(|event| {
                event
                    .pivot_actual_bars
                    .zip(event.piv_len)
                    .is_some_and(|(bars, piv_len)| bars <= piv_len + 2.0)
            })
            .count();
        let avg_confirm = avg_events(&group, |event| event.pivot_confirm_bars);
        let avg_actual = avg_events(&group, |event| event.pivot_actual_bars);
        out.push_str(&format!(
            "| {} | {} | {} | {} | {} | {} | {} |\n",
            escape_md(&key),
            n,
            if has_pivot_timing {
                pct_s(pct(confirm_now, n))
            } else {
                "na".to_string()
            },
            if has_pivot_timing {
                pct_s(pct(confirm_near, n))
            } else {
                "na".to_string()
            },
            if has_pivot_timing {
                pct_s(pct(actual_near, n))
            } else {
                "na".to_string()
            },
            opt(avg_confirm),
            opt(avg_actual),
        ));
    }
    out
}

fn render_grouped_table<F>(trades: &[Trade], key_fn: F) -> String
where
    F: Fn(&Trade) -> String,
{
    let mut groups: BTreeMap<String, Stats> = BTreeMap::new();
    for trade in trades {
        groups.entry(key_fn(trade)).or_default().add(trade);
    }
    render_table(groups.into_iter().collect())
}

fn render_table(rows: Vec<(String, Stats)>) -> String {
    let mut out = String::new();
    out.push_str("| Slice | Trades | Net | WR | avg R | MFE | MAE | Capture | Target Hit | Bars | Bars Target | Fav Pivot R | Adv Pivot R |\n");
    out.push_str("|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|\n");
    for (key, s) in rows {
        out.push_str(&format!(
            "| {} | {} | {} | {} | {} | {} | {} | {} | {} | {} | {} | {} | {} |\n",
            escape_md(&key),
            s.n,
            f(s.pnl_sum),
            pct_s(s.win_rate()),
            avg_s(s.r_sum, s.r_n),
            avg_s(s.mfe_sum, s.mfe_n),
            avg_s(s.mae_sum, s.mae_n),
            avg_s(s.capture_sum, s.capture_n),
            pct_s(s.target_rate()),
            avg_s(s.bars_sum, s.bars_n),
            avg_s(s.bars_to_target_sum, s.bars_to_target_n),
            avg_s(s.fav_pivot_r_sum, s.fav_pivot_r_n),
            avg_s(s.adv_pivot_r_sum, s.adv_pivot_r_n),
        ));
    }
    out
}

fn render_trades_csv(trades: &[Trade]) -> String {
    let mut out = String::new();
    out.push_str("source,tf,chart_sec,profile,execution_mode,dir,family,exit,pnl,R,MFE,MAE,capture_pct,target_room_r,target_room_atr,target_hit,bars_held,bars_to_target,fav_pivot_r,bars_to_fav_pivot,adv_pivot_r,bars_to_adv_pivot,entry_score,structure,structure_phase,playbook,wt_bull_div,wt_bear_div,high_confirm_bars,low_confirm_bars,high_actual_bars,low_actual_bars,hh,hl,lh,ll,long_struct,short_struct,range_pos\n");
    for t in trades {
        out.push_str(
            &[
                csv(&t.source),
                csv(&t.tf),
                opt_i(t.chart_sec),
                csv(&t.profile),
                csv(&t.execution_mode),
                csv(&t.dir),
                csv(&t.family),
                csv(&t.exit),
                opt(t.pnl),
                opt(t.r),
                opt(t.mfe),
                opt(t.mae),
                opt(t.capture_pct),
                opt(t.target_room_r),
                opt(t.target_room_atr),
                t.target_hit.to_string(),
                opt(t.bars_held),
                opt(t.bars_to_target),
                opt(t.fav_pivot_r),
                opt(t.bars_to_fav_pivot),
                opt(t.adv_pivot_r),
                opt(t.bars_to_adv_pivot),
                opt(t.entry_score),
                csv(&structure_label(t)),
                csv(&t.structure_phase),
                csv(&t.playbook),
                opt_b(t.wt_bull_div),
                opt_b(t.wt_bear_div),
                opt(t.high_confirm_bars),
                opt(t.low_confirm_bars),
                opt(t.high_actual_bars),
                opt(t.low_actual_bars),
                opt_b(t.hh),
                opt_b(t.hl),
                opt_b(t.lh),
                opt_b(t.ll),
                opt_b(t.long_struct),
                opt_b(t.short_struct),
                opt(t.range_pos),
            ]
            .join(","),
        );
        out.push('\n');
    }
    out
}

fn render_schema_markdown() -> String {
    let mut out = String::new();
    out.push_str("# WT3 REAL EXIT Log Format\n\n");
    out.push_str("Version: `1`\n\n");
    out.push_str("Canonical event marker:\n\n");
    out.push_str("```text\nWT3 REAL EXIT | key=value | key=value | ...\n```\n\n");
    out.push_str("Rules:\n\n");
    out.push_str("- Fields are separated by ` | `.\n");
    out.push_str("- Keys are case-sensitive and stable.\n");
    out.push_str("- Decimal separator is `.`.\n");
    out.push_str("- Missing optional numeric values must be logged as `NaN`.\n");
    out.push_str("- Booleans must be `true` or `false`.\n");
    out.push_str("- `entryStruct` is a comma-separated nested `key=value` list.\n");
    out.push_str("- New fields may be appended, but existing keys must not be renamed.\n\n");

    out.push_str("## Required Fields\n\n");
    out.push_str("| Field | Type |\n|---|---|\n");
    for (key, kind) in REQUIRED_FIELDS {
        out.push_str(&format!("| `{key}` | {} |\n", kind_name(*kind)));
    }

    out.push_str("\n## Required `entryStruct` Fields\n\n");
    out.push_str("| Field | Type |\n|---|---|\n");
    for (key, kind) in ENTRY_STRUCT_FIELDS {
        out.push_str(&format!("| `{key}` | {} |\n", kind_name(*kind)));
    }

    out.push_str("\n## Optional `entryStruct` Fields\n\n");
    out.push_str("| Field | Type | Purpose |\n|---|---|---|\n");
    out.push_str(
        "| `structurePhase` | text | Named HH/HL/LL/LH phase used by playbook routing. |\n",
    );
    out.push_str("| `playbook` | text | Active entry-side playbook for the trade direction. |\n");
    out.push_str(
        "| `wtBullDiv` | bool | Confirmed WT bullish divergence at the latest low-pivot pair. |\n",
    );
    out.push_str(
        "| `wtBearDiv` | bool | Confirmed WT bearish divergence at the latest high-pivot pair. |\n",
    );
    out.push_str("| `highConfirmBars` | optional number | Bars since the latest swing-high pivot was confirmed. |\n");
    out.push_str("| `lowConfirmBars` | optional number | Bars since the latest swing-low pivot was confirmed. |\n");
    out.push_str("| `highActualBars` | optional number | Bars since the actual latest swing-high pivot bar. |\n");
    out.push_str("| `lowActualBars` | optional number | Bars since the actual latest swing-low pivot bar. |\n");

    out
}

fn summarize<'a, I>(trades: I) -> Stats
where
    I: Iterator<Item = &'a Trade>,
{
    let mut stats = Stats::default();
    for trade in trades {
        stats.add(trade);
    }
    stats
}

fn structure_label(t: &Trade) -> String {
    match (t.hh, t.hl, t.lh, t.ll) {
        (Some(true), Some(true), _, _) => "HH/HL".to_string(),
        (_, _, Some(true), Some(true)) => "LL/LH".to_string(),
        (_, Some(true), Some(true), _) => "HL/LH".to_string(),
        (Some(true), _, _, Some(true)) => "HH/LL".to_string(),
        _ => "other".to_string(),
    }
}

fn wt_divergence_label(t: &Trade) -> &'static str {
    match (t.wt_bull_div, t.wt_bear_div) {
        (Some(true), Some(true)) => "bull+bear div",
        (Some(true), _) => "bull div",
        (_, Some(true)) => "bear div",
        (Some(false), Some(false)) => "no div",
        (Some(false), None) => "no bull div",
        (None, Some(false)) => "no bear div",
        _ => "unknown",
    }
}

fn normalize_tf(raw: &str, chart_sec: Option<i64>) -> String {
    match chart_sec {
        Some(300) => "5m".to_string(),
        Some(900) => "15m".to_string(),
        Some(3600) => "1H".to_string(),
        Some(14400) => "4H".to_string(),
        Some(86400) => "1D".to_string(),
        _ if raw.is_empty() => "unknown".to_string(),
        _ => raw.to_string(),
    }
}

fn error_class(t: &Trade) -> &'static str {
    let mfe = t.mfe.unwrap_or(f64::NAN);
    let mae = t.mae.unwrap_or(f64::NAN);
    let capture = t.capture_pct.unwrap_or(f64::NAN);
    let target_r = t.target_room_r.unwrap_or(f64::NAN);

    if mfe >= 1.0 && capture < 35.0 {
        "good idea / poor capture"
    } else if mfe < 0.5 && mae >= 0.8 {
        "bad idea / no follow-through"
    } else if !t.target_hit && target_r > 1.5 && mfe < target_r * 0.6 {
        "target too far"
    } else if t.bars_to_adv_pivot.is_some_and(|bars| bars <= 3.0) && mae >= 0.8 {
        "early adverse pivot"
    } else {
        "mixed/ok"
    }
}

fn add_opt(value: Option<f64>, sum: &mut f64, n: &mut usize) {
    if let Some(value) = value {
        if value.is_finite() {
            *sum += value;
            *n += 1;
        }
    }
}

fn avg_events<T>(items: &[&T], value: impl Fn(&T) -> Option<f64>) -> Option<f64> {
    let mut sum = 0.0;
    let mut n = 0;
    for item in items {
        if let Some(v) = value(*item) {
            if v.is_finite() {
                sum += v;
                n += 1;
            }
        }
    }
    if n == 0 { None } else { Some(sum / n as f64) }
}

fn parse_f64(value: Option<&String>) -> Option<f64> {
    let value = value?.trim();
    if value.is_empty() || value.eq_ignore_ascii_case("nan") || value.eq_ignore_ascii_case("na") {
        return None;
    }
    value.parse::<f64>().ok().filter(|v| v.is_finite())
}

fn parse_i64(value: Option<&String>) -> Option<i64> {
    value?.trim().parse::<i64>().ok()
}

fn parse_bool(value: Option<&String>) -> Option<bool> {
    match value?.trim() {
        "true" => Some(true),
        "false" => Some(false),
        _ => None,
    }
}

fn validate_field_value(value: &str, kind: FieldKind) -> Option<String> {
    match kind {
        FieldKind::Text => {
            if value.trim().is_empty() {
                Some("empty text".to_string())
            } else {
                None
            }
        }
        FieldKind::Number => value
            .trim()
            .parse::<f64>()
            .ok()
            .filter(|v| v.is_finite())
            .map(|_| ())
            .ok_or_else(|| "expected finite number".to_string())
            .err(),
        FieldKind::OptionalNumber => {
            let value = value.trim();
            if value.eq_ignore_ascii_case("nan") || value.eq_ignore_ascii_case("na") {
                None
            } else {
                value
                    .parse::<f64>()
                    .ok()
                    .filter(|v| v.is_finite())
                    .map(|_| ())
                    .ok_or_else(|| "expected finite number or NaN".to_string())
                    .err()
            }
        }
        FieldKind::Integer => value
            .trim()
            .parse::<i64>()
            .map(|_| ())
            .map_err(|_| "expected integer".to_string())
            .err(),
        FieldKind::Bool => match value.trim() {
            "true" | "false" => None,
            _ => Some("expected true or false".to_string()),
        },
        FieldKind::EntryStruct => {
            if value.trim().is_empty() {
                Some("empty entryStruct".to_string())
            } else {
                None
            }
        }
        FieldKind::Enum(allowed) => {
            if allowed.iter().any(|candidate| candidate == &value.trim()) {
                None
            } else {
                Some(format!("expected one of {}", allowed.join(", ")))
            }
        }
    }
}

fn kind_name(kind: FieldKind) -> String {
    match kind {
        FieldKind::Text => "`text`".to_string(),
        FieldKind::Number => "`number`".to_string(),
        FieldKind::OptionalNumber => "`number | NaN`".to_string(),
        FieldKind::Integer => "`integer`".to_string(),
        FieldKind::Bool => "`bool`".to_string(),
        FieldKind::EntryStruct => "`entryStruct`".to_string(),
        FieldKind::Enum(values) => format!("enum `{}`", values.join(" | ")),
    }
}

fn text(fields: &BTreeMap<String, String>, key: &str) -> String {
    text_default(fields, key, "")
}

fn text_default(fields: &BTreeMap<String, String>, key: &str, default: &str) -> String {
    fields
        .get(key)
        .cloned()
        .unwrap_or_else(|| default.to_string())
}

fn pct(num: usize, den: usize) -> f64 {
    if den == 0 {
        f64::NAN
    } else {
        num as f64 / den as f64 * 100.0
    }
}

fn avg_s(sum: f64, n: usize) -> String {
    if n == 0 {
        "na".to_string()
    } else {
        f(sum / n as f64)
    }
}

fn pct_s(value: f64) -> String {
    if value.is_finite() {
        format!("{value:.1}%")
    } else {
        "na".to_string()
    }
}

fn f(value: f64) -> String {
    if !value.is_finite() {
        "na".to_string()
    } else if value.abs() >= 100.0 {
        format!("{value:.0}")
    } else {
        format!("{value:.2}")
    }
}

fn opt(value: Option<f64>) -> String {
    value.map(f).unwrap_or_default()
}

fn opt_i(value: Option<i64>) -> String {
    value.map(|v| v.to_string()).unwrap_or_default()
}

fn opt_b(value: Option<bool>) -> String {
    value.map(|v| v.to_string()).unwrap_or_default()
}

fn escape_md(value: &str) -> String {
    value.replace('|', "\\|")
}

fn csv(value: &str) -> String {
    if value.contains(',') || value.contains('"') || value.contains('\n') {
        format!("\"{}\"", value.replace('"', "\"\""))
    } else {
        value.to_string()
    }
}

fn short_file_name(path: &str) -> &str {
    Path::new(path)
        .file_name()
        .and_then(|name| name.to_str())
        .unwrap_or(path)
}

fn write_parented(path: &Path, bytes: &[u8]) -> io::Result<()> {
    if let Some(parent) = path.parent() {
        fs::create_dir_all(parent)?;
    }
    fs::write(path, bytes)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn parses_quoted_csv_last_field() {
        let line = "2026-01-01,\"WT3 REAL EXIT | dir=LONG | family=er | pnl=1.23\"";
        assert_eq!(
            csv_last_field(line),
            "WT3 REAL EXIT | dir=LONG | family=er | pnl=1.23"
        );
    }

    #[test]
    fn parses_real_exit_trade() {
        let msg = "WT3 REAL EXIT | dir=SHORT | family=pb | exit=Short Exit | profile=Balanced | tf=60 | chartSec=3600 | executionMode=Bracket SL/TP | pnl=-12.5 | R=-1 | MFE=0.4 | MAE=1.1 | capturePct=-250 | targetHit=false | entryStruct=hh=false,hl=true,lh=true,ll=false,longStruct=false,shortStruct=true,structurePhase=compression,playbook=pullback_short,wtBullDiv=false,wtBearDiv=true,rangePos=0.57";
        let trade = parse_trade(msg, Path::new("pine-logs.csv")).expect("trade");

        assert_eq!(trade.dir, "SHORT");
        assert_eq!(trade.family, "pb");
        assert_eq!(trade.tf, "1H");
        assert_eq!(trade.chart_sec, Some(3600));
        assert_eq!(trade.r, Some(-1.0));
        assert_eq!(trade.hl, Some(true));
        assert_eq!(trade.lh, Some(true));
        assert_eq!(trade.structure_phase, "compression");
        assert_eq!(trade.playbook, "pullback_short");
        assert_eq!(trade.wt_bull_div, Some(false));
        assert_eq!(trade.wt_bear_div, Some(true));
        assert_eq!(structure_label(&trade), "HL/LH");
        assert_eq!(error_class(&trade), "bad idea / no follow-through");
    }

    #[test]
    fn validates_required_log_contract() {
        let msg = "WT3 REAL EXIT | dir=SHORT | family=pb | exit=Short Exit | trade=1 | barsHeld=5 | pnl=-12.5 | R=-1 | entry=4.1 | exitPx=4.2 | profile=Balanced | tf=60 | chartSec=3600 | executionMode=Bracket SL/TP | MFE=0.4 | MAE=1.1 | capturePct=-250 | targetPx=4.0 | targetRoomR=1.2 | targetRoomATR=2.4 | targetHit=false | barsToTarget=NaN | favPivotPx=NaN | favPivotR=NaN | barsToFavPivot=NaN | advPivotPx=4.3 | advPivotR=0.5 | barsToAdvPivot=3 | entryScore=4.5 | entryStruct=hh=false,hl=true,lh=true,ll=false,longStruct=false,shortStruct=true,rangePos=0.57,target=4.0,stop=4.3";
        let diagnostics = validate_message(msg, Path::new("pine-logs.csv"), 1);

        assert!(diagnostics.is_empty());
    }
}
