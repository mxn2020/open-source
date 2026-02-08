# Changelog

All notable changes to the monorepo will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [0.1.0] - 2026-02-08

### Added

- Initial monorepo structure with 11 projects
- Root CI/CD workflows (lint, test, release)
- Root documentation site with mkdocs-material
- Pre-commit hooks configuration
- Makefile with bootstrap, lint, test, ci, docs targets
- Projects:
  - config-drift-detector: Detect drift between configuration sources
  - pr-reviewer-bot: Automated PR review suggestions
  - dotenv-doctor: Validate and diagnose .env files
  - feature-flag-service: Feature flag management API
  - api-rate-limit-visualizer: Visualize API rate limit usage
  - prompt-version-control: Version control for LLM prompts
  - model-output-evaluator: Evaluate and score model outputs
  - timezone-safe-date-utils: Timezone-safe date utilities
  - retry-with-backoff: Retry with configurable backoff strategies
  - error-log-summarizer: Summarize and categorize error logs
  - good-first-issue-generator: Generate good first issues for projects
