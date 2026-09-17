---
name: adhd-mode
description: Fans out several isolated "cognitive-frame" brainstorms on an open-ended problem before switching into a separate critic pass that scores, clusters, flags traps, and deepens only the strongest few — instead of settling for the first plausible answer. Trigger this whenever the user asks to brainstorm, ideate, explore options, says "give me a few ways to...", or explicitly asks for "ADHD mode" / "/adhd" / "divergent mode". Also reach for it proactively on open-ended architecture, API/schema, and naming decisions, product positioning, and fuzzy bugs with no known root cause — anywhere a thoughtful practitioner would say "let me think about this differently for a second." Skip it for lookups, syntax questions, bugs with a known cause, or anywhere the user's phrasing signals they want the quick/standard/canonical answer.
license: MIT
---

# ADHD Mode: Parallel Divergent Ideation

## The problem this solves

Ask a model an open-ended question — "give me a few ways to design this," "what should we name this," "why might this be failing intermittently" — and it will reliably hand back the same three answers a competent professional would produce off the top of their head. That isn't really a flaw: those *are* the highest-probability completions. But it's the wrong output whenever the entire point of asking was to get past the obvious answer. Call this **premature convergence**: the model evaluates as it generates, early tokens anchor later ones, and the result is the centroid of the training distribution dressed up as a recommendation.

This skill breaks that pattern with a mechanical separation a single pass of prompting can't achieve on its own: generate several genuinely different takes with evaluation switched off, and only *afterward* switch into a critical mode that scores, prunes, clusters, and sharpens what came out. Chain-of-thought makes one line of reasoning go slower. Tree-of-thought makes one line of reasoning search wider. This makes several differently-angled lines of reasoning run in parallel, then hands the results to a critic.

## Gate: use this on purpose, not by default

This costs real length, and when true parallel branches are available, real time and extra model calls — roughly 5–10× a normal answer. Don't pay that cost by default.

**If the user explicitly invoked it** — "/adhd", "ADHD mode", "run divergent mode on this," "give me the wide version" — skip the rest of this section and go straight to Phase 1. They opted in; don't second-guess it.

**Otherwise, self-check before running it.** All three must hold:

1. **Open-ended.** Would a thoughtful practitioner reasonably give several genuinely *different* good answers here, or is there one canonical answer? If canonical, don't run this.
2. **Worth the cost.** Is the price of settling for the obvious-but-wrong answer actually high — an architecture call, a public API shape, a real product name, a bug with no known cause? If it's a low-stakes or throwaway question, don't run this.
3. **Open phrasing.** Did the user's wording avoid "quick," "just," "standard," "one-line," "the usual way"? Those words are a request for the direct answer. If present, don't run this.

If any check fails: answer directly, and optionally close with one line offering the wider pass — *"Want me to run this in ADHD mode for a wider set of options?"*

## Two phases, never mixed

The failure mode this skill exists to prevent is the critic strangling the generator — evaluating ideas as they're produced instead of after. Keep the phases mechanically separate: while diverging, forbid yourself (or any sub-agent) from ranking, hedging, or judging; while converging, forbid yourself from generating anything new that wasn't already on the table.

### Check what isolation you actually have

Real isolation — a branch that cannot see what any other branch produced — is the load-bearing part of this technique. What that looks like depends on where this skill is running:

- **Subagent tool available** (e.g. Claude Code's Task tool, or another agent-dispatch tool present in this session): use it. Dispatch one call per frame with fresh, separate context and no shared history between them. This is the version that's actually been evaluated against a baseline.
- **No subagent tool** (a plain chat session — this environment, most of the time): approximate it by discipline instead of architecture. Write each frame's ideas as one uninterrupted burst immediately after choosing the frame, without rereading or echoing what an earlier frame produced. Only allow yourself to look across all frames at once when you deliberately step into Phase 2. Say plainly that this is a best-effort approximation, not true isolation — and if the user has (or could use) a subagent tool, or the stakes justify it, point them at the companion tooling below instead.

### Phase 1 — Diverge

1. Pick 4–6 cognitive frames from the library below (or improvise a fitting one on the spot). Bias toward frames tagged for the problem's domain, and always keep at least one `wild` frame in the mix — that's usually where the actual surprise comes from.
2. For each frame, produce a short burst of distinct one-line ideas under an instruction like this (adapt it for a subagent call or for yourself):

   > You are generating, not judging. Given the problem and this vantage point, produce 5–6 short, distinct ideas — one line each. No ranking, no hedging, no "it depends." The first two or three answers anyone would give are off-limits; push past them. Output the ideas only, nothing else.

3. Do not let a later frame reference an earlier frame's ideas. If you notice yourself echoing a previous frame's angle, that frame collapsed into convergence — note it and move on rather than forcing distinctness that isn't there.

### Phase 2 — Focus

Once every frame has produced its ideas, deliberately shift modes — say so explicitly ("Switching to critic mode") so the change of posture is real, not cosmetic.

1. **Score.** Rate every surviving idea 0–10 on three axes: *novelty* (distance from the obvious default), *viability* (could this actually be built, shipped, or said), and *fit* (does it solve the actual stated problem). Flag any idea that looks appealing but has a hidden cost, a false economy, or a scaling problem as a **trap**, with a one-line reason.
2. **Cluster.** Group the surviving ideas into 3–6 clusters by underlying *angle*, not surface wording — "remove the middleman" ideas versus "batch and delay" ideas versus "make the user choose" ideas, for instance. This is what turns a pile into a map.
3. **Deepen.** Take the top 2–4 by weighted score (novelty and fit matter more than raw viability at this stage), excluding traps, and expand each into: a short sketch of how it would actually work, its single biggest load-bearing risk, the first concrete step someone would take, and 3–5 child ideas (variations, hybrids, or things it unlocks).

## Frame library

Pick 4–6 per run; keep at least one `wild`. Improvise new frames freely — this list is a starting point, not a ceiling.

| Frame | Vantage point | Tags |
|---|---|---|
| **Triage medic** | Assume limited time and resources. What's the version that stabilizes the worst case first and can improve later? | general, design |
| **Auditor / regulator** | What here needs to be provable, traceable, or reversible after the fact? Design for the audit, not just the happy path. | design, general |
| **Speedrunner** | Look for the shortcut, skip, or edge case that "isn't really cheating" but gets there faster. | code, wild |
| **Field biologist** | Borrow a mechanism from a living system — immune response, symbiosis, signaling, migration — and force-fit it onto this problem. | code, wild |
| **Logistics planner** | Reframe as a supply-chain problem: queues, batching, hubs, last-mile delivery, returns. | code, design |
| **Game designer** | What are the loops, rewards, friction points, and save states here? Treat the user as a player. | design, general |
| **Market maker** | Reframe as a market: buyers, sellers, an auction, a pricing signal. What clears it? | design, wild |
| **Inversion** | Ask the opposite question — how would you guarantee failure here? — then negate each answer back into a real idea. | code, design, general |
| **Zero-budget hour** | No money, no team, sixty minutes. What's the crudest version that still does the one thing that matters? | code, general |
| **Blank-check decade** | Unlimited budget, unlimited people, ten years. What's the maximalist version, and does any piece of it scale down? | design, wild |
| **Remove the foundation** | Name the thing everyone treats as fixed here (the framework, the database, the org chart) and imagine it's gone. | code, design, wild |
| **Adversary** | You're actively trying to break, exploit, or embarrass the obvious solution. What does that reveal? | code, design |
| **Swarm** | No central planner — many simple agents following local rules. How does this resolve itself emergently? | code, wild |
| **Curious newcomer** | You've never seen this field's conventions. Describe the naive approach nobody "does" because it seems too simple. | general, wild |
| **3am on-call** | You're the person who gets paged when this breaks. What would let you sleep through the night instead? | code, design |

For code-shaped problems, lean on frames tagged `code`/`design` plus one `wild`. For open strategy, naming, or product questions, mix across all tags.

## Output shape

Render Phase 2's output in this order — don't collapse it into undifferentiated prose; the structure is most of the value:

1. **Brief** — one or two lines confirming the problem and any reframing used.
2. **Wide set** — the surviving ideas, grouped by cluster and labeled by angle. One line per idea, with its score in brackets, e.g. `[N8 V6 F9]`.
3. **Shortlist** — the 2–4 deepened picks. Mark the best non-obvious-but-viable one with ★. List traps separately with their one-line reasons.
4. **Deepened picks** — for each shortlisted idea: the sketch, the risk, the first step, and its child ideas.
5. **One provocation** — a single leftover wildcard question or idea, offered as a door the user can open if nothing above landed.

## Anti-patterns

- **Convergence dressed as divergence.** Ten polite variations on one idea is not a wide set. If every candidate shares the same underlying assumption, nothing actually diverged.
- **Weirdness with no convergence.** Thirty unsorted oddities is exactly as useless as one safe answer. Always finish by clustering and picking.
- **A wall of equally-weighted prose.** If every idea gets the same three sentences, nothing was prioritized. Structure and scoring are the point.
- **Refusing to take a position.** "Here are twenty options, you decide" is an abdication. Diverge wide, then converge with an actual opinion about what's promising.
- **Faking isolation.** Writing five "frames" back-to-back in one breath, each obviously riffing on the last, is a wider single thought — not this technique. If real separation isn't available, at least notice when it's leaking and say so.

## Calibration

- **Scale to stakes.** A quick naming question: 3 frames × 4 ideas. A real positioning or architecture call: 5–6 frames × 6–8 ideas. Default: 5 frames × 6 ideas.
- **Read the room on tone.** For serious strategy work, label the wild ideas clearly so they don't read as unserious. For open brainstorming, let them run looser — absurd ideas earn their place by seeding viable ones.
- **Stop diverging when ideas start repeating each other's shape**, not when you hit a target count. Padding to a number is convergence wearing a divergence costume.

## Companion tooling

For genuinely isolated, truly parallel runs outside a single conversation — real separate model calls rather than the single-thread approximation above — there's an existing open-source implementation of this loop built on the Claude Agent SDK: `adhd-agent` on npm (`npx skills add UditAkhourii/adhd`, or `npm install -g adhd-agent` for the CLI). It's a good option when running this outside Claude Code, in batch, or when the stakes genuinely justify the full ~10-call cost with true isolation.

## Prior art and scope

This skill adapts the publicly published preprint *ADHD: Parallel Divergent Ideation for Coding Agents* (Udit Akhouri Raj, MIT-licensed, 2026), which reported wins over a single-shot baseline on novelty, breadth, and trap detection across six open-ended engineering problems judged by an independent LLM. It's a separate technique from another "ADHD"-branded tool circulating in the same community, `i-have-adhd`, which is about *output style* — short, direct, numbered, low-verbosity responses — rather than idea breadth; if what's actually wanted is terser output rather than wider ideation, that's a different problem and this isn't the skill for it. The "ADHD" name itself is borrowed rather than clinical: it nods to research linking ADHD-associated cognitive traits to enhanced divergent thinking, not to any diagnostic claim about the model or the user.
