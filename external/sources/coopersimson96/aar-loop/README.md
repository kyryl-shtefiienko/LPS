# AAR Loop

A human-run version of Reflexion for AI agents, built on a military method that's been standard practice for fifty years.

Run `/aar-loop` after any task or session. It does three things:

1. **Reviews the session** with the US Army's 4-question After Action Review.
2. **Finds what's worth fixing** and writes the improvement straight into your skills or rules files, so the fix is there before you need it again, not just written down somewhere.
3. **Saves the lessons** to a persistent LESSONS.md file that your AI loads next time.

Point the next session at that file (and at whatever skill or rule got patched) and the agent stops repeating the same mistake. Run it every session and the agent compounds instead of restarting from zero each time.

## Where the method comes from

The US Army formalized the After Action Review in the mid-1970s, in the years after Vietnam, as a structured debrief for training exercises. It became official doctrine in 1993 with field manual TC 25-20, and it's still run after every rotation at the National Training Center, Fort Irwin, one of the most realistic combat training environments in the world. Fifty years of continuous use on one method, because the mechanism is simple and hard to argue with: separate the debrief from blame, ask what was supposed to happen versus what actually happened, and the gap tells you exactly what to fix before the next fight.

The 4 questions, verbatim:

1. What was supposed to happen?
2. What actually happened?
3. Why was there a difference?
4. What do we do the same or differently next time?

## The research parallel

This is also, functionally, a manual version of **Reflexion** (Shinn et al., 2023, [arXiv:2303.11366](https://arxiv.org/abs/2303.11366)): an agent framework where a model generates a verbal self-reflection after a failed attempt, stores it in an episodic memory buffer, and carries it into the next attempt. Reflexion agents that keep their reflections outperform agents that start every attempt from scratch.

Nobody's wired that loop into your AI harness by default. This skill is the manual version: you run the reflection step yourself, once per session, and LESSONS.md is the buffer. Same idea, no automation, and it costs you five minutes.

## Install

Paste this into Claude Code, Codex, or your AI harness:

> Install this skill globally: https://github.com/coopersimson96/aar-loop

## Use

```
/aar-loop
```

or just say "run an aar" after finishing something. Sample output:

```
AAR · production deploy

1. What was supposed to happen?
   Deploy the new build and have all three services (web, worker,
   scheduler) come up on the new version.

2. What actually happened?
   The deploy script reported success and exited 0. Web and worker were on
   the new version, but the scheduler was still running the old one; it had
   never actually restarted.

3. Why was there a difference?
   The deploy script only checks the exit code of the restart command, not
   the running version of each service afterward. The restart command for
   the scheduler returned success even though the process manager skipped
   it because it thought the service was already healthy.

4. What do we do the same or differently next time?
   Never trust a deploy script's exit code alone; after any deploy, check
   the actual running version on every service it touches, not just the
   ones it printed a success line for.

FIX PLAN
1. Target: CLAUDE.md
   Add rule: "After any deploy, verify the running version on every service
   it touched. Do not trust the deploy script's exit code alone."
2. Target: skills/deploy/SKILL.md, step 6
   Insert a post-deploy check: query each service's running version and
   compare it against the build hash before reporting the deploy as done.

Apply these fixes? (approve, or say "apply"/"fix it" next time to skip the ask)

Lesson written to LESSONS.md:
  ## 2026-07-24 -- Never trust a deploy script's exit code alone; check the running version on every service it touches after a deploy.
  - Expected: All three services (web, worker, scheduler) run the new build after deploy.
  - Actual: Deploy script exited 0 but the scheduler stayed on the old version.
  - Why: The script checks restart-command exit codes, not the actual running version per service.
  - tags: deploy,verification,fix-applied
```

Once the fix plan is approved, CLAUDE.md and the deploy skill get the new rule directly, and the next deploy AAR starts from a checklist that already checks running versions, not exit codes. Even without the fix plan applied, the next session still reads LESSONS.md (pointed to from CLAUDE.md or AGENTS.md), sees this entry, and checks the running version on every service without being told.

## Files

1. `SKILL.md` -- the 4-question method, how to extract a concrete lesson, how to turn a lesson into a fix plan and apply it on approval, and how to write and load lessons.
2. `scripts/append_lesson.py` -- appends a dated, structured lesson to LESSONS.md, and lists existing lessons so the same one doesn't get written twice. Stdlib only.

## What this is, and isn't

It's a disciplined reflection-and-write habit, not automatic learning. It proposes, and on approval writes, changes to the skills, rules, and lessons files you load, not the model itself. Nothing here retrains anything or changes model weights, and it runs after the session ends: the fix takes effect starting next time, not mid-session and not in real time. A proposed fix only helps once it's actually applied and actually loaded.

It only compounds if the lessons are specific enough to check ("batch size over 100 fails with a timeout") instead of vague ("write better code"), fix plans name an exact file and an exact edit instead of a vague intention, and something actually reads the file before the next relevant task. All three are on you.

## License

MIT.
