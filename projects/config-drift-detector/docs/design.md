# Design Decisions

This document captures the key architectural and design decisions made in
Config Drift Detector.

## Format Auto-Detection

**Decision:** Detect the configuration format from the file extension rather
than requiring the user to specify it.

**Rationale:** Configuration files almost always use standard extensions
(`.yaml`, `.yml`, `.json`, `.toml`). Auto-detection reduces CLI flags and
makes the tool easier to use. If a file has a non-standard extension, the user
gets a clear error message listing supported formats.

## Recursive Deep Comparison

**Decision:** Walk both dictionaries recursively and produce a flat list of
drift items with dot-notation paths.

**Rationale:** Configuration files are typically nested. A shallow comparison
would miss changes inside nested sections. Dot-notation paths (e.g.,
`database.host`) are human-readable and easy to filter or search
programmatically.

## DriftItem Dataclass

**Decision:** Use a frozen dataclass to represent each drift.

**Rationale:** Immutability makes drift items safe to pass around, collect, and
serialize. The dataclass gives us equality, hashing, and a clean repr for free.

## Tag Filtering

**Decision:** Allow the user to restrict comparison to specific top-level keys
via `--tags`.

**Rationale:** In large configurations, operators often care only about a
specific section (e.g., `database` or `feature_flags`). Filtering before
comparison keeps output focused and avoids noise.

## Exit Codes

**Decision:** Use three exit codes — `0` (no drift), `1` (drift found), `2`
(error).

**Rationale:** This follows common CLI conventions and makes the tool usable in
CI pipelines where the exit code drives pass/fail decisions.

## Stdlib TOML

**Decision:** Use `tomllib` from the Python 3.11+ standard library instead of
the third-party `tomli` package.

**Rationale:** The project targets Python ≥ 3.12, so `tomllib` is always
available. Fewer dependencies mean a smaller install footprint and fewer
supply-chain concerns.
