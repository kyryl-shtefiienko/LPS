#!/usr/bin/env python3
"""Static, offline hygiene/overlap scorer for a library of Agent Skills.

No network, no agent CLI, no API key. Scans every SKILL.md under the given
roots, scores each on a fixed 100-point rubric, prints a ranked table to the
console, and writes a full breakdown to a JSON report for editing.

Edit WEIGHTS / THRESHOLDS below to change scoring, then re-run.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field, asdict
from datetime import date, datetime
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:
    yaml = None

# ---------------------------------------------------------------------------
# Tunables - edit these to change how skills are scored.
# ---------------------------------------------------------------------------

WEIGHTS = {
    "description": 25,   # trigger clarity + reasonable length
    "tools": 15,          # allowed-tools/tools scoped, not wildcard/absent
    "freshness": 20,      # metadata.last_reviewed recency
    "size": 15,           # SKILL.md body under the ~500-line guideline
    "overlap": 15,        # low description overlap with other skills
    "specificity": 10,    # names a concrete domain/language/tool (informational)
}
assert sum(WEIGHTS.values()) == 100

TRIGGER_PATTERN = re.compile(r"\buse\b(?:\s+\w+){0,3}\s+(when|whenever|if|for)\b|\btrigger", re.IGNORECASE)
STOPWORDS = {
    "the", "a", "an", "and", "or", "of", "to", "for", "in", "on", "with", "is",
    "are", "this", "that", "it", "as", "by", "be", "when", "use", "skill",
    "skills", "you", "your", "their", "even", "any", "into", "such", "will",
    "can", "if", "not", "no", "do", "does", "so", "than", "then", "also",
}
TECH_TERMS = {
    "python", "rust", "javascript", "typescript", "java", "go", "golang", "c++",
    "docker", "kubernetes", "aws", "gcp", "azure", "sql", "postgres", "mysql",
    "react", "django", "flask", "fastapi", "numpy", "pandas", "pytorch",
    "tensorflow", "cuda", "slurm", "latex", "git", "bash", "powershell",
    "matplotlib", "sympy", "scikit-learn", "networkx", "zarr", "modal",
    "docx", "pptx", "xlsx", "pdf", "mermaid", "mcp", "yaml", "json", "html",
    "css", "node", "npm", "pymatgen", "rdkit", "pymc", "pymoo",
}

OVERLAP_HIGH = 0.40
OVERLAP_MEDIUM = 0.25
MAX_BODY_LINES = 500


@dataclass
class SkillRecord:
    name: str
    path: str
    description: str = ""
    allowed_tools: Any = None
    last_reviewed: str | None = None
    version: str | None = None
    body_lines: int = 0
    has_scripts: bool = False
    has_references: bool = False
    parse_error: str | None = None
    scores: dict[str, float] = field(default_factory=dict)
    issues: list[str] = field(default_factory=list)
    scope: str = "general"
    total: float = 0.0


def find_skill_files(roots: list[Path]) -> list[Path]:
    seen: set[Path] = set()
    out: list[Path] = []
    for root in roots:
        if not root.exists():
            continue
        for p in root.rglob("SKILL.md"):
            rp = p.resolve()
            if rp not in seen:
                seen.add(rp)
                out.append(p)
    return out


def parse_frontmatter(text: str) -> tuple[dict, str]:
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", text, re.DOTALL)
    if not m:
        return {}, text
    raw, body = m.group(1), m.group(2)
    if yaml is not None:
        try:
            data = yaml.safe_load(raw)
            return (data if isinstance(data, dict) else {}), body
        except yaml.YAMLError:
            pass
    # Minimal fallback: only pulls top-level "key: value" scalar lines.
    data = {}
    for line in raw.splitlines():
        m2 = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if m2:
            data[m2.group(1)] = m2.group(2).strip().strip("'\"")
    return data, body


def tokenize(text: str) -> set[str]:
    words = re.findall(r"[a-z][a-z0-9+#.-]{2,}", text.lower())
    return {w for w in words if w not in STOPWORDS}


def jaccard(a: set[str], b: set[str]) -> float:
    if not a or not b:
        return 0.0
    inter = len(a & b)
    union = len(a | b)
    return inter / union if union else 0.0


def score_description(desc: str) -> tuple[float, list[str]]:
    if not desc.strip():
        return 0.0, ["empty description - skill will effectively never trigger"]
    words = len(desc.split())
    issues = []
    score = 0.0
    if 20 <= words <= 220:
        score += 15
    elif words < 20:
        issues.append(f"description very short ({words} words) - may under-trigger")
        score += 5
    else:
        issues.append(f"description is {words} words - costs context on every turn")
        score += 8
    if TRIGGER_PATTERN.search(desc):
        score += 10
    else:
        issues.append("no explicit 'use when / triggers on' language")
    return score, issues


def score_tools(allowed_tools: Any) -> tuple[float, list[str]]:
    if allowed_tools is None:
        return 5.0, ["no allowed-tools/tools field - can't tell what it needs"]
    if isinstance(allowed_tools, list) and len(allowed_tools) == 0:
        return 8.0, ["tools: [] - unscoped, treat as informational only"]
    if isinstance(allowed_tools, str) and allowed_tools.strip() in ("*", "all"):
        return 5.0, ["allowed-tools is a wildcard"]
    return 15.0, []


def score_freshness(last_reviewed: str | None) -> tuple[float, list[str]]:
    if not last_reviewed:
        return 10.0, ["no metadata.last_reviewed - can't judge staleness"]
    try:
        d = datetime.fromisoformat(str(last_reviewed)).date()
    except ValueError:
        return 10.0, [f"last_reviewed '{last_reviewed}' isn't ISO date"]
    age_days = (date.today() - d).days
    if age_days <= 90:
        return 20.0, []
    if age_days <= 365:
        return 14.0, [f"last reviewed {age_days}d ago"]
    return 6.0, [f"stale - last reviewed {age_days}d ago"]


def score_size(body_lines: int, has_scripts: bool, has_references: bool) -> tuple[float, list[str]]:
    issues = []
    score = 0.0
    if body_lines <= MAX_BODY_LINES:
        score += 12
    else:
        score += 4
        issues.append(f"SKILL.md body is {body_lines} lines (guideline: <{MAX_BODY_LINES}); push detail into references/")
    if has_scripts or has_references:
        score += 3
    return score, issues


def score_specificity(desc: str, name: str) -> tuple[float, list[str], str]:
    tokens = tokenize(desc) | tokenize(name)
    hits = tokens & TECH_TERMS
    is_path_scoped = ":" in name or "/" in name
    if hits or is_path_scoped:
        return 10.0, [], "specific"
    return 5.0, ["no named language/framework/tool - treated as a general skill"], "general"


def build_records(files: list[Path]) -> list[SkillRecord]:
    records = []
    for f in files:
        try:
            text = f.read_text(encoding="utf-8")
        except OSError as e:
            records.append(SkillRecord(name=f.parent.name, path=str(f), parse_error=str(e)))
            continue
        fm, body = parse_frontmatter(text)
        name = fm.get("name") or f.parent.name
        metadata = fm.get("metadata") if isinstance(fm.get("metadata"), dict) else {}
        rec = SkillRecord(
            name=str(name),
            path=str(f),
            description=str(fm.get("description") or ""),
            allowed_tools=fm.get("allowed-tools", fm.get("tools", fm.get("allowedTools"))),
            last_reviewed=metadata.get("last_reviewed") if metadata else None,
            version=str(metadata.get("version")) if metadata and metadata.get("version") is not None else None,
            body_lines=len(body.strip().splitlines()),
            has_scripts=(f.parent / "scripts").is_dir(),
            has_references=(f.parent / "references").is_dir(),
        )
        records.append(rec)
    return records


def score_records(records: list[SkillRecord]) -> None:
    desc_tokens = [tokenize(r.description) for r in records]

    for i, r in enumerate(records):
        if r.parse_error:
            r.issues.append(f"could not read file: {r.parse_error}")
            r.total = 0.0
            continue

        s_desc, i_desc = score_description(r.description)
        s_tools, i_tools = score_tools(r.allowed_tools)
        s_fresh, i_fresh = score_freshness(r.last_reviewed)
        s_size, i_size = score_size(r.body_lines, r.has_scripts, r.has_references)
        s_spec, i_spec, scope = score_specificity(r.description, r.name)

        best_j, best_sim = -1, 0.0
        for j, other in enumerate(records):
            if j == i:
                continue
            sim = jaccard(desc_tokens[i], desc_tokens[j])
            if sim > best_sim:
                best_sim, best_j = sim, j

        i_overlap = []
        if best_sim >= OVERLAP_HIGH:
            s_overlap = 3.0
            i_overlap.append(
                f"high description overlap with '{records[best_j].name}' (jaccard={best_sim:.2f}) "
                "- check skill-hierarchy for precedence, or consider merging"
            )
        elif best_sim >= OVERLAP_MEDIUM:
            s_overlap = 9.0
            i_overlap.append(f"moderate overlap with '{records[best_j].name}' (jaccard={best_sim:.2f})")
        else:
            s_overlap = 15.0

        # Rescale each raw component (already 0..WEIGHTS[key] by construction above)
        # to make later edits to WEIGHTS take effect without touching the score_* functions.
        raw_max = {"description": 25, "tools": 15, "freshness": 20, "size": 15, "overlap": 15, "specificity": 10}
        raw = {"description": s_desc, "tools": s_tools, "freshness": s_fresh,
               "size": s_size, "overlap": s_overlap, "specificity": s_spec}
        scaled = {k: (raw[k] / raw_max[k]) * WEIGHTS[k] if raw_max[k] else 0 for k in raw}

        r.scores = scaled
        r.total = round(sum(scaled.values()), 1)
        r.scope = scope
        r.issues = i_desc + i_tools + i_fresh + i_size + i_spec + i_overlap


def print_console_report(records: list[SkillRecord], top: int | None) -> None:
    ordered = sorted(records, key=lambda r: r.total, reverse=True)
    if top:
        ordered = ordered[:top]

    name_w = max(len(r.name) for r in ordered) if ordered else 20
    name_w = min(max(name_w, 12), 40)

    header = f"{'#':>3}  {'score':>5}  {'scope':<8}  {'name':<{name_w}}  top issue"
    print(header)
    print("-" * len(header))
    for i, r in enumerate(ordered, 1):
        top_issue = r.issues[0] if r.issues else "-"
        nm = r.name if len(r.name) <= name_w else r.name[: name_w - 1] + "…"
        print(f"{i:>3}  {r.total:>5.1f}  {r.scope:<8}  {nm:<{name_w}}  {top_issue}")

    n_general = sum(1 for r in records if r.scope == "general")
    n_specific = len(records) - n_general
    n_flagged_overlap = sum(1 for r in records if any("overlap" in i for i in r.issues))
    n_stale = sum(1 for r in records if any("stale" in i for i in r.issues))
    print()
    print(f"{len(records)} skills scanned  |  {n_specific} specific / {n_general} general  |  "
          f"{n_flagged_overlap} with notable overlap  |  {n_stale} stale")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--roots", nargs="*", default=None,
                     help="Directories to scan for SKILL.md (default: ~/.claude/skills)")
    ap.add_argument("--out", default=None, help="Path to write report.json (default: alongside this script's skill dir)")
    ap.add_argument("--top", type=int, default=None, help="Only print the top N rows to console")
    ap.add_argument("--json", action="store_true", help="Also print the full report as JSON to stdout")
    args = ap.parse_args()

    roots = [Path(r).expanduser() for r in args.roots] if args.roots else [Path.home() / ".claude" / "skills"]
    files = find_skill_files(roots)
    if not files:
        print(f"No SKILL.md files found under: {', '.join(str(r) for r in roots)}", file=sys.stderr)
        return 1

    records = build_records(files)
    score_records(records)
    print_console_report(records, args.top)

    out_path = Path(args.out) if args.out else Path(__file__).resolve().parent.parent / "report.json"
    report = {
        "generated": datetime.now().isoformat(timespec="seconds"),
        "roots": [str(r) for r in roots],
        "weights": WEIGHTS,
        "skills": [asdict(r) for r in sorted(records, key=lambda r: r.total, reverse=True)],
    }
    out_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"\nFull breakdown written to: {out_path}")

    if args.json:
        print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
