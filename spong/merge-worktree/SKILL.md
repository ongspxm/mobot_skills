---
name: merge-worktree
description: Merge a worktree branch into the repository root
---

# merge worktree
1. if you are not in a git worktree, stop and exit
2. identify the main branch to merge into (usually main or develop, use "gwt list" for details), clarify if unclear
3. git commit in current worktree, clean up the commits, concise descriptive titles
4. git cherry-pick them back to the main branch (resolving any conflicts, clarify if necessary)
5. perform gwtdel on current git worktree
