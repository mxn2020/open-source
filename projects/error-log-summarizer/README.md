# Error Log Summarizer

A command-line tool that parses, categorizes, and summarizes error logs from multiple formats.

## Features

- **Multi-format parsing** — automatically detects and parses Syslog, Apache/Nginx, generic timestamp-level, and JSON Lines log formats.
- **Error categorization** — groups errors into categories like ConnectionError, TimeoutError, FileNotFound, PermissionError, MemoryError, and SyntaxError.
- **Frequency analysis** — identifies the most common error messages with normalized pattern matching.
- **Rich terminal output** — colored tables and panels using Rich.
- **JSON output** — machine-readable output for integration with other tools.
- **Exit codes** — `0` for clean logs, `1` when errors are found, `2` for parse/file errors.

## Installation

```bash
cd projects/error-log-summarizer
pip install -e ".[dev]"
```

## Quick Start

Summarize a log file:

```bash
error-log-summarizer summarize examples/sample.log
```

Get JSON output:

```bash
error-log-summarizer summarize examples/sample.log --json
```

Show only the top 5 errors:

```bash
error-log-summarizer summarize examples/sample.log --top 5
```

Categorize errors by type:

```bash
error-log-summarizer categorize examples/apache_errors.log
```

## Supported Log Formats

### Generic Format

```
2024-01-15 10:30:00 ERROR Something failed
2024-01-15T10:30:00 WARNING Disk space low
```

### Apache/Nginx Error Format

```
[Wed Jan 15 10:30:00 2024] [error] client denied by server
```

### Syslog Format

```
Jan 15 10:30:00 myhost sshd[1234]: Connection refused from 1.2.3.4
```

### JSON Lines Format

```json
{"timestamp": "2024-01-15T10:30:00", "level": "error", "message": "db connection lost"}
```

## Commands

### `summarize`

Parse a log file and display an aggregated summary with entry counts, error categories, and the most frequent error messages.

```
Usage: error-log-summarizer summarize [OPTIONS] LOGFILE

Arguments:
  LOGFILE  Path to the log file to analyze  [required]

Options:
  --json           Output as JSON
  --top, -n  INT   Number of top errors to show  [default: 10]
```

### `categorize`

Parse a log file and display errors grouped by category.

```
Usage: error-log-summarizer categorize [OPTIONS] LOGFILE

Arguments:
  LOGFILE  Path to the log file to analyze  [required]

Options:
  --json   Output as JSON
```

## Exit Codes

| Code | Meaning              |
|------|----------------------|
| 0    | Success, no errors   |
| 1    | Errors found in logs |
| 2    | Parse or file error  |

## Development

Install in development mode:

```bash
pip install -e ".[dev]"
```

Run tests:

```bash
pytest
```

Run tests with coverage:

```bash
pytest --cov=error_log_summarizer
```

Lint:

```bash
ruff check src/ tests/
```

Format:

```bash
black src/ tests/
```

## License

MIT License. See [LICENSE](LICENSE) for details.
