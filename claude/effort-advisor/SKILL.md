---
name: effort-advisor
description: Scores how complex the current request actually is, then prints a one-line Claude model + effort recommendation (Haiku 4.5 / Sonnet 5 / Opus 5 / Fable 5.1, at low/medium/high/xhigh/max) so the user can switch manually and avoid overpaying in tokens. Use before starting any non-trivial task — coding, debugging, writing, analysis, research — especially when the session might be running a bigger model or higher effort than the task needs. Trigger phrases — "check complexity", "am I overpaying", "which model should I use", "recommend effort", "right-size this", "cost check", "is this overkill".
---

# Effort Advisor

Score the request, state the tier, recommend a model + effort pair, then do the work as normal at whatever the session is currently running. **Never switch the model or effort yourself — only the user can.** This skill only prints a recommendation; it deliberately carries no `model` or `effort` frontmatter override, so it stays useful outside Claude Code too (claude.ai, the Skills API).

## When to run this

- Once per new, distinct task — not on every back-and-forth reply within the same task.
- Skip it for replies that just continue work already scoped in this conversation, clarifying questions, or short acknowledgements.
- Skip it entirely if the user has said to stop checking this session.
- If the current setup already roughly matches the recommendation, say so in one line instead of the full block ("Current setup already fits — no change needed."). Don't manufacture a mismatch just to justify having run.

## Score the request (0–10)

Rate each axis 0–2 from the request as given, then add them up.

| Axis | 0 | 1 | 2 |
|---|---|---|---|
| Reasoning depth | lookup / mechanical transform | some multi-step logic | deep multi-step reasoning, proof, or design |
| Scope | one small edit / short answer | one function, section, or page | multi-file, system-wide, or long-form |
| Ambiguity | fully specified | some interpretation needed | open-ended, needs exploring options |
| Stakes | low-stakes draft / exploratory | will be used, easy to fix if wrong | production, security, irreversible, money/legal/health-adjacent |
| Novelty | formulaic / templated | some original synthesis | genuinely novel strategy or design |

**Total → Tier:** 0–1 Trivial · 2–3 Low · 4–5 Medium · 6–7 High · 8–10 Very High

If you're unsure between two adjacent scores on an axis, round down — the bias section below explains why.

## Tier → recommendation

| Tier | Model | Effort | Why |
|---|---|---|---|
| Trivial | Haiku 4.5 | thinking off | rote task, no reasoning needed — cheapest and fastest option |
| Low | Haiku 4.5, or Sonnet 5 | low | scoped and latency-sensitive, not intelligence-sensitive |
| Medium | Sonnet 5 | medium | cost-sensitive default; roughly matches a prior-generation model at high effort |
| High | Sonnet 5 | high (xhigh if it's a hard coding/agentic task) | quality matters more than cost here |
| Very High | Opus 5, or Fable 5.1 for the longest-horizon work | xhigh or max | architecture-level, highest-stakes, or long-horizon agentic work |

For exact per-model effort support, current model IDs, and switch commands by surface, see `reference.md`. Model line-ups and effort support change between releases — if a level or model this table names isn't actually offered, defer to what `/model` (or the claude.ai model picker) shows and say so.

## Output format

Print this block before starting the task, then proceed with the work at whatever the session is currently running:

```
📊 Complexity: {score}/10 → {Tier}
→ Suggested: {Model}, effort {level}  (session effort right now: ${CLAUDE_EFFORT})
→ Why: {one clause}
→ To switch: /model, then /effort {level}   [claude.ai: use the model/effort picker instead]
```

Keep it to those three or four lines — the check itself should cost near-zero tokens, or it defeats its own purpose.

## Bias: default toward cheaper

When a task could plausibly go either way, recommend the cheaper option and name the risk in the "Why" line, e.g. "Sonnet 5 at medium — bump to high if it under-thinks the edge cases." A slightly-too-low effort that occasionally needs a follow-up is usually still cheaper than defaulting high on everything. See `reference.md` for the fuller cost mental model (model tier vs. effort level, and when a cheaper model at higher effort beats a pricier model at low effort).

For calibration on how requests map to scores, see `examples.md`.
