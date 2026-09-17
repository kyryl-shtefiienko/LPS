# Testing a CLI and a GUI

## CLI: in-process, never subprocess

Use the framework's own test runner (`typer.testing.CliRunner`, or Click's equivalent) so
invocations run in-process — no subprocess spawn cost, and `exit_code`, `output`, `stdout`,
and `stderr` are all available separately for assertions:

```python
"""Tests for CLI subcommands.

Uses ``typer.testing.CliRunner`` to invoke commands without spawning a subprocess.
"""

from typer.testing import CliRunner

from yourpackage.cli import app

runner = CliRunner()


class TestSingleSearch:
    """Tests for the ``single`` subcommand."""

    def test_valid_input_exits_zero(self):
        """A recognized input returns exit code 0."""
        result = runner.invoke(app, ["single", "FeCoCrNi"])
        assert result.exit_code == 0

    def test_invalid_input_exits_nonzero(self):
        """An unrecognized input causes a non-zero exit code."""
        result = runner.invoke(app, ["single", "Xx"])
        assert result.exit_code != 0
```

## Test every output mode, not just the default

If the CLI has a machine-readable mode (`--json`) alongside a human-readable default, test
both explicitly, and test that they don't leak into each other (no human labels in `--json`
output, no JSON where a human expects a table):

```python
def test_json_output_is_valid_json(self):
    """--json output is a valid JSON object."""
    result = runner.invoke(app, ["single", "FeCoCrNi", "--json"])
    data = json.loads(result.output)
    assert isinstance(data, dict)

def test_json_output_no_human_readable_labels(self):
    """--json output does not include human-readable property labels."""
    result = runner.invoke(app, ["single", "FeCoCrNi", "--json"])
    assert "Density" not in result.output
```

## Test flag validation and mutual exclusivity explicitly

```python
def test_json_and_csv_flags_are_mutually_exclusive(self):
    """Passing both --json and --csv causes a non-zero exit code."""
    result = runner.invoke(app, ["range", ..., "--json", "--csv"])
    assert result.exit_code != 0
```

## Filesystem-touching CLI tests: `tempfile`/`tmp_path`, always cleaned up

```python
def test_valid_csv_exits_zero(self):
    """A CSV file containing valid input runs without error."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        f.write("composition\nFeCoCrNi\n")
        tmp_path = f.name
    try:
        result = runner.invoke(app, ["csv", tmp_path])
        assert result.exit_code == 0
    finally:
        Path(tmp_path).unlink()
```

`tmp_path` (the built-in pytest fixture) is equally valid and slightly less boilerplate when
you don't need a specific suffix/mode combination — either is fine, but be consistent within
a file.

## Test bad-input handling doesn't crash, it degrades gracefully

```python
def test_bad_row_is_skipped_not_crash(self):
    """A CSV with one invalid row in the middle does not crash; remaining rows still appear."""
    ...
    assert result.exit_code == 0
    assert "FeCoCrNi" in result.output
    assert "FeNi" in result.output
```

## GUI: gate the whole module, run offscreen in CI

```python
"""Tests for the GUI module.

All tests are skipped when the GUI toolkit is not installed or no display is available.
"""

import pytest

PyQt6 = pytest.importorskip("PyQt6", reason="PyQt6 not installed")

from PyQt6 import QtWidgets
from yourpackage.app import MainWindow
```

In CI, set the toolkit's offscreen platform so no real display is required:

```yaml
- name: Run tests
  env:
    QT_QPA_PLATFORM: offscreen
  run: uv run pytest tests/ -v
```

## Testing the "optional dependency missing" import guard

If importing the GUI (or another optional-heavy) module without its extra installed is
supposed to fail loudly (`SystemExit` with a clear message) rather than raising a confusing
`ImportError` deep in a third-party stack, test that behavior via a real subprocess with the
dependency faked as absent — this is the one place a subprocess is the right tool, because
you're testing process-level import behavior that can't be observed once the real interpreter
has already imported the thing:

```python
def test_missing_dependency_raises_system_exit(self):
    """Importing the GUI module without the toolkit available raises SystemExit."""
    result = subprocess.run(
        [sys.executable, "-c",
         "import sys; sys.modules['PyQt6']=None; sys.modules['PyQt6.QtCore']=None; "
         "sys.modules['PyQt6.QtGui']=None; sys.modules['PyQt6.QtWidgets']=None; "
         "import yourpackage.app"],
        capture_output=True, text=True, check=False,
    )
    assert result.returncode != 0
    assert "PyQt6 is required for GUI mode." in result.stderr
```
