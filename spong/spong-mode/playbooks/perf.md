### Perf

Measurable speedups, trace analysis, and metric hillclimb.

1. Copy these steps to todo.txt via todolist skill, update it as you work thru the steps.
2. Set one metric, better direction, stop predicate, and regression gate before edits.
3. Capture baseline and vet every number before acting or reporting:
   - Profile an unmeasured run to name the limiter ("why not double?").
   - Match prod tuning on both sides (release flags, warm/cold cache, batching, same data).
   - Check math against hardware/time limits (cutting a 10% step cannot save 50%).
   - Count errors and verify work actually ran in timed window (not cached, lazy, or dropped).
   - Run >=5 interleaved A/B/A/B samples; report median and spread (delta < spread = inconclusive). Use 1 run only for quick ballpark and label it.
   - Report micro speedup alongside share of full end-to-end user path.
   - Dump large traces to sqlite or script to find hot frames (file:line).
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

Reply with: metric and target, baseline to final delta, run count + spread, limiter, kept vs reverted tries, worklog.tsv path, next idea.
