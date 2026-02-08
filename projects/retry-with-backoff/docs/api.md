# API Reference

## Decorators

### `retry`

```python
retry(
    max_attempts: int = 3,
    strategy: BackoffStrategy | None = None,
    on: tuple[type[Exception], ...] = (Exception,),
    on_retry: Callable[[int, Exception], None] | None = None,
) -> Callable
```

Decorator that retries a synchronous function on specified exceptions.

**Parameters:**

- `max_attempts`: Maximum total attempts including the initial call. Default: 3.
- `strategy`: Backoff strategy instance. Default: `ExponentialBackoff()`.
- `on`: Tuple of exception types to retry on. Default: `(Exception,)`.
- `on_retry`: Callback invoked before each retry with `(attempt_number, exception)`.

**Behavior:**

- On success, returns the function's return value.
- On failure after all attempts, raises `MaxRetriesExceeded`.
- Exceptions not in `on` propagate immediately without retry.

### `async_retry`

```python
async_retry(
    max_attempts: int = 3,
    strategy: BackoffStrategy | None = None,
    on: tuple[type[Exception], ...] = (Exception,),
    on_retry: Callable[[int, Exception], None] | None = None,
) -> Callable
```

Same as `retry` but for async functions. Uses `asyncio.sleep` for delays.

## Strategies

### `BackoffStrategy` (ABC)

```python
class BackoffStrategy(ABC):
    @abstractmethod
    def delay(self, attempt: int) -> float: ...
```

Abstract base class. Implement `delay(attempt)` returning seconds to wait.
The `attempt` parameter is zero-based (0 = first retry).

### `ConstantBackoff`

```python
ConstantBackoff(delay: float = 1.0)
```

Returns the same delay for every attempt.

### `LinearBackoff`

```python
LinearBackoff(initial: float = 1.0, increment: float = 1.0)
```

`delay = initial + attempt * increment`

### `ExponentialBackoff`

```python
ExponentialBackoff(base: float = 1.0, multiplier: float = 2.0, max_delay: float = 60.0)
```

`delay = min(base * multiplier^attempt, max_delay)`

### `JitteredExponentialBackoff`

```python
JitteredExponentialBackoff(base: float = 1.0, multiplier: float = 2.0, max_delay: float = 60.0)
```

Calculates exponential delay then returns `random.uniform(0, delay)`.

## Exceptions

### `MaxRetriesExceeded`

```python
class MaxRetriesExceeded(Exception):
    attempts: int
    last_exception: Exception
```

Raised when all retry attempts are exhausted. The original exception is set as
`__cause__` for exception chaining.
