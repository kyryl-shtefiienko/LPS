---
name: skill-hierarchy
description: >-
  Resolves conflicts when two or more loaded skills (or a skill and general
  house-style guidance) give different instructions for the same action.
  Rule: the more specific skill wins, but only on the exact point of
  overlap -- the general skill still governs everything else it covers that
  the specific one doesn't address. Use whenever you notice two skills, or a
  general skill and a project/language-specific one, disagree about how to
  do something -- e.g. a general "how to write code" or style skill
  conflicts with a Python-specific, framework-specific, or project-scoped
  skill (such as dogusariturk-python-style in this repository); a general
  code-review skill conflicts with a language-specific linting/idiom skill;
  or two skills at the same specificity level genuinely disagree. Also use
  proactively before applying multiple loaded skills to the same file or
  task, not only after a contradiction is noticed.
---

# Skill Hierarchy

When multiple loaded skills bear on the same action and they disagree, don't
average them, don't silently pick your favorite, and don't apply both and
let the last one read win. Resolve it with one rule:

> **On the exact point where two skills conflict, the more specific skill
> wins. Everywhere else, both skills still apply as written.**

A specific skill doesn't replace a general one -- it overrides it locally.
If a general skill covers ten concerns and a specific skill disagrees on
one of them, follow the specific skill on that one and the general skill on
the other nine.

## Why specificity, not recency or verbosity

A general skill (a house style guide, "how to write clean code," a broad
code-review checklist) is written to hold up across every language and
context it might ever meet -- which means it's necessarily hedged and
generic. A specific skill (a Python idiom guide, a project's own testing
convention, a framework's documented gotcha) was written by someone who hit
the general rule's blind spot for that exact context and wrote down the
correction. The specific rule encodes more situational knowledge, not just a
stronger opinion, so it should win on its home turf. This repository already
applies the idea in `dogusariturk-python-style`, which states outright that
where it conflicts with an assistant's generic defaults, it is correct and
the generic default is wrong -- this skill generalizes that pattern to any
pair of loaded skills, not just that one.

## The specificity ladder

From most to least specific. When two conflicting skills sit on different
rungs, the lower rung number wins:

1. **The user's explicit instruction in the current conversation.** Always
   wins over any skill, full stop -- a skill is a standing default, a
   direct instruction is a live decision.
2. **Path/directory-scoped skill for the file or area actually in play**
   (e.g. a skill listed with a path prefix, or a project-local
   `.claude/skills/` entry). It was written for exactly this codebase.
3. **Skill that names the concrete language, framework, or library
   currently in use** (e.g. `dogusariturk-python-style` beats a generic
   "how to write good code" skill when the file being edited is `.py`).
4. **Skill scoped to the exact task/role in progress** (e.g. a code-review
   skill when the current action is a code review, over a skill that only
   mentions review in passing).
5. **General-purpose skill** with no named technology and no task
   scoping -- broadly correct, but the fallback, not the tiebreaker.

## Tie-breaks when two skills land on the same rung

Apply in order until one resolves it:

1. **Exactness** -- whichever skill's name/description names the *current*
   file's language or library more precisely (a NumPy-specific skill beats
   a general Python one when the code is NumPy-heavy).
2. **Scope origin** -- a project-level skill over a globally installed one;
   the project's own maintainers curated it for this codebase on purpose.
3. **Freshness/version** -- higher `metadata.version`, or a more recent
   `metadata.last_reviewed`, if both skills carry that field; weak evidence,
   but better than nothing.
4. **Still tied, or the conflict is substantive** (changes behavior, not
   just style) -- stop and ask the user rather than silently guessing.
   Silent resolution is fine for style nits; it is not fine for anything
   that changes what gets built or shipped.

## Applying it

1. Name the exact point of disagreement -- not "these two skills differ" but
   the specific instruction each one gives for the specific situation.
2. Rank the two (or more) skills on the ladder above.
3. Follow the winner **on that point only**. Re-check whether the loser's
   other guidance still applies elsewhere in the same task -- it usually
   does.
4. If the resolution is non-obvious or consequential, say one short
   sentence noting which skill you followed and why. Don't narrate trivial
   or expected resolutions -- that's noise.

### Worked example

A general engineering-practices skill says "prefer explicit type
annotations on every function." `dogusariturk-python-style` says "avoid
annotating obvious return types self-inferred by mypy in local helpers."
Both are loaded while editing a `.py` file.

- Point of conflict: annotating obvious-return-type local helpers.
- Ladder: the style skill names the language (Python) and is more specific
  than the general practices skill -- rung 3 vs. rung 5. It wins.
- Apply: skip annotations on obvious local helpers as the style skill says.
  Elsewhere -- annotating public APIs, module boundaries -- the general
  skill's "prefer explicit annotations" is untouched, since the style skill
  never addressed that case.

## Optional: the ranking helper

For a quick sanity check rather than eyeballing the ladder, run:

```bash
python scripts/rank_specificity.py --skills general-skill-name specific-skill-name
```

It reads each skill's `SKILL.md` frontmatter under `~/.claude/skills` (pass
`--roots` for other locations such as an LPS checkout's `common/` or
`claude/`, or `--pairs "name::description"` to skip the lookup) and prints a
ranked table with the reason for each rung, plus which one wins on overlap.
It's a heuristic tie-breaker, not an authority -- use your own reading of
both SKILL.md files as the real source of truth, especially for tie-break
steps 3-4 above, which the script only partially implements (it does not
stop to ask the user).

## Relationship to skill-benchmark

`skill-benchmark` flags pairs of skills with high description overlap as a
*static hygiene* signal (they may be redundant and worth merging). This
skill is for the different case where two skills overlap *on purpose* --
one general, one a deliberate specialization -- and both should stay
loaded. Don't merge skills just because this skill resolved a conflict
between them; merging is only right when the overlap is redundancy, not
intentional specialization.
