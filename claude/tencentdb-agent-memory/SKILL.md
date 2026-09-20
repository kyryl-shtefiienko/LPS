---
name: tencentdb-agent-memory
description: >-
  Read and write the local, API-free project-memory store at
  C:\Claude\TencentDB-Agent_Memory\ — a layered memory design (persona /
  per-project scenarios / per-project atomic facts) modeled on
  TencentCloud/TencentDB-Agent-Memory, but run as plain files with Claude
  doing the distillation itself instead of Docker, a Node service, or an LLM
  API key. Use this at the start of work on a known project (precipitree,
  model-router, research-harness, research-vault, lps, or any later addition)
  to load real context instead of guessing, and whenever the user says "save
  to memory", "update project memory", "remember this for <project>", or asks
  for a daily memory pass. Claude-only: assumes Claude Code's own filesystem
  and git access.
---

# TencentDB Agent Memory (local adaptation)

A project-memory store at `C:\Claude\TencentDB-Agent_Memory\`, laid out like
this:

```
TencentDB-Agent_Memory/
  README.md                    — rationale and layout (read once for context)
  memory/
    L3-persona.md              — stable, cross-project facts about the user
    L2-scenarios/<project>.md  — what a project is, its design, current
                                  status, and how to help with it
    L1-facts/<project>.jsonl   — atomic, dated, sourced facts per project
  _vendor/TencentDB-Agent-Memory/ — reference clone of the upstream project;
                                  format inspiration only, never run
```

There is deliberately no L0 (raw conversation log), no Docker, no Node
service, no LLM API key, and nothing proxying Claude Code's own API traffic.
Claude performs the extraction/distillation step directly, the way
`research-harness`'s console mode does extraction without an API key — not a
hosted pipeline on a timer. Do not suggest standing up the real Docker/Node/
LLM-proxy stack; if the user wants that later, treat it as a new decision
requiring fresh confirmation, not a natural next step of this skill.

## Reading (do this before assuming anything about a project)

When work touches a project this store knows about, or the user references
one by name, read `memory/L2-scenarios/<project>.md` and
`memory/L3-persona.md` first. Treat what's there as current until you observe
otherwise (a stale scenario is a reason to update it, not to distrust the
whole system).

## Writing

Trigger on: finishing a meaningful chunk of work, or the user saying "save to
memory" / "update project memory" / "remember this for `<project>`" / asking
for a daily pass.

1. **L1 facts** — append one JSON object per new atomic fact to
   `memory/L1-facts/<project>.jsonl`: `{"id": "<project>-NNN", "date":
   "YYYY-MM-DD", "fact": "...", "source": "..."}`. IDs increment per project
   (check the last one already in the file). Only write what you actually
   observed — a file, git history, or something the user just said — and
   name that source. Never fabricate a fact to fill a gap.
2. **L2 scenario** — fold anything that changes the project's ongoing shape
   (status, design decisions, new direction, new remote, phase changes) into
   `memory/L2-scenarios/<project>.md`. This is prose/structure, not a log —
   edit it in place rather than appending indefinitely; keep the "Status (as
   of <date>)" section current.
3. **Daily pass** (only when asked): review what changed since the L2 file's
   last "as of" date — `git log` across known project folders, README/file
   diffs — and update both layers. This runs live in whatever session is
   open; it is not a background job.
4. **New project**: the first time a project folder with no
   `L2-scenarios/<name>.md` comes up in conversation, create one seeded from
   a quick look at its README, structure, and git log, plus a matching
   (possibly empty) `L1-facts/<name>.jsonl` — the same way the first five
   projects were seeded.

## Persona discipline

`L3-persona.md` holds only genuinely stable, cross-project facts: identity,
working style, standing preferences (e.g. "confirm before pushing",
"lightweight-over-heavy-infra when both work"). Per-project status belongs in
that project's L2 scenario file, not here — if you're about to add something
that will look dated in a month, it's a scenario fact, not a persona fact.
