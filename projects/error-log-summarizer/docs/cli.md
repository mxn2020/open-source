# CLI Reference

## Global Options

Error Log Summarizer uses [Typer](https://typer.tiangolo.com/) and supports `--help` on all commands.

```bash
error-log-summarizer --help
```

## Commands

### `summarize`

Parse a log file and display an aggregated summary.

```
Usage: error-log-summarizer summarize [OPTIONS] LOGFILE
```

**Arguments:**

| Argument  | Description                        | Required |
|-----------|------------------------------------|----------|
| `LOGFILE` | Path to the log file to analyze    | Yes      |

**Options:**

| Option         | Description                          | Default |
|----------------|--------------------------------------|---------|
| `--json`       | Output as JSON instead of Rich text  | Off     |
| `--top`, `-n`  | Number of top error messages to show | 10      |

**Examples:**

```bash
# Rich terminal output
error-log-summarizer summarize /var/log/app.log

# JSON output, top 5 errors
error-log-summarizer summarize /var/log/app.log --json --top 5
```

**Output fields (JSON):**

```json
{
  "total_entries": 100,
  "error_count": 15,
  "warning_count": 8,
  "info_count": 77,
  "categories": {
    "ConnectionError": 5,
    "TimeoutError": 3,
    "Generic": 7
  },
  "top_errors": [
    {"message": "Connection refused to cache server at <N>", "count": 5},
    {"message": "Request timed out after <N>s", "count": 3}
  ]
}
```

### `categorize`

Parse a log file and display errors grouped by category.

```
Usage: error-log-summarizer categorize [OPTIONS] LOGFILE
```

**Arguments:**

| Argument  | Description                        | Required |
|-----------|------------------------------------|----------|
| `LOGFILE` | Path to the log file to analyze    | Yes      |

**Options:**

| Option   | Description                          | Default |
|----------|--------------------------------------|---------|
| `--json` | Output as JSON instead of Rich text  | Off     |

**Examples:**

```bash
# Rich terminal output
error-log-summarizer categorize /var/log/apache2/error.log

# JSON output
error-log-summarizer categorize /var/log/apache2/error.log --json
```

**Output fields (JSON):**

```json
{
  "ConnectionError": [
    {
      "timestamp": "2024-01-15 10:30:00",
      "level": "ERROR",
      "message": "Connection refused to database",
      "source": ""
    }
  ],
  "FileNotFound": [...]
}
```

## Exit Codes

| Code | Meaning                                    |
|------|--------------------------------------------|
| 0    | Log processed successfully, no errors found |
| 1    | Log processed, errors were present          |
| 2    | File not found or permission denied          |

## Supported Log Formats

The parser auto-detects the following formats on a per-line basis:

### Generic

```
2024-01-15 10:30:00 ERROR Something failed
2024-01-15T10:30:00 WARNING Disk space low
```

Levels: `DEBUG`, `INFO`, `WARNING`, `WARN`, `ERROR`, `CRITICAL`, `FATAL` (case-insensitive).

### Apache/Nginx Error Log

```
[Wed Jan 15 10:30:00 2024] [error] client denied by server
```

### Syslog

```
Jan 15 10:30:00 myhost sshd[1234]: Connection refused from 1.2.3.4
```

Level is inferred from keywords in the message text.

### JSON Lines

```json
{"timestamp": "2024-01-15T10:30:00", "level": "error", "message": "db down"}
```

Requires `level` and `message` fields. `timestamp` and `source` are optional.
