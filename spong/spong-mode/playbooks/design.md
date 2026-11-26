### Design

Run before new abstractions, cross-module changes, data-shape changes, or unclear edits.

1. State goal and non-goals.
2. Check deletion, reuse, stdlib, and native behavior before designing new code.
3. Read current shapes, callers, owners, boundaries, and failure paths.
4. Pick smallest clear data shape and owner (state machine, table, or union over scattered booleans). When adding new requirement, redesign as if it existed from day one instead of bolting it on.
5. Sketch key types, Production and Tests call graphs, and ordered tracer-bullet steps.
6. If reading cant settle real fork, build throwaway prototype in /tmp (no tests, no prod abstractions, label variants behind one switch) and watch real output.
7. Plan errors, logging, caller migration, old-path deletion, and checks.
8. Show mechanical plan (files, diffs, checks) and ask "ok to go?" before editing.

Reply with: chosen shape, rejected options, changed boundaries, check plan, and "ok to go?".
