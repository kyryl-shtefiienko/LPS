---
name: git-advanced
description: Use when performing git operations that could rewrite history, discard work, or affect a shared branch — interactive rebase, force-push, reset/clean, branch deletion, conflict resolution, or bisecting for a regression — to apply safe defaults and avoid destructive mistakes.
---

# Advanced Git Operations

## Overview

**Core principle:** Reversible operations are free to attempt. Irreversible ones need a safety net first — a backup ref, a clean working tree, or your human partner's explicit go-ahead.

**Announce at start:** "I'm using the git-advanced skill for this git operation."

## What to do

- Before any history rewrite (`rebase -i`, `commit --amend`, `filter-branch`, BFG): `git branch backup-<name>` first, and confirm `git status` is clean.
- Prefer `git push --force-with-lease` over `--force` — it fails safely if the remote moved since your last fetch, instead of silently clobbering someone else's push.
- Use `git reflog` as the first move to recover ANY "lost" commit, dropped stash, or bad reset — it holds ~90 days of history by default, well past what feels recoverable.
- Keep commits atomic (one logical change) and rebase-clean — squash "wip"/"fix typo" commits before a PR is opened, not after.
- Resolve conflicts by reading both sides first (`git diff --ours`, `git diff --theirs`, `git diff --base`) before picking one — `checkout --ours`/`--theirs` blindly can silently drop the other side's real fix.
- Delete only branches that are `--merged` into whatever you're comparing against; `git fetch --prune` regularly to clear stale remote-tracking refs.
- Bisect with a script (`git bisect run ./test.sh`) whenever the pass/fail check is scriptable — faster, and removes manual-judgment error from the loop.
- Pick a branch strategy deliberately and match the team's cadence: trunk-based (short-lived branches, frequent integration) for fast-moving/CI-heavy teams; Git Flow (`develop`/`release/*`/`hotfix/*`) for scheduled releases with multiple live versions. See `examples/branch_strategies.md`.

## What NOT to do

- **Never rewrite history on a branch anyone else may have pulled** (`rebase`, `commit --amend`, `filter-branch`, `push --force`) — it strands their local history, and both `--force-with-lease` and their next pull turn painful. Confirm with your human partner before rewriting anything already pushed to a shared branch.
- **Never force-push to `main`/`master`** (or any branch protected/shared by convention) — if a force-push is genuinely needed there, that's a conversation with your human partner first, not a unilateral call.
- **Never run `git reset --hard`, `git clean -f`, `git checkout -- .` / `git restore .`, or force-delete a branch (`-D`)** without running `git status` first and confirming nothing uncommitted is about to be discarded.
- **Never skip hooks** (`--no-verify`) or bypass signing (`--no-gpg-sign`) to get past a failing check — fix the underlying issue, or ask if the check itself is wrong.
- **Never resolve a conflict by guessing** — a blind `--ours`/`--theirs` pick is a last resort for genuinely equivalent changes, not a way to make the conflict marker go away faster. Test after resolving; don't assume the merge is correct because it compiles.
- **Don't leave a rebase or merge half-finished** — `git rebase --abort` / `git merge --abort` and re-approach, rather than leaving the repo in a conflicted, uncommittable state across a session boundary.

## Quick Command Reference

### Interactive rebase

```bash
git rebase -i HEAD~5          # last 5 commits
git rebase -i main            # onto main
git rebase --continue         # after resolving a conflict
git rebase --abort            # bail out, back to original state
```

Rebase-editor verbs: `pick` (keep) · `reword` (keep, edit message) · `edit` (keep, stop to amend) · `squash` (combine, keep message) · `fixup` (combine, discard message) · `drop` (remove). Full walkthrough: `examples/interactive_rebase.md`.

### Conflicts

```bash
git status                         # list conflicted files
git diff --ours / --theirs / --base <file>
git checkout --ours|--theirs <file>  # only after reading both sides
git add <file>                     # mark resolved
git merge --continue   # or: git rebase --continue
git mergetool           # if a configured merge tool is preferred
```

More patterns: `examples/conflict_resolution.md`.

### Bisect

```bash
git bisect start
git bisect bad
git bisect good <known-good-commit>
git bisect run ./test-script.sh   # or step manually: good/bad per commit
git bisect reset
```

### Cherry-pick

```bash
git cherry-pick <commit>
git cherry-pick -n <commit>   # apply without committing
git cherry-pick A^..B         # range
```

### Reflog recovery

```bash
git reflog                         # view history, including "lost" states
git checkout -b recovery <commit>  # recover a dangling commit
git reset --hard HEAD@{N}          # undo a bad reset/rebase
git fsck --lost-found              # find fully dangling commits
```

Full recovery techniques: `references/reflog-recovery.md`.

### Branch cleanup

```bash
git branch --merged main | grep -v "\*\|main\|develop" | xargs git branch -d
git fetch --prune
bash scripts/git_helper.sh cleanup-branches   # scripted equivalent
```

Strategy detail: `references/branch-management.md`. Comprehensive best practices: `references/best-practices.md`.

## Common Rationalizations

| Excuse | Reality |
|---|---|
| "It's just my branch, no one else has it" | Confirm no one has fetched it. Once it's pushed, someone might have — `--force-with-lease` costs nothing when you're right and saves you when you're wrong. |
| "`--force` is faster than `--force-with-lease`" | Same speed in the safe case; `--force` additionally clobbers a remote that moved. There's no upside to the plain flag. |
| "The conflict is obviously just formatting, I'll take theirs" | Read the diff first. An "obvious" conflict has silently dropped real fixes before — `--theirs` doesn't know which side is right, only which side you picked. |
| "Tests passed before the rebase, so they still pass" | A rebase replays commits on new history; run the suite again on the result before trusting it. |
| "`--no-verify` just this once, the hook is being annoying" | If the hook is wrong, fix or disable it properly. If it's right, it just caught something real. |
| "I'll clean up unmerged branches too, they look stale" | `--merged` is the check for a reason — an unmerged branch may hold work that exists nowhere else. |

## Troubleshooting

- **Rebase conflicts too complex to untangle:** `git rebase --abort`, then reconsider — a `git merge --no-ff <branch>` is sometimes the simpler path.
- **Lost commits:** `git reflog` first, always — then `git checkout -b recovery <commit-hash>`.
- **Detached HEAD:** `git checkout -b new-branch-name` to keep the work, or `git checkout main` to abandon it.
- **Push rejected after a rebase:** confirm the branch isn't shared, then `git push --force-with-lease` — never plain `--force`. If it's shared, push a new branch instead: `git push origin HEAD:feature-v2`.

Full guide: `references/troubleshooting.md`.

## Additional Resources

- `examples/interactive_rebase.md`, `examples/conflict_resolution.md`, `examples/branch_strategies.md` — worked scenarios.
- `references/branch-management.md`, `references/reflog-recovery.md`, `references/best-practices.md`, `references/troubleshooting.md` — full reference detail.
- `scripts/git_helper.sh` — branch cleanup and conflict-resolution utilities.
