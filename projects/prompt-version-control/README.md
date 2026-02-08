# prompt-version-control

A CLI tool for version controlling LLM prompts. Track changes, compare versions, tag releases,
and manage your prompt library from the terminal.

## Features

- **Version tracking**: Automatically version prompts with incrementing version numbers.
- **Diff support**: Compare any two versions of a prompt with unified diff output.
- **Tagging**: Mark important versions with human-readable tags (e.g., "production", "stable").
- **Metadata**: Attach key-value metadata to each version (model, temperature, etc.).
- **JSON output**: All commands support `--json` for scripting and CI/CD integration.
- **SQLite storage**: Zero-configuration local storage with ACID guarantees.
- **Rich formatting**: Beautiful terminal output powered by Rich.

## Installation

```bash
cd projects/prompt-version-control
pip install -e ".[dev]"
```

## Quick Start

Save a prompt:

```bash
pv save greeting --content "You are a friendly assistant. Greet the user warmly."
```

Save with metadata:

```bash
pv save greeting --content "Be helpful and concise." --meta model=gpt-4 --meta temperature=0.7
```

Save from a file:

```bash
pv save summarize --file examples/prompts/summarize.yaml
```

Get the latest version:

```bash
pv get greeting
```

Get a specific version:

```bash
pv get greeting --version 1.0
```

List all prompts:

```bash
pv list
```

List versions of a prompt:

```bash
pv list --name greeting
```

Tag a version:

```bash
pv tag greeting 1.0 production
```

Get a tagged version:

```bash
pv get greeting --tag production
```

Compare two versions:

```bash
pv diff greeting 1.0 2.0
```

Delete a prompt:

```bash
pv delete greeting
```

## JSON Output

All commands support `--json` for machine-readable output:

```bash
pv save greeting --content "Hello!" --json
pv get greeting --json
pv list --json
```

## Exit Codes

| Code | Meaning     |
|------|-------------|
| 0    | Success     |
| 1    | Not found   |
| 2    | Error       |

## Development

Install development dependencies:

```bash
pip install -e ".[dev]"
```

Run tests:

```bash
pytest
```

Run linting:

```bash
ruff check src/ tests/
black --check src/ tests/
```

See [docs/development.md](docs/development.md) for the full development guide.

## Documentation

- [CLI Reference](docs/cli.md) — Full command reference.
- [Design Document](docs/design.md) — Architecture and design decisions.
- [Development Guide](docs/development.md) — Setup and contribution workflow.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
