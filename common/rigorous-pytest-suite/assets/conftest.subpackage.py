"""Shared fixtures for <subpackage> module tests.

Provides a fixture chain: ``base_object`` -> ``derived_object`` -> ``composite_object``,
plus a ``factory`` fixture for tests that need several variants of ``base_object``.
"""

from __future__ import annotations

import pytest

from yourpackage.subpackage.base import BaseObject
from yourpackage.subpackage.composite import CompositeObject
from yourpackage.subpackage.derived import DerivedObject

_REFERENCE_INPUT = "reference-value"


@pytest.fixture
def base_object() -> BaseObject:
    """Return a BaseObject built from the module's reference input.

    Returns:
        A BaseObject constructed from the fixed reference input.
    """
    return BaseObject(_REFERENCE_INPUT)


@pytest.fixture
def derived_object(base_object: BaseObject) -> DerivedObject:
    """Return a DerivedObject built on top of ``base_object``.

    Returns:
        A DerivedObject wrapping the reference BaseObject.
    """
    return DerivedObject(base_object)


@pytest.fixture
def composite_object(base_object: BaseObject, derived_object: DerivedObject) -> CompositeObject:
    """Return a CompositeObject combining ``base_object`` and ``derived_object``.

    Returns:
        A fully assembled CompositeObject for the reference input.
    """
    return CompositeObject(base_object, derived_object)


@pytest.fixture
def base_object_factory():
    """Return a factory for constructing a BaseObject from an arbitrary input.

    Use this instead of ``base_object`` when a test needs several distinct variants
    rather than the single fixed reference input.

    Returns:
        Callable taking an input value and returning a BaseObject built from it.
    """

    def _factory(value: str) -> BaseObject:
        return BaseObject(value)

    return _factory
