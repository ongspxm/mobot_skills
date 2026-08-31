# TDD

Use when requested or when a bug has a cheap local test path. Do not force brittle or expensive tests.

1. Identify intended behavior and the smallest reproduction.
2. Choose the closest existing test path.
3. Write the focused regression test.
4. Run it before the fix and confirm the intended failure.
5. Make the smallest fix.
6. Rerun it and nearby checks.

If a failing test is impractical, explain why and use the closest executable check. Report before failure, after pass, nearby validation, and missing evidence.
