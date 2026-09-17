# CI/CD and automation

## Why CI is the highest-leverage automation to add first

Two things happen the moment a repo has real CI: breakage gets caught before it reaches `main` instead of being discovered by the next person who pulls, and every visitor who checks the Actions tab or the badge gets a signal the project is actually maintained. Almost everything else in this file (CodeQL, Dependabot, release automation) is worth less without this foundation in place first.

## Minimum viable CI

For any repo with code, at minimum: **lint and test on every push and pull request.** `assets/workflows/ci-python.yml` and `assets/workflows/ci-node.yml` are ready-to-adapt starting points — copy the one matching the project's language, then replace the placeholder lint/test commands with the project's real ones. A workflow file with a placeholder command that fails on every PR is worse than no CI, since it trains contributors to ignore red checks.

Two structural choices worth keeping from the templates:
- **Trigger on both `push` to main and `pull_request`** — catches breakage from direct pushes and from PRs alike.
- **Matrix across a few runtime versions** (e.g. 3 Python or Node minor versions) — catches version-specific breakage that a single-version pipeline misses, at reasonably low CI-minutes cost for most project sizes.

## Pairing CI with branch protection

CI running is necessary but not sufficient — without a branch protection rule requiring it to pass, someone can still merge a PR with a red check. This is a repo **Settings** change (Settings → Branches → branch protection rule for `main`), not a file this skill can generate directly. Recommend, at minimum:
- Require status checks to pass before merging (select the CI job(s) by name).
- Require at least one pull request review before merging.
- Optionally: require branches to be up to date before merging, and restrict who can push directly to `main`.

If a GitHub MCP connector or `gh` CLI is available in the current session, this can be configured directly (`gh api repos/{owner}/{repo}/branches/main/protection ...` or the equivalent MCP tool) rather than only described — but always confirm with the user before changing repo settings on their behalf.

## Native GitHub security features (Settings → Security, no workflow file needed)

Several of these are toggles in repo settings rather than files, and are free for public repos:
- **Dependabot alerts** — flags known-vulnerable dependencies.
- **Dependabot security updates** — auto-opens a PR to bump a vulnerable dependency to a patched version.
- **Secret scanning** — flags accidentally committed credentials matching known provider patterns (this complements, but is more thorough than, `scripts/validate_repo.py`'s basic regex scan in this skill).
- **Push protection** — blocks a push that contains a detected secret before it ever lands in history.

Recommend enabling all four for any public repo; there's essentially no downside.

## CodeQL

GitHub's free static analysis security scanner. `assets/workflows/codeql.yml` runs it on push/PR to main plus a weekly schedule (catches new vulnerability patterns in CodeQL's own ruleset being discovered against unchanged code). Set the `language` matrix entry to match the project — it supports scanning multiple languages if the repo is polyglot.

## Dependabot version updates

Distinct from Dependabot *security* updates above: this opens routine PRs to keep dependencies current even absent a known vulnerability, which keeps upgrades small and frequent instead of one large, risky jump later. `assets/dependabot.yml.template` → `.github/dependabot.yml`; set `package-ecosystem` to the project's actual package manager, and keep a second entry for `github-actions` so the workflow files themselves stay current too.

## Release automation

`assets/workflows/release.yml` builds and publishes a GitHub Release whenever a version tag (`vX.Y.Z`) is pushed, using `generate_release_notes` to auto-draft notes from merged PRs. Add build/publish steps specific to the project's ecosystem (build a wheel and push to PyPI, `npm publish`, build and attach binaries, etc.). Only worth wiring up once the project is actually cutting tagged releases — see `references/git-and-versioning.md` for tagging conventions. Don't add this to a brand-new, unreleased project; it'll have nothing to do and just adds noise to the Actions tab.

## Stale bot

`assets/workflows/stale.yml` auto-labels and eventually closes inactive issues/PRs. Only useful once a project has enough issue volume that backlog grooming is a real burden — on a new or low-traffic repo it has nothing to clean up and isn't worth the added Action runs.

## Caching and speed

For any CI that installs dependencies, use the setup action's built-in caching (`actions/setup-python`'s `cache: pip`, `actions/setup-node`'s `cache: npm`) rather than a bare install every run — this is already wired into the bundled templates. On a slow-to-install project, a stale or missing cache is often the actual reason CI "feels slow," not the test suite itself.
