# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2024-01-15

### Added

- Initial release of error-log-summarizer.
- Multi-format log parser supporting Generic, Apache/Nginx, Syslog, and JSON Lines formats.
- Automatic format detection per line.
- Error categorization into ConnectionError, TimeoutError, FileNotFound, PermissionError, MemoryError, SyntaxError, and Generic categories.
- Frequency-based top error analysis with message normalization.
- `summarize` command with `--json` and `--top` options.
- `categorize` command with `--json` option.
- Rich terminal output with colored tables and panels.
- JSON output mode for machine-readable results.
- Exit codes: 0 (success), 1 (errors found), 2 (parse error).
- Example log files for testing and demonstration.
- Full test suite with pytest.
