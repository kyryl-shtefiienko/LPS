# Research / academic software profile

This profile is for software released alongside (or in support of) academic research — a lab's simulation code, a method implementation tied to a paper, a scientific CLI/library. It's based on a consistent, real pattern observed across a working materials-science research group's public repositories (multiple Python packages plus one C++/CMake project, spanning single-maintainer tools to a 70+ star multi-contributor framework). Where this profile's defaults **conflict with the generic guidance elsewhere in this skill, this profile wins for a repo that fits it** — the differences below aren't oversights in the generic guidance, they're a genuinely different, well-established norm for this kind of repo.

Use this profile when the repo is: an implementation accompanying a publication, a lab/group's shared research tool, anything with a Zenodo/arXiv DOI or an ORCID-bearing author, or when the user says things like "materials science," "computational research," "cite this software," or names a paper it goes with.

## What's consistent across every repo in the pattern

Regardless of language, every repo had: a `LICENSE`, a README with a dedicated **Citation** section (human-readable citation *and* BibTeX), a Zenodo DOI badge, and CI status badges. Everything below fills in the specifics.

## Where this profile overrides the generic defaults

| Generic skill default | Research profile | Why |
|---|---|---|
| MIT as the default license assumption (Step 4) | **GPL-3.0-or-later** as the default | Observed 4 of 5 times, including the flagship framework. Academic groups building on each other's simulation/analysis code often want derivative works to stay open — the same reasoning as `references/licensing-guide.md`'s copyleft case, just a stronger prior for *this* kind of repo. Still ask if the user has a specific preference; don't silently override an explicit choice. |
| Community health files scaled to "public = include most of them" (Step 5) | **Skip nearly all of them by default** | Zero of five repos had CODE_OF_CONDUCT.md, SECURITY.md, issue templates, PR templates, or CODEOWNERS. Only the single most-starred, most-contributed-to repo had a CONTRIBUTING.md. For a lab tool with one or a few maintainers, this infrastructure is overhead nobody uses — add it later if the project actually grows a contributor base (see PhaseForge's CONTRIBUTING.md, added once it had significant external interest), not up front. |
| Generic `pip install -r requirements.txt` / setuptools framing | **`uv` as the primary package manager** | Every Python repo used `uv` (`uv add`, `uv.lock` committed, `uv_build` as the PEP 517 backend) with `pip` documented only as a fallback. |
| Generic lint/format/type-check placeholders in CI templates | **`ruff` (lint + format) + `ty` (type checking)**, not black/flake8/isort/mypy | Every `pyproject.toml` observed used exactly this combination — `ruff` doing both linting and formatting in one tool, and `ty` (Astral's newer, fast type checker) instead of mypy. |
| No pre-commit setup in the generic skill at all | **`.pre-commit-config.yaml` is standard** | See the exact hook set below — this profile adds a bundled `.pre-commit-config.yaml` the generic profile doesn't have. |
| No citation file mentioned in the generic skill at all | **`CITATION.cff` at repo root, plus a README "Citation" section with BibTeX** | This is the single biggest gap in the generic skill for this audience — see below. |
| Sphinx assumed or left unspecified for docs | **MkDocs + Material theme + mkdocstrings** | Every Python repo used this stack, deployed to GitHub Pages, not Sphinx/ReadTheDocs. |

## CITATION.cff

The [Citation File Format](https://citation-file-format.github.io/) is a small YAML file GitHub natively recognizes — a repo with one gets a "Cite this repository" button in its sidebar. Every research-profile repo observed had one at the root, following this shape:

```yaml
cff-version: 1.2.0
message: "If you use this software, please cite it as below."
title: <project name>
version: <current version>
date-released: "YYYY-MM-DD"
license: <SPDX identifier>
repository-code: "https://github.com/<user>/<repo>"
doi: <Zenodo DOI, e.g. 10.5281/zenodo.NNNNNNN>
url: "https://doi.org/<that DOI>"
abstract: "<1-2 sentence abstract>"
authors:
  - family-names: "<Last>"
    given-names: "<First>"
    email: <email>
    orcid: "https://orcid.org/XXXX-XXXX-XXXX-XXXX"
```

`assets/CITATION.cff.template` follows this exactly. Get a real Zenodo DOI by connecting the repo to [Zenodo](https://zenodo.org/account/settings/github/) — pushing a GitHub Release then mints a versioned DOI automatically. Don't fabricate a DOI; leave it as a `TODO:` placeholder until one actually exists, and don't publish an unsupported citation claim.

## README structure specific to this profile

Same core sections as `references/readme-standards.md`, arranged and extended for a citable research artifact:

1. **Logo** (if one exists) at the very top, linked to the full-size image.
2. **Title**, then three tiers of badges, each on its own line: (1) License, language/Python version, supported platforms; (2) CI status (tests, lint); (3) DOI badges — the software's own Zenodo DOI *and*, notably, a separate DOI badge for each associated paper. Citing the paper(s) the software implements, not just the software itself, is a distinctive and valuable pattern here.
3. One-paragraph description.
4. A single line of links: `Report a Bug | Request a Feature | Documentation` — pre-filled, pre-labeled issue URLs (`issues/new?labels=bug`) rather than a link to a CONTRIBUTING.md. This is the lightweight substitute for issue templates this profile favors by default.
5. Features (grouped, can include numbered footnote citations to the literature backing a specific claim or method — Markdown footnote syntax: `claim[^1]` with `[^1]: full citation` at the bottom).
6. Installation — lead with `uv` (`uv add`, or `uv tool install` / `uvx` for a CLI tool), `pip` as a documented fallback.
7. Quickstart / Usage with real, runnable code.
8. License.
9. **Citation** — a blockquote-style human-readable citation (and one per associated paper, if there are several) immediately followed by a fenced BibTeX code block with matching `@software`/`@article`/`@misc` entries. This section is never skipped in the pattern observed, even in the smallest repos.

`assets/README.research.template.md` implements this layout.

## Python tooling stack

`pyproject.toml` conventions observed, consistently, across every Python repo:

- License declared via the PEP 621 table form: `license = { text = "GPL-3.0-or-later" }` (not the bare string form).
- `classifiers` always include `Intended Audience :: Science/Research` and `Topic :: Scientific/Engineering`.
- `[project.optional-dependencies] docs = ["mkdocs-material==<pin>", "mkdocstrings[python]==<pin>"]` — docs tooling is an optional extra, not a dev dependency.
- `[dependency-groups] dev = ["prek", "pytest", "ruff", "ty"]` — the modern PEP 735 dependency-groups table, not a `[tool.uv] dev-dependencies` block. `prek` is a fast, pre-commit-compatible hook runner; the `.pre-commit-config.yaml` format itself is unchanged, so either `pre-commit` or `prek` can run it.
- `[tool.pytest.ini_options]` with `testpaths = ["tests"]` and `pythonpath = ["src"]` — the `pythonpath` entry matters for the src-layout (see `references/repo-structure.md`), letting pytest find the package without an editable install.
- `[tool.ruff]` with an intentionally broad `select` list (pyflakes, pycodestyle, bugbear, comprehensions, pydocstyle with the Google convention, pyupgrade, simplify, and more) and a short, deliberate `ignore` list for rules that fight normal scientific code (e.g. `PLR0913`/`PLR0915` for functions with many physically-meaningful parameters).
- `[tool.ty.src] include = ["src", "tests"]` for the type checker.

`assets/.pre-commit-config.yaml` mirrors the hook set observed exactly:

```yaml
repos:
  - repo: https://github.com/astral-sh/uv-pre-commit
    rev: <pin>
    hooks: [{id: uv-lock}]
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: <pin>
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
    rev: <pin>
    hooks: [trailing-whitespace, end-of-file-fixer, check-case-conflict, mixed-line-ending, check-yaml, check-toml, check-merge-conflict]
```

(As of this writing, Astral hadn't shipped an official `ty` pre-commit hook yet, hence the `local`/`uvx` workaround above — check whether `astral-sh/ty-pre-commit` exists yet and prefer it once it does.)

## CI: `tests.yml` and `lint.yml`, not one combined `ci.yml`

This profile uses two separate workflow files rather than the generic profile's single `ci.yml` with two jobs — same effect, split files. `assets/workflows/tests.yml` and `assets/workflows/lint.yml` use `astral-sh/setup-uv` to install `uv`, then `uv run pytest` / `uv run ruff check` / `uv run ruff format --check` / `uvx ty check`, matching the `uv`-first tooling above rather than a bare `pip install`.

## Documentation: MkDocs, not Sphinx

`assets/mkdocs.yml.template` mirrors the observed setup: `mkdocs-material` theme with a light/dark/auto palette toggle, `mkdocstrings` (Python handler, Google docstring style) for API-reference generation from docstrings, and MathJax loaded via `extra_javascript` for LaTeX equation rendering — expected for anything with real mathematical or physical notation in its docs.

The navigation structure is a distinctive, worth-copying pattern beyond materials science specifically: **Usage** (practical how-to, task by task) is kept separate from **Theory** (the scientific/mathematical background — what the equations mean and where they come from) which is kept separate again from **API Reference** (generated from docstrings, not hand-written). A reader who wants to run something doesn't have to wade through derivations to find the function call, and a reader who wants to understand the method doesn't have to reverse-engineer it from API docs.

## Non-Python repos

The one C++ project in the pattern (CMake-based, using git submodules for a vendored dependency) kept the same README/citation/license conventions as the Python repos, but naturally used CMake's own build conventions instead of `uv`/`pyproject.toml`, and was also the one repo with a `CONTRIBUTING.md` — added, notably, only once the project had substantially more external stars and contributors than the others. Read this as confirmation that the "skip community health files by default" guidance above is about project maturity and contributor count, not language — add `CONTRIBUTING.md` back in once outside contribution is actually happening, exactly as the generic skill's Step 5 already says.

## A gap worth flagging, not copying

One repo in the pattern had no `LICENSE` file at all despite its README describing it as "fully open-source." Don't read this as license-optional being acceptable — flag it as exactly the gap `references/licensing-guide.md` warns about, and treat it as a bug to fix (ask which license, most likely GPL-3.0-or-later to match its sibling repos) rather than a variant worth reproducing.

## Using this profile with the scripts

`scripts/init_repo.py --profile research` applies every default above: GPL-3.0-or-later license, `CITATION.cff`, `mkdocs.yml`, `.pre-commit-config.yaml`, `.python-version`, the `uv`/`ruff`/`ty` CI workflows, the research README template, and community health files skipped unless `--with-community-files` is also passed. `scripts/validate_repo.py` includes a situational `CITATION.cff` check alongside the generic checklist.
