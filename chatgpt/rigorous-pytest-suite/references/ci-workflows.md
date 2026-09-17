# CI workflows

## Split tests and lint into separate workflows

Keep `tests.yml` and `lint.yml` as two independent GitHub Actions workflows rather than one
combined job. They fail for different reasons, run at different speeds, and a contributor
looking at a red check should immediately know which category broke without opening the logs.

## `tests.yml`: an OS x Python-version matrix

```yaml
name: Tests

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  workflow_dispatch:
  workflow_call:

permissions:
  contents: read

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

jobs:
  test:
    name: Test (Python ${{ matrix.python-version }}, ${{ matrix.os }})
    runs-on: ${{ matrix.os }}
    strategy:
      fail-fast: false
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        python-version: ["3.10", "3.11", "3.12", "3.13"]

    steps:
      - name: Checkout code
        uses: actions/checkout@v7

      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v7
        with:
          python-version: ${{ matrix.python-version }}

      - name: Install uv
        uses: astral-sh/setup-uv@v10
        with:
          enable-cache: true

      - name: Install dependencies
        run: uv sync --all-extras

      - name: Run tests
        run: uv run pytest tests/ -v
```

Notes on each piece:

- **`workflow_call`** lets a separate `release.yml` require this workflow as a prerequisite
  (`needs:` / `uses: ./.github/workflows/tests.yml`), so a release literally cannot ship
  without green tests, rather than that being a manually-enforced convention.
- **`concurrency` with `cancel-in-progress: true`** cancels a stale run automatically when a
  new commit lands on the same branch/PR, so CI minutes aren't wasted testing code that's
  already been superseded.
- **`fail-fast: false`** — a failure on one OS/version combination shouldn't hide results from
  the others; you want the full matrix's signal on every run.
- Installing with the exact same command a contributor runs locally (`uv sync --all-extras`)
  is what makes "passes in CI" and "passes on my machine" the same statement.

## Marker-gated subsets in CI

If the suite has `slow`/`integration`-marked tests that shouldn't run on every push, exclude
them in the main job and either skip them entirely or run them as a separate, explicitly
triggered job:

```yaml
- name: Run tests
  run: uv run pytest -v -m "not integration and not slow"
```

## One job per optional extra, for packages with many heavy optional dependencies

When a package has several optional backends that each pull in a large dependency (an ML
framework, a proprietary tool wrapper), don't install them all into one job — matrix over
extras, each job installing exactly one, caching whatever model/asset that extra needs, and
running only the tests scoped to it:

```yaml
jobs:
  test-extra:
    name: "${{ matrix.name }} Tests"
    runs-on: ubuntu-latest
    strategy:
      fail-fast: false
      matrix:
        include:
          - name: backend-a
            install: --extra backend-a
            tests: tests/backends/test_backend_a.py
          - name: backend-b
            install: --extra backend-b
            cache_key: backend-b-model-v1
            cache_path: ~/.cache/backend-b
            tests: tests/backends/test_backend_b.py

    steps:
      - uses: actions/checkout@v7
      - uses: actions/setup-python@v7
        with:
          python-version-file: ".python-version"
      - uses: astral-sh/setup-uv@v10
        with:
          enable-cache: true
          cache-suffix: ${{ matrix.name }}
      - run: uv sync --frozen ${{ matrix.install }} --group dev
      - name: Cache downloaded model
        if: matrix.cache_key
        uses: actions/cache@v6
        with:
          path: ${{ matrix.cache_path }}
          key: model-${{ matrix.name }}-${{ matrix.cache_key }}
      - run: uv run pytest -v ${{ matrix.tests }}
```

This keeps the default/core job (no heavy extras installed) fast on every push, while still
giving every optional code path real, if less frequent, CI coverage.

## `lint.yml`: one job, same install, runs the same hooks as local `git commit`

```yaml
name: Lint

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v7
      - uses: actions/setup-python@v7
        with:
          python-version-file: ".python-version"
      - uses: astral-sh/setup-uv@v10
        with:
          enable-cache: true
      - run: uv sync --all-extras
      - uses: j178/prek-action@v3
        with:
          prek-version: "0.3.8"
```

Running the exact `prek`/pre-commit hook suite in CI (rather than reimplementing "run ruff,
run ty" as separate steps) guarantees CI enforces precisely what the local git hook enforces —
no drift between the two.

## `dependabot.yml`

Keep the lockfile and Action versions current automatically, which also means dependency
bumps get the same CI scrutiny as any other change:

```yaml
version: 2
updates:
  - package-ecosystem: "uv"
    directory: "/"
    schedule:
      interval: "weekly"
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
```
