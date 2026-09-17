"""Tests for yourpackage.subpackage.base.BaseObject.

Covers construction from the reference input, derived properties, and edge cases
(empty input, a second distinct example, and invalid input).
"""

from __future__ import annotations

import math

import pytest

from yourpackage.subpackage.base import BaseObject
from yourpackage.subpackage.exceptions import InvalidInputError


class TestBaseObjectConstruction:
    """Tests for basic construction and stored attributes."""

    def test_stores_input_value(self, base_object):
        """The constructor stores the input value unchanged."""
        assert base_object.value == "reference-value"

    def test_derived_property_is_float(self, base_object):
        """The derived numeric property is always a float."""
        assert isinstance(base_object.derived_quantity, float)

    def test_derived_property_matches_expected(self, base_object):
        """The derived quantity for the reference input matches its known value."""
        assert base_object.derived_quantity == pytest.approx(1.2345, abs=1e-4)


class TestBaseObjectFactoryVariants:
    """Tests exercising several distinct inputs via the factory fixture."""

    @pytest.mark.parametrize(
        "value,expected",
        [
            ("case-a", 1.0),
            ("case-b", 2.5),
            ("case-c", 0.0),
        ],
    )
    def test_derived_quantity_for_input(self, base_object_factory, value, expected):
        """Each named case's derived quantity matches its known value."""
        obj = base_object_factory(value)
        assert obj.derived_quantity == pytest.approx(expected, abs=1e-6)


class TestBaseObjectEdgeCases:
    """Tests for boundary and error-path inputs."""

    def test_empty_input_raises(self):
        """An empty input string raises InvalidInputError."""
        with pytest.raises(InvalidInputError):
            BaseObject("")

    def test_missing_reference_data_is_nan(self, base_object_factory):
        """An input with no reference data yields NaN, not an exception."""
        obj = base_object_factory("unknown-case")
        assert math.isnan(obj.derived_quantity)


class TestBaseObjectExceptionHierarchy:
    """Tests for the module's custom exception, kept alongside the code it protects."""

    def test_invalid_input_error_is_value_error(self):
        """InvalidInputError is catchable as ValueError."""
        assert issubclass(InvalidInputError, ValueError)

    def test_invalid_input_error_stores_offending_value(self):
        """InvalidInputError stores the offending value as its first argument."""
        exc = InvalidInputError("bad-value")
        assert exc.args[0] == "bad-value"
