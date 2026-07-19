"""Basic descriptive statistics and an ordinary least squares line fit.

The formulas here are the ones used to produce the regression line and the
uncertainty budget in the report.  They are implemented from scratch so the
package stays dependency free; for the modest sample sizes of the experiment
the straightforward implementations are more than fast enough.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Sequence


def mean(values: Sequence[float]) -> float:
    """Return the arithmetic mean of *values*."""
    if not values:
        raise ValueError("mean() requires at least one value")
    return math.fsum(values) / len(values)


def sample_variance(values: Sequence[float]) -> float:
    """Return the (Bessel corrected) sample variance of *values*."""
    n = len(values)
    if n < 2:
        raise ValueError("sample_variance() requires at least two values")
    mu = mean(values)
    return math.fsum((v - mu) ** 2 for v in values) / (n - 1)


def standard_deviation(values: Sequence[float]) -> float:
    """Return the sample standard deviation of *values*."""
    return math.sqrt(sample_variance(values))


def standard_error(values: Sequence[float]) -> float:
    """Return the standard error of the mean of *values*."""
    return standard_deviation(values) / math.sqrt(len(values))


@dataclass(frozen=True)
class LinearFit:
    """Result of an ordinary least squares fit ``y = slope * x + intercept``."""

    slope: float
    intercept: float
    slope_err: float
    intercept_err: float
    r_squared: float
    n: int

    def predict(self, x: float) -> float:
        """Evaluate the fitted line at *x*."""
        return self.slope * x + self.intercept


def linear_regression(xs: Sequence[float], ys: Sequence[float]) -> LinearFit:
    """Fit a straight line to *(xs, ys)* by ordinary least squares.

    The standard errors are the usual textbook expressions derived from the
    residual variance.  A :class:`ValueError` is raised when there are fewer
    than three points (the residual degrees of freedom would otherwise be
    non-positive) or when all *xs* are identical.
    """
    if len(xs) != len(ys):
        raise ValueError("xs and ys must have the same length")
    n = len(xs)
    if n < 3:
        raise ValueError("linear_regression() requires at least three points")

    mx = mean(xs)
    my = mean(ys)
    sxx = math.fsum((x - mx) ** 2 for x in xs)
    if sxx == 0.0:
        raise ValueError("linear_regression() requires non-constant xs")
    sxy = math.fsum((x - mx) * (y - my) for x, y in zip(xs, ys))
    syy = math.fsum((y - my) ** 2 for y in ys)

    slope = sxy / sxx
    intercept = my - slope * mx

    residual_ss = max(syy - slope * sxy, 0.0)
    dof = n - 2
    residual_var = residual_ss / dof
    slope_err = math.sqrt(residual_var / sxx)
    intercept_err = math.sqrt(residual_var * (1.0 / n + mx * mx / sxx))
    r_squared = 1.0 if syy == 0.0 else 1.0 - residual_ss / syy

    return LinearFit(
        slope=slope,
        intercept=intercept,
        slope_err=slope_err,
        intercept_err=intercept_err,
        r_squared=r_squared,
        n=n,
    )
