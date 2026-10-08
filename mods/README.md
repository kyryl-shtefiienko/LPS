# Claude Code mods

Mods I use in Claude Code, with my edited versions where I changed something. Install any of them with `/plugin marketplace add <repo>` then `/plugin install <name>@<marketplace>`, then `/reload-plugins`.

## Edited versions (in this folder)

| Mod | What I changed |
| --- | --- |
| [`prismantis`](prismantis/) (full plugin copy, see [`MODIFICATIONS.md`](prismantis/MODIFICATIONS.md)) | Adds a `▣ png` button on tables and diagrams that saves a PNG and copies the image to the clipboard (not in upstream). |
| [`flightdeck`](flightdeck/) (full plugin copy, see [`MODIFICATIONS.md`](flightdeck/MODIFICATIONS.md)) | Config only: permission gate panel removed. |

## Other mods (links only)

From [hamzafer/claude-code-mods](https://github.com/hamzafer/claude-code-mods) (marketplace `claude-code-mods`):

| Mod | Purpose |
| --- | --- |
| [`where-am-i`](https://github.com/hamzafer/claude-code-mods/tree/main/mods/where-am-i) | Live recap above the prompt: goal, doing now, waiting on you, next. `/where` for a longer one. |
| [`next-steps`](https://github.com/hamzafer/claude-code-mods/tree/main/mods/next-steps) | Suggests 2 or 3 likely next prompts after each turn. |
| [`agent-radar`](https://github.com/hamzafer/claude-code-mods/tree/main/mods/agent-radar) | One live line per running subagent. `/radar` shows all agents. |
| [`review-watch`](https://github.com/hamzafer/claude-code-mods/tree/main/mods/review-watch) | Live line per running code review, with a toast of findings at the end. |
| [`md-preview`](https://github.com/hamzafer/claude-code-mods/tree/main/mods/md-preview) | Renders Markdown files Claude edits next to the chat. `/md` opens it. |
| [`blast-radius`](https://github.com/hamzafer/claude-code-mods/tree/main/mods/blast-radius) | Holds risky Bash commands and shows what they would change first. |

Other plugins:

| Plugin | Repo |
| --- | --- |
| token-optimizer | [alexgreensh/token-optimizer](https://github.com/alexgreensh/token-optimizer) |
| human-in-the-loop | [tzafrir/human-in-the-loop](https://github.com/tzafrir/human-in-the-loop) |

Removed: `token-weather`, `mission-control`, `replay-theater`.
