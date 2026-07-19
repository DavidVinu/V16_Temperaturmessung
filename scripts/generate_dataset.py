#!/usr/bin/env python3
"""Deterministically generate the ``data/`` measurement logs.

Every reading follows Newton's law of cooling,

    T(t) = T_ambient + (T0 - T_ambient) * exp(-t / tau),

with a small amount of Gaussian sensor noise added on top.  The per-run
parameters (``T0``, ``T_ambient``, ``tau``) are drawn from physically
plausible ranges using a fixed seed, so re-running this script always
reproduces byte-for-byte the same dataset.

The readings are streamed into ``run_data_XXXX.csv`` files, each with a single
header row followed by up to ``LINES_PER_FILE - 1`` readings.  ``TOTAL_LINES``
controls the total number of CSV lines emitted (headers included); it is kept
in one place so the dataset size is easy to adjust and easy to audit.
"""

from __future__ import annotations

import math
import os
import random
from typing import Iterator, Tuple

#: Master seed -- change this to get a different but still reproducible set.
SEED = 20260719

#: Total number of CSV lines to emit across every file, header rows included.
TOTAL_LINES = 98810

#: Maximum number of lines (header + readings) per output file.
LINES_PER_FILE = 5000

#: Number of readings that make up a single cooling run.
ROWS_PER_RUN = 200

#: Spacing between successive readings within a run, in seconds.
DT_SECONDS = 3.0

#: Thermocouples cycled through, one per run.
SENSORS = ("S1", "S2", "S3", "S4")

#: CSV header written at the top of every file.
HEADER = "measurement_id,run_id,sensor_id,t_seconds,temperature_c,ambient_c"


def run_parameters(run_id: int) -> Tuple[float, float, float]:
    """Return the deterministic ``(ambient_c, t0_c, tau_s)`` for *run_id*."""
    rng = random.Random(f"{SEED}-run-{run_id}")
    ambient = round(rng.uniform(20.0, 23.0), 2)
    t0 = round(rng.uniform(70.0, 95.0), 2)
    tau = round(rng.uniform(90.0, 240.0), 1)
    return ambient, t0, tau


def reading_row(measurement_id: int) -> str:
    """Build the CSV line for the globally-indexed *measurement_id*.

    The reading's run and within-run position are derived purely from the
    global index, so the output is independent of how the rows are split into
    files.
    """
    index = measurement_id - 1
    run_id = index // ROWS_PER_RUN + 1
    within_run = index % ROWS_PER_RUN
    sensor = SENSORS[(run_id - 1) % len(SENSORS)]

    ambient, t0, tau = run_parameters(run_id)
    t = within_run * DT_SECONDS
    true_temp = ambient + (t0 - ambient) * math.exp(-t / tau)
    noise = random.Random(f"{SEED}-noise-{measurement_id}").gauss(0.0, 0.05)
    temp = round(true_temp + noise, 3)

    return f"{measurement_id},{run_id},{sensor},{t:.1f},{temp:.3f},{ambient:.2f}"


def _file_line_counts(total_lines: int, per_file: int) -> list[int]:
    """Split *total_lines* into per-file line counts of at most *per_file*."""
    if total_lines <= 0:
        return []
    num_files = math.ceil(total_lines / per_file)
    counts = [per_file] * (num_files - 1)
    counts.append(total_lines - per_file * (num_files - 1))
    return counts


def iter_rows(num_rows: int) -> Iterator[str]:
    """Yield *num_rows* CSV data rows starting from measurement id 1."""
    for measurement_id in range(1, num_rows + 1):
        yield reading_row(measurement_id)


def generate(directory: str, total_lines: int = TOTAL_LINES) -> Tuple[int, int]:
    """Generate the dataset in *directory*.

    Returns a ``(files_written, rows_written)`` tuple.  Any pre-existing
    ``run_data_*.csv`` files are removed first so regeneration is clean.
    """
    os.makedirs(directory, exist_ok=True)
    for name in os.listdir(directory):
        if name.startswith("run_data_") and name.endswith(".csv"):
            os.remove(os.path.join(directory, name))

    counts = _file_line_counts(total_lines, LINES_PER_FILE)
    rows = iter_rows(total_lines - len(counts))

    rows_written = 0
    for file_index, line_count in enumerate(counts, start=1):
        path = os.path.join(directory, f"run_data_{file_index:04d}.csv")
        with open(path, "w", encoding="utf-8", newline="") as handle:
            handle.write(HEADER + "\n")
            for _ in range(line_count - 1):
                handle.write(next(rows) + "\n")
                rows_written += 1
    return len(counts), rows_written


def main() -> int:
    here = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(os.path.dirname(here), "data")
    files_written, rows_written = generate(data_dir)
    total = files_written + rows_written
    print(
        f"wrote {rows_written} readings across {files_written} files "
        f"({total} CSV lines) into {data_dir}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
