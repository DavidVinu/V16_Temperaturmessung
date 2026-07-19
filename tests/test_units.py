"""Tests for :mod:`tempkit.units`."""

import math

import pytest

from tempkit import units


def test_celsius_kelvin_roundtrip():
    for c in (-273.15, -40.0, 0.0, 21.5, 100.0):
        k = units.celsius_to_kelvin(c)
        assert math.isclose(units.kelvin_to_celsius(k), c, abs_tol=1e-9)


def test_celsius_fahrenheit_reference_points():
    assert math.isclose(units.celsius_to_fahrenheit(0.0), 32.0)
    assert math.isclose(units.celsius_to_fahrenheit(100.0), 212.0)
    assert math.isclose(units.fahrenheit_to_celsius(32.0), 0.0)
    assert math.isclose(units.fahrenheit_to_celsius(212.0), 100.0)


def test_minus_forty_is_the_same_in_both_scales():
    assert math.isclose(units.celsius_to_fahrenheit(-40.0), -40.0)


def test_absolute_zero_in_kelvin_is_zero():
    assert math.isclose(units.celsius_to_kelvin(units.ABSOLUTE_ZERO_C), 0.0)


def test_convert_routes_through_celsius():
    assert math.isclose(units.convert(0.0, "C", "K"), 273.15)
    assert math.isclose(units.convert(273.15, "K", "C"), 0.0)
    assert math.isclose(units.convert(100.0, "C", "F"), 212.0)
    assert math.isclose(units.convert(212.0, "F", "K"), 373.15)


def test_convert_is_case_insensitive():
    assert math.isclose(units.convert(0.0, "c", "k"), 273.15)


def test_convert_rejects_unknown_units():
    with pytest.raises(ValueError):
        units.convert(0.0, "C", "R")
    with pytest.raises(ValueError):
        units.convert(0.0, "Q", "C")
