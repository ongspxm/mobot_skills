### Debug

Run for bugs, regressions, flakes, failed checks, and wrong behavior.

1. Copy these steps to todo.txt via todolist skill, update it as you work thru the steps.
2. State expected behavior, observed behavior, path, and repro.
3. Repro on real matching surface first. If trace or log already exists, query it before guessing.
4. Read callers, tests, logs, and recent "git log" or "git blame".
5. Binary-search causes with runtime logs or probes. If 2+ fixes fail on same assumption, write assumption down using log-work skill and test it directly.
6. Write smallest failing regression test first when cheap local test exists.
7. Make smallest root-cause fix. Never swallow errors or add downstream guards for broken internal state.
8. Rerun original repro and nearby checks, strip debug residue, inspect diff.

Reply with: what broke, root cause (file:line), fix, failing-then-passing repro output, unverified cases.
