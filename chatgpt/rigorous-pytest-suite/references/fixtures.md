# Fixture design

## Chain small fixtures instead of building one large one

Start from the cheapest, most atomic object and layer each derived fixture on top of the last
one, each documented with a one-line `Returns:` docstring. This lets a test ask for exactly
the layer it needs — a test of low-level parsing doesn't have to pay for (or depend on) the
full composite object's construction:

```python
"""Shared fixtures for core module tests.

Provides a fixture chain built on the FeCoCrNi reference alloy:
``composition`` -> ``thermodynamics`` -> ``predictor``.
"""

import pytest

from yourpackage.core.composition import AlloyComposition
from yourpackage.core.models import SolidSolutionPredictor
from yourpackage.core.thermodynamics import Thermodynamics

_REFERENCE_ALLOY = "FeCoCrNi"


@pytest.fixture
def composition():
    """Return an AlloyComposition for the reference alloy.

    Returns:
        Parsed composition for the reference alloy at equal molar fractions.
    """
    return AlloyComposition(_REFERENCE_ALLOY)


@pytest.fixture
def thermodynamics(composition):
    """Return a Thermodynamics instance for the reference alloy.

    Returns:
        Thermodynamics instance bound to the reference composition.
    """
    return Thermodynamics(composition)


@pytest.fixture
def predictor(composition, thermodynamics):
    """Return a SolidSolutionPredictor for the reference alloy.

    Returns:
        Predictor instance bound to the reference composition and its thermodynamics.
    """
    return SolidSolutionPredictor(composition, thermodynamics)
```

Name the reference input as a documented module-level constant (`_REFERENCE_ALLOY`, or a named
"canonical example" of whatever the domain object is) instead of a magic string repeated in
every fixture — when you need to switch the reference case, there's exactly one place to edit.

## Factory fixtures: return a callable, not a value

When tests need many *variants* of the same kind of construction, make the fixture return a
function instead of a fixed object. This avoids either a combinatorial explosion of near-
identical fixtures or tests reaching around the fixture layer to construct things by hand:

```python
@pytest.fixture
def thermo():
    """Return a factory for the thermodynamics object of an alloy.

    Returns:
        Callable taking a formula and returning its thermodynamic descriptors.
    """

    def _thermo(formula):
        return Thermodynamics(AlloyComposition(formula))

    return _thermo


def test_named_alloys(thermo):
    """A specific alloy's descriptors match the reference source."""
    calculated = thermo("CoCrFeNi")
    ...
```

The same pattern applies to fixtures that return an **assertion helper** rather than data —
useful when a nontrivial check (e.g. "the median error across these rows stays under a bound")
is needed in many test files and shouldn't be reimplemented in each one:

```python
@pytest.fixture
def assert_median_error():
    """Return a function asserting the median error between computed and published values
    stays under a bound.

    Returns:
        Callable performing the assertion.
    """

    def _assert(rows, computed, published, *, below, rows_compared=None):
        errors = [abs(computed(r) - published(r)) for r in rows if computed(r) is not None]
        if rows_compared is not None:
            assert len(errors) >= rows_compared, f"only {len(errors)} of {len(rows)} rows compared"
        median = statistics.median(errors)
        assert median < below, f"median error {median:.4f}, expected below {below}"

    return _assert
```

See `golden-and-validation-tests.md` for the full context this pattern is used in.

## `autouse=True` inside a class: parse once, assert many times

For golden-file / regression-style tests, an autouse fixture at class scope that stashes the
parsed result on `self` avoids re-parsing the same file in every single test method while
keeping each assertion in its own named, independently-readable test:

```python
class TestSampleGO:
    """Regression tests for the sample GO output file."""

    @pytest.fixture(autouse=True)
    def result(self, sample_go_path):
        """Parse the sample fixture once for every test in this class."""
        self.r = parse_go(sample_go_path)

    def test_mesh_params(self):
        """Header mesh parameters match the known-good values."""
        assert self.r.meshr == 400

    def test_convergence(self):
        """The reference calculation converged."""
        assert self.r.converged is True
```

## Scope: default to function scope; use `session` deliberately

Leave fixtures at pytest's default function scope unless construction is genuinely expensive
*and* the object is read-only in every test that uses it. Session-scoped fixtures for
foundational, immutable domain objects (a couple of canonical structures/records used
read-only across dozens of test files) go in the root `tests/conftest.py`:

```python
@pytest.fixture(scope="session")
def reference_structure() -> Structure:
    """Minimal, canonical structure used read-only across the suite."""
    return Structure(...)
```

If any test needs to *mutate* a session-scoped fixture's value, that's a bug waiting to
contaminate other tests — have that test copy it first (`.copy()`), or give it its own
function-scoped fixture instead of "fixing" the sharing after the fact.

## Where a fixture belongs

- Used by every test in the suite, cheap or immutable → `tests/conftest.py`.
- Used across multiple files within one subpackage → `tests/<subpackage>/conftest.py`.
- Used by more than one test in a single file, nowhere else → defined at the top of that
  `test_*.py` file.
- Used by exactly one test → don't make it a fixture; build the value inline in the test.
