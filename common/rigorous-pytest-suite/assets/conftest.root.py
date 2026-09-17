"""Shared, session-scoped fixtures for the whole test suite.

Only put a fixture here if it's (a) used across more than one subpackage's tests, and
(b) cheap enough to be safely reused read-only across the whole session. Anything narrower
belongs in a subpackage's own conftest.py instead — see references/fixtures.md.
"""

from __future__ import annotations

import pytest

from yourpackage.models import CanonicalExample


@pytest.fixture(scope="session")
def canonical_example() -> CanonicalExample:
    """Minimal, canonical example object used read-only across the suite.

    Returns:
        A small, well-understood instance suitable as a default test input.
    """
    return CanonicalExample(...)


@pytest.fixture(scope="session")
def alternate_example() -> CanonicalExample:
    """A second canonical example, distinct enough to catch cases the first one wouldn't.

    Returns:
        A second, deliberately different instance for comparison/edge-case tests.
    """
    return CanonicalExample(...)
