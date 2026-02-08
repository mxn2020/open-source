# Design

## Architecture Overview

Error Log Summarizer follows a pipeline architecture:

```
Log File → Parser → Categorizer → Reporter → Output
```

### Parser (`parser.py`)

The parser reads a log file line by line and attempts to match each line against known log formats in a priority order:

1. **JSON Lines** — checked first if the line starts with `{`.
2. **Generic format** — `<timestamp> <LEVEL> <message>` with ISO-style timestamps.
3. **Apache/Nginx** — `[<timestamp>] [<level>] <message>` bracket-delimited format.
4. **Syslog** — `<timestamp> <hostname> <service>: <message>` with keyword-based level inference.

Lines that do not match any format are silently skipped, making the parser tolerant of mixed-format files and non-log content interleaved with log entries.

The parser produces a list of `LogEntry` dataclass instances with normalized level strings (`DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`).

### Categorizer (`categorizer.py`)

The categorizer groups `ERROR` and `CRITICAL` entries into categories using keyword matching:

| Category        | Keywords                                    |
|-----------------|---------------------------------------------|
| ConnectionError | connect, connection, refused, reset         |
| TimeoutError    | timeout, timed out                          |
| FileNotFound    | file not found, no such file, enoent        |
| PermissionError | permission, denied, forbidden               |
| MemoryError     | memory, out of memory, oom, heap            |
| SyntaxError     | syntax, parse error, unexpected token       |
| Generic         | Anything that does not match above patterns |

The summarizer also performs frequency analysis by normalizing error messages (replacing numbers with `<N>` placeholders) to group similar messages.

### Reporter (`reporter.py`)

Two output modes:

- **Text**: Uses Rich library tables and panels for colored, formatted terminal output.
- **JSON**: Produces a structured JSON document for piping into other tools.

### CLI (`cli.py`)

Built with Typer, the CLI exposes two commands:

- `summarize` — shows an aggregated summary of the log file.
- `categorize` — shows errors grouped by category.

Both commands support `--json` for machine-readable output.

## Data Flow

```
parse_log_file(path)
    → list[LogEntry]
        → categorize_errors(entries) → dict[str, list[LogEntry]]
        → summarize(entries) → Summary
            → report_text(summary) / report_json(summary)
```

## Exit Codes

- `0`: Log file processed successfully, no errors found.
- `1`: Log file processed, errors were present.
- `2`: Could not read or parse the log file (file not found, permission denied).
