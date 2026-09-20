# Console mode (no API keys)

When `ANTHROPIC_API_KEY`/`OPENAI_API_KEY` are not configured, extraction and
merging are done by **you** (the agent) directly instead of an API call. Use
this staged flow instead of `run`/`import`/`deepen`, which require an LLM key.

## 1. Search and pick candidates

```
uv run research-harness search "<topic>" --source arxiv --max-results 10 > /tmp/results.json
```
`--source semanticscholar` works the same way, and also unlocks `lookup`/
`related`/`recommend`/`enrich` — none of these need an LLM key either. Use
`enrich results.json` to fill in a missing DOI/abstract/PDF url before
fetching, and `related "<id>" citations`/`references` to expand from a paper
you already have rather than a fresh keyword search. Read the JSON. Drop
anything off-topic. If you're keeping a subset, write the trimmed list to a
new file before continuing.

## 2. Check dedup/trash before spending effort

```
uv run research-harness source-status "<identifier>"
```
Skip anything already `trash` or `processed`.

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

## 5. Ingest

Write a JSON file: a list of `{"id": <existing-id-or-omit>, "gist":, "knowledge":, "open_questions":, "topic":, "tags":}`,
then:
```
uv run research-harness ingest-ideas "<source-identifier>" ideas.json
```
This writes the note(s), marks the source `processed`, and rebuilds the
index — no LLM call anywhere in this step.

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
