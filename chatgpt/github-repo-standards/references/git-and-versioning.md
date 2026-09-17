# Git conventions and versioning

Apply these going forward on a repo, not retroactively — rewriting existing commit history to match a new convention causes more disruption than the convention is worth.

## Conventional Commits

A commit message format: `<type>(<optional scope>): <description>`. The **why** it's worth adopting: it makes commit history scannable at a glance, and it's what enables automated tooling — a CHANGELOG generator or a semantic-version bumper can read `feat:` vs `fix:` vs a `BREAKING CHANGE:` footer and know exactly what changed, without a human curating a changelog by hand.

Common types:

| Type | Meaning |
|---|---|
| `feat` | A new feature |
| `fix` | A bug fix |
| `docs` | Documentation only |
| `style` | Formatting, no code meaning change (whitespace, semicolons) |
| `refactor` | Code change that neither fixes a bug nor adds a feature |
| `perf` | A performance improvement |
| `test` | Adding or correcting tests |
| `build` | Build system or external dependency changes |
| `ci` | CI configuration changes |
| `chore` | Everything else (tooling, maintenance) |
| `revert` | Reverts a previous commit |

A breaking change is marked either with `!` after the type/scope (`feat!: drop support for Node 16`) or a `BREAKING CHANGE:` footer with details — this is the signal a semantic-version bumper uses to know a change needs a MAJOR bump rather than MINOR.

**Example:**
Input: Added user authentication with JWT tokens
Output: `feat(auth): implement JWT-based authentication`

Keep the first line under ~72 characters, written in the imperative mood ("add X," not "added X" or "adds X") — this matches the convention Git itself uses for its own generated commit messages (merges, reverts), so the whole history reads consistently.

## Semantic Versioning (SemVer)

Version numbers as `MAJOR.MINOR.PATCH`:
- **MAJOR** — incompatible / breaking API change.
- **MINOR** — new functionality, backward compatible.
- **PATCH** — backward-compatible bug fix.

A `0.y.z` version signals "anything may change at any time" by convention — don't promise MAJOR-level stability guarantees before a real `1.0.0`. The value of SemVer is that a consumer can pin `^1.2.0` and trust that any `1.x` upgrade won't break them; violating that (shipping a breaking change as a MINOR bump) undermines the entire point of using it.

## Branching model

Two common models — pick based on release cadence, not habit:

- **Trunk-based (recommended default for most projects):** one long-lived `main` branch, short-lived feature branches (`feat/short-description`, `fix/short-description`) merged in quickly via PR. Simple, low-overhead, works well with continuous deployment. Use this unless there's a specific reason not to.
- **GitFlow-style (`main` + `develop` + release branches):** worth the added overhead only when a project maintains multiple release lines simultaneously (e.g. patching an old major version while developing the next) or has scheduled, batched releases rather than continuous ones. Don't adopt this by default — it adds real process overhead that most projects don't need.

## Tagging releases

```bash
git tag -a v1.2.0 -m "v1.2.0"
git push origin v1.2.0
```

Pushing a tag matching `v*.*.*` is what triggers `assets/workflows/release.yml` if it's wired up (see `references/ci-cd-and-automation.md`). Tag the exact commit that was released, not a later one — if a hotfix is needed, that's a new tag, not a moved one (moving tags breaks anything that already fetched the old commit at that tag).

## CHANGELOG format

`assets/CHANGELOG.template.md` follows the widely-used "Keep a Changelog" convention: each release gets a dated `## [X.Y.Z] - YYYY-MM-DD` heading, with changes grouped under `Added` / `Changed` / `Deprecated` / `Removed` / `Fixed` / `Security` subheadings, plus an `[Unreleased]` section at the top for changes not yet in a tagged release. If commits consistently follow Conventional Commits, this file can largely be generated from `git log` between tags rather than written by hand — group by commit type, drop `chore`/`ci`/`style` entries as usually not user-facing.
