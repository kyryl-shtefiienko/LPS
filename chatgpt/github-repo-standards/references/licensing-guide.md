# Licensing guide

## Why this file exists, and why it's not optional

Publishing code on GitHub without a LICENSE file does **not** put it in the public domain. Default copyright applies: legally, nobody else has permission to use, copy, modify, or distribute it — even though they can see and clone it. A public repo with no LICENSE is a display case, not an invitation. If the goal is for other people to actually use the code, a license is what grants that permission. This is the single most common and most consequential gap `validate_repo.py` checks for.

The other end of the same mistake: don't pick a license as an afterthought and then contradict it in the README ("feel free to use this, just don't sell it" next to an MIT license, which permits exactly that). The LICENSE file is the actual legal grant; anything in the README should be consistent with it, not layer on extra restrictions informally.

None of this is legal advice, and this skill isn't a substitute for a lawyer on anything beyond picking a standard, common OSI license for a straightforward project.

**Research/academic software:** if `references/research-software.md` applies to this repo, its default is **GPL-3.0-or-later**, not MIT — that profile overrides the "maximum adoption" default below based on a consistently observed pattern in published research-software repos. Everything else on this page (the decision guide, the comparison table, how to apply it) still applies; only the default choice changes.

## Decision guide

Answer these roughly in order:

1. **Is this closed-source / internal / proprietary?**
   Don't add an open-source LICENSE file at all. Either leave it unlicensed (default copyright, all rights reserved — correct for private repos) or add a short proprietary notice if the repo might ever be seen outside the org. Keep the repo **private**.

2. **Do you want essentially no restrictions, maximum adoption, including by proprietary/commercial software?**
   → **MIT** (shortest, most widely recognized, most permissive-and-simple) or **Apache-2.0** (also permissive, but adds an explicit patent grant and a NOTICE mechanism — better fit if patents are a realistic concern, e.g. anything touching hardware, codecs, or ML methods).

3. **Do you want derivative works to stay open source under the same terms (copyleft)?**
   → **GPL-3.0** for strong copyleft (anything distributing a derivative work must also be GPL and source-available). → **LGPL-3.0** if it's a library you want usable by proprietary software while keeping the library itself copyleft. → **MPL-2.0** for file-level copyleft (modified files must stay open, but it can be combined with proprietary code in the same project more easily than GPL).

4. **Do you want to place it as close to public domain as license law allows?**
   → **Unlicense** or **MIT-0** (MIT without the attribution requirement). Avoid CC0 for code specifically — it was written for creative works and has patent/warranty gaps that matter more for software; Unlicense or MIT-0 are the code-appropriate equivalents.

5. **Is this documentation or creative content, not code?**
   → Creative Commons (commonly **CC-BY-4.0** or **CC-BY-SA-4.0**) is the right family for docs, articles, or media — not a software license.

## Comparison table

| License | Permissive/Copyleft | Patent grant | Must disclose source of modifications | Good for |
|---|---|---|---|---|
| MIT | Permissive | No | No | Default choice for most projects wanting maximum adoption |
| Apache-2.0 | Permissive | Yes, explicit | No | Same as MIT, plus real patent exposure (ML, hardware, codecs) |
| BSD-3-Clause | Permissive | No | No | Similar to MIT; common in academic/research code |
| MPL-2.0 | Weak copyleft | Yes | Only modified files | Libraries that want to stay open but be embeddable in proprietary apps |
| LGPL-3.0 | Weak copyleft | Yes | Only the library itself | Libraries meant to be linked by proprietary software |
| GPL-3.0 | Strong copyleft | Yes | Yes, whole derivative work | Projects that want all downstream use to stay open source |
| Unlicense / MIT-0 | Public-domain-equivalent | No | No | Maximum freedom, no attribution requirement |
| (none / all rights reserved) | N/A | N/A | N/A | Closed-source, internal, or "look but don't use" repos |

## Getting the exact text

License text must be exact — never paraphrase or retype from memory. `scripts/init_repo.py --license <key>` fetches the canonical text live from GitHub's license API (`api.github.com/licenses/<key>`) and substitutes in the year and copyright holder. If that's not available, get it directly from https://choosealicense.com/licenses/<key>/.

## Applying it correctly

- Put the full license text in a `LICENSE` (no extension) or `LICENSE.md` file at the repo root — this is what GitHub detects and displays in the repo sidebar.
- Also declare it in the package manifest so tooling picks it up automatically: `"license": "MIT"` in `package.json`, `license = "MIT"` in `pyproject.toml`, etc.
- For copyleft licenses (GPL/LGPL family), source files conventionally carry a short header comment with the license notice — check the license's own "how to apply" appendix for the exact recommended wording.
- If the project depends on other packages, and the chosen license is copyleft, check that dependencies' licenses are actually compatible (e.g. a GPL-3.0 project generally cannot depend on Apache-2.0-only code in a way that creates a combined GPL-incompatible work in some interpretations — this is exactly the kind of edge case to flag rather than resolve unilaterally).

## Common mistakes

- No LICENSE at all on a public repo the author wants others to use — the most common gap, and the one with the most real consequence.
- Picking GPL for a library, then being surprised nobody in the (often permissively-licensed) ecosystem it targets can adopt it.
- Editing the license text itself (adding clauses, removing the warranty disclaimer) — this creates an unclear, likely-unenforceable custom license instead of the well-understood standard one.
- Choosing a license and then contradicting its terms informally elsewhere (README, CONTRIBUTING) — the LICENSE file governs; keep other docs consistent with it rather than layering on ad hoc restrictions.
