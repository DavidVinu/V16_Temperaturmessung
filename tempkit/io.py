"""Reading and writing the CSV measurement logs.

The on-disk format is a plain comma separated file with a single header row::

    measurement_id,run_id,sensor_id,t_seconds,temperature_c,ambient_c

Only the standard library :mod:`csv` module is used so the files can be
opened just as happily in a spreadsheet as by this loader.
"""

from __future__ import annotations

import csv
import os
from typing import Iterable, List

from .models import Measurement, MeasurementSeries

#: The column order written by :func:`save_measurements`.
FIELDNAMES = (
    "measurement_id",
    "run_id",
    "sensor_id",
    "t_seconds",
    "temperature_c",
    "ambient_c",
)


def _row_to_measurement(row: dict) -> Measurement:
    return Measurement(
        measurement_id=int(row["measurement_id"]),
        run_id=int(row["run_id"]),
        sensor_id=str(row["sensor_id"]),
        t_seconds=float(row["t_seconds"]),
        temperature_c=float(row["temperature_c"]),
        ambient_c=float(row["ambient_c"]),
    )


def load_measurements(path: str) -> MeasurementSeries:
    """Load a single CSV file into a :class:`MeasurementSeries`."""
    series = MeasurementSeries()
    with open(path, newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        missing = set(FIELDNAMES) - set(reader.fieldnames or ())
        if missing:
            raise ValueError(f"{path}: missing columns {sorted(missing)}")
        for row in reader:
            series.add(_row_to_measurement(row))
    return series


def load_dataset(directory: str) -> MeasurementSeries:
    """Load and concatenate every ``*.csv`` file in *directory*.

    Files are read in sorted order so the concatenation is deterministic.
    """
    series = MeasurementSeries()
    for name in sorted(os.listdir(directory)):
        if not name.endswith(".csv"):
            continue
        series.extend(load_measurements(os.path.join(directory, name)))
    return series


def save_measurements(path: str, measurements: Iterable[Measurement]) -> int:
    """Write *measurements* to *path* and return the number of rows written."""
    count = 0
    with open(path, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
        writer.writeheader()
        for m in measurements:
            writer.writerow(
                {
                    "measurement_id": m.measurement_id,
                    "run_id": m.run_id,
                    "sensor_id": m.sensor_id,
                    "t_seconds": m.t_seconds,
                    "temperature_c": m.temperature_c,
                    "ambient_c": m.ambient_c,
                }
            )
            count += 1
    return count


def iter_csv_files(directory: str) -> List[str]:
    """Return the sorted list of CSV file paths in *directory*."""
    return [
        os.path.join(directory, name)
        for name in sorted(os.listdir(directory))
        if name.endswith(".csv")
    ]
