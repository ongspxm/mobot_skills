### Debug

Run for bugs, regressions, flakes, failed checks, and wrong behavior.

1. State expected behavior, observed behavior, path, repro.
2. Repro on real surface first; check existing trace/log before guessing.
3. Read callers, tests, logs, recent "git log" or "git blame".
4. Narrow causes with read-only probes. If 2+ approved fixes fail same assumption -> stop, test shared assumption directly, and record failed tries in todo.txt ("REVERT ..."); if root-cause direction changes -> re-pause before widening scope.
5. Pause at gate (spong-mode skill): show root cause (file:line), test + fix diff, checks; wait for "ok to go?".
6. After OK, copy remaining steps to todo.txt via todolist skill; update as you work.
7. Write smallest failing regression test first when cheap local test exists.
8. Make smallest root-cause fix. Never swallow errors or add downstream guards for broken internal state.
9. Rerun original repro and nearby checks, strip debug residue, inspect diff.

Reply with: what broke, root cause (file:line), fix, failing-then-passing repro output, unverified cases.
