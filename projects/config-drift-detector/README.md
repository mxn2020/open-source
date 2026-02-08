# Config Drift Detector

A CLI tool that detects configuration drift between two sources — YAML, JSON,
or TOML files. Built for developers and SREs who need to quickly spot
differences between baseline and actual configurations.

## Why This Exists

Configuration drift is a common source of outages and unexpected behavior.
Manually comparing configuration files is tedious and error-prone, especially
when files are deeply nested. Config Drift Detector automates this process with
clear, actionable output suitable for both human review and CI pipelines.

## Features

- **Multi-format support** — YAML, JSON, and TOML with automatic format
  detection based on file extension.
- **Deep recursive comparison** — Detects added, removed, and changed values at
  any nesting depth.
- **Tag filtering** — Compare only specific top-level sections (e.g., just the
  `database` block).
- **Dual output modes** — Rich-formatted tables for humans, JSON for machines.
- **CI-friendly exit codes** — `0` = no drift, `1` = drift found, `2` = error.

## Installation

```bash
pip install -e ".[dev]"
```

Or install from the project directory:

```bash
cd projects/config-drift-detector
pip install .
```

## Quickstart

```bash
# Compare two YAML files
drift check --a examples/config_a.yaml --b examples/config_b.yaml

# Output as JSON
drift check --a examples/config_a.yaml --b examples/config_b.yaml --json

# Compare only specific sections
drift check --a examples/config_a.yaml --b examples/config_b.yaml --tags database,cache
```

## CLI Reference

### `drift check`

Compare two configuration files and report drift.

| Option    | Description                                    |
| --------- | ---------------------------------------------- |
| `--a`     | Path to the baseline configuration file.       |
| `--b`     | Path to the target configuration file.         |
| `--json`  | Output results as JSON instead of a table.     |
| `--tags`  | Comma-separated top-level keys to compare.     |

### `drift --version`

Print the version and exit.

### Exit Codes

| Code | Meaning         |
| ---- | --------------- |
| `0`  | No drift found  |
| `1`  | Drift detected  |
| `2`  | Error occurred  |

## Architecture Overview

```
cli.py          Typer-based CLI entry point
  ├── parsers.py      Format detection + file parsing
  ├── comparator.py   Recursive dict comparison → DriftItem list
  └── reporter.py     Rich table / JSON formatting
```

1. **Parsers** read a file path, detect the format from the extension, and
   return a Python `dict`.
2. **Comparator** walks both dicts recursively, producing a flat list of
   `DriftItem` dataclass instances with dot-notation paths.
3. **Reporter** formats the drift list for output — either a Rich table for
   terminal use or JSON for piping to other tools.
4. **CLI** wires everything together, handles errors, and sets the exit code.

## Limitations

- Only supports flat-file configuration sources (no remote APIs or databases).
- List/array comparison is by value equality, not element-wise diff.
- TOML parsing uses Python 3.11+ `tomllib` (stdlib); Python < 3.11 is not
  supported.

## Roadmap

- [ ] Environment variable overlay support
- [ ] Ignore-path patterns (e.g., `--ignore "metadata.*"`)
- [ ] Side-by-side diff view
- [ ] TOML and INI output formats
- [ ] GitHub Actions integration

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines. In short: fork, branch,
test, and open a pull request.

## License

[MIT](LICENSE)
