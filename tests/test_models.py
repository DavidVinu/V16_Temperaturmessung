"""Tests for :mod:`tempkit.models`."""

import math

from tempkit.models import Measurement, MeasurementSeries, Sensor


def _measurement(mid, run, sensor, t, temp, ambient=21.0):
    return Measurement(mid, run, sensor, t, temp, ambient)


def test_measurement_delta():
    m = _measurement(1, 1, "s1", 0.0, 80.0, ambient=20.0)
    assert math.isclose(m.delta_c, 60.0)


def test_sensor_quantise():
    sensor = Sensor("s1", resolution_c=0.1)
    assert math.isclose(sensor.quantise(21.03), 21.0)
    assert math.isclose(sensor.quantise(21.06), 21.1)


def test_series_columns_and_len():
    series = MeasurementSeries()
    series.add(_measurement(1, 1, "s1", 0.0, 80.0))
    series.add(_measurement(2, 1, "s1", 1.0, 79.0))
    assert len(series) == 2
    assert series.times == [0.0, 1.0]
    assert series.temperatures == [80.0, 79.0]


def test_series_sorted_by_time():
    series = MeasurementSeries()
    series.add(_measurement(1, 1, "s1", 2.0, 78.0))
    series.add(_measurement(2, 1, "s1", 0.0, 80.0))
    ordered = series.sorted_by_time()
    assert ordered.times == [0.0, 2.0]
    # original is untouched
    assert series.times == [2.0, 0.0]


def test_series_filtering():
    series = MeasurementSeries()
    series.add(_measurement(1, 1, "s1", 0.0, 80.0))
    series.add(_measurement(2, 2, "s2", 0.0, 70.0))
    assert list(series.run_ids()) == [1, 2]
    assert list(series.sensor_ids()) == ["s1", "s2"]
    assert len(series.for_run(1)) == 1
    assert series.for_sensor("s2")[0].temperature_c == 70.0
