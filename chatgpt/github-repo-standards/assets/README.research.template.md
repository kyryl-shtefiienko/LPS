<!--
  README template — research-software profile, github-repo-standards skill.
  See references/research-software.md for the reasoning behind this layout.
  Delete this comment block once done. Fill every {{PLACEHOLDER}}, delete
  the logo block if there's no logo yet, and delete any badge that doesn't
  point at something real yet.
-->

<!-- Delete this block if there's no logo yet. -->
[![{{PROJECT_NAME}} logo](docs/assets/logo.png)](docs/assets/logo.png)

# {{PROJECT_NAME}}

[![License: {{LICENSE_NAME}}](https://img.shields.io/badge/license-{{LICENSE_NAME}}-blue.svg)](LICENSE) [![Python](https://img.shields.io/badge/python-{{PYTHON_VERSION}}-blue)](https://www.python.org/) [![Platforms](https://img.shields.io/badge/platform-linux%20%7C%20macos-lightgrey)](https://img.shields.io/badge/platform-linux%20%7C%20macos-lightgrey)

[![Tests](https://github.com/{{GITHUB_USER}}/{{REPO_NAME}}/actions/workflows/tests.yml/badge.svg)](https://github.com/{{GITHUB_USER}}/{{REPO_NAME}}/actions/workflows/tests.yml) [![Lint](https://github.com/{{GITHUB_USER}}/{{REPO_NAME}}/actions/workflows/lint.yml/badge.svg)](https://github.com/{{GITHUB_USER}}/{{REPO_NAME}}/actions/workflows/lint.yml)

<!-- Zenodo badge: connect the repo at https://zenodo.org/account/settings/github/,
     push a Release to mint a real DOI, then replace TODO below.
     Add one more DOI badge per associated paper, same pattern. -->
[![DOI](https://img.shields.io/badge/DOI-TODO-blue.svg)](https://doi.org/TODO)

{{ONE_LINE_DESCRIPTION}}

[Report a Bug](https://github.com/{{GITHUB_USER}}/{{REPO_NAME}}/issues/new?labels=bug) | [Request a Feature](https://github.com/{{GITHUB_USER}}/{{REPO_NAME}}/issues/new?labels=enhancement) | [Documentation](https://{{GITHUB_USER}}.github.io/{{REPO_NAME}})

---

## Features

<!-- Group related bullets under sub-headings if there are many. A claim tied
     to a specific published method can carry a footnote citation:
     "implements the XYZ correction[^1]" with "[^1]: Author, Journal, Year."
     at the bottom of the file. Don't force footnotes where a claim doesn't
     need literature backing. -->

- TODO: feature one
- TODO: feature two
- TODO: feature three

---

## Installation

We recommend [uv](https://docs.astral.sh/uv/) for dependency management, though a plain `pip` install also works.

### Add to a project with uv

```bash
uv add {{PROJECT_NAME}}
```

### pip

```bash
pip install {{PROJECT_NAME}}
```

<!-- Delete this section if the project has no CLI. -->
### Use as a standalone CLI tool with uv

```bash
uv tool install {{PROJECT_NAME}}
{{PROJECT_NAME}} --help
```

Or run a one-off command without installing:

```bash
uvx {{PROJECT_NAME}} TODO-example-command
```

---

## Quickstart

<!-- Real, runnable code. Test it yourself before publishing. -->

```python
TODO: minimal working example
```

---

## License

This project is licensed under the {{LICENSE_NAME}} license — see [LICENSE](LICENSE) for the full text.

---

## Citation

If you use `{{PROJECT_NAME}}` in your research, please cite:
> TODO: Author(s). ({{YEAR}}). {{PROJECT_NAME}}. Zenodo. <https://doi.org/TODO>

<!-- Add one more blockquote line per associated paper, same pattern, above the software citation. -->

BibTeX:

```bibtex
@software{TODO_citekey,
  author    = {TODO: Last, First},
  title     = {{{PROJECT_NAME}}},
  year      = {{YEAR}},
  publisher = {Zenodo},
  doi       = {TODO},
  url       = {https://doi.org/TODO},
}
```

<!-- Optional: numbered footnotes for literature cited inline above, e.g.:
[^1]: Author, A. et al. *Journal Name* **Volume**, pages (Year). https://doi.org/... -->
