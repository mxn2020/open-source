# dotenv-doctor

A CLI tool that validates and diagnoses `.env` files. Catch configuration mistakes before they cause runtime errors.

## Why dotenv-doctor?

Environment variables are a critical part of application configuration, but `.env` files are fragile:

- Typos in key names go unnoticed until runtime.
- Duplicate keys silently override earlier values.
- Missing required variables cause cryptic startup failures.
- There is no standard way to validate `.env` files against a template.

**dotenv-doctor** catches these problems early by linting your `.env` files and comparing them against templates.

## Features

- **Validate** `.env` files for common issues (duplicates, empty values, invalid key names).
- **Compare** against a template (`.env.example`) to detect missing or extra variables.
- **Compare** two `.env` files side-by-side to see differences.
- **Rich terminal output** with colored tables, or **JSON** for CI pipelines.
- **Zero configuration** — works out of the box with sensible defaults.

## Installation

```bash
pip install dotenv-doctor
```

Or install from source:

```bash
git clone <repo-url>
cd projects/dotenv-doctor
pip install -e ".[dev]"
```

## Quickstart

### Validate a `.env` file

```bash
dotenv-doctor check .env
```

### Validate against a template

```bash
dotenv-doctor check .env --template .env.example
```

### Compare two files

```bash
dotenv-doctor compare .env.staging .env.production
```

### JSON output (for CI)

```bash
dotenv-doctor check .env --json
```

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | No issues (or only warnings/info) |
| 1 | Errors found (e.g., missing required keys) |
| 2 | Runtime error (file not found, etc.) |

## Validation Rules

| Rule | Severity | Description |
|------|----------|-------------|
| Duplicate keys | Warning | Same key defined more than once |
| Empty values | Warning | Key exists but has no value |
| Invalid key name | Warning | Key does not match `[A-Z_][A-Z0-9_]*` |
| Missing from template | Error | Key required by template is absent |
| Not in template | Info | Key exists in `.env` but not in template |

## Architecture

```
src/dotenv_doctor/
├── __init__.py       # Package version
├── cli.py            # Typer CLI commands (check, compare)
├── parser.py         # .env file parser → EnvEntry dataclass
├── validator.py      # Validation rules → Issue dataclass
└── reporter.py       # Output formatting (Rich table, JSON)
```

The design follows a pipeline: **parse → validate → report**. Each stage is independent and testable.

## Limitations

- **Multiline values** are not supported. Each variable must be on a single line.
- **Variable interpolation** (e.g., `${OTHER_VAR}`) is not expanded.
- **Encoding**: only UTF-8 files are supported.

## Roadmap

- [ ] Multiline value support
- [ ] Variable interpolation detection
- [ ] Custom validation rules via config file
- [ ] Pre-commit hook integration
- [ ] Watch mode for continuous validation

## License

MIT — see [LICENSE](LICENSE) for details.
