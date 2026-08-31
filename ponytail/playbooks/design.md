# Design

Use before new abstractions, cross-module changes, data-model changes, or structural decisions. Skip mechanical edits.

1. State the requirement and non-goals.
2. Run the YAGNI ladder.
3. Read current shapes, callers, owners, boundaries, and failure paths.
4. Choose the smallest clear data shape and owner.
5. Compare 2 or 3 options only when a real fork exists.
6. Decide errors, logging, migration order, and verification.
7. Specify caller migration and old-path deletion. Apply them later in `implement.md`.

Return the choice, rejected alternatives, changed boundaries, and verification plan. Do not manufacture a design exercise.
