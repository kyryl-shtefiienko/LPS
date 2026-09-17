#!/usr/bin/env python3
"""
validate_repo.py — Audit a repository against the github-repo-standards
skill's checklist (see references/repo-checklist.md) and print a scored,
actionable Markdown report.

Pure standard library. No pip installs required.

Usage:
    python validate_repo.py --path /path/to/repo
    python validate_repo.py --path . --json
    python validate_repo.py --path . --strict   # also require situational items

Exit code is always 0 — this is a report, not a gate. Use --json if you want
to wire pass/fail into something else.
"""

import argparse
import json
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Checklist definition
# ---------------------------------------------------------------------------
# Each check: id, category, human label, "required" (always expected) vs
# "situational" (only expected for certain repos — see notes), a check
# function taking the repo Path, and a remediation pointer back into the
# skill's own reference/asset files.

CHECKS = []


def check(id_, category, label, required, remediation):
    def decorator(fn):
        CHECKS.append({
            "id": id_, "category": category, "label": label,
            "required": required, "remediation": remediation, "fn": fn,
        })
        return fn
    return decorator


def exists_any(repo: Path, *names):
    return any((repo / n).exists() for n in names)


def read(repo: Path, name: str) -> str:
    p = repo / name
    if not p.exists():
        return ""
    try:
        return p.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return ""


@check("readme_exists", "Documentation", "README.md exists", True,
       "Run scripts/init_repo.py or start from assets/README.template.md (Step 3 in SKILL.md).")
def _(repo):
    return exists_any(repo, "README.md", "README.rst", "README")


@check("readme_sections", "Documentation",
       "README covers install / usage / license", True,
       "See references/readme-standards.md for the required section list.")
def _(repo):
    text = read(repo, "README.md").lower()
    if not text:
        return False
    has_install = bool(re.search(r"#+\s*(install|getting started|setup)", text))
    has_usage = bool(re.search(r"#+\s*(usage|quickstart|quick start|example)", text))
    has_license_mention = "license" in text
    return has_install and has_usage and has_license_mention


@check("readme_not_stub", "Documentation", "README is more than a one-line stub", True,
       "Flesh out assets/README.template.md's sections — see references/readme-standards.md.")
def _(repo):
    text = read(repo, "README.md")
    return len(text.split()) >= 60


@check("license_exists", "Legal", "LICENSE file exists", True,
       "Run scripts/init_repo.py --license <key>, or see references/licensing-guide.md to choose one.")
def _(repo):
    return exists_any(repo, "LICENSE", "LICENSE.md", "LICENSE.txt", "COPYING")


@check("contributing_exists", "Community health", "CONTRIBUTING.md exists", False,
       "Situational: needed once outside contributors are expected. See assets/CONTRIBUTING.template.md.")
def _(repo):
    return exists_any(repo, "CONTRIBUTING.md", ".github/CONTRIBUTING.md")


@check("code_of_conduct_exists", "Community health", "CODE_OF_CONDUCT.md exists", False,
       "Situational: needed for public projects accepting outside contributions. See assets/CODE_OF_CONDUCT.template.md.")
def _(repo):
    return exists_any(repo, "CODE_OF_CONDUCT.md", ".github/CODE_OF_CONDUCT.md")


@check("security_md_exists", "Community health", "SECURITY.md exists", False,
       "Situational: strongly recommended for public projects/libraries. See assets/SECURITY.template.md.")
def _(repo):
    return exists_any(repo, "SECURITY.md", ".github/SECURITY.md")


@check("codeowners_exists", "Community health", "CODEOWNERS exists", False,
       "Situational: useful once there's more than one maintainer. See assets/CODEOWNERS.template.")
def _(repo):
    return exists_any(repo, "CODEOWNERS", ".github/CODEOWNERS", "docs/CODEOWNERS")


@check("issue_templates_exist", "Community health", "Issue templates exist", False,
       "Situational: for public projects taking bug reports. See assets/ISSUE_TEMPLATE/.")
def _(repo):
    d = repo / ".github" / "ISSUE_TEMPLATE"
    return d.is_dir() and any(d.iterdir())


@check("pr_template_exists", "Community health", "Pull request template exists", False,
       "Situational: useful once there's more than one contributor. See assets/PULL_REQUEST_TEMPLATE.md.")
def _(repo):
    return exists_any(repo, ".github/PULL_REQUEST_TEMPLATE.md", "PULL_REQUEST_TEMPLATE.md",
                       "docs/PULL_REQUEST_TEMPLATE.md")


@check("gitignore_exists", "Git hygiene", ".gitignore exists", True,
       "Run scripts/init_repo.py, or fetch the right template from https://github.com/github/gitignore.")
def _(repo):
    return exists_any(repo, ".gitignore")


@check("editorconfig_exists", "Git hygiene", ".editorconfig exists", False,
       "Copy assets/.editorconfig verbatim — it's language-agnostic.")
def _(repo):
    return exists_any(repo, ".editorconfig")


@check("gitattributes_exists", "Git hygiene", ".gitattributes exists", False,
       "Copy assets/.gitattributes verbatim.")
def _(repo):
    return exists_any(repo, ".gitattributes")


@check("ci_exists", "CI/CD", "A GitHub Actions workflow exists", True,
       "Copy the matching template from assets/workflows/ (Step 7 in SKILL.md).")
def _(repo):
    d = repo / ".github" / "workflows"
    return d.is_dir() and any(f.suffix in (".yml", ".yaml") for f in d.iterdir())


@check("dependabot_exists", "CI/CD", "Dependabot config exists", False,
       "Copy assets/dependabot.yml.template to .github/dependabot.yml and set the right package ecosystem.")
def _(repo):
    return exists_any(repo, ".github/dependabot.yml")


@check("changelog_exists", "Release management", "CHANGELOG.md exists", False,
       "Situational: valuable once the project starts cutting releases. See assets/CHANGELOG.template.md.")
def _(repo):
    return exists_any(repo, "CHANGELOG.md")


@check("citation_file_exists", "Research software", "CITATION.cff exists", False,
       "Situational: for research/academic software people should cite. See references/research-software.md "
       "and assets/CITATION.cff.template, or scripts/init_repo.py --profile research.")
def _(repo):
    return exists_any(repo, "CITATION.cff")


@check("badges_present", "Polish", "README has at least one status badge", False,
       "Add CI/license/version badges once they're true — see Step 8 in SKILL.md. Don't add a badge for "
       "something that doesn't exist yet.")
def _(repo):
    text = read(repo, "README.md")
    return "](https://img.shields.io" in text or "](https://github.com/" in text and "badge" in text.lower()


# ---------------------------------------------------------------------------
# Lightweight secrets scan (defensive hygiene check, not a full scanner)
# ---------------------------------------------------------------------------

SECRET_PATTERNS = [
    ("AWS Access Key ID", re.compile(r"AKIA[0-9A-Z]{16}")),
    ("Generic private key header", re.compile(r"-----BEGIN (RSA |OPENSSH |EC |DSA )?PRIVATE KEY-----")),
    ("Slack token", re.compile(r"xox[baprs]-[0-9A-Za-z-]{10,}")),
    ("Generic long hex/base64 secret assigned to a *_key/*_secret/*_token var",
     re.compile(r"(?i)(api|secret|access|private)[_-]?(key|token)\s*[:=]\s*['\"][A-Za-z0-9/+_-]{20,}['\"]")),
]

SKIP_DIRS = {".git", "node_modules", "dist", "build", "__pycache__", ".venv", "venv", "target"}
SKIP_SUFFIXES = {".png", ".jpg", ".jpeg", ".gif", ".ico", ".pdf", ".zip", ".woff", ".woff2", ".ttf", ".lock"}
MAX_SCAN_BYTES = 2_000_000  # skip huge files


def scan_for_secrets(repo: Path, max_files=4000):
    hits = []
    count = 0
    for p in repo.rglob("*"):
        if count >= max_files:
            break
        if p.is_dir():
            continue
        if any(part in SKIP_DIRS for part in p.parts):
            continue
        if p.suffix.lower() in SKIP_SUFFIXES:
            continue
        try:
            if p.stat().st_size > MAX_SCAN_BYTES:
                continue
            text = p.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        count += 1
        for name, pattern in SECRET_PATTERNS:
            m = pattern.search(text)
            if m:
                hits.append({"file": str(p.relative_to(repo)), "pattern": name})
    return hits


# ---------------------------------------------------------------------------
# Runner / report
# ---------------------------------------------------------------------------

def run(repo: Path, strict: bool):
    results = []
    for c in CHECKS:
        try:
            passed = bool(c["fn"](repo))
        except Exception as e:  # a check failing to run shouldn't crash the whole audit
            passed = False
        results.append({**{k: v for k, v in c.items() if k != "fn"}, "passed": passed})

    scored = [r for r in results if r["required"] or strict]
    passed_count = sum(1 for r in scored if r["passed"])
    total = len(scored)

    secret_hits = scan_for_secrets(repo)

    return {
        "repo": str(repo),
        "score": f"{passed_count}/{total}",
        "score_fraction": (passed_count / total) if total else 1.0,
        "results": results,
        "secret_scan_hits": secret_hits,
    }


def render_markdown(report: dict, strict: bool) -> str:
    lines = []
    lines.append(f"# Repo audit: `{report['repo']}`\n")
    lines.append(f"**Score: {report['score']}** "
                 f"({'strict — situational items included' if strict else 'required items only; run with --strict to include situational ones'})\n")

    by_category = {}
    for r in report["results"]:
        by_category.setdefault(r["category"], []).append(r)

    for category, items in by_category.items():
        lines.append(f"## {category}\n")
        for r in items:
            mark = "✅" if r["passed"] else ("❌" if r["required"] else "⚠️ ")
            tag = "" if r["required"] else " _(situational)_"
            lines.append(f"- {mark} {r['label']}{tag}")
            if not r["passed"]:
                lines.append(f"  - Fix: {r['remediation']}")
        lines.append("")

    lines.append("## Secrets scan (basic, not a substitute for a real scanner)\n")
    if report["secret_scan_hits"]:
        lines.append("⚠️  Possible secrets found — verify and remove/rotate before pushing:\n")
        for hit in report["secret_scan_hits"]:
            lines.append(f"- `{hit['file']}` — matched pattern: {hit['pattern']}")
    else:
        lines.append("✅ No obvious secret patterns found in scanned files.")
    lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Audit a repo against the github-repo-standards checklist.")
    parser.add_argument("--path", default=".", help="Path to the repo to audit.")
    parser.add_argument("--json", action="store_true", help="Print JSON instead of Markdown.")
    parser.add_argument("--strict", action="store_true",
                        help="Also score situational items (community health files) as required.")
    args = parser.parse_args()

    repo = Path(args.path).resolve()
    if not repo.is_dir():
        print(f"Error: '{repo}' is not a directory", file=sys.stderr)
        sys.exit(1)

    report = run(repo, args.strict)

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(render_markdown(report, args.strict))


if __name__ == "__main__":
    main()
