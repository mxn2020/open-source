"""Custom exceptions for retry-with-backoff."""


class MaxRetriesExceeded(Exception):
    """Raised when all retry attempts have been exhausted.

    Wraps the original exception that caused the final failure.
    """

    def __init__(self, attempts: int, last_exception: Exception) -> None:
        self.attempts = attempts
        self.last_exception = last_exception
        super().__init__(
            f"Max retries exceeded after {attempts} attempts. "
            f"Last exception: {last_exception!r}"
        )
        self.__cause__ = last_exception
