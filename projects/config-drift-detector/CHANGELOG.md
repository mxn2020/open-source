# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2024-01-01

### Added

- Initial release.
- YAML, JSON, and TOML configuration parsing via auto-detection.
- Recursive deep comparison of nested configuration structures.
- Tag-based filtering to compare only specific top-level keys.
- Human-readable Rich table output and machine-readable JSON output.
- CLI entry point (`drift check`) with exit codes for CI integration.
