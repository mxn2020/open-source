"""Retry decorators with backoff strategies."""

import asyncio
import functools
import time
from collections.abc import Callable
from typing import Any

from retry_with_backoff.exceptions import MaxRetriesExceeded
from retry_with_backoff.strategies import BackoffStrategy, ExponentialBackoff


def retry(
    max_attempts: int = 3,
    strategy: BackoffStrategy | None = None,
    on: tuple[type[Exception], ...] = (Exception,),
    on_retry: Callable[[int, Exception], None] | None = None,
) -> Callable:
    """Decorator that retries a function on specified exceptions with backoff.

    Args:
        max_attempts: Maximum number of attempts (including the first call).
        strategy: Backoff strategy to use for delays. Defaults to ExponentialBackoff.
        on: Tuple of exception types to catch and retry on.
        on_retry: Optional callback invoked before each retry with (attempt, exception).

    Returns:
        A decorator that wraps the target function with retry logic.
    """
    if strategy is None:
        strategy = ExponentialBackoff()

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            last_exception: Exception | None = None
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except on as exc:
                    last_exception = exc
                    if attempt < max_attempts - 1:
                        if on_retry is not None:
                            on_retry(attempt + 1, exc)
                        delay = strategy.delay(attempt)
                        time.sleep(delay)
            raise MaxRetriesExceeded(max_attempts, last_exception)  # type: ignore[arg-type]

        return wrapper

    return decorator


def async_retry(
    max_attempts: int = 3,
    strategy: BackoffStrategy | None = None,
    on: tuple[type[Exception], ...] = (Exception,),
    on_retry: Callable[[int, Exception], None] | None = None,
) -> Callable:
    """Decorator that retries an async function on specified exceptions with backoff.

    Args:
        max_attempts: Maximum number of attempts (including the first call).
        strategy: Backoff strategy to use for delays. Defaults to ExponentialBackoff.
        on: Tuple of exception types to catch and retry on.
        on_retry: Optional callback invoked before each retry with (attempt, exception).

    Returns:
        A decorator that wraps the target async function with retry logic.
    """
    if strategy is None:
        strategy = ExponentialBackoff()

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            last_exception: Exception | None = None
            for attempt in range(max_attempts):
                try:
                    return await func(*args, **kwargs)
                except on as exc:
                    last_exception = exc
                    if attempt < max_attempts - 1:
                        if on_retry is not None:
                            on_retry(attempt + 1, exc)
                        delay = strategy.delay(attempt)
                        await asyncio.sleep(delay)
            raise MaxRetriesExceeded(max_attempts, last_exception)  # type: ignore[arg-type]

        return wrapper

    return decorator
