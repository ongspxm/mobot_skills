### Custom Flow

Large, multi-phase, or cross-cutting work where no single playbook fits.

1. Gather full context: read AGENTS.md, entry points, callers, constraints, and external docs (playbooks/research.md if needed).
2. Split work into small ordered slices or PRs with explicit deps and disjoint files.
3. Write plan and dep graph in todo.txt (todolist skill); log key forks in worklog.tsv (log-work skill).
4. Ask "ok to go?" on slice split before editing.
5. Run each slice with matching core playbook (playbooks/design.md, playbooks/implement.md, playbooks/refactor.md, playbooks/debug.md). Run independent slices in separate gwtadd worktrees; never share mutable files across parallel workers.
6. Verify unit and live behavior per slice before starting next.
7. Run playbooks/review.md per slice and leave worktrees open for user review; fix any comments in the slice worktree.
8. After user OK, merge slices back using merge-worktree skill (handles gwtdel cleanup).

Reply with: slice graph, status per slice, check evidence, open items.
