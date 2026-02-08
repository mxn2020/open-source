"""Tests for the retry decorator."""

from unittest.mock import MagicMock

import pytest

from retry_with_backoff import MaxRetriesExceeded, retry
from retry_with_backoff.strategies import ConstantBackoff


class TestRetry:
    def test_succeeds_on_first_attempt(self):
        mock = MagicMock(return_value="ok")

        @retry(max_attempts=3, strategy=ConstantBackoff(0))
        def fn():
            return mock()

        assert fn() == "ok"
        assert mock.call_count == 1

    def test_succeeds_after_failures(self):
        mock = MagicMock(side_effect=[ValueError("fail"), ValueError("fail"), "ok"])

        @retry(max_attempts=3, strategy=ConstantBackoff(0), on=(ValueError,))
        def fn():
            return mock()

        assert fn() == "ok"
        assert mock.call_count == 3

    def test_raises_max_retries_exceeded(self):
        mock = MagicMock(side_effect=ValueError("always fails"))

        @retry(max_attempts=3, strategy=ConstantBackoff(0), on=(ValueError,))
        def fn():
            return mock()

        with pytest.raises(MaxRetriesExceeded) as exc_info:
            fn()

        assert exc_info.value.attempts == 3
        assert isinstance(exc_info.value.last_exception, ValueError)
        assert mock.call_count == 3

    def test_does_not_catch_unspecified_exceptions(self):
        mock = MagicMock(side_effect=TypeError("wrong type"))

        @retry(max_attempts=3, strategy=ConstantBackoff(0), on=(ValueError,))
        def fn():
            return mock()

        with pytest.raises(TypeError):
            fn()

        assert mock.call_count == 1

    def test_on_retry_callback(self):
        callback = MagicMock()
        mock = MagicMock(side_effect=[ValueError("1"), ValueError("2"), "ok"])

        @retry(max_attempts=3, strategy=ConstantBackoff(0), on=(ValueError,), on_retry=callback)
        def fn():
            return mock()

        assert fn() == "ok"
        assert callback.call_count == 2
        # First retry: attempt=1
        assert callback.call_args_list[0][0][0] == 1
        assert isinstance(callback.call_args_list[0][0][1], ValueError)
        # Second retry: attempt=2
        assert callback.call_args_list[1][0][0] == 2

    def test_on_retry_callback_on_exhaustion(self):
        callback = MagicMock()
        mock = MagicMock(side_effect=ValueError("fail"))

        @retry(max_attempts=2, strategy=ConstantBackoff(0), on=(ValueError,), on_retry=callback)
        def fn():
            return mock()

        with pytest.raises(MaxRetriesExceeded):
            fn()

        # on_retry is called before retries, not after the last failure
        assert callback.call_count == 1

    def test_preserves_return_value(self):
        @retry(max_attempts=1, strategy=ConstantBackoff(0))
        def fn():
            return {"key": "value"}

        assert fn() == {"key": "value"}

    def test_passes_arguments(self):
        @retry(max_attempts=1, strategy=ConstantBackoff(0))
        def fn(a, b, c=None):
            return (a, b, c)

        assert fn(1, 2, c=3) == (1, 2, 3)

    def test_default_strategy(self):
        mock = MagicMock(return_value="ok")

        @retry(max_attempts=1)
        def fn():
            return mock()

        assert fn() == "ok"

    def test_max_retries_exceeded_wraps_exception(self):
        original = ValueError("original error")
        mock = MagicMock(side_effect=original)

        @retry(max_attempts=1, strategy=ConstantBackoff(0), on=(ValueError,))
        def fn():
            return mock()

        with pytest.raises(MaxRetriesExceeded) as exc_info:
            fn()

        assert exc_info.value.__cause__ is original
