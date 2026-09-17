# Project tooling and configuration

## The dev toolchain

Four tools, each with one job, wired together so a single command runs all of them:

- **[uv](https://docs.astral.sh/uv/)** — dependency management, virtualenvs, and running
  commands (`uv run pytest`). Fast and reproducible; `uv.lock` is committed so CI and every
  contributor resolve identical versions.
- **[pytest](https://docs.pytest.org/)** — the test runner itself.
- **[ruff](https://docs.astral.sh/ruff/)** — linting *and* formatting in one tool (replaces
  flake8 + isort + black).
- **[ty](https://github.com/astral-sh/ty)** — static type checking.
- **[prek](https://github.com/j178/prek)** — a fast pre-commit-hooks-compatible runner; wires
  ruff, ty, and a handful of hygiene hooks into `git commit` and into CI.

All four dev dependencies live in one place so `uv sync` (or `uv sync --dev` / `--all-extras`)
gets a contributor everything they need in one command:

```toml
[dependency-groups]
dev = [
    "prek>=0.5.0",
    "pytest>=8.0",
    "ruff>=0.16",
    "ty>=0.0.77",
]
```

If the project isn't on `uv`, this becomes a poetry dependency group, an extras group in
`setup.cfg`/`pyproject.toml`, or a `requirements-dev.txt` — the pinned, single-command-install
property is what matters, not the specific tool.

## `[tool.pytest.ini_options]`

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["src"]
addopts = "--strict-markers -ra"
markers = [
    "slow: marks tests as slow-running",
    "integration: marks tests that require an installed optional dependency",
]
```

- `testpaths = ["tests"]` — pytest only looks in `tests/`; nothing accidentally collected from
  scratch scripts or example notebooks elsewhere in the repo.
- `pythonpath = ["src"]` — only needed for a `src/` layout *without* an editable install
  already on the path; lets `pytest` import the package without a separate `pip install -e .`
  step. Omit it if the package is always installed editable in CI and locally.
- `addopts = "--strict-markers -ra"` — `--strict-markers` turns an unregistered
  `@pytest.mark.foo` (usually a typo) into a hard collection error instead of a silently
  ignored marker. `-ra` prints a short summary of all non-passing tests (skips, xfails,
  errors), so a skip never quietly disappears from the output.
- `markers = [...]` — every custom marker used anywhere in the suite must be registered here
  with a one-line explanation; that explanation is what `pytest --markers` prints, so make it
  useful to a new contributor, not just a keyword.

Add more markers as the project needs them (`gpu`, `network`, `flaky`), but keep each one
narrow enough that "run everything except this marker" is still a meaningful, fast subset.

## `[tool.coverage.run]` / `[tool.coverage.report]`

```toml
[tool.coverage.run]
source = ["src/yourpackage"]
omit = [
    "src/yourpackage/__main__.py",
    "src/yourpackage/gui/*",
]

[tool.coverage.report]
omit = [
    "src/yourpackage/__main__.py",
    "src/yourpackage/gui/*",
]
```

Exclude thin wrapper entrypoints (a `__main__.py` that just calls into `cli.py`, a GUI module
that's mostly Qt boilerplate) from the coverage *target*, not from testing — those modules
still get tests (see `references/cli-and-gui-testing.md`), but coverage percentage should
track the logic that actually matters, not widget wiring. Naming every omitted path explicitly
(rather than a broad glob) keeps the omission list itself reviewable in a PR diff.

## Linting and type-check rule selection (ruff / ty)

Keep the omitted-rule list short and each entry commented with *why* it's off — a rule list
with no comments is a rule list nobody trusts enough to tighten later. A representative
starting selection:

```toml
[tool.ruff]
line-length = 130

[tool.ruff.lint]
select = [
    "A", "B", "C4", "D", "E", "ERA", "F", "FA", "I", "ICN",
    "N", "PL", "PTH", "Q", "SIM", "TC", "UP", "W",
]
ignore = [
    "E501",    # line-too-long: ruff format already wraps what it safely can
    "PLR0913", # too-many-arguments: common and fine for config-heavy constructors
    "PLR2004", # magic-value-in-comparison: too noisy for numeric/scientific code
]

[tool.ruff.lint.pydocstyle]
convention = "google"
```

`D` (pydocstyle) is what makes the "every test has a docstring" convention *enforced*, not just
followed by habit — turn it on for `tests/**/*.py` too, not just `src/`.

## Pre-commit hooks (`prek` / `.pre-commit-config.yaml`)

```yaml
repos:
  - repo: https://github.com/astral-sh/uv-pre-commit
    rev: 0.12.7
    hooks:
      - id: uv-lock

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.16.5
    hooks:
      - id: ruff-check
        args: ["--fix"]
      - id: ruff-format

  - repo: local
    hooks:
      - id: ty
        name: ty type check
        language: system
        entry: uvx ty check
        types_or: [python, pyi]
        pass_filenames: false

  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v6.0.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-case-conflict
      - id: mixed-line-ending
      - id: check-yaml
      - id: check-toml
      - id: check-merge-conflict
```

`uv-lock` keeps the committed lockfile from drifting out of sync with `pyproject.toml`
unnoticed. The `ty` hook is `local`/`system` because — at the time this pattern was captured —
Astral hadn't shipped an official pre-commit hook for it yet; check whether one exists before
copying the local-hook workaround verbatim.

## The commands a contributor actually runs

Document these explicitly in `CONTRIBUTING.md` — don't make a contributor reverse-engineer
them from CI YAML:

```sh
uv sync --all-extras --dev      # one-time / after pulling new deps
uv run prek install             # installs the git hooks
uv run pytest tests/ -v         # run the suite
uv run prek run --all-files     # lint + format + type-check, same as CI
```
