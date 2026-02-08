# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-01-01

### Added

- `retry` decorator for synchronous functions with configurable backoff.
- `async_retry` decorator for asynchronous functions with configurable backoff.
- `ConstantBackoff` strategy for fixed delay between retries.
- `LinearBackoff` strategy for linearly increasing delay.
- `ExponentialBackoff` strategy for exponentially increasing delay with max cap.
- `JitteredExponentialBackoff` strategy for exponential delay with random jitter.
- `BackoffStrategy` abstract base class for custom strategies.
- `MaxRetriesExceeded` exception raised when all attempts are exhausted.
- `on_retry` callback support for logging or side effects before each retry.
- Full type hint support with `functools.wraps` preservation.
