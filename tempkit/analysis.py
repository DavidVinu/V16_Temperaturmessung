"""Higher level fits built on top of the statistics helpers.

The key physical model of the experiment is Newton's law of cooling,

    T(t) = T_ambient + (T0 - T_ambient) * exp(-t / tau),

which linearises to

    ln(T(t) - T_ambient) = ln(T0 - T_ambient) - t / tau.

Fitting a straight line to ``ln(delta)`` against ``t`` therefore recovers the
time constant ``tau`` from the slope and the initial excess temperature from
the intercept.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

from .models import MeasurementSeries
from .statistics import LinearFit, linear_regression


@dataclass(frozen=True)
class CoolingFit:
    """Result of a Newton-cooling fit for one run."""

    tau_s: float
    tau_err_s: float
    delta0_c: float
    r_squared: float
    n: int

    def half_life_s(self) -> float:
        """The time for the excess temperature to halve."""
        return self.tau_s * math.log(2.0)


def fit_cooling(series: MeasurementSeries, min_delta_c: float = 0.5) -> CoolingFit:
    """Fit Newton's law of cooling to *series*.

    Points whose excess temperature has fallen below *min_delta_c* are dropped
    before taking the logarithm; they are dominated by sensor noise and would
    otherwise bias the slope.  The returned time constant comes from the slope
    of the linearised fit, ``tau = -1 / slope``.
    """
    ordered = series.sorted_by_time()
    ts: list[float] = []
    log_deltas: list[float] = []
    for m in ordered:
        if m.delta_c > min_delta_c:
            ts.append(m.t_seconds)
            log_deltas.append(math.log(m.delta_c))
    if len(ts) < 3:
        raise ValueError("fit_cooling() needs at least three usable points")

    fit: LinearFit = linear_regression(ts, log_deltas)
    if fit.slope >= 0:
        raise ValueError("fit_cooling() expected a decaying series")

    tau = -1.0 / fit.slope
    tau_err = fit.slope_err / (fit.slope * fit.slope)
    delta0 = math.exp(fit.intercept)
    return CoolingFit(
        tau_s=tau,
        tau_err_s=tau_err,
        delta0_c=delta0,
        r_squared=fit.r_squared,
        n=fit.n,
    )


def regression_line(series: MeasurementSeries) -> LinearFit:
    """Fit a plain straight line of temperature against time.

    This is the raw regression line drawn in the report before the cooling law
    is applied; it is handy as a quick sanity check of the data.
    """
    ordered = series.sorted_by_time()
    return linear_regression(ordered.times, ordered.temperatures)


def cooling_fits_by_run(
    series: MeasurementSeries, min_delta_c: float = 0.5
) -> dict[int, CoolingFit]:
    """Fit every run in *series* independently and collect the results.

    Runs that do not contain enough usable points are skipped rather than
    raising, so a single short run does not abort a whole-dataset analysis.
    """
    results: dict[int, CoolingFit] = {}
    for run_id in series.run_ids():
        try:
            results[run_id] = fit_cooling(series.for_run(run_id), min_delta_c)
        except ValueError:
            continue
    return results
