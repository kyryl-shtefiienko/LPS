---
name: context-compactor
description: >-
  Keep large or repeated tool output from flooding context by archiving the
  full result to a file (a "handle") and bringing only a compact excerpt
  into the conversation, with exact paged recall from the handle whenever
  the real content is needed later. Also folds handles into checkpoints
  instead of re-pasting raw output, and fuses an edit with its narrow
  follow-up validation into one turn. Use when a tool call is about to
  return (or just returned) a big or repeated result — a verbose build/test
  log, a broad grep, a large file read, background command output; when the
  same large content would otherwise be re-fetched or re-pasted; when
  writing a checkpoint for a task that produced long tool output; or when
  the user asks to "truncate", "compact", "not paste the whole thing", or
  reduce token/context usage from tool output specifically (as opposed to
  conversation-level checkpointing, which the `checkpoint` skill already
  covers).
---

# Context Compactor

## Where this comes from

Adapted from [NVlabs/SoL-Pi](https://github.com/NVlabs/SoL-Pi), a set of context-efficiency mechanisms built for a different coding agent ("Pi") that has a hook API letting an extension rewrite tool results before they enter context. Claude Code has no equivalent hook for that — nothing outside the model can quietly shrink a tool result after the fact. So this skill reproduces the useful *behaviors* (ObservationPack, Online Context Compact, Action Fusion) as things Claude does on purpose, going forward, rather than as infrastructure sitting underneath it. It cannot shrink something already sitting in context; it only prevents the next large result from bloating context in the same way.

This composes with two skills already in place, rather than replacing them:
- **`checkpoint`** — owns cross-session resumability. This skill feeds it handles instead of raw output.
- **`headroom`** — an actual external compression process, when installed and running. This skill is the manual fallback for when it isn't.

## Mechanism 1 — ObservationPack (handle + paged recall)

**Trigger:** before or right after a tool call that is likely to return a large or repeated result — a verbose build/test log, a broad grep/search, reading a large file, a background command, an API response with a big body. Rule of thumb: if it would run past roughly 150-200 lines, or it's the same content being fetched a second time, it qualifies. Don't bother for small, one-off output — the archiving overhead isn't worth it there.

**What to do:**
1. Get the full result onto disk as a stable, findable file — the "handle." In practice this is usually already true for free (`Bash` with `run_in_background` writes stdout to a task output file; redirecting a verbose command to a file in the scratchpad directory works for anything else). Give it a name that says what it is, not a random temp name.
2. Bring only a compact excerpt into the conversation: a head/tail sample, a match count, the handful of lines that actually matter to the decision at hand. State the handle's path and its total size (lines or bytes) alongside the excerpt, e.g. "full output: `scratchpad/build-2026-09-29.log`, 4,812 lines, 3 errors shown below."
3. Before reusing that content later, check whether a handle for it already exists rather than re-running the tool or re-reading the whole file again.
4. When exact content is needed again — a specific error string, an exact value, a quote — re-open the handle with `Read`'s `offset`/`limit` (or a targeted `Grep` on the archived file) and read only the slice needed. Never reconstruct an exact quote from memory of your own earlier summary; re-read the archive. This is the one non-negotiable rule — it's what keeps a compacted summary honest instead of a paraphrase pretending to be a fact.

**Don't:**
- Archive-and-summarize trivial output — a 10-line command result belongs in context directly.
- Let handles pile up unlabeled — an untraceable pile of scratch files defeats the purpose as surely as no archiving at all.
- Quote "from memory" once the original excerpt has scrolled out of view — re-read the handle instead.

## Mechanism 2 — Online Context Compact (handles inside checkpoints)

**Trigger:** any of the `checkpoint` skill's own triggers (long conversation, a system note about length, the user mentioning low tokens/limits/switching models, finishing a task phase) — specifically for steps whose evidence is large tool output.

**What to do:** when a step is done and you're recording it (in a checkpoint file, or just in your own running account of progress), record the *handle* for its evidence, not the raw content — "step 3: build passed, 2 warnings → full log at `scratchpad/build-step3.log`" rather than pasting the log. Once that's written down, it's safe to let the raw output drop from active attention: the checkpoint's compact record plus the handle is what has to survive, not the live transcript. If context does get auto-summarized or the session restarts from a checkpoint, the handle still resolves to the exact original — nothing is actually lost, only deferred.

This is pure addition to how `checkpoint` already works — don't duplicate its format or triggers, just make sure any step involving a handle carries that handle forward into the checkpoint instead of a raw dump or a lossy paraphrase.

## Mechanism 3 — Action Fusion (turn reduction)

**Trigger:** an edit or write that has an obvious, narrow, cheap follow-up check — a lint pass, a type-check, the one test file that covers the change, a build of just the touched module.

**What to do:** issue the edit and its narrow validation together rather than across two round-trips — as parallel tool calls in the same message when they're independent, or immediately in sequence when the check depends on the edit having landed. Keep the validation scoped to what the edit actually touched.

**Don't fuse in anything slow or broad** — a full test suite, a full rebuild, a long-running integration check. Fusing those back in just re-creates the token/turn cost this whole skill exists to avoid; run those separately, and if their output is large, that's exactly what Mechanism 1 is for.

## The one rule that matters most

Evidence over paraphrase: whatever gets summarized, truncated, or excerpted, the full original stays retrievable at a known path, and any claim made from memory of a summary gets re-verified against that path before being treated as fact. That's the difference between compacting context and quietly guessing.
