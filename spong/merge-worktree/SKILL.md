---
name: merge-worktree
description: Merge a worktree branch into the repository root.
---

# Merge Worktree

1. Not in git worktree -> stop and exit.
2. Find target main branch (usually main or develop; check with "gwt list"). Ask if unclear.
3. Commit in current worktree; clean commits with concise descriptive titles.
4. Cherry-pick commits onto target branch; resolve conflicts or ask if unclear.
5. Remove current worktree with gwtdel.
