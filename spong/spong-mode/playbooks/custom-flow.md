### Custom Flow

Large, multi-phase, or cross-cutting work where no single playbook fits.

1. Read AGENTS.md, entry points, callers, constraints, external docs (playbooks/research.md if needed).
2. Split work into small ordered slices or PRs; list deps and keep files disjoint.
3. Draft slice plan + dep graph.
4. Pause at gate (spong-mode skill): show slices, deps, checks; wait for "ok to go?" before edits.
5. After OK, copy plan to todo.txt via todolist skill.
6. Run each slice with matching core playbook (playbooks/design.md, playbooks/implement.md, playbooks/refactor.md, playbooks/debug.md); each slice keeps its playbook gate unless user approved all slices.
   Split shared state first: give parallel workers own files, keys, or gwtadd worktrees -> merge on read; use lock or single writer only when shared target is real invariant.
7. Verify unit and live behavior per slice before starting next.
8. Run playbooks/review.md per slice and leave worktrees open for user review; fix any comments in the slice worktree.
9. After user OK, merge slices with merge-worktree skill (handles gwtdel cleanup).

Reply with: slice graph, status per slice, check evidence, open items.
