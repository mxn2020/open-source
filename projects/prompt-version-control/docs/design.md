# Design Document

## Overview

prompt-version-control (`pv`) is a CLI tool for tracking and managing versions of LLM prompts.
It provides Git-like version control semantics tailored specifically for prompt engineering
workflows.

## Motivation

As LLM-based applications grow in complexity, managing prompts becomes a significant challenge.
Prompts are iterated on frequently, and small changes can have large effects on model behavior.
Teams need a way to track prompt changes over time, compare versions, and roll back when needed.

## Architecture

### Storage Layer

The tool uses SQLite as its storage backend. This provides:

- Zero-configuration setup (no external database required).
- ACID transactions for data integrity.
- Single-file storage that is easy to back up and share.

The database schema consists of three tables:

- **prompts**: Stores prompt names and descriptions.
- **versions**: Stores individual prompt versions with content, metadata, and timestamps.
- **tags**: Maps human-readable tag names to specific versions.

### Data Model

Each prompt is identified by a unique name. Versions are auto-incremented integers with a
`.0` suffix (e.g., `1.0`, `2.0`, `3.0`). Each version tracks its parent version to maintain
a linear history.

Metadata is stored as a JSON object and can contain arbitrary key-value pairs such as model
name, temperature, max tokens, or any other parameters relevant to the prompt.

### CLI Layer

The CLI is built with Typer for argument parsing and Rich for terminal formatting. All
commands support a `--json` flag for machine-readable output, making it easy to integrate
with scripts and CI/CD pipelines.

### Diff Engine

Version comparison uses Python's built-in `difflib` module to produce unified diffs. This
provides a familiar format for developers who are used to Git diffs.

## Design Decisions

1. **SQLite over flat files**: SQLite provides better query performance, data integrity, and
   concurrent access compared to YAML/JSON files on disk.

2. **Auto-incrementing versions**: Simplifies the user experience by not requiring manual
   version numbering. The linear versioning model is sufficient for prompt management.

3. **Tags over branches**: Prompts typically follow a linear evolution path. Tags provide a
   lightweight way to mark important versions without the complexity of branching.

4. **Metadata as JSON**: Flexible key-value metadata accommodates different LLM providers
   and their varying configuration parameters.
