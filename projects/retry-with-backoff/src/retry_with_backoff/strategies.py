"""Backoff strategies for retry logic."""

import random
from abc import ABC, abstractmethod


class BackoffStrategy(ABC):
    """Abstract base class for backoff strategies."""

    @abstractmethod
    def delay(self, attempt: int) -> float:
        """Calculate the delay in seconds for the given attempt number.

        Args:
            attempt: The zero-based attempt number (0 for the first retry).

        Returns:
            The delay in seconds before the next retry.
        """


class ConstantBackoff(BackoffStrategy):
    """Returns a constant delay between retries.

    Args:
        delay: The constant delay in seconds.
    """

    def __init__(self, delay: float = 1.0) -> None:
        self._delay = delay

    def delay(self, attempt: int) -> float:
        return self._delay


class LinearBackoff(BackoffStrategy):
    """Returns a linearly increasing delay between retries.

    delay = initial + attempt * increment

    Args:
        initial: The initial delay in seconds.
        increment: The increment added per attempt.
    """

    def __init__(self, initial: float = 1.0, increment: float = 1.0) -> None:
        self._initial = initial
        self._increment = increment

    def delay(self, attempt: int) -> float:
        return self._initial + attempt * self._increment


class ExponentialBackoff(BackoffStrategy):
    """Returns an exponentially increasing delay between retries.

    delay = min(base * multiplier^attempt, max_delay)

    Args:
        base: The base delay in seconds.
        multiplier: The multiplier applied per attempt.
        max_delay: The maximum delay in seconds.
    """

    def __init__(
        self, base: float = 1.0, multiplier: float = 2.0, max_delay: float = 60.0
    ) -> None:
        self._base = base
        self._multiplier = multiplier
        self._max_delay = max_delay

    def delay(self, attempt: int) -> float:
        return min(self._base * (self._multiplier**attempt), self._max_delay)


class JitteredExponentialBackoff(BackoffStrategy):
    """Exponential backoff with random jitter.

    Calculates an exponential delay then applies uniform random jitter
    between 0 and the calculated delay.

    Args:
        base: The base delay in seconds.
        multiplier: The multiplier applied per attempt.
        max_delay: The maximum delay in seconds.
    """

    def __init__(
        self, base: float = 1.0, multiplier: float = 2.0, max_delay: float = 60.0
    ) -> None:
        self._exponential = ExponentialBackoff(base, multiplier, max_delay)

    def delay(self, attempt: int) -> float:
        exp_delay = self._exponential.delay(attempt)
        return random.uniform(0, exp_delay)
