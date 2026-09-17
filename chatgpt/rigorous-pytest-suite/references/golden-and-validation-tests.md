# Golden-file regression tests and validation-against-a-source tests

These two patterns go beyond ordinary unit testing: one checks that a real-world parser keeps
agreeing with itself over time, the other checks that a model or algorithm still agrees with
an external, trusted source. Use them whenever the package's job is to parse real external
data or to reproduce a known quantitative result.

## Golden-file regression tests

Bundle small, real, representative sample files under `tests/data/` (see
`directory-layout.md` for the recommended `in/`/`out/` split), point fixtures at them, and
parse once per test class via an `autouse` fixture — then assert on many individually-named
fields, each its own test:

```python
"""Tests for the sample Fe BCC output file."""

class TestFeGO:
    """Regression tests for the sample Fe BCC GO output."""

    @pytest.fixture(autouse=True)
    def result(self, fe_go_path):
        """Parse the Fe GO fixture once for every test in this class."""
        self.r = parse_go(fe_go_path)

    def test_mesh_params(self):
        """Header mesh parameters match the known-good values."""
        assert self.r.meshr == 400
        assert self.r.mse == 35

    def test_convergence(self):
        """The reference calculation converged in the expected number of iterations."""
        assert self.r.converged is True
        assert len(self.r.iterations) == 38

    def test_final_value(self):
        """The final computed value matches the known-good result within tolerance."""
        assert self.r.iterations[-1].moment == pytest.approx(2.1686, rel=1e-3)
```

Why this shape: one parse per class (not per test) keeps the suite fast even with many
assertions on the same parsed object, while still giving each field its own named, isolated
test — if `test_convergence` fails, you know instantly which guarantee broke, instead of
untangling one giant `test_parse_everything` failure.

Add one such class per representative sample file (different lattice types, different element
counts, a deliberately non-converged case, an edge case like a missing block) — breadth across
realistic inputs matters more here than depth on any single one.

## Literature / scientific-validation tests

When the package implements a published model, formula, or algorithm, don't just test it
against values you computed with the same code (that only proves the code is consistent with
itself). Transcribe the *source's own* reported numbers into a typed, documented Python
module colocated with the tests:

```python
"""Reference table from Source et al., Journal XX (Year) pp-pp, Table 1."""

SOURCE_2012_TABLE_1 = [
    {"formula": "CoCrFeNi", "delta": 1.06, "omega": 5.71, "structure": "solid solution"},
    {"formula": "CoCrFeNiCu", "delta": 1.07, "omega": 7.36, "structure": "solid solution"},
    # ... every row from the paper's table, transcribed exactly
]
```

Then assert **aggregate error bounds**, not exact equality — these are physically- or
empirically-derived approximations being checked against independently measured/reported
numbers, so some spread is expected and the *bound* on that spread is the actual spec:

```python
def test_reproduces_reference_table(thermo, assert_median_error):
    """Computed values track the published column within the stated bound."""
    assert_median_error(
        TABLE,
        computed=lambda row: thermo(row["formula"]).some_value,
        published=lambda row: row["delta"],
        below=0.30,
        rows_compared=125,   # guards against a bug that silently empties the comparison
    )
```

The `rows_compared` guard matters: an aggregate-error assertion evaluated over zero
successfully-computed rows trivially "passes" with no information content — always assert a
minimum sample size alongside the error bound.

For classification-style validation (does the model call something "solid solution" vs.
"intermetallic" the way the source does), check recall **per class**, not just overall
accuracy, so a criterion can't pass by always predicting the majority label:

```python
def test_classification_matches_reference(assert_classification):
    """The criterion reproduces the source's phase labels with acceptable recall per class."""
    assert_classification(
        TABLE,
        predict=lambda row: predictor(row["formula"]).verdict,
        expected=lambda row: row["is_solid_solution"],
        overall=0.80, solid_solution=0.75, intermetallic=0.70,
        rows_scored=125,
    )
```

## When to reach for exact equality vs. an aggregate bound

- Exact (`==`) or tight `pytest.approx`: the code's own deterministic output on a fixed input
  (a parser's field values, a formula's output for a hand-verified case).
- Aggregate bound (median/mean error under a threshold, recall above a bound, over a named
  minimum sample size): the code's output compared against an *external* source of truth where
  some disagreement is expected and quantifying "how much" is the actual point of the test.

Getting this distinction right is what keeps validation tests meaningful instead of either
too brittle (failing on noise) or too loose (never catching a real regression).
