---
name: dogusariturk-python-style
description: Reference Python style guide reverse-engineered from Doguhan Sariturk's (github.com/dogusariturk) real production repositories (HEACalculator, MaterialsFramework, PhaseForgePlus). Use this whenever writing, generating, reviewing, refactoring, or cleaning up ANY Python code for this user — scripts, modules, packages, CLIs, tests, or turning a vibe-coded/notebook-style script into something real — even if the user never mentions style explicitly. Covers project layout (src-layout, uv, ruff, ty, pre-commit, pytest), short single-responsibility files, typing, Google-style docstrings with units and literature references, cached_property for lazy derived attributes, narrow custom exceptions, named unit-conversion constants instead of magic numbers, composition over deep inheritance, registries for optional heavy dependencies, and multiprocessing worker conventions. Where this conflicts with a generic assistant default, this style is correct and the generic default is wrong — apply it before finalizing any Python output for this user. Where it conflicts instead with an established convention already in play for the current codebase (an existing project-scoped skill, or a style already consistently used in the repo being edited), that more specific convention wins on the point of conflict per skill-hierarchy; this skill still governs everywhere that convention doesn't address.
---

# Write Python like dogusariturk

This is not a generic style guide. It is reverse-engineered from real, shipped
code — HEACalculator, MaterialsFramework, and PhaseForgePlus by Doguhan
Sariturk (github.com/dogusariturk) — and it is the standard this user wants
applied to their own Python. When any instinct here conflicts with a more
"generic assistant" habit (bare `except Exception`, numpy-style docstrings,
`Optional[X]`, inline magic numbers, one giant script), **this document wins.
Follow it, don't hedge toward the generic habit "for safety."**

This authority is over generic defaults, not over a more specific convention.
If the current codebase already has its own established style (a project-scoped
skill, an existing lint config, a pattern used consistently throughout the repo
being edited), that convention is more specific than this one and wins on the
exact point where they disagree — see `skill-hierarchy`. Everywhere that
convention is silent, this document still applies.

The examples below are written fresh to illustrate each pattern — they are
not copied from his repos. For README / repo-scaffolding concerns (Quick
Start bloat, CITATION.cff, unpinned environments) see the
`matsci-python-antipatterns` and `github-repo-standards` skills; this skill
is about the code itself.

## 1. Project & tooling baseline

Every real project is `src`-layout, `uv`-managed, `ruff`-linted, `ty`-typed,
and `pre-commit`-enforced. For anything bigger than a one-off script, scaffold:

```
project/
├── src/project_name/
│   ├── __init__.py
│   └── ...
├── tests/
│   └── test_*.py
├── pyproject.toml
├── uv.lock
└── .pre-commit-config.yaml
```

`pyproject.toml` — adapt, don't paste blindly:

```toml
[tool.ruff]
line-length = 130
force-exclude = true

[tool.ruff.lint]
select = ["A", "B", "C4", "D", "E", "ERA", "F", "FA", "I", "ICN", "N", "PL", "PTH", "Q", "SIM", "TC", "UP", "W"]
ignore = ["E501", "PLR0913", "PLR2004"]  # long lines and magic-value comparisons are judgment calls, not lint failures
pydocstyle.convention = "google"

[tool.ruff.format]
quote-style = "double"

[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["src"]
```

`.pre-commit-config.yaml` runs, in order: `uv lock`, `ruff check --fix`,
`ruff format`, a type check (`ty` or `mypy`), then the standard hygiene hooks
(trailing-whitespace, end-of-file-fixer, check-yaml/toml, check-merge-conflict).

CLIs use **typer**, not bare `argparse`. Docs (when the project has them) are
**mkdocs-material** + **mkdocstrings**, not a hand-written API reference.

Don't scaffold all of this for a 20-line throwaway script — but even a small
script still gets functions, type hints, and a docstring. See §12.

## 2. File length & module boundaries

Files are short. This was checked directly: across all three source repos,
counting every non-test, non-`__init__.py`, non-generated `.py` file (116
files), the median is **~82 lines**, the mean **~188**, and three-quarters of
them are under **170 lines**. Roughly two-thirds are 100 lines or shorter.

The handful of outliers prove the rule rather than break it. The two files
over 3,000 lines are PyQt GUI pages (`parametersPage.py`,
`batchCalculationsPage.py`) — dense widget-wiring code, a different genre
from computational logic — and the one file over 17,000 lines
(`HEACalculator_rc.py`) is Qt's auto-generated resource-compiler output,
never hand-written and never a model for anything. Excluding those, his
largest genuinely hand-written *logic* modules — a stability-map calculator,
a thermodynamics module, an MD driver, an elastic-constants module — all land
in the **500–700 line** range, and none of his computational code goes higher
than that.

Apply this as a real constraint, not just an aspiration:

- **One file, one responsibility.** A module name is a concept (one model,
  one calculator, one data source, one CLI command group) — not `utils.py`
  or `helpers.py` collecting whatever didn't have an obvious home.
- **Write toward the short end.** Most modules should read like his
  median — well under 200 lines. A file only grows past that because its
  logic genuinely earns the length, not because unrelated concerns piled up
  in it.
- **500–700 hand-written logic lines is the observed ceiling**, not a hard
  cutoff — but treat a module crossing it as a prompt to split by concept
  (pull out a class, a submodule, or a sibling module in the same package)
  rather than a reason to keep appending.
- **Judge by logic, not by line count alone.** A thoroughly Google-docstringed
  module (§4) legitimately runs longer than an undocumented one covering the
  same behavior — don't trim docstrings or collapse whitespace just to hit a
  number. Weigh what the file *does*.
- **Recognized exceptions announce themselves**: a GUI layout page wiring up
  many widgets, or a literature/reference-data table, can legitimately run
  long. Auto-generated code (a Qt `*_rc.py`, a protobuf stub) isn't part of
  this convention at all — it's machine output, not a style to emulate or to
  count against a hand-written module's budget.

## 3. Typing & imports

- Modern builtin generics and unions everywhere: `list[str]`, `dict[str, float]`,
  `X | None`. Never `typing.List`, `typing.Dict`, `typing.Optional`.
- `from __future__ import annotations` at the top of any module that has
  forward references or wants the modern union syntax guaranteed.
- Anything imported **only** for type annotations goes behind
  `if TYPE_CHECKING:` — keeps runtime imports light and breaks import cycles:

```python
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from myproject.core.composition import AlloyComposition


class Thermodynamics:
    def __init__(self, composition: AlloyComposition) -> None:
        self._c = composition
```

- Import order (ruff `I` / isort): stdlib, blank line, third-party, blank
  line, local package — always, no manual reordering later.

## 4. Docstrings

**Google convention, always** (`pydocstyle.convention = "google"`). One-line
summary, blank line, then `Args:` / `Returns:` / `Raises:` / `Note:` /
`References:` as needed. This applies even to small private (`_leading_underscore`)
helpers — "it's internal" is not a reason to skip the docstring.

- State physical units explicitly wherever they matter (`pm`, `kJ/mol`,
  `eV`, `K`) — in the `Returns:`/`Args:` line, not just in a variable name.
- When a formula comes from a paper, cite it in a `References:` section.
- Use raw strings (`r"""..."""`) for docstrings containing LaTeX/math.

```python
def average_radius(fractions: dict[str, float], radii: dict[str, float]) -> float:
    """Composition-weighted average atomic radius.

    Args:
        fractions (dict[str, float]): Atomic fraction per element symbol.
        radii (dict[str, float]): Atomic radius per element symbol, in pm.

    Returns:
        Composition-weighted average radius in pm.
    """
    return sum(frac * radii[elm] for elm, frac in fractions.items())
```

## 5. Class design

- **`functools.cached_property` for any derived attribute that's expensive
  or just non-trivial to compute.** Don't compute everything eagerly in
  `__init__`, and don't write a `calculate()` method that mutates a pile of
  instance attributes. Let each property compute itself lazily, once.
- **Composition over deep inheritance.** A class that needs another object's
  services stores it as a single-underscore-prefixed attribute (`self._c`,
  `self._t`) and calls into it — it doesn't inherit from it or reach into a
  God-object.
- `__init__` does the minimum: store what was passed in, validate hard
  invariants, nothing else. One-line docstring is fine there; the real
  documentation lives on the properties.

```python
class SolidSolutionPredictor:
    """Applies formation criteria to an alloy composition.

    Args:
        composition (AlloyComposition): Parsed alloy composition.
        thermodynamics (Thermodynamics): Thermodynamics calculator for the same composition.
    """

    def __init__(self, composition: AlloyComposition, thermodynamics: Thermodynamics) -> None:
        """Initialize with a parsed composition and its thermodynamics calculator."""
        self._c = composition
        self._t = thermodynamics

    @cached_property
    def microstructure(self) -> str:
        """Expected crystal structure based on VEC.

        Returns:
            One of "FCC", "BCC", "HCP", or "BCC+FCC".
        """
        ...
```

## 6. Exceptions

Define **narrow, named exceptions subclassing the closest builtin**, with
nothing but a one-line docstring — not a bare `raise ValueError(...)` and not
one giant generic `AppError`:

```python
class MissingPairDataError(KeyError):
    """Raised when a binary element pair has no entry in a data table."""


class ElementNotFoundError(KeyError):
    """Raised when an element symbol has no entry in the element database."""
```

Catch narrow-to-broad, most specific first, and when re-raising at a
boundary (e.g. a CLI), chain with `from e` and add a human-readable message:

```python
except ElementNotFoundError as e:
    raise typer.BadParameter(f"Unknown element in '{alloy}': {e}") from e
except Exception as e:  # generic fallback, last, still explicit
    raise typer.BadParameter(f"Could not process '{alloy}': {e}") from e
```

## 7. Constants over magic numbers

Any non-obvious numeric literal — especially a unit conversion — gets a
named `_UPPER_SNAKE` constant with an inline comment showing the conversion,
defined right where it's used (module-level if shared, local if not):

```python
_J_PER_MOL_TO_MEV_PER_ATOM = 0.0103642688  # 1 J/mol = 0.010364 meV/atom
```

Module-wide physical constants live once near the top of the module:

```python
GAS_CONSTANT = 8.314462618  # J / (mol*K)
```

## 8. Readability details that are deliberate, not accidental

- `zip(a, b, strict=True)` whenever two sequences are assumed equal length —
  catches silent truncation bugs.
- `pathlib.Path`, never `os.path`.
- Long boolean/ternary expressions are wrapped across lines in parens for
  readability, even where the linter would allow a long single line:

```python
return (
    "Solid Solution"
    if lower_bound < min_formation_enthalpy and max_formation_enthalpy < threshold
    else "Multiple Phases"
)
```

- Comments explain *why*, not *what*. If a comment just restates the code,
  delete it and improve a name instead.

## 9. Multiprocessing workers

Worker functions passed to `ProcessPoolExecutor` are:
- defined at **module level** (must be picklable — no closures/lambdas/nested defs),
- fully docstringed, noting they're a pool worker,
- lazy-importing anything heavy inside the function body when that avoids
  paying import cost in the parent process, with a comment saying why,
- returning `(result, error_message)` tuples instead of letting exceptions
  cross the process boundary:

```python
def _range_worker(formula: str) -> tuple[list | None, str | None]:
    """Compute results for a single formula.

    Intended as a ProcessPoolExecutor worker; imports lazily so worker
    processes don't pay import cost they don't need.

    Returns:
        (result, None) on success, or (None, error_message) on failure.
    """
    from myproject.core import Calculator

    try:
        return Calculator(formula).get_list(), None
    except Exception as e:
        return None, str(e)
```

## 10. Optional heavy dependencies: lazy registries

When a package offers many interchangeable backends and each backend has its
own heavy optional dependency (an ML framework, a simulation engine), don't
import them all eagerly. Map name → `(module, attr)` and resolve lazily via
`__getattr__`, so `import mypackage` stays cheap and a user only pays for the
backend they actually use:

```python
_BACKEND_MAP: dict[str, tuple[str, str]] = {
    "FooBackend": ("mypackage.backends.foo", "FooBackend"),
    "BarBackend": ("mypackage.backends.bar", "BarBackend"),
}


def __getattr__(name: str) -> type:
    """Lazily import and return a backend class by name."""
    if name not in _BACKEND_MAP:
        raise AttributeError(name)
    module_name, attr = _BACKEND_MAP[name]
    import importlib

    return getattr(importlib.import_module(module_name), attr)
```

## 11. Tests

- `unittest.TestCase`-style classes grouped by the function/class under test
  (`class TestFindAllComps(TestCase):`), run through pytest.
- One test method = one behavior, with a one-line docstring stating exactly
  what it proves (not "test 1", not restating the method name).
- `pytest.approx(...)` for any float comparison.
- Cover edge cases explicitly as separate named tests: empty input, boundary
  values, fractional/unusual step sizes — not just the happy path.

```python
class TestAverageRadius(TestCase):
    """Tests for the `average_radius` helper."""

    def test_single_element_returns_its_radius(self):
        """A one-element composition returns that element's own radius."""
        assert average_radius({"Fe": 1.0}, {"Fe": 126.0}) == pytest.approx(126.0)
```

## 12. Anti-patterns to flag and fix

When reviewing existing ("vibe-coded") Python against this style, these are
the recurring problems to call out and fix:

1. **Top-to-bottom script, no functions/classes.** Even a one-off analysis
   script gets broken into functions with type hints and docstrings — it
   should be importable and testable, not just runnable.
2. **Bare `except:` or `except Exception:`** with no narrower exception, no
   re-raise, no logging — silently swallowing errors.
3. **Magic numbers inline** with no named constant, especially unit
   conversions.
4. **Mixed or missing docstring style** — inconsistent numpy/Google/none.
   Standardize on Google, everywhere, including private helpers.
5. **`Optional[X]`, `List[X]`, `Dict[X, Y]`** instead of `X | None`, `list[X]`,
   `dict[X, Y]`.
6. **Deep inheritance chains or god objects** where composition (`self._x`
   holding a collaborator) would be simpler and more testable.
7. **Eager, unnecessary imports of heavy optional dependencies** at module
   top-level when a lazy registry (§10) would do.
8. **`os.path` instead of `pathlib.Path`.**
9. **One test that asserts five unrelated things** instead of small, named,
   single-purpose tests.
10. **A single file quietly absorbing unrelated responsibilities** well past
    the ~500–700 hand-written-logic-line ceiling (§2) instead of being split
    by concept — a `utils.py` that keeps growing is the classic shape of this.

## 13. Note on personal metadata

His files carry `__author__` / `__email__` module headers — that's a
personal-project convention tied to *his* identity, not a code-quality rule.
Don't stamp his name/email into this user's code. If the user wants an
attribution header pattern, use *their* name/email; otherwise just skip it.

## 14. Before finalizing any Python for this user

Run this checklist over what you're about to output:

- [ ] `list[X]` / `dict[X, Y]` / `X | None`, not `typing.List`/`Optional`
- [ ] Google-style docstring on every public **and** private function/class,
      with units stated where relevant
- [ ] Derived/expensive attributes are `cached_property`, not eager `__init__`
      work or a mutating `calculate()` method
- [ ] Narrow custom exception(s) instead of bare `ValueError`/`Exception`
      where the caller might reasonably want to catch a specific failure
- [ ] No unexplained magic numbers — named constant + comment
- [ ] `pathlib.Path`, `zip(..., strict=True)`
- [ ] Multiprocessing workers are module-level, docstringed, return
      `(result, error)` tuples
- [ ] It's a real module with functions/classes, not a flat script — even
      for something small
- [ ] No file is quietly carrying multiple unrelated responsibilities past
      the observed ~500–700 hand-written-logic-line ceiling (§2) — split by
      concept before it gets there
