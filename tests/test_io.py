"""Tests for :mod:`tempkit.io`."""

import os

from tempkit.io import load_dataset, load_measurements, save_measurements
from tempkit.models import Measurement


def _sample():
    return [
        Measurement(1, 1, "s1", 0.0, 80.0, 21.0),
        Measurement(2, 1, "s1", 1.0, 79.2, 21.0),
        Measurement(3, 1, "s1", 2.0, 78.5, 21.0),
    ]


def test_save_and_load_roundtrip(tmp_path):
    path = os.path.join(tmp_path, "run.csv")
    written = save_measurements(path, _sample())
    assert written == 3
    series = load_measurements(path)
    assert len(series) == 3
    assert series[0].temperature_c == 80.0
    assert series[2].measurement_id == 3


def test_load_dataset_concatenates(tmp_path):
    save_measurements(os.path.join(tmp_path, "a.csv"), _sample())
    save_measurements(os.path.join(tmp_path, "b.csv"), _sample())
    series = load_dataset(tmp_path)
    assert len(series) == 6


def test_load_rejects_missing_columns(tmp_path):
    path = os.path.join(tmp_path, "bad.csv")
    with open(path, "w", encoding="utf-8") as handle:
        handle.write("measurement_id,run_id\n1,1\n")
    try:
        load_measurements(path)
    except ValueError as exc:
        assert "missing columns" in str(exc)
    else:  # pragma: no cover
        raise AssertionError("expected ValueError for missing columns")
