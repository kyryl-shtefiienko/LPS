# LPS — Lazy Person's Skills

> A private collection of reusable skills for ChatGPT Codex and Claude that turns recurring workflows into repeatable instructions.

LPS keeps personal assistant skills in one versioned repository so they can be reviewed, backed up, and installed on another machine without rebuilding them from chat history. The collection covers software testing, repository quality, materials-science conventions, divergent ideation, context compression, and model-effort selection.

## Contents

### Common skills

These skills work with both ChatGPT Codex and Claude.

| Skill | Purpose |
| --- | --- |
| [`adhd-mode`](common/adhd-mode/) | Generates ideas through separate cognitive frames, then scores, clusters, and deepens the strongest options. |
| [`github-repo-standards`](common/github-repo-standards/) | Scaffolds and audits professional GitHub repositories, documentation, automation, and community files. |
| [`headroom`](common/headroom/) | Configures and troubleshoots Headroom context compression for Codex, Claude Code, MCP, proxy, Python, and TypeScript workflows. |
| [`matsci-python-antipatterns`](common/matsci-python-antipatterns/) | Flags common README and repository mistakes in materials-science Python projects. |
| [`rigorous-pytest-suite`](common/rigorous-pytest-suite/) | Builds disciplined pytest suites, fixtures, tooling, and matching CI for Python projects. |

### ChatGPT Codex only

| Skill | Purpose |
| --- | --- |
| [`chatgpt-effort-advisor`](chatgpt/chatgpt-effort-advisor/) | Recommends a ChatGPT model and thinking level based on task complexity and cost. |

### Claude only

| Skill | Purpose |
| --- | --- |
| [`effort-advisor`](claude/effort-advisor/) | Recommends a Claude model and effort level based on the complexity of the current task. |

Each skill is self-contained. Its `SKILL.md` defines when it should run and how the assistant should apply it; supporting references, examples, scripts, and assets stay beside that file.

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

For example, ask ChatGPT Codex to “set up rigorous pytest coverage” to use `rigorous-pytest-suite`, or ask Claude to “check complexity” to use `effort-advisor`.

## Add or update a skill

1. Put cross-platform skills under `common/<skill-name>/`, ChatGPT Codex-only skills under `chatgpt/<skill-name>/`, and Claude-only skills under `claude/<skill-name>/`.
2. Keep `SKILL.md` at the root of the skill directory.
3. Store only resources referenced by that skill, such as `references/`, `assets/`, `scripts/`, or `examples.md`.
4. Update the contents table above when adding or removing a skill.
5. Review changes before committing so credentials, machine-specific paths, and generated files stay out of the repository.

## License

This is a private personal collection. No repository-wide license is declared. Individual skills retain any license metadata stated in their own `SKILL.md` files.
