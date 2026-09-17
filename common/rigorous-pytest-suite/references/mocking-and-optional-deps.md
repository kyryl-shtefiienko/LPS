# Test doubles, spying, and optional dependencies

## Prefer a real, dependency-free double over mocking the interface

When a package has multiple interchangeable backends (several ML model calculators, several
storage drivers, several parser strategies) and some backends require large optional
dependencies, write one small, real, dependency-free implementation of the same interface
(a "random"/"fake"/"in-memory" backend) and test the shared base-class logic against *it*,
not against a `MagicMock` standing in for the interface:

```python
class _EMTCalculator(BaseCalculator):
    """Minimal concrete BaseCalculator backed by a dependency-free implementation.

    Unlike the heavy real backends, this does NOT override relax()/calculate(), so it
    exercises BaseCalculator's own shared logic directly, the same way every real
    backend does.
    """
    AVAILABLE_PROPERTIES = ["energy", "forces"]
    ...
```

This catches real bugs in the shared logic that a mock — which only returns whatever you told
it to — structurally cannot catch, because the fake still runs the actual code path.

## `monkeypatch` as a spy, not a blanket replacement

When a test needs to prove *how* an internal collaborator was invoked (what kwargs a
constructor received, whether a code path was reached at all) without faking its behavior,
wrap or subclass the real thing, record the call, and delegate to the real implementation:

```python
def test_relax_applies_fix_symmetry_constraint_when_enabled(monkeypatch, perturbed_structure):
    """relax() constructs a FixSymmetry constraint with the configured symprec."""
    calls = []
    real_fix_symmetry = calculator_module.FixSymmetry

    def spy(*args, **kwargs):
        calls.append(kwargs)
        return real_fix_symmetry(*args, **kwargs)

    monkeypatch.setattr(calculator_module, "FixSymmetry", spy)

    _EMTCalculator(fix_symmetry=True, symprec=0.05, ...).relax(perturbed_structure)

    assert len(calls) == 1
    assert calls[0]["symprec"] == pytest.approx(0.05)
```

Where the code under test does an `isinstance()` check against the patched name, a bare
`lambda`/`MagicMock` won't do — subclass the real type instead, so the patched object still
*is* one, and only its constructor is intercepted:

```python
def _spy_subclass(real_type, calls):
    class _Spy(real_type):
        def __init__(self, *args, **kwargs):
            calls.append(kwargs)
            super().__init__(*args, **kwargs)
    return _Spy
```

`monkeypatch` (not `unittest.mock.patch`) is the default choice for this because it's
automatically undone at the end of the test with no `with` block or decorator needed, and it
composes cleanly with other fixtures.

## `unittest.mock` for OS/process/filesystem boundary tests

Reserve `MagicMock` / `patch` / `mock_open` for tests that are specifically about a boundary
with the outside world — a subprocess call, an environment-variable-gated code path, a file
open that you don't want to actually touch disk for:

```python
def test_missing_optional_dependency_raises_system_exit():
    """Importing the GUI module without the GUI extra installed raises SystemExit."""
    result = subprocess.run(
        [sys.executable, "-c", "import sys; sys.modules['PyQt6']=None; import yourpackage.app"],
        capture_output=True, text=True, check=False,
    )
    assert result.returncode != 0
    assert "PyQt6 is required" in result.stderr
```

This subprocess pattern is the *exception* to "never subprocess for CLI tests" (see
`cli-and-gui-testing.md`) — it's specifically testing process-level import behavior, which
can't be observed any other way once the interpreter has already imported the real dependency.

## Optional/heavy dependencies: `pytest.importorskip`

Any test module that exercises an optional extra should skip cleanly, at collection time, when
that extra isn't installed — never let `pytest tests/ -v` hard-fail in a minimal environment:

```python
"""Integration tests for the Mace-backed calculator."""

import pytest

pytest.importorskip("mace")

from yourpackage.calculators.mace import MaceCalculator
```

Put the `importorskip` call *before* the import of anything that transitively needs the
optional package, right after the standard-library/pytest imports.

## Markers: `slow` and `integration`

Register every custom marker in `pyproject.toml` (see `tooling-and-config.md`) and apply them
to the tests they actually describe:

```python
@pytest.mark.integration
def test_calculate_energy(calc, reference_structure):
    """calculate() returns a negative float energy for the reference structure."""
    ...
```

Run subsets from the command line or in CI:

```sh
uv run pytest -v -m "not slow"
uv run pytest -v -m "not integration and not slow"
```

## CI: one job per optional extra

For a package with many optional heavy backends, don't try to install all of them into one CI
job — matrix over them, one job per extra, each installing exactly that extra (plus whatever
model checkpoint or asset it needs, cached across runs) and running only the tests that need
it. This keeps the default job fast while still giving every optional code path real CI
coverage somewhere. See `references/ci-workflows.md` for the matrix shape.
