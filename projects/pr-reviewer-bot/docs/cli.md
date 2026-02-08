# CLI Reference

Complete reference for the pr-reviewer-bot command-line interface.

## Usage

```
pr-reviewer review [OPTIONS] [DIFF_FILE]
```

## Arguments

| Argument    | Description                                               |
|-------------|-----------------------------------------------------------|
| `DIFF_FILE` | Path to a unified diff file. Use `-` or omit to read from stdin. |

## Options

| Option              | Type   | Default | Description                                      |
|---------------------|--------|---------|--------------------------------------------------|
| `--json`            | flag   | off     | Output results as JSON instead of a Rich table.  |
| `--severity`        | string | `info`  | Minimum severity to report: `info`, `warning`, or `error`. |
| `--help`            | flag   |         | Show help message and exit.                      |

## Exit Codes

| Code | Meaning          |
|------|------------------|
| 0    | No issues found  |
| 1    | Issues found     |
| 2    | Input error      |

## Examples

### Review a diff file

```bash
pr-reviewer review changes.diff
```

### Review from stdin

```bash
git diff | pr-reviewer review -
git diff | pr-reviewer review
```

### JSON output for CI

```bash
pr-reviewer review changes.diff --json
```

### Filter by severity

```bash
pr-reviewer review changes.diff --severity warning
pr-reviewer review changes.diff --severity error --json
```

### Use in CI pipeline

```bash
git diff origin/main...HEAD > /tmp/pr.diff
pr-reviewer review /tmp/pr.diff --json --severity warning
echo "Exit code: $?"
```
