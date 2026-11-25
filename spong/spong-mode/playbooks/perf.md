### Perf

Measurable speedups, trace analysis, and metric hillclimb.

1. Copy these steps to todo.txt via todolist skill, update it as you work thru the steps.
2. Set one metric, better direction, stop predicate, and regression gate before edits.
3. Capture baseline and verify harness repeats clean (median of N runs, error count, work count). Dump large traces to sqlite or script to find hot frames (file:line).
4. Log every try in worklog.tsv via log-work skill (decision, hypothesis, before->after artifact, kept or reverted).
5. Try fixes in mantra order, cheapest first:
   1. Skip unused work.
   2. Cache repeated work.
   3. Do less work per item.
   4. Defer work until needed.
   5. Move work off critical path.
   6. Run concurrently (split shared state first).
   7. Optimize hot algorithm or data layout.
6. Loop one hypothesis per change: measure after -> keep and commit only if past noise and gate stays green; else revert full.
7. On plateau, switch category or re-read trace; never relax stop predicate.

Reply with: metric and target, baseline to final delta, kept vs reverted tries, worklog.tsv path, next idea.
