**Research/academic software:** if `references/research-software.md` applies to this repo, skip nearly everything on this page by default — that profile's real-world pattern consistently omits CODE_OF_CONDUCT, SECURITY.md, issue/PR templates, and CODEOWNERS even in public, well-starred repos, in favor of a lightweight `Report a Bug | Request a Feature` link row instead. Add any of these back in once the project actually grows a contributor base, exactly as the general guidance below already recommends — the research default just starts from "skip" instead of "include."

# Community health files

GitHub calls this specific set of files "community health files" and actually scores a repo against them under the **Insights → Community Standards** tab — this isn't just convention, it's something GitHub itself surfaces to visitors as a maintenance signal. They can live at the repo root, inside `.github/`, or inside `docs/`; GitHub checks all three locations. For an organization with many repos, the same files placed in a special `.github`-named repo become the **org-wide default** for any repo that doesn't have its own copy.

Scale which of these you add to the project's actual audience — see the table in `SKILL.md` Step 5. Adding all of them to a private, single-maintainer repo is just noise; skipping all of them on a public project asking for outside contributions makes the project harder to contribute to than it needs to be.

## CONTRIBUTING.md

**Purpose:** answers "how do I actually get a change merged here?" without the maintainer re-explaining it in every PR.

A good one covers, in order:
1. What to do before writing code (small fix → just PR it; larger change → open an issue first to discuss direction).
2. Dev environment setup — exact, copy-pasteable commands.
3. How to run the test suite.
4. Coding style / linter, and the command to run it.
5. Commit message convention, if the project has one (see `references/git-and-versioning.md`).
6. The PR process itself: branch naming, what CI must pass, what review looks like.

Common mistake: a CONTRIBUTING.md that's pure boilerplate with no project-specific commands — it should contain the *actual* test/lint commands for this project, not a generic placeholder left unfilled.

## CODE_OF_CONDUCT.md

**Purpose:** sets behavioral expectations up front so they don't have to be improvised during the first conflict. This matters most for public projects with (or hoping for) outside contributors; it's largely unnecessary for a private solo repo.

A good one is short, states expected and unacceptable behavior concretely (not just "be nice"), says where to report a problem, and says roughly what happens when it's violated. Keep the reporting contact real and monitored — a Code of Conduct with a dead-end contact is worse than none, since it sets an expectation it can't meet.

## SECURITY.md

**Purpose:** gives security researchers a clear, private channel to report a vulnerability, instead of them defaulting to a public issue (which discloses the vulnerability to everyone, including attackers, before it's fixed).

A good one states: which versions are currently supported with security fixes, exactly how to report privately (GitHub's built-in private vulnerability reporting under the Security tab is the easiest option — no separate infrastructure needed), what response time to expect, and a request for coordinated disclosure (give the maintainers time to fix it before going public). Strongly recommended for any public library or anything handling user data, even a small one — being small doesn't make a vulnerability report less likely, just less anticipated.

## SUPPORT.md

**Purpose:** routes usage questions away from the bug tracker. Only worth adding once a project has enough traffic that this routing problem is real — a brand-new project doesn't need it yet.

Point questions at Discussions (or a labeled issue type if Discussions isn't enabled), point bugs at Issues, point security reports at SECURITY.md, and set a rough expectation for response time so people aren't left wondering if they've been ignored.

## CODEOWNERS

**Purpose:** automatically requests the right reviewers on a PR based on which files it touches, and can be wired into branch protection to require an owner's approval. Only useful once there's more than one maintainer — with a single maintainer, it's redundant with "you review everything anyway."

Syntax is `path-pattern @user-or-team`, evaluated top to bottom with later matches overriding earlier ones — most repos want one default `*` owner line plus a few overrides for specific directories.

## Issue templates (`.github/ISSUE_TEMPLATE/`)

**Purpose:** gets the information a maintainer actually needs (repro steps, version, environment) on the first message instead of after three rounds of "can you provide more detail?" GitHub's newer YAML-based issue forms (`.yml`, structured fields with required/optional) are strictly better than the older free-text Markdown templates for anything that needs specific fields — use YAML forms unless there's a reason not to. A `config.yml` alongside them controls whether a "blank issue" option remains available and can add links to other support channels.

Include at minimum: a bug report form and a feature request form. Only relevant once a project takes outside bug reports — skip for a private repo with no external users.

## Pull request template (`PULL_REQUEST_TEMPLATE.md`)

**Purpose:** gets a PR description that actually explains *what* and *why*, plus a self-review checklist, instead of an empty description or just a linked issue number.

A good one asks: what changed and why, how it was tested, and a short checklist (tests pass, docs updated, self-reviewed). Keep the checklist short — a 15-item checklist gets rubber-stamped, not actually followed.

## Putting it together

`scripts/init_repo.py` (without `--minimal`) generates all of these from `assets/`, pre-filled with the project name and other known values. Review what it fills in versus what's still a `TODO:` placeholder — the script fills in what it can infer, not what only a human knows (real dev-setup commands, a real security contact, real supported-version numbers).
