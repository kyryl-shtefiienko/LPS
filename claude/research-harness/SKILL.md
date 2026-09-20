---
name: research-harness
description: Drive the research-harness pipeline interactively — search a topic (arXiv, Semantic Scholar, or a manual Consensus/ResearchRabbit/Litmaps export), look up papers by identifier, follow citation graphs, get recommendations, fetch and convert papers, extract distilled ideas with an LLM, merge them into the Obsidian idea graph, mark sources or ideas as trash, and deepen an idea with a targeted follow-up search. Use this skill when the user asks to research a topic, find papers on something, look up or recommend papers, add papers to their knowledge graph/vault, deepen or develop an idea further, or clean up (trash) a paper or idea that turned out useless.
allowed-tools: Bash Read
metadata:
  version: "0.1"
  openclaw:
    primaryEnv: ANTHROPIC_API_KEY
    envVars:
    - name: ANTHROPIC_API_KEY
      required: false
      description: Anthropic API key. Leave unset to use console mode (the agent extracts/merges ideas itself, no API call).
    - name: OPENAI_API_KEY
      required: false
      description: OpenAI API key. Leave unset to use console mode (the agent extracts/merges ideas itself, no API call).
    - name: OBSIDIAN_VAULT_PATH
      required: true
      description: Path to the Obsidian vault the idea graph lives in.
    - name: RESEARCH_HARNESS_DATA_DIR
      required: false
      description: Directory for sources.db and the markitdown conversion cache (default ./data).
    - name: ZOTERO_API_KEY
      required: false
      description: Optional — only used for the secondary, non-blocking bare-DOI Zotero sync.
    - name: ZOTERO_LIBRARY_ID
      required: false
      description: Optional Zotero library id, paired with ZOTERO_API_KEY.
    - name: ELSEVIER_API_KEY
      required: false
      description: Not yet usable — Elsevier/ScienceDirect is a stub pending a university API key.
    - name: SEMANTIC_SCHOLAR_API_KEY
      required: false
      description: Optional — Semantic Scholar works unauthenticated too, just at a lower rate limit.
---

# research-harness

Grows an **idea-centric** knowledge graph in Obsidian: the unit you search and
browse is an *idea* (a mechanism, method, finding, attempted approach, or
open question), not a paper. Papers are evidence, tracked by bare identifier
(DOI, or `arxiv:{id}`) only — never duplicated as their own notes.

**Capture broadly, tag by best fit.** Once a paper is fetched, extract every
durable idea it contains — not just the ones that match whatever topic was
searched for. A generically useful idea encountered in an off-topic paper is
still worth keeping; give it whatever `topic` slug fits *its own* content,
not necessarily the run's search topic. An attempted approach plus a
negative/null result is a valid idea too, not just headline findings.

**Back specific claims with claim-level evidence.** Beyond the bare source
list, an idea can carry an `evidence` list tying one particular piece of
`knowledge` to a verbatim excerpt of where it came from — see the
`evidence` field in `ingest-ideas` (`references/commands.md`). A quoted
excerpt is checked against the source's cached converted text before it's
written, so this only works for a source you've already converted, and the
excerpt must be copied, not retyped from memory.

**Topic slugs nest under a general-topic folder.** Use
`{general-topic}/{specific-subtopic}` as the `topic` slug (e.g.
`cold-spray-additive-manufacturing/simulation`, not a flat
`cold-spray-simulation`) — both `Ideas/` and `Topics/` mirror this on disk, so
`Ideas/{general-topic}/{specific-subtopic}/{id}.md`. Run `list-topics` first;
reuse an existing general-topic folder when the idea genuinely belongs there,
and only introduce a new top-level general topic when starting a subject
area with nothing existing to nest under. A topic with no natural subtopic
yet can just be `{general-topic}/overview` until it grows a natural split.

This skill sequences the `research-harness` CLI (`uv run research-harness
...`, run from the repo root) and reads its JSON output back with `Read`
between stages, so you can prune, dedupe, and make judgment calls a script
shouldn't make alone. Prefer the staged flow below over the `run` one-shot
for anything beyond a quick pass — that's the entire reason this lives in an
agent rather than a plain script.

**Check `ANTHROPIC_API_KEY`/`OPENAI_API_KEY` first.** If neither is set (the
common case — this project is designed to run without any LLM API key), use
**console mode**: `references/console-mode.md`. There, extraction and
merging are done by you directly — reading converted paper markdown and
deciding idea content yourself — via `fetch-pdfs`/`convert`/`match-idea`/
`ingest-ideas` instead of `run`/`import`/`deepen`. Even discovery itself
doesn't need a key: `discover`/`discover-for-idea` run the same connector
channels `run`/`deepen` do (search, citation expansion, recommendations),
just stopping before the LLM-requiring extract step, and persist the
resulting candidates so you can resume screening them later — see
"Discovery without an LLM key" in `references/commands.md`. Everything
below this point describes the automatic path, which only applies once a
key is configured.

## Staged flow (preferred, requires an LLM key)

1. **Search**: `uv run research-harness search "<topic>" --source arxiv --max-results 10`
   Prints raw `SearchResult` JSON. Read it and drop anything obviously
   off-topic before spending fetch/LLM budget on it — there's no `run`-style
   filtering step built in, so this is the point to exercise judgment.
2. **Run the kept results through the pipeline.** There's no separate
   fetch/convert/extract CLI stage for a live search result list today — the
   pragmatic path is `uv run research-harness run "<topic>" --max-results N`
   for the full topic, or narrow `--max-results` down first. If the search
   turned up results you don't want processed, tell the user you're running
   the full topic and let them confirm, rather than silently including
   everything.
3. **Review what came out.** The `run`/`import` JSON summary lists per-source
   outcomes (`fetch`, `convert`, `extract`, `merge`) and every `idea_ids`
   touched this run. For any source whose `extract` outcome shows few/no
   ideas or looks off-topic, trash it (step 5) right away — don't leave dead
   weight for a future run to re-skip silently.
4. **Inspect new/updated ideas** with `uv run research-harness query "<keywords>"`
   or by reading the note file directly under `$OBSIDIAN_VAULT_PATH/Ideas/`.
   Summarize what changed for the user in plain language — this is usually
   more useful to them than raw JSON.
5. **Trash judgment calls**:
   - A paper that looked promising but is useless: `uv run research-harness trash-source "<doi-or-identifier>"`.
   - An idea that turned out wrong/uninteresting: `uv run research-harness trash-idea "<idea-id>"`.
   Do this inline as you notice it, not as a separate cleanup pass.
6. **Deepen on request**: when the user says they want to explore an idea
   further, run `uv run research-harness deepen "<idea-id>" --max-results 5`.
   This generates targeted follow-up queries from the idea's own "Open
   Questions" section — it does not need a fresh topic from the user.

## Quick pass

`uv run research-harness run "<topic>" --max-results N` does search → fetch →
convert → extract → merge for every connector-returned result in one call.
Use it when the user just wants a fast first pass and accepts you'll trash
the noise afterward, not as the default for a careful research session.

## Discovery beyond keyword search (Semantic Scholar, Crossref, OpenCitations)

All keyless — no LLM key, no account, no API key needed for any of these
(Crossref/OpenCitations never require one at all; Semantic Scholar works
unauthenticated too, just at a lower rate limit):
- `uv run research-harness lookup "<identifier>" --source semanticscholar`
  (a bare DOI, or a prefixed id like `DOI:10.1/x`/`ARXIV:2401.01234`) or
  `--source crossref` (bare DOI only — Crossref's index is DOI-only).
- `uv run research-harness related "<identifier>" references` (what it
  cites) or `... citations` (what cites it) — `--source semanticscholar`,
  or `--source opencitations` for a pure citation-graph provider with wider
  DOI coverage than Semantic Scholar for many fields. OpenCitations results
  come back as **bare DOIs only** (no title/abstract/pdf_url) — `enrich`
  them against Crossref or Semantic Scholar before treating one as fetchable.
- `uv run research-harness recommend <seeds-file>` — given
  `{"positive": [...], "negative": [...]}`, both seed lists matter: negative
  seeds actively steer recommendations away from directions you've already
  ruled out, not just toward the positive ones. Semantic Scholar only.
- `uv run research-harness enrich <results-file>` — fills in a missing DOI/
  abstract/open-access-PDF-url on results from `search` or
  `import --parse-only`, without overwriting anything already present.

Calling an unsupported capability on a connector that doesn't implement it
(e.g. `recommend --source arxiv`) raises a clear capability error rather
than failing silently — check what a connector actually supports before
assuming it works the same way across all of them. Crossref never populates
`pdf_url` at all (its `link` metadata mixes free and paywalled full text
with no reliable way to tell them apart) — pass `--open-access-only` to
`discover`/`discover-for-idea` (see below) to drop these and any other
metadata-only result automatically instead of checking each one by hand.

## Sources with no API (Consensus, ResearchRabbit, Litmaps)

These have no public search API. Ask the user to export their results (CSV
or BibTeX) from the source's own web UI, then run:
`uv run research-harness import <consensus|researchrabbit|litmaps> <path-to-export> [--max-results N]`
— or add `--parse-only` first to see what the export actually parsed to
(no LLM key needed) before spending pipeline budget on it. Exports now
preserve abstract, an arXiv id derived from a URL/`eprint` field when no DOI
is present, and everything else in `raw_metadata`, instead of keeping only
title and DOI.

## NotebookLM (Gemini Notebook)

Requires the separately-installed `nlm` CLI (`uv tool install
notebooklm-mcp-cli`, then `nlm login` once — it opens a browser). This is a
second, complementary way to work with a topic's sources, not a replacement
for `markitdown`+LLM extraction (still the default ingestion path):
- `uv run research-harness export-to-notebook "<topic>"` pushes a topic's
  already-converted source files and idea notes into a Gemini Notebook,
  creating it on first call and only pushing what's new on later calls.
- `uv run research-harness query-notebook "<topic>" "<question>"` asks that
  notebook a question over its sources and returns the raw answer — read it
  yourself and decide what becomes a new/updated idea via `ingest-ideas`,
  same judgment call as everywhere else in console mode.
- Math in a notebook's answer (`\(...\)`/`\[...\]`, sometimes doubled to
  `\\(...\\)`) is auto-converted to Obsidian's `$...$`/`$$...$$` MathJax
  syntax whenever it lands in an idea's `gist`/`knowledge`/`open_questions`
  — no manual cleanup needed before folding a notebook answer into a note.

## Out of scope for now

- **Elsevier/ScienceDirect**: stubbed until the user has a university API
  key. If asked to search it, say so rather than attempting a scrape.
- **OpenAlex**: not yet added as a connector (planned as a secondary
  metadata/citation provider once its current rate-limit/auth model is
  re-verified against live docs — they were found inconsistent across
  cached snapshots during research).

## This isn't the only way in

Every command here is also exposed as a local MCP tool of the same name
(`src/research_harness/mcp_server.py`), so ChatGPT Desktop's Codex/agent
mode can drive research-harness the same way this skill does — see
`docs/quickstart.md`'s "Using this from ChatGPT Desktop (Codex)" section.
The CLI and the MCP server share the exact same underlying logic
(`src/research_harness/actions.py`), so nothing behaves differently between
the two. Any failure, from either entry point, is automatically persisted to
`logs/errors/{timestamp}-{context}.json` — see "If something fails" in
`references/console-mode.md`.

## Reference

See `references/console-mode.md` for the no-API-key flow (the default for
this project), `references/commands.md` for the full CLI surface and JSON
shapes, and `references/vault-schema.md` for the idea note frontmatter
schema (useful when reading a note directly with `Read` instead of `query`).

For mining the existing graph itself for new research directions (e.g. "find
research ideas at the intersection of Bayesian optimization and cold spray
additive manufacturing"), use the sibling `research-harness-explore` skill
instead — this skill is about growing the graph from papers, not
synthesizing across what's already in it.
