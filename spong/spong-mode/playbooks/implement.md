### Implement

Run for approved behavior changes, features, and focused edits.

1. Run playbooks/investigate.md or playbooks/design.md first if path or shape unclear; wait for "ok to go?".
2. Copy these steps to todo.txt via todolist skill, update it as you work thru the steps. Use gwtadd when isolation helps.
3. Delete dead code and unused paths first. Reuse existing code and stdlib before adding helpers or deps.
4. Build one tracer-bullet slice end to end, then edge cases. Keep core pure, validate at edges.
5. Add focused tests on observable outputs, not internals.
6. Run real checks on matching surface (command, UI, CLI, tests).
7. Strip slop and unused comments, keep "TODO:" and "HACKY:" intact, split into cohesive one-concern commits ("(feat|fix|chore|docs): component. desc").
8. Run playbooks/review.md before handoff. If using worktree, leave it open for user review and fix any comments there; run merge-worktree skill only after user OK.

Reply with: what changed, checks run and real output, remaining risk, commits/branch/git status.
