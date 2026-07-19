"""Temperature unit conversions used throughout the analysis.

The experiment records everything in degrees Celsius, but the report also
quotes a few values in Kelvin (for the absolute temperature that enters the
cooling law) and occasionally in Fahrenheit for comparison.  Keeping the
conversions in one place means the constants only have to be correct once.
"""

from __future__ import annotations

#: Absolute zero expressed in degrees Celsius.
ABSOLUTE_ZERO_C: float = -273.15

#: The canonical unit names understood by :func:`convert`.
SUPPORTED_UNITS = ("C", "K", "F")


def celsius_to_kelvin(celsius: float) -> float:
    """Convert a temperature from degrees Celsius to Kelvin."""
    return celsius - ABSOLUTE_ZERO_C


def kelvin_to_celsius(kelvin: float) -> float:
    """Convert a temperature from Kelvin to degrees Celsius."""
    return kelvin + ABSOLUTE_ZERO_C


def celsius_to_fahrenheit(celsius: float) -> float:
    """Convert a temperature from degrees Celsius to degrees Fahrenheit."""
    return celsius * 9.0 / 5.0 + 32.0


def fahrenheit_to_celsius(fahrenheit: float) -> float:
    """Convert a temperature from degrees Fahrenheit to degrees Celsius."""
    return (fahrenheit - 32.0) * 5.0 / 9.0


def kelvin_to_fahrenheit(kelvin: float) -> float:
    """Convert a temperature from Kelvin to degrees Fahrenheit."""
    return celsius_to_fahrenheit(kelvin_to_celsius(kelvin))


def fahrenheit_to_kelvin(fahrenheit: float) -> float:
    """Convert a temperature from degrees Fahrenheit to Kelvin."""
    return celsius_to_kelvin(fahrenheit_to_celsius(fahrenheit))


def _to_celsius(value: float, unit: str) -> float:
    unit = unit.upper()
    if unit == "C":
        return value
    if unit == "K":
        return kelvin_to_celsius(value)
    if unit == "F":
        return fahrenheit_to_celsius(value)
    raise ValueError(f"unknown temperature unit: {unit!r}")


def _from_celsius(value: float, unit: str) -> float:
    unit = unit.upper()
    if unit == "C":
        return value
    if unit == "K":
        return celsius_to_kelvin(value)
    if unit == "F":
        return celsius_to_fahrenheit(value)
    raise ValueError(f"unknown temperature unit: {unit!r}")


def convert(value: float, from_unit: str, to_unit: str) -> float:
    """Convert *value* from *from_unit* to *to_unit*.

    Both unit strings are case insensitive and must be one of ``"C"``,
    ``"K"`` or ``"F"``.  The conversion always routes through Celsius so that
    only the six single step conversions above have to be correct.
    """
    return _from_celsius(_to_celsius(value, from_unit), to_unit)
