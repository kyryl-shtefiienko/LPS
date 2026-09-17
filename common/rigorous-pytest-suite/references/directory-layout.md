# Directory layout: `tests/` mirrors `src/`

## The core rule

For every subpackage under `src/yourpackage/`, there is a matching directory under `tests/`.
For every module inside it, there is a matching `test_<module>.py`. Given a source file's
path, you can compute its test file's path by substitution alone — no searching required.

```
src/yourpackage/                    tests/
├── core/                           ├── core/
│   ├── composition.py              │   ├── conftest.py
│   ├── converter.py                │   ├── test_composition.py
│   └── models.py                   │   └── test_converter.py, test_models.py
├── calculators/                    ├── calculators/
│   ├── registry.py                 │   ├── conftest.py            (if needed)
│   ├── mace.py                     │   ├── test_registry.py
│   └── chgnet.py                   │   ├── test_mace.py
│                                   │   └── test_chgnet.py
├── cli.py                          ├── test_cli.py
├── app.py            (GUI)         ├── test_app.py
├── __main__.py                     ├── test_main.py
├── exceptions.py                   ├── test_exceptions.py
└── utils.py                        └── test_utils.py
tests/conftest.py                   (root-level, cross-cutting fixtures)
```

Modules that aren't tied to one subpackage — the CLI entrypoint, a GUI module, the package's
custom exception classes, a grab-bag `utils.py` — get a top-level `test_*.py` sitting directly
in `tests/`, not nested under a subpackage directory that doesn't otherwise exist.

## `conftest.py` at every level that needs it

- `tests/conftest.py` — fixtures shared across the *whole* suite: expensive or foundational
  objects most test files will want (e.g. a couple of canonical input structures/records),
  usually `scope="session"` since they're read-only.
- `tests/<subpackage>/conftest.py` — fixtures specific to that subpackage: a fixture chain
  built from that subpackage's own domain objects. Don't hoist a subpackage-local fixture to
  the root just to avoid one extra file; keep fixtures at the narrowest scope that uses them
  so a reader of `tests/calculators/conftest.py` sees everything relevant to calculators and
  nothing else.
- A **class-local** fixture (defined at the top of one `test_*.py` file, not in `conftest.py`)
  when only that one file's tests need it — most fixtures should live in the narrowest place
  that's still shared by more than one test function in the same file.

## Real sample data lives inside `tests/`

If the package parses or produces real file formats, keep small representative samples under
`tests/data/` (or `tests/fixtures/`), organized to mirror the *pipeline stage* they represent
rather than dumped in one flat folder:

```
tests/data/
├── in/        # sample inputs the tool consumes
├── out/       # the tool's own output on those inputs — golden files for regression tests
└── data/      # raw third-party reference files unrelated to the tool's own I/O
```

Point fixtures at these paths rather than hardcoding path strings inside test functions:

```python
SAMPLES = Path(__file__).parent / "data"

@pytest.fixture
def fe_go() -> Path:
    """Return the sample Fe GO output path.

    Returns:
        The path to the fixture file.
    """
    return SAMPLES / "out" / "fe"
```

## Large reference tables are Python, not JSON/CSV

When a test module needs a substantial table of reference data (transcribed literature values,
a large parametrize table), put it in its own module colocated with the tests
(`tests/<subpackage>/published_data.py`) and import it, rather than embedding it inline or
loading it from a data file at collection time:

```python
from published_data import SOURCE_2012_TABLE_1 as TABLE
```

This keeps the data typed, diffable, documented (a module docstring citing the source), and
importable — a plain data file gives you none of that, and inlining a 100-row table inside a
test function buries the actual assertions under noise.

## `__init__.py` in `tests/`

Some projects in this style include `tests/__init__.py` (and one per subpackage), others
don't — pytest's own test discovery doesn't require it under `testpaths`. Pick one convention
and apply it consistently within a project; don't mix. If the project already has one way,
follow it rather than "fixing" it as a drive-by change.
