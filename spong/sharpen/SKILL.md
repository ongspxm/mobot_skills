---
name: sharpen
description: Deepen a draft prompt before starting work using specialist methods, raw sources, and external checks.
---

# Sharpen

Use on a draft prompt BEFORE starting work when unsure you asked for right depth, source, or proof.
Make prompt deeper, not bigger. Do not execute task; hand back rewritten prompt only.

1. Name 4 things before rewriting:
   - What a top pro in this field does here that prompt skipped.
   - Rawest source material to start from instead of digested summaries.
   - Specific methods and tools they use (examples, non-exhaustive: EXPLAIN ANALYZE on slow SQL, schema/parser diff on config migrations, wire logs or repro tests on races, DOM/screenshots on UI).
   - External check (other than user or agent) that proves result right.
2. Rewrite prompt asking for those steps.
3. Tell agent to prototype any fork an experiment can settle and recommend winner from real output; leave product or preference calls to user.

Reply with: the 4 findings + rewritten prompt.
