# retry-with-backoff

A Python library that provides retry functionality with configurable backoff strategies.
Zero runtime dependencies, pure Python.

## Features

- **Sync and async support**: `@retry` for synchronous functions, `@async_retry` for async.
- **Built-in strategies**: Constant, Linear, Exponential, and Jittered Exponential backoff.
- **Custom strategies**: Implement the `BackoffStrategy` interface for your own logic.
- **Selective exception handling**: Retry only on specified exception types.
- **Retry callbacks**: Hook into retry events for logging or monitoring.
- **Type-safe**: Full type hints with `functools.wraps` preservation.

## Installation

```bash
pip install retry-with-backoff
```

## Quick Start

```python
from retry_with_backoff import retry, ExponentialBackoff

@retry(
    max_attempts=5,
    strategy=ExponentialBackoff(base=1.0, multiplier=2.0, max_delay=30.0),
    on=(ConnectionError, TimeoutError),
)
def fetch_data(url: str) -> dict:
    # your code here
    ...
```

## Backoff Strategies

### ConstantBackoff

Returns a fixed delay between retries.

```python
from retry_with_backoff import retry, ConstantBackoff

@retry(max_attempts=3, strategy=ConstantBackoff(delay=2.0))
def my_function():
    ...
```

### LinearBackoff

Delay increases linearly: `delay = initial + attempt * increment`.

```python
from retry_with_backoff import retry, LinearBackoff

@retry(max_attempts=5, strategy=LinearBackoff(initial=1.0, increment=0.5))
def my_function():
    ...
```

### ExponentialBackoff

Delay increases exponentially: `delay = min(base * multiplier^attempt, max_delay)`.

```python
from retry_with_backoff import retry, ExponentialBackoff

@retry(max_attempts=5, strategy=ExponentialBackoff(base=1.0, multiplier=2.0, max_delay=60.0))
def my_function():
    ...
```

### JitteredExponentialBackoff

Exponential backoff with random jitter between 0 and the calculated delay.

```python
from retry_with_backoff import retry, JitteredExponentialBackoff

@retry(max_attempts=5, strategy=JitteredExponentialBackoff(base=1.0, multiplier=2.0))
def my_function():
    ...
```

## Custom Strategies

Implement the `BackoffStrategy` abstract base class:

```python
from retry_with_backoff import BackoffStrategy, retry

class FibonacciBackoff(BackoffStrategy):
    def delay(self, attempt: int) -> float:
        a, b = 1.0, 1.0
        for _ in range(attempt):
            a, b = b, a + b
        return a

@retry(max_attempts=5, strategy=FibonacciBackoff())
def my_function():
    ...
```

## Retry Callbacks

Use the `on_retry` parameter to hook into retry events:

```python
import logging

from retry_with_backoff import retry, ExponentialBackoff

logger = logging.getLogger(__name__)

@retry(
    max_attempts=3,
    strategy=ExponentialBackoff(),
    on_retry=lambda attempt, exc: logger.warning(f"Retry {attempt}: {exc}"),
)
def my_function():
    ...
```

## Async Support

```python
import asyncio
from retry_with_backoff import async_retry, ExponentialBackoff

@async_retry(max_attempts=3, strategy=ExponentialBackoff(base=0.1))
async def fetch_async(url: str) -> str:
    # your async code here
    ...
```

## Exception Handling

When all retries are exhausted, `MaxRetriesExceeded` is raised. It wraps the
original exception:

```python
from retry_with_backoff import retry, MaxRetriesExceeded, ConstantBackoff

@retry(max_attempts=3, strategy=ConstantBackoff(0), on=(ValueError,))
def failing():
    raise ValueError("always fails")

try:
    failing()
except MaxRetriesExceeded as exc:
    print(f"Failed after {exc.attempts} attempts")
    print(f"Last error: {exc.last_exception}")
    print(f"Cause: {exc.__cause__}")
```

## Development

```bash
pip install -e ".[dev]"
python -m pytest tests/ -v
ruff check src/ tests/
black --check src/ tests/
```

## License

MIT License. See [LICENSE](LICENSE) for details.
