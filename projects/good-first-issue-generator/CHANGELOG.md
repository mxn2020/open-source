# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-01-01

### Added

- Initial release of the Good First Issue Generator
- Scanner module for detecting TODO/FIXME/HACK/XXX comments
- Scanner module for detecting missing test files
- Scanner module for detecting missing docstrings in Python files
- Scanner module for detecting missing return type hints in Python files
- Generator module for converting opportunities into issue templates
- Reporter module with Rich text, JSON, and Markdown output formats
- CLI with `scan` and `stats` commands
- Configurable file extensions and maximum issue count
- Comprehensive test suite
