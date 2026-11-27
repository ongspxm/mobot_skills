### Design

Run before new abstractions, cross-module or data-shape changes, or unclear edits.

1. State goal and non-goals.
2. Check deletion, reuse, stdlib, and native behavior before designing new code.
3. Read current shapes, callers, owners, boundaries, and failure paths.
4. Pick smallest clear data shape and owner (state machine, table, or union over scattered booleans). When adding new requirement, redesign as if it existed from day one instead of bolting it on.
5. Sketch key types, Production and Tests call graphs, and ordered tracer-bullet steps.
6. If reading cant settle real fork: draft prototype variants + experiment plan for gate; write no prototype code yet.
7. Plan errors, logs, caller migration, old-path deletion, checks.
8. Pause at gate (spong-mode skill): show files, diffs, checks; ask "pausing here, back to user: ok to go?".
9. After OK, build approved throwaway prototype in /tmp (no tests or prod abstractions; label variants behind one switch) -> inspect real output. If result changes design or scope, re-pause before prod edits.

Reply with: chosen shape, rejected options, changed boundaries, checks, "pausing here, back to user: ok to go?".
