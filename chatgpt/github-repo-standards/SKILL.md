---
name: github-repo-standards
description: Creates, scaffolds, and audits GitHub repositories to a professional standard — README, LICENSE, CONTRIBUTING, CODE_OF_CONDUCT, SECURITY.md, issue/PR templates, CI/CD (GitHub Actions), .gitignore, CODEOWNERS, branch protection, semantic versioning, CHANGELOG. Includes a research/academic-software profile (CITATION.cff, Zenodo/DOI citation sections, MkDocs+Material docs, uv/ruff/ty tooling) for lab code, paper companion repos, and other scientific software. Use whenever the user asks to create, scaffold, initialize, structure, clean up, polish, or "make professional" a GitHub repo or open-source project; asks for a README, LICENSE, CONTRIBUTING guide, issue/PR templates, CI setup, a CITATION.cff, or a repo health audit; is preparing a repo for public release, a portfolio, or open-sourcing; or is releasing research/scientific software or anything needing a citation — even if they only mention one piece (e.g. "write me a README") rather than the whole repo.
license: MIT
compatibility: Works anywhere Claude has bash and Python 3 (standard library only, no pip installs needed). scripts/init_repo.py optionally fetches live LICENSE and .gitignore text from api.github.com and raw.githubusercontent.com, and falls back to bundled minimal versions if outbound network access isn't available. No MCP connector or GitHub account required. If a GitHub MCP/gh CLI connector is connected, this skill's standards still apply on top of it.
metadata:
  author: Claude
  version: 1.1.0
  category: software-engineering
  tags: [github, git, readme, open-source, ci-cd, documentation, repo-scaffolding, research-software, citation]
---

# GitHub Repo Standards

## Why this exists

A repo full of working code with no README, no license, and no tests reads as unfinished, even when the code itself is excellent. The gap between "code that runs" and "a repository people trust enough to use, star, or contribute to" is almost entirely made of the things in this skill: clear documentation, a real license, consistent structure, and a few automation guardrails. None of it is technically hard — it's just the first thing that gets skipped under time pressure, and the first thing an evaluator, hiring manager, or downstream user notices. This skill exists so it never gets skipped.

Apply it any time you create a new repo, hand off a project, or someone says something like "clean this up," "make this repo look professional," "get this ready for GitHub," or "prep this for open source."

## Before you start: figure out the scope

Work out which of these three situations you're in — it changes how much of this skill to apply:

| Situation | What to do |
|---|---|
| **Brand-new repo from scratch** | Full scaffold. Follow Steps 1–9 in order. |
| **Existing repo, "make it better"** | Audit first (`scripts/validate_repo.py`), then fill only the gaps it finds. Don't rewrite things that already meet the bar. |
| **One specific artifact** ("write me a README", "add a LICENSE") | Jump straight to that step. Don't scaffold the rest of the repo unless asked. |

A quick `ls -la` and `git status` in the working directory usually settles which situation you're in.

## Research / academic software: a different profile, not an exception

If the repo is software released alongside research — a lab tool, a method implementation tied to a paper, anything with (or headed for) a Zenodo/arXiv DOI or an ORCID-bearing author — use the **research profile** instead of the defaults below. It's based on a real, consistent pattern observed across a working research group's published repositories, and it **overrides** several of this skill's generic defaults rather than just adding to them: GPL-3.0-or-later instead of MIT as the default license, a `CITATION.cff` file plus a README "Citation" section with BibTeX (entirely absent from the generic flow), MkDocs+Material instead of an unspecified docs setup, `uv`/`ruff`/`ty` instead of generic pip/lint placeholders, and — notably — *skipping* most community-health files (Step 5) by default rather than including them, since real repos of this kind consistently omit CODE_OF_CONDUCT/SECURITY/issue+PR templates until the project has grown well past its original size. Full detail, the reasoning, and ready-to-use templates are in `references/research-software.md`; the fast path is:

```bash
python scripts/init_repo.py --name mytool --profile research --language python \
    --author "Jane Doe" --github-user janedoe --output-dir ./mytool
```

Trigger this profile on cues like "materials science," "computational research," "cite this software," a mentioned paper/DOI, or a user who's clearly releasing lab code — read `references/research-software.md` before scaffolding once any of these show up. Everything else in this file still applies to a research repo except where that reference explicitly overrides it.

## Step 1: Gather the essentials

Five things determine everything else. Infer as many as you can from context — existing files, a git remote, `package.json`/`pyproject.toml`/`go.mod`, or the conversation itself — before asking the user directly:

1. **Project name** — from the folder name, an existing manifest file, or ask.
2. **One-sentence description** — what it does and who it's for.
3. **Primary language / ecosystem** — Python, Node/TypeScript, Go, Rust, Java, or generic/polyglot. This decides the layout (`references/repo-structure.md`) and which CI template to use.
4. **License** — see `references/licensing-guide.md` if the choice isn't obvious. Default assumption for a new open-source project is MIT. Never invent a license choice for a closed-source or internal repo — ask, or omit LICENSE entirely.
5. **Visibility and audience** — public open-source project, internal company repo, or personal/private. This determines how much community infrastructure is worth including; a private solo repo doesn't need a Code of Conduct or issue templates.

Don't interrogate the user with all five questions up front if most are inferable — state your assumptions in one line and move on. Only stop and ask when the license or visibility genuinely can't be inferred, since getting those wrong is the costliest mistake here.

## Step 2: Repo structure

Lay out directories before writing files into them. `references/repo-structure.md` has full per-language conventions (Python src-layout, Node/TypeScript, Go, Rust, Java, and monorepos). The universal shape, regardless of language:

```
project-name/
├── .github/
│   ├── workflows/
│   ├── ISSUE_TEMPLATE/
│   ├── PULL_REQUEST_TEMPLATE.md
│   ├── CODEOWNERS
│   └── dependabot.yml
├── src/                 (or the language-idiomatic equivalent)
├── tests/
├── docs/                (only once docs outgrow the README)
├── .gitignore
├── .editorconfig
├── .gitattributes
├── LICENSE
├── README.md
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
├── SECURITY.md
└── CHANGELOG.md
```

Not every repo needs every file — Step 5's table says what to skip and when.

## Step 3: README — the one file that matters most

The README is the repo's front door; most visitors decide whether to keep reading within the first few seconds. Full section-by-section guidance and good/bad examples live in `references/readme-standards.md`. Start from `assets/README.template.md` and fill it in rather than writing one from a blank page.

Non-negotiable sections, in this order: title and one-line pitch, badges, what it does and why it exists, install, a quickstart/usage example, an API or configuration reference (inline or linked to `docs/`), how to contribute (linking to CONTRIBUTING.md), and license. Everything else is optional and situational.

**The quickstart must be copy-pasteable.** If a reader can't get from a fresh clone to a running example by pasting your commands verbatim, the quickstart has failed — test it yourself before calling it done.

## Step 4: License

Check `references/licensing-guide.md` if the choice isn't obvious. Then get the actual license text — never write license text from memory or approximate it, it has to be exact:

```bash
python scripts/init_repo.py --license mit --author "Jane Doe" --output-dir .
```

This fetches the canonical text live from GitHub's license API (`api.github.com/licenses/<key>`) and writes a correctly formatted `LICENSE` file with the year and holder name substituted in. If outbound network access isn't available, the script falls back to a bundled copy of the most common permissive licenses (MIT, Apache-2.0) and otherwise tells you to pull the exact text from https://choosealicense.com rather than approximating it.

## Step 5: Community health files

Scale these to the audience identified in Step 1 — a private solo repo doesn't need most of this, while a public open-source project benefits from all of it. Templates live in `assets/`; full guidance on what belongs in each is in `references/community-health-files.md`.

| File | Include when | Template |
|---|---|---|
| `CONTRIBUTING.md` | Anyone besides you might submit a PR | `assets/CONTRIBUTING.template.md` |
| `CODE_OF_CONDUCT.md` | Public project accepting outside contributions | `assets/CODE_OF_CONDUCT.template.md` |
| `SECURITY.md` | Any public project, especially a library others depend on or one handling user data | `assets/SECURITY.template.md` |
| `SUPPORT.md` | Project gets enough usage questions to need a documented channel | `assets/SUPPORT.template.md` |
| `CODEOWNERS` | More than one maintainer, or you want auto-requested reviewers | `assets/CODEOWNERS.template` |
| Issue templates | Public project taking bug reports or feature requests | `assets/ISSUE_TEMPLATE/` |
| PR template | Any project with more than one contributor | `assets/PULL_REQUEST_TEMPLATE.md` |

## Step 6: Git hygiene

- **`.gitignore`** — language-specific, fetched live from GitHub's official `github/gitignore` templates by `scripts/init_repo.py`, or hand-picked from `references/repo-structure.md` if offline.
- **`.editorconfig`** — copy `assets/.editorconfig` verbatim; it's language-agnostic.
- **`.gitattributes`** — copy `assets/.gitattributes`; it normalizes line endings and marks generated/binary files so diffs stay clean.
- **Commit messages and branching** — `references/git-and-versioning.md` covers Conventional Commits and a lightweight trunk-based branching model. Don't rewrite an existing repo's history to match; apply going forward only.

## Step 7: CI/CD and automation

Minimum viable CI for any repo with code: lint and test on every push and PR. Full patterns and per-language notes are in `references/ci-cd-and-automation.md`; ready-to-use workflow files are in `assets/workflows/`. Copy the one matching Step 1's language, then adjust the actual lint/test commands to match the project — a template with the wrong test command is worse than no CI, since it fails loudly on every PR for the wrong reason.

At minimum, wire up:

1. **CI** (`assets/workflows/ci-python.yml` or `ci-node.yml`) — lint and test on push/PR.
2. **CodeQL** (`assets/workflows/codeql.yml`) — free static security scanning for public repos.
3. **Dependabot** (`assets/dependabot.yml.template` → `.github/dependabot.yml`) — automated dependency update PRs.

Release automation (`assets/workflows/release.yml`) and a stale-issue bot (`assets/workflows/stale.yml`) are worth adding once a project has actual users — skip them on a brand-new, empty repo, since they'll have nothing to do yet.

## Step 8: Badges and polish

Add badges to the top of the README only for things that are actually true and actually maintained: CI status, latest release version, license, package registry version (PyPI/npm), test coverage if it's tracked. A badge for a workflow that doesn't exist yet, or a coverage badge with no coverage tooling behind it, is worse than no badge at all — it's a claim the repo can't back up.

## Step 9: Validate before calling it done

Run the audit script against the finished repo and fix anything it flags:

```bash
python scripts/validate_repo.py --path /path/to/repo
```

This produces a scored checklist report (`references/repo-checklist.md` explains what it checks and why each item matters) plus a basic scan for accidentally committed secrets. Treat a low score as a to-do list, not a verdict — some items genuinely don't apply to every repo (see Step 5's table), and the report says so rather than penalizing them.

## Using the scripts directly

- **`scripts/init_repo.py`** — scaffolds a new repo, or fills in missing standard files in an existing one. Never overwrites a file that already exists unless `--force` is passed. Add `--profile research` for the academic/research-software profile (`references/research-software.md`). Run `python scripts/init_repo.py --help` for all flags.
- **`scripts/validate_repo.py`** — audits a repo and prints a Markdown report (or JSON with `--json`). Run `python scripts/validate_repo.py --help` for all flags.

Both are pure Python 3 standard library — no `pip install` required.

## Examples

**Example 1 — new project from scratch**
User says: "I just finished a Python CLI tool called `pixsort` that organizes photos by date. Set it up as a proper GitHub repo, MIT license, my name is Jane Doe."
Actions: confirm the one-line description → `python scripts/init_repo.py --name pixsort --language python --license mit --author "Jane Doe" --description "..."` → fill in the generated README's usage section with `pixsort`'s actual CLI flags → run `validate_repo.py` → report the score and what's left to fill in (only Jane knows the real example commands, so flag that the quickstart still needs her input).

**Example 2 — audit an existing repo**
User says: "does my repo look professional enough to put on my resume?"
Actions: run `validate_repo.py --path .` → walk through the report with the user, prioritizing the highest-impact gaps first — usually missing LICENSE, a thin README, or no CI — rather than listing every item with equal weight.

**Example 3 — single artifact**
User says: "write me a CONTRIBUTING.md for this repo"
Actions: skim the existing repo for language, test command, and branch model if any → fill `assets/CONTRIBUTING.template.md` with the specifics found rather than generic placeholders → don't touch any other file.

**Example 4 — research software**
User says: "I'm releasing the Python code behind our paper on grain-boundary energy prediction. Set up the repo — my name's Alex Kim, GitHub handle akim-lab."
Actions: read `references/research-software.md` → `python scripts/init_repo.py --name <tool> --profile research --language python --author "Alex Kim" --github-user akim-lab --description "..."` → flag clearly that the `CITATION.cff` DOI and the README's citation block are placeholders until a Zenodo release exists → skip suggesting CODE_OF_CONDUCT/issue templates unless Alex asks, since the profile already reflects that this ecosystem skips them by default.

## Troubleshooting

**`init_repo.py` can't reach the network, or license/`.gitignore` text comes back empty**
Expected in sandboxed environments without outbound access. The script prints which file it couldn't fetch and falls back to a bundled minimal version (MIT/Apache-2.0 license text, a short generic `.gitignore`). Point the user to the live source (`https://choosealicense.com/licenses/<key>/`, `https://github.com/github/gitignore`) for anything the fallback doesn't cover.

**Target directory already has files**
`init_repo.py` never overwrites an existing file by default — it skips it and reports what it skipped in the summary. Use `--force` only if the user explicitly asks to overwrite.

**User wants a license that isn't MIT/Apache-2.0/GPL-3.0/BSD-3-Clause/MPL-2.0**
`references/licensing-guide.md` covers the common ones; `init_repo.py --license <spdx-id>` works for anything in GitHub's license API. For anything obscure or custom — dual-licensing, a commercial EULA — that's a legal question. Say so and point to a lawyer rather than drafting custom license terms.

**Repo is a monorepo or has multiple packages**
The single-package layout in Step 2 doesn't apply directly — read the monorepo note in `references/repo-structure.md` before scaffolding.

**User's project is private or internal-only**
Skip CODE_OF_CONDUCT, issue templates, and public badges — they signal "outside contributors welcome," which is noise on a repo that isn't. Keep README, LICENSE (if applicable — many internal repos have none), CONTRIBUTING (for internal teammates), and CI.
