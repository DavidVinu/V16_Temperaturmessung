"""Lightweight data containers for the measurement logs.

The raw data lives in CSV files with one row per reading.  These dataclasses
give the rest of the toolkit a typed view of that data without pulling in a
heavyweight dependency such as pandas.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable, Iterator, List, Sequence


@dataclass(frozen=True)
class Sensor:
    """Metadata describing a single temperature sensor."""

    sensor_id: str
    kind: str = "thermocouple"
    resolution_c: float = 0.1

    def quantise(self, temperature_c: float) -> float:
        """Round *temperature_c* to the sensor's resolution."""
        if self.resolution_c <= 0:
            return temperature_c
        steps = round(temperature_c / self.resolution_c)
        return steps * self.resolution_c


@dataclass(frozen=True)
class Measurement:
    """A single temperature reading taken at a point in time."""

    measurement_id: int
    run_id: int
    sensor_id: str
    t_seconds: float
    temperature_c: float
    ambient_c: float

    @property
    def delta_c(self) -> float:
        """Temperature above ambient, the quantity that decays over time."""
        return self.temperature_c - self.ambient_c


@dataclass
class MeasurementSeries:
    """An ordered collection of :class:`Measurement` objects.

    A series usually corresponds to a single cooling run, but nothing in the
    class enforces that -- it is simply a convenience wrapper that exposes the
    individual columns as plain lists so they can be fed to the statistics and
    analysis helpers.
    """

    measurements: List[Measurement] = field(default_factory=list)

    def __len__(self) -> int:
        return len(self.measurements)

    def __iter__(self) -> Iterator[Measurement]:
        return iter(self.measurements)

    def __getitem__(self, index: int) -> Measurement:
        return self.measurements[index]

    def add(self, measurement: Measurement) -> None:
        """Append a single measurement to the series."""
        self.measurements.append(measurement)

    def extend(self, measurements: Iterable[Measurement]) -> None:
        """Append many measurements to the series."""
        self.measurements.extend(measurements)

    def sorted_by_time(self) -> "MeasurementSeries":
        """Return a new series ordered by the elapsed time column."""
        return MeasurementSeries(sorted(self.measurements, key=lambda m: m.t_seconds))

    @property
    def times(self) -> List[float]:
        """The elapsed time column in seconds."""
        return [m.t_seconds for m in self.measurements]

    @property
    def temperatures(self) -> List[float]:
        """The measured temperature column in degrees Celsius."""
        return [m.temperature_c for m in self.measurements]

    @property
    def ambients(self) -> List[float]:
        """The ambient temperature column in degrees Celsius."""
        return [m.ambient_c for m in self.measurements]

    @property
    def deltas(self) -> List[float]:
        """The temperature-above-ambient column in degrees Celsius."""
        return [m.delta_c for m in self.measurements]

    def run_ids(self) -> Sequence[int]:
        """Return the sorted, de-duplicated run ids present in the series."""
        return sorted({m.run_id for m in self.measurements})

    def sensor_ids(self) -> Sequence[str]:
        """Return the sorted, de-duplicated sensor ids present in the series."""
        return sorted({m.sensor_id for m in self.measurements})

    def for_run(self, run_id: int) -> "MeasurementSeries":
        """Return a sub-series containing only the given *run_id*."""
        return MeasurementSeries([m for m in self.measurements if m.run_id == run_id])

    def for_sensor(self, sensor_id: str) -> "MeasurementSeries":
        """Return a sub-series containing only the given *sensor_id*."""
        return MeasurementSeries(
            [m for m in self.measurements if m.sensor_id == sensor_id]
        )
