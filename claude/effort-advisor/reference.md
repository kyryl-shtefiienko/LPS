# Effort Advisor — Model Reference

Detail for `SKILL.md`'s recommendation table. Not loaded on every run — only open this when the tier table isn't enough, e.g. the user asks "why" or a suggested model/level turns out not to be offered.

## Current Claude models (check docs.claude.com for changes)

| Model | Model ID | Tier | Effort control | Notes |
|---|---|---|---|---|
| Claude Haiku 4.5 | `claude-haiku-4-5-20251001` | Fast / cheap | Extended thinking on/off, with manual `budget_tokens` — not the low/medium/high/xhigh/max ladder | Default choice for mechanical, high-volume, or latency-sensitive work |
| Claude Sonnet 5 | `claude-sonnet-5` | Mid, flagship-capable | Full adaptive ladder: low, medium, high (default), xhigh, max | Medium is roughly comparable in intelligence to a prior-generation Sonnet at high |
| Claude Opus 5 | `claude-opus-5` | Flagship | Full adaptive ladder: low, medium, high (default), xhigh, max | Best default for the hardest coding, agentic, and reasoning-heavy work |
| Claude Fable 5.1 | `claude-fable-5-1` | Above Opus | Full adaptive ladder; also supports changing effort mid-conversation without losing prompt cache | Built for the longest-horizon, most demanding multi-step agentic work; highest per-token cost |
| Claude Mythos 5.1 | — | Above Opus | — | Not generally available — Project Glasswing partner access only. Don't recommend it to a general user |

Anthropic ships new models and revises effort support fairly often. If anything above conflicts with what `/model` or the claude.ai picker actually shows, trust the picker and mention the discrepancy briefly rather than insisting on this table.

## Switching, by surface

**Claude Code**
- `/model` — opens the interactive model picker
- `/model <name>` — switches directly
- `/effort` — opens the interactive effort slider (Enter saves it as your default; `s` applies it to this session only)
- `/effort <level>` — sets directly: `low`, `medium`, `high`, `xhigh`, `max`
- `/effort auto` — resets to the model's own default

**claude.ai and the Claude apps**
Use the model + effort control in the chat composer. Each model lists its recommended ("Default") effort level there; there's no slash command.

**API / Agent SDK**
Set `model` and `effort` directly on the request. On models that use the adaptive-effort ladder (Sonnet 5, Opus 5, Fable 5.1), also setting `thinking.budget_tokens` returns an error — `effort` replaces it. Haiku 4.5 still uses the older manual `thinking.budget_tokens` mechanism, since it predates the `effort` parameter.

## Cost mental model

- Dropping one **model** tier (e.g. Opus 5 → Sonnet 5) usually saves more than dropping one **effort** level on the same model.
- Dropping one effort level on the same model cuts thinking-token volume; it doesn't change the per-token price.
- A cheaper model at a higher effort sometimes matches a pricier model at low effort for less total cost — on a borderline call, it's often worth trying "smaller model, higher effort" before reaching for the bigger model.
- `xhigh` and `max` can use several times the tokens of `low`/`medium` on the same task. Reserve them for work that has already fallen short at `high`, not as a default starting point.
