---
name: research-publications
description: Use whenever the task involves finding, reading, or analyzing academic papers, publications, preprints, studies, or research PDFs (uploaded or found online) — literature reviews, "find papers on X", summarizing a study's findings, comparing multiple papers, or pulling data out of a research PDF. Two rules apply no matter how the request is phrased — (1) when publications need to be found, search Consensus (peer-reviewed academic search over 220M+ papers) before falling back to general web search, so results are relevant peer-reviewed papers instead of generic web hits, and (2) before analyzing any PDF or publication's content, convert it to Markdown with markitdown first and read/analyze from that .md file rather than the raw PDF. Trigger this even if the user never says "markitdown" or "Consensus" by name — e.g. "find some recent papers on CRISPR delivery and summarize what they found", "read this study and tell me what they concluded", "compare these three papers on X".
---

# Research Publications Workflow

Two rules govern this workflow, in this order: search Consensus before the open web when you need to *find* papers, and convert to Markdown with markitdown before you *analyze* any PDF. Both exist for the same underlying reason — a specialized tool built for the job gives cleaner, more consistent input to work from than a generic one, which pays off the moment more than one paper or one analysis step is involved.

## Step 1 — Finding publications: Consensus first

When the task requires finding papers (rather than analyzing ones already in hand):

1. **Load Consensus.** If `mcp__Consensus__search` isn't already in your tool list, call `tool_search` with keywords like `["consensus", "academic papers", "research search"]` to load it.
2. **Search before committing to a reading list.** Run one or more `mcp__Consensus__search` queries covering the topic. Split a multi-part question into separate queries — a combined query returns shallower coverage of each part, same as with regular web search.
3. **Treat it as the primary pass, not the only one.** If Consensus comes back thin or empty (a very new preprint it hasn't indexed yet, a topic outside peer-reviewed literature), supplement with `web_search`/`web_search_fast` — but always try Consensus first for anything that's an academic or research question, and lead with what it found.
4. **Build the candidate list before opening any PDFs.** Note title, authors, venue/year, and link or DOI for each candidate, then decide which ones are worth pulling full text for.

If no Consensus connector is available at all in this session, say so and fall back to web search biased toward scholarly sources (journal sites, PubMed, arXiv, etc.) rather than silently skipping the academic-search step.

## Step 2 — Analyzing a PDF or publication: markitdown first

Whenever a PDF is about to be read or analyzed — whether it came from the Consensus search above, a link the user gave you, or a file they uploaded — convert it to Markdown before doing anything else with its content:

```bash
# first time only; use [all] instead of [pdf] if docx/pptx/xlsx are also in play
pip install "markitdown[pdf]" --break-system-packages

markitdown /path/to/paper.pdf -o /path/to/paper.md
```

Or from Python, which is more convenient when converting several papers in a loop:

```python
from markitdown import MarkItDown

md = MarkItDown()
result = md.convert("/path/to/paper.pdf")
with open("/path/to/paper.md", "w") as f:
    f.write(result.text_content)
```

Then read, quote, summarize, and analyze from the resulting `.md` file — not the original PDF, and not a raw `pdftotext`/`pypdf` dump. Markitdown preserves headings, section structure, and tables, which is exactly what's needed to correctly attribute a claim to "Methods" vs. "Discussion," pull a results table cleanly, or line sections up across papers for comparison.

**Batch conversion for multi-paper tasks.** If the task involves several papers (a literature review, a comparison table across studies), convert every PDF to its own `.md` file first, then read and analyze the full set together. Don't interleave "convert one, analyze one, convert the next" — having the whole set already in clean Markdown up front makes cross-paper comparison far easier.

**When markitdown isn't enough.** It converts text, tables, and structure, but not visual-only content — a chart with no underlying data table, an equation rendered as an image. For those specific pages, fall back to the `pdf-reading` skill's rasterize-and-view approach, while still treating the markitdown output as the source of truth for everything else in the paper. If markitdown fails outright on a scanned/image-only PDF with no text layer, that's also a case for `pdf-reading`'s OCR/rasterize path for that particular file.

## Putting it together

For a request like "find recent papers on X and summarize what they found," or "here's a PDF, what did this study conclude":

1. If papers need to be found → Consensus first (Step 1), web search only as backup.
2. For every PDF that will actually be analyzed → convert to Markdown with markitdown first (Step 2).
3. Read and analyze from the `.md` output.
4. Synthesize across papers and cite appropriately — paraphrase findings in your own words rather than quoting large chunks, same as any other sourced writing.

## Scope

This skill covers *finding and analyzing* publications. For PDF creation, form-filling, merging, splitting, or encryption, use the `pdf` skill instead. For extraction mechanics beyond what markitdown gives you — embedded images, form fields, targeted page rasterization — `pdf-reading` still applies; reach for it as a supplement once you're working from the markitdown output, not as the first step.
