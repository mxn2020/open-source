# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-01-01

### Added

- Initial release of prompt-version-control.
- SQLite-backed storage for prompt versions.
- CLI commands: `save`, `get`, `list`, `tag`, `diff`, `delete`.
- Auto-incrementing version numbers for prompts.
- Tagging support for marking important versions (e.g., "production", "stable").
- Unified diff output for comparing prompt versions.
- JSON output mode for machine-readable output.
- Rich-formatted terminal output.
- Metadata support for prompts (model, temperature, etc.).
