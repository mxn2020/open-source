# Changelog

All notable changes to dotenv-doctor will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-01-01

### Added

- Initial release.
- `check` command to validate `.env` files.
- `check --template` to compare against a template file.
- `compare` command to diff two `.env` files.
- Validation rules: duplicate keys, empty values, invalid key names, template comparison.
- Rich terminal output with colored tables.
- JSON output mode for CI integration.
