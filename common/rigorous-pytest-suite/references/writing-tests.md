# Writing the test modules

## Module docstring

Every `test_*.py` (and every `conftest.py`) opens with a docstring summarizing what it covers,
in plain English, 1–3 sentences. This is the first thing a reader sees and should tell them
whether this is the file they're looking for without reading further:

```python
"""Tests for AlloyComposition.

Covers formula parsing, atomic-percentage normalization, pair-list
generation, and pair-percentage calculations for equimolar,
non-equimolar, and binary alloy inputs.
"""
```

## Group related cases into classes

Use `class Test<Subject><Scenario>:` to group test methods that share a scenario or fixture
context, each with its own one-line docstring. This does two things: it makes the `pytest -v`
output scannable (class name + method name reads as a sentence), and it's where class-scoped
`autouse` fixtures attach when a whole group of tests shares one expensive setup (see
`fixtures.md`).

```python
class TestAlloyCompositionEquimolar:
    """Tests for formula parsing and derived composition data."""

    def test_formula_stored(self, composition):
        """Formula attribute stores the original input string."""
        assert composition.formula == "FeCoCrNi"

    def test_alloy_element_count(self, composition):
        """Parsed alloy contains exactly four elements including all of Fe, Co, Cr, Ni."""
        assert len(composition.alloy) == 4

    def test_atomic_percentage_sums_to_one(self, composition):
        """Atomic percentages are normalized so that all fractions sum to 1.0."""
        assert sum(composition.atomic_percentage.values()) == pytest.approx(1.0, abs=1e-10)
```

Plain module-level `def test_...():` functions are fine too, and are the right choice when a
test doesn't share fixtures or context with anything else in the file — don't force a class
around a single unrelated test just for consistency.

## The docstring-per-test rule

**Every** test function or method gets a one-line docstring stating the guarantee it checks,
written as a declarative sentence in present tense — not "Test that X" (which just restates the
function name with three extra words), but the fact itself:

```python
def test_pair_list_length(self, composition):
    """Four-element alloy produces C(4, 2) = 6 unique element pairs."""
    assert len(composition.pair_list) == 6
```

If you can't compress the assertion into one honest sentence, that's a signal the test is
checking more than one thing — split it. This docstring is what shows up in `pytest -v`
output (with `-ra`/verbose reporting) in place of the bare function name, so a full test run's
output doubles as a specification document.

## Naming

`test_<subject>_<expected_outcome>` — fully descriptive, no `test_1`, `test_2`, no abbreviating
past what's still unambiguous. The name and the docstring should agree; if they say different
things, one of them is wrong.

```python
test_average_atomic_radius_cn12_fecocrni   # not test_radius_2 or test_case_a
```

## Floats: always `pytest.approx`

Never compare floats with bare `==`. Always pass an explicit tolerance — `abs=` for
comparisons near zero or with a known absolute precision, `rel=` for comparisons that scale
with magnitude — and pick the number deliberately, not by copying whatever the first passing
run happened to produce:

```python
assert composition.average_allen_electronegativity == pytest.approx(1.7925, abs=1e-4)
assert calculated.omega == pytest.approx(omega_paper, rel=0.02)
```

## Tabular cases: `@pytest.mark.parametrize`

When the same assertion shape repeats over a small table of inputs and expected outputs, use
`parametrize` instead of copy-pasted near-identical test functions:

```python
@pytest.mark.parametrize(
    "formula,delta_paper,omega_paper",
    [("CoCrFeNi", 1.06, 5.71), ("CoCrFeNiCu", 1.07, 7.36), ("CoCrFeNiAl", 5.25, 1.83)],
)
def test_named_alloys(thermo, formula, delta_paper, omega_paper):
    """Alloys the reference source reports are reproduced within tolerance."""
    calculated = thermo(formula)
    assert calculated.atomic_size_difference_cn12 == pytest.approx(delta_paper, abs=0.25)
```

## Cover edge cases as their own class or block, not as afterthought asserts

Single-element inputs, empty inputs, values with missing/`NaN` data, repeated/duplicate
entries — give each its own small fixture and its own `class Test<Subject><EdgeCase>:` rather
than bolting an extra `assert` onto an unrelated happy-path test:

```python
class TestAlloyCompositionSingleElement:
    """Tests for a single-element 'alloy'."""

    def test_pair_list_is_empty(self, single_element_composition):
        """A single-element alloy has no binary pairs."""
        assert single_element_composition.pair_list == []


class TestAlloyCompositionNaNAllenCE:
    """Tests for alloys containing elements with no reference data (e.g., lanthanides)."""

    def test_average_is_nan_when_element_missing(self):
        """The weighted average is NaN when any element lacks reference data."""
        comp = AlloyComposition("FeLa")
        assert math.isnan(comp.average_allen_electronegativity)
```

## Exception hierarchies get explicit tests

If the package defines custom exceptions, test both the inheritance relationships and that
they're catchable as their standard-library base — this is what actually guarantees
backward-compatible `except` clauses keep working:

```python
class TestExceptionHierarchy:
    """Tests for exception inheritance relationships."""

    def test_custom_error_is_key_error(self):
        """CustomLookupError is a subclass of KeyError."""
        assert issubclass(CustomLookupError, KeyError)

    def test_custom_error_catchable_as_key_error(self):
        """CustomLookupError raised by the data layer is catchable as KeyError."""
        with pytest.raises(KeyError):
            raise CustomLookupError("missing-key")
```

## Registries / plugin-discovery systems: test the live registry, not a hardcoded list

If the package exposes a plugin/entry-point registry, complement any hardcoded
"these names should exist" check with one that walks the *live* registry, so a renamed class
or a typo'd entry-point target fails loudly even for a name the hardcoded list doesn't cover:

```python
def test_every_registered_name_resolves():
    """Every entry-point-registered name resolves to a real, loadable class."""
    for name in list_registered():
        with contextlib.suppress(TypeError):  # TypeError = needs constructor args, that's fine
            get_registered(name)
```
