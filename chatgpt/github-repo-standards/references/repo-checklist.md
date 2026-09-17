# The ultimate GitHub repo checklist

This is the full standard behind `scripts/validate_repo.py`. The script checks everything marked **[scriptable]** automatically; items marked **[manual]** require judgment or a repo settings change and aren't (and mostly can't be) checked by a script. Items marked **situational** only apply to some repos — see the notes.

## Documentation

- [ ] **[scriptable]** `README.md` exists
- [ ] **[scriptable]** README covers install, usage/quickstart, and mentions the license
- [ ] **[scriptable]** README is substantive, not a one-line stub
- [ ] **[manual]** The quickstart has actually been tested and works from a clean clone
- [ ] **[manual]** No TODO/placeholder text left unfilled in published docs
- situational **[manual]** `docs/` directory for content that's outgrown the README
- situational **[manual]** Architecture diagram, for projects complex enough to benefit from one
- situational **[manual]** Screenshots/demo for anything with a visual or CLI surface

## Legal

- [ ] **[scriptable]** `LICENSE` file exists
- [ ] **[manual]** The license is an intentional choice, not a default, and matches how the author actually wants the code used (see `references/licensing-guide.md`)
- [ ] **[manual]** License is also declared in the package manifest (`package.json`, `pyproject.toml`, etc.)
- [ ] **[manual]** No contradictory licensing claims elsewhere in the repo (README, CONTRIBUTING)

## Community health

*(All situational — scale to the project's actual audience; see `SKILL.md` Step 5.)*

- [ ] **[scriptable]**, situational `CONTRIBUTING.md` exists
- [ ] **[scriptable]**, situational `CODE_OF_CONDUCT.md` exists
- [ ] **[scriptable]**, situational `SECURITY.md` exists
- [ ] **[manual]**, situational `SUPPORT.md` exists, once question volume justifies it
- [ ] **[scriptable]**, situational `CODEOWNERS` exists, once there's more than one maintainer
- [ ] **[scriptable]**, situational Issue templates exist, for projects taking outside bug reports
- [ ] **[scriptable]**, situational PR template exists, for projects with more than one contributor
- [ ] **[manual]** GitHub's own "Community Standards" checklist (repo Insights → Community) shows all applicable items green

## Git hygiene

- [ ] **[scriptable]** `.gitignore` exists and matches the project's actual language/tooling
- [ ] **[scriptable]** `.editorconfig` exists
- [ ] **[scriptable]** `.gitattributes` exists (line-ending normalization, generated-file marking)
- [ ] **[manual]** No committed build artifacts, dependency directories, or IDE-specific files that `.gitignore` should have caught
- [ ] **[manual]** Commit history follows a consistent convention going forward (Conventional Commits or another explicit standard — see `references/git-and-versioning.md`)
- [ ] **[manual]** Default branch is named `main` (or a deliberate choice, not an unexamined legacy default)

## CI/CD and security automation

- [ ] **[scriptable]** At least one GitHub Actions workflow exists under `.github/workflows/`
- [ ] **[manual]** CI actually runs lint and test, with real (not placeholder) commands
- [ ] **[manual]** Branch protection on `main` requires CI to pass and requires review before merge
- [ ] **[scriptable]** Dependabot config (`.github/dependabot.yml`) exists
- [ ] **[manual]** Dependabot security updates enabled (repo Settings → Security)
- [ ] **[manual]** Secret scanning + push protection enabled (repo Settings → Security), for public repos
- situational **[manual]** CodeQL workflow enabled, for public repos
- situational **[manual]** Release automation wired up, once the project cuts tagged releases

## Release management

- [ ] **[scriptable]**, situational `CHANGELOG.md` exists, once the project starts cutting releases
- [ ] **[manual]** Version numbers follow SemVer meaningfully (breaking changes bump MAJOR)
- [ ] **[manual]** Releases are tagged (`vX.Y.Z`) at the exact released commit

## Code quality signals

*(Outside this skill's scope to generate, but worth checking as part of an audit — a beautifully documented repo with a failing test suite still isn't "done.")*

- [ ] **[manual]** Test suite exists and actually exercises meaningful behavior, not just smoke tests
- [ ] **[manual]** CI is currently green, not red-and-ignored
- [ ] **[manual]** A linter/formatter is configured and actually enforced in CI, not just present in config

## Polish and discoverability

- [ ] **[scriptable]** README has at least one status badge
- [ ] **[manual]** Every badge shown is currently true (no failing-CI badge, no coverage badge with no coverage tool)
- [ ] **[manual]** Repo has a one-line GitHub description and relevant topics/tags set (repo Settings → About) — this is what search and the GitHub explore surfaces use, and it's easy to forget since it's not a file in the repo at all
- [ ] **[manual]** Repo social preview image set, for a project meant to be shared/promoted (Settings → General → Social preview)

## Security hygiene

- [ ] **[scriptable]** Basic secrets scan (`validate_repo.py`'s built-in check) finds nothing
- [ ] **[manual]** GitHub's native secret scanning (more thorough than this skill's regex check) shows no unresolved alerts
- [ ] **[manual]** No `.env` files, credentials, or private keys in git history (not just the current working tree — a file removed in a later commit is still in history unless it was purged)

## How to use this list

Run `python scripts/validate_repo.py --path .` for everything marked **[scriptable]** — it produces a scored report automatically. Walk the **[manual]** items yourself afterward; they need judgment a script can't apply. Prioritize by impact, not by list order: a missing LICENSE or a thin README on a public repo matters far more than a missing `SUPPORT.md`. Situational items are exactly that — situational; a low score from skipping every community-health file on a private solo repo isn't a real gap.
