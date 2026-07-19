"""Human readable summaries of a measurement dataset.

The functions here turn the fitted numbers into the short text blocks that are
pasted into the lab report, keeping the wording consistent between runs.
"""

from __future__ import annotations

from typing import List

from .analysis import cooling_fits_by_run, regression_line
from .models import MeasurementSeries
from .statistics import mean, standard_deviation


def summarise_series(series: MeasurementSeries) -> str:
    """Return a one-paragraph summary of a single run."""
    if len(series) == 0:
        return "empty series"
    temps = series.temperatures
    line = regression_line(series)
    return (
        f"{len(series)} readings, "
        f"T = {mean(temps):.2f} +/- {standard_deviation(temps):.2f} C, "
        f"slope = {line.slope:.4f} C/s (R^2 = {line.r_squared:.4f})"
    )


def summarise_dataset(series: MeasurementSeries) -> str:
    """Return a multi-line summary covering every run in *series*."""
    lines: List[str] = []
    lines.append(f"dataset: {len(series)} readings across "
                 f"{len(series.run_ids())} runs and "
                 f"{len(series.sensor_ids())} sensors")
    fits = cooling_fits_by_run(series)
    if fits:
        taus = [f.tau_s for f in fits.values()]
        lines.append(
            f"time constant tau = {mean(taus):.1f} +/- "
            f"{standard_deviation(taus):.1f} s "
            f"(from {len(taus)} runs)"
        )
        for run_id in sorted(fits):
            fit = fits[run_id]
            lines.append(
                f"  run {run_id}: tau = {fit.tau_s:.1f} s, "
                f"delta0 = {fit.delta0_c:.1f} C, "
                f"R^2 = {fit.r_squared:.4f}"
            )
    else:
        lines.append("no run had enough usable points for a cooling fit")
    return "\n".join(lines)
