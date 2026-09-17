# Calibration examples

Scores below assume the stated scope. Columns are reasoning, scope, ambiguity, stakes, and novelty. Recommendations assume the relevant choices are available; resolve model names using reference.md.

| Request | R | S | A | Stakes | N | Total | Suggested choice |
|---|---|---|---|---|---|---|---|
| Fix a typo in a draft | 0 | 0 | 0 | 0 | 0 | 0 | Instant, only announce if advice was requested |
| Summarize a short supplied changelog | 0 | 0 | 0 | 0 | 0 | 0 | Instant |
| Rewrite a customer email with clear tone requirements | 0 | 0 | 1 | 1 | 0 | 2 | Instant |
| Write tests for a bounded, documented function | 1 | 1 | 0 | 1 | 0 | 3 | Instant; reassess if behavior is unclear |
| Explain a reproducible bug spanning two functions | 1 | 1 | 1 | 1 | 0 | 4 | Medium |
| Compare three proposals with competing requirements | 1 | 1 | 1 | 1 | 1 | 5 | Medium |
| Refactor a module with interacting dependencies | 1 | 2 | 1 | 1 | 1 | 6 | High |
| Develop an argument for an unfamiliar policy proposal | 1 | 1 | 2 | 1 | 2 | 7 | High |
| Diagnose an unfamiliar production failure | 2 | 1 | 2 | 2 | 1 | 8 | Extra High if available; verify evidence |
| Design a multi-tenant authorization system | 2 | 2 | 2 | 2 | 2 | 10 | Extra High; consider an available Pro model |

## Edge cases

- **Free/Go user, difficult problem:** Recommend Think if offered. Continue without implying that Sol or Pro is available.
- **Plus user, very difficult problem:** Recommend the highest suitable option actually offered, rather than promising Extra High or Pro access.
- **"Use Instant; speed matters":** Honor that choice. Mention a material tradeoff once if necessary, then work.
- **"Is my current model overkill?":** If current settings are unknown, recommend an appropriate setting and state that you cannot compare it to the unseen current selection.
- **Long transcription or bulk formatting:** Length can increase scope without making the task deeply analytical; do not select Pro solely by word count.
- **"Calculate the risk" with no inputs:** Request the necessary inputs. Extra effort cannot recover missing data.
- **Research needing fresh evidence:** Use available research tools and sources. Model choice does not establish that browsing happened.
- **"Which model for this migration?" only:** Recommend a setting; do not begin the migration.
- **Current setup already matches:** Report the fit in one line, without a switching instruction.
- **Follow-up within the same task:** Do not repeat the assessment unless complexity materially changes.
- **User asks for an API model:** Recognize the different product and use current API guidance instead of substituting ChatGPT picker labels.
