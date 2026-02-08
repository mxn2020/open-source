# Design Document

## Overview

`timezone-safe-date-utils` is a TypeScript library that provides timezone-aware date utilities built entirely on the native `Intl.DateTimeFormat` API. The library requires zero runtime dependencies and offers a simple, functional API for common timezone operations.

## Goals

1. **Correctness** – Handle timezone conversions accurately, including DST transitions.
2. **Zero dependencies** – Rely only on built-in JavaScript APIs (`Intl.DateTimeFormat`, `Date`).
3. **Type safety** – Full TypeScript with strict mode, providing clear type signatures for all public functions.
4. **Simplicity** – Expose a small, focused API that covers the most common timezone use cases.

## Architecture

The library is organized into four focused modules:

### `zones.ts` – Timezone Information

Provides timezone validation and metadata. Uses `Intl.DateTimeFormat` to verify timezone identifiers and compute UTC offsets. Maintains a curated list of common IANA timezone names for convenience.

### `convert.ts` – Timezone Conversion

Handles converting dates between timezones and to/from UTC. All conversions work by calculating the UTC offset difference between timezones at the given moment, which correctly accounts for DST.

### `format.ts` – Date Formatting

Provides timezone-aware formatting using `Intl.DateTimeFormat` and `formatToParts`. Includes ISO 8601 formatting with correct timezone offsets and human-readable relative time formatting.

### `parse.ts` – Date Parsing

Parses date strings with explicit timezone context. Supports ISO 8601 strings natively and provides a `parseInTimezone` function for parsing wall-clock time strings in a given timezone.

## Key Design Decisions

### Using `Intl.DateTimeFormat` for Timezone Operations

The `Intl.DateTimeFormat` API is the only reliable, built-in mechanism for timezone-aware date formatting in JavaScript. By using `formatToParts` and `resolvedOptions`, the library can extract timezone-specific date components and compute offsets without bundling timezone data.

### Date Object Convention

JavaScript's `Date` object always stores time as UTC milliseconds. When functions like `fromUTC` or `nowIn` return a Date representing a wall-clock time in a specific timezone, the Date's UTC components are used to carry the wall-clock values. This is a common convention in JavaScript timezone libraries and is documented in each function's JSDoc.

### Offset Calculation Strategy

The `getTimezoneOffset` function computes offsets by formatting the same instant in both UTC and the target timezone using `toLocaleString`, then measuring the difference. This approach automatically handles DST transitions because the offset is always computed for a specific moment in time.

### Input Validation

All public functions that accept timezone strings validate them using `isValidTimezone` before proceeding. Invalid timezones throw descriptive errors rather than producing undefined behavior.

## Limitations

- The library does not include a comprehensive timezone database; it relies on the host environment's `Intl` implementation.
- Parsing is limited to ISO 8601 and two common date string formats. Custom format strings beyond `"YYYY-MM-DD"` and `"YYYY-MM-DD HH:mm:ss"` are not supported.
- The `formatRelative` function uses approximate durations (30-day months, 365-day years) for simplicity.
