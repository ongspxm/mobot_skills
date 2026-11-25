### Review

Audit code, diffs, plans, or PRs before calling work done.

1. Reconstruct goal, constraints, and intended design before judging code.
2. Read full diff ("git diff" or tuicr) plus callers, types, tests, and boundaries.
3. Check deletion, reuse, native behavior, and simpler shape. Flag one-caller wrappers and speculative flags.
4. Check correctness, edge validation, error paths, secrets, PII, dead code, and debug residue.
5. Run real checks yourself; verify tests check changed outputs, not internals.
6. Check AGENTS.md rules (ASCII-only files, key TODO/HACKY comments, confirmation gate followed).
7. Report findings as blocker, concern, or nit with file:line. Fix blockers only after OK; else report.

Reply with: verdict, findings by severity (file:line), checks run and output, remaining risk.
