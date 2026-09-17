---
name: checkpoint
description: >-
  Keep long, multi-step tasks resumable across a new Claude conversation or a
  different Claude model via one lean checkpoint file: goal, key decisions
  made, completed work with its actual results (not just checkmarks), files
  produced, and what is left. A fresh session resumes for a fraction of the
  tokens re-explaining everything would cost. Use proactively, unprompted,
  for long or multi-phase tasks: multi-file coding, long research, iterative
  writing, large data work, or anything with more than a handful of steps.
  Checkpoint before a big chunk of remaining work starts, when the
  conversation has grown long, when a system note about conversation length
  appears, or when the user mentions running low on usage, tokens, or
  credits, hitting a limit, switching models, or worrying about losing
  progress. Also use this when the user uploads or references a checkpoint
  file, or says resume, continue where I left off, or pick up from my last
  chat: read it fully first, then continue from it instead of starting
  over.
---

# Checkpoint & Resume

## Why this exists

Every Claude conversation runs inside a session that eventually ends — a usage limit gets hit, the conversation gets very long, or the user simply wants to switch to a different Claude model partway through. Without preparation, the next session has two bad options: re-read the entire prior transcript (expensive, slow, and often impossible since a fresh conversation doesn't have it), or have the user re-explain everything from memory (lossy and tedious). Both waste the exact things that were in short supply: tokens and time.

The fix is a small, purpose-built file — a checkpoint — that carries forward only what actually matters: the goal, the decisions already locked in, the real results produced so far, and precisely what's left to do. A new session, same model or a different one, reads a few hundred words instead of tens of thousands, and picks up exactly where things stopped.

## When to use this

Use this on any task with enough scope that losing the session would genuinely hurt: multi-file coding projects, long research or analysis, iterative writing with several rounds, large document or data processing, or anything with more than a handful of distinct steps. Don't bother for a quick question or a single small edit — the overhead isn't worth it there.

Checkpoint proactively, without waiting to be asked, when:

- You're about to start a big, expensive chunk of remaining work (a long generation, a big batch of file edits, a long tool-call sequence). Checkpoint *before* it starts, not just after — that's the point where an interruption would cost the most.
- The conversation has grown very long, or you receive a system note indicating the conversation is getting long. Treat that as a cue to wrap up a checkpoint soon rather than pushing further.
- The user says anything like "I'm running low on tokens/credits/usage," "I might hit my limit," "I want to switch models," or "I don't want to lose this." Take these at face value and checkpoint immediately — you have no way to see the user's actual usage limits or remaining context budget, so their word is the most reliable signal you'll get.
- You just finished a natural phase of work (a milestone, not every tiny step).

Also use this in the other direction: when the user uploads or references a checkpoint file, or says something like "resume," "continue where I left off," or "pick up from my last chat" — read it in full before doing anything else, and continue from it rather than restarting the task or re-asking questions it already answers.

## Being honest about "token-aware"

You cannot directly measure how many tokens are left in the conversation's context, or in the user's plan — there's no meter to read. "Token-aware" here means using the observable signals above (task shape, conversation length, explicit system notes, and what the user tells you) to checkpoint *before* you'd need the safety net, rather than trying to predict a hard cutoff precisely. When in doubt, checkpoint a little earlier than feels necessary — a checkpoint that turns out to be premature costs a minute; one that never gets written can cost the whole session.

## What goes in a checkpoint

One file, written for a stranger — a fresh Claude, possibly a different model, with none of this conversation's context — to pick up cold. Use this shape, adapting section names to the task:

```markdown
# Checkpoint — <short task name>
_Saved <date>, mid-task · <one-line status, e.g. "step 3 of 5 done">_

## Goal
<1-3 sentences: what the user is trying to accomplish, end to end>

## Decisions already made (don't re-litigate these)
- <a choice the user made or you settled on, and why, if it's not obvious>
- <specific values, names, formats, style choices that were pinned down>

## Done so far
- <step> → <the actual result: a value, a finding, a summary of what was produced — not just "completed">
- <step> → <result, or "full output in path/to/file.ext" for anything long>

## Files produced
- `path/to/file.ext` — what it is, and whether it's finished or a draft

## In progress when this was saved
<exactly what you were doing, how far it got, and any partial output — inline if short, or saved to a file if long>

## Remaining steps
- [ ] <next step>
- [ ] <step after that>

## Resume instructions
Read this whole file first. Everything in "Done so far" is finished — don't redo it or re-ask about the decisions above. Continue with the first unchecked item in "Remaining steps." Re-read a file from "Files produced" only if the next step actually needs its contents.
```

Drop sections that don't apply — a research task might not produce files; a coding task will lean heavily on that section.

## How to write a good checkpoint

- **Record results, not just status.** "Step 2 done" tells a new session nothing useful; "step 2 done — the API returns paginated results, 50/page, and the rate limit is 10 req/s" means it never has to rediscover that. The whole point is to save the *expensive* part: things that took searching, computing, or back-and-forth with the user to establish.
- **Reference, don't duplicate.** If a result is long (a full dataset, a drafted chapter, generated code), save it as its own file and point to it in the checkpoint rather than pasting it in. The checkpoint should stay short enough to read in a few seconds; the new session can open a referenced file only if the next step actually needs it.
- **Write decisions down even if they seem obvious right now** — they won't be obvious to a session that wasn't there when the user corrected you or picked an option.
- **Keep it current, not exhaustive.** Update it at natural milestones, not after every tool call — a checkpoint that's mildly stale but readable beats one that's perfectly current but took as long to update as the work itself.

## Delivering a checkpoint

- In a plain chat (Claude.ai, the desktop or mobile app, Cowork): write the checkpoint with the file tools, save it under `/mnt/user-data/outputs/`, and present it so the user gets an actual downloadable file — a checkpoint that only exists inside a session about to end doesn't help anyone. Name it something identifiable, e.g. `checkpoint-<task-slug>.md`, so it doesn't get lost among other files if the user has several going.
- In Claude Code, or any task working inside a repo: just keep the checkpoint (e.g. `CHECKPOINT.md` at the repo root, or wherever project notes live) as a normal tracked file and keep it updated. It persists with the project already, and there's no need to package or hand anything over separately.
- Whenever you deliver a checkpoint, tell the user plainly that you did, why, and what to do with it: attach it — plus any files it references — to a new conversation and say something like "continue from the attached checkpoint." A short, literal sentence they can copy-paste into the new chat removes any guesswork.
- If a checkpoint is being saved reactively (context risk, user says they're low on usage) rather than at a planned milestone, say so directly — "I'm saving a checkpoint now so we don't lose progress" — rather than silently trailing off or continuing as if nothing changed.

## Resuming from a checkpoint

When a conversation starts with a checkpoint file (uploaded, or referenced by path), or the user asks to resume:

1. Read the whole file before doing anything else, including any files it references that are actually needed for the immediate next step. Don't reread every referenced file up front "just in case" — that reintroduces the token cost this whole approach exists to avoid.
2. Give a brief one-line confirmation of what you understand the state to be, so the user can correct anything that drifted — but don't re-ask questions the checkpoint already answered.
3. Continue with the first unchecked item in "Remaining steps." Don't restart finished work or re-derive results the checkpoint already recorded.
4. If a referenced file is missing, ask for that specific file rather than treating the whole checkpoint as unusable.
5. Keep updating the same checkpoint (or start a new one, same shape) as the task continues, following the same guidance above.
