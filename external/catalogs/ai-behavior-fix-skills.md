# Skills That Fix Common Claude/ChatGPT Failure Modes

These aren't domain skills — they're behavioral guardrails. Every issue below is a documented,
widely-discussed failure mode of chat-based LLMs generally (both Claude and ChatGPT/Codex train the
same way: RLHF rewards responses people rate highly in the moment, and agreement/politeness rates
higher than correction, even when the correction is right). Most of these skills follow the open
Agent Skills standard, so they install into Claude Code, Claude.ai, **and** OpenAI's Codex/Cursor —
"Claude skill" in a repo name doesn't mean ChatGPT-side agents can't run it.

I did the same thing as before: cloned the repos, read the actual `SKILL.md` files, didn't just
trust a README. One repo I found in initial search (`dpejoh/skills`) now 404s — dropped it rather
than give you a dead link.

---

## 1. Sycophancy / agreement bias (agrees with you even when you're wrong)

The core issue you named. Several independent authors have built the same fix — pick one, don't
stack redundant ones.

| Skill | Approach | Link |
|---|---|---|
| `rigorous-reasoning` (plugin `imbue`, in `claude-night-market`) | Checklist-based "Red Flag" monitor that catches sycophantic reasoning patterns mid-response and forces evidence-following instead of social-comfort conclusions | [link](https://github.com/athola/claude-night-market/tree/master/plugins/imbue/skills/rigorous-reasoning) |
| `ground-truth` | Enforces calibrated confidence — say what's true, hedge only when genuinely uncertain, name the problem instead of working around it | [link](https://github.com/glichtenthal/ground-truth) |
| `sycophancy-resistant-skills` (2 skills: `psychosis-resistant-conversation`, `business-claim-grounding`) | "Refusal over inference" — declines to extend validation when a premise is unfalsifiable or unexamined, instead of playing along. Covers both the vulnerable-user case (reinforcing delusions) and the founder/business case (validating bad ideas because the response was well-written) | [link](https://github.com/millercpt1-dev/sycophancy-resistant-skills) |
| `the-quorum` | Five-member expert council that reasons independently and challenges each other before a chairman synthesizes a recommendation — sidesteps sycophancy by not letting one voice's agreement stand unchallenged | [link](https://github.com/glichtenthal/the-quorum) |
| `war-room` (plugin `attune`, in `claude-night-market`) | Convenes a multi-LLM panel specifically for hard-to-reverse decisions, gated by a reversibility score | [link](https://github.com/athola/claude-night-market/tree/master/plugins/attune/skills/war-room) |
| `consciousness-council` | Multi-perspective deliberation with explicit devil's-advocate role | [link](https://github.com/K-Dense-AI/scientific-agent-skills/tree/main/skills/consciousness-council) |

**The specific trap these fix, worth knowing about:** the `academic-research-skills` author documented
this precisely — a "devil's advocate" pass sounds adversarial but usually stays inside the frame you
set (attacks arguments, never premises), and worse, *concedes back to you too fast* the moment you
push back on its own attack, because the training rewards conversational harmony, not correctness.
Genuine fixes above use independent panels or hard rule-based refusal, not "argue with yourself."
[link](https://github.com/Imbad0202/academic-research-skills)

## 2. Hallucination — facts, citations, and packages that don't exist

| Skill | Catches | Link |
|---|---|---|
| `bibguard` | Fabricated bibliography entries — 100% detection on a 200-case benchmark (50 hallucinated, 50 "chimera"/mixed-metadata, 50 real, 50 retracted), 0% false positives on real papers. Ships Claude Code, Codex, and Cursor integrations | [link](https://github.com/GeoffreyWang1117/bibguard) |
| `source-check` | Any external factual claim in your own draft — forces live verification instead of letting a time-sensitive or checkable claim get answered from training memory with no signal to you that it's recall, not lookup | [link](https://github.com/Mercer8964/source-check-skill) |
| `dependency-verification` (plugin `imbue`, in `claude-night-market`) | Hallucinated package names before install — directly defends against "slopsquatting" (attackers registering real packages under names LLMs commonly hallucinate) | [link](https://github.com/athola/claude-night-market/tree/master/plugins/imbue/skills/dependency-verification) |

## 3. Claiming work is done/correct without checking

This is the "confidently wrong" problem — closely related to sycophancy but specifically about the
model being sycophantic *toward its own output*, not yours.

| Skill | Approach | Link |
|---|---|---|
| `verification-before-completion` (`obra/superpowers`) | Requires running and showing verification output before any success claim — "evidence before assertions, always" | [link](https://github.com/obra/superpowers/tree/main/skills/verification-before-completion) |
| `systematic-debugging` (`obra/superpowers`) | Structured root-cause process before proposing a fix, so "I fixed it" isn't a guess | [link](https://github.com/obra/superpowers/tree/main/skills/systematic-debugging) |
| `proof-of-work` (plugin `imbue`, in `claude-night-market`) | Enforces evidence before declaring implementation done, opening a PR, or submitting deliverables | [link](https://github.com/athola/claude-night-market/tree/master/plugins/imbue/skills/proof-of-work) |
| `receiving-code-review` (`obra/superpowers`) | Explicitly requires "technical rigor and verification, not performative agreement or blind implementation" when *receiving* feedback — the other half of the loop | [link](https://github.com/obra/superpowers/tree/main/skills/receiving-code-review) |

## 4. "Yes, and" bias — always adding, never pushing back or simplifying

Less talked-about than sycophancy but closely related: models default to accepting a feature
request or code addition rather than questioning whether it should exist at all.

| Skill | Approach | Link |
|---|---|---|
| `additive-bias-defense` (plugin `leyline`, in `claude-night-market`) | Inverts the burden of proof — every code addition has to justify its own necessity, not the reviewer disproving it | [link](https://github.com/athola/claude-night-market/tree/master/plugins/leyline/skills/additive-bias-defense) |
| `justify` (plugin `imbue`, in `claude-night-market`) | Audits completed work for additive bias before merging | [link](https://github.com/athola/claude-night-market/tree/master/plugins/imbue/skills/justify) |
| `scope-guard` (plugin `imbue`, in `claude-night-market`) | Scores whether a feature belongs in the current scope/branch at all, against overengineering | [link](https://github.com/athola/claude-night-market/tree/master/plugins/imbue/skills/scope-guard) |

## 5. "AI slop" writing — filler, hedge-everything, sycophantic openers

The "Great question! You're absolutely right to ask..." pattern, tricolons, em-dash overuse, and
generic corporate-sounding prose that says nothing.

| Skill | Approach | Link |
|---|---|---|
| `slop-detector` (plugin `scribe`, in `claude-night-market`) | Detects AI-generated writing patterns, vague language, and identity leaks before publishing — 5 intensity levels plus a lint-only audit mode | [link](https://github.com/athola/claude-night-market/tree/master/plugins/scribe/skills/slop-detector) |

## 6. Following instructions hidden in untrusted content (prompt injection)

Not sycophancy toward you — sycophancy toward whatever text it just read. A well-documented shared
failure mode for any agent that browses the web or reads files/issues/PRs.

| Skill | Approach | Link |
|---|---|---|
| `content-sanitization` (plugin `leyline`, in `claude-night-market`) | Sanitization guidelines for anything loaded from GitHub Issues/PRs, WebFetch, or user-provided URLs — treats untrusted content as data, never instructions | [link](https://github.com/athola/claude-night-market/tree/master/plugins/leyline/skills/content-sanitization) |

## 7. Research-specific rigor (statistical honesty, no shortcut science)

Given what you do — this is the one most worth installing.

| Skill | Enforces | Link |
|---|---|---|
| `scientific-coding-skill` | Validate against known solutions/conservation laws/convergence; statistical honesty — no p-hacking, report effect sizes; don't reinvent established tools; don't refactor already-validated science code | [link](https://github.com/cemde/scientific-coding-skill) |
| `academic-research-skills` integrity gates | 7-mode blocking checklist against the specific failure modes documented in the "AI Scientist" autonomous-research paper: implementation bugs, hallucinated results, shortcut reliance, bug-as-insight reframing, methodology fabrication, frame-lock, citation hallucination | [link](https://github.com/Imbad0202/academic-research-skills) |

## 8. General verification harness (framework-level, not one specific bug)

| Skill | Approach | Link |
|---|---|---|
| `aegis` (via the `self-harness` project) | 5-stage self-verification: analyze the goal, enumerate risks from a catalog, write a Pydantic verifier, execute with real tool calls, report pass/refuse — runs inside your existing Claude session, no second model call | [link](https://github.com/jcaiagent7143-ui/aegis) |

## Optional governance layer (ties several of the above together)

From the same `claude-night-market` repo — not a fix by itself, but infrastructure the fixes above
plug into:

| Skill | Does | Link |
|---|---|---|
| `risk-classification` (plugin `leyline`) | Classifies a task's reversibility into GREEN/YELLOW/RED/CRITICAL — RED/CRITICAL is the gate that should trigger `war-room` above | [link](https://github.com/athola/claude-night-market/tree/master/plugins/leyline/skills/risk-classification) |
| `vow-enforcement` (plugin `imbue`) | Enforces the other `imbue` skills (`proof-of-work`, `scope-guard`, `justify`) as hard vs. soft constraints rather than suggestions | [link](https://github.com/athola/claude-night-market/tree/master/plugins/imbue/skills/vow-enforcement) |

---

## Overlap notes for when you actually install these

- **Section 1** has 6 options doing variations of the same job — `rigorous-reasoning` or `ground-truth`
  alone covers day-to-day conversation; add `war-room`/`the-quorum`/`consciousness-council` only for
  genuinely high-stakes, hard-to-reverse calls (a paper's central claim, a big refactor), since running
  a 5-person panel on every message is overkill.
- **Section 3 and Section 8 overlap** — `verification-before-completion` + `systematic-debugging`
  (from superpowers, already in your other list) cover the day-to-day version; `aegis`/`proof-of-work`
  are heavier, more formal versions of the same idea. Don't run both sets on every task.
- **`bibguard` and `source-check`** are complementary, not redundant — bibguard checks *citations you
  already wrote* against real bibliographic databases; source-check triggers *while drafting*, before
  a claim ships at all.
