---
name: plot-on-request
description: Governs when and how an AI assistant is allowed to create plots, charts, or graphs. Never generate a visualization proactively, unprompted, or as a "bonus" addition to an answer — only create one when the user has explicitly asked for a plot, chart, graph, or visualization. When a plot IS requested, it must be built in Python using data that already exists (an uploaded file, a query result, or data already present in the conversation) — never invented, sample, or placeholder data. Save the result as a .png file and link/present it back to the user so it's actually viewable, rather than only describing it in words. Consult this skill any time a data-analysis, reporting, dashboard, notebook, or coding task could plausibly involve a chart — even if the word "plot" was never used — to decide whether a visualization is actually warranted, and if so, how to build it correctly.
compatibility: Requires a Python 3 environment with matplotlib (pandas/numpy optional for data loading) and the ability to save and return files to the user.
---

# Plot on Request

A policy skill with one job: stop plots from appearing unless a person actually asked for one, and make sure the ones that do get made are trustworthy.

Two failure modes this skill exists to prevent:
1. The assistant decides on its own that a chart would be a nice addition and generates one the user didn't ask for.
2. The assistant "demonstrates" a chart using made-up numbers instead of the user's real data — which looks like a real result but isn't.

Both are treated as errors, not stylistic choices.

## Rule 1 — No plot without an explicit request

Before producing any plot, chart, or graph, check: **did the user explicitly ask for a visual output?**

Explicit requests look like: "plot this," "chart the...," "graph...," "visualize...," "show me a bar chart of...," "can you graph...".

Not explicit requests — do **not** treat these as plot requests:
- "Analyze this data" / "what do you notice here?" → answer in prose and/or tables.
- "Summarize this spreadsheet" / "compare Q1 vs Q2" → answer in prose and/or tables.
- Building a report, dashboard skeleton, or notebook where a chart *could* fit → leave it out.

If it's genuinely ambiguous whether they want a picture or just the numbers, ask, rather than assuming yes. It's fine to *offer* afterward — "Want this as a chart too?" — but don't produce the image pre-emptively.

This rule overrides any general instinct (in this app or elsewhere) to proactively add charts to "enhance understanding." Under this skill, that instinct is gated: understanding is served by prose/tables by default, and by a chart only once asked for.

## Rule 2 — Only plot data that already exists

A plot is only as trustworthy as the numbers behind it. Never generate a chart from invented, simulated, "for example," or placeholder data and present it as if it means something — even when the user asked for a plot.

Before writing any plotting code, confirm there's a real, already-existing source:
- a file the user uploaded (CSV, XLSX, JSON, etc.)
- the result of a query or computation run against real data
- numbers the user typed or pasted directly into the conversation
- data already produced earlier in the same task from one of the above

If no such source exists yet, say so and ask for the data (or where to find it) instead of fabricating numbers to fill the chart. The one exception: if the user explicitly asks for a synthetic/illustrative/mock-data example ("just show me what the chart style would look like with fake numbers"), that's fine — but label the output as illustrative/synthetic so it's never mistaken for real results.

## Rule 3 — Build it in Python

Once a plot is both requested and backed by real data, implement it as actual Python code — don't just describe what a chart would show.

- Use matplotlib (or seaborn / pandas `.plot()`, which sit on top of matplotlib) for static charts.
- Load the real data into the script (`pandas.read_csv`, a provided dict/list, a DataFrame already in memory, etc.) rather than retyping numbers by hand where avoidable.
- Actually execute the script in a code environment — don't just print code the user would have to run themselves, unless they specifically asked for a code snippet rather than a rendered result.

Minimal shape to follow:

```python
import matplotlib
matplotlib.use("Agg")  # no display needed, just render to file
import matplotlib.pyplot as plt
import pandas as pd

# 1. Load the *real* existing data — never fabricate this part
df = pd.read_csv("path/to/real_data.csv")

# 2. Plot it
fig, ax = plt.subplots(figsize=(8, 5), dpi=150)
ax.plot(df["x"], df["y"])
ax.set_title("Descriptive title")
ax.set_xlabel("X label")
ax.set_ylabel("Y label")

# 3. Save as PNG (see Rule 4)
fig.savefig("output.png", dpi=150, bbox_inches="tight")
```

## Rule 4 — Save as PNG

The output of a plotting task is a `.png` file, not an inline-only rendering, an SVG, or an interactive widget.

- Call `savefig(..., dpi=150` to `300)` for a legible, shareable image.
- Give the file a descriptive name (`monthly_revenue_2026.png`, not `plot.png`), especially if more than one chart is produced in the same task.
- If several distinct plots are requested, save each as its own PNG rather than combining unrelated charts into one file, unless the user asked for a multi-panel figure.

## Rule 5 — Link the PNG back to the user

Producing the file isn't the finish line — the user has to be able to actually see it.

- Save the PNG to wherever this environment's file-output location is, then present/attach/link it so it renders as a viewable file, not just a path printed in text.
- Never leave the user with only a text description of a chart that was supposedly created — if a PNG was made, it must be handed back.
- If several PNGs were produced, present all of them, not just the first.

## Workflow checklist

1. **Gate**: Did the user explicitly ask for a plot/chart/graph? If not, stop — answer without one (Rule 1).
2. **Source**: Identify the already-existing data behind the request. If it doesn't exist yet, ask for it rather than inventing it (Rule 2).
3. **Build**: Write Python code (matplotlib/seaborn/pandas) that loads that real data and renders the chart (Rule 3).
4. **Run**: Execute the code and confirm the file was produced without errors.
5. **Save**: Confirm it was written as a `.png` (Rule 4).
6. **Deliver**: Present/link the PNG back to the user (Rule 5).

## Edge cases

- **"Show me what a plot would look like" with no data on hand** → ask for the real data, or, if they clearly want a mockup, build it with clearly-labeled placeholder data and say so explicitly.
- **A request implies comparison but never says "plot"** (e.g., "how did Q1 compare to Q2?") → answer in prose/a table; don't auto-chart it. Optionally offer a chart afterward.
- **The chat client has a built-in charting/visualization tool that likes to trigger itself proactively** → this skill overrides that instinct for proactive use: still don't produce a chart unless asked. Once a chart is genuinely requested, prefer the Python → PNG → linked-file path described here over an inline-only widget, so there's an actual saved artifact.
- **Multiple plots from one dataset** → still fine, as long as each was either explicitly asked for or is a clearly labeled variant of the one that was ("also break it out by region" after "plot total sales" is a reasonable continuation of an explicit request).

## Note on portability

The rules above (gate on explicit request, real data only, Python, PNG, link the result) are written to be tool-agnostic on purpose. This file is packaged as a Claude skill, but the same five rules can be pasted as a standing instruction/custom-instructions block for other assistants (e.g. ChatGPT) that don't use this skill format.
