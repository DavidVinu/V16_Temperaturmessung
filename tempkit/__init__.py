"""tempkit -- a small analysis toolkit for the V16 Temperaturmessung experiment.

The package bundles the pieces that are needed to turn the raw temperature
readings recorded during the lab into the numbers that appear in the written
report:

* :mod:`tempkit.units` -- temperature unit conversions.
* :mod:`tempkit.models` -- lightweight data containers for measurements.
* :mod:`tempkit.statistics` -- means, spreads and linear regression.
* :mod:`tempkit.io` -- reading and writing the CSV measurement logs.
* :mod:`tempkit.analysis` -- higher level fits (Newton cooling, regression).
* :mod:`tempkit.report` -- human readable summaries of a dataset.

Everything is written in plain Python with no third party dependencies so it
can run inside the CI container without an install step.
"""

from .models import Measurement, MeasurementSeries, Sensor
from .statistics import (
    LinearFit,
    linear_regression,
    mean,
    sample_variance,
    standard_deviation,
    standard_error,
)
from .units import (
    ABSOLUTE_ZERO_C,
    celsius_to_fahrenheit,
    celsius_to_kelvin,
    convert,
    fahrenheit_to_celsius,
    kelvin_to_celsius,
)

__all__ = [
    "ABSOLUTE_ZERO_C",
    "LinearFit",
    "Measurement",
    "MeasurementSeries",
    "Sensor",
    "celsius_to_fahrenheit",
    "celsius_to_kelvin",
    "convert",
    "fahrenheit_to_celsius",
    "kelvin_to_celsius",
    "linear_regression",
    "mean",
    "sample_variance",
    "standard_deviation",
    "standard_error",
]

__version__ = "1.0.0"
