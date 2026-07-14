# RESEARCH DECISION RECORD (RDR)

```markdown
---
type: rdr
title: "<Hypothesis or idea name>"
tags: [<list, match tags in docs/index.md>]
timestamp: <ISO 2026-07-09T09:38:26Z string>
---

# [Hypothesis or Idea Name]

## 1. Context & Hypothesis

- **Question:** What problem are you trying to solve?
- **Hypothesis:** "If I try [X], then [Y] will happen because [Z]."
- **Success signal:** What result would support or reject it?
- **Prior work:** [Related RDR, issue, paper, or ADR]

## 2. Experiments Tried

### Attempt A: [Short Description]

- **When / owner:** [Date] / [Person or agent]
- **What I did:** [Change, method or code path, key inputs and controls]
- **Evidence:** [Raw data, output, commit, notebook, or analysis link]
- **Result:** [Data, error message, or metric]
- **Takeaway:** [Supported | Refuted | Inconclusive] - why?
- **Deviation:** [Unexpected condition or `None`]

### Attempt B: [Next Iteration]

- **When / owner:** [Date] / [Person or agent]
- **What I did:** [Change, method or code path, key inputs and controls]
- **Evidence:** [Raw data, output, commit, notebook, or analysis link]
- **Result:** [Data, error message, or metric]
- **Takeaway:** [Supported | Refuted | Inconclusive] - why?
- **Deviation:** [Unexpected condition or `None`]

## 3. Final Decision / Current State

- **Status:** [Abandoned | Paused | Succeeded]
- **Outcome:** What do the findings support, and what did you choose to do?
- **Decision record:** [ADR link, if a final architecture choice was made]

## 4. Next Actions

- [ ] [Owner] Action item 1
- [ ] [Owner] Action item 2
```

# USE

Use one RDR per research thread. Append new attempts in order; do not rewrite failed attempts. Link exact raw evidence so a teammate can reproduce the conclusion. When research produces a final architecture choice, create or update a separate ADR.

# INSTRUCTIONS

1. State a falsifiable hypothesis and success signal before the first attempt when possible.
2. Record each attempt while work is fresh. Include inputs, controls, exact code or protocol revision, and raw evidence location when relevant.
3. Append corrections as a new note or attempt; do not overwrite earlier observations or results.
4. Mark each result supported, refuted, or inconclusive. Record deviations, including tool, environment, or equipment failures.
5. Set the current status and outcome after each meaningful conclusion. Keep next actions actionable and owned.
6. Create `$REPO_ROOT/docs/research/YYYY-MM-DD-<slug>.md`, unless the repository has a different registered research location.
