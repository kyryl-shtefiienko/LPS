# README standards

A README has one job: get a stranger from "found this repo" to "understands what it does, and can try it" as fast as possible. Everything below serves that job. If a section doesn't serve it, cut the section.

## Section-by-section

### Title and one-line pitch
The project name as an H1, then a single italic or blockquote line describing what it does. Not "A tool for X" (vague) — say what it actually does: "Converts messy CSV exports into normalized Parquet files." A reader should know from this line alone whether to keep reading.

### Badges
Row of shields.io-style badges directly under the pitch: build status, license, latest version, package registry link. Rules:
- Only include a badge for something that's true *right now*. A red/failing badge or a badge pointing at a workflow that doesn't exist is worse than no badge.
- Order by what a reader cares about most: build status first (is this maintained?), then license, then version.
- Don't stack more than ~5-6 badges; past that it reads as clutter rather than signal.

### Table of contents
Only needed once the README is long enough that scrolling to find something is annoying — roughly, once it has more than 5-6 major sections. A short README (install + quickstart + license) doesn't need one.

### About / description
2-4 sentences. Expand on the one-line pitch with: what problem it solves, who it's for, and — only if genuinely true — what makes it different from the obvious alternative. Don't pad this with marketing adjectives ("blazing fast", "next-generation", "enterprise-grade") unless there's a benchmark or fact backing the claim up. Concrete beats impressive-sounding.

### Screenshots / demo
For anything with a visual or CLI output component, a screenshot or short GIF answers "what does using this actually look like?" faster than any amount of prose. Not needed for libraries with no visual surface.

### Features
3-6 bullets, each one concrete capability, not a restated pitch. Lead with what a reader would care about most, not what was hardest to build.

### Install
Every command must be copy-pasteable, in order, from a clean environment, with no silent prerequisites. If there's a prerequisite (a specific runtime version, a system package), state it in one line before the block rather than assuming it.

### Quickstart
The single highest-value section in the whole file. A reader should be able to paste this block and see a working result with zero edits — if it needs an API key or a config file first, say so in one short line immediately before the block, not buried in prose above it. **Test the quickstart yourself before publishing it.** A quickstart that silently assumes an environment variable is already set is a common, easy-to-miss failure.

### Usage / configuration
Deeper usage than the quickstart: configuration options, common flags, how to do the second and third most common things (not just the first). Once this grows past a few screens, move it to `docs/` and link to it rather than letting the README balloon — a README's job is orientation, not being the entire manual.

### API reference
For a library: either inline (short APIs) or linked to generated docs / `docs/api.md` (larger surface area). Don't hand-write exhaustive API docs into the README for anything beyond a handful of functions — it goes stale immediately and is painful to maintain by hand.

### Architecture (optional)
Worth a section, often with a diagram, once the project has enough moving parts that "how does this fit together" is a real question a contributor would ask. Skip this for anything simple.

### Roadmap (optional)
A short list of what's planned, or a link to the issue tracker's roadmap/milestones. Keep it short — a long aspirational roadmap that never moves erodes trust faster than no roadmap at all.

### FAQ (optional)
Only add this once real, repeated questions exist (from issues, Discussions, or support channels). A speculative FAQ answering questions nobody's actually asked is just padding.

### Contributing
One or two lines plus a link to `CONTRIBUTING.md` — don't duplicate that file's content here.

### License
One line: which license, and a link to the `LICENSE` file. Don't summarize the license's terms in prose; the file is the source of truth and a paraphrase can be legally imprecise.

### Acknowledgments (optional)
Credit for dependencies, inspiration, or contributors who deserve a specific callout beyond the contributors graph.

## Writing style

- **Active voice, concrete verbs.** "Parses log files into structured events" beats "Log files can be parsed."
- **Show, don't just tell.** A code block demonstrating behavior beats a paragraph describing it.
- **Avoid unqualified superlatives.** "Fast," "simple," "powerful" are meaningless without a comparison or number. If it's actually fast, show a benchmark.
- **Write for a reader with zero context.** They don't know your project's internal vocabulary yet — define terms on first use.

## Good vs. bad, side by side

**Bad:** "This is an awesome, blazing-fast library for handling data."
**Good:** "Parses CSV files up to 10x faster than the standard library by streaming rows instead of loading the whole file into memory."

**Bad:** "Install the dependencies and run the script."
**Good:**
```bash
pip install -r requirements.txt
python main.py --input data.csv
```

**Bad:** a wall of unbroken prose describing every configuration option in paragraph form.
**Good:** a table with columns Option / Default / Description.

## Length and accessibility

- A typical single-package project's README runs roughly 100-300 lines. Past that, it usually means "Usage" or "API reference" belongs in `docs/` instead.
- Give images meaningful alt text — screen readers and search both rely on it.
- Don't encode meaning in color or emoji alone (e.g. a red vs. green dot with no label); pair it with text.
