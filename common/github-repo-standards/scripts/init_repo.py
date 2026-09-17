#!/usr/bin/env python3
"""
init_repo.py — Scaffold a new GitHub repository to the github-repo-standards
skill's standard, or fill in missing standard files in an existing one.

Pure standard library. No pip installs required.

Usage:
    python init_repo.py --name my-project --language python --license mit \
        --author "Jane Doe" --description "A tool that does X" \
        --output-dir ./my-project

    # Research/academic software profile (see references/research-software.md):
    # GPL-3.0-or-later default, CITATION.cff, mkdocs.yml, .pre-commit-config.yaml,
    # .python-version, uv/ruff/ty-based CI, and community-health files skipped
    # by default (pass --with-community-files to keep them).
    python init_repo.py --name mytool --profile research --language python \
        --author "Jane Doe" --github-user janedoe --output-dir ./mytool

    python init_repo.py --help

Design notes:
- Never overwrites an existing file unless --force is passed.
- Tries to fetch canonical LICENSE and .gitignore text live from GitHub's
  own APIs (api.github.com, raw.githubusercontent.com). Falls back to a
  small bundled set if the network isn't reachable, and never fabricates
  or approximates license text.
- Every generated file uses {{PLACEHOLDER}} tokens where the caller's real
  content (a real usage example, a real API reference) still needs to be
  filled in by hand — the script fills in what it *knows*, not what it
  would have to invent.
"""

import argparse
import datetime
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parent.parent
ASSETS_DIR = SKILL_ROOT / "assets"

TIMEOUT = 6  # seconds; fail fast and fall back rather than hang

# ---------------------------------------------------------------------------
# Language -> layout / gitignore template / CI workflow mapping
# ---------------------------------------------------------------------------

LANGUAGE_CONFIG = {
    "python": {
        "gitignore_template": "Python",
        "dirs": ["src", "tests"],
        "ci_workflow": "ci-python.yml",
    },
    "node": {
        "gitignore_template": "Node",
        "dirs": ["src", "tests"],
        "ci_workflow": "ci-node.yml",
    },
    "go": {
        "gitignore_template": "Go",
        "dirs": ["cmd", "internal", "pkg"],
        "ci_workflow": "ci-node.yml",  # placeholder ref; see note printed below
    },
    "rust": {
        "gitignore_template": "Rust",
        "dirs": ["src", "tests"],
        "ci_workflow": "ci-node.yml",
    },
    "java": {
        "gitignore_template": "Java",
        "dirs": ["src/main/java", "src/test/java"],
        "ci_workflow": "ci-node.yml",
    },
    "generic": {
        "gitignore_template": None,
        "dirs": ["src", "tests"],
        "ci_workflow": None,
    },
}

# Profile-level defaults. "research" matches the pattern documented in
# references/research-software.md — observed consistently across a working
# set of published academic research-software repos. Where this conflicts
# with the "generic" profile's defaults, research-profile behavior wins for
# any repo using this profile; see that reference file for the "why."
PROFILE_DEFAULT_LICENSE = {
    "generic": "mit",
    "research": "gpl-3.0-or-later",
}

# Fallback license text used only when the live fetch fails. Kept to the two
# shortest, most common permissive licenses — both explicitly designed to be
# copied verbatim into a project's LICENSE file as part of applying them.
FALLBACK_LICENSES = {
    "mit": """MIT License

Copyright (c) {year} {author}

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
""",
    "apache-2.0": None,  # too long to vendor sensibly offline; see NOTE below
}

FALLBACK_GITIGNORE = """# Fallback minimal .gitignore (offline mode — see README.md note)
# Get the full, language-specific version from https://github.com/github/gitignore

# OS files
.DS_Store
Thumbs.db

# Editors
.vscode/
.idea/
*.swp

# Dependencies / build output
node_modules/
dist/
build/
*.egg-info/
__pycache__/
*.pyc
.venv/
venv/
target/
"""

NOTE_NO_LICENSE_FETCHED = """LICENSE text for "{key}" could not be fetched (no network access) and isn't
bundled offline. Get the exact, official text from:

    https://choosealicense.com/licenses/{key}/
    https://api.github.com/licenses/{key}

then replace this file's contents with it. Never approximate or paraphrase
license text — it has to be the exact, official wording to be valid.
"""

# GitHub's license API only recognizes base SPDX keys (e.g. "gpl-3.0"), not
# the "-or-later"/"-only" suffix variants some projects declare in badges
# and CITATION.cff. The license *body text* is identical either way — the
# suffix communicates which future license versions apply, not a different
# document — so strip it only for the purposes of fetching text, while the
# original key (with suffix) is still what's displayed to the user.
LICENSE_DISPLAY_NAMES = {
    "mit": "MIT",
    "apache-2.0": "Apache-2.0",
    "gpl-3.0": "GPL-3.0",
    "gpl-3.0-or-later": "GPL-3.0-or-later",
    "gpl-2.0": "GPL-2.0",
    "lgpl-3.0": "LGPL-3.0",
    "lgpl-3.0-or-later": "LGPL-3.0-or-later",
    "agpl-3.0": "AGPL-3.0",
    "bsd-2-clause": "BSD-2-Clause",
    "bsd-3-clause": "BSD-3-Clause",
    "mpl-2.0": "MPL-2.0",
    "epl-2.0": "EPL-2.0",
    "unlicense": "Unlicense",
}


def license_api_key(license_key: str) -> str:
    key = license_key.lower()
    for suffix in ("-or-later", "-only"):
        if key.endswith(suffix):
            return key[: -len(suffix)]
    return key


def license_display_name(license_key: str) -> str:
    return LICENSE_DISPLAY_NAMES.get(license_key.lower(), license_key.upper())


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def log(msg):
    print(msg)


def fetch_json(url):
    req = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json",
                                                 "User-Agent": "github-repo-standards-skill"})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        return json.loads(resp.read().decode("utf-8"))


def fetch_text(url):
    req = urllib.request.Request(url, headers={"User-Agent": "github-repo-standards-skill"})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        return resp.read().decode("utf-8")


def write_file(path: Path, content: str, force: bool, created, skipped):
    if path.exists() and not force:
        skipped.append(str(path))
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    created.append(str(path))


def read_asset(rel_path: str) -> str:
    p = ASSETS_DIR / rel_path
    if not p.exists():
        raise FileNotFoundError(f"Missing bundled asset: {p}")
    return p.read_text(encoding="utf-8")


def fill_placeholders(text: str, values: dict) -> str:
    for key, val in values.items():
        text = text.replace("{{" + key + "}}", val)
    return text


# ---------------------------------------------------------------------------
# License handling
# ---------------------------------------------------------------------------

def get_license_text(license_key: str, author: str, year: str):
    """Returns (text, source) where source is 'live', 'fallback', or 'unavailable'."""
    license_key = license_key.lower()
    api_key = license_api_key(license_key)

    # 1. Try live fetch from GitHub's license API — this is the canonical
    #    source and keeps the text exact and up to date. Uses api_key (the
    #    -or-later/-only suffix stripped) since that's what GitHub's API
    #    recognizes; the fetched body text is correct for either form.
    try:
        data = fetch_json(f"https://api.github.com/licenses/{api_key}")
        body = data.get("body", "")
        if body:
            body = body.replace("[year]", year).replace("[yyyy]", year)
            body = body.replace("[fullname]", author)
            body = body.replace("[fullname copyright owner]", author)
            body = body.replace("[name of copyright owner]", author)
            body = body.replace("[name of author]", author)
            return body, "live"
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, OSError, ValueError):
        pass

    # 2. Fall back to a small bundled set (currently just MIT).
    fallback = FALLBACK_LICENSES.get(api_key)
    if fallback:
        return fallback.format(year=year, author=author), "fallback"

    # 3. Give up gracefully with clear next steps rather than inventing text.
    return NOTE_NO_LICENSE_FETCHED.format(key=api_key), "unavailable"


def get_gitignore_text(language: str):
    config = LANGUAGE_CONFIG.get(language, LANGUAGE_CONFIG["generic"])
    template_name = config.get("gitignore_template")
    if not template_name:
        return FALLBACK_GITIGNORE, "fallback"
    try:
        url = f"https://raw.githubusercontent.com/github/gitignore/main/{template_name}.gitignore"
        return fetch_text(url), "live"
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, OSError):
        return FALLBACK_GITIGNORE, "fallback"


# ---------------------------------------------------------------------------
# Main scaffold logic
# ---------------------------------------------------------------------------

def scaffold(args):
    out = Path(args.output_dir).resolve()
    out.mkdir(parents=True, exist_ok=True)

    # Resolve the license: an explicit --license always wins; otherwise fall
    # back to the profile's default (MIT for generic, GPL-3.0-or-later for
    # research — see PROFILE_DEFAULT_LICENSE and references/research-software.md).
    license_key = args.license or PROFILE_DEFAULT_LICENSE.get(args.profile, "mit")
    # research profile skips community-health scaffolding by default, since
    # that's what was actually observed — opt back in with --with-community-files.
    effective_minimal = args.minimal or (args.profile == "research" and not args.with_community_files)

    created, skipped = [], []
    year = str(datetime.date.today().year)
    values = {
        "PROJECT_NAME": args.name,
        "REPO_NAME": args.name,
        "ONE_LINE_DESCRIPTION": args.description or "TODO: one-sentence description of what this project does and who it's for.",
        "AUTHOR": args.author or "TODO: author name",
        "GITHUB_USER": args.github_user or "TODO-github-username",
        "YEAR": year,
        "LANGUAGE": args.language,
        "LICENSE_NAME": license_display_name(license_key) if license_key != "none" else "UNLICENSED",
        "PYTHON_VERSION": args.python_version,
    }

    config = LANGUAGE_CONFIG.get(args.language, LANGUAGE_CONFIG["generic"])

    # 1. Directory layout
    for d in config["dirs"]:
        (out / d).mkdir(parents=True, exist_ok=True)
        gitkeep = out / d / ".gitkeep"
        if not any((out / d).iterdir()):
            gitkeep.write_text("")
    (out / "docs").mkdir(exist_ok=True)
    (out / ".github" / "workflows").mkdir(parents=True, exist_ok=True)
    (out / ".github" / "ISSUE_TEMPLATE").mkdir(parents=True, exist_ok=True)

    # 2. README (research profile uses the citation-oriented template)
    readme_template = "README.research.template.md" if args.profile == "research" else "README.template.md"
    readme = fill_placeholders(read_asset(readme_template), values)
    write_file(out / "README.md", readme, args.force, created, skipped)

    # 3. LICENSE
    if license_key != "none":
        text, source = get_license_text(license_key, values["AUTHOR"], year)
        write_file(out / "LICENSE", text, args.force, created, skipped)
        if source != "live":
            log(f"  note: LICENSE text came from '{source}' (not a live fetch) — verify it before publishing.")

    # 4. .gitignore
    gi_text, gi_source = get_gitignore_text(args.language)
    write_file(out / ".gitignore", gi_text, args.force, created, skipped)
    if gi_source != "live":
        log("  note: .gitignore is a generic fallback — replace with the language-specific "
            "version from https://github.com/github/gitignore when you have network access.")

    # 5. Git hygiene files
    write_file(out / ".editorconfig", read_asset(".editorconfig"), args.force, created, skipped)
    write_file(out / ".gitattributes", read_asset(".gitattributes"), args.force, created, skipped)

    if not effective_minimal:
        # 6. Community health files
        write_file(out / "CONTRIBUTING.md", fill_placeholders(read_asset("CONTRIBUTING.template.md"), values),
                   args.force, created, skipped)
        write_file(out / "CODE_OF_CONDUCT.md", fill_placeholders(read_asset("CODE_OF_CONDUCT.template.md"), values),
                   args.force, created, skipped)
        write_file(out / "SECURITY.md", fill_placeholders(read_asset("SECURITY.template.md"), values),
                   args.force, created, skipped)
        write_file(out / "SUPPORT.md", fill_placeholders(read_asset("SUPPORT.template.md"), values),
                   args.force, created, skipped)
        write_file(out / "CHANGELOG.md", fill_placeholders(read_asset("CHANGELOG.template.md"), values),
                   args.force, created, skipped)
        write_file(out / ".github" / "CODEOWNERS", fill_placeholders(read_asset("CODEOWNERS.template"), values),
                   args.force, created, skipped)
        write_file(out / ".github" / "PULL_REQUEST_TEMPLATE.md", read_asset("PULL_REQUEST_TEMPLATE.md"),
                   args.force, created, skipped)
        write_file(out / ".github" / "ISSUE_TEMPLATE" / "bug_report.yml",
                   fill_placeholders(read_asset("ISSUE_TEMPLATE/bug_report.yml"), values),
                   args.force, created, skipped)
        write_file(out / ".github" / "ISSUE_TEMPLATE" / "feature_request.yml",
                   read_asset("ISSUE_TEMPLATE/feature_request.yml"), args.force, created, skipped)
        write_file(out / ".github" / "ISSUE_TEMPLATE" / "config.yml",
                   fill_placeholders(read_asset("ISSUE_TEMPLATE/config.yml"), values),
                   args.force, created, skipped)
        write_file(out / ".github" / "dependabot.yml",
                   fill_placeholders(read_asset("dependabot.yml.template"), values),
                   args.force, created, skipped)

    # 7. Research profile: citation + tooling infrastructure (independent of
    #    --minimal — these aren't community-health files, they're the
    #    citation/reproducibility infra this profile is specifically for).
    if args.profile == "research":
        write_file(out / "CITATION.cff", fill_placeholders(read_asset("CITATION.cff.template"), values),
                   args.force, created, skipped)
        write_file(out / "mkdocs.yml", fill_placeholders(read_asset("mkdocs.yml.template"), values),
                   args.force, created, skipped)
        write_file(out / ".pre-commit-config.yaml", read_asset(".pre-commit-config.yaml"),
                   args.force, created, skipped)
        if args.language == "python":
            write_file(out / ".python-version", fill_placeholders(read_asset("python-version.template"), values),
                       args.force, created, skipped)
        (out / "docs" / "assets").mkdir(parents=True, exist_ok=True)

    if not args.no_ci:
        # 8. CI workflow. Research profile (Python) uses the uv/ruff/ty-based
        #    tests.yml + lint.yml pair observed in the pattern; CodeQL wasn't
        #    observed there, so it's left out by default for that profile —
        #    copy assets/workflows/codeql.yml manually if wanted.
        if args.profile == "research" and args.language == "python":
            write_file(out / ".github" / "workflows" / "tests.yml", read_asset("workflows/tests.yml"),
                       args.force, created, skipped)
            write_file(out / ".github" / "workflows" / "lint.yml", read_asset("workflows/lint.yml"),
                       args.force, created, skipped)
        else:
            ci_name = config.get("ci_workflow")
            if args.language in ("go", "rust", "java") and ci_name:
                log(f"  note: no dedicated CI template for '{args.language}' yet — using ci-node.yml as a "
                    f"structural starting point. Replace the install/lint/test commands with {args.language}-native ones "
                    f"(see references/ci-cd-and-automation.md).")
            if ci_name:
                write_file(out / ".github" / "workflows" / "ci.yml", read_asset(f"workflows/{ci_name}"),
                           args.force, created, skipped)
            write_file(out / ".github" / "workflows" / "codeql.yml", read_asset("workflows/codeql.yml"),
                       args.force, created, skipped)

    # 8. Summary
    log(f"\nScaffolded '{args.name}' into {out}")
    log(f"  {len(created)} file(s) created, {len(skipped)} skipped (already existed).")
    if created:
        log("\nCreated:")
        for f in created:
            log(f"  + {Path(f).relative_to(out)}")
    if skipped:
        log("\nSkipped (already existed — use --force to overwrite):")
        for f in skipped:
            log(f"  = {Path(f).relative_to(out)}")

    log("\nStill needs a human (or another pass of this conversation) to fill in:")
    log("  - A real, tested quickstart example in README.md")
    log("  - Any TODO: placeholders left in the generated files")
    if args.profile == "research":
        log("  - CITATION.cff and the README Citation section: version, date, DOI (mint one via Zenodo), authors/ORCID")
        log("  - .pre-commit-config.yaml: pin the 'rev:' fields to current release tags")
        log("  - mkdocs.yml: fill in the nav to match this project's real docs pages")
    else:
        log("  - Actual lint/test commands in .github/workflows/ci.yml")
    log("\nRun scripts/validate_repo.py against this directory to check the result.")


def main():
    parser = argparse.ArgumentParser(description="Scaffold a repo to the github-repo-standards skill's standard.")
    parser.add_argument("--name", required=True, help="Project / repo name.")
    parser.add_argument("--description", default="", help="One-sentence description.")
    parser.add_argument("--language", default="generic",
                        choices=sorted(LANGUAGE_CONFIG.keys()), help="Primary language/ecosystem.")
    parser.add_argument("--license", default=None,
                        help="SPDX-style key (mit, apache-2.0, gpl-3.0, bsd-3-clause, mpl-2.0, unlicense) or 'none'. "
                             "Defaults to the active --profile's default (mit for generic, gpl-3.0-or-later for research).")
    parser.add_argument("--author", default="", help="Copyright holder / author name.")
    parser.add_argument("--github-user", default="", help="GitHub username or org, used in badge URLs.")
    parser.add_argument("--output-dir", default=".", help="Directory to scaffold into (created if missing).")
    parser.add_argument("--profile", default="generic", choices=["generic", "research"],
                        help="'generic' (default) or 'research' — the academic/research-software profile from "
                             "references/research-software.md: GPL-3.0-or-later default, CITATION.cff, mkdocs.yml, "
                             ".pre-commit-config.yaml, .python-version, uv/ruff/ty-based CI, and community-health "
                             "files skipped by default (see --with-community-files).")
    parser.add_argument("--python-version", default="3.12",
                        help="Python version to pin in .python-version (research profile only). Default: 3.12.")
    parser.add_argument("--with-community-files", action="store_true",
                        help="With --profile research: also generate CONTRIBUTING/CODE_OF_CONDUCT/SECURITY/issue "
                             "and PR templates, which that profile skips by default.")
    parser.add_argument("--minimal", action="store_true",
                        help="Skip community health files (CONTRIBUTING, CODE_OF_CONDUCT, SECURITY, issue/PR templates). "
                             "Use for private/internal repos. (research profile skips these by default already.)")
    parser.add_argument("--no-ci", action="store_true", help="Skip GitHub Actions workflow files.")
    parser.add_argument("--force", action="store_true", help="Overwrite existing files instead of skipping them.")
    args = parser.parse_args()

    scaffold(args)


if __name__ == "__main__":
    main()
