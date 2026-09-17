<!-- CONTRIBUTING template — github-repo-standards skill. Delete this comment
     when done. Fill in the real dev-setup and test commands; don't leave
     generic placeholders in a file people will actually try to run. -->

# Contributing to {{PROJECT_NAME}}

Thanks for taking the time to contribute. This document covers how to get a development environment running, the expectations for pull requests, and how to propose larger changes.

## Before you start

- **Small fix (typo, obvious bug)?** Open a pull request directly.
- **New feature or larger change?** Open an issue first to discuss the approach before writing code — this avoids spending time on a PR that doesn't fit the project's direction.
- **Found a security issue?** Do not open a public issue. See [SECURITY.md](SECURITY.md).

## Development setup

```bash
TODO: clone, install dependencies, and any one-time setup steps
```

## Running tests

```bash
TODO: the actual test command, e.g. `pytest` / `npm test` / `go test ./...`
```

All pull requests must pass CI (lint + tests) before being merged.

## Coding style

TODO: linter/formatter used, and how to run it, e.g.:

```bash
TODO: e.g. `ruff check .` / `npm run lint`
```

## Commit messages

This project follows [Conventional Commits](https://www.conventionalcommits.org/) (`feat:`, `fix:`, `docs:`, `chore:`, etc.) — see `references/git-and-versioning.md` in the github-repo-standards skill for the full convention if you're generating this from scratch. Keep the first line under ~72 characters and written in the imperative mood ("add X", not "added X").

## Pull request process

1. Fork the repo and create a branch from `main` (`feat/short-description` or `fix/short-description`).
2. Make your change, with tests for new behavior.
3. Make sure CI passes.
4. Open the PR using the pull request template — fill in what changed and why.
5. Address review feedback. A maintainer will merge once it's approved.

## Code of Conduct

This project follows the [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you're expected to uphold it.
