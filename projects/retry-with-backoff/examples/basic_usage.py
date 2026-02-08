"""Basic usage of retry-with-backoff."""

import random

from retry_with_backoff import ExponentialBackoff, retry


@retry(
    max_attempts=5,
    strategy=ExponentialBackoff(base=0.1, multiplier=2.0, max_delay=5.0),
    on=(ConnectionError,),
    on_retry=lambda attempt, exc: print(f"  Retry #{attempt} after: {exc}"),
)
def fetch_data(url: str) -> str:
    """Simulate fetching data from a URL that may fail."""
    if random.random() < 0.7:
        raise ConnectionError(f"Failed to connect to {url}")
    return f"Data from {url}"


if __name__ == "__main__":
    print("Attempting to fetch data...")
    try:
        result = fetch_data("https://api.example.com/data")
        print(f"Success: {result}")
    except Exception as exc:
        print(f"Failed after all retries: {exc}")
