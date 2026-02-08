# Design

## Overview

`retry-with-backoff` provides a simple, composable retry mechanism for Python functions.
The library separates the retry logic from the backoff strategy, allowing users to mix and
match or create custom strategies.

## Architecture

The library consists of three modules:

- **`strategies`**: Defines the `BackoffStrategy` ABC and built-in implementations.
- **`retry`**: Provides `retry` and `async_retry` decorators that use strategies.
- **`exceptions`**: Defines `MaxRetriesExceeded` for clear error reporting.

## Design Decisions

### Strategy Pattern

Backoff logic is encapsulated in strategy objects rather than configuration parameters.
This allows users to implement arbitrarily complex backoff logic by subclassing
`BackoffStrategy`.

### Zero-Based Attempt Counting

The `delay(attempt)` method uses zero-based counting where `attempt=0` represents the
delay before the first retry (after the first failure). This aligns naturally with
exponential calculations: `base * multiplier^0 = base`.

### Exception Wrapping

`MaxRetriesExceeded` wraps the last exception using `__cause__` to preserve the full
exception chain, making debugging straightforward.

### Sync and Async Separation

Rather than a single decorator that auto-detects async functions, the library provides
separate `retry` and `async_retry` decorators for explicitness and type safety.

### No Runtime Dependencies

The library uses only the Python standard library to minimize dependency conflicts
and keep the install footprint small.
