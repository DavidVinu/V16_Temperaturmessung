"""Tests for :mod:`tempkit.statistics`."""

import math

import pytest

from tempkit import statistics as stats


def test_mean():
    assert math.isclose(stats.mean([1.0, 2.0, 3.0]), 2.0)


def test_mean_requires_values():
    with pytest.raises(ValueError):
        stats.mean([])


def test_sample_variance_and_std():
    data = [2.0, 4.0, 4.0, 4.0, 5.0, 5.0, 7.0, 9.0]
    assert math.isclose(stats.sample_variance(data), 32.0 / 7.0)
    assert math.isclose(stats.standard_deviation(data), math.sqrt(32.0 / 7.0))


def test_standard_error_scales_with_sqrt_n():
    data = [1.0, 2.0, 3.0, 4.0]
    expected = stats.standard_deviation(data) / 2.0
    assert math.isclose(stats.standard_error(data), expected)


def test_linear_regression_recovers_known_line():
    xs = [0.0, 1.0, 2.0, 3.0, 4.0]
    ys = [1.0, 3.0, 5.0, 7.0, 9.0]  # y = 2x + 1
    fit = stats.linear_regression(xs, ys)
    assert math.isclose(fit.slope, 2.0, abs_tol=1e-9)
    assert math.isclose(fit.intercept, 1.0, abs_tol=1e-9)
    assert math.isclose(fit.r_squared, 1.0, abs_tol=1e-12)
    assert math.isclose(fit.predict(10.0), 21.0, abs_tol=1e-9)


def test_linear_regression_needs_three_points():
    with pytest.raises(ValueError):
        stats.linear_regression([0.0, 1.0], [0.0, 1.0])


def test_linear_regression_rejects_constant_x():
    with pytest.raises(ValueError):
        stats.linear_regression([1.0, 1.0, 1.0], [1.0, 2.0, 3.0])


def test_linear_regression_reports_positive_errors_on_noisy_data():
    xs = [0.0, 1.0, 2.0, 3.0, 4.0, 5.0]
    ys = [0.1, 2.1, 3.9, 6.2, 7.8, 10.1]
    fit = stats.linear_regression(xs, ys)
    assert fit.slope_err > 0.0
    assert fit.intercept_err > 0.0
    assert 0.0 < fit.r_squared <= 1.0
