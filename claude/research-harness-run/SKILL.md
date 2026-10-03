---
name: research-harness-run
description: Run a full research-harness pass on a topic given just a topic and a depth level (quick/standard/deep, or 1-3) — drives the research-harness CLI end-to-end as a black box, without reading or editing that project's own source or skill. Use when the user says "research <topic>", "add papers on X to my vault", or gives a topic + depth and wants the idea graph updated without walking through the staged flow themselves.
allowed-tools: Bash Read
metadata:
  version: "0.1"
---

# research-harness-run

Thin driver over the `research-harness` CLI. It treats `research-harness` as
an external tool: it calls the CLI and reads *its own JSON output* and *its
own reference docs* (`research-harness/.claude/skills/research-harness/references/`),
but never edits anything under `research-harness/` — no source, no config, no
its own `.claude/skills/research-harness/`. If the pipeline needs a real code
change to do what's asked, stop and tell the user rather than patching it
from here.

This skill exists for the common case: the user just wants to hand over a
topic and a depth and get the vault updated, without making the staged
search → review → run → deepen calls themselves. For careful/interactive
research sessions (pruning search results before spending budget, judgment
calls on trashing), point them at the `research-harness` skill instead — that
one is meant to be driven turn-by-turn.

**Capture broadly, tag by best fit.** The topic you're given is what to
*search* for — it is not a filter on what to *extract*. Once a paper is
fetched, pull out every durable idea it contains, including ones tangential
to the search topic (a generically useful idea found by accident is still
worth keeping) and attempted approaches with negative/null results. Give
each idea whichever `topic` slug fits its own content, not necessarily the
topic you were asked to run.

## Locating the repo

Default path: `C:\Claude\research-harness`. Verify it exists (`Read`/`ls`)
before doing anything; if it's been moved, ask once and remember for the rest
of the session. All commands below run from that repo root via
`uv run research-harness <command> ...`.

## Inputs

- **topic** (required): free-text search topic, passed straight to `search`/`run`.
- **depth** (required): one of `quick` (1), `standard` (2), `deep` (3). Accept
  either the word or the number. If the user gives neither, ask — don't
  guess a depth, since it changes how much API spend and vault churn happens.

## Depth → behavior

| Depth | Initial `run --max-results` | Deepen rounds after |
|---|---|---|
| quick / 1 | 6 | 0 |
| standard / 2 | 10 | 1 |
| deep / 3 | 15 | 2 |

"Deepen rounds" means: after the initial `run`, take the `idea_ids` it
touched, and for each one call `uv run research-harness deepen "<idea-id>"
--max-results 5`, repeated for that many rounds (a round = one deepen pass
over every idea touched so far, including ones spun off by the previous
round via `extends`). Skip an idea's next round if its last `deepen` outcome
produced zero new/updated ideas — don't keep hammering a dead end.

## Procedure

1. **Survey the existing knowledge graph before touching any connector.**
   This always runs first, regardless of depth — the whole point is to know
   what's already connected before spending search/fetch/LLM budget on it.
   - `uv run research-harness list-topics` — see the full topic map and where
     this topic might already live (topics are slugs; match loosely, e.g.
     "cold spray bonding" ~ `cold-spray-bonding-mechanism`).
   - `uv run research-harness query "<topic>"` — cheap Tier-0 keyword search
     over every active idea's gist/topic/tags. This is the real check: it
     surfaces relevant ideas anywhere in the graph, not just under an
     exactly-matching topic name.
   - For any topic(s) that clearly match, `uv run research-harness list-ideas
     --topic <slug>` to see depth and how recently each idea was updated.
   - Decide what this buys you:
     - **Nothing relevant found** → proceed to step 2 as normal.
     - **Related ideas found, shallow/stale** → still proceed to step 2, but
       mention the existing coverage in the final report instead of treating
       this as a from-scratch topic.
     - **Related ideas found, already deep/fresh** → this is a judgment call,
       not an automatic skip: tell the user what's already there (ids, gist,
       depth) and ask whether they want a fresh `run` anyway, want to
       `deepen` those existing ideas instead (often cheaper and more
       targeted — it generates queries from each idea's own "Open Questions"
       section), or want both. Don't silently skip the research they asked
       for, and don't silently duplicate it either.
   - Note: `run`/`import` already dedupe at the source level (`sources.db`)
     and at the idea level (merge-matching), so this step isn't about
     preventing hard duplicates — it's about not re-running expensive
     fetch/convert/extract on ground the graph already covers, and about
     giving the user the existing context before new results bury it.

2. **Check for an LLM key.** Read `research-harness/.env` (or check
   `ANTHROPIC_API_KEY`/`OPENAI_API_KEY` in the environment). This determines
   which path to take:
   - **Key present (automatic path):** continue with steps 3-5 below.
   - **No key (console mode):** don't improvise — read
     `research-harness/.claude/skills/research-harness/references/console-mode.md`
     and follow that flow yourself (you do the extraction/merge judgment
     calls it describes), scaling how many sources you process by the same
     depth table above. This is still "using, not editing" — you're reading
     its documented manual workflow, not modifying the project.

3. **Run**: `uv run research-harness run "<topic>" --max-results <N from table>`
   (or, if step 1 led to a decision to deepen existing ideas instead of/in
   addition to a fresh run, do that per step 4). Read the JSON summary. If
   most outcomes are `"stage": "skip"` (already processed/trashed), say so
   plainly — don't silently report a hollow success; this is expected and
   useful if step 1 already told you the ground was covered.

4. **Deepen** (skip if depth is `quick`, unless step 1's judgment call chose
   deepening existing ideas specifically): for each relevant `idea_id`
   (from the run's output, and/or from step 1's survey if deepening
   existing ideas), `uv run research-harness deepen "<idea-id>" --max-results
   5`. Repeat for the configured number of rounds, folding in any new idea
   ids `extends`-linked by the previous round. Stop early on an idea if a
   round returns no new/updated ideas for it.

5. **Record the request**: once step 3/4 are done, `uv run research-harness
   record-run "<topic>" <idea-id>...` in console mode (the automatic path's
   `run`/`deepen` already records this internally, so skip this call if a key
   was present in step 2) — pass every idea id touched across the whole
   request (initial run plus every deepen round), not just the initial run's.

6. **Report**, in plain language, not raw JSON:
   - What step 1 found already in the graph, and what you did about it
     (proceeded fresh, merged into existing coverage, deepened instead).
   - How many sources were fetched/converted/extracted/skipped and why.
   - How many ideas were created vs. updated, and under which topics
     (`uv run research-harness list-topics` if useful for context).
   - Anything that looked off-topic or low-signal enough that the user might
     want to `trash-source`/`trash-idea` — surface it as a suggestion, don't
     trash it yourself without asking (that's a judgment call, same as in
     the interactive skill).
   - The vault path so they know where to look.

## Out of scope

- Consensus/ResearchRabbit imports (manual export files) — those need a
  file path from the user; if they want that, use the `import` command per
  `references/commands.md` in the research-harness skill, same depth-based
  deepen loop afterward.
- Anything requiring a change to research-harness itself (new connector,
  changed pipeline behavior, model swap, etc.) — that's a code change, hand
  it back to the user or make it in a separate conversation about the
  project directly, not through this driver skill.
