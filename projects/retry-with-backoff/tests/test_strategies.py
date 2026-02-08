"""Tests for backoff strategies."""

from retry_with_backoff.strategies import (
    ConstantBackoff,
    ExponentialBackoff,
    JitteredExponentialBackoff,
    LinearBackoff,
)


class TestConstantBackoff:
    def test_returns_constant_delay(self):
        strategy = ConstantBackoff(delay=2.0)
        assert strategy.delay(0) == 2.0
        assert strategy.delay(1) == 2.0
        assert strategy.delay(5) == 2.0
        assert strategy.delay(100) == 2.0

    def test_default_delay(self):
        strategy = ConstantBackoff()
        assert strategy.delay(0) == 1.0


class TestLinearBackoff:
    def test_linear_increase(self):
        strategy = LinearBackoff(initial=1.0, increment=0.5)
        assert strategy.delay(0) == 1.0
        assert strategy.delay(1) == 1.5
        assert strategy.delay(2) == 2.0
        assert strategy.delay(3) == 2.5

    def test_default_values(self):
        strategy = LinearBackoff()
        assert strategy.delay(0) == 1.0
        assert strategy.delay(1) == 2.0
        assert strategy.delay(2) == 3.0

    def test_zero_initial(self):
        strategy = LinearBackoff(initial=0.0, increment=1.0)
        assert strategy.delay(0) == 0.0
        assert strategy.delay(3) == 3.0


class TestExponentialBackoff:
    def test_exponential_increase(self):
        strategy = ExponentialBackoff(base=1.0, multiplier=2.0, max_delay=60.0)
        assert strategy.delay(0) == 1.0
        assert strategy.delay(1) == 2.0
        assert strategy.delay(2) == 4.0
        assert strategy.delay(3) == 8.0

    def test_max_delay_cap(self):
        strategy = ExponentialBackoff(base=1.0, multiplier=2.0, max_delay=5.0)
        assert strategy.delay(0) == 1.0
        assert strategy.delay(1) == 2.0
        assert strategy.delay(2) == 4.0
        assert strategy.delay(3) == 5.0  # capped at max_delay
        assert strategy.delay(10) == 5.0

    def test_default_values(self):
        strategy = ExponentialBackoff()
        assert strategy.delay(0) == 1.0
        assert strategy.delay(1) == 2.0

    def test_custom_base_and_multiplier(self):
        strategy = ExponentialBackoff(base=0.5, multiplier=3.0, max_delay=100.0)
        assert strategy.delay(0) == 0.5
        assert strategy.delay(1) == 1.5
        assert strategy.delay(2) == 4.5


class TestJitteredExponentialBackoff:
    def test_delay_within_bounds(self):
        strategy = JitteredExponentialBackoff(base=1.0, multiplier=2.0, max_delay=60.0)
        for attempt in range(10):
            exp_delay = 1.0 * (2.0**attempt)
            exp_delay = min(exp_delay, 60.0)
            d = strategy.delay(attempt)
            assert 0 <= d <= exp_delay

    def test_jitter_varies(self):
        strategy = JitteredExponentialBackoff(base=1.0, multiplier=2.0, max_delay=60.0)
        delays = {strategy.delay(5) for _ in range(20)}
        # With 20 samples from uniform distribution, we should get multiple distinct values
        assert len(delays) > 1

    def test_respects_max_delay(self):
        strategy = JitteredExponentialBackoff(base=1.0, multiplier=2.0, max_delay=10.0)
        for _ in range(50):
            assert strategy.delay(100) <= 10.0
