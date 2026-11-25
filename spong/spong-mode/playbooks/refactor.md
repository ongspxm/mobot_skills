### Refactor

Change structure with zero behavior change. Keep separate from feature or bug edits.

1. Copy these steps to todo.txt via todolist skill, update it as you work thru the steps.
2. Pin current behavior first with characterization test, snapshot, or diff script (typecheck and lint alone not a pin).
3. Name target shape (types, layout, call graph) and confirm it removes branches or invalid states.
4. Delete dead code, inline one-caller wrappers, and shrink mutable state first.
5. Move in small steps, keep pin green after each step.
6. Migrate all callers and delete old API in one wave; keep no compat shims unless required. Check renames in strings, docs, and config.
7. Prove outputs unchanged on real artifact (diff old vs new output or run smoke check).
8. Confirm lower reader load; if diff adds indirection without clearing flow, revert it.
9. Commit deletion separate from reshape, then run playbooks/review.md.

Reply with: structure changed, pin used, equivalence proof, reader-load delta, commits.
