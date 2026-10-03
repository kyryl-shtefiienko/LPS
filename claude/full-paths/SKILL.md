---
name: full-paths
description: Use whenever creating, editing, or referencing any file on the user's machine (plots, scripts, data, logs) - always state its complete absolute path, not just a filename, so the user can open or navigate to it directly.
---

# Always Give Full File Paths

The user wants the complete, absolute path to any file mentioned, created, or
edited - never just a bare filename, a relative path, or an inline preview
alone (even when the content is also shown as an image or rendered inline).

## Rule

Whenever you:
- create a new file (a plot, script, CSV, report, etc.)
- edit an existing file
- reference a file already made earlier in the conversation

State its full absolute Windows path as literal text, e.g.:
`C:\Users\kyryl\OneDrive\Документы\projects\PrecipiTree\results\plots\example.png`

## Why

The user wants to physically open/access files themselves (Explorer, another
tool, a copy-paste), not just see them described or rendered inline. They've
had to ask for this more than once - treat it as a standing default, not a
one-off request.

## How to apply

- Give the path as literal text, not only a clickable link, so it can be
  copied verbatim.
- Repeat the path even if it was already shown earlier in the conversation -
  don't assume the user remembers or scrolled back.
- When work happens on a remote machine (e.g. via SSH/WSL to a cluster) but
  the deliverable is copied back or also exists locally, give the
  Windows-visible path the user can actually open, not the remote path alone.
- Do this by default, without being asked each time.
