#!/usr/bin/env python3
"""Rank two or more loaded skills by specificity for conflict resolution.

Not a source of truth by itself -- a tie-breaking aid. Give it skill names
(looked up under the given roots) or raw "name::description" pairs, and it
prints a most-specific-first ranking with the reason for each rung, mirroring
the ladder in SKILL.md.

Usage:
  python rank_specificity.py --skills skill-a skill-b [--roots DIR ...]
  python rank_specificity.py --pairs "name::description" "name::description"
"""
from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

TECH_TERMS = {
    "python", "rust", "javascript", "typescript", "java", "go", "golang", "c++",
    "docker", "kubernetes", "aws", "gcp", "azure", "sql", "postgres", "mysql",
    "react", "django", "flask", "fastapi", "numpy", "pandas", "pytorch",
    "tensorflow", "cuda", "slurm", "latex", "git", "bash", "powershell",
    "matplotlib", "sympy", "scikit-learn", "networkx", "zarr", "modal",
    "docx", "pptx", "xlsx", "pdf", "mermaid", "mcp", "yaml", "json", "html",
    "css", "node", "npm", "pymatgen", "rdkit", "pymc", "pymoo",
}
ROLE_TERMS = {
    "review", "reviewer", "triage", "audit", "debug", "debugging", "deploy",
    "migration", "refactor", "test", "testing", "benchmark", "eval",
}


@dataclass
class Candidate:
    name: str
    description: str
    last_reviewed: str | None = None
    version: str | None = None
    project_scoped: bool = False


def load_from_roots(name: str, roots: list[Path]) -> Candidate:
    for root in roots:
        p = root / name / "SKILL.md"
        if p.exists():
            text = p.read_text(encoding="utf-8")
            m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
            fm = {}
            if m and yaml is not None:
                try:
                    fm = yaml.safe_load(m.group(1)) or {}
                except yaml.YAMLError:
                    fm = {}
            metadata = fm.get("metadata") if isinstance(fm.get("metadata"), dict) else {}
            return Candidate(
                name=str(fm.get("name", name)),
                description=str(fm.get("description", "")),
                last_reviewed=metadata.get("last_reviewed") if metadata else None,
                version=str(metadata.get("version")) if metadata and metadata.get("version") else None,
                project_scoped="project" in str(root).lower() and ".claude" in str(root).lower() and str(root).lower() != str(Path.home() / ".claude" / "skills").lower(),
            )
    return Candidate(name=name, description="")


def specificity_rung(c: Candidate) -> tuple[int, str]:
    """Lower rung number = more specific = wins on overlap. Mirrors SKILL.md's ladder."""
    text = f"{c.name} {c.description}".lower()
    if ":" in c.name or "/" in c.name:
        return 1, "path/directory-scoped skill name"
    tech_hits = {t for t in TECH_TERMS if t in text}
    if tech_hits:
        return 2, f"names a concrete technology ({', '.join(sorted(tech_hits))})"
    role_hits = {t for t in ROLE_TERMS if t in text}
    if role_hits:
        return 3, f"role/task-specific ({', '.join(sorted(role_hits))})"
    return 4, "no named technology or task -- general-purpose skill"


def rank(candidates: list[Candidate]) -> list[tuple[Candidate, int, str]]:
    scored = [(c, *specificity_rung(c)) for c in candidates]
    scored.sort(key=lambda t: (
        t[1],
        0 if t[0].project_scoped else 1,
        -(float(t[0].version)) if t[0].version and t[0].version.replace(".", "").isdigit() else 0,
        [t[0].last_reviewed or ""],
    ))
    return scored


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--skills", nargs="*", default=[], help="Skill names to look up under --roots")
    ap.add_argument("--roots", nargs="*", default=None, help="Dirs to search for <name>/SKILL.md (default: ~/.claude/skills)")
    ap.add_argument("--pairs", nargs="*", default=[], help='Raw "name::description" entries, skip lookup')
    args = ap.parse_args()

    roots = [Path(r).expanduser() for r in args.roots] if args.roots else [Path.home() / ".claude" / "skills"]

    candidates: list[Candidate] = []
    for name in args.skills:
        candidates.append(load_from_roots(name, roots))
    for pair in args.pairs:
        if "::" not in pair:
            print(f"Skipping malformed pair (need name::description): {pair}", file=sys.stderr)
            continue
        name, desc = pair.split("::", 1)
        candidates.append(Candidate(name=name.strip(), description=desc.strip()))

    if len(candidates) < 2:
        print("Give at least two skills via --skills and/or --pairs.", file=sys.stderr)
        return 1

    ranked = rank(candidates)
    print(f"{'rung':>4}  {'name':<30}  reason")
    print("-" * 70)
    for c, rung, reason in ranked:
        print(f"{rung:>4}  {c.name:<30}  {reason}")
    print()
    winner = ranked[0][0]
    print(f"On any point where these conflict: follow '{winner.name}' -- "
          f"but only for that specific point. Everything the others cover "
          f"that '{winner.name}' does not address still applies.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
