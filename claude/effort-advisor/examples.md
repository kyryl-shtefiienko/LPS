# Effort Advisor — Worked Examples

Anchors for calibrating the rubric in `SKILL.md`, not hard rules. Adjust for context a bare one-line description doesn't capture — e.g. a "simple" rename across 40 files with inconsistent naming conventions is Scope 2, not 0.

| Request | Reasoning | Scope | Ambiguity | Stakes | Novelty | Total | Tier | Recommendation |
|---|---|---|---|---|---|---|---|---|
| "Rename this variable across the file" | 0 | 0 | 0 | 0 | 0 | 0 | Trivial | Haiku 4.5, thinking off |
| "Fix this typo in the README" | 0 | 0 | 0 | 0 | 0 | 0 | Trivial | Haiku 4.5, thinking off |
| "Write a docstring for this function" | 0 | 0 | 1 | 0 | 0 | 1 | Trivial | Haiku 4.5, thinking off |
| "Summarize this changelog in three bullets" | 0 | 0 | 0 | 0 | 0 | 0 | Trivial | Haiku 4.5, thinking off |
| "Add a loading spinner to this button component" | 1 | 1 | 0 | 0 | 0 | 2 | Low | Haiku 4.5 or Sonnet 5, low |
| "Translate this paragraph into Spanish" | 0 | 0 | 1 | 0 | 0 | 1 | Trivial | Haiku 4.5, thinking off |
| "Debug why this test fails intermittently" | 1 | 1 | 1 | 1 | 0 | 4 | Medium | Sonnet 5, medium |
| "Write unit tests for this module" | 1 | 1 | 1 | 0 | 0 | 3 | Low | Sonnet 5, low–medium |
| "Refactor this module to remove the singleton pattern" | 1 | 2 | 1 | 1 | 1 | 6 | High | Sonnet 5, high |
| "Write a persuasive essay for a novel policy position" | 1 | 1 | 2 | 1 | 2 | 7 | High | Sonnet 5, high |
| "Investigate this production outage and propose a fix" | 2 | 1 | 2 | 2 | 1 | 8 | Very High | Opus 5, xhigh |
| "Design the auth flow for a new multi-tenant SaaS product" | 2 | 2 | 2 | 2 | 2 | 10 | Very High | Opus 5 or Fable 5.1, xhigh/max |
| "Plan and execute a multi-week migration across 200 files" | 2 | 2 | 2 | 2 | 1 | 9 | Very High | Fable 5.1, xhigh |

A rough sanity check once you've scored: if you'd feel comfortable letting an intern with no context handle it from a checklist, it's Trivial or Low. If a senior engineer would want to think before touching it, it's High or Very High.
