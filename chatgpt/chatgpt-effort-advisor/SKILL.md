---
name: chatgpt-effort-advisor
description: Recommend a ChatGPT model and thinking level from task complexity, speed needs, and available account options. Use once before a distinct non-trivial ChatGPT task or when asked which model to use, to check complexity, recommend effort, right-size a request, or assess whether a setup is overkill. Gives advice without changing settings. Not an API or Codex model selector.
---

# ChatGPT Effort Advisor

Score the request, recommend a ChatGPT model and thinking level, then continue the requested work using the active session. Never change settings, purchase access, or claim that a recommendation changed the running model. If the user only asks for a recommendation, give that recommendation without executing the example task.

## When to run

- Run once per distinct non-trivial task, not on every follow-up. Score trivial requests only when explicitly asked.
- Skip acknowledgements, clarifications, and continuations unless scope changes materially. Respect a request to stop advising.
- Preserve the user's explicit model choice and speed/quality preference. Do not repeatedly propose an alternative they declined.
- If reliable session information shows the current setup fits, say: "Current setup fits — no change needed." Otherwise do not guess the current model or thinking level from your writing style, task performance, or identity.

## Score complexity: 0–10

Use the request and relevant context. Score each axis 0–2 and add the values. This is a routing heuristic, not a benchmark or predicted success rate.

| Axis | 0 | 1 | 2 |
|---|---|---|---|
| Reasoning | Mechanical transform or direct answer | Several connected steps | Difficult diagnosis, proof, or design |
| Scope | Small edit or short answer | One bounded deliverable | Many interacting parts or a long workflow |
| Ambiguity | Clear requirements | Some interpretation | Competing goals or substantial unknowns |
| Stakes | Exploratory, easy to discard | Used in practice, easy to correct | Material consequences or difficult reversal |
| Novelty | Familiar template | Original synthesis | Unfamiliar strategy or design |

Totals: **0–1 Trivial · 2–3 Low · 4–5 Medium · 6–7 High · 8–10 Very High**.

Favor the lighter option on a close call when mistakes are cheap to detect and correct. Do not round down known stakes. Task length alone does not establish reasoning difficulty.

## Turn the score into a recommendation

Read [reference.md](reference.md) for the dated ChatGPT model mapping and availability boundaries. Use [examples.md](examples.md) only when calibration is useful.

These are starting recommendations, not claims that higher settings guarantee better results:

| Tier | Starting choice | Escalation signal |
|---|---|---|
| Trivial / Low | Instant | The task reveals non-obvious dependencies or repeated reasoning errors |
| Medium | Medium | A concrete inconsistency survives a focused correction |
| High | High | The problem requires unusually deep reasoning or a previous attempt demonstrably failed |
| Very High | Extra High, where available | Consider an available Pro model for exceptionally demanding or long-running work |

For a difficult task on Free or Go, recommend Think when available. If the account lacks a proposed option, use its strongest suitable available choice; do not make upgrading a prerequisite to continuing.

Before finalizing, check the practical constraints:

- Recommend exact model names only when supported by the reference plus current documentation or the user's available options. If those are unknown, give the thinking-level recommendation conditionally without inventing access.
- If required tools, file handling, or modalities are unavailable with a candidate, choose a compatible option. More thinking does not supply missing tools, data, or permission.
- Resolve a missing critical input directly; do not present a higher model tier as the solution to missing facts. Consequential work still needs suitable verification.
- Increase one step when a specific failure warrants it. Do not automatically prescribe Pro for every high-stakes task or the highest setting for every long prompt.
- Distinguish faster responses, usage allowance, and monetary cost. Claim savings only when the user's actual billing rules support them.

## Output

Keep the advice to three short lines, with an optional fourth line when switching guidance helps:

```text
Complexity: {score}/10 — {tier}
Suggested: {verified ChatGPT model + thinking level, or conditional available option}
Why: {one task-specific reason or tradeoff}
To switch: choose the suggested option in ChatGPT's model/thinking controls.
```

Do not show a made-up current setting, environment variable, slash command, or API parameter. If current settings are unknown, omit them. If options cannot be verified, briefly say the recommendation depends on availability.

Proceed without waiting for the user to switch unless they explicitly asked to pause. A prompt asking for deeper thought is not evidence of a settings change.
