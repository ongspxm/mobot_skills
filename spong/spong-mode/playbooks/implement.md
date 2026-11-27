### Implement

Run for approved behavior changes, features, and focused edits.

1. Read target files + callers (run playbooks/investigate.md or playbooks/design.md if path/shape unclear); draft exact prose/diff + checks.
2. Pause at gate (spong-mode skill): show draft/diff + checks; wait for "ok to go?".
3. After OK, copy steps to todo.txt via todolist skill; update as you work. Use gwtadd when isolation helps.
4. Delete dead code + unused paths first; reuse existing code + stdlib before new helpers or deps.
5. Build one tracer-bullet slice end to end, then edge cases. Keep core pure; validate at edges.
6. Read principle-test-outputs-not-guts skill -> add focused tests on observable outputs, not internals.
7. Run real checks on matching surface (command, UI, CLI, tests).
8. Strip slop + unused comments; keep "TODO:" and "HACKY:" intact; split commits by concern ("feat/fix/chore/docs: component. desc").
9. Run playbooks/review.md before handoff. If using worktree, leave open for review + fix comments there; run merge-worktree skill only after user OK.

Reply with: what changed, checks run and real output, remaining risk, commits/branch/git status.
