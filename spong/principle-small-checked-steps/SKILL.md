---
name: principle-small-checked-steps
description: Change one unit, verify it, then proceed. One concern, one commit
---

# Small Checked Steps

Work in small loops: passing state -> one change -> verify -> next step.

- Never start the next step while the current check is failing.
- Run the check even if a script or codemod did the edit.
- Order steps so each proves the next: repro test before fix, delete dead code before refactor, baseline before optimization.
- Commit one concern at a time, not one dump commit or one-file-per-commit.
