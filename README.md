# LPS — Lazy Person's Skills

> A private collection of reusable skills for ChatGPT, Codex, and Claude that turns recurring workflows into repeatable instructions.

LPS keeps personal assistant skills in one versioned repository so they can be reviewed, backed up, and installed on another machine without rebuilding them from chat history. It also keeps third-party skills in a separate, provenance-tracked collection for installation tools. The personal collection covers software testing, repository quality, materials-science conventions, divergent ideation, context compression, publication research, and plotting on request.

## Contents

### Common skills

These skills are shared across assistants; individual workflows may require tools or connectors listed below.

| Skill | Purpose |
| --- | --- |
| [`adhd-mode`](common/adhd-mode/) | Generates ideas through separate cognitive frames, then scores, clusters, and deepens the strongest options. |
| [`dogusariturk-python-style`](common/dogusariturk-python-style/) | Applies Doguhan Sariturk's production Python conventions when writing, reviewing, refactoring, or structuring Python code. |
| [`github-repo-standards`](common/github-repo-standards/) | Scaffolds and audits professional GitHub repositories, documentation, automation, and community files. |
| [`matsci-python-antipatterns`](common/matsci-python-antipatterns/) | Flags common README and repository mistakes in materials-science Python projects. |
| [`plot-on-request`](common/plot-on-request/) | Creates plots only when explicitly requested, using real data and Python, then saves and presents PNG files. Clearly labeled synthetic examples require an explicit request. |
| [`research-publications`](common/research-publications/) | Searches Consensus first when finding papers, falls back to scholarly web sources when needed, and converts research PDFs to Markdown with MarkItDown before analysis. |
| [`rigorous-pytest-suite`](common/rigorous-pytest-suite/) | Builds disciplined pytest suites, fixtures, tooling, and matching CI for Python projects. |

### ChatGPT / Codex skills

| Skill | Purpose |
| --- | --- |
| [`lps-add-skill-chatgpt`](chatgpt/lps-add-skill-chatgpt/) | Creates, imports, or updates LPS skills from ChatGPT / Codex, with repository-tool and draft-only workflows and authorized publishing. |

### Claude only

| Skill | Purpose |
| --- | --- |
| [`context-compactor`](claude/context-compactor/) | Archives large or repeated tool output to a file handle, keeps only a compact excerpt in context with exact paged recall, feeds handles into checkpoints, and fuses edits with their narrow follow-up validation. |
| [`full-paths`](claude/full-paths/) | Always states the complete absolute path for any file created, edited, or referenced, instead of a bare filename. |
| [`git-advanced`](claude/git-advanced/) | Applies safe defaults for git operations that could rewrite history or discard work — rebase, force-push, reset/clean, branch deletion, conflicts, bisect — with explicit what-to-do / what-not-to-do guidance. |
| [`lps-add-skill`](claude/lps-add-skill/) | Creates, imports, or updates LPS skills from Claude, maintains the README catalog, and commits or pushes when authorized. |
| [`research-harness`](claude/research-harness/) | Drives the research-harness idea-graph CLI interactively — search, fetch, extract, and merge papers into an Obsidian vault (topics nest under a general-topic folder), plus Semantic Scholar discovery and NotebookLM export/query. |
| [`research-harness-explore`](claude/research-harness-explore/) | Mines the existing research-harness idea graph for new research directions by intersecting two or more concept clusters, proposing candidate topics, and growing the promising ones via the deepen loop. |
| [`research-harness-run`](claude/research-harness-run/) | Drives a full research-harness pass end-to-end as a black box given just a topic and a depth level, without reading or editing the project's own source or skill. |
| [`skill-benchmark`](claude/skill-benchmark/) | Statically scores and ranks every installed skill on description quality, tool scoping, staleness, size, and overlap with other skills, printed as a console table. |
| [`skill-hierarchy`](claude/skill-hierarchy/) | Resolves conflicts between loaded skills by having the more specific skill win on the exact point of disagreement, leaving the general skill in force elsewhere. |
| [`tencentdb-agent-memory`](claude/tencentdb-agent-memory/) | Reads and writes a local, API-free project-memory store modeled on TencentDB Agent Memory's layered design (persona / scenarios / atomic facts), with Claude performing the distillation directly instead of Docker, a service, or an LLM API key. |

### Claude Code mods

[`mods/`](mods/) holds the Claude Code mods I use: my edited versions of `prismantis` and `flightdeck`, plus links to the others.

### Third-party skills

Third-party skills are stored under [`external/`](external/) and excluded from the personal-skill bulk-install commands. Each entry retains its upstream directory structure, source URL, exact commit, and available license or notice files.

| Source collection | Skill packages |
| --- | ---: |
| [AI behavior-fix catalog](external/catalogs/ai-behavior-fix-skills.md) | 76 |
| [Materials-science Python catalog](external/catalogs/materials-science-python-skills-direct.md) | 80 |
| [RTK](external/sources/rtk-ai/rtk/) | 12 |
| [Ponytail](external/sources/dietrichgebert/ponytail/) | 6 |
| [Microsoft Data Formulator](external/sources/microsoft/data-formulator/) | 3 |
| [Diagram Design](external/sources/cathrynlavery/diagram-design/) | 1 |

The two catalogs overlap, so their counts should not be added together. The external collection currently contains 129 unique vendored skill packages from 18 upstream repositories. See the [external manifest](external/MANIFEST.csv) and [source inventory](external/README.md) for exact paths and revisions.

[`headroomlabs-ai/headroom`](external/sources/headroomlabs-ai/headroom/) also lives under `external/`, but it is original usage guidance for that third-party tool rather than a vendored copy of an upstream `SKILL.md`, so it is not counted in the totals above and is not listed in the manifest.

Each skill is self-contained. Its `SKILL.md` defines when it should run and how the assistant should apply it; supporting references, examples, scripts, and assets stay beside that file.

### Workflow requirements

- **Publication research:** Python with `markitdown[pdf]` for PDF conversion. The skill prefers a Consensus connector and explicitly falls back to scholarly web search when that connector is unavailable. Its tool names may need mapping to the host assistant's tools. Image-only pages and figures require PDF rendering or OCR; the referenced `pdf-reading` helper is not bundled in LPS.
- **Plotting:** A Python environment with matplotlib and file-output support; pandas or NumPy may be needed for the input data. The skill uses prose or tables unless the user requests a plot.

The publication and plotting skills retain the supplied source text. Local files are stored as unpacked skill directories; `.skill` archives and duplicate standalone Markdown exports are not needed for installation.

## Install

Clone the private repository with an authenticated GitHub account:

```powershell
git clone https://github.com/kyryl-shtefiienko/LPS.git
Set-Location LPS
```

Install all ChatGPT Codex skills on Windows:

```powershell
New-Item -ItemType Directory -Force "$env:USERPROFILE\.codex\skills" | Out-Null
Copy-Item -Recurse -Force .\common\* "$env:USERPROFILE\.codex\skills\"
Copy-Item -Recurse -Force .\chatgpt\* "$env:USERPROFILE\.codex\skills\"
```

Install all Claude skills on Windows:

```powershell
New-Item -ItemType Directory -Force "$env:USERPROFILE\.claude\skills" | Out-Null
Copy-Item -Recurse -Force .\common\* "$env:USERPROFILE\.claude\skills\"
Copy-Item -Recurse -Force .\claude\* "$env:USERPROFILE\.claude\skills\"
```

Restart the relevant app or begin a new conversation after installation so its skill catalog refreshes.

## Usage

Ask the assistant for a task that matches a skill's description, or name the skill explicitly when you want to force that workflow. Each assistant reads the installed `SKILL.md` and applies its instructions; scripts and templates remain local resources for that skill.

For example, ask ChatGPT Codex to “set up rigorous pytest coverage” to use `rigorous-pytest-suite`.

Examples for the new workflows:

- “Use research-publications to find papers on precipitation kinetics and compare their methods.”
- “Use plot-on-request to plot temperature versus time from this CSV and return a PNG.”

## Add or update a skill

Use `lps-add-skill` in Claude or `lps-add-skill-chatgpt` in ChatGPT / Codex to handle this workflow. For example: "Add this skill to LPS, update the README, and push the changes." Without repository access, either version prepares files for handoff and reports what still needs to be applied.

1. Put cross-platform skills under `common/<skill-name>/`, ChatGPT / Codex skills under `chatgpt/<skill-name>/`, and Claude-only skills under `claude/<skill-name>/`.
2. Keep `SKILL.md` at the root of the skill directory.
3. Store only resources referenced by that skill, such as `references/`, `assets/`, `scripts/`, or `examples.md`.
4. Update the contents table above when adding or removing a skill.
5. Review changes so credentials, machine-specific paths, and generated files stay out of the repository. Stage, commit, or push only when explicitly requested.

## License

This is a private personal collection. No repository-wide license is declared. Individual skills retain any license metadata stated in their own `SKILL.md` files.
