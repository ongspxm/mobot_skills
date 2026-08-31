# Implement

Use for behavior changes, refactors, migrations, and focused fixes.

1. Read investigate or design first when the path is unclear.
2. Restate the behavior and smallest sufficient change.
3. Follow local patterns. Reuse before adding helpers, flags, wrappers, or dependencies.
4. Edit one coherent slice and update callers.
5. Delete obsolete code.
6. Add the closest useful test, not coverage theater.
7. Run focused checks and nearby validation when risk warrants it.
8. Read the final diff and simplify it.

Stop and explain if the request is speculative, already satisfied, architecturally undecided, or not verifiable. Report files, behavior, checks, results, and uncertainty.
