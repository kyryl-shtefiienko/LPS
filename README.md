# LPS — Lazy Person's Skills

> A private collection of reusable skills for ChatGPT, Codex, and Claude that turns recurring workflows into repeatable instructions.

LPS keeps personal assistant skills in one versioned repository so they can be reviewed, backed up, and installed on another machine without rebuilding them from chat history. It also keeps third-party skills in a separate, provenance-tracked collection for installation tools. The personal collection covers software testing, repository quality, materials-science conventions, divergent ideation, and adding skills to this repository.

## Contents

### Common skills

These skills are shared across assistants; individual workflows may require tools or connectors listed below.

| Skill | Purpose |
| --- | --- |
| [`adhd-mode`](common/adhd-mode/) | Generates ideas through separate cognitive frames, then scores, clusters, and deepens the strongest options. |
| [`dogusariturk-python-style`](common/dogusariturk-python-style/) | Applies Doguhan Sariturk's production Python conventions when writing, reviewing, refactoring, or structuring Python code. |
| [`github-repo-standards`](common/github-repo-standards/) | Scaffolds and audits professional GitHub repositories, documentation, automation, and community files. |
| [`matsci-python-antipatterns`](common/matsci-python-antipatterns/) | Flags common README and repository mistakes in materials-science Python projects. |
| [`rigorous-pytest-suite`](common/rigorous-pytest-suite/) | Builds disciplined pytest suites, fixtures, tooling, and matching CI for Python projects. |

### Claude only

| Skill | Purpose |
| --- | --- |
| [`lps-add-skill`](claude/lps-add-skill/) | Creates, imports, or updates LPS skills from Claude, maintains the README catalog, and commits or pushes when authorized. |
| [`research-harness-run`](claude/research-harness-run/) | Drives a full research-harness pass end-to-end as a black box given just a topic and a depth level, without reading or editing the project's own source or skill. |

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

## Install

Clone the private repository with an authenticated GitHub account:

```powershell
git clone https://github.com/kyryl-shtefiienko/LPS.git
Set-Location LPS
```

Install the common skills for ChatGPT Codex on Windows:

```powershell
New-Item -ItemType Directory -Force "$env:USERPROFILE\.codex\skills" | Out-Null
Copy-Item -Recurse -Force .\common\* "$env:USERPROFILE\.codex\skills\"
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

## Add or update a skill

Use `lps-add-skill` in Claude to handle this workflow. For example: "Add this skill to LPS, update the README, and push the changes." Without repository access, it prepares files for handoff and reports what still needs to be applied.

1. Put cross-platform skills under `common/<skill-name>/` and Claude-only skills under `claude/<skill-name>/`.
2. Keep `SKILL.md` at the root of the skill directory.
3. Store only resources referenced by that skill, such as `references/`, `assets/`, `scripts/`, or `examples.md`.
4. Update the contents table above when adding or removing a skill.
5. Review changes so credentials, machine-specific paths, and generated files stay out of the repository. Stage, commit, or push only when explicitly requested.

## License

This is a private personal collection. No repository-wide license is declared. Individual skills retain any license metadata stated in their own `SKILL.md` files.
