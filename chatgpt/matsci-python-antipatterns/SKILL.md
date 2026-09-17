---
name: matsci-python-antipatterns
description: Checklist of common bad practices to avoid when writing a README, Quick Start, or repo layout for a materials-science (or other scientific) Python project — bloated "Repository Structure" trees, over-explained Quick Starts, notebook-only packages, unpinned environments, committed data, missing citations. Use this whenever creating, scaffolding, cleaning up, or reviewing a README or repo structure for a materials-informatics, computational-chemistry, DFT, or ML-for-materials Python codebase — even if the user just says "write me a README" or "clean up this repo" without naming these anti-patterns.
---

# Matsci Python Repo: Bad Practices to Avoid

Materials-science Python repos (DFT/ML/informatics projects) tend to copy the
same bloat from each other. Check new or existing READMEs / repo layouts
against this list. Keep fixes as short as the list itself.

## Avoid

1. **"Repository Structure" tree in the README.** A hand-maintained folder
   tree goes stale the moment a file moves. Drop it — GitHub's file browser
   and `tree -L 2` already show this, live.

2. **Bloated Quick Start.** No prose, no badge parade, no "see section 4.2
   for details." Just the uv install link + install lines:
   ````markdown
   ## Quick start
   [Install uv](https://docs.astral.sh/uv/getting-started/installation/)

   ```bash
   uv venv
   uv pip install -e .
   ```
   ````

3. **Notebooks as the only interface.** Numbered `.ipynb` files with no
   `pyproject.toml` can't be `pip install`ed, imported, or tested. Ship a
   real package; notebooks call into it, not the other way around.

4. **Unpinned environments.** `environment.yml` or `requirements.txt` with
   no version pins breaks reproducibility — a real cost when the repo backs
   a published result. Pin versions; prefer a lockfile (`uv.lock`) over a
   hand-maintained conda YAML.

5. **Data and notebook outputs committed to git.** CIF/POSCAR/trajectory
   files and executed cells bloat the repo. Point to Zenodo / Materials
   Project / figshare instead, and clear notebook outputs before committing.

6. **No `CITATION.cff` despite backing a paper.** Materials-informatics repos
   usually exist to support a publication. Add `CITATION.cff` instead of
   burying a BibTeX block mid-README.

7. **Ambiguous physical units.** Composition/DFT/ML code silently mixes eV,
   kJ/mol, Å, K. State units once (docstring or README header), not per
   function.

8. **One README trying to be paper + tutorial + API reference.** Split it:
   README = what/why + quick start; docs or notebooks = tutorial;
   docstrings = reference.

## Reviewing an existing repo

Check the README's structure/quick-start sections and the top-level file
layout against the list above. Call out violations by number instead of
silently rewriting, then fix only what the user confirms.
