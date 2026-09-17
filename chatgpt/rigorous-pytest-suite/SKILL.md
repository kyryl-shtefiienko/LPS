---
name: rigorous-pytest-suite
description: 'Sets up and writes comprehensive, rigorous pytest test suites for Python projects: project tooling (uv, ruff, ty, prek), a tests/ tree mirroring src/ 1:1, conftest.py fixture chains, one test file per module with a docstring on every test stating what it proves, pytest.approx for floats, parametrize tables, slow/integration markers, importorskip for optional heavy dependencies, monkeypatch "spy" patterns instead of blanket mocking, CliRunner-based CLI testing, gated GUI testing, golden-file regression tests, and statistical literature-validation tests for scientific/numerical code. Also scaffolds matching GitHub Actions CI (OS x Python-version matrix, separate lint job, dependabot). Use whenever the user asks to write tests, add a test suite, set up pytest, create conftest.py or fixtures, add CI testing workflows, test a CLI or GUI, or make an existing suite more thorough and disciplined - even a bare "add tests" or "set up testing".'
---

# Rigorous Pytest Suite

## Where this comes from

This skill distills a testing house-style that shows up nearly identically across a body of
actively-maintained, real-world Python packages (scientific/engineering tooling with CLIs, a
GUI, file parsers, and numerical models). It isn't one person's one-off preference on one
repo — the same tooling, directory shape, fixture patterns, and CI setup recur project after
project, which is what makes it worth encoding as a reusable standard rather than copying a
single example. Everything below generalizes to any Python codebase, not just scientific ones.

## Philosophy

A test suite built this way is written to be **read**, not just run. Every test's docstring is
a one-line spec sentence; a `pytest tests/ -v` run reads almost like a table of contents of the
package's guarantees. Tooling choices (uv, ruff, ty, prek) exist to make the suite fast and
reproducible so the discipline doesn't decay under time pressure. CI mirrors local dev exactly
— same `uv sync` command, same pytest invocation — so "works on my machine" isn't a failure
mode. Explain the *why* to yourself as you write each test; that's what keeps the suite from
turning into brittle assertions nobody trusts.

## The whole picture, at a glance

| Convention | In short |
|---|---|
| Layout | `tests/` mirrors `src/<package>/` one subpackage, one file, at a time |
| Test files | `test_<module>.py` maps 1:1 to the source module it covers |
| Fixtures | `conftest.py` at every level that needs shared fixtures; chained, not duplicated |
| Grouping | `class Test<Subject><Scenario>:` with a one-line class docstring |
| Docstrings | Every test has a one-line docstring stating the behavior it proves, present tense |
| Naming | `test_<subject>_<expected_outcome>`, no numbers, fully descriptive |
| Floats | Always `pytest.approx(x, abs=... )` or `rel=...` — never bare `==` |
| Tables of cases | `@pytest.mark.parametrize` |
| Slow/optional | `@pytest.mark.slow` / `@pytest.mark.integration`, registered + `--strict-markers` |
| Optional deps | `pytest.importorskip("heavy_pkg", reason="...")` at module top |
| Spying | `monkeypatch.setattr` wrapping/subclassing the real thing, not blanket mocks |
| CLI | `typer.testing.CliRunner` / Click's equivalent — no subprocess |
| GUI | `pytest.importorskip` gate + `QT_QPA_PLATFORM=offscreen` in CI |
| Regression | Real sample files under `tests/data/`, parsed once via an autouse fixture |
| Scientific validation | Literature tables as typed Python data + aggregate-error assertions |
| Coverage | Excludes thin CLI/GUI wrapper entrypoints, focuses on real logic |
| CI | `tests.yml` (OS x Python matrix) + separate `lint.yml`, wired to `workflow_call` |

## Workflow: setting up or extending a test suite

Work through these in order. Each step links to a reference file with the full detail and
runnable examples, and to a ready-to-adapt template in `assets/`. Don't read every reference
up front — pull in the one that matches what you're actually doing right now.

### 1. Confirm the tooling baseline

Check whether the project already uses `uv` (a `uv.lock` or `[dependency-groups]` in
`pyproject.toml` is the tell). If so, add a `dev` dependency group with `pytest`, `ruff`, `ty`,
and `prek`, and wire `[tool.pytest.ini_options]` + `[tool.coverage.*]`. If the project uses
something else (poetry, plain pip, unittest), keep the *conventions* below and translate the
tooling — see "Adapting to other setups" at the end of this file.

→ `references/tooling-and-config.md` · template: `assets/pyproject.testing.toml`

### 2. Lay out `tests/` to mirror `src/`

Before writing a single test, create the directory skeleton so it matches the package
structure exactly — one test directory per subpackage, one test file per module. This is what
makes a large suite navigable: given a source file, its tests are never more than a rename
away.

→ `references/directory-layout.md`

### 3. Write `conftest.py` fixture chains

Start from the cheapest, most atomic fixture and layer derived fixtures on top of it. Put
fixtures at the narrowest `conftest.py` that needs them — package-wide in the root, narrower
in a subpackage's own `conftest.py`. Use factory fixtures (a fixture that returns a callable)
when a test needs many variants of the same construction.

→ `references/fixtures.md` · templates: `assets/conftest.root.py`, `assets/conftest.subpackage.py`

### 4. Write the test modules

One file per source module. Group related test cases into `class Test<Subject><Scenario>:`
blocks. Give every single test a one-line docstring that states the guarantee being checked,
not "test that X" — write it as if it's a line in the package's spec.

→ `references/writing-tests.md` · template: `assets/test_module_template.py`

### 5. Handle optional dependencies and slow paths

Register `slow` and `integration` markers and enforce them with `--strict-markers`. Gate any
test module that needs an optional/heavy dependency with `pytest.importorskip` at the top,
so the default `pytest tests/ -v` run stays green without every extra installed.

→ `references/mocking-and-optional-deps.md`

### 6. CLI and GUI coverage, if the project has either

CLIs get tested in-process with the framework's test runner (never subprocess, except for the
one case of testing an import guard). GUIs get an `importorskip` gate and an offscreen platform
in CI.

→ `references/cli-and-gui-testing.md`

### 7. Golden-file and scientific-validation tests, where they apply

If the package parses real external file formats, bundle small real samples under `tests/data/`
and regression-test against them. If it implements a published model or algorithm, transcribe
the paper's reference numbers into typed Python data and assert aggregate error bounds rather
than exact equality.

→ `references/golden-and-validation-tests.md`

### 8. Wire up CI

A `tests.yml` matrix (OS x Python version) and a separate `lint.yml`, both installed the same
way local dev is, plus `dependabot.yml` to keep it current.

→ `references/ci-workflows.md` · templates: `assets/tests.yml`, `assets/lint.yml`, `assets/pre-commit-config.yaml`

## Anti-patterns this style deliberately avoids

- A bare `assert some_value` with no docstring — if you can't say in one sentence what the
  assertion proves, you don't understand the test yet.
- Comparing floats with `==`. Always `pytest.approx`, always with an explicit, reasoned
  tolerance.
- Mocking the exact thing under test. Prefer a real, lightweight, dependency-free
  implementation of the same interface (a "random"/"fake" backend alongside the real ones) so
  shared base-class logic gets exercised for real, not `MagicMock`ed into meaninglessness.
- One giant `test_everything.py`. Tests live next to the module they cover, at the same
  granularity as the source tree.
- Silently skipped tests. If a test can't run without an optional dependency or a display,
  say so explicitly via `importorskip` or a marker with a `reason=`, never a quiet early
  `return`.
- Exact-equality checks on physically- or statistically-derived numbers. State the tolerance
  and, for literature validation, the aggregate error bound and the minimum sample size —
  a bound checked over zero rows is not a passing test.

## Adapting to other setups

- **No `uv`**: keep the same `[tool.pytest.ini_options]` / `[tool.coverage.*]` sections; swap
  the dev-dependency mechanism for the project's own (poetry group, `requirements-dev.txt`,
  etc.) and the CI install step accordingly.
- **Click instead of Typer**: swap `typer.testing.CliRunner` for `click.testing.CliRunner` —
  the pattern (in-process invocation, checking `exit_code`/`output` separately, testing both
  human and machine-readable output modes) is identical.
- **unittest-only codebase**: keep the docstring-per-test and class-grouping conventions
  (they work fine on `unittest.TestCase` subclasses too, as seen in CLI/GUI/entrypoint test
  files in this style); adopt `pytest` at least as the *runner* so markers, `importorskip`,
  and `pytest.approx` are available even if some modules keep `TestCase`-style classes.
- **Non-Python project**: the layout, docstring, golden-file, and CI-matrix principles port
  directly (test-directory-mirrors-source, one file per unit, one sentence per test); the
  specific fixture/marker/`importorskip` mechanics are pytest-specific and need a translation
  to the target framework's equivalent (e.g. table-driven tests + subtests, or a `testdata/`
  fixture directory pattern).
