"""Tests for decorator behavior and async_retry."""

import asyncio
import inspect
from unittest.mock import MagicMock

import pytest

from retry_with_backoff import MaxRetriesExceeded, async_retry, retry
from retry_with_backoff.strategies import ConstantBackoff


class TestDecoratorPreservation:
    def test_preserves_function_name(self):
        @retry(max_attempts=1, strategy=ConstantBackoff(0))
        def my_function():
            """My docstring."""

        assert my_function.__name__ == "my_function"
        assert my_function.__doc__ == "My docstring."

    def test_preserves_function_module(self):
        @retry(max_attempts=1, strategy=ConstantBackoff(0))
        def my_function():
            pass

        assert my_function.__module__ == __name__

    def test_async_preserves_function_name(self):
        @async_retry(max_attempts=1, strategy=ConstantBackoff(0))
        async def my_async_function():
            """Async docstring."""

        assert my_async_function.__name__ == "my_async_function"
        assert my_async_function.__doc__ == "Async docstring."

    def test_wrapped_function_is_callable(self):
        @retry(max_attempts=1, strategy=ConstantBackoff(0))
        def my_function():
            return 42

        assert callable(my_function)
        assert my_function() == 42

    def test_async_wrapped_function_is_coroutine(self):
        @async_retry(max_attempts=1, strategy=ConstantBackoff(0))
        async def my_async_function():
            return 42

        assert inspect.iscoroutinefunction(my_async_function)


class TestAsyncRetry:
    def test_async_succeeds_on_first_attempt(self):
        mock = MagicMock(return_value="ok")

        @async_retry(max_attempts=3, strategy=ConstantBackoff(0))
        async def fn():
            return mock()

        result = asyncio.run(fn())
        assert result == "ok"
        assert mock.call_count == 1

    def test_async_succeeds_after_failures(self):
        mock = MagicMock(side_effect=[ValueError("1"), ValueError("2"), "ok"])

        @async_retry(max_attempts=3, strategy=ConstantBackoff(0), on=(ValueError,))
        async def fn():
            return mock()

        result = asyncio.run(fn())
        assert result == "ok"
        assert mock.call_count == 3

    def test_async_raises_max_retries_exceeded(self):
        mock = MagicMock(side_effect=ValueError("fail"))

        @async_retry(max_attempts=2, strategy=ConstantBackoff(0), on=(ValueError,))
        async def fn():
            return mock()

        with pytest.raises(MaxRetriesExceeded) as exc_info:
            asyncio.run(fn())

        assert exc_info.value.attempts == 2
        assert isinstance(exc_info.value.last_exception, ValueError)

    def test_async_on_retry_callback(self):
        callback = MagicMock()
        mock = MagicMock(side_effect=[ValueError("1"), "ok"])

        @async_retry(
            max_attempts=3, strategy=ConstantBackoff(0), on=(ValueError,), on_retry=callback
        )
        async def fn():
            return mock()

        result = asyncio.run(fn())
        assert result == "ok"
        assert callback.call_count == 1
        assert callback.call_args_list[0][0][0] == 1

    def test_async_passes_arguments(self):
        @async_retry(max_attempts=1, strategy=ConstantBackoff(0))
        async def fn(x: int, y: int = 0) -> int:
            return x + y

        result = asyncio.run(fn(3, y=4))
        assert result == 7

    def test_async_does_not_catch_unspecified_exceptions(self):
        mock = MagicMock(side_effect=TypeError("wrong"))

        @async_retry(max_attempts=3, strategy=ConstantBackoff(0), on=(ValueError,))
        async def fn():
            return mock()

        with pytest.raises(TypeError):
            asyncio.run(fn())

        assert mock.call_count == 1

    def test_async_default_strategy(self):
        mock = MagicMock(return_value="ok")

        @async_retry(max_attempts=1)
        async def fn():
            return mock()

        assert asyncio.run(fn()) == "ok"
