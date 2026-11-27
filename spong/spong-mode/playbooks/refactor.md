### Refactor

Change structure with zero behavior change. Keep separate from feature or bug edits.

1. Name target shape (types, layout, call graph) + confirm it cuts branches or invalid states.
2. Find behavior pin (characterization test, snapshot, or diff script; typecheck/lint alone != pin), dead code, wrappers, string/doc/config renames.
3. Pause at gate (spong-mode skill): show target, pin plan, planned deletes/moves, equivalence check; wait for "ok to go?".
4. After OK, copy remaining steps to todo.txt via todolist skill; update as you work.
5. Pin current behavior first.
6. Delete dead code, inline one-caller wrappers, and shrink mutable state first.
7. Move in small steps, keep pin green after each step.
8. Migrate all callers + delete old API in one wave; keep no compat shims unless needed.
9. Prove outputs unchanged on real artifact (diff old vs new output or run smoke check).
10. Check reader load; if diff adds indirection without clearing flow, revert.
11. After OK, commit deletion separate from reshape -> run playbooks/review.md.

Reply with: structure changed, pin used, equivalence proof, reader-load delta, commits.
