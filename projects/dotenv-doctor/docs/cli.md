# CLI Reference

dotenv-doctor provides two commands: `check` and `compare`.

## `dotenv-doctor check`

Validate a `.env` file, optionally against a template.

```
dotenv-doctor check <ENVFILE> [OPTIONS]
```

### Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `ENVFILE` | Yes | Path to the `.env` file to validate |

### Options

| Option | Short | Description |
|--------|-------|-------------|
| `--template <FILE>` | `-t` | Template file to compare against |
| `--json` | `-j` | Output results as JSON instead of a table |

### Examples

```bash
# Basic validation
dotenv-doctor check .env

# Validate against a template
dotenv-doctor check .env --template .env.example

# JSON output for CI
dotenv-doctor check .env --json
```

## `dotenv-doctor compare`

Compare two `.env` files and show differences in keys and values.

```
dotenv-doctor compare <FILE1> <FILE2> [OPTIONS]
```

### Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `FILE1` | Yes | First `.env` file |
| `FILE2` | Yes | Second `.env` file |

### Options

| Option | Short | Description |
|--------|-------|-------------|
| `--json` | `-j` | Output results as JSON instead of a table |

### Examples

```bash
# Compare staging and production
dotenv-doctor compare .env.staging .env.production

# JSON output
dotenv-doctor compare .env.local .env.production --json
```

## Exit Codes

| Code | Meaning |
|------|---------|
| `0` | No issues found (check) or files are identical (compare) |
| `1` | Issues with errors found (check) or differences found (compare) |
| `2` | Runtime error (file not found, invalid arguments) |
