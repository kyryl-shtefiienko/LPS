---
name: skill-benchmark
description: >
  Statically score and rank every installed Agent Skill on hygiene signals —
  description trigger-clarity and length, allowed-tools scoping, staleness
  (metadata.last_reviewed), SKILL.md size against the ~500-line guideline,
  and description overlap with other skills (possible redundant/colliding
  triggers). Prints a ranked table straight to the console (no agent CLI, no
  network, no API key) and writes an editable JSON report. Use whenever the
  user wants to "benchmark my skills", "audit my skill library", "which
  skills are redundant, stale, or poorly worded", or "rank/score my skills"
  — this is a library-wide static audit, distinct from skill-evaluator
  (which drives a coding-agent CLI to measure whether ONE skill's runtime
  behavior actually beats no-skill). Hand off to skill-evaluator for a deep
  runtime eval once a candidate skill is picked, and to skill-hierarchy when
  this audit flags two skills that overlap and might conflict.
license: Apache-2.0
compatibility: Python 3.10+. No network or API key needed; PyYAML optional (falls back to a minimal parser).
metadata:
  author: kshtefiienko
  version: "1.0.0"
  last_reviewed: "2026-09-18"
allowed-tools: Read, Bash, Write, Glob
---

# Skill Benchmark

A fast, offline hygiene audit across an entire skill library. It answers
"which of my skills are well-formed, fresh, and non-redundant" — not "does
this skill's logic actually work" (that's `skill-evaluator`'s job, and it
requires running a real coding-agent CLI). Run this one first, cheaply, to
decide *which* skills are worth putting through the heavier runtime harness.

## Run it

```bash
python scripts/benchmark_skills.py
```

By default it scans `~/.claude/skills`. Pass `--roots <dir> <dir> ...` to
also cover project-level `.claude/skills` or plugin skill directories. Useful
flags:

- `--top N` — only print the N lowest/highest scorers to keep the console short
- `--json` — also dump the full report to stdout (in addition to the file)
- `--out <path>` — where to write `report.json` (default: `report.json` next to this SKILL.md)

Show the printed console table to the user directly — that's the point of
running this statically instead of through a heavier eval loop. They can:

- **Edit `report.json`** — strike an issue that doesn't apply, add notes, or
  re-sort by hand before deciding what to fix.
- **Edit the script** — `WEIGHTS`, `TRIGGER_PHRASES`, `TECH_TERMS`, and the
  overlap thresholds (`OVERLAP_HIGH`/`OVERLAP_MEDIUM`) are all constants near
  the top of `scripts/benchmark_skills.py`, deliberately kept easy to tweak
  and re-run rather than buried in logic.

## The rubric (100 points, weights editable in the script)

| Component | Points | What it checks |
|---|---|---|
| description | 25 | Reasonable length (~20–220 words) and explicit "use when / triggers on" language — the actual triggering mechanism |
| tools | 15 | `allowed-tools`/`tools` is scoped, not absent or a wildcard |
| freshness | 20 | `metadata.last_reviewed` age (full marks ≤90 days, decaying past a year) |
| size | 15 | SKILL.md body ≤500 lines (the progressive-disclosure guideline); bonus for pushing detail into `scripts/`/`references/` |
| overlap | 15 | Jaccard similarity of description keywords against every other scanned skill — flags likely-redundant or competing triggers |
| specificity | 10 | Informational only: does the description/name name a concrete language, framework, or tool, or is it a general-purpose skill? Feeds `skill-hierarchy`'s precedence ordering |

None of these components measure whether the skill's *instructions* produce
correct output — only whether the skill is well-formed as metadata. A skill
can score 100 here and still give bad advice; that's what `skill-evaluator`
Layer 3 (with/without-skill delta) is for.

## After running

1. Report the console table and the overall summary line (specific vs.
   general count, skills with notable overlap, stale skills) to the user.
2. For any skill flagged with high overlap (`jaccard ≥ 0.40`), read both
   SKILL.md files and tell the user concretely whether they should merge,
   or whether the overlap is intentional (e.g. a general skill and a
   narrower one meant to take precedence on top of it — in that case load
   `skill-hierarchy` and apply its precedence rule instead of merging).
3. For any skill flagged stale or poorly described, offer to open
   `skill-creator`'s improvement loop on it rather than hand-editing —
   that loop also re-optimizes the description's triggering.

## Limitations

- Pure static analysis of SKILL.md metadata and structure — it does not
  execute anything, so it cannot tell you a script is broken or a rubric is
  wrong. Use `skill-evaluator` Layer 1 (`run_script_checks.py`) for that.
- Overlap detection is bag-of-words Jaccard on the description text, not
  semantic similarity — it will miss overlaps phrased in very different
  words, and will occasionally flag two skills that share vocabulary but
  cover unrelated ground. Treat every flag as "look closer," not verdict.
- "Specificity" is a keyword heuristic against a small `TECH_TERMS` list; a
  skill about an unlisted technology will read as "general." Extend the
  list in the script rather than trusting the label blindly.
