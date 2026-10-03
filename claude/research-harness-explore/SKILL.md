---
name: research-harness-explore
description: Mine the existing research-harness knowledge graph for new research directions by intersecting two or more concept clusters already in the vault (e.g. "Bayesian optimization" and "cold spray additive manufacturing"), proposing candidate research topics, and growing the most promising ones via the existing deepen loop. Use when the user wants to generate research ideas from what's already in their vault, asks "what could I research at the intersection of X and Y", or wants to combine two existing topics into new directions — not for adding papers on a single topic (use research-harness-run for that).
allowed-tools: Bash Read
metadata:
  version: "0.1"
---

# research-harness-explore

Treats the knowledge graph itself as raw material for new research ideas,
instead of only growing from fresh papers. Given two or more seed concepts,
it finds what the graph already knows about each, looks for a genuine
intersection between them, checks the literature for whether that
intersection is already well-trodden or a real gap, proposes a small number
of candidate research directions, and grows the promising ones with the same
`deepen` mechanism `research-harness-run` uses — fully automatically,
end-to-end, reporting only at the end.

Like `research-harness-run`, this is a driver over the `research-harness`
CLI: it never edits anything under `research-harness/` (no source, no
config, no its own skill folder). If the workflow below needs a real code
change to do what's asked, stop and tell the user rather than patching it
from here.

## Locating the repo

Default path: `C:\Claude\research-harness`. Verify it exists before doing
anything; if it's been moved, ask once and remember for the rest of the
session. All commands below run from that repo root via `uv run
research-harness <command> ...`.

## Inputs

- **seeds** (required): 2 or more free-text concepts to intersect, e.g.
  "Bayesian optimization" and "cold spray additive manufacturing". More than
  2 seeds is fine — the procedure below generalizes, but intersections get
  harder to find meaningfully past 3-4.
- **deepen rounds** (optional, default 2): how many deepen rounds to run on
  each proposal idea that gets created — "a couple of times" in the default
  case. Accept an explicit override if the user gives one.

## Procedure

### 1. Expand each seed into a concept cluster

For each seed:
- `uv run research-harness list-topics` (once, covers all seeds) to see the
  topic map and spot any topic slug that obviously matches a seed already.
- `uv run research-harness query "<seed>"` plus 2-3 obviously related terms
  for that seed (e.g. for "Bayesian optimization": also query "acquisition
  function", "Gaussian process", "surrogate model", "kernel"; for "cold
  spray additive manufacturing": also "cold spray", "particle bonding",
  "coating", "process parameters"). Union the hits into that seed's
  candidate id list.
- For every id returned, `uv run research-harness show-idea "<id>"` to read
  the full record (gist, knowledge, open_questions, topic, tags, relations)
  — the intersection step needs the actual content, not just gists.

Keep each seed's cluster (ids + full records) separate — don't merge them
yet.

### 2. Find intersection candidates

Read across both (or all) clusters and look for:
- An idea in one cluster whose `Open Questions` text plausibly connects to
  the other cluster's subject matter.
- Two ideas (one per cluster) that share an underlying mechanism or
  technique even though they're filed under unrelated topics (e.g. a
  kernel-design idea from one cluster + a process-modeling idea from the
  other → "use a custom kernel to model cold-spray process parameters for
  Bayesian optimization").
- A concept that's clearly present in one cluster's tags/knowledge but
  completely absent from the other's — often the actual gap worth
  proposing research into.

This is judgment, not a mechanical set intersection — with only word-overlap
matching in the graph, direct id overlap between clusters will usually be
empty; the real intersections come from reading the content.

### 3. Check the literature at each candidate intersection

For each candidate intersection identified in step 2, run a real search to
see whether it's already well-studied or a genuine gap, and to pull in real
sources to ground the proposal in:
```
uv run research-harness search "<precise intersection query>" --source arxiv --max-results 5
```
Note per candidate: does prior work already sit here, or does this look
genuinely underexplored? Either way, keep any directly relevant results —
they become sources for the proposal idea in step 4.

### 4. Propose and ingest candidate research topics

Pick 2-4 of the most promising candidates from steps 2-3. For each, write it
up as a new idea and ingest it:
- **topic**: `<seed-a-slug>-x-<seed-b-slug>` (or similar, combining the
  seeds' slugs).
- **tags**: include `research-proposal` alongside normal topic tags.
- **gist**: the proposed research direction in one sentence.
- **knowledge**: the hypothesis/angle, why it's motivated by what's in the
  graph (name the specific idea ids from step 2 that led here), and what
  step 3's literature check found (well-studied vs. a plausible gap).
- **open_questions**: the concrete research questions this proposal would
  need to answer — this is what `deepen` will turn into follow-up searches.
- **sources**: any papers found in step 3 that directly support or motivate
  it (via the normal `ingest-ideas` source-identifier mechanism — you'll
  need to fetch/convert those the same way `console-mode.md` describes if
  you want their content merged in, or you can ingest the proposal idea
  itself against a synthetic identifier if no single paper backs it — ask
  console-mode.md's flow for the exact ingest shape).

Then link it to the graph ideas that motivated it:
```
uv run research-harness link-ideas "<proposal-id>" related_to "<motivating-idea-id>"
```
(repeat per motivating idea from both clusters).

### 5. Deepen loop

For each proposal idea, run the deepen cycle for the configured number of
rounds (default 2):
- **LLM key present**: `uv run research-harness deepen "<proposal-id>"
  --max-results 5` per round.
- **Console mode**: follow `research-harness/.claude/skills/research-harness/references/console-mode.md`'s
  manual deepen flow — generate 2-4 follow-up queries yourself from the
  proposal's `Open Questions`, then search → fetch → convert → extract →
  merge back into the same proposal id, same as `research-harness-run`'s
  depth-based deepen loop.

Same stop-early rule as `research-harness-run`: skip a proposal's next round
if its last round produced zero new/updated ideas — don't keep hammering a
dead end.

### 6. Record and report

```
uv run research-harness record-run "<seed-a> x <seed-b> intersection" <idea-id>...
```
covering every proposal idea plus everything pulled in while deepening them,
then `uv run research-harness reindex`. Report to the user in plain
language: which candidate topics were proposed and why (cite the graph ideas
each one connects), what the literature check found for each, and what
deepening turned up — not raw JSON. Point them at the vault path and the new
topic folder(s) so they know where to read the results.

## Out of scope

- Adding papers on a single topic with no cross-graph synthesis — use
  `research-harness-run` for that.
- Anything requiring a real code change to `research-harness` itself — hand
  it back to the user or make it in a separate conversation about the
  project directly, not through this driver skill.
