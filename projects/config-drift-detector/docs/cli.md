# CLI Reference

## Overview

Config Drift Detector provides a single command, `drift`, with subcommands for
detecting configuration differences.

## Commands

### `drift check`

Compare two configuration files and report any drift.

```bash
drift check --a <baseline> --b <target> [--json] [--tags <keys>]
```

#### Options

| Option          | Type   | Required | Description                                          |
| --------------- | ------ | -------- | ---------------------------------------------------- |
| `--a`           | PATH   | Yes      | Path to the baseline (source) configuration file.    |
| `--b`           | PATH   | Yes      | Path to the target (actual) configuration file.      |
| `--json`        | FLAG   | No       | Output results as JSON instead of a Rich table.      |
| `--tags`        | STRING | No       | Comma-separated list of top-level keys to compare.   |

#### Exit Codes

| Code | Meaning                               |
| ---- | ------------------------------------- |
| `0`  | No configuration drift detected.      |
| `1`  | Configuration drift was found.        |
| `2`  | An error occurred (file not found, unsupported format, etc.). |

#### Examples

```bash
# Basic comparison
drift check --a config_a.yaml --b config_b.yaml

# JSON output for piping to jq
drift check --a config_a.json --b config_b.json --json | jq '.[] | .path'

# Compare only the database and cache sections
drift check --a config_a.yaml --b config_b.yaml --tags database,cache
```

### `drift --version`

Print the tool version and exit.

```bash
drift --version
```

### `drift --help`

Show the help message.

```bash
drift --help
drift check --help
```
