---
name: skill-benchmark
description: >-
  Statically score and rank every installed Agent Skill on hygiene signals --
  description trigger-clarity and length, allowed-tools scoping, staleness
  (metadata.last_reviewed), SKILL.md size against the ~500-line guideline,
  and description overlap with other skills (possible redundant/colliding
  triggers). Prints a ranked table straight to the console (no agent CLI, no
  network, no API key) and writes an editable JSON report. Use whenever the
  user wants to "benchmark my skills", "audit my skill library", "which
  skills are redundant, stale, or poorly worded", or "rank/score my skills"
  -- this is a library-wide static audit, distinct from an agent-driven
  eval harness (which measures whether ONE skill's runtime behavior beats
  no-skill for that skill alone). Hand off to skill-hierarchy when this audit
  flags two skills that overlap and might genuinely conflict rather than
  just be redundant.
---

# Skill Benchmark

A fast, offline hygiene audit across an entire skill library. It answers
"which of my skills are well-formed, fresh, and non-redundant" -- not "does
this skill's logic actually work," which needs a real agent run and is out
of scope here. Run this one first, cheaply, to decide which skills are worth
a deeper look.

## Run it

```bash
python scripts/benchmark_skills.py
```

By default it scans `~/.claude/skills`. Pass `--roots <dir> <dir> ...` to
also cover project-level `.claude/skills`, an LPS checkout's `common/`,
`claude/`, and `chatgpt/` directories, or any other location. Useful flags:

- `--top N` -- only print the N lowest/highest scorers to keep the console short
- `--json` -- also dump the full report to stdout (in addition to the file)
- `--out <path>` -- where to write `report.json` (default: next to this SKILL.md)

Show the printed console table to the user directly -- that's the point of
running this statically instead of through a heavier eval loop. They can:

- **Edit `report.json`** -- strike an issue that doesn't apply, add notes, or
  re-sort by hand before deciding what to fix.
- **Edit the script** -- `WEIGHTS`, `TRIGGER_PHRASES`, `TECH_TERMS`, and the
  overlap thresholds (`OVERLAP_HIGH`/`OVERLAP_MEDIUM`) are all constants near
  the top of `scripts/benchmark_skills.py`, kept easy to tweak and re-run
  rather than buried in logic.

## The rubric (100 points, weights editable in the script)

| Component | Points | What it checks |
|---|---|---|
| description | 25 | Reasonable length (~20-220 words) and explicit "use when / triggers on" language -- the actual triggering mechanism |
| tools | 15 | `allowed-tools`/`tools` is scoped, not absent or a wildcard |
| freshness | 20 | `metadata.last_reviewed` age (full marks <=90 days, decaying past a year) |
| size | 15 | SKILL.md body <=500 lines (the progressive-disclosure guideline); bonus for pushing detail into `scripts/`/`references/` |
| overlap | 15 | Jaccard similarity of description keywords against every other scanned skill -- flags likely-redundant or competing triggers |
| specificity | 10 | Informational only: does the description/name name a concrete language, framework, or tool, or is it a general-purpose skill? Feeds skill-hierarchy's precedence ordering |

None of these components measure whether the skill's *instructions* produce
correct output -- only whether the skill is well-formed as metadata. A skill
can score 100 here and still give bad advice; that needs an actual with/
without run of a real coding agent, which this tool deliberately does not do.

## After running

1. Report the console table and the overall summary line (specific vs.
   general count, skills with notable overlap, stale skills) to the user.
2. For any skill flagged with high overlap (`jaccard >= 0.40`), read both
   SKILL.md files and tell the user concretely whether they should merge,
   or whether the overlap is intentional (a general skill and a narrower
   one meant to take precedence on top of it) -- in that case, use
   skill-hierarchy's precedence rule instead of merging.
3. For any skill flagged stale or poorly described, offer to rewrite its
   description and bump `metadata.last_reviewed` rather than hand-editing
   blindly.

## Limitations

- Pure static analysis of SKILL.md metadata and structure -- it does not
  execute anything, so it cannot tell you a bundled script is broken or a
  documented number is wrong.
- Overlap detection is bag-of-words Jaccard on the description text, not
  semantic similarity -- it will miss overlaps phrased in very different
  words, and will occasionally flag two skills that share vocabulary but
  cover unrelated ground. Treat every flag as "look closer," not a verdict.
- "Specificity" is a keyword heuristic against a small `TECH_TERMS` list in
  the script; a skill about an unlisted technology will read as "general."
  Extend the list rather than trusting the label blindly.
