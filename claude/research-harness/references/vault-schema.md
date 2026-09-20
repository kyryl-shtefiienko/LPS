# Vault schema

The vault (`$OBSIDIAN_VAULT_PATH`) holds only ideas — no per-paper notes.
Ideas are grouped into per-topic subfolders under `Ideas/` so the vault stays
browsable as it grows, instead of collapsing into one flat pile of files.

```
vault/
  Ideas/{topic}/{id}.md   # active idea notes, grouped by topic subfolder
  Trash/{id}.md            # trashed idea notes (flat — not grouped; still readable, wikilinks still resolve)
  Topics/{topic}.md          # AUTO-GENERATED sorted index of one topic's ideas — don't hand-edit, `reindex` overwrites it
  Topics/index.md              # AUTO-GENERATED top-level list of every topic + its idea count
  Runs/{date}-{topic}.md          # one persistent record per research request — written once by `record-run`, never regenerated
  Runs/index.md                     # AUTO-GENERATED list of every run note, newest first — `reindex` rebuilds it
  _index/ideas.db                      # derived FTS5 cache — never hand-edit, `reindex` rebuilds it
```

`{topic}` may itself be a `/`-separated path, e.g.
`cold-spray-additive-manufacturing/simulation` — a slash in a topic slug is
just another directory separator, so both `Ideas/` and `Topics/` nest under
that general-topic folder exactly the way a plain topic sits directly under
`Ideas/`. Use this to keep a growing vault organized as one folder per
general subject area (see the "Topic slugs nest..." guidance in `SKILL.md`).

`id` is unique **vault-wide**, not just within a topic — Obsidian wikilinks
resolve by filename regardless of folder, and `research-harness` looks ideas
up by id the same way (searching recursively), so moving or regrouping files
never breaks a `[[link]]`. An idea with no topic set lands in
`Ideas/uncategorized/`.

## Browsing: Topic pages and CLI commands

`reindex` (also run automatically by `run`/`deepen`/`ingest-ideas`/etc.)
regenerates `Topics/*.md`: one sorted table per topic, plus a top-level
`Topics/index.md` linking to all of them. Pick the sort order with
`--sort {updated|depth|id}` (default `updated`: most recently touched
first). These pages are fully regenerated every time — never hand-edit them.

To browse without opening Obsidian: `research-harness list-topics` (topic
names + idea counts) and `research-harness list-ideas [--topic X] [--sort
updated|depth|id]` (the same grouping/sorting, as JSON, straight to the
terminal).

## Run notes: what one request produced

Every `run`/`import`/`deepen` call (and, in console mode, every explicit
`record-run`) writes one `Runs/{date}-{topic-slug}.md` note: a frontmatter
block (`type: run`, `topic`, `date`, `idea_count`) plus a plain list of
`[[idea-id]]` wikilinks to everything that request touched. Unlike Topic
pages, this is **not regenerated** — it is written once and stays a true
record of that request even after the ideas it lists are later edited,
merged, or trashed. `Runs/index.md` (auto-generated, newest first) is the
one thing here that *is* rebuilt on every `reindex`.

Use a run note when you want "what did I get out of running the harness on
X last Tuesday" without reconstructing it from source-identifier timestamps.

## Idea note (`Ideas/{topic}/{id}.md`)

```yaml
---
id: cold-spray-particle-bonding-mechanism
type: idea
topic: cold-spray-additive-manufacturing/bonding-mechanism
status: active            # active | trash
depth: 1                    # incremented each time `deepen` runs on this idea
created: 2026-09-19
updated: 2026-09-19
gist: "One compressed sentence — the only thing scanned by `query`."
sources: [10.1016/j.actamat.2023.118877, arxiv:2401.01234]
relations:
  related_to: ["[[adiabatic-shear-instability]]"]
  contradicts: []
  extends: []
tags: [#cold-spray, #bonding-mechanism]
---
## Knowledge
As complete a writeup as the source material supports.

## Open Questions / To Deepen
Gaps `deepen` will turn into follow-up search queries.

## Sources
- 10.1016/j.actamat.2023.118877
- arxiv:2401.01234
```

`relations` are writable, not just readable: `link-ideas <id-a> <relation>
<id-b>` adds a link between two existing ideas, and `ingest-ideas` accepts
`related_to`/`contradicts`/`extends` per item (each unioned into the note's
existing list, never overwritten). `related_to` is symmetric — linking A to
B also links B to A; `extends`/`contradicts` are directional.

`sources` are bare identifiers only — no cached titles/authors. Full
bibliographic detail lives in Zotero (if the optional sync is configured) or
can be looked up by DOI when actually needed; duplicating it here was a
deliberate simplification, not an oversight.

`gist` is the only field `query` scans — keep any manual edits to it short.
The `Knowledge` section has no such pressure; completeness there is the
point.
