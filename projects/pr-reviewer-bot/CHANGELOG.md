# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-01-01

### Added

- Initial release of pr-reviewer-bot.
- Unified diff parser supporting single and multi-file diffs.
- Pattern-based analyzer with six rules: large-change, todo-comment, debug-statement, hardcoded-secret, long-line, trailing-whitespace.
- Rich-formatted text output and JSON output for CI integration.
- CLI with severity filtering, stdin support, and meaningful exit codes.
