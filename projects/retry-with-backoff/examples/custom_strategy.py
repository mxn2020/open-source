"""Example of implementing a custom backoff strategy."""

from retry_with_backoff import BackoffStrategy, retry


class FibonacciBackoff(BackoffStrategy):
    """Backoff strategy using the Fibonacci sequence for delays.

    Produces delays: 1, 1, 2, 3, 5, 8, 13, ...
    """

    def __init__(self, max_delay: float = 60.0) -> None:
        self._max_delay = max_delay

    def delay(self, attempt: int) -> float:
        a, b = 1.0, 1.0
        for _ in range(attempt):
            a, b = b, a + b
        return min(a, self._max_delay)


call_count = 0


@retry(
    max_attempts=6,
    strategy=FibonacciBackoff(max_delay=30.0),
    on=(ValueError,),
    on_retry=lambda attempt, exc: print(f"  Retry #{attempt}, error: {exc}"),
)
def unreliable_operation() -> str:
    """Simulate an operation that fails a few times before succeeding."""
    global call_count
    call_count += 1
    if call_count < 4:
        raise ValueError(f"Attempt {call_count} failed")
    return "success"


if __name__ == "__main__":
    # Demonstrate Fibonacci backoff delays
    fib = FibonacciBackoff()
    print("Fibonacci backoff delays:")
    for i in range(8):
        print(f"  Attempt {i}: {fib.delay(i):.1f}s")

    print("\nRunning unreliable operation with Fibonacci backoff...")
    result = unreliable_operation()
    print(f"Result: {result}")
