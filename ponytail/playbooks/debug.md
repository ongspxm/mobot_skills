# Debug

Use for bugs, regressions, flakes, failed checks, and unexpected results.

1. State expected behavior, observed behavior, path, and reproduction.
2. Read code, callers, tests, logs, and recent history.
3. Reproduce before editing when possible.
4. Trace the symptom to its root cause.
5. Read `tools/tdd.md` from the skill directory when a cheap regression test is practical.
6. Make the smallest root-cause fix. Do not hide failures with guards or fallbacks unless intended.
7. Rerun the reproduction and nearby checks.
8. Remove debugging residue and inspect the diff.

If reproduction fails, record what was tried and use the closest executable check. Report before evidence, cause, fix, after evidence, and unverified conditions.
