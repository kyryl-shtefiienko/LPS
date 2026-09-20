# Console mode (no API keys)

When `ANTHROPIC_API_KEY`/`OPENAI_API_KEY` are not configured, extraction and
merging are done by **you** (the agent) directly instead of an API call. Use
this staged flow instead of `run`/`import`/`deepen`, which require an LLM key.

## 1. Search and pick candidates

Prefer `discover`/`discover-for-idea` over a bare `search` call — they run
the same connector channels (`discover` = keyword search, `discover-for-idea`
= citation expansion + recommendations + your own keyword queries) but
additionally dedup against known `trash`/`processed` sources automatically
(step 2 below, done for you) and **persist** the resulting candidate list as
a batch, so if this session ends mid-screening, a later one can resume with
`show-discovery-batch <batch-id>` instead of re-searching or guessing what
was already looked at:
```
uv run research-harness discover "<topic>" --max-results 10
uv run research-harness discover-for-idea "<idea-id>" --query "<query one>" --query "<query two>"
```
Read the printed `candidates` (or re-fetch them later via
`show-discovery-batch`). Drop anything off-topic — the rest of this flow
only needs whichever subset you're keeping; you don't need to write it back
anywhere, just pass those specific candidate objects to `fetch-pdfs` next.

A bare `search "<topic>" --source arxiv --max-results 10` still works too
(and `--source semanticscholar` also unlocks `lookup`/`related`/`recommend`/
`enrich`, none of which need an LLM key either — `enrich results.json` fills
in a missing DOI/abstract/PDF url, `related "<id>" citations`/`references`
expands from a paper you already have) — use it directly only when you
specifically don't want the batch persisted, or need one of these other
capabilities `discover` doesn't wrap.

## 2. Check dedup/trash before spending effort (skip if you used `discover`)

```
uv run research-harness source-status "<identifier>"
```
Skip anything already `trash` or `processed`. Not needed after
`discover`/`discover-for-idea` — they already excluded these.

## 3. Fetch and convert

```
uv run research-harness fetch-pdfs results.json --out data/pdfs
uv run research-harness convert fetch-pdfs-output.json --out data/converted
```
(Save each command's JSON output to a file to feed the next stage.)

## 4. Read the converted markdown yourself and extract ideas

Read the `.md` file at the `converted_path` from step 3. Extract distinct
ideas the same way the built-in LLM prompt would (see
`src/research_harness/extraction/prompts.py` for the exact instructions if
you want to match its shape precisely): each idea needs a one-sentence
`gist`, a complete `knowledge` writeup, an `open_questions` note, a `topic`
slug, and short `tags`. Don't write a paper-level summary — extract the
underlying mechanisms/findings/methods as their own ideas.

**Capture broadly, not just what's on-topic.** Once a paper is fetched, don't
filter its extracted ideas back down to only what matches the search query
that found it — a paper fetched for one topic often contains a genuinely
useful mechanism, dataset detail, or technique that belongs to a completely
different topic. Extract it anyway, and give it whichever `topic` slug
actually fits *that idea's own* subject matter, not the run's search topic.
An attempted approach plus its result is a valid idea even when the result
was negative or null ("X was tried and didn't help" is still worth keeping).
The only filtering that belongs in this pipeline is at the paper level (step
1: don't fetch an obviously irrelevant paper) — once fetched, extract
everything durable it contains.

For each candidate idea, check whether it should merge into something that
already exists:
```
uv run research-harness match-idea "<topic>" "<gist>"
```
If it returns a match, read that existing idea's `Knowledge` section
(from the JSON, or read the note file directly) and write the merged
knowledge text yourself — extend it, note agreement/contradiction, don't
just concatenate.

**Also extract a definition for every acronym/jargon term you use.** As you
write each idea's `gist`/`knowledge`/`tags`, notice any acronym or technical
term a reader outside this subfield wouldn't already know (CFD, RANS, an
uncommon method name — not every tag needs this, just genuine jargon). A tag
like `#cfd` with no note anywhere explaining what CFD is is a dead end for
whoever reads the graph later. For each such term, check it's not already
defined:
```
uv run research-harness find-definition "<term>"
```
If nothing comes back, add a `kind: "definition"` element to the same
ingest batch: `gist` is the bare term itself (e.g. `"CFD"`, nothing more —
this is what `find-definition` matches on), `knowledge` is a clear
explanation of what it means and how this paper uses it, `open_questions`
empty, `topic`/`tags` same as you'd pick for a finding on this subject.

## 5. Ingest

Write a JSON file: a list of `{"id": <existing-id-or-omit>, "gist":, "knowledge":, "open_questions":, "topic":, "tags":, "kind": <omit for "finding", or "definition">, "evidence": <optional>}`
— findings and definitions for the same source can mix in one list — then:
```
uv run research-harness ingest-ideas "<source-identifier>" ideas.json
```
This writes the note(s), marks the source `processed`, and rebuilds the
index — no LLM call anywhere in this step.

**Back a finding with evidence whenever you're quoting or paraphrasing a
specific result**, not just summarizing the paper in general. Each entry:
`{"source": "<source-identifier>", "excerpt": "<verbatim span from that
source's converted text>", "location": "<section/page, optional>",
"conditions": "<optional>", "type": "reported_finding" (default),
"author_interpretation", or "harness_inference"}`. Copy `excerpt` straight
from the converted text you already read — don't retype it from memory —
since the first two `type`s are checked against that cached text and a
mismatch fails the whole ingest batch. If you don't already have the
converted text open, `search-source-text "<topic>" --source
"<source-identifier>"` finds a matching chunk to copy from without reading
the whole file. Use `harness_inference` for a conclusion you drew yourself
rather than something the source states.
Example:
```json
{
  "gist": "Coating porosity drops sharply above 500 m/s particle velocity",
  "knowledge": "...",
  "topic": "cold-spray-additive-manufacturing/process-parameters",
  "evidence": [
    {
      "source": "10.1016/j.example.2024.01.001",
      "excerpt": "porosity decreased from 8.2% to 1.1% as impact velocity increased from 400 to 550 m/s",
      "location": "Section 3.2, Fig. 4",
      "type": "reported_finding"
    }
  ]
}
```

## 6. Review, trash, deepen

Same as the automatic flow: `trash-source`/`trash-idea` for anything that
turned out useless, and for `deepen`, generate the 2-4 follow-up queries
yourself from the idea's "Open Questions" section instead of calling
`deepen` (which requires an LLM key) — then run steps 1-5 again scoped to
those queries, feeding results back into the same idea id.

If two already-ingested ideas turn out to be connected (one motivates,
contradicts, or extends the other) but aren't similar enough for
`match-idea` to catch, link them explicitly:
```
uv run research-harness link-ideas "<id-a>" related_to "<id-b>"
```
(`related_to` is symmetric; use `extends`/`contradicts` for a directional
relation.) Don't hand-edit a note's frontmatter for this — always go through
`link-ideas`.

## 7. Record the request

Once every source for this request has been ingested (and any immediate
deepening done), record what the whole request produced — once, not per
paper:
```
uv run research-harness record-run "<topic>" <idea-id-1> <idea-id-2> ... [--note "..."]
```
This writes a persistent `Runs/{date}-{topic}.md` note listing every idea
touched, so a future session can see "what did this request produce" without
reconstructing it from source-identifier timestamps.

## If something fails

Any CLI command's own failure (a connector error, a bad file, a crash) is
already persisted automatically to `logs/errors/{timestamp}-{context}.json`
— you don't need to do anything extra for that case, just report the error
message you were shown to the user and move on or retry as appropriate.

If instead *you* hit a failure that isn't a command error at all — a file
read failed, a paper's data turned out unusable, a judgment call went wrong
— record it the same way so it's reviewable later, instead of just letting
it scroll past:
```
uv run research-harness log-error "<context>" "<what went wrong>" [--detail "..."]
```
