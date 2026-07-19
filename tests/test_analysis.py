"""Tests for :mod:`tempkit.analysis`."""

import math

from tempkit.analysis import cooling_fits_by_run, fit_cooling, regression_line
from tempkit.models import Measurement, MeasurementSeries


def _cooling_series(tau=120.0, delta0=60.0, ambient=21.0, n=60, dt=5.0, run=1):
    series = MeasurementSeries()
    for i in range(n):
        t = i * dt
        temp = ambient + delta0 * math.exp(-t / tau)
        series.add(Measurement(i + 1, run, "s1", t, temp, ambient))
    return series


def test_fit_cooling_recovers_tau():
    fit = fit_cooling(_cooling_series(tau=120.0))
    assert math.isclose(fit.tau_s, 120.0, rel_tol=1e-6)
    assert math.isclose(fit.delta0_c, 60.0, rel_tol=1e-6)
    assert fit.r_squared > 0.999


def test_half_life_matches_tau():
    fit = fit_cooling(_cooling_series(tau=120.0))
    assert math.isclose(fit.half_life_s(), 120.0 * math.log(2.0), rel_tol=1e-6)


def test_regression_line_runs():
    line = regression_line(_cooling_series())
    assert line.slope < 0.0  # cooling means temperature falls with time


def test_cooling_fits_by_run_collects_multiple():
    series = MeasurementSeries()
    series.extend(_cooling_series(tau=100.0, run=1))
    series.extend(_cooling_series(tau=200.0, run=2))
    fits = cooling_fits_by_run(series)
    assert set(fits) == {1, 2}
    assert math.isclose(fits[1].tau_s, 100.0, rel_tol=1e-6)
    assert math.isclose(fits[2].tau_s, 200.0, rel_tol=1e-6)
