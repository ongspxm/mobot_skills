---
name: principle-fix-root-cause
description: Trace failures to the first mismatched expectation. Test shared assumptions before retrying fixes.
---

# Fix Root Cause

Fix the mismatched expectation, not where it surfaced.

- Reproduce first. Ask why until the answer is a mismatched expectation in code or config.
- If 2 or more fixes share an assumption and all fail, write the assumption down and test it directly.
- Valid state -> handle it where it broke. Buggy state -> fix what created it, not downstream guards or swallowed errors.
- Fix every instance of the same fault pattern.
