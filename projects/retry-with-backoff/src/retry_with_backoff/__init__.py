"""Retry with configurable backoff strategies."""

__version__ = "0.1.0"

from retry_with_backoff.exceptions import MaxRetriesExceeded
from retry_with_backoff.retry import async_retry, retry
from retry_with_backoff.strategies import (
    BackoffStrategy,
    ConstantBackoff,
    ExponentialBackoff,
    JitteredExponentialBackoff,
    LinearBackoff,
)

__all__ = [
    "retry",
    "async_retry",
    "BackoffStrategy",
    "ConstantBackoff",
    "LinearBackoff",
    "ExponentialBackoff",
    "JitteredExponentialBackoff",
    "MaxRetriesExceeded",
]
